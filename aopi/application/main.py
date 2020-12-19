from fastapi import FastAPI
from loguru import logger
from starlette.responses import UJSONResponse

from aopi.models import create_db
from aopi.models.meta import database


async def connect_db() -> None:
    await database.connect()
    logger.info("Database connected")


async def startup() -> None:
    await connect_db()


def get_application() -> FastAPI:
    from aopi.api import router

    app = FastAPI(
        title="Another One Package Index",
        default_response_class=UJSONResponse,
    )
    create_db()
    logger.debug("DB initialized")
    app.on_event("startup")(startup)
    app.include_router(router)
    logger.debug("Routes mounted")
    logger.info("Worker is up")
    return app
