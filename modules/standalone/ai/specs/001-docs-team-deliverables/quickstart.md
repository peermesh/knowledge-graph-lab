# Quick Start Guide: AI Development Module

**Last Updated**: 2025-10-20  
**Module**: AI Development Module  
**Version**: 1.0.0

## Overview

The AI Development Module extracts entities and relationships from unstructured text, constructs knowledge graphs, and provides intelligent content analysis capabilities. This guide helps you get started with development, testing, and deployment.

---

## Prerequisites

### Required Software
- **Python**: 3.11 or higher
- **Docker**: For running PostgreSQL, Qdrant, and RabbitMQ locally
- **Git**: For version control

### Required Services
- **PostgreSQL 15+**: Structured data storage
- **Qdrant**: Vector database for embeddings
- **RabbitMQ**: Message queue for async processing

### API Keys
- **OpenAI API Key**: For GPT-4/GPT-3.5-turbo (entity extraction)
- **Anthropic API Key**: For Claude (fallback provider)

---

## Quick Setup (5 minutes)

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/knowledge-graph-lab/ai-module.git
cd ai-module

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Services with Docker Compose

```bash
# Start PostgreSQL, Qdrant, and RabbitMQ
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys and configuration
nano .env  # or your preferred editor
```

**Required Environment Variables**:
```env
# Database
DATABASE_URL=postgresql://ai_user:password@localhost:5432/ai_module

# Qdrant Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-qdrant-key

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672

# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Configuration
LOG_LEVEL=INFO
PROCESSING_WORKERS=4
MAX_DAILY_COST=50.00
```

### 4. Initialize Database

```bash
# Run database migrations
python -m alembic upgrade head

# Optional: Seed with sample data
python scripts/seed_database.py
```

### 5. Start the API Server

```bash
# Start FastAPI server
uvicorn src.ai.api.main:app --reload --port 8000
```

**Verify**: Navigate to http://localhost:8000/docs for interactive API documentation

---

## Project Structure

```
src/ai/
├── models/              # Data models (SQLAlchemy + Pydantic)
│   ├── entity.py
│   ├── relationship.py
│   ├── knowledge_graph.py
│   └── processing_job.py
├── services/            # Business logic
│   ├── entity_extractor.py
│   ├── relationship_mapper.py
│   ├── graph_builder.py
│   ├── vector_search.py
│   └── quality_monitor.py
├── api/                 # FastAPI endpoints
│   ├── main.py         # App initialization
│   ├── extraction.py   # Entity extraction endpoints
│   ├── graph_query.py  # Knowledge graph endpoints
│   ├── content_analysis.py
│   └── health.py       # Health check endpoints
├── integrations/        # External service clients
│   ├── llm_client.py   # LangChain LLM interface
│   ├── vector_db.py    # Qdrant client
│   ├── postgres.py     # Database client
│   └── message_queue.py # RabbitMQ client
└── lib/                 # Shared utilities
    ├── confidence_scoring.py
    ├── deduplication.py
    └── text_processing.py

tests/
├── contract/            # API contract tests
├── integration/         # Integration tests
└── unit/                # Unit tests

specs/001-docs-team-deliverables/
├── spec.md             # Feature specification
├── plan.md             # Implementation plan
├── research.md         # Technology decisions
├── data-model.md       # Database schemas
├── quickstart.md       # This file
└── contracts/          # OpenAPI specifications
    ├── entity-extraction-api.yaml
    ├── knowledge-graph-api.yaml
    └── content-analysis-api.yaml
```

---

## Common Tasks

### Extract Entities from a Document

```bash
# Using curl
curl -X POST http://localhost:8000/ai/v1/extract-entities \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "document_id": "550e8400-e29b-41d4-a716-446655440000",
    "content": "Microsoft invested $10 billion in OpenAI to accelerate AI development.",
    "document_type": "text",
    "extraction_config": {
      "entity_types": ["organization", "person", "funding_amount"],
      "confidence_threshold": 0.7,
      "language": "en"
    },
    "priority": "normal"
  }'
```

### Query Knowledge Graph

```bash
curl -X POST http://localhost:8000/ai/v1/graph/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "query": "OpenAI funding",
    "query_type": "entity_search",
    "filters": {
      "entity_types": ["organization"],
      "confidence_threshold": 0.8,
      "limit": 20
    }
  }'
```

### Run Tests

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/

# Run with coverage
pytest --cov=src/ai --cov-report=html

# View coverage report
open htmlcov/index.html  # On macOS/Linux
start htmlcov/index.html  # On Windows
```

### Monitor Quality Metrics

```bash
# View processing metrics
python scripts/view_metrics.py --period=24h

# Generate quality report
python scripts/generate_quality_report.py --output=report.html
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Write Tests First (TDD)

