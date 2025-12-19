#!/bin/bash
# Development startup script for AI Module

set -e

echo "🚀 Starting AI Development Module - Development Mode"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Start services
echo "📦 Starting PostgreSQL, Qdrant, and RabbitMQ..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys before continuing!"
    echo "   Required: OPENAI_API_KEY"
    exit 1
fi

# Run database migrations
echo "🗄️  Running database migrations..."
alembic upgrade head || echo "⚠️  Migrations may have failed. Check if database is ready."

# Start FastAPI server
echo "🌐 Starting FastAPI server..."
echo "=================================================="
echo "📍 API Server: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/ai/v1/health"
echo "=================================================="
echo ""

uvicorn src.ai.api.main:app --reload --port 8000

