from app.database import Base, db_master
from app.exceptions import BaseAppException, BaseErrorCode
from app.auth import auth_manager


"""Подключение внешних зависимостей к пакету 
(для изоляции пакета и ухода от циклических зависимостей)

    -->> Base - Настроенный внешний базовый класс sql(DeclarativeBase)
         *так же используется для подключения моделей пакета к alembic через
         импорт в app.database.models_registry



"""
__all__ = [
    "Base",  # Настроенный внешний базовый класс sql - DeclarativeBase -->>  он же используется в app.database
    "db_master",
    "auth_manager", 
    "BaseAppException",  # Настроенный внешний  базовый  - HTTPException
    "BaseErrorCode", # Пользовательские сообщения
]
