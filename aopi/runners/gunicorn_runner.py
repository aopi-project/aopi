from typing import Any, Dict, Optional

from aiohttp.web_app import Application
from gunicorn.app.base import BaseApplication

from aopi.settings import settings


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
    settings.pprint()
    options = {
        "bind": f"{settings.host}:{settings.port}",
        "workers": settings.workers_count,
        "worker_class": "aiohttp.worker.GunicornUVLoopWebWorker",
        "pidfile": settings.pid_file,
        "reload": settings.reload,
        "timeout": 0,
    }
    StandaloneApplication(options).run()
