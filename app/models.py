from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text

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
