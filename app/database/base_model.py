
from typing import Any
from typing import ClassVar

from sqlalchemy import DateTime, Integer, MetaData, event, func, text
from sqlalchemy.dialects.postgresql import UUID as types_Uuid
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.config import settings

from .utils import camel_case_to_snake_case
from typing import cast


class CommonAttrsMixin:
    """
    Для автоматического добавления часто используемых колонок в модели
    Применение:
    Пример с uuid:
    class UUIDModel(Base, CommonAttrsMixin):
        __include_id__ = True # включить добавление id
        __id_type__ = "uuid" # настроить тип id ("uuid" | "int")
        __include_created_at__ = True
        __include_updated_at__ = True

    Пример с int:
    class IntModel(Base, CommonAttrsMixin):
        __include_id__ = True
        __id_type__ = "int"
        __include_created_at__ = True
    """

    __include_id__: bool = False
    __id_type__: str = "uuid"  # или "int"
    __include_created_at__: bool = False
    __include_updated_at__: bool = False

    @declared_attr
    def id(cls) -> Mapped[Any]:
        if not cls.__include_id__:
            return cast(Mapped[Any], None)

        if cls.__id_type__ == "uuid":
            return mapped_column(
                types_Uuid(as_uuid=True),
                primary_key=True,
                server_default=text("gen_random_uuid()"),
            )
        elif cls.__id_type__ == "int":
            return mapped_column(
                Integer,
                primary_key=True,
                autoincrement=True,
            )
        else:
            raise ValueError(f"Unsupported id type: {cls.__id_type__}")

    @declared_attr
    def created_at(cls) -> Mapped[Any]:
        if cls.__include_created_at__:
            return mapped_column(
                nullable=False,
                server_default=func.CURRENT_TIMESTAMP(),
                type_=DateTime(timezone=True),
            )
        return cast(Mapped[Any], None)

    @declared_attr
    def updated_at(cls) -> Mapped[Any]:
        if cls.__include_updated_at__:
            return mapped_column(
                nullable=True,
                server_default=None,
                server_onupdate=func.CURRENT_TIMESTAMP(),
                type_=DateTime(timezone=True),
            )
        return cast(Mapped[Any], None)


class Base(
    CommonAttrsMixin,
    DeclarativeBase,
):
    """Base settings for all models"""

    __abstract__ = True


    metadata = MetaData(naming_convention=settings.database.naming_convention)

    @declared_attr # type: ignore
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
