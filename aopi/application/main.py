from fastapi import FastAPI
from loguru import logger
from starlette.responses import UJSONResponse
from starlette.staticfiles import StaticFiles

from aopi import FRONTEND_DIR
from aopi.application.lifetime import shutdown, startup
from aopi.application.plugin_manager import plugin_manager
from aopi.models import create_db
from aopi.settings import settings
from aopi.utils.logging import configure_logging


def get_application() -> FastAPI:
    from aopi.routes import api_router

    configure_logging()
    app = FastAPI(
        title="Another One Package Index",
        default_response_class=UJSONResponse,
    )
    app.on_event("startup")(startup)
    app.on_event("shutdown")(shutdown)
    plugin_manager.load()
    plugin_manager.add_routes(app)
    create_db()
    logger.debug("DB initialized")
    app.include_router(api_router, prefix="/api")
    if not settings.no_ui:
        app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
    logger.debug("Routes mounted")
    logger.info("Worker is up")
    return app
