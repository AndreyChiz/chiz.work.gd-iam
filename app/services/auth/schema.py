import re
from datetime import datetime
from fastapi import Form
from pydantic import (
    BaseModel,
    Field,
    SecretStr,
    field_validator,
)

from .exceptions import WeakPasswordError

STRONG_PASSWORD_PATTERN = re.compile(
    r"^(?=.*[\d])(?=.*[!_@#$%^&*])[\w!_@#$%^&*]{6,128}$"
)


class InRegisterSchema(BaseModel):
    username: str = Field(
        description="Имя пользователя: только ASCII-символы, без пробелов. Приводится к нижнему регистру.",
        examples=["john_doe"],
    )
    password: SecretStr = Field(
        min_length=6,
        max_length=128,
        description="""Пароль должен содержать хотя бы одну цифру,
        один специальный символ, состоять только из латинских букв,
        цифр и допустимых спецсимволов, длина — от 6 до 128 символов.""",
        examples=["Qwe_1234", "Passw0rd!"],
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if " " in value:
            raise ValueError("Пробелы в username не допускаются")

        if not value.isascii():
            raise ValueError("Username должен содержать только ASCII-символы")

        return value.strip().lower()

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: SecretStr) -> SecretStr:
        if not re.match(STRONG_PASSWORD_PATTERN, password.get_secret_value()):
            raise WeakPasswordError()
        return password
    
class OutRegisterSchema(BaseModel):
    id: int
    username: str
    created_at: datetime



class LoginFormSchema:
    def __init__(
        self,
        username: str = Form(..., description="Имя пользователя"),
        password: str = Form(..., description="Пароль"),
    ):
        self.username = username
        self.password = password


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
