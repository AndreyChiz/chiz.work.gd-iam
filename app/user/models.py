from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import LargeBinary, DateTime, func


from app.database import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] 
    password: Mapped[str] = mapped_column(LargeBinary)
    role: Mapped[str]
    frmware_acces_group: Mapped[str]
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
    )
