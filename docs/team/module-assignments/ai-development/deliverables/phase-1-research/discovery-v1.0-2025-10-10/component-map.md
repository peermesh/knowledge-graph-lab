# Component Map - AI Module

**Generated:** 2025-10-10
**Purpose:** Technology primitives needed for AI Module implementation

---

## Core Components

### 1. Web Framework
**Purpose:** API endpoints for entity extraction, embedding generation, summarization
**Requirements:**
- Async/await support for non-blocking I/O
- Auto-generated API documentation (OpenAPI/Swagger)
- Request validation and serialization
- High performance (10,000+ requests/sec)
- Built-in dependency injection

**Current Decision:** FastAPI (Python)

---

### 2. Programming Language Runtime
**Purpose:** Execute AI/ML code, integrate with libraries
**Requirements:**
- Rich AI/ML ecosystem (transformers, NLP libraries)
- Async/await support
- Strong typing (optional type hints)
- Package management
- Production-ready

**Current Decision:** Python 3.11

---

### 3. Entity Extraction Library (Local)
**Purpose:** Basic named entity recognition without external API costs
**Requirements:**
- Pre-trained NER models
- Support for: organizations, people, dates, locations, amounts
- Fast inference (< 100ms per document)
- Offline capability
- Custom entity training support

**Current Decision:** spaCy

---

### 4. Large Language Model API (Primary)
**Purpose:** Complex entity extraction, relationship mapping, content synthesis
**Requirements:**
- High accuracy (GPT-4 class performance)
- Structured output support (JSON mode)
- Function calling capability
- 8k+ token context window
- Rate limiting: 60+ requests/minute
- API reliability: 99.9% uptime

**Current Decision:** OpenAI API (GPT-4)

---

### 5. Large Language Model API (Secondary/Fallback)
**Purpose:** Alternative for long documents, fallback when primary unavailable
**Requirements:**
- Large context window (100k+ tokens)
- Comparable accuracy to primary
- Different provider (avoid single point of failure)
- Rate limiting: 50+ requests/minute
- JSON output support

**Current Decision:** Anthropic API (Claude)

---

### 6. Local LLM (Optional - Future)
**Purpose:** Cost-sensitive operations, offline capability
**Requirements:**
- Self-hosted capability
- GPU acceleration support
- Reasonable accuracy (80%+ of GPT-4)
- Low latency (< 2 seconds inference)
- Fine-tuning support

**Candidate:** Llama 3, Mistral (research needed)

---

### 7. Embedding Model
**Purpose:** Generate semantic vectors for documents
**Requirements:**
- 768 or 1536 dimensional vectors
- Cosine similarity support
- Batch processing capability
- Consistent embeddings (same input → same output)
- Multi-language support

**Current Decision:** OpenAI text-embedding-ada-002 (primary), sentence-transformers (local fallback)

---

### 8. Message Queue / Event Bus
**Purpose:** Asynchronous job processing, inter-service communication
**Requirements:**
- Durable message storage
- Pub/sub and queue patterns
- Dead letter queues for failed messages
- Message prioritization
- Exactly-once delivery semantics (or at-least-once with idempotency)
- Management UI
- High throughput (10,000+ messages/sec)

**Current Decision:** RabbitMQ

---

### 9. Caching Layer
**Purpose:** Cache frequently extracted entities, API responses, embeddings
**Requirements:**
- Key-value store
- TTL (time-to-live) support
- Sub-millisecond latency
- Pub/sub for cache invalidation
- Cluster support for HA
- Memory-based (not disk)

**Current Decision:** Redis

---

### 10. Containerization
**Purpose:** Consistent deployment across environments
**Requirements:**
- Image building and management
- Multi-stage builds for optimization
- Health check support
- Resource limits (CPU/memory)
- Non-root user support for security
- Image registry integration

**Current Decision:** Docker

---

### 11. Container Orchestration (Production)
**Purpose:** Deploy, scale, and manage containers in production
**Requirements:**
- Auto-scaling based on metrics (queue depth, CPU)
- Rolling updates with health checks
- Service discovery
- Configuration management (ConfigMaps, Secrets)
- Resource quotas
- Liveness/readiness probes

**Candidate:** Kubernetes (standard choice for microservices)

---

### 12. Metrics Collection
**Purpose:** Track processing metrics, accuracy, costs, errors
**Requirements:**
- Time-series database
- Query language (PromQL)
- Retention policies (90 days)
- Alerting rules engine
- Histogram and counter support
- Pull-based scraping

**Candidate:** Prometheus

---

### 13. Metrics Visualization
**Purpose:** Dashboard for monitoring AI module health
**Requirements:**
- Prometheus integration
- Custom dashboards
- Alerting visualization
- Real-time updates
- Multi-user support

**Candidate:** Grafana

---

### 14. Structured Logging Library
**Purpose:** JSON-formatted logs with context
**Requirements:**
- JSON output
- Contextual fields (job_id, correlation_id)
- Log levels (DEBUG, INFO, WARN, ERROR)
- Performance (low overhead)
- Integration with Python logging

**Candidate:** structlog (Python)

---

### 15. Log Aggregation (Optional)
**Purpose:** Centralized log storage and search
**Requirements:**
- Full-text search
- Log retention (30 days)
- Query DSL
- Visualization
- High ingestion rate

**Candidate:** Elasticsearch + Kibana (ELK Stack)

