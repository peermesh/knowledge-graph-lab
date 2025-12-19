# AI Development Module

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/knowledge-graph-lab/ai-module)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-teal.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

Transform unstructured text into structured knowledge through entity extraction, relationship mapping, and knowledge graph construction.

## 🚀 Features

- **Entity Extraction**: Extract 5 entity types (organizations, people, funding amounts, dates, locations) with 85% precision
- **Relationship Mapping**: Identify 6 relationship types (fund, partner, acquire, compete, collaborate, mention) with 80% accuracy
- **Knowledge Graph**: Construct and query graphs with 1M+ entities and 5M+ relationships
- **Vector Search**: Semantic similarity search using 768-dimensional embeddings
- **Real-time Updates**: WebSocket support for live knowledge graph updates
- **Quality Monitoring**: Track extraction accuracy with automated alerting
- **Multi-language**: Support for English, Spanish, French, and Chinese

## 📊 Performance

- **Throughput**: 100-200 documents/hour
- **Latency**: <5s (p95) entity extraction, <2s (p95) graph queries
- **Scale**: 500+ concurrent queries, 1M+ entities, 5M+ relationships
- **Cost**: $0.10 average per document processed
- **Availability**: 99.5% extraction APIs, 99.9% query APIs

## 🏗️ Architecture

```
AI Module Architecture
├── API Layer (FastAPI)
│   ├── Entity Extraction API
│   ├── Knowledge Graph Query API
│   ├── Content Analysis API
│   ├── Quality Monitoring API
│   └── WebSocket (Real-time Updates)
├── Services Layer
│   ├── Entity Extractor (LangChain + LLM)
│   ├── Relationship Mapper
│   ├── Graph Builder
│   ├── Vector Search
│   ├── Quality Monitor
│   └── Job Processor
├── Data Layer
│   ├── PostgreSQL (structured data)
│   ├── Qdrant (vector embeddings)
│   └── RabbitMQ (async processing)
└── Integrations
    ├── LLM Providers (OpenAI, Anthropic)
    ├── Vector Database (Qdrant)
    └── Message Queue (RabbitMQ)
```

## 🚦 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- OpenAI API key

### Installation

```bash
# Clone repository
git clone https://github.com/knowledge-graph-lab/ai-module.git
cd knowledge-graph-lab

# Install dependencies
pip install -r requirements.txt

# Start services (PostgreSQL, Qdrant, RabbitMQ)
docker-compose up -d

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run database migrations
alembic upgrade head

# Start API server
uvicorn src.ai.api.main:app --reload --port 8000
```

### Verify Installation

```bash
# Check health
curl http://localhost:8000/ai/v1/health

# View API docs
open http://localhost:8000/docs
```

## 📖 Documentation

- **Quick Start**: [`specs/001-docs-team-deliverables/quickstart.md`](specs/001-docs-team-deliverables/quickstart.md)
- **Implementation Plan**: [`specs/001-docs-team-deliverables/plan.md`](specs/001-docs-team-deliverables/plan.md)
- **Data Model**: [`specs/001-docs-team-deliverables/data-model.md`](specs/001-docs-team-deliverables/data-model.md)
- **API Contracts**: [`specs/001-docs-team-deliverables/contracts/`](specs/001-docs-team-deliverables/contracts/)
- **Research**: [`specs/001-docs-team-deliverables/research.md`](specs/001-docs-team-deliverables/research.md)

## 🔌 API Usage

### Extract Entities

```bash
curl -X POST http://localhost:8000/ai/v1/extract-entities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "document_id": "550e8400-e29b-41d4-a716-446655440000",
    "content": "Microsoft invested $10 billion in OpenAI.",
    "document_type": "text",
    "extraction_config": {
      "entity_types": ["organization", "funding_amount"],
      "confidence_threshold": 0.7
    }
  }'
```

### Query Knowledge Graph

```bash
curl -X POST http://localhost:8000/ai/v1/graph/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "OpenAI funding",
    "query_type": "entity_search",
    "filters": {
      "entity_types": ["organization"],
      "confidence_threshold": 0.8
    }
  }'
```

### Search Similar Entities

