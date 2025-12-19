# Technical Context - AI Module

**Distilled from:** architecture.md, ai-publishing-integration.md, PRD.md

**Date:** 2025-10-10

---

## System Architecture Overview

### Microservices Architecture

Knowledge Graph Lab uses a **microservices architecture** with 5 independent services designed for scalability, maintainability, and parallel development.

**The 5 Services:**

1. **Data Ingestion Service** - Collects and normalizes content from external sources
2. **AI Processing Service** - **Our module**: Extracts entities, maps relationships, generates insights
3. **Graph Database Layer** - Stores interconnected entities and relationships
4. **API Gateway** - Routes requests, handles auth, manages caching
5. **Publishing Service** - Personalizes and distributes content to users

**Architecture Benefits:**

- **Parallel Development:** Teams work independently on separate services
- **Service Isolation:** Failures contained, don't cascade
- **Independent Scaling:** Scale AI processing without scaling ingestion
- **Resilience:** Loose coupling through event-driven patterns

**Source:** `architecture.md` lines 5-40

---

## AI Processing Service Architecture

### Service Responsibilities

**Core Functions:**

- Extract meaningful entities from normalized content
- Identify and map relationships between entities
- Apply confidence scoring to extracted information
- Leverage modern language models for understanding
- Maintain processing pipeline for continuous improvement

**Position in Data Flow:**
```
Data Ingestion → AI Processing → Graph Database → API Gateway → Publishing
```

**Source:** `architecture.md` lines 14-20

---

### Internal Architecture (AI Service)

**Layer Structure:**
```
API Layer (FastAPI)
    ↓
Service Layer (Business Logic)
    ↓
Processing Layer (AI/ML Pipeline)
    ↓
Integration Layer (External APIs, Databases)
```

**Components:**

**1. API Layer:**

- FastAPI application with async support
- 3 core endpoints: /extract, /embed, /summarize
- Request validation with Pydantic models
- OpenAPI documentation generation

**2. Service Layer:**

- Model selection logic (GPT-4 vs. Claude vs. Llama)
- Prompt template management
- Confidence calculation algorithms
- Error handling and retry logic

**3. Processing Layer:**

- Document chunking (1000-2000 tokens)
- Entity extraction pipeline
- Relationship inference engine
- Embedding generation
- News report synthesis

**4. Integration Layer:**

- LLM provider clients (OpenAI, Anthropic)
- Vector database connections (Pinecone/Qdrant)
- Event bus integration (RabbitMQ)
- Metrics collection (Prometheus)

**Source:** `PRD.md` lines 177-194

---

## Communication Patterns

### Event-Driven Architecture

**Primary Pattern:** Services communicate through an event bus (RabbitMQ) for asynchronous, loosely-coupled integration.

**Event Bus Capabilities:**

- **Asynchronous Processing:** Non-blocking operations for better performance
- **Retry Mechanisms:** Handle transient failures automatically
- **Dead Letter Queues:** Capture failed messages for analysis
- **Event Replay:** System recovery through event sourcing
- **Audit Trails:** Complete history for compliance

**AI Module Event Types:**

- **Publishes:** `entity.extracted`, `relationship.discovered`, `report.generated`, `processing.failed`
- **Subscribes:** `document.normalized`, `extraction.requested`, `feedback.received`

**Source:** `architecture.md` lines 88-99

---

### Resilience Patterns

**Implemented Patterns:**

- **Circuit Breakers:** Prevent cascade failures to external LLM APIs
- **Exponential Backoff:** Intelligent retry with increasing delays
- **Health Checks:** `/health` and `/ready` endpoints for orchestration
- **Graceful Degradation:** Fallback to simpler models when primary unavailable
- **Bulkhead Isolation:** Separate thread pools for different operations

**Example: LLM API Circuit Breaker:**
```python
if consecutive_failures > 5:
    circuit_breaker.open()
    use_fallback_model()
    alert_ops_team()
```

**Source:** `architecture.md` lines 100-107

---

## Data Storage Strategy

### Multi-Database Approach

The system employs multiple storage technologies optimized for different data patterns:

**1. Object Storage (S3/MinIO):**

- Purpose: Raw document preservation
- AI Module Usage: Retrieve original documents for re-processing

