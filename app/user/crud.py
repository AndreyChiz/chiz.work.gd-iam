from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, asc, desc
from .models import User
from .schema import UserQueryParams


class UserCRUD:
    """Класс для работы с пользователями"""

    async def get_all(self, session: AsyncSession, query: UserQueryParams):
        filters = []

        if query.id is not None:
            filters.append(User.id == query.id)
        if query.username:
            filters.append(User.username.ilike(f"%{query.username}%"))
        if query.is_active is not None:
            filters.append(User.is_active == query.is_active)
        if query.is_admin is not None:
            filters.append(User.is_admin == query.is_admin)
        if query.created_from:
            filters.append(User.created_at >= query.created_from)
        if query.created_to:
            filters.append(User.created_at <= query.created_to)

        order_column = getattr(User, query.order_by)
        order_func = asc if query.order_dir == "asc" else desc

        stmt = (
            select(User)
            .where(and_(*filters))
            .order_by(order_func(order_column))
            .offset(query.offset)
            .limit(query.limit)
        )

        result = await session.execute(stmt)
        return result.scalars().all()

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
