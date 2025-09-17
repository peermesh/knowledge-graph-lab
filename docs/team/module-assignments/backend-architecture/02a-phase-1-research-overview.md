# Backend Architecture - Phase 1 Research

Optional Deep Dive: see [02c-phase-1-research-advanced.md](02c-phase-1-research-advanced.md)

## Your Focus Area

You'll design and build the core backend infrastructure that powers the entire Knowledge Graph Lab system. This includes data pipelines, database architecture, deployment strategies, and authentication systems.

## Critical Requirement: Local-First Development

**The entire system MUST run locally in Docker containers on a developer's machine**
- No cloud services required for core functionality
- Optional cloud deployment for production
- All dependencies included in Docker setup
- Single `docker-compose up` to start everything

## Research Objectives

You need to research and make recommendations for:

1. **Database Strategy** - Compare PostgreSQL (structured data), MongoDB (documents), Neo4j (relationships), Redis (cache/sessions)
   - Example: Can PostgreSQL + pgvector handle 10K embeddings vs dedicated vector DB?
   - Benchmark: Insert 1K entities with relationships in <100ms

2. **API Framework** - Test FastAPI (async), Django REST (batteries-included), Flask (lightweight)
   - Example: Build identical CRUD endpoint, measure response time and documentation quality
   - Benchmark: Generate OpenAPI spec with <5 manual steps

3. **Container Orchestration** - Docker Compose (local), Kubernetes (production scale), Docker Swarm (simple clustering)
   - Example: Start all services (DB, API, Redis, queue worker) with single command
   - Benchmark: Services start and communicate in <30 seconds

4. **Authentication Method** - JWT (stateless), Session cookies (server state), OAuth (third-party)
   - Example: Implement login flow with 90% of routes protected by default
   - Benchmark: Auth middleware adds <10ms per request

5. **Message Queue System** - Redis (simple), RabbitMQ (reliable), database table (MVP)
   - Example: Queue 100 file processing jobs, handle failures gracefully
   - Benchmark: Process 50 jobs/minute with retry logic

## Research Tasks Checklist

### Foundation Setup
- [ ] Docker environment: All services start with `docker-compose up`, accessible on localhost
- [ ] Database comparison: Load test with 10K records, measure query speed (<50ms for common queries)
- [ ] Redis setup: Configure as cache (90%+ hit rate) and simple job queue (handles 100+ jobs/minute)
- [ ] Vector storage: Compare pgvector vs Pinecone vs Weaviate for 1K+ embeddings, similarity search <200ms

### API Development
- [ ] FastAPI prototype: `/health`, `/upload`, `/search` endpoints with automatic OpenAPI docs
- [ ] Framework comparison: Build same 5 endpoints, compare code lines, auto-docs quality, async support
- [ ] API documentation: Interactive Swagger UI accessible at `/docs`, includes auth examples
- [ ] Auth implementation: Choose library that provides JWT + password reset + user management in <200 lines

### Infrastructure Planning
- [ ] Research Docker Compose for local development
- [ ] Evaluate container orchestration options
- [ ] Compare cloud providers (AWS vs GCP vs Azure)
- [ ] Research monitoring solutions (Datadog vs New Relic vs self-hosted)
- [ ] Evaluate CI/CD options (GitHub Actions vs GitLab CI)

### Data Management
- [ ] File pipeline: Handle uploads up to 50MB, process in background, show progress, graceful failures
- [ ] Content extraction testing:
  - PDF: Test with 10-page technical document, extract text + metadata in <5 seconds
  - Office docs: Test .docx with tables/images, maintain formatting structure
  - Web scraping: Extract article content from 5 common news sites, avoid rate limits
- [ ] Migration strategy: Version-controlled SQL migrations, rollback capability, zero-downtime deploys
- [ ] Backup plan: Daily automated backups, 30-day retention, tested restore procedure (<2 hours)

## Key Questions to Answer

### System Design
- **Load handling**: Test API gateway + connection pooling + Redis cache for 10K requests/minute (target: <200ms p95)
- **Migrations**: Alembic for SQL schema changes, backward-compatible API changes, feature flags for breaking changes
- **API versioning**: URL versioning (/v1/api/) vs header versioning, deprecation timeline (6 months minimum)
- **Graph backups**: Neo4j dump vs PostgreSQL pg_dump for relationship data, test restore time
- **Disaster recovery**: RTO <4 hours, RPO <1 hour, documented runbook with actual restore times

### File Processing
- **Upload reliability**: Multipart upload with resume capability, virus scanning, format validation at upload
- **Processing mode**: Real-time for <1MB files, queue for larger files, user notification system
- **Large files**: Stream processing for 10-50MB PDFs, chunk extraction, memory usage <500MB per file
- **Failure handling**: Retry with exponential backoff (3 attempts), partial progress saving, user error notifications
- **Duplicate prevention**: SHA-256 file hashing + content similarity detection (>90% match threshold)
- **Content provenance**: Track original URL, upload timestamp, user ID, processing version for audit trail

