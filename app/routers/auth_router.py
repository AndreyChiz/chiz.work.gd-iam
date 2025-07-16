from fastapi import APIRouter
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import user_crud
from app.services.auth import auth_manager
from fastapi import APIRouter, Depends, status
from app.database import db_master
from app.services.user import InCreateUserSchema, OutUserSchema

from app.services.auth import InLoginSchema

router = APIRouter()


@router.post("/login", response_model=OutUserSchema)
async def login(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
    username: InLoginSchema,
):
    return await user_crud.get(session, username.username)
