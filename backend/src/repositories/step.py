from typing import Type

from models import TestStepTable
from schemas import TestStepDB, TestStepDBInput

from .base import BaseRepository


class TestStepRepository(BaseRepository[TestStepDBInput, TestStepDB, TestStepTable]):
    @property
    def _in_schema(self) -> Type[TestStepDBInput]:
        return TestStepDBInput

    @property
    def _schema(self) -> Type[TestStepDB]:
        return TestStepDB

    @property
    def _table(self) -> Type[TestStepTable]:
        return TestStepTable