## MVP Implementation Focus

**MVP Technical Specifications:**
1. **File upload**: POST /api/v1/files, accepts multipart/form-data, max 10MB, returns job ID
2. **Queue system**: PostgreSQL table with status enum (pending/processing/completed/failed), worker polls every 5s
3. **Supported formats**: PDF (text extraction), Markdown (parsing), Plain text (direct), JSON (validation)
4. **Progress tracking**: WebSocket endpoint /ws/jobs/{id} with percentage updates every 10% completion
5. **Error handling**: HTTP status codes + human-readable messages ("File too large" not "413 error")

## Phase 1 Deliverables

### Must Complete
1. **Docker & Local Development** - Everything runs locally first
2. **System Requirements** - Know the constraints
3. **PostgreSQL + Redis** - Core data layer
4. **Authentication** - Security from day one
5. **REST API with Swagger** - Interactive documentation required
6. **Data Ingestion** - Get content into the system
7. **Basic Monitoring** - Know when things break

### Required Research Brief Sections

**Format**: Markdown document with working code examples
1. **Executive Summary** (1 page) - Final architecture recommendation with 3 key decisions and rationale
2. **Decision Matrix** - Scoring table (1-5) for each technology across criteria: performance, complexity, cost, learning curve
3. **Architecture Diagram** - Docker containers + data flow diagram, exportable as PNG
4. **Technology Stack** - Specific versions (e.g., "PostgreSQL 15.3, FastAPI 0.100.0") with migration path from MVP
5. **Working Prototype** - GitHub repository with README, runs on fresh machine in <10 minutes
6. **Performance Benchmarks** - Load test results for target scenarios (100 concurrent users, 1K file uploads)
7. **Cost Analysis** - Monthly hosting costs for 10/100/1K users with breakeven calculations
8. **Risk Register** - Top 5 technical risks with probability, impact, and mitigation strategies
9. **Implementation Roadmap** - Task breakdown for Phase 2 development (no fixed deadlines, effort estimates only)

## Specific Learning Resources

### Framework Decision Support
- **FastAPI**: Tutorial sections 1-6, async database connections, WebSocket chat example
- **Docker**: Multi-stage builds, health checks, volume management, development vs production configs
- **PostgreSQL**: Connection pooling (pgbouncer), JSON columns vs separate tables, full-text search setup
- **Authentication**: fastapi-users examples, JWT refresh tokens, rate limiting implementations

### Architecture Research
- **Queue patterns**: Celery task routing, Redis pub/sub for real-time updates, database polling vs message brokers
- **File processing**: Chunked upload examples (tus.io), background job monitoring, memory-efficient PDF parsing
- **Monitoring**: Prometheus metrics collection, health check endpoints, structured logging with correlation IDs

### Real-World System Analysis
- **Obsidian file sync**: How they handle conflict resolution, file watching, incremental sync
- **Notion API**: Rate limiting (3 requests/second), pagination patterns, webhook reliability
- **GitHub API**: Authentication flows, webhook verification, API versioning strategies
- **Stripe API**: Idempotency keys, error handling, webhook endpoint security

## Measurable Success Criteria

Phase 1 research is complete when you demonstrate:

### Technical Proof Points
- **Technology decisions**: Score matrix comparing 3+ options for each major component (database, API framework, queue)
- **Working prototype**: Git repository that starts all services in <2 minutes, includes health checks at `/health`
- **API functionality**: Minimum 5 endpoints (auth, upload, list, search, status) with OpenAPI documentation
- **Performance baseline**: Load test results showing system handles 50 concurrent users with <500ms response time
- **Database operations**: CRUD operations + one complex query (JOIN or aggregation) executing in <100ms

### Documentation Deliverables
- **Architecture decision records**: One ADR per major technology choice with alternatives considered
- **Runbook**: Step-by-step guide for local development setup, testable by team member in <15 minutes
- **Cost model**: Hosting cost calculator with sliders for users/storage/requests, accurate within 20%
- **Risk assessment**: 5 technical risks with quantified probability/impact and specific mitigation plans
- **Phase 2 roadmap**: Development tasks broken into 2-4 hour increments with dependency mapping

### Verification Tests
- [ ] Fresh laptop can run full system from README instructions
- [ ] API documentation renders correctly and includes authentication examples
- [ ] Database schema supports all planned entities with proper relationships
- [ ] Cost estimates validated against actual cloud provider pricing
- [ ] Two team members can understand and critique the technical decisions