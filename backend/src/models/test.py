from pynamodb.attributes import MapAttribute, NumberAttribute, UnicodeAttribute

from .base import BaseModel


class Viewport(MapAttribute):
    width = NumberAttribute(null=False)
    height = NumberAttribute(null=False)


class DeviceInfo(MapAttribute):
    ua = UnicodeAttribute(null=False)
    viewport = Viewport()


class TestTable(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "paparazzi_test_table"

    user_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute()
    frequency = UnicodeAttribute()
    base_url = UnicodeAttribute()
    device = DeviceInfo()
    state = UnicodeAttribute()

if not TestTable.exists():
    TestTable.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
