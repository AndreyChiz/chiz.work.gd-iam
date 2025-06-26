from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, LargeBinary, DateTime, Boolean, func


from app.database import Base


class User(Base):
    username: Mapped[String]
    password: Mapped[LargeBinary]
    created_at: Mapped[DateTime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP(),
        type_=DateTime(timezone=True),
    )
    updated_at: Mapped[DateTime] = mapped_column(
        nullable=True,
        server_onupdate=func.CURRENT_TIMESTAMP(),
        type_=DateTime(timezone=True),
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