**2. Graph Database (Neo4j):**

- Purpose: Relationship-centric queries
- AI Module Usage: Store extracted entities and relationships
- Query Pattern: `MATCH (e:Entity)-[r:FUNDS]->(g:Grant) WHERE ...`

**3. Vector Storage (Pinecone/Qdrant):**

- Purpose: Semantic similarity search
- AI Module Usage: Store document embeddings (768 or 1536 dimensions)
- Query Pattern: Nearest neighbor search for similar documents

**4. Caching Layer (Redis):**

- Purpose: Performance optimization
- AI Module Usage: Cache frequently extracted entities, prompt responses

**5. Traditional Database (PostgreSQL):**

- Purpose: Structured metadata
- AI Module Usage: Store processing job status, metrics, logs

**Source:** `architecture.md` lines 59-65

---

## Data Flow Pipeline

### Complete Pipeline

**End-to-End Flow:**
```
1. Discovery: Ingestion service collects raw documents
2. Normalization: Convert to standard format
3. Queue: Place in processing queue with priority
4. AI Processing: Extract entities, relationships, generate reports
5. Storage: Persist to graph DB, vector DB, report storage
6. Query: API gateway enables frontend/publishing to retrieve
7. Distribution: Publishing delivers to users via email/web
```

**AI Module's Position:**

- **Receives:** Normalized documents from Backend
- **Processes:** Extracts intelligence
- **Delivers:** Structured data to Backend for storage
- **Enables:** Frontend queries, Publishing distribution

**Source:** `architecture.md` lines 42-52

---

### AI Processing Pipeline Detail

**Stage-by-Stage Processing:**

**Stage 1: Input Reception**

- Receive job from queue (RabbitMQ message)
- Parse document metadata and content
- Validate format and completeness
- Estimate processing complexity

**Stage 2: Document Chunking**

- Split into 1000-2000 token segments
- Maintain context across boundaries
- Preserve document structure metadata
- Handle multi-page PDFs, long articles

**Stage 3: Entity Extraction**

- Select appropriate model (GPT-4, Claude, spaCy)
- Apply extraction prompt templates
- Parse structured output (JSON)
- Validate entity formats and types

**Stage 4: Relationship Inference**

- Analyze entity co-occurrence patterns
- Apply relationship extraction prompts
- Identify explicit and implicit connections
- Build relationship graph

**Stage 5: Confidence Scoring**

- Calculate source reliability score
- Analyze context (multiple mentions)
- Get model confidence values
- Apply formula: `(source*0.3) + (context*0.4) + (model*0.3)`

**Stage 6: Embedding Generation**

- Generate document embeddings (768 or 1536 dims)
- Store in vector database
- Index for similarity search

**Stage 7: Validation & Output**

- Check entity formats (dates, amounts)
- Validate relationship consistency
- Format output JSON
- Send to Backend via API or event

**Stage 8: Report Generation** (if applicable)

- Synthesize findings from multiple extractions
- Apply news-writing prompts
- Generate headline, lead, body
- Tag with topics, entities, priority
- Submit to Backend storage

**Source:** `AI-Development-Spec.md` lines 41-49, `PRD.md` lines 109-132

---

## Integration Contracts

### AI Module ↔ Backend Integration

**What AI Receives from Backend:**
```json
{
  "job_id": "uuid",
  "document_id": "doc-123",
  "source_url": "https://example.com/article",
  "content_type": "text/html",
  "content": "raw text content...",
  "priority": "high|medium|low",
  "metadata": {
    "source": "RSS feed name",
    "published_date": "ISO-8601",
    "language": "en"
  }
}
```

**What AI Returns to Backend:**
```json
{
  "job_id": "uuid",
  "status": "success|partial|failed",
  "processing_time_ms": 1523,
  "entities": [
    {
      "id": "entity-uuid",
      "name": "YouTube",
      "type": "platform",
      "confidence": 95,
      "positions": [{"start": 0, "end": 7}]
    }
  ],
  "relationships": [
    {
      "id": "rel-uuid",
      "from_entity": "entity-uuid-1",
      "to_entity": "entity-uuid-2",
      "type": "funds",
      "confidence": 82
    }
  ],
  "embeddings": {
    "model": "text-embedding-ada-002",
    "dimensions": 1536,
    "vector": [0.012, -0.023, ...]
  }
}
```

