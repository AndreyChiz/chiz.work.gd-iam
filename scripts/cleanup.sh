#!/bin/bash
set -e

echo "🧹 Cleaning up dangling images and containers..."
docker image prune -f
docker container prune -f
