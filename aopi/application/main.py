from aopi_index_builder import AopiContextBase, init_context, load_plugins
from fastapi import FastAPI
from loguru import logger
from starlette.responses import UJSONResponse

from aopi.models import create_db
from aopi.models.meta import database, metadata
from aopi.settings import settings
from aopi.utils.logging import configure_logging


async def connect_db() -> None:
    await database.connect()
    logger.info("Database connected")


async def startup() -> None:
    await connect_db()


def init_plugins(app: FastAPI) -> None:
    init_context(
        AopiContextBase(
            database=database, metadata=metadata, main_dir=settings.packages_dir
        )
    )
    plugins = load_plugins()
    logger.info(f"Found {len(plugins)} plugins.")
    for plugin in plugins:
        index = plugin.package_index
        logger.debug(
            f"Enabling plugin {plugin.plugin_name} "
            f"from {plugin.package_name}:{plugin.package_version}"
        )
        app.include_router(
            router=index.router, prefix=plugin.prefix, tags=[plugin.package_name]
        )


def get_application() -> FastAPI:
    from aopi.routes import router

    configure_logging()
    app = FastAPI(
        title="Another One Package Index",
        default_response_class=UJSONResponse,
    )
    init_plugins(app)
    create_db()
    logger.debug("DB initialized")
    app.on_event("startup")(startup)
    app.include_router(router)
    logger.debug("Routes mounted")
    logger.info("Worker is up")
    return app
