from aopi.settings import settings
from aopi.utils.logging import configure_logging

try:
    from aopi.runners.gunicorn_runner import run_app
except ImportError:
    from aopi.runners.uvicorn_runner import run_app


def main() -> None:
    settings.pprint()
    configure_logging()
    run_app()


if __name__ == "__main__":
    main()
