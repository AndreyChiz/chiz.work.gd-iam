## How to & tutorials

- https://docs.astral.sh/uv/guides/integration/fastapi/ - интеграция fastapi --> uv
- https://vkvideo.ru/video-220000737_456239229 - базовая настройка
- https://vkvideo.ru/video-220000737_456239249 - регистрация аутентификация ...
- https://vkvideo.ru/video-220000737_456239168 - jwt
- https://jwt.io/ 

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

## JWT
- https://pyjwt.readthedocs.io/en/stable/

```sh
# generate private key
openssl genrsa -out jwt-private.pem 2048
# genetate public key
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

```