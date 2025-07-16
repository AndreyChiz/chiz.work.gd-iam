import re
from datetime import datetime
from typing import Literal, Optional
from .exceptions import WeakPasswordError


from pydantic import (
    BaseModel,
    field_validator,
    Field,
    SecretStr,
)


STRONG_PASSWORD_PATTERN = re.compile(
    r"^(?=.*[\d])(?=.*[!_@#$%^&*])[\w!_@#$%^&*]{6,128}$"
)


class InCreateUserSchema(BaseModel):
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


class OutUserSchema(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime | None
    is_active: bool
    is_admin: bool


class UserQueryParams(BaseModel):
    """Схема фиьтра, сортировки, пагинации"""

    id: Optional[int] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None

    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    order_by: Literal["id", "username", "created_at"] = "id"
    order_dir: Literal["asc", "desc"] = "asc"
