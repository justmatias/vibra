import sys
from enum import Enum
from functools import cache

from loguru import logger
from loguru._logger import Logger


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@cache
def get_logger() -> Logger:
    logger.remove()
    logger.add(
        sys.stdout,
        level="DEBUG",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    )
    return logger  # type: ignore[return-value]


def log(message: str, level: LogLevel = LogLevel.INFO) -> None:
    logger_ = get_logger()
    logger_.log(level.value, message)
