# Install uv
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --link-mode=copy --no-install-project --no-editable --no-group dev

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked  --no-editable --link-mode=copy --no-group dev

FROM python:3.12-slim

COPY --from=builder --chown=app:app /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["gunicorn"]

CMD [\
    "-k", "uvicorn.workers.UvicornWorker",\
    "app.main:app",\
    "--bind", "0.0.0.0:8080",\
    "--workers", "1",\
    "--log-level", "debug",\
    "--capture-output"\
    ]