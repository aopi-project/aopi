from fastapi import FastAPI
from loguru import logger
from starlette.responses import UJSONResponse
from starlette.staticfiles import StaticFiles

from aopi.application.plugin_manager import plugin_manager
from aopi.application.startup import startup
from aopi.models import create_db
from aopi.routes import api_router
from aopi.settings import settings
from aopi.ui import static_path
from aopi.utils.logging import configure_logging


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
