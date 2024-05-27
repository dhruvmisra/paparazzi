from enum import Enum


class TestState(str, Enum):
    RECORDING = "RECORDING"
    RECORDED = "RECORDED"


class TestFrequency(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
