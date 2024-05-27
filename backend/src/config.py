import os


# os.getenv but also raises error for required variables
def getenv(name, default=None, required=True):
    try:
        return os.environ[name] if required and default is None else os.environ.get(name, default)
    except KeyError as e:
        print(f"Required environment variable {e} not defined")
        raise


ENVIRONMENT = getenv("ENVIRONMENT")
VERSION = getenv("VERSION", "")
DEBUG = ENVIRONMENT.casefold() == "development".casefold()

HOST = getenv("APPLICATION_HOST", "0.0.0.0")
PORT = int(getenv("APPLICATION_PORT", "3000"))

STRUCTURED_LOGGING = getenv("STRUCTURED_LOGGING", "false").lower() == "true"
LOG_LEVEL = getenv("LOG_LEVEL", "DEBUG")
DEFAULT_LOG_FIELDS = {"server": "paparazzi", "env": ENVIRONMENT, "version": VERSION}

SQS_QUEUE_URL = getenv("SQS_QUEUE_URL")
SQS_QUEUE_NAME = getenv("SQS_QUEUE_NAME")
