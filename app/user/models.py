from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, LargeBinary



from database import Base


class User(Base):
    __include_uuid_id__ = True
    __include_created_at__ = True
    __include_updated_at__ = True

    
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    password: Mapped[LargeBinary] =  mapped_column(LargeBinary)


