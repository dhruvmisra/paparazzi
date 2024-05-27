import logging

import coloredlogs
from asgi_correlation_id import CorrelationIdFilter
from asgi_correlation_id.context import correlation_id
from ecs_logging import StdlibFormatter

import config

CONSOLE_LOG_FORMAT = "%(levelname)s: %(asctime)s %(filename)s:%(lineno)d → %(message)s"
CONSOLE_LEVEL_STYLES = {
    "critical": {"color": "red", "bright": True, "bold": True},
    "debug": {"color": "green", "faint": True},
    "error": {"color": "red", "bright": True},
    "info": {"color": "green", "bold": True},
    "notice": {"color": "cyan"},
    "spam": {"color": "white", "faint": True},
    "success": {"color": "green", "bold": True},
    "verbose": {"color": "blue"},
    "warning": {"color": "magenta", "bold": True},
}

###################
# Context filters
###################
class TraceIDLogFilter(CorrelationIdFilter):
    """
    Log filter to inject the current request id of the request under `log_record.trace_id`
    """

    def filter(self, log_record):
        cid = correlation_id.get()
        if self.uuid_length is not None and cid:
            log_record.trace_id = cid[: self.uuid_length]  # type: ignore[attr-defined]
        else:
            log_record.trace_id = cid  # type: ignore[attr-defined]
        return log_record


def clear_uvicorn_logger_handlers():
    logging.getLogger("watchfiles.main").setLevel(logging.INFO)
    logging.getLogger("uvicorn").handlers.clear()


def setup(logger: logging.Logger):
    if logger.hasHandlers():
        logger.handlers.clear()
    clear_uvicorn_logger_handlers()

    if config.STRUCTURED_LOGGING:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            StdlibFormatter(
                fmt=CONSOLE_LOG_FORMAT,
                exclude_fields=[
                    "log.original",
                    "log.origin",
                    "log.logger",
                    "process",
                    "ecs",
                ],
                extra=config.DEFAULT_LOG_FIELDS,
            )
        )
        logger.addHandler(stream_handler)
    else:
        coloredlogs.install(
            level=config.LOG_LEVEL,
            fmt=CONSOLE_LOG_FORMAT,
            level_styles=CONSOLE_LEVEL_STYLES,
        )

    logger.addFilter(TraceIDLogFilter())
    logger.setLevel(config.LOG_LEVEL)

    return logger


log = logging.getLogger()
log = setup(log)
