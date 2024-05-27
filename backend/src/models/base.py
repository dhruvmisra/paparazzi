from datetime import datetime, timezone

from pynamodb.attributes import UTCDateTimeAttribute
from pynamodb.models import Model

from config import AWS_REGION, DB_HOST


class BaseModel(Model):
    class Meta:
        host = DB_HOST
        region = AWS_REGION

    created_at = UTCDateTimeAttribute(default_for_new=lambda: datetime.now(timezone.utc))
    updated_at = UTCDateTimeAttribute(default_for_new=lambda: datetime.now(timezone.utc))
