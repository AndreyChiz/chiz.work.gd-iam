from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_master
from app.exceptions import NotFoundException, TokenInvalidException, UnactiveException
from app.services.auth import auth_service
from app.services.user import (
    OutGetUserSchema,
    UserFilterDep,
    UserPaginationDep,
    user_crud,
)

http_bearer = HTTPBearer()

router = APIRouter()

# Just for not foget :-) ... maybe use later TODO
# think i could use this alias for filters
# UserFilterDepDep = Annotated[UserFilterDep, Depends()]


@router.get("", response_model=list[OutGetUserSchema])
async def get_users(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
    filters: Annotated[UserFilterDep, Depends()],
    pagination: Annotated[UserPaginationDep, Depends()],
):
    return await user_crud.get_many(
        session=session,
        user_filters=filters,
        user_pagination=pagination,
    )


def get_current_user_data_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    try:
        payload = auth_service.token.decode_payload(token)
    except ExpiredSignatureError:
        raise TokenInvalidException

    return payload


async def get_auth_user(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
    user_data_from_token: dict = Depends(get_current_user_data_from_token),
):
    username = str(user_data_from_token.get("username"))

    if not (
        user := await user_crud.get(
            session,
            username,
        )
    ):
        raise NotFoundException
    if not user.is_active:
        raise UnactiveException
    return user


@router.get("/me", response_model=OutGetUserSchema)
def get_self_info(
    user: OutGetUserSchema = Depends(get_auth_user),
):
    return user
