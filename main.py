from aopi.settings import settings

try:
    from aopi.runners.gunicorn_runner import run_app
except ImportError:
    from aopi.runners.asyncio_runner import run_app


def main() -> None:
    settings.pprint()
    run_app()


if __name__ == "__main__":
    main()
