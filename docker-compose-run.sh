#!/bin/bash
# Docker Compose wrapper script
# Uses Docker Desktop's docker binary

DOCKER_BIN="/Applications/Docker.app/Contents/Resources/bin/docker"

if [ ! -f "$DOCKER_BIN" ]; then
    echo "❌ Docker Desktop not found at $DOCKER_BIN"
    echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker Desktop is running
if ! "$DOCKER_BIN" info > /dev/null 2>&1; then
    echo "❌ Docker Desktop is not running"
    echo "Please start Docker Desktop and try again"
    exit 1
fi

# Run docker compose commands
"$DOCKER_BIN" compose "$@"


