from datetime import datetime

from pydantic import BaseModel
from .models import UserRole



class RqstCreateUserSchema(BaseModel):
    username: str
    password: str   
    
    


class RspUserSchema(BaseModel):
    id: int
    username: str
    role: str
    frmware_acces_group: str | None
    created_at: datetime
    updated_at: datetime | None
    is_active: bool
