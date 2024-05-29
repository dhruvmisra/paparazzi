from pynamodb.attributes import MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection

from util.id import generate_test_id

from .base import BaseModel


class Viewport(MapAttribute):
    width = NumberAttribute()
    height = NumberAttribute()


class DeviceInfo(MapAttribute):
    ua = UnicodeAttribute()
    viewport = Viewport()


class FrequencyIndex(GlobalSecondaryIndex):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        projection = KeysOnlyProjection()

    frequency = UnicodeAttribute(hash_key=True)


class TestTable(BaseModel):
    class Meta(BaseModel.Meta):
        table_name = "paparazzi_test_table"

    user_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True, default_for_new=lambda: generate_test_id())
    name = UnicodeAttribute()
    frequency = UnicodeAttribute()
    base_url = UnicodeAttribute()
    device = DeviceInfo()
    state = UnicodeAttribute()
    frequency_index = FrequencyIndex()


if not TestTable.exists():
    TestTable.create_table(read_capacity_units=5, write_capacity_units=5, wait=True)
