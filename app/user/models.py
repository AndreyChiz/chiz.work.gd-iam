from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import LargeBinary, DateTime, func


from app.database import Base


class User(Base):

    __include_id__ = True
    __id_type__ = "uuid"
    __include_created_at__ = True
    __include_updated_at__ = True

    username: Mapped[str] 
    password: Mapped[str] = mapped_column(LargeBinary)
    role: Mapped[str]
    frmware_acces_groups: Mapped[str]

    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
