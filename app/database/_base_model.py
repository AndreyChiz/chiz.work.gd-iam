import datetime
import uuid
from typing import Any
from sqlalchemy import text, event, DateTime, func, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as types_Uuid
from sqlalchemy.ext.declarative import declared_attr

from . import settings
from ._utils import camel_case_to_snake_case


class CommonAttrsMixin:
    """Set common fields in models

    use --> set in model __include_uuid_id__: bool = True for adding field
    """

    __include_uuid_id__: bool = False
    __include_created_at__: bool = False
    __include_updated_at__: bool = False

    @declared_attr
    def id(cls) -> Mapped[uuid.UUID]:
        if cls.__include_uuid_id__:
            return mapped_column(
                types_Uuid(as_uuid=True),
                primary_key=True,
                server_default=text("gen_random_uuid()"),
            )

    @declared_attr
    def created_at(cls) -> Mapped[datetime.datetime]:
        if cls.__include_created_at__:
            return mapped_column(
                nullable=False,
                server_default=func.CURRENT_TIMESTAMP(),
                type_=DateTime(timezone=True),
            )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime.datetime]:
        if cls.__include_updated_at__:
            return mapped_column(
                server_default=None,
                server_onupdate=func.CURRENT_TIMESTAMP(),
                type_=DateTime(timezone=True),
            )


class Base(CommonAttrsMixin, DeclarativeBase):
    """Base settings for models"""

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
