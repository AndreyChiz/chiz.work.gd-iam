#!/bin/bash
set -e

# Используем переменную $IMAGE_NAME из Jenkins
echo "🛠 Building Docker image: $IMAGE_NAME"

export DOCKER_BUILDKIT=1
docker build \
    --file Dockerfile \
    --tag "$IMAGE_NAME" \
    --progress=plain .