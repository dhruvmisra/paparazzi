from pynamodb.attributes import MapAttribute, NumberAttribute, UnicodeAttribute

from util.id import generate_test_step_id

from .base import BaseModel


class ClickPosition(MapAttribute):
    x = NumberAttribute()
    y = NumberAttribute()


class ScrollPosition(MapAttribute):
    x = NumberAttribute()
    y = NumberAttribute()


class Location(MapAttribute):
    url = UnicodeAttribute()


class TestStepTable(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "paparazzi_test_step_table"

    user_test_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True, default_for_new=lambda: generate_test_step_id())
    type = UnicodeAttribute()
    click_position = ClickPosition(null=True)
    scroll_position = ScrollPosition(null=True)
    location = Location(null=True)


if not TestStepTable.exists():
    TestStepTable.create_table(read_capacity_units=5, write_capacity_units=5, wait=True)
