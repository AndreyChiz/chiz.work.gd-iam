from datetime import datetime
from typing import Literal, Optional


from pydantic import BaseModel, field_validator, Field


class InCreateUserSchema(BaseModel):
    username: str = Field(
        description="Имя пользователя: только ASCII-символы, без пробелов. Приводится к нижнему регистру.",
        examples=["john_doe"],
    )
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if " " in value:
            raise ValueError("Пробелы в username не допускаются")

        if not value.isascii():
            raise ValueError("Username должен содержать только ASCII-символы")

        return value.strip().lower()


class OutUserSchema(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime | None
    is_active: bool
    is_admin: bool


class UserQueryParams(BaseModel):
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