**Error Handling:**

- Timeout errors: Retry with exponential backoff (max 3 attempts)
- Invalid format: Log error and skip processing
- Rate limit exceeded: Queue for delayed processing
- Model unavailable: Use fallback model or fail gracefully

**Source:** `AI-Development-Spec.md` lines 126-167

---

### AI Module → Publishing Integration

**News Report Storage:**

AI generates standalone reports and submits to Backend:
```
POST /api/reports
{
  "report_id": "uuid",
  "url": "/reports/2025-09-22/openai-funding",
  "generated_at": "2025-09-22T10:00:00Z",
  "report_type": "breaking_news|analysis|update|summary",
  "headline": "OpenAI Raises $10B...",
  "lead": "In a landmark deal...",
  "body": [
    {"type": "paragraph", "content": "..."},
    {"type": "quote", "content": "...", "attribution": "..."}
  ],
  "metadata": {
    "entities": ["OpenAI", "Microsoft"],
    "topics": ["AI", "venture_capital"],
    "priority": "breaking|important|standard",
    "relevance_scores": {
      "ai_industry": 0.98,
      "venture_capital": 0.95
    }
  },
  "source_documents": ["doc-id-1", "doc-id-2"]
}
```

**Publishing Query Interface:**

Publishing module queries Backend (NOT AI directly):
```
GET /api/reports?date_range=2025-09-22&topics=AI&min_relevance=0.7
```

**Separation of Concerns:**

- **AI:** Generates reports, has no knowledge of subscribers
- **Backend:** Stores reports, provides query API
- **Publishing:** Queries reports, personalizes, distributes

**Source:** `ai-publishing-integration.md` lines 43-163

---

## Technology Stack

### Core Technologies

**Application Framework:**

- **Python 3.11:** Latest stable Python for async and performance
- **FastAPI:** Modern async web framework with OpenAPI support
- **Pydantic:** Data validation and serialization
- **Docker:** Containerization for consistent deployment

**AI/ML Libraries:**

- **spaCy:** Local NER for basic entity extraction
- **OpenAI API:** GPT-4 for complex extraction and synthesis
- **Anthropic API:** Claude as alternative/fallback
- **LangChain/LlamaIndex:** RAG orchestration (TBD)
- **sentence-transformers:** Local embeddings (optional)

**Infrastructure:**

- **RabbitMQ:** Event bus for async communication
- **Redis:** Caching and rate limiting
- **Prometheus:** Metrics collection
- **Grafana:** Monitoring dashboards
- **Sentry:** Error tracking

**Source:** `PRD.md` lines 32-39

---

### External Dependencies

**LLM Providers:**

- **OpenAI:** GPT-4 for high-accuracy extraction
- **Anthropic:** Claude for alternative approach
- **Local Models:** Llama, Mistral for cost-sensitive operations

**Storage Services:**

- **Neo4j:** Graph database (Backend manages)
- **Pinecone/Qdrant:** Vector database (Backend manages)
- **PostgreSQL:** Relational database (Backend manages)

**Monitoring:**

- **Datadog/New Relic:** APM (optional)
- **ELK Stack:** Log aggregation (optional)

**Source:** `architecture.md` lines 119-123

---

## Development Approach

### Mock-First Strategy

**Phase 1 (Weeks 1-6): Mock Implementation**

- Build API with hardcoded mock responses
- No AI API costs during infrastructure development
- Enables Backend team to integrate in parallel
- Tests deployment and scaling patterns

**Example Mock Implementation:**
```python
def mock_extract_entities(text):
    entities = []
    if "youtube" in text.lower():
        entities.append({"name": "YouTube", "type": "platform", "confidence": 95})
    if "fund" in text.lower():
        entities.append({"name": "Creator Fund", "type": "grant", "confidence": 87})
    return {"entities": entities}
```

**Phase 2 (Weeks 7-10): Real AI Integration**

- Replace mocks with actual LLM calls
- Implement real entity extraction with GPT-4/Claude
- Add prompt engineering and optimization
- Handle API errors and rate limits

