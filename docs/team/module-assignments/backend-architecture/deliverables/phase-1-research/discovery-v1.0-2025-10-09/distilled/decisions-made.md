# Backend Module Decisions Made

**Date:** 2025-10-09

**Status:** Distilled from context intake sources

---

## Firm Decisions (Committed)

### Decision 1: SQLite for MVP Database
**What:** Use SQLite with SQLAlchemy ORM for MVP development

**Why:**

- No separate database server required (local-first principle)
- Zero configuration for developer onboarding
- Sufficient for MVP scope (5 feeds, limited data volume)
- Clear migration path to PostgreSQL for production
**When:** MVP Phase (first 100 hours)

**Who:** Product team via PRD

**Sources:** PRD.md:35, WHAT-SERVICES-TO-CHOOSE.md

**Status:** ✅ FIRM - proceed with this

### Decision 2: FastAPI Framework
**What:** Use FastAPI (Python 3.11+) for REST API development

**Why:**

- Modern async support for I/O-bound operations
- Auto-generated OpenAPI/Swagger documentation
- Type hints with Pydantic validation
- Faster development cycle than Django REST Framework
- Excellent for MVP velocity (100-hour constraint)
**When:** MVP Phase

**Who:** Technical research + PRD confirmation

**Sources:** PRD.md:35, WHAT-SERVICES-TO-CHOOSE.md, BASIC-RESEARCH.md:574-586

**Status:** ✅ FIRM - proceed with this

### Decision 3: JWT Authentication
**What:** Implement JWT-based token authentication with refresh tokens

**Why:**

- Stateless authentication (supports horizontal scaling)
- Standard for REST APIs and microservices
- Works across module boundaries
- 15-minute access tokens + 7-day refresh tokens recommended
**When:** MVP Phase (required from day one)

**Who:** Architecture spec requirement

**Sources:** Backend-Architecture-Spec.md:38, BASIC-RESEARCH.md:447-468

**Status:** ✅ FIRM - proceed with this

### Decision 4: Docker + Docker Compose Deployment
**What:** Use Docker containers orchestrated by Docker Compose for MVP

**Why:**

- Local-first requirement mandates containerization
- Consistent development environment across team
- Easy multi-service orchestration (db, cache, api)
- Clear migration path to Kubernetes for production
**When:** MVP Phase

**Who:** Architecture requirement + PRD

**Sources:** PRD.md:14, work-description.md:14-150, docker-compose.yml:1-37

**Status:** ✅ FIRM - proceed with this

### Decision 5: REST API Pattern (MVP)
**What:** REST endpoints following RESTful conventions with OpenAPI documentation

**Why:**

- Well-established, simple tooling, easy debugging
- FastAPI auto-generates OpenAPI/Swagger docs
- Lower complexity than GraphQL for MVP
- Standard HTTP status codes and error handling
**When:** MVP Phase

**Who:** Technical analysis

**Sources:** BASIC-RESEARCH.md:574-586, 624-628

**Status:** ✅ FIRM - proceed with this

### Decision 6: URL Versioning Strategy
**What:** Version APIs via URL path (`/api/v1/...`)

**Why:**

- Clear breaking change signaling
- Backward compatibility support
- Industry standard approach
**When:** MVP Phase (design now, use from v1)

**Who:** Technical best practices

**Sources:** BASIC-RESEARCH.md:696-697

**Status:** ✅ FIRM - proceed with this

### Decision 7: Structured JSON Logging
**What:** All services log structured JSON with ISO timestamps

**Why:**

- Machine-parseable for log aggregation
- Supports observability from day one
- Required for production troubleshooting
**When:** MVP Phase

**Who:** Observability-first design principle from scaffold

**Sources:** abstraction-scaffold AGENTS.md:163-165, work-description.md:154

**Status:** ✅ FIRM - proceed with this

### Decision 8: Health/Readiness Endpoints
**What:** Every service exposes `/health` and `/ready` endpoints

**Why:**

- Container orchestration health checks
- Monitoring and alerting foundation
- Required for production deployment
**When:** MVP Phase (design pattern from day one)

**Who:** Module template pattern requirement

