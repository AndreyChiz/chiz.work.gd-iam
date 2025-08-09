from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, asc, desc
from app.models import User
from .schema import UserFilterDep, UserPaginationDep


class UserCRUD:
    """Класс для работы с пользователями"""

    async def get_by_name(self, session: AsyncSession, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def get_by_id(self, session: AsyncSession, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def get_many(
        self,
        session: AsyncSession,
        
        user_filters: UserFilterDep,
        user_pagination: UserPaginationDep,
    ):
        filters = []

        if user_filters.id is not None:
            filters.append(User.id == user_filters.id)
        if user_filters.username:
            filters.append(User.username.ilike(f"%{user_filters.username}%"))
        if user_filters.is_active is not None:
            filters.append(User.is_active == user_filters.is_active)
        if user_filters.is_admin is not None:
            filters.append(User.is_admin == user_filters.is_admin)
        if user_filters.created_from:
            filters.append(User.created_at >= user_filters.created_from)
        if user_filters.created_to:
            filters.append(User.created_at <= user_filters.created_to)

        order_column = getattr(User, user_pagination.order_by)
        order_func = asc if user_pagination.order_dir == "asc" else desc

        stmt = (
            select(User)
            .where(and_(*filters))
            .order_by(order_func(order_column))
            .offset(user_pagination.offset)
            .limit(user_pagination.limit)
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
