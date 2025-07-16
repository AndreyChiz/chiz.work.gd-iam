from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_master
from app.services.auth import (
    LoginForm,
    UnautorisedException,
    UnactiveException,
    TokenResponse,
    auth_service,
)
from app.services.user import user_crud


router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
    form: LoginForm = Depends(),
):
    username = form.username
    password = form.password
    if not (
        (user := await user_crud.get(session, username))
        and (auth_service.password.validate_password(password, user.password_hash))
    ):
        raise UnautorisedException
    if not user.is_active:
        raise UnactiveException

    access_token = auth_service.get_jwt_token(user)

    return TokenResponse(access_token=access_token)