---

### 16. Error Tracking
**Purpose:** Capture exceptions, stack traces, error context
**Requirements:**
- Automatic exception capture
- Stack trace with locals
- Breadcrumb tracking
- Performance monitoring
- Issue grouping and deduplication
- Alerts on new errors

**Candidate:** Sentry

---

### 17. Data Validation Library
**Purpose:** Validate API requests/responses, entity formats
**Requirements:**
- Schema definition (similar to JSON Schema)
- Automatic parsing and validation
- Clear error messages
- Python integration
- JSON serialization

**Current Decision:** Pydantic (Python)

---

### 18. Testing Framework
**Purpose:** Unit tests, integration tests, API tests
**Requirements:**
- Fixture support
- Mocking capabilities
- Async test support
- Coverage reporting
- Fast execution

**Current Decision:** pytest (Python)

---

### 19. HTTP Client Library
**Purpose:** Call external APIs (LLM providers, Backend APIs)
**Requirements:**
- Async support
- Connection pooling
- Timeout handling
- Retry with exponential backoff
- JSON parsing
- HTTP/2 support

**Candidate:** httpx (Python) or aiohttp

---

### 20. Prompt Template Engine
**Purpose:** Manage and version prompt templates
**Requirements:**
- Variable substitution
- Template versioning
- Few-shot example management
- Prompt chaining
- Output parsing

**Candidate:** LangChain or custom implementation

---

## External Services (Backend-Provided)

### 21. Graph Database
**Purpose:** Store entities and relationships
**Requirements:**
- Graph query language (Cypher)
- ACID transactions
- Index support for fast lookups
- Relationship traversal
- High availability

**Note:** Backend owns this - AI just writes to it

---

### 22. Vector Database
**Purpose:** Store document embeddings for similarity search
**Requirements:**
- High-dimensional vector storage (768 or 1536 dims)
- Nearest neighbor search (ANN)
- Cosine similarity metric
- Index types (HNSW, IVF)
- Metadata filtering
- High query throughput (1000+ QPS)

**Note:** Backend owns this - AI writes embeddings

---

### 23. Report Storage
**Purpose:** Store generated news reports
**Requirements:**
- Document storage with metadata
- Query by date, tags, entities
- Full-text search
- URL generation
- High availability

**Note:** Backend provides storage API

---

## Development Tools

### 24. Package Manager
**Purpose:** Dependency management for Python libraries
**Requirements:**
- Lock file for reproducible builds
- Virtual environment support
- Fast dependency resolution

**Current Decision:** pip + requirements.txt (or Poetry for advanced)

---

### 25. Code Formatter
**Purpose:** Consistent code style
**Requirements:**
- Automatic formatting
- PEP 8 compliant
- No configuration needed

**Candidate:** black (Python)

---

### 26. Linter
**Purpose:** Static code analysis, catch bugs
**Requirements:**
- Type checking
- Unused import detection
- Code complexity analysis

**Candidate:** pylint or flake8 + mypy (type checker)

---

## Component Dependencies

**Critical Path (Must Have for MVP):**
1. Python 3.11
2. FastAPI
3. spaCy (local NER)
4. OpenAI API
5. RabbitMQ (or Backend queue)
6. Redis (caching)
7. Docker
8. Pydantic (validation)
9. pytest (testing)

**Important (Phase 4):**
10. Anthropic API (Claude)
11. Prometheus + Grafana (monitoring)
12. structlog (logging)
13. Kubernetes (orchestration)
14. httpx/aiohttp (HTTP client)

**Nice to Have (Phase 5+):**
15. Llama/Mistral (local LLM)
16. ELK Stack (log aggregation)
17. Sentry (error tracking)
18. LangChain (prompt management)

---

## Integration Points

**AI Module Provides:**
- REST API endpoints (FastAPI)
- Event publishing (RabbitMQ)
- Metrics endpoint (Prometheus format)
- Health/readiness endpoints

**AI Module Consumes:**
- Job queue (RabbitMQ messages)
- Vector DB connection (Backend provides)
- Graph DB connection (Backend provides)
- Report storage API (Backend provides)

---

## Technology Risk Assessment

**Low Risk (Proven Technologies):**
- Python, FastAPI, Docker, Redis, RabbitMQ
- OpenAI API, spaCy
- pytest, Pydantic

**Medium Risk (Less Familiar):**
- Anthropic API (newer, less battle-tested)
- Kubernetes (operational complexity)
- Vector databases (newer technology)

**High Risk (Requires Research):**
- Local LLM deployment (Llama, Mistral)
- Prompt engineering frameworks (LangChain complexity)
- Fine-tuning workflows (cost and complexity)

---

## Deployment Architecture

**Development:**
- Docker Compose with all services local
- Mock LLM APIs to save costs
- SQLite for lightweight storage

**Staging:**
- Kubernetes with 2 replicas
- Real LLM APIs with rate limits
- Shared Backend services

**Production:**
- Kubernetes with 2-20 replicas (auto-scaling)
- Production LLM API keys with full quotas
- Dedicated Backend services
- Full monitoring and alerting

---

## Sources

- `docs/modules/ai-development/PRD.md` - Tech stack decisions
- `docs/design/system/architecture.md` - System architecture
- `requirements-notes.md` - Detailed requirements
- `technical-context.md` - Technical architecture
- `decisions-made.md` - Technology decisions
