from abc import ABCMeta, abstractmethod
from datetime import datetime, timezone
from typing import Generic, Type, TypeVar

from exceptions import DatabaseException, RecordNotFoundException
from models import BaseModel
from schemas import BaseSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE", bound=BaseModel)


class BaseRepository(Generic[IN_SCHEMA, SCHEMA, TABLE], metaclass=ABCMeta):
    @property
    @abstractmethod
    def _table(self) -> Type[TABLE]: ...

    @property
    @abstractmethod
    def _schema(self) -> Type[SCHEMA]: ...

    def create(self, item_input: IN_SCHEMA) -> SCHEMA:
        try:
            item = self._table(**item_input.dict())
            item.save()
            return self._schema(**item.attribute_values)
        except Exception as e:
            raise DatabaseException(e)

    def list(self, *args) -> SCHEMA:
        try:
            items = self._table.query(*args)
            return [self._schema(**item.attribute_values) for item in items]
        except Exception as e:
            raise e

    def get(self, *args) -> SCHEMA:
        try:
            item = self._table.get(*args)
            return self._schema(**item.attribute_values)
        except self._table.DoesNotExist as e:
            raise RecordNotFoundException(e)
        except Exception as e:
            raise DatabaseException(e)

    def update(self, updated_item: SCHEMA, *args) -> SCHEMA:
        try:
            item = self._table.get(*args)
            updated_data = {**item.attribute_values, **updated_item.dict(exclude_unset=True)}
            updated_data["updated_at"] = datetime.now(timezone.utc)
            new_item = self._table(**updated_data)
            new_item.save()
            return self._schema(**new_item.attribute_values)
        except self._table.DoesNotExist as e:
            raise RecordNotFoundException(e)
        except Exception as e:
            raise DatabaseException(e)

    def delete(self, *args) -> None:
        try:
            item = self._table.get(*args)
            item.delete()
        except self._table.DoesNotExist as e:
            raise RecordNotFoundException(e)
        except Exception as e:
            raise DatabaseException(e)
