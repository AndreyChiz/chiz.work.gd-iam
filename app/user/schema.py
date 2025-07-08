from datetime import datetime

from pydantic import BaseModel







class RspUserSchema(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
