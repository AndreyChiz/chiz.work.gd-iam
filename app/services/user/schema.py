from datetime import datetime
from typing import Literal, Optional


from pydantic import (
    BaseModel,
    Field,
)


class OutGetUserSchema(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime | None
    is_active: bool
    is_admin: bool


class UserPaginationDep(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    order_by: Literal["id", "username", "created_at"] = "id"
    order_dir: Literal["asc", "desc"] = "asc"


class UserFilterDep(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
