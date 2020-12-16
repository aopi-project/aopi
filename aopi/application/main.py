import aiohttp_jinja2
import jinja2
from aiohttp.web import Application
from loguru import logger

from aopi.api import routes
from aopi.models import create_db, database


async def startup_operations(_: Application) -> None:
    await database.connect()
    logger.debug("Database connected")


def get_application() -> Application:
    app = Application()
    app.add_routes(routes=routes)
    app.on_startup.append(startup_operations)
    logger.debug("Routes mounted")
    create_db()
    logger.debug("DB initialized")
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("./aopi/templates"))
    logger.debug("App created")
    return app
