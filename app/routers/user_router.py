from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_master

from app.services.user import (
    user_crud,
    OutGetUserSchema,
    UserQueryParams,
)


router = APIRouter()


@router.get("", response_model=list[OutGetUserSchema ])
async def get_users(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
    query: Annotated[UserQueryParams, Depends()],
):
    return await user_crud.get_many(session=session, query=query)
