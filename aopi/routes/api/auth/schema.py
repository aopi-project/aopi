from pydantic import BaseModel


class LoginRequestModel(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
