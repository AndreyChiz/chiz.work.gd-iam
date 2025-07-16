from typing import Annotated

from fastapi import APIRouter, Depends 
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_master
from app.services.auth import LoginForm, UnautorisedException, TokenResponse
from app.services.user import user_crud


router = APIRouter()




@router.post("/login", response_model=TokenResponse)
async def login(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
    form: LoginForm = Depends()

):
    
    username = form.username
    password = form.password
    if not (user:= await user_crud.get(session, username)):
        raise UnautorisedException
    

    return user