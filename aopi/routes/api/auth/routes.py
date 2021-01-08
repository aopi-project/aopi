from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from aopi.models import AopiUser, database
from aopi.models.dict_proxy import DictProxy
from aopi.routes.api.auth.schema import LoginRequestModel, LoginResponse
from aopi.utils.passwords import verify_password

auth_router = APIRouter()


@auth_router.post("/login", response_model=LoginResponse)
async def aopi_user_login(
    credentials: LoginRequestModel,
    auth: AuthJWT = Depends(),
) -> LoginResponse:
    search_query = AopiUser.find(username=credentials.username)
    user = DictProxy(await database.fetch_one(search_query))
    if user.is_none() or not await verify_password(user.password, credentials.password):
        raise HTTPException(status_code=401, detail="Wrong credentials")
    access_token = auth.create_access_token(subject=user.id)
    refresh_token = auth.create_refresh_token(
        subject=user.id,
    )
    return LoginResponse(access_token=access_token, refresh_token=refresh_token)
