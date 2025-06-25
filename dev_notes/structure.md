# FastAPI Microservice Boilerplate

Минимальный, оптимизированный микросервис на FastAPI с Alembic и Docker. Подходит для продакшен-старта.

## 📁 Структура проекта

```
project_name/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   └── models/
│   │       ├── __init__.py
│   │       └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── crud/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── main.py
│   └── deps.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── alembic.ini
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔧 Основные файлы

### `app/main.py`
```python
from fastapi import FastAPI
from app.api.v1 import routes

app = FastAPI()
app.include_router(routes.router, prefix="/api/v1")
```

---

### `app/core/config.py`
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://user:password@db/dbname"

settings = Settings()
```

---

### `app/db/session.py`
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

---

### 📦 Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 🐳 docker-compose.yml
```yaml
version: "3.9"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql+psycopg2://user:password@db/dbname

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: dbname
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

---

### 📜 requirements.txt
```txt
fastapi
uvicorn[standard]
sqlalchemy[asyncio]
alembic
asyncpg
```

---

### 🧪 Миграции
```bash
# Инициализация Alembic
alembic init alembic

# Создание миграции
alembic revision --autogenerate -m "init"

# Применение миграции
alembic upgrade head
```
