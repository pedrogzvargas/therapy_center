from pydantic import BaseModel
from pydantic import EmailStr


class Login(BaseModel):
    email: EmailStr
    password: str


class RefreshToken(BaseModel):
    refresh_token: str


class Logout(BaseModel):
    access_token: str
