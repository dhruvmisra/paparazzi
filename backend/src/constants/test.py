from enum import Enum


class TestState(str, Enum):
    RECORDING = "RECORDING"
    QUEUED = "QUEUED"
    COMPLETED = "COMPLETED"


class TestFrequency(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
