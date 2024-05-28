from datetime import datetime
from typing import Optional

from pydantic import Field

from constants import TestStepType

from .base import BaseSchema


class TestStepScrollPosition(BaseSchema):
    x: int
    y: int


class TestStepClickPosition(BaseSchema):
    x: int
    y: int


class TestStepLocation(BaseSchema):
    url: str


class CreateTestStepRequest(BaseSchema):
    id: str
    created_at: datetime = Field(..., alias="createdAt")
    type: TestStepType
    click_position: Optional[TestStepClickPosition] = Field(None, alias="clickPosition")
    scroll_position: Optional[TestStepScrollPosition] = Field(None, alias="scrollPosition")
    location: Optional[TestStepLocation] = None


class TestStepDBInput(CreateTestStepRequest):
    user_test_id: str


class TestStepDB(TestStepDBInput):
    updated_at: datetime


class CreateTestStepResponse(BaseSchema):
    id: str
    message: str = "Test step created successfully"


class TestStepResponse(CreateTestStepRequest):
    updated_at: datetime = Field(..., alias="updatedAt")

