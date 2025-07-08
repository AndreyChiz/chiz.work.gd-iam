from typing import Any

from sqlalchemy import MetaData, event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from app.config import settings
from .utils import camel_case_to_snake_case





class Base(DeclarativeBase):
    """Base settings for all models"""

    __abstract__ = True

    metadata = MetaData(naming_convention=settings.database.naming_convention)

    @declared_attr
    def __tablename__(cls) -> str:
        """Automatic naming table"""
        return camel_case_to_snake_case(cls.__name__)

    def __repr__(self) -> str:
        values = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        )
        return f"{self.__class__.__name__}({values})"

    def to_dict(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }

    def to_json(self) -> str:
        import json

        return json.dumps(self.to_dict(), default=str)


@event.listens_for(Base, "before_update")
def receive_before_update(mapper, connection, target):
    print(f"Updating {target.__tablename__}: {target}")


@event.listens_for(Base, "before_insert")
def receive_before_insert(mapper, connection, target):
    print(f"Inserting into {target.__tablename__}: {target}")

