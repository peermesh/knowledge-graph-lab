# AI Development Module

AI-powered entity extraction and knowledge graph management service for the Knowledge Graph Lab platform.

## Overview

The AI Development Module transforms unstructured text into structured knowledge through:

- **Entity Extraction**: Extract organizations, people, funding amounts, dates, and locations with 85%+ precision
- **Relationship Mapping**: Identify and score relationships between entities (fund, partner, acquire, etc.)
- **Knowledge Graph**: Build and maintain graph structures for relationship discovery
- **Multi-language Support**: Process content in English, Spanish, French, and Chinese
- **Quality Monitoring**: Track accuracy metrics and performance over time

## Features

- **Multi-Provider LLM Integration**: Support for OpenAI GPT-4, Anthropic Claude, and open-source models
- **Vector Similarity Search**: 768-dimensional embeddings with Qdrant for semantic search
- **Async Processing**: RabbitMQ-based job queuing for scalable document processing
- **Real-time APIs**: FastAPI endpoints with <200ms response times
- **Comprehensive Testing**: >85% test coverage with TDD approach

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7.0+
- RabbitMQ
- Qdrant vector database

### Installation

1. **Clone and setup**:
   ```bash
   cd src/ai-module
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment setup**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Database setup**:
   ```bash
   # Run migrations
   alembic upgrade head

   # Or create tables directly
   python -c "from app.core.database import create_tables; import asyncio; asyncio.run(create_tables())"
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

5. **Access the API**:
   - API Documentation: http://localhost:8001/docs
   - Health Check: http://localhost:8001/health

## API Endpoints

### Entity Management
- `GET /api/v1/entities` - List entities with filtering
- `POST /api/v1/entities` - Create new entity
- `GET /api/v1/entities/{id}` - Get entity by ID
- `PUT /api/v1/entities/{id}` - Update entity
- `DELETE /api/v1/entities/{id}` - Delete entity
- `POST /api/v1/entities/extract` - Extract entities from content

### Relationship Management
- `GET /api/v1/relationships` - List entity relationships
- `POST /api/v1/relationships` - Create relationship
- `GET /api/v1/relationships/graph/query` - Query knowledge graph
- `GET /api/v1/relationships/graph/traversal` - Traverse graph from entity

### System Health
- `GET /health` - Comprehensive health check
- `GET /ready` - Kubernetes readiness probe
- `GET /live` - Kubernetes liveness probe

## Configuration

The application uses environment variables for configuration:

```bash
# Database
POSTGRES_URL=postgresql+asyncpg://user:pass@localhost:5432/ai_module

# Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-qdrant-key

# Message Queue
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# LLM Providers
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Application
DEBUG=true
SECRET_KEY=your-secret-key
```

## Development

### Testing

Run the test suite:

```bash
pytest tests/ -v --cov=app
```

### Code Quality

```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint code
flake8 app/ tests/
mypy app/

# Run all checks
pre-commit run --all-files
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Docker Deployment

### Build and run with Docker Compose:

```bash
docker-compose up -d
```

### Production deployment:

```bash
# Build image
docker build -t ai-module:1.0.0 .

# Run container
docker run -p 8001:8001 \
  -e POSTGRES_URL=postgresql+asyncpg://... \
  -e OPENAI_API_KEY=... \
  ai-module:1.0.0
```

## Performance Targets

- **Entity Extraction**: 100 documents/hour, <5s latency (p95)
- **API Responses**: <200ms (p95), <500ms (p99)
- **Knowledge Graph Queries**: <2s (p95), <5s (p99)
- **Accuracy**: 85% precision, 80% recall for entity extraction
- **Uptime**: 99.5% availability with comprehensive monitoring

## Monitoring

The service provides comprehensive monitoring through:

- **Health Checks**: Database, vector DB, LLM providers, message queue
- **Performance Metrics**: Response times, throughput, error rates
- **Quality Metrics**: Extraction accuracy, confidence scoring validation
- **Resource Monitoring**: CPU, memory, database connections

## Integration

The AI module integrates with:

- **Backend Module**: Provides entity storage and retrieval APIs
- **Frontend Module**: Delivers data for graph visualization and search
- **Publishing Module**: Supplies content for personalization and distribution

## Contributing

1. Follow the established code style (black, isort, flake8)
2. Write tests for new functionality (TDD approach)
3. Update documentation for API changes
4. Ensure all tests pass before submitting PRs

## License

MIT License - see LICENSE file for details.

---

*Part of the Knowledge Graph Lab platform - Transforming information chaos into actionable intelligence.*
