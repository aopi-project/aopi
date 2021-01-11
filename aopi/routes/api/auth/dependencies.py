from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette import status

from aopi.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_sub_from_jwt(token: str, error: Exception) -> int:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise error
    except JWTError:
        raise error
    return user_id


if settings.enable_users:

    def get_current_user_id(token: str = Depends(oauth2_scheme)) -> Optional[int]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return int(get_sub_from_jwt(token, credentials_exception))


else:

    def get_current_user_id() -> Optional[int]:  # type: ignore
        return None
