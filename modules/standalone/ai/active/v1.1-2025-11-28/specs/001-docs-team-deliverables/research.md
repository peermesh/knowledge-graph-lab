# Phase 0: Research & Technical Decisions

**Feature**: AI Development Module  
**Date**: 2025-10-20  
**Status**: Complete

## Technology Stack Decisions

### 1. Entity Extraction Framework

**Decision**: LangChain with multiple LLM provider support (OpenAI GPT-4, Anthropic Claude)

**Rationale**:
- Unified interface for multiple LLM providers enables fallback mechanisms
- Built-in prompt management and chain composition reduces boilerplate
- Active community and extensive documentation
- Native support for entity extraction patterns
- Streaming capabilities for real-time processing

**Alternatives Considered**:
- **spaCy NER**: Evaluated but limited accuracy for domain-specific entities (funding amounts, relationship types)
- **Hugging Face Transformers**: Considered but requires more infrastructure for model serving
- **Custom Fine-tuned Models**: Rejected due to time/cost constraints for initial MVP

**Best Practices**:
- Use structured output with Pydantic models for type safety
- Implement retry logic with exponential backoff for API calls
- Cache frequently used prompts for performance
- Monitor token usage and costs per document

---

### 2. Vector Database

**Decision**: Qdrant for vector embeddings and similarity search

**Rationale**:
- Native support for 768-dimensional embeddings (OpenAI/sentence-transformers standard)
- High-performance similarity search (< 500ms p95 for 50K vectors)
- Built-in filtering capabilities for entity type and confidence thresholds
- Docker-first deployment model matches our infrastructure
- Cost-effective compared to managed services for our scale

