from typing import Annotated

import jwt
from fastapi import APIRouter, Cookie, Depends, Response, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_master
from app.exceptions import (
    AlreadyExistException,
    NoRefreshToken,
    RefreshTokenExpireException,
    RefreshTokenInvalidException,
    UnactiveException,
    UnautorisedException,
)
from app.services.auth import (
    InRegisterSchema,
    LoginFormSchema,
    OutRegisterSchema,
    TokenResponseSchema,
    auth_service,
)
from app.services.user import user_crud

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=OutRegisterSchema,
)
async def register_user(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
    new_user: InRegisterSchema,
):
    try:
        user = await user_crud.create(
            session=session,
            username=new_user.username,
            password_hash=auth_service.password.hash(
                new_user.password.get_secret_value()
            ),
        )
    except IntegrityError:
        raise AlreadyExistException

    return user


@router.post(
    "/login",
    response_model=TokenResponseSchema,
)
async def login(
    response: Response,
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
    form: LoginFormSchema = Depends(),
):
    username = form.username
    password = form.password
    if not (
        (user := await user_crud.get_by_name(session, username))
        and (auth_service.password.validate_password(password, user.password_hash))
    ):
        raise UnautorisedException
    if not user.is_active:
        raise UnactiveException

    access_token = auth_service.create_access_token(user)
    refresh_token = auth_service.create_refresh_token(user)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        # secure=True,
        samesite="lax",
    )

    return TokenResponseSchema(
        access_token=access_token
    )


@router.post("/auth/refresh")  # TODO CHECK!!!!!!!!
async def refresh_token(
    session: Annotated[AsyncSession, Depends(db_master.session_getter)],
    refresh_token: str = Cookie(None),
):
    if refresh_token is None:
        raise NoRefreshToken

    try:
        print(refresh_token)
        payload = auth_service.token.decode_payload(refresh_token)
    except jwt.ExpiredSignatureError:
        raise RefreshTokenExpireException
    except jwt.PyJWTError:
        raise RefreshTokenInvalidException
    try:
        user_id = int(payload.get("sub"))  # type: ignore
    except TypeError:
        raise RefreshTokenInvalidException

    if not (user := await user_crud.get_by_id(session, user_id=user_id)):
        raise UnautorisedException
    if not user.is_active:
        raise UnactiveException

    new_access_token = auth_service.create_access_token(user)

    return TokenResponseSchema(

        access_token=new_access_token,
    )
