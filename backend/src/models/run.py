from pynamodb.attributes import JSONAttribute, ListAttribute, MapAttribute, UnicodeAttribute

from util.id import generate_test_run_id

from .base import BaseModel


class TestResultStep(MapAttribute):
    test_step_id = UnicodeAttribute()
    type = UnicodeAttribute()
    status = UnicodeAttribute()
    artifacts = ListAttribute(of=JSONAttribute)


class TestResult(MapAttribute):
    status = UnicodeAttribute()
    steps = ListAttribute(of=TestResultStep)


class TestRunTable(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "paparazzi_test_run_table"

    user_test_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True, default_for_new=lambda: generate_test_run_id())
    state = UnicodeAttribute()
    result = TestResult()


if not TestRunTable.exists():
    TestRunTable.create_table(read_capacity_units=5, write_capacity_units=5, wait=True)
