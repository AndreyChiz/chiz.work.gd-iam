# IAM Service (HTTP + AMQP)

A centralized identity and access management (IAM) microservice that provides:

- User registration and login via HTTP and AMQP
- JWT and session-based authentication
- Role-based access control (RBAC)
- Admin panel for managing users and permissions
- Swagger UI for API interaction and testing

## Features

- 🔐 Authentication via HTTP (REST) and AMQP (MQTT-style)
- 🧾 JSON Web Token (JWT) and session storage (Redis)
- ⚙️ Admin UI (optional)
- 📚 Auto-generated OpenAPI docs (Swagger UI)

## Requirements

- Python 3.12+
- Redis
- MQTT broker 

## Quickstart

1. Create Postgres database instance with settings like in app/config.py 
2. Uncomment vars in app/config.py or add .env with each vars
3. 
```bash
uv sync
docker-compose up -d
source .venv/bin/activate
alembic upgrade head 
uv run fastapi dev
```
