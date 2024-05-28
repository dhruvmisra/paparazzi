from pynamodb.attributes import MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.indexes import KeysOnlyProjection, LocalSecondaryIndex

from util.id import generate_test_id

from .base import BaseModel


class Viewport(MapAttribute):
    width = NumberAttribute()
    height = NumberAttribute()


class DeviceInfo(MapAttribute):
    ua = UnicodeAttribute()
    viewport = Viewport()


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


if not TestTable.exists():
    TestTable.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


class FrequencyIndex(LocalSecondaryIndex):
    class Meta:
        projection = KeysOnlyProjection()

    user_id = UnicodeAttribute(hash_key=True)
    frequency = UnicodeAttribute(range_key=True)