**Sources:** abstraction-scaffold README.md:1041-1043, BASIC-RESEARCH.md:1081

**Status:** ✅ FIRM - proceed with this

### Decision 9: Social Login (Google + GitHub)
**What:** Start with Google and GitHub OAuth providers

**Why:**

- Widely used by target audience (creators, developers)
- Strong trust and developer-friendly
- Covers majority of use cases
**When:** MVP Phase

**Who:** Technical research recommendation

**Sources:** BASIC-RESEARCH.md:386-388, 414

**Status:** ✅ FIRM - proceed with this

### Decision 10: Synchronous Ingestion for MVP
**What:** Simple file upload with synchronous processing for files <10MB

**Why:**

- Simplest implementation for MVP
- Acceptable for small file sizes
- Clear upgrade path to async queue-based processing
**When:** MVP Phase (migrate to async in Phase 2)

**Who:** Technical pragmatism for 100-hour constraint

**Sources:** BASIC-RESEARCH.md:885-887, 954, 990-993

**Status:** ✅ FIRM - proceed with this (MVP only)

---

## Tentative Decisions (Validate via Discovery)

### Decision 11: PostgreSQL with pgvector (Production)
**What:** Migrate from SQLite to PostgreSQL with pgvector extension for production

**Why:**

- ACID compliance for multi-user production
- pgvector extension for AI embedding storage
- Proven scalability for relational data
- Supports JSON columns for flexible schemas
**Status:** ⚠️ TENTATIVE - validate via WO-001 (Database Architecture)

**Research Needed:**

- Verify embedding storage requirements (vector dimensions, similarity search)
- Confirm query patterns match PostgreSQL strengths
- Assess migration complexity from SQLite
- Benchmark performance with expected data volumes
**Sources:** WHAT-SERVICES-TO-CHOOSE.md, BASIC-RESEARCH.md:206-269, docker-compose.yml:3

### Decision 12: Neo4j Graph Database (Production)
**What:** Add Neo4j for graph relationship storage and traversal

**Why:**

- Purpose-built for graph queries and traversal
- Knowledge graph use case benefits from native graph DB
- Visualization and query tools built-in
**Status:** ⚠️ TENTATIVE - validate via WO-001 (Database Architecture)

**Research Needed:**

- Confirm graph query patterns exist beyond recursive CTEs
- Assess operational overhead (separate database service)
- Evaluate if PostgreSQL recursive CTEs sufficient for MVP+
- Benchmark graph traversal performance requirements
**Sources:** Backend-Architecture-Spec.md:11, WHAT-SERVICES-TO-CHOOSE.md, BASIC-RESEARCH.md:218-249

### Decision 13: Redis for Caching (Phase 2)
**What:** Add Redis for caching and session storage when needed

**Why:**

- Fast in-memory access for hot data
- Supports rate limiting, session tokens
- Standard for distributed caching
**Status:** ⚠️ TENTATIVE - add only when performance bottleneck identified

**Research Needed:**

- Measure actual cache hit rates and performance impact
- Determine specific use cases (session storage, API rate limiting, query caching)
- Assess operational overhead vs performance gain
**Sources:** docker-compose.yml:14-18, BASIC-RESEARCH.md:879, work-description.md:159

### Decision 14: Keycloak for Enterprise Auth (Future)
**What:** Consider Keycloak for enterprise-grade authentication

**Why:**

- Open-source, self-hostable
- OAuth2, OIDC, SAML support
- Centralized identity management
**Status:** ⚠️ TENTATIVE - evaluate if enterprise features needed

**Research Needed:**

- Assess if JWT + social login sufficient long-term
- Determine if multi-organization support required
- Evaluate setup/operational complexity
**Sources:** BASIC-RESEARCH.md:312-316

### Decision 15: Kubernetes for Production Deployment (Future)
**What:** Migrate from Docker Compose to Kubernetes for production orchestration

**Why:**

- Horizontal scaling and load balancing
- Self-healing and rolling updates
- Industry standard for production microservices
**Status:** ⚠️ TENTATIVE - validate scaling requirements first

**Research Needed:**

