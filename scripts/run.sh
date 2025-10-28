#!/bin/bash
set -e

# 🔹 Читаем версию из pyproject.toml
VERSION=$(grep -E '^version\s*=' pyproject.toml | sed 's/version\s*=\s*"\(.*\)"/\1/')
NAME=$(grep -E '^name\s*=' pyproject.toml | sed 's/name\s*=\s*"\(.*\)"/\1/')

# 🔹 Формируем тег образа
IMAGE_NAME="${NAME}:${VERSION}"
echo "📦 Using image: $IMAGE_NAME"

export IMAGE_NAME



# 🔹 Поднимаем сервисы в фоне
docker compose up --build -d

# 🔹 Показываем последние 50 строк логов после сборки
echo "📄 Build logs:"
docker compose logs --tail=50

echo "✅ Docker-compose started successfully. Containers running in background."
