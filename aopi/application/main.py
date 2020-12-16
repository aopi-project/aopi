import aiohttp_jinja2
import jinja2
from aiohttp.web import Application
from loguru import logger

from aopi.api import routes
from aopi.models import create_db
from aopi.models.meta import database


async def connect_db(_: Application) -> None:
    await database.connect()
    logger.info("Database connected")


def get_application() -> Application:
    app = Application()
    app.add_routes(routes=routes)
    app.on_startup.append(connect_db)
    logger.debug("Routes mounted")
    create_db()
    logger.debug("DB initialized")
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("./aopi/templates"))
    logger.info("Worker is up")
    return app
