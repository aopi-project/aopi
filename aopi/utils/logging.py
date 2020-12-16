import logging
import sys
from typing import Optional, Union

from loguru import logger

from aopi.arg_parser import LogLevel
from aopi.settings import settings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        level: Optional[Union[str, int]] = None
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure_logging() -> None:
    intercept_handler = InterceptHandler()
    logger.remove()
    logger.add(sys.stderr, level=settings.log_level.value)
    logging.root.setLevel(LogLevel.error.value)

    seen = {"sqlalchemy", "databases"}
    for name in [
        *logging.root.manager.loggerDict.keys(),  # type: ignore
        "aopi",
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "aiohttp.access",
        "aiohttp",
        "aiohttp.server",
        "aiohttp.web",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            tmp_logger = logging.getLogger(name)
            tmp_logger.setLevel(settings.log_level.value)
            tmp_logger.handlers = [intercept_handler]

    logger.configure(handlers=[{"sink": sys.stdout}])
