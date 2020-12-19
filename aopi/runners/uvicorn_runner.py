import uvicorn

from aopi.settings import settings


def run_app() -> None:
    uvicorn.run(
        app="aopi.application:get_application",
        factory=True,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        workers=settings.workers_count,
    )
