from typing import Optional

from fastapi import APIRouter, Depends, Form
from fastapi_jwt_auth import AuthJWT
from starlette.requests import Request
from starlette.responses import Response

from aopi.models import AopiUser, database
from aopi.models.dict_proxy import DictProxy
from aopi.ui import templates
from aopi.utils.passwords import verify_password

user_router = APIRouter()


@user_router.get("/")
def aopi_index_page(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("main/index.jinja2", {"request": request})


@user_router.get("/login")
def aopi_login_page(
    request: Request, error: Optional[str] = None
) -> templates.TemplateResponse:
    return templates.TemplateResponse(
        "main/login.jinja2", {"request": request, "error": error}
    )


@user_router.post("/user/login")
async def aopi_user_login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    auth: AuthJWT = Depends(),
) -> templates.TemplateResponse:
    search_query = AopiUser.find(username)
    user = DictProxy(await database.fetch_one(search_query))
    if user.is_none() or not await verify_password(user.password, password):
        return templates.TemplateResponse(
            "main/login.jinja2", {"request": request, "error": "Wrong credentials"}
        )
    access_token = auth.create_access_token(
        subject=username, user_claims={"id": user.id}
    )
    refresh_token = auth.create_refresh_token(
        subject=username, user_claims={"id": user.id}
    )
    auth.set_access_cookies(access_token)
    auth.set_refresh_cookies(refresh_token)
    return templates.TemplateResponse(
        "main/index.jinja2", {"request": request}, headers=response.headers
    )
