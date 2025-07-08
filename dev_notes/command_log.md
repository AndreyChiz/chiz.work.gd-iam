## How to & tutorials

- https://docs.astral.sh/uv/guides/integration/fastapi/ - интеграция fastapi --> uv
- https://vkvideo.ru/video-220000737_456239229 - базовая настройка
- https://vkvideo.ru/video-220000737_456239249 - регистрация аутентификация ...

## Initialization

```sh
 uv init --app
 uv add fastapi --extra standard
```

## RUN comands

### dev
```sh
uv run fastapi dev
```
### prod

```sh
fastapi run "app/main.py" --host 8010 --port 80
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