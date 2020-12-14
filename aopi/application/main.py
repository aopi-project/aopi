import aiohttp_jinja2
import jinja2
from aiohttp.web import Application

from aopi.api import routes
from aopi.models import create_db


def get_application() -> Application:
    app = Application()
    app.add_routes(routes=routes)
    create_db()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("./aopi/templates"))
    return app
