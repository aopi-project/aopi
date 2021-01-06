from urllib.parse import urlencode

from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from loguru import logger
from starlette.requests import Request
from starlette.responses import RedirectResponse, UJSONResponse
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_303_SEE_OTHER

from aopi.application.plugin_manager import plugin_manager
from aopi.application.startup import startup
from aopi.models import create_db
from aopi.routes import api_router
from aopi.settings import Settings, settings
from aopi.ui import static_path
from aopi.utils.logging import configure_logging


@AuthJWT.load_config
def jwt_settings() -> Settings:
    return settings


def authjwt_exception_handler(
    request: Request, _: AuthJWTException
) -> RedirectResponse:
    return RedirectResponse(
        url=f"{request.url_for('aopi_login_page')}"
        f"?{urlencode({'error': 'You must login before access'})}",
        status_code=HTTP_303_SEE_OTHER,
    )


def get_application() -> FastAPI:
    from aopi.routes import user_router

    configure_logging()
    app = FastAPI(
        title="Another One Package Index",
        default_response_class=UJSONResponse,
    )
    plugin_manager.load()
    plugin_manager.add_routes(app)
    create_db()
    app.exception_handler(AuthJWTException)(authjwt_exception_handler)
    logger.debug("DB initialized")
    app.on_event("startup")(startup)
    app.include_router(api_router, prefix="/api", tags=["aopi api"])
    if not settings.no_ui:
        app.include_router(user_router, tags=["aopi ui"])
        app.mount("/static", StaticFiles(directory=static_path), name="static")
    logger.debug("Routes mounted")
    logger.info("Worker is up")
    return app