**Alternatives Considered**:
- **Pinecone**: Evaluated but pricing model expensive at 1M+ vectors
- **Weaviate**: Considered but overkill for our use case (we don't need full semantic search engine)
- **pgvector (PostgreSQL extension)**: Rejected due to performance limitations beyond 100K vectors

**Best Practices**:
- Use separate collections for different entity types for query performance
- Implement batch embedding operations (100+ entities at once)
- Configure HNSW index parameters for accuracy/speed tradeoff
- Enable quantization for memory efficiency

---

### 3. Structured Data Storage

**Decision**: PostgreSQL 15+ with JSONB support

**Rationale**:
- ACID compliance ensures data consistency for entity relationships
- Native JSONB support for flexible metadata storage
- Mature ecosystem with battle-tested reliability
- Excellent support for complex relationship queries with CTEs
- Connection pooling and replication capabilities
- Team familiarity reduces implementation risk

**Alternatives Considered**:
- **MongoDB**: Evaluated but eventual consistency model problematic for relationship integrity
- **Neo4j**: Considered for native graph capabilities but adds operational complexity

**Best Practices**:
- Use UUIDs for all primary keys (distributed system compatibility)
- Index frequently queried fields (entity_type, confidence, source_document_id)
- Implement database connection pooling (min 10, max 100 connections)
- Use transactions for multi-table updates (entity + relationship creation)
- Regular VACUUM and ANALYZE for query performance

---

### 4. Asynchronous Processing

**Decision**: RabbitMQ for job queue management

**Rationale**:
- Priority queue support enables high/normal/low priority document processing
- Message persistence ensures no job loss during system failures
- Dead letter exchange for failed job handling
- Proven scalability (100+ concurrent workers)
- Strong Python client libraries

**Alternatives Considered**:
- **Celery with Redis**: Evaluated but lacks native priority queue support
- **AWS SQS**: Considered but adds cloud vendor lock-in
- **Kafka**: Overkill for our throughput requirements (100-200 docs/hour)

**Best Practices**:
- Configure separate queues for different priority levels
- Implement retry with exponential backoff (1s, 2s, 4s, 8s, 16s max)
- Use message TTL to prevent queue bloat
- Monitor queue depth and alert on backlogs
- Enable message acknowledgment for reliability

---

### 5. API Framework

**Decision**: FastAPI with async/await support

**Rationale**:
- Native async support critical for I/O-bound operations (LLM calls, DB queries)
- Automatic OpenAPI documentation generation
- Pydantic integration for request/response validation
- High performance (comparable to Node.js and Go)
- Excellent developer experience with type hints

**Alternatives Considered**:
- **Flask**: Lacks native async support (would require ASGI adapter)
- **Django**: Too heavyweight for microservice architecture

**Best Practices**:
- Use dependency injection for database connections and clients
- Implement middleware for authentication, logging, and error handling
- Enable request ID tracking for distributed tracing
- Configure rate limiting at API gateway level
- Use background tasks for async operations

---

### 6. Confidence Scoring Approach

**Decision**: Weighted multi-factor confidence formula

**Formula**: `confidence = (source_score × 0.3) + (context_score × 0.4) + (model_confidence × 0.3)`

**Rationale**:
- **Source Score (30%)**: Reflects reliability of document source (official sites > social media)
- **Context Score (40%)**: Highest weight as context/co-occurrence patterns most predictive
- **Model Confidence (30%)**: LLM-provided confidence useful but can be overconfident

**Best Practices**:
- Calibrate weights based on validation dataset
- Log confidence components separately for debugging
- Set threshold at 70% for "medium confidence" and 85% for "high confidence"
- Implement confidence trending to detect model drift

---

### 7. Multi-language Processing

**Decision**: Language-specific LLM prompts with fallback to translation

**Rationale**:
- Native language processing more accurate than translate-then-extract
- LangChain supports language-specific prompt templates
- Cost-effective for our 4-language requirement (EN, ES, FR, ZH)

**Alternatives Considered**:
- **Translate-first approach**: Rejected due to information loss in translation
- **Separate models per language**: Overkill for MVP

**Best Practices**:
- Detect language before extraction using `langdetect` library
- Use language-specific entity type variations (e.g., Chinese company name patterns)
- Provide transliteration for non-Latin scripts
- Track accuracy metrics per language separately

---

### 8. Testing Strategy

**Decision**: Three-tier testing (unit, integration, contract)

**Test Levels**:
1. **Unit Tests**: Service logic, confidence scoring, deduplication
2. **Integration Tests**: Database operations, vector search, message queue
3. **Contract Tests**: API endpoints against OpenAPI spec, cross-module contracts

**Framework**: pytest with async support, pytest-asyncio, testcontainers

**Best Practices**:
- Mock external LLM calls in unit tests
- Use testcontainers for integration tests (PostgreSQL, Qdrant, RabbitMQ)
- Generate test data with known entities for accuracy validation
- Target >80% line coverage for business logic
- Run contract tests on every PR

---

### 9. Deployment Architecture

**Decision**: Docker containers on AWS ECS

**Rationale**:
- Docker enables consistent dev/prod environments
- ECS provides managed container orchestration
- Auto-scaling based on queue depth and CPU utilization
- Integration with existing AWS infrastructure (RDS, ECS)

**Best Practices**:
- Multi-stage Docker builds for smaller images
- Health check endpoints for container orchestration
- Resource limits (8GB memory, 2 vCPU per worker)
- Blue-green deployment for zero-downtime updates

---

### 10. Cost Optimization

**Decision**: Tiered LLM provider strategy

**Approach**:
- **High-priority docs**: OpenAI GPT-4 (highest accuracy, $0.15/doc)
- **Normal priority**: OpenAI GPT-3.5-turbo ($0.08/doc)
- **Low priority**: Claude Instant ($0.05/doc)
- **Fallback**: Open-source models on local infrastructure ($0.01/doc)

**Daily Budget Management**:
- Track costs per document in real-time
- Switch to cheaper models when approaching daily budget ($50/day = 500 docs at $0.10)
- Queue high-cost documents for next day when budget exhausted
- Alert ops team when consistently exceeding budget

**Best Practices**:
- Cache entity extractions to avoid re-processing
- Batch similar documents to same model for efficiency
- Monitor cost per entity extracted (target: <$0.02 per entity)

---

## Integration Patterns

### Backend Module Integration

**Pattern**: REST API + RabbitMQ message queue

**Flow**:
1. Backend POSTs document to `/api/ai/extract-entities`
2. AI module creates processing job and returns job_id
3. AI module processes asynchronously, publishes results to `ai.results.{job_id}` queue
4. Backend consumes results from queue

**Contract**: See `contracts/backend-integration.yaml`

---

### Frontend Module Integration

**Pattern**: REST API for queries, WebSocket for real-time updates

**Flow**:
1. Frontend queries entities via GET `/api/ai/graph/query`
2. Frontend subscribes to WebSocket for real-time graph updates
3. AI module pushes graph changes to connected clients

**Contract**: See `contracts/frontend-integration.yaml`

---

### Publishing Module Integration

**Pattern**: REST API for content analysis and entity enrichment

**Flow**:
1. Publishing calls POST `/api/ai/analyze-content` with article text
2. AI returns entities, topics, sentiment for personalization
3. Publishing uses entity data for recommendation algorithms

**Contract**: See `contracts/publishing-integration.yaml`

---

## Performance Optimization

### Database Optimization
- Index strategy: entity_type, confidence, source_document_id, created_at
- Connection pooling: min 10, max 100 connections
- Query optimization: Use CTEs for complex relationship queries
- Partitioning: Consider partitioning by created_at for >10M entities

### Vector Search Optimization
- HNSW index parameters: M=16, ef_construct=200 (accuracy/speed balance)
- Batch operations: Process 100+ embeddings at once
- Quantization: Enable scalar quantization for 4x memory reduction
- Collection per entity type: Separate collections for faster searches

### API Performance
- Response caching: Cache frequent entity queries (15-minute TTL)
- Connection pooling: Reuse HTTP connections to external services
- Background tasks: Use FastAPI background tasks for non-blocking operations
- Request batching: Support batch entity extraction in single API call

---

## Security Considerations

### Authentication
- JWT tokens for user authentication (RS256 algorithm)
- Service-to-service authentication using API keys
- Token expiration: 1 hour (access tokens), 7 days (refresh tokens)

### Authorization
- Role-based access control (RBAC): user, admin, moderator roles
- Entity-level permissions for sensitive data
- API rate limiting: 100 requests/minute per user

### Data Protection
- Encryption at rest: PostgreSQL encryption, encrypted Qdrant volume
- Encryption in transit: TLS 1.3 for all API communication
- Input validation: Comprehensive validation using Pydantic
- Audit logging: Log all entity access and modifications

---

## Monitoring & Observability

### Metrics to Track
- **Processing**: docs/hour, entities/hour, latency percentiles (p50/p95/p99)
- **Quality**: extraction accuracy, confidence score distributions, error rates
- **Performance**: API response times, database query times, vector search latency
- **Cost**: LLM API costs per document, total daily spend
- **Resources**: Memory usage, CPU utilization, queue depth

### Logging Strategy
- Structured logging with JSON format
- Log levels: DEBUG (development), INFO (production), ERROR (always)
- Correlation IDs for request tracing across services
- Centralized logging to CloudWatch or ELK stack

### Alerting
- Extraction accuracy drops below 80%
- API error rate exceeds 5%
- Queue depth exceeds 1000 pending jobs
- Daily cost exceeds budget threshold
- Memory usage exceeds 7GB per worker

---

## Open Questions Resolved

All technical clarifications have been researched and documented above. No remaining open questions blocking implementation.

---

**Research Complete**: All technology decisions made and documented. Ready for Phase 1 design.
