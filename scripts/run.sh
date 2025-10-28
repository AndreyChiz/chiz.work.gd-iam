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
docker-compose up --build -d

# 🔹 Фолловим логи только во время сборки
echo "📄 Following logs..."
docker-compose logs -f --tail=50

# 🔹 После отображения логов сборки можно отпустить контейнеры в фоне
echo "✅ Docker-compose started successfully. Containers running in background."
