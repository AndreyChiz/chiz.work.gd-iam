from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_master

from .crud import user_crud
from .schema import RspUserSchema, RqstCreateUserSchema

from app.auth import auth_manager # TODO move


router = APIRouter()


@router.get("", response_model=list[RspUserSchema])
async def get_users(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
):
    users = await user_crud.get_all(session=session)
    return users


@router.post("", response_model=RspUserSchema)
async def create_new_user(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
    new_user: RqstCreateUserSchema,
):
    user = await user_crud.create(
        session=session,
        username = new_user.username,
        password_hash=auth_manager.password.hash(new_user.password)
    )
    return user
