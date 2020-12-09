import argparse
from typing import Any, Dict, Optional

from aiohttp.web_app import Application
from gunicorn.app.base import BaseApplication


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
        from application import app

        return app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0", dest="host")
    parser.add_argument("-p", "--port", type=int, default=8000, dest="port")
    parser.add_argument(
        "-r", "--reload", action="store_true", default=8000, dest="reload"
    )
    parser.add_argument("-w", "--workers", type=int, default=4, dest="workers_count")
    parser.add_argument(
        "--pid-file", type=str, default="/tmp/aopi-server.pid", dest="pid_file"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    options = {
        "bind": f"{args.host}:{args.port}",
        "workers": args.workers_count,
        "worker_class": "aiohttp.worker.GunicornWebWorker",
        "pidfile": args.pid_file,
        "reload": True,
        "timeout": 0,
    }
    StandaloneApplication(options).run()
