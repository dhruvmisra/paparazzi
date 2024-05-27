from typing import Type

from models import TestTable
from schemas import TestDB, TestDBInput

from .base import BaseRepository


class TestRepository(BaseRepository[TestDBInput, TestDB, TestTable]):
    @property
    def _in_schema(self) -> Type[TestDBInput]:
        return TestDBInput

    @property
    def _schema(self) -> Type[TestDB]:
        return TestDB

    @property
    def _table(self) -> Type[TestTable]:
        return TestTable
