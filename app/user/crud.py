from typing import Sequence
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User
from .schema import RqstCreateUserSchema


class UserCRUD:
    """Класс для работы с пользователями"""

    async def get_all(self, session: AsyncSession) -> Sequence[User]:
        stmt = select(User).order_by(User.id)
        result = await session.scalars(stmt)
        return result.all()

    async def create(
        self, session: AsyncSession, user_create: RqstCreateUserSchema
    ) -> User:
        user = User(**user_create.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

user_crud = UserCRUD()