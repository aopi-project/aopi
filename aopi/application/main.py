from fastapi import FastAPI, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from loguru import logger
from starlette.requests import Request
from starlette.responses import UJSONResponse
from starlette.staticfiles import StaticFiles

from aopi import FRONTEND_DIR
from aopi.application.lifetime import shutdown, startup
from aopi.application.plugin_manager import plugin_manager
from aopi.models import create_db
from aopi.settings import Settings, settings
from aopi.utils.logging import configure_logging


@AuthJWT.load_config
def jwt_settings() -> Settings:
    return settings


def authjwt_exception_handler(_: Request, exc: AuthJWTException) -> None:
    logger.exception(exc)
    raise HTTPException(status_code=401, detail="Wrong tokens")


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
    app.exception_handler(AuthJWTException)(authjwt_exception_handler)
    logger.debug("DB initialized")
    app.include_router(api_router, prefix="/api")
    if not settings.no_ui:
        app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
    logger.debug("Routes mounted")
    logger.info("Worker is up")
    return app
