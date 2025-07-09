from datetime import datetime

from pydantic import BaseModel



class RqstCreateUserSchema(BaseModel):
    username: str
    password: str
    role: str



class RspUserSchema(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime | None
    is_active: bool
