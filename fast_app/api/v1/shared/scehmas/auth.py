from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class RefreshToken(BaseModel):
    refresh_token: str


class Logout(BaseModel):
    access_token: str
