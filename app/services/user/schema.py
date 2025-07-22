from datetime import datetime
from typing import Literal, Optional
from fastapi import Query


from pydantic import (
    BaseModel,
)


class OutGetUserSchema(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime | None
    is_active: bool
    is_admin: bool


class UserPaginationDep(BaseModel):
    limit: int = Query(default=10, ge=1, le=100)
    offset: int = Query(default=0, ge=0)
    order_by: Literal["id", "username", "created_at"] = Query("id")
    order_dir: Literal["asc", "desc"] = Query("asc")


class UserFilterDep(BaseModel):
    id: Optional[int] = Query(None)
    username: Optional[str] = Query(None)
    is_active: Optional[bool] = Query(None)
    is_admin: Optional[bool] = Query(None)
    created_from: Optional[datetime] = Query(None)
    created_to: Optional[datetime] = Query(None)
