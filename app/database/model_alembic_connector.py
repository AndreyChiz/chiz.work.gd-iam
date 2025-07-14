"""
Подключение моделей из пакетов приложения к Alembic для автогенерации миграций.

Импортируйте базовый класс (или модели), чтобы Alembic мог обнаружить их при автогенерации.

Пример:
    from app.user.external_deps import Base as AlembicAutogenerateUserModelsConnector
"""
from app.user.external_deps import Base as AlembicAutogenerateUserModelsConnector  # noqa: F401  # for Alembic autogeneration
