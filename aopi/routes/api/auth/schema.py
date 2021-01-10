from typing import Optional

from pydantic import BaseModel


class LoginRequestModel(BaseModel):
    username: Optional[str]
    password: Optional[str]


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
