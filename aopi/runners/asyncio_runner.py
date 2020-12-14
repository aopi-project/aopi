from aiohttp import web

from aopi.settings import settings


def run_app() -> None:
    from aopi.application import get_application

    settings.pprint()
    application = get_application()
    web.run_app(app=application, host=settings.host, port=settings.port)
