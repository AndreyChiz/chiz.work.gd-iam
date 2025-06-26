## Initialization

https://docs.astral.sh/uv/guides/integration/fastapi/

```sh
 uv init --app
 uv add fastapi --extra standard
```
## dev run

```sh
uv run fastapi dev
```

```sh
 uv add pydantic-settings
 uv add "sqlalchemy[asyncio]"
 uv add asyncpg  
 uv add --dev pytest-asyncio
 ```
```sh
uv run pytest -v
```

## Alembic

```sh
 uv add --dev alembic   
alembic init -t async alembic
alembic revision --autogenerate -m "Initial"
alembic upgrade head 
```