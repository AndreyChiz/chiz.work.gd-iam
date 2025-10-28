#!/bin/bash
set -e

# 🔹 Читаем версию из pyproject.toml
VERSION=$(grep -E '^version\s*=' pyproject.toml | sed 's/version\s*=\s*"\(.*\)"/\1/')
NAME=$(grep -E '^name\s*=' pyproject.toml | sed 's/name\s*=\s*"\(.*\)"/\1/')

# 🔹 Формируем тег образа
IMAGE_NAME="${NAME}:${VERSION}"
echo "📦 Using image: $IMAGE_NAME"

export IMAGE_NAME

# 🔹 Если задан реестр и креды, логинимся
if [[ -n "$REGISTRY" && -n "$DOCKER_USER" && -n "$DOCKER_PASS" ]]; then
    echo "🔐 Logging in to registry $REGISTRY as $DOCKER_USER"
    echo "$DOCKER_PASS" | docker login "$REGISTRY" -u "$DOCKER_USER" --password-stdin
    echo "✅ Login successful"
else
    echo "⚠️ Registry login skipped: REGISTRY, DOCKER_USER or DOCKER_PASS is empty"
fi

# 🔹 Поднимаем сервисы в фоне
docker compose up --build -d

# 🔹 Показываем последние 50 строк логов после сборки
echo "📄 Build logs:"
docker compose logs --tail=50

echo "✅ Docker-compose started successfully. Containers running in background."
