from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from aopi.models import AopiUser, database
from aopi.models.auth_tokens import AuthTokens
from aopi.models.users import AopiUserModel
from aopi.routes.api.auth.dependencies import get_current_user_id, get_sub_from_jwt
from aopi.routes.api.auth.logic import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
)
from aopi.routes.api.auth.schema import LoginRequestModel, LoginResponse, RefreshRequest

auth_router = APIRouter()


@auth_router.post("/login", response_model=LoginResponse)
async def get_new_token_pair(user_info: LoginRequestModel) -> LoginResponse:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if user_info.username is None or user_info.password is None:
        raise unauthorized
    user = await authenticate_user(user_info.username, user_info.password)
    if user is None:
        raise unauthorized
    access_token = create_access_token(user_id=user.id)
    refresh_token = create_refresh_token(user_id=user.id)
    delete_query = AuthTokens.delete_query().where(AuthTokens.user_id == user.id)
    await database.execute(delete_query)
    add_query = AuthTokens.add(
        access_token=access_token, refresh_token=refresh_token, user_id=user.id
    )
    await database.execute(add_query)
    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/refresh", response_model=LoginResponse)
async def refresh_token_pair(refresh_data: RefreshRequest) -> LoginResponse:
    token_query = AuthTokens.select_query().where(
        AuthTokens.refresh_token == refresh_data.refresh_token
    )
    token = await database.fetch_one(token_query)
    incorrect_token = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect refresh token",
    )
    if token is None:
        raise incorrect_token
    user_id = get_sub_from_jwt(refresh_data.refresh_token, incorrect_token)

    access_token = create_access_token(user_id=user_id)
    refresh_token = create_refresh_token(user_id=user_id)
    delete_query = AuthTokens.delete_query().where(AuthTokens.user_id == user_id)
    await database.execute(delete_query)
    add_query = AuthTokens.add(
        access_token=access_token, refresh_token=refresh_token, user_id=user_id
    )
    await database.execute(add_query)
    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.get(
    "/user", response_model=AopiUserModel, response_model_exclude={"password"}
)
async def get_current_user_info(
    user_id: int = Depends(get_current_user_id),
) -> AopiUserModel:
    user_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )
    if user_id is None:
        raise user_not_found
    find_query = AopiUser.select_query().where(AopiUser.id == user_id)
    if user_dict := await database.fetch_one(find_query):
        return AopiUserModel.from_orm(user_dict)
    raise user_not_found


@auth_router.post("/logout")
async def logout(user_id: int = Depends(get_current_user_id)) -> None:
    delete_query = AuthTokens.delete_query().where(AuthTokens.user_id == user_id)
    await database.execute(delete_query)
