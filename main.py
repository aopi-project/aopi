try:
    from aopi.runners.gunicorn_runner import run_app as gunicorn_app
except ImportError:
    gunicorn_app = None  # type: ignore

try:
    from aopi.runners.asyncio_runner import run_app as aiohttp_app
except ImportError:
    aiohttp_app = None  # type: ignore


def main() -> None:
    if gunicorn_app:
        gunicorn_app()
    elif aiohttp_app:
        aiohttp_app()
    else:
        print(
            "Can't run the application. "
            "Try to install aopi with unix extra"
            " (python -m pip install aopi[unix])."
        )


if __name__ == "__main__":
    main()
