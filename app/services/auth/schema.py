
from pydantic import BaseModel


class InLoginSchema(BaseModel):
    username: str
    password: str 
