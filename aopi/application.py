from aiohttp.web import Application
from api import routes


def add_routes(app: Application) -> None:
    app.add_routes(routes)


app = Application()
add_routes(app)
