
from pydantic import BaseModel
from fastapi import  Form




class LoginForm:
    def __init__(
        self,
        username: str = Form(..., description="Имя пользователя"),
        password: str = Form(..., description="Пароль"),
    ):
        self.username = username
        self.password = password


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"