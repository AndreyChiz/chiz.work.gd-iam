from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import LargeBinary

import enum
from sqlalchemy import Enum


from app.database import Base

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __include_id__ = True
    __id_type__ = "int"
    __include_created_at__ = True
    __include_updated_at__ = True

    username: Mapped[str]
    password: Mapped[str] #TODO = mapped_column(LargeBinary)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False,
    )
    frmware_acces_group: Mapped[str | None]  # TODO add comments to fields
    # TODO Check nullable marks

    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