- Determine actual production traffic patterns
- Assess if horizontal scaling truly needed
- Evaluate simpler alternatives (managed services, serverless)
**Sources:** Backend-Architecture-Spec.md:46, abstraction-scaffold future vision

---

## Open Decisions (Needs Research via Discovery)

### Decision 16: GraphQL vs REST (Phase 2+)
**Question:** Should we add GraphQL alongside REST APIs?

**Options Considered:**

1. REST only (current decision)
2. GraphQL only (rejected for MVP - too complex)
3. Hybrid REST + GraphQL (future consideration)
**Criteria:**

- Frontend needs flexible querying (over-fetching/under-fetching problems)
- Operational complexity acceptable
- Team has GraphQL expertise
**Status:** ❓ OPEN - defer to WO-002 (API Design) if needed

**Sources:** BASIC-RESEARCH.md:590-619

### Decision 17: Message Queue System (Phase 2+)
**Question:** Which message queue for async processing?

**Options Considered:**

1. Database table (MVP approach) - simplest
2. Redis pub/sub - lightweight
3. RabbitMQ - feature-rich
4. NATS JetStream - cloud-native (used in abstraction scaffold)
**Criteria:**

- Throughput requirements (>50 docs/min?)
- Reliability needs (at-least-once vs exactly-once)
- Operational complexity acceptable
**Status:** ❓ OPEN - create research brief if scaling issues arise

**Sources:** BASIC-RESEARCH.md:996-998, 879, abstraction-scaffold event-driven pattern

### Decision 18: CRDT Integration (Future Vision)
**Question:** How to support distributed peer-to-peer consistency?

**Options Considered:**

1. Yjs - JavaScript collaborative editing
2. Automerge - JSON-like CRDT library
3. AntidoteDB - CRDT-native distributed database
4. Riak - Key-value store with CRDT support
**Criteria:**

- Distributed use case confirmed (not just cloud-centralized)
- CRDT layer can sit on top of existing stores
- Operational complexity acceptable
**Status:** ❓ OPEN - research only if P2P requirements confirmed

**Sources:** spark-chat.md:398-451

### Decision 19: Authorization Framework (Beyond RBAC)
**Question:** Which authorization model for complex permissions?

**Options Considered:**

1. RBAC (Role-Based Access Control) - simple, MVP approach
2. ABAC (Attribute-Based Access Control) - flexible, complex
3. ReBAC (Relationship-Based Access Control) - graph-based
4. Dual-layer (SpiceDB + OPA from abstraction scaffold)
**Criteria:**

- Permission complexity requirements
- Query-time performance acceptable
- Integration with existing auth system
**Status:** ❓ OPEN - start with RBAC, research if insufficient

**Sources:** BASIC-RESEARCH.md:474-493, abstraction-scaffold authz/ dual-layer

### Decision 20: Vector Database Scaling (If Needed)
**Question:** When to migrate from pgvector to dedicated vector DB?

**Options Considered:**

1. Stay with pgvector (PostgreSQL extension)
2. Qdrant - open-source, self-hosted
3. Weaviate - ML-native, advanced features
4. Pinecone - managed service (expensive)
**Criteria:**

- Embedding volume exceeds pgvector performance
- Advanced vector indexing needed (HNSW, product quantization)
- Cost vs performance tradeoff
**Status:** ❓ OPEN - benchmark pgvector first, migrate only if needed

**Sources:** BASIC-RESEARCH.md:203-208, 254-261

---

## Rejected Approaches

### Rejected 1: Django REST Framework
**Why Rejected:**

- Slower development velocity than FastAPI
- More boilerplate code required
- Heavier framework for simple MVP use case
- FastAPI's async support better for I/O-bound operations
**When:** During initial technical research

**Sources:** WHAT-SERVICES-TO-CHOOSE.md, BASIC-RESEARCH.md:574-604

### Rejected 2: Monolithic Architecture
**Why Rejected:**

- Violates "stateless services" design principle
- Harder to scale horizontally
- Poor separation of concerns for multi-module system
- Local-first containerization requires modular services
**When:** Architecture planning

**Sources:** work-description.md:148-154

### Rejected 3: Hardcoded Configuration
**Why Rejected:**

