from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_master

from .crud import get_all_users, create_user
from .schema import RspUserSchema, RqstCreateUserSchema


router = APIRouter()


@router.get("", response_model=list[RspUserSchema])
async def get_users(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
):
    users = await get_all_users(session=session)
    return users


@router.post("", response_model=RspUserSchema)
async def new_user(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
    user_create: RqstCreateUserSchema,
):
    user = await create_user(
        session=session,
        user_create=user_create,
    )
    return user
