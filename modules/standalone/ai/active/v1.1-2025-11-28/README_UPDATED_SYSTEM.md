# Knowledge Graph Lab - Updated System

## Overview

This is a completely rebuilt version of the Knowledge Graph Lab system according to the updated specification (spec.md). The system now features:

- **Flexible Entity Extraction**: No restrictions on entity types
- **Dynamic Relationship Mapping**: Support for any relationship types
- **Configurable Vector Embeddings**: Dynamic dimensional embeddings (default: 384)
- **Simplified Architecture**: Removed multi-language complexity
- **Scalable Processing**: High-performance async processing

## Key Changes from Previous Version

### ✅ Removed Restrictions
- **Entity Types**: No longer restricted to 5 core types (organization, person, funding_amount, date, location)
- **Relationship Types**: No longer restricted to 6 core types (fund, partner, acquire, compete, collaborate, mention)
- **Embedding Dimensions**: No longer fixed to 768 dimensions
- **Multi-language Support**: Simplified to focus on core functionality

### ✅ Enhanced Flexibility
- **Dynamic Type Detection**: System can identify any relevant entity or relationship types
- **Configurable Embeddings**: Choose optimal dimensions for your use case (256, 384, 512, 768)
- **Flexible Confidence Scoring**: Adjustable thresholds for quality control
- **Scalable Architecture**: Configurable processing workers and concurrency

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file based on the configuration options below:

```bash
# Database
DATABASE_URL=postgresql://ai_user:password@localhost:5432/ai_module

# Vector Database
QDRANT_URL=http://localhost:6333

# LLM Providers (choose at least one)
OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Optional fallback

# Configuration
ENV=development
LOG_LEVEL=INFO
EMBEDDING_DIMENSIONS=384  # Options: 256, 384, 512, 768

# Processing
PROCESSING_WORKERS=4
MAX_CONCURRENT_JOBS=100

# Quality Control
MEDIUM_CONFIDENCE_THRESHOLD=0.70
HIGH_CONFIDENCE_THRESHOLD=0.85
```

### 3. Start Services
```bash
# Start infrastructure services
docker-compose up -d

# Wait for services to be ready, then run migrations
alembic upgrade head

# Start the API server
uvicorn src.ai.api.main:app --reload
```

### 4. View API Documentation
Open http://localhost:8000/docs for interactive API documentation.

## System Architecture

### Core Components

1. **Entity Extractor** (`src/ai/services/entity_extractor.py`)
   - Flexible entity extraction with dynamic type detection
   - Confidence scoring and quality filtering
   - Async processing with configurable concurrency

2. **Relationship Mapper** (`src/ai/services/relationship_mapper.py`)
   - Dynamic relationship type identification
   - Evidence-based relationship scoring
   - Multi-hop relationship traversal

3. **Knowledge Graph Builder** (`src/ai/services/graph_builder.py`)
   - Scalable graph construction from extracted entities
   - Vector embedding integration
   - Database persistence with PostgreSQL

4. **Vector Search** (`src/ai/services/vector_search.py`)
   - Configurable dimensional embeddings
   - Similarity search with Qdrant
   - Real-time query processing

5. **Graph Query Engine** (`src/ai/services/graph_query.py`)
   - Multi-hop relationship queries
   - Filtering and aggregation
   - Performance optimization

### API Endpoints

- `POST /extract` - Extract entities and relationships from documents
- `GET /graph/query` - Query knowledge graph relationships
- `GET /search/similar` - Vector similarity search
- `GET /quality/metrics` - Quality monitoring and reporting
- `GET /health` - System health check

## Configuration Options

### Embedding Dimensions
Choose the optimal embedding dimensions for your use case:

- **256**: Fast search, lower memory usage (recommended for development)
- **384**: Balanced performance (default, recommended for production)
- **512**: Higher accuracy, moderate resource usage
- **768**: Maximum accuracy, higher resource usage (original system default)

### Confidence Thresholds
Control extraction quality with configurable thresholds:

- **Medium Confidence**: 0.70 (default) - Good balance of precision/recall
- **High Confidence**: 0.85 (default) - High precision, lower recall

### Processing Workers
Scale processing capacity:

- **Development**: 2-4 workers
- **Production**: 8-16 workers (depending on hardware)

## Performance Benchmarks

- **Entity Extraction**: <5 seconds (p95) for standard documents
- **Graph Queries**: <2 seconds (p95) for relationship queries
- **Throughput**: 100-200 documents/hour sustained
- **Concurrent Users**: 500+ simultaneous queries
- **Uptime**: 99.9% target availability

## Quality Metrics

The system provides comprehensive quality monitoring:

- **Extraction Accuracy**: Configurable confidence-based filtering
- **Processing Performance**: Real-time latency and throughput tracking
- **Error Rates**: Automated monitoring and alerting
- **Cost Optimization**: Daily cost tracking and budget management

## Demo

Run the demo to see the updated system in action:

```bash
python demo.py
```

The demo showcases:
- Flexible entity extraction with dynamic types
- Dynamic relationship mapping
- Configurable embedding options
- System architecture overview
- Performance characteristics

## Development

### Testing
```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run contract tests
pytest tests/contract/
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

### Monitoring
- **Logs**: Structured logging with configurable levels
- **Health Checks**: Automated health monitoring endpoints
- **Metrics**: Performance and quality metrics collection
- **Alerts**: Configurable alerting for system issues

## Support

For issues or questions:
- Check the API documentation at `/docs`
- Review the system specifications in `specs/001-docs-team-deliverables/`
- Monitor system health at `/health`
- Check logs for detailed error information

## License

MIT License - see LICENSE file for details.
