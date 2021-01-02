from typing import Optional
from urllib.parse import urlencode

from fastapi import APIRouter, Form
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from aopi.ui import templates

ui_router = APIRouter()


@ui_router.get("/")
def aopi_index_page(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("main/index.jinja2", {"request": request})


@ui_router.get("/login")
def aopi_login_page(
    request: Request, error: Optional[str] = None
) -> templates.TemplateResponse:
    print(error)
    return templates.TemplateResponse("main/login.jinja2", {"request": request})


@ui_router.post("/user/login")
async def aopi_user_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
) -> RedirectResponse:
    request.url_for("aopi_login_page")
    if username != "s3rius" or password != "123":
        return RedirectResponse(
            url=request.url_for("aopi_login_page")
            + "?"
            + urlencode(dict(error="Shit")),
            status_code=HTTP_303_SEE_OTHER,
        )
    return RedirectResponse(
        url=request.url_for("aopi_index_page"), status_code=HTTP_303_SEE_OTHER
    )
