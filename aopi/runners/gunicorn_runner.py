import logging
import sys
from typing import Any, Dict, Optional, Union

from aiohttp.web_app import Application
from gunicorn.app.base import BaseApplication
from gunicorn.config import Config
from gunicorn.glogging import Logger
from loguru import logger

from aopi.settings import settings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        print(record.__class__)
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


class StubbedGunicornLogger(Logger):
    def setup(self, cfg: Config) -> None:
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_logger.setLevel(settings.log_level.value)
        self.access_logger.setLevel(settings.log_level.value)


class StandaloneApplication(BaseApplication):
    def init(self, parser: Any, opts: Any, args: Any) -> None:
        super(StandaloneApplication, self).init(parser, opts, args)

    def __init__(self, run_options: Optional[Dict[str, Any]] = None):
        self.options = run_options or {}
        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> Application:
        from aopi.application import get_application

        return get_application()


def run_app() -> None:
    intercept_handler = InterceptHandler()
    logging.root.setLevel(settings.log_level.value)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),  # type: ignore
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]

    logger.configure(handlers=[{"sink": sys.stdout}])

    options = {
        "bind": f"{settings.host}:{settings.port}",
        "workers": settings.workers_count,
        "worker_class": "aiohttp.worker.GunicornUVLoopWebWorker",
        "pidfile": settings.pid_file,
        "reload": settings.reload,
        "accesslog": "-",
        "errorlog": "-",
        "logger_class": StubbedGunicornLogger,
        "timeout": 0,
    }
    StandaloneApplication(options).run()
