from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_master

from .crud import get_all_users
from .schema import RspUserSchema


router = APIRouter()


@router.get("", response_model=list[RspUserSchema])
async def get_users(
    session: AsyncSession = Depends(
        db_master.session_getter,
    ),
):
    users = await get_all_users(session=session)
    return users