**Example Real Implementation:**
```python
def extract_entities_gpt(text):
    prompt = f"""
    Extract entities from this text about the creator economy.
    Categories: person, organization, platform, grant, program

    Text: {text}

    Return as JSON list with name, type, and confidence.
    """
    response = openai.complete(prompt)
    return json.loads(response)
```

**Benefits:**

- Saves API costs during development
- Validates architecture before expensive operations
- Enables parallel team work
- Reduces risk of cost overruns

**Source:** `PRD.md` lines 109-150

---

## Deployment Strategy

### Containerization

**Docker Setup:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Container Features:**

- Multi-stage builds for smaller images
- Non-root user for security
- Health check endpoints
- Graceful shutdown handling

**Source:** `PRD.md` lines 212-215

---

### Kubernetes Deployment (Future)

**Deployment Pattern:**

- Horizontal pod autoscaling based on queue depth
- Multiple replicas for high availability
- Resource limits: CPU, memory quotas
- Liveness and readiness probes
- ConfigMaps for environment variables
- Secrets for API keys

**Scaling Strategy:**

- Scale based on processing queue size
- Scale based on API response times
- Independent from other services

**Source:** Implied by microservices architecture

---

## Performance Optimization

### Caching Strategy

**What to Cache:**

- **Frequently Extracted Entities:** Common org names, platforms
- **Prompt Responses:** Recently processed similar documents
- **Embeddings:** Document vectors for re-use
- **Model Responses:** High-confidence extractions

**Cache Invalidation:**

- TTL-based expiration (24 hours for entity cache)
- Confidence-based (only cache high-confidence results)
- Manual invalidation for corrections

**Source:** `PRD.md` lines 98-102

---

### Batch Processing

**Batch Optimization:**

- Process multiple documents in single LLM API call (where possible)
- Batch embeddings generation (OpenAI supports batching)
- Parallel processing with worker pools
- Queue prioritization for urgent documents

**Trade-offs:**

- Latency vs. throughput
- Cost vs. speed
- Accuracy vs. processing time

---

## Monitoring & Observability

### Key Metrics

**Processing Metrics:**

- Documents processed per hour
- Average processing time per document
- Processing time by document type (HTML, PDF, text)
- Queue depth and wait times

**Accuracy Metrics:**

- Entity extraction accuracy (by type)
- Relationship extraction accuracy
- Confidence score calibration
- Hallucination rate

**Cost Metrics:**

- API cost per document
- Cost by provider (OpenAI, Anthropic)
- Token usage per request
- Cost trends over time

**Error Metrics:**

- Error rate by error type
- Retry success rate
- Timeout frequency
- API failure rate

**Source:** `AI-Development-Spec.md` lines 241-254

---

### Logging Structure

**Structured JSON Logs:**
```json
{
  "timestamp": "2025-10-10T14:30:00Z",
  "level": "INFO",
  "job_id": "job-uuid",
  "stage": "entity_extraction",
  "duration_ms": 1523,
  "model": "gpt-4",
  "tokens_used": 1200,
  "entities_found": 12,
  "confidence_avg": 0.87
}
```

**Log Levels:**

- **DEBUG:** Model responses, intermediate results
- **INFO:** Processing stages, successful operations
- **WARN:** Retries, fallback model usage, low confidence
- **ERROR:** Failures, exceptions, data quality issues

**Source:** `AI-Development-Spec.md` lines 248-254

---

## Security Considerations

### API Key Management

**Best Practices:**

- Store API keys in environment variables (never hardcode)
- Use separate keys for dev/staging/production
- Rotate keys periodically
- Implement key rotation without downtime
- Monitor API key usage for anomalies

### Rate Limiting

**Implementation:**

- Rate limit by client/user
- Rate limit by API key
- Exponential backoff for external APIs
- Queue overflow protection

### Data Privacy

**Sensitive Data Handling:**

- Sanitize PII before logging
- Encrypt sensitive data in transit (TLS)
- Don't store raw API keys in logs
- Redact sensitive entities in debug output

---

## Sources

- `docs/design/system/architecture.md` - System architecture and communication patterns
- `docs/design/system/ai-publishing-integration.md` - Integration specifications
- `docs/modules/ai-development/PRD.md` - Tech stack and implementation approach
- `docs/modules/ai-development/AI-Development-Spec.md` - Pipeline and processing details
