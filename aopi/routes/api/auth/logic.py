from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import jwt

from aopi.models import AopiUser, database
from aopi.models.users import AopiUserModel
from aopi.settings import settings
from aopi.utils.passwords import verify_password


def create_jwt(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def create_access_token(user_id: int) -> str:
    access_token_expires = timedelta(minutes=30)
    return create_jwt(data={"sub": str(user_id)}, expires_delta=access_token_expires)


def create_refresh_token(user_id: int) -> str:
    refresh_token_expires = timedelta(days=30)
    return create_jwt(data={"sub": str(user_id)}, expires_delta=refresh_token_expires)


async def authenticate_user(username: str, password: str) -> Optional[AopiUserModel]:
    user_query = AopiUser.find(username=username)
    found_users = await database.fetch_all(user_query)
    if len(found_users) != 1:
        return None
    user = AopiUserModel.from_orm(found_users[0])
    if user.password is None:
        return None
    if not await verify_password(user.password, password):
        return None
    return user
