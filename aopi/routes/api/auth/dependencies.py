from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette import status

from aopi.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

if settings.enable_users:

    async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> Optional[int]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
            )
            user_id: int = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return int(user_id)


else:

    async def get_current_user_id() -> Optional[int]:  # type: ignore
        return None