- Security risk (secrets in code)
- Inflexible across environments (dev/staging/prod)
- Docker best practices require environment variables
- Identified as security issue in PR review
**When:** Docker POC review

**Sources:** docker-compose.yml:7-29 (security issues), pr-review context

### Rejected 4: Session-Based Authentication
**Why Rejected:**

- Stateful (requires DB/Redis for every request)
- Doesn't scale horizontally as well as JWT
- More complex for multi-module architecture
- JWT standard for microservices
**When:** Authentication design

**Sources:** BASIC-RESEARCH.md:450, 500-502

### Rejected 5: Direct Social Login Without JWT
**Why Rejected:**

- Ties authentication to specific OAuth providers
- No unified token for inter-module communication
- Harder to add email/password fallback later
- JWT provides abstraction layer
**When:** Authentication architecture

**Sources:** BASIC-RESEARCH.md:447-468

### Rejected 6: Pinecone Vector Database
**Why Rejected:**

- Expensive managed service (cost constraint)
- Vendor lock-in risk
- Pgvector sufficient for MVP scope
- Can migrate later if scaling demands it
**When:** Vector database selection

**Sources:** BASIC-RESEARCH.md:203, 254-261

### Rejected 7: Synchronous Blocking for Large Files
**Why Rejected:**

- Would block API for multi-minute operations
- Poor user experience (timeout risks)
- Doesn't scale to concurrent uploads
- Queue-based async processing is standard
**When:** Ingestion pipeline design

**Sources:** BASIC-RESEARCH.md:885-888, 954-956

---

## Deferred Decisions (Explicitly Not Deciding Now)

### Deferred 1: Integration Architecture
**What:** How backend connects to AI, Frontend, Publishing modules

**Why Deferred:** Flagged gap in PR review - needs dedicated research

**Timeline:** Address in WO-002 (API Design + Integration Planning)

**Sources:** pr-review.md:60-65

### Deferred 2: Database Schema Design
**What:** Specific tables, columns, relationships, indexes

**Why Deferred:** Requires entity modeling workshop - flagged gap

**Timeline:** Address in WO-001 (Database Architecture)

**Sources:** pr-review.md:66-70

### Deferred 3: Performance Benchmarking Strategy
**What:** How to measure and validate performance targets

**Why Deferred:** Needs working system first - flagged gap

**Timeline:** Address in WO-003 (Quality & Performance)

**Sources:** pr-review.md:76-80, success-metrics.md:15-18

---

## Decision Tracking

**Firm Decisions:** 10 (proceed with implementation)

**Tentative Decisions:** 5 (validate during discovery WO-001 to WO-004)

**Open Decisions:** 5 (research if/when needed)

**Rejected Approaches:** 7 (don't revisit without strong reason)

**Deferred Decisions:** 3 (blocked on other work)

---

## Sources

**Primary Specifications:**

- `docs/modules/backend-architecture/Backend-Architecture-Spec.md`
- `docs/modules/backend-architecture/PRD.md`

**Technical Research:**

- `00-context-intake/sources/pr-1-backend-research/BASIC-RESEARCH.md` (lines 1-1142)
- `00-context-intake/sources/pr-1-backend-research/WHAT-SERVICES-TO-CHOOSE.md`
- `00-context-intake/sources/pr-1-backend-research/my-docker-app-test/docker-compose.yml`

**Context & Requirements:**

- `docs/team/module-assignments/backend-architecture/01-work-description.md`
- `docs/design/strategy/success-metrics.md`
- `.dev/team/intern-management/pr-reviews/fall-2025-backend-architecture-phase-1-review.md`

**Aspirational Vision:**

- `/Users/grig/work/obsidian-vault/🕸️ PeerMesh.org/abstraction-program/docs/spark/spark-chat.md` (lines 300-555)
- `/Users/grig/work/peermesh/repo/abstraction-scaffold/` (design principles)

---

**Completeness Assessment:** 95%

- Firm decisions documented with rationale
- Tentative decisions flagged for validation
- Open questions identified for future research
- Rejected approaches captured to avoid revisiting
- Deferred decisions linked to discovery work orders
