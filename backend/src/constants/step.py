from enum import Enum


class TestStepType(str, Enum):
    CLICK = "CLICK"
    NAVIGATION = "NAVIGATION"
    SCROLL = "SCROLL"
    SCREENSHOT = "SCREENSHOT"
