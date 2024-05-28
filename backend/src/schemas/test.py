from datetime import datetime
from typing import Optional

from pydantic import Field

from constants import TestFrequency, TestState

from .base import BaseSchema


class TestDeviceInfoViewport(BaseSchema):
    width: int
    height: int


class TestDeviceInfo(BaseSchema):
    ua: str
    viewport: TestDeviceInfoViewport


class CreateTestRequest(BaseSchema):
    name: str
    frequency: TestFrequency
    base_url: str = Field(..., alias="baseUrl")
    device: TestDeviceInfo


class TestDBInput(CreateTestRequest):
    user_id: str
    state: TestState


class TestDB(TestDBInput):
    id: str
    created_at: datetime
    updated_at: datetime


class TestResponse(CreateTestRequest):
    id: str
    state: TestState
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class UpdateTestRequest(BaseSchema):
    name: Optional[str] = None
    frequency: Optional[TestFrequency] = None
    base_url: Optional[str] = Field(None, alias="baseUrl")
    state: Optional[TestState] = None
