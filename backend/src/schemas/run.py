from datetime import datetime

from pydantic import Field

from constants import TestResultStatus, TestRunState, TestStepType

from .base import BaseSchema


class TestRunResultStep(BaseSchema):
    test_step_id: str = Field(..., alias="testStepId")
    type: TestStepType
    status: TestResultStatus
    artifacts: list[dict]


class TestRunResult(BaseSchema):
    status: TestResultStatus
    steps: list[TestRunResultStep]


class TestRunDBInput(BaseSchema):
    user_test_id: str
    state: TestRunState
    result: TestRunResult


class TestRunDB(TestRunDBInput):
    id: str
    created_at: datetime
    updated_at: datetime


class QueueTestRunResponse(BaseSchema):
    id: str
    message: str = "Test run queued successfully"


class TestRunResponse(BaseSchema):
    id: str
    state: TestRunState
    result: TestRunResult
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
