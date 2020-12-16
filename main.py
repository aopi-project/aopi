from aopi.settings import settings
from aopi.utils.logging import configure_logging
from aopi.utils.package_explorer import discover_packages

try:
    from aopi.runners.gunicorn_runner import run_app
except ImportError:
    from aopi.runners.asyncio_runner import run_app


def main() -> None:
    settings.pprint()
    configure_logging()
    discover_packages()
    run_app()


if __name__ == "__main__":
    main()
