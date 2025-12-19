# Development startup script for AI Module (PowerShell)

Write-Host "Starting AI Development Module - Development Mode" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Error: Docker is not running. Please start Docker first." -ForegroundColor Red
    exit 1
}

# Start services
Write-Host "Starting PostgreSQL, Qdrant, and RabbitMQ..." -ForegroundColor Cyan
docker-compose up -d

# Wait for services to be ready
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "WARNING: No .env file found. Copying from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "WARNING: Please edit .env with your API keys before continuing!" -ForegroundColor Yellow
    Write-Host "   Required: OPENAI_API_KEY" -ForegroundColor Yellow
    exit 1
}

# Run database migrations
Write-Host "Running database migrations..." -ForegroundColor Cyan
try {
    alembic upgrade head
} catch {
    Write-Host "WARNING: Migrations may have failed. Check if database is ready." -ForegroundColor Yellow
}

# Start FastAPI server
Write-Host "Starting FastAPI server..." -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Green
Write-Host "API Server: http://localhost:8000" -ForegroundColor White
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "Health Check: http://localhost:8000/ai/v1/health" -ForegroundColor White
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""

uvicorn src.ai.api.main:app --reload --port 8000

