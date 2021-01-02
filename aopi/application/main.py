from fastapi import FastAPI
from loguru import logger
from starlette.responses import UJSONResponse
from starlette.staticfiles import StaticFiles

from aopi.application.plugin_manager import plugin_manager
from aopi.models import AopiUser, create_db
from aopi.models.meta import database
from aopi.routes import api_router
from aopi.settings import settings
from aopi.ui import static_path
from aopi.utils.logging import configure_logging
from aopi.utils.passwords import hash_password


async def connect_db() -> None:
    await database.connect()
    logger.info("Database connected")


async def fill_db() -> None:
    if settings.enable_users:
        hashed_pass = await hash_password("admin")
        insert_query = AopiUser.create("admin", hashed_pass)
        try:
            await database.execute(insert_query)
        except Exception as e:
            logger.error(e)
        logger.warning(plugin_manager.get_roles())


async def startup() -> None:
    await connect_db()
    await fill_db()


def get_application() -> FastAPI:
    from aopi.routes import ui_router

    configure_logging()
    app = FastAPI(
        title="Another One Package Index",
        default_response_class=UJSONResponse,
    )
    plugin_manager.load()
    plugin_manager.add_routes(app)
    create_db()
    logger.debug("DB initialized")
    app.on_event("startup")(startup)
    app.include_router(api_router, prefix="/api", tags=["aopi api"])
    if not settings.no_ui:
        app.include_router(ui_router, tags=["aopi ui"])
        app.mount("/static", StaticFiles(directory=static_path), name="static")
    logger.debug("Routes mounted")
    logger.info("Worker is up")
    return app
