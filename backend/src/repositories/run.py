from typing import Type

from models import TestRunTable
from schemas import TestRunDB, TestRunDBInput

from .base import BaseRepository


class TestRunRepository(BaseRepository[TestRunDBInput, TestRunDB, TestRunTable]):
    @property
    def _in_schema(self) -> Type[TestRunDBInput]:
        return TestRunDBInput

    @property
    def _schema(self) -> Type[TestRunDB]:
        return TestRunDB

    @property
    def _table(self) -> Type[TestRunTable]:
        return TestRunTable