```python
# tests/unit/test_entity_extractor.py
import pytest
from src.ai.services.entity_extractor import EntityExtractor

def test_extract_organizations():
    extractor = EntityExtractor()
    text = "Microsoft and OpenAI are collaborating."
    
    entities = extractor.extract(text, entity_types=["organization"])
    
    assert len(entities) == 2
    assert any(e.text == "Microsoft" for e in entities)
    assert any(e.text == "OpenAI" for e in entities)
```

### 3. Implement Feature

```python
# src/ai/services/entity_extractor.py
from typing import List
from src.ai.models.entity import Entity

class EntityExtractor:
    def extract(self, text: str, entity_types: List[str]) -> List[Entity]:
        # Implementation here
        pass
```

### 4. Run Tests

```bash
pytest tests/unit/test_entity_extractor.py -v
```

### 5. Submit Pull Request

```bash
git add .
git commit -m "Add entity extraction for organizations"
git push origin feature/your-feature-name
```

---

## Debugging Tips

### Enable Debug Logging

```bash
# In .env
LOG_LEVEL=DEBUG

# Restart server
uvicorn src.ai.api.main:app --reload --log-level debug
```

### Check Service Health

```bash
curl http://localhost:8000/ai/v1/health
```

### View Database Tables

```bash
# Connect to PostgreSQL
docker exec -it ai-postgres psql -U ai_user -d ai_module

# List tables
\dt

# View entities
SELECT id, text, entity_type, confidence FROM extracted_entities LIMIT 10;
```

### Monitor Message Queue

```bash
# RabbitMQ Management UI
open http://localhost:15672
# Username: guest, Password: guest
```

### Debug LLM Calls

```python
# Add to your code
import logging
logging.basicConfig(level=logging.DEBUG)

# LangChain will log all LLM interactions
```

---

## Performance Optimization

### Database Connection Pooling

```python
# config/database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### Batch Processing

```python
# Process multiple documents at once
documents = [doc1, doc2, doc3, ...]
results = await extractor.extract_batch(documents, batch_size=10)
```

### Caching Frequent Queries

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_entity_by_text(text: str):
    return session.query(Entity).filter_by(text=text).first()
```

---

## Deployment

### Build Docker Image

```bash
docker build -t ai-module:latest .
```

### Deploy to AWS ECS

```bash
# Configure AWS CLI
aws configure

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_REPO
docker tag ai-module:latest YOUR_ECR_REPO/ai-module:latest
docker push YOUR_ECR_REPO/ai-module:latest

# Update ECS service
aws ecs update-service --cluster ai-cluster --service ai-module --force-new-deployment
```

### Environment-Specific Configuration

```bash
# Production
export ENV=production
export DATABASE_URL=postgresql://...  # Production database
export PROCESSING_WORKERS=8
export MAX_DAILY_COST=200.00

# Staging
export ENV=staging
export DATABASE_URL=postgresql://...  # Staging database
export PROCESSING_WORKERS=4
export MAX_DAILY_COST=50.00
```

---

## Troubleshooting

### Issue: Entity Extraction Failing

**Symptoms**: HTTP 500 errors from `/extract-entities`

**Solutions**:
1. Check LLM API keys are valid
2. Verify LLM API rate limits not exceeded
3. Review logs for specific error messages
4. Test with simpler document content

### Issue: Slow Query Performance

**Symptoms**: Knowledge graph queries taking >5 seconds

**Solutions**:
1. Check database indexes exist (`\di` in psql)
2. Analyze query execution plan (`EXPLAIN ANALYZE`)
3. Increase PostgreSQL shared_buffers
4. Consider adding entity_type-specific indexes

### Issue: High Memory Usage

**Symptoms**: Workers using >8GB memory

**Solutions**:
1. Enable vector quantization in Qdrant
2. Reduce batch size for embedding operations
3. Clear entity cache periodically
4. Check for memory leaks in long-running workers

---

## Additional Resources

### API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Specs**: `specs/001-docs-team-deliverables/contracts/`

### Architecture Documentation
- **Implementation Plan**: `specs/001-docs-team-deliverables/plan.md`
- **Data Model**: `specs/001-docs-team-deliverables/data-model.md`
- **Research Decisions**: `specs/001-docs-team-deliverables/research.md`

### External Documentation
- **FastAPI**: https://fastapi.tiangolo.com/
- **LangChain**: https://python.langchain.com/docs/
- **Qdrant**: https://qdrant.tech/documentation/
- **SQLAlchemy**: https://docs.sqlalchemy.org/

---

## Getting Help

### Internal Support
- **Slack**: #ai-module-dev
- **Email**: ai-team@knowledge-graph-lab.com
- **Office Hours**: Mondays 2-3 PM EST

### Reporting Issues
- **GitHub Issues**: https://github.com/knowledge-graph-lab/ai-module/issues
- **Bug Template**: Include logs, reproduction steps, environment details

---

**Quick Start Complete!** You're ready to develop and extend the AI module. For detailed implementation guidance, see `plan.md` and `research.md`.
