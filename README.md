# chiz.work.gd-iam 🔐

[![Status](https://img.shields.io/badge/status-in%20development-yellow)](#)

> A centralized Identity and Access Management (IAM) microservice with HTTP + AMQP support.  
> Проект находится в активной разработке.

---

## 💡 Описание

`chiz.work.gd-iam` — это микросервис для централизованного управления пользователями и доступом.  
Он предоставляет:

- Регистрацию и авторизацию пользователей через HTTP и AMQP  
- JWT и сессионную аутентификацию  
- Ролевая модель доступа (RBAC)  
- Админ-панель для управления пользователями и правами  
- Swagger UI для тестирования и взаимодействия с API  

---

## ⚙️ Основные возможности

- 🔐 Аутентификация через HTTP (REST) и AMQP (MQTT-style)  
- 🧾 JSON Web Token (JWT) и сессии с хранением в Redis  
- ⚙️ Админ-панель (опционально)  
- 📚 Автоматическая генерация документации OpenAPI (Swagger UI)  

---

## 🛠 Требования

- Python 3.12+  
- Redis  
- MQTT broker  
- Postgres (для хранения данных пользователей)  

---

## 🚀 Быстрый старт

```bash
# Создать базу данных Postgres согласно настройкам в app/config.py

# Скопировать шаблон .env
cp .env.template .env

# Запустить docker-compose
docker-compose up -d

# Активировать виртуальное окружение
source .venv/bin/activate

# Применить миграции Alembic
alembic upgrade head

# Создать ключи для JWT
mkdir -p ./app.services/app/.keys
openssl genrsa -out ./app.services/app/.keys/jwt-private.pem 2048
openssl rsa -in ./app.services/app/.keys/jwt-private.pem -outform PEM -pubout -out ./app.services/app/.keys/jwt-public.pem

# Запуск FastAPI в dev режиме
./scripts/run.sh
