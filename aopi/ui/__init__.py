from pathlib import Path

from starlette.templating import Jinja2Templates

ui_dir = Path(__file__).parent
static_path = ui_dir / "static"
templates_path = ui_dir / "templates"
templates = Jinja2Templates(directory=templates_path)
