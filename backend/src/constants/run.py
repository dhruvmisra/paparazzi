from enum import Enum


class TestRunState(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    EXECUTION_FAILED = "EXECUTION_FAILED"


class TestResultStatus(str, Enum):
    PENDING = "PENDING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