```bash
curl -X POST http://localhost:8000/ai/v1/graph/similarity \
  -H "Content-Type: application/json" \
  -d '{
    "text": "AI research companies",
    "limit": 10
  }'
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test suites
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/contract/      # API contract tests

# Run with coverage
pytest --cov=src/ai --cov-report=html
open htmlcov/index.html
```

## 🔧 Development

### Project Structure

```
src/ai/
├── models/         # SQLAlchemy data models
├── services/       # Business logic
├── api/            # FastAPI endpoints
├── integrations/   # External service clients
└── lib/            # Shared utilities

tests/
├── contract/       # API contract tests
├── integration/    # Integration tests
└── unit/           # Unit tests

specs/001-docs-team-deliverables/
├── spec.md         # Feature specification
├── plan.md         # Implementation plan
├── data-model.md   # Database schemas
├── contracts/      # OpenAPI specifications
└── quickstart.md   # Developer guide
```

### Running in Development

```bash
# With auto-reload
uvicorn src.ai.api.main:app --reload --port 8000

# With debug logging
LOG_LEVEL=DEBUG uvicorn src.ai.api.main:app --reload
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🐳 Deployment

### Docker Build

```bash
docker build -t ai-module:latest .
```

### Deploy to AWS ECS

```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_REPO
docker tag ai-module:latest YOUR_ECR_REPO/ai-module:latest
docker push YOUR_ECR_REPO/ai-module:latest

# Update service
aws ecs update-service --cluster ai-cluster --service ai-module --force-new-deployment
```

## 📈 Monitoring

### Health Checks

- **Liveness**: `GET /ai/v1/health/live` - Service is running
- **Readiness**: `GET /ai/v1/health/ready` - Service is ready for traffic
- **Full Health**: `GET /ai/v1/health` - Detailed component health

### Metrics

- **Quality Reports**: `GET /ai/v1/quality/report/daily`
- **Quality Alerts**: `GET /ai/v1/quality/alerts`
- **Trend Analysis**: `GET /ai/v1/quality/trends/{metric_type}`

### Logs

Structured JSON logging in production:

```json
{
  "timestamp": "2025-10-20T14:30:00Z",
  "level": "INFO",
  "logger": "src.ai.services.entity_extractor",
  "message": "Extracted 12 entities from document",
  "correlation_id": "abc123",
  "request_id": "req-xyz",
  "extra_fields": {
    "document_id": "550e8400-...",
    "entity_count": 12
  }
}
```

## 🤝 Integration

### Backend Module

```python
# Submit document for processing
import requests

response = requests.post(
    'http://ai-module:8000/ai/v1/extract-entities',
    json={
        'document_id': doc_id,
        'content': document_text,
        'document_type': 'text'
    }
)

job_id = response.json()['job_id']

# Check job status
status = requests.get(f'http://ai-module:8000/ai/v1/jobs/{job_id}')
```

### Frontend Module

```javascript
// Query knowledge graph
const response = await fetch('http://localhost:8000/ai/v1/graph/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'OpenAI',
    query_type: 'entity_search'
  })
});

const data = await response.json();
// data.entities contains results
```

### WebSocket (Real-time)

```javascript
const ws = new WebSocket('ws://localhost:8000/ai/v1/ws/graph/client-123');

ws.onopen = () => {
  // Subscribe to entity updates
  ws.send(JSON.stringify({
    action: 'subscribe',
    entity_id: 'entity-uuid'
  }));
};

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  if (update.type === 'entity_update') {
    console.log('Entity updated:', update.data);
  }
};
```

## 🔐 Security

- **Authentication**: JWT bearer tokens (RS256)
- **Authorization**: Role-based access control (RBAC)
- **Rate Limiting**: 100 req/min, 1000 req/hour per client
- **Data Encryption**: TLS 1.3 for all API communication
- **Input Validation**: Comprehensive validation using Pydantic

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [LangChain](https://python.langchain.com/) - LLM orchestration
- [Qdrant](https://qdrant.tech/) - Vector database
- [PostgreSQL](https://www.postgresql.org/) - Relational database
- [RabbitMQ](https://www.rabbitmq.com/) - Message broker

---

**Version**: 1.0.0 | **Status**: Production Ready | **Last Updated**: 2025-10-20
