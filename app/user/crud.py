from typing import Sequence


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User


class UserCRUD:
    """Класс для работы с пользователями"""

    async def get_all(self, session: AsyncSession) -> Sequence[User]:
        stmt = select(User).order_by(User.id)
        result = await session.scalars(stmt)
        return result.all()

    async def create(
        self,
        session: AsyncSession,
        username: str,
        password_hash: bytes,
    ) -> User:
        user = User(
            username=username,
            password_hash=password_hash,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


user_crud = UserCRUD()
