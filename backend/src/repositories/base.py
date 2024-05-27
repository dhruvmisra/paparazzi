from abc import ABCMeta, abstractmethod
from typing import Any, Generic, List, Optional, Tuple, Type, TypeVar

from sqlalchemy import Column, delete, desc, func, select, update
from sqlalchemy.engine import CursorResult, Result
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from constants import CursorPrefix
from exceptions import (
    ApplicationException,
    DatabaseException,
    RecordIntegrityException,
    RecordNotFoundException,
)
from models import Base
from schemas import BaseSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE", bound=Base)


class BaseRepository(Generic[IN_SCHEMA, SCHEMA, TABLE], metaclass=ABCMeta):
    def __init__(self, db_session: AsyncSession, *args, **kwargs) -> None:
        self._db_session: AsyncSession = db_session

    @property
    @abstractmethod
    def _table(self) -> Type[TABLE]:
        ...

    @property
    @abstractmethod
    def _schema(self) -> Type[SCHEMA]:
        ...

    async def create(self, in_schema: IN_SCHEMA) -> SCHEMA:
        try:
            entry = self._table(**in_schema.dict())
            await entry.save(self._db_session)
            return self._schema.from_orm(entry)
        except IntegrityError as e:
            raise RecordIntegrityException(e)
        except Exception as e:
            raise DatabaseException(e)

    async def count(
        self,
        where: Optional[List] = None,
        **filter_query: Any,
    ) -> int:
        try:
            q = select(func.count()).select_from(self._table)

            if where:
                q = q.where(*where, self._table.is_deleted == False)  # NOSONAR  # noqa
            else:
                q = q.filter_by(**filter_query, is_deleted=False)

            q = q.order_by(None)
            result: Result = await self._db_session.execute(q)
            count = result.scalars().one()
            return count
        except Exception as e:
            raise DatabaseException(e)

    async def list(
        self,
        where: Optional[List] = None,
        order_by: Optional[List] = None,
        limit: int = -1,
        load_relationships: Optional[List] = None,
        raise_if_no_records: bool = False,
        **filter_query: Any,
    ) -> list[SCHEMA]:
        try:
            q = select(self._table)

            if where:
                q = q.where(*where, self._table.is_deleted == False)  # NOSONAR  # noqa
            else:
                q = q.filter_by(**filter_query, is_deleted=False)

            if load_relationships:
                q = q.options(*load_relationships)

            if order_by:
                q = q.order_by(*order_by)

            if limit > 0:
                q = q.limit(limit)

            result: Result = await self._db_session.execute(q)
            entries = result.scalars().all()
            if len(entries) == 0:
                raise NoResultFound(f"{self._table.__name__}<{filter_query}> not found")
            return [self._schema.from_orm(entry) for entry in entries]
        except NoResultFound as e:
            if raise_if_no_records:
                raise RecordNotFoundException(e)
            else:
                return []
        except Exception as e:
            raise DatabaseException(e)

    async def list_with_pagination(
        self,
        where: List,
        limit: int,
        cursor_prefix: Optional[CursorPrefix],
        cursor_value: Optional[Any],
        cursor_field: Column,
        order_by: List = [],
        load_relationships: Optional[List] = None,
        raise_if_no_records: bool = False,
    ) -> Tuple[List[SCHEMA], int, bool]:
        try:
            paginated_where = [*where]
            paginated_order_by = [*order_by]

            if cursor_prefix == CursorPrefix.NEXT:
                paginated_order_by.append(cursor_field)
                paginated_where.append(cursor_field > cursor_value)
            elif cursor_prefix == CursorPrefix.PREV:
                paginated_order_by.append(desc(cursor_field))
                paginated_where.append(cursor_field < cursor_value)

            count = await self.count(where=where)
            entries = await self.list(
                where=paginated_where,
                limit=limit + 1,
                order_by=paginated_order_by,
                load_relationships=load_relationships,
                raise_if_no_records=raise_if_no_records,
            )

            has_more_entries = False
            if len(entries) == limit + 1:
                has_more_entries = True
                entries.pop()

            if cursor_prefix == CursorPrefix.PREV:
                entries.reverse()

            return entries, count, has_more_entries
        except ApplicationException:
            raise
        except Exception as e:
            raise DatabaseException(e)

    async def get(
        self,
        where: Optional[List] = None,
        load_relationships: Optional[List] = None,
        **filter_query: Any,
    ) -> SCHEMA:
        try:
            q = select(self._table)
            if where:
                q = q.where(*where, self._table.is_deleted == False)  # NOSONAR  # noqa
            else:
                q = q.filter_by(**filter_query, is_deleted=False)

            if load_relationships:
                q = q.options(*load_relationships)

            result: Result = await self._db_session.execute(q)
            entry = result.scalars().one()
            if not entry:
                raise NoResultFound(f"{self._table.__name__}<{filter_query}> not found")
            return self._schema.from_orm(entry)
        except NoResultFound as e:
            raise RecordNotFoundException(e)
        except Exception as e:
            raise DatabaseException(e)

    async def update(
        self,
        updated_schema: Optional[SCHEMA] = None,
        values: dict = {},
        where: Optional[List] = None,
        load_relationships: Optional[List] = None,
        **filter_query: Any,
    ) -> SCHEMA:
        try:
            q = update(self._table)
            if where:
                q = q.where(*where, self._table.is_deleted == False)  # NOSONAR  # noqa
            else:
                q = q.filter_by(**filter_query, is_deleted=False)

            if updated_schema:
                q = q.values(**updated_schema.dict())
            else:
                q = q.values(**values)

            cursor_result: CursorResult = await self._db_session.execute(q)
            if cursor_result.rowcount == 0:
                raise NoResultFound(f"{self._table.__name__}<{filter_query}> not found")
            await self._db_session.commit()

            q = select(self._table)
            if where:
                q = q.where(*where, self._table.is_deleted == False)  # NOSONAR  # noqa
            else:
                q = q.filter_by(**filter_query, is_deleted=False)

            if load_relationships:
                q = q.options(*load_relationships)
            result: Result = await self._db_session.execute(q)
            # Switched to first() to make sure we only return one record
            # TODO: Will switch to support a list later
            entry = result.scalars().first()
            return self._schema.from_orm(entry)
        except NoResultFound as e:
            raise RecordNotFoundException(e)
        except Exception as e:
            raise DatabaseException(e)

    async def delete(
        self,
        where: Optional[List] = None,
        permanent_operation: bool = False,
        **filter_query: Any,
    ) -> None:
        try:
            if permanent_operation:
                q = delete(self._table)
                if where:
                    q = q.where(*where, self._table.is_deleted == False)  # NOSONAR  # noqa
                else:
                    q = q.filter_by(**filter_query, is_deleted=False)

                await self._db_session.execute(q)
            else:
                q = select(self._table)
                if where:
                    q = q.where(*where, self._table.is_deleted == False)  # NOSONAR  # noqa
                else:
                    q = q.filter_by(**filter_query, is_deleted=False)

                result: Result = await self._db_session.execute(q)
                entries = result.scalars().all()
                if len(entries) == 0:
                    raise NoResultFound(f"{self._table.__name__}<{filter_query}> not found")
                for entry in entries:
                    await entry.delete(self._db_session)
            return None
        except NoResultFound as e:
            raise RecordNotFoundException(e)
        except Exception as e:
            raise DatabaseException(e)
