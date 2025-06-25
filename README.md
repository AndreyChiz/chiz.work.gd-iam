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

- Python 3.13+
- Redis
- MQTT broker 

## Quickstart

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload
