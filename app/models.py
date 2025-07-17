from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text, ForeignKey

from app.database import Base


class User(Base):
    __include_id__ = True
    __id_type__ = "int"
    __include_created_at__ = True
    __include_updated_at__ = True

    username: Mapped[str] = mapped_column(index=True, unique=True)
    password_hash: Mapped[bytes]  # TODO = mapped_column(LargeBinary)

    is_active: Mapped[bool] = mapped_column(
        server_default=text("true"),
    )
    is_admin: Mapped[bool] = mapped_column(
        server_default=text("false"),
    )

#     refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
#         back_populates="user", cascade="all, delete-orphan"
#     )


# class RefreshToken(Base):
#     __include_id__ = True
#     __id_type__ = "uuid"
#     __include_created_at__= True
#     __include_updated_at__ = True


#     token_hash: Mapped[str] = mapped_column(index=True)
#     expires_at: Mapped[datetime]
#     created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
#     revoked: Mapped[bool] = mapped_column(default=False)

#     user_id: Mapped[int] = mapped_column(
#         ForeignKey("users.id", ondelete="CASCADE")
#     )
#     user: Mapped["User"] = relationship(back_populates="refresh_tokens")

#     user_agent: Mapped[str | None] = mapped_column(nullable=True)
#     ip_address: Mapped[str | None] = mapped_column(nullable=True)