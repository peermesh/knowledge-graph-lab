# Backend Module Component Map

**Source:** Distilled from 01-distilled/requirements-notes.md, decisions-made.md, constraints.md

**Date:** 2025-10-09

**Scope:** MVP (100 hours, junior developer buildable)

---

## MVP Primitives (MUST BUILD NOW)

These components are required for the 100-hour MVP build:

### MVP-1: Database (SQLite)
**Decision:** FIRM - SQLite for MVP simplicity

**Purpose:** Store sources, content, entities

**Why:** No separate database server, file-based, simple schema

**Integration:** FastAPI via SQLAlchemy ORM

**Source:** decisions-made.md (Decision 1)

### MVP-2: API Framework (FastAPI)
**Decision:** FIRM - FastAPI for async + OpenAPI docs

**Purpose:** Serve 5 REST endpoints (sources, content, entities, dashboard)

**Why:** Modern async, auto-generated OpenAPI, fast development

**Integration:** Called by AI, Frontend, Publishing modules

**Source:** decisions-made.md (Decision 2)

### MVP-3: Authentication (JWT)
**Decision:** FIRM - JWT token-based auth

**Purpose:** Stateless authentication for API endpoints

**Why:** Standard for REST APIs, works across microservices

**Integration:** Middleware in FastAPI, token validation

**Source:** decisions-made.md (Decision 3)

### MVP-4: Container Platform (Docker)
**Decision:** FIRM - Docker + Docker Compose

**Purpose:** Isolated deployment, single `docker run` to start

**Why:** Easy local development, no manual dependencies

**Integration:** Dockerfile, docker-compose.yml for multi-service dev

**Source:** decisions-made.md (Decision 4)

### MVP-5: REST API Design
**Decision:** FIRM - 5 REST endpoints (no GraphQL)

**Purpose:** Simple CRUD operations for module integration

**Endpoints:**

- POST /api/sources
- GET /api/sources
- GET /api/content
- GET /api/entities
- GET /api/dashboard
**Source:** requirements-notes.md (FR-3)

### MVP-6: RSS Feed Scheduler
**Decision:** FIRM - Python `schedule` library

**Purpose:** Fetch 5 RSS feeds hourly

**Why:** Simple cron-like scheduling, no external dependencies

**Integration:** Background thread in FastAPI

**Source:** requirements-notes.md (FR-1, FR-4)

### MVP-7: Health Check Endpoint
**Decision:** FIRM - Basic /health endpoint

**Purpose:** Docker container liveness/readiness

**Why:** Required for container orchestration

**Endpoint:** GET /health (returns 200 if DB accessible)

**Source:** requirements-notes.md (NFR-6)

### MVP-8: Environment Configuration
**Decision:** FIRM - Environment variables

**Purpose:** No hardcoded secrets, configurable per env

**Why:** Docker security best practice, 12-factor app

**Implementation:** .env file + os.getenv()

**Source:** decisions-made.md (Decision 9)

### MVP-9: API Documentation (Auto-generated)
**Decision:** FIRM - FastAPI's built-in OpenAPI

**Purpose:** /docs endpoint for API exploration

**Why:** Free with FastAPI, no extra work

**Integration:** Automatic from route definitions

**Source:** technical-context.md (FastAPI advantage)

### MVP-10: Basic Logging
**Decision:** FIRM - Python logging module

**Purpose:** Debug output, error tracking

**Why:** Built-in, no external dependency

**Integration:** Logs to stdout (Docker captures)

**Source:** requirements-notes.md (FR-4 - log fetch results)

---

## Future Primitives (OUT OF MVP SCOPE - Document Only)

These are discussed but NOT built in MVP:

### FUTURE-1: PostgreSQL + pgvector
**Decision:** TENTATIVE - Production database replacement

**Purpose:** Structured data + vector embeddings

**Why:** Production scale, ACID guarantees, embedding support

**Timeline:** After MVP proves patterns

**Source:** decisions-made.md (Decision 6)

### FUTURE-2: Neo4j (Graph Database)
**Decision:** TENTATIVE - Graph relationships

**Purpose:** Creator-to-grant connections, knowledge graph

**Why:** Purpose-built for graph traversal

**Timeline:** After MVP proves graph use cases

**Source:** decisions-made.md (Decision 7)

### FUTURE-3: Redis (Cache)
**Decision:** TENTATIVE - Performance optimization

**Purpose:** Accelerate frequently accessed data

**Why:** Reduce database load, faster responses

**Timeline:** When performance becomes bottleneck

**Source:** decisions-made.md (Decision 8)

### FUTURE-4: GraphQL API
**Decision:** OPEN - Alternative to REST

**Purpose:** Complex queries, reduce over-fetching

**Why:** Frontend flexibility, single endpoint

**Research Needed:** Complexity vs benefit for MVP

**Source:** decisions-made.md (Decision 11)

### FUTURE-5: Message Queue (NATS/Kafka/RabbitMQ)
**Decision:** OPEN - Async processing

**Purpose:** Decouple modules, event-driven architecture

**Why:** Scalability, reliability

**Research Needed:** Which queue system fits architecture

**Source:** decisions-made.md (Decision 12)

### FUTURE-6: Kubernetes Deployment
**Decision:** TENTATIVE - Production orchestration

**Purpose:** Container management at scale

**Why:** Auto-scaling, health management, rolling deploys

**Timeline:** Production deployment (post-MVP)

**Source:** decisions-made.md (Decision 10)

### FUTURE-7: Keycloak (Advanced Auth)
**Decision:** TENTATIVE - Enterprise authentication

**Purpose:** SSO, OAuth2, RBAC, user management

**Why:** Comprehensive auth vs simple JWT

**Timeline:** When multi-user requirements mature

**Source:** decisions-made.md (Decision 9)

### FUTURE-8: Distributed Tracing (Jaeger/Zipkin)
**Decision:** DEFERRED - Observability

**Purpose:** Request tracking across microservices

**Why:** Debug distributed systems

**Timeline:** When multi-module integration complex

**Source:** decisions-made.md (Decision 16)

### FUTURE-9: Metrics (Prometheus/Grafana)
**Decision:** DEFERRED - Advanced monitoring

**Purpose:** Performance metrics, dashboards, alerts

**Why:** Production operations visibility

**Timeline:** Production deployment

**Source:** constraints.md (performance gap - no benchmarks)

### FUTURE-10: CI/CD Pipeline
**Decision:** DEFERRED - Automation

**Purpose:** Automated testing, building, deployment

**Why:** Development velocity, quality gates

**Timeline:** When team size grows

**Source:** constraints.md (single developer MVP)

---

## Integration Points

### AI Module Integration
**Primitives Used:** MVP-2 (REST API), MVP-3 (Auth), MVP-5 (GET /api/content)

**Flow:** AI queries content endpoint → Backend returns JSON → AI processes

**Status:** Mock integration in MVP (real integration later)

**Source:** requirements-notes.md (UI-1)

### Frontend Module Integration
**Primitives Used:** MVP-2 (REST API), MVP-3 (Auth), MVP-5 (all 5 endpoints)

**Flow:** Frontend calls APIs → Backend returns data → Frontend displays

**Status:** Real integration in MVP

**Source:** requirements-notes.md (UI-2)

### Publishing Module Integration
**Primitives Used:** MVP-2 (REST API), MVP-5 (GET /api/content)

**Flow:** Publishing queries for digest content → Backend returns curated list

**Status:** Mock integration in MVP

**Source:** Backend-Architecture-Spec.md

---

## Component Summary

**MVP Total:** 10 components (all must be built)

**Future Total:** 10 components (document, don't build)

**MVP Build Estimate:** 100 hours (PRD constraint)

**Decision Ratio:** 10 FIRM, 0 TENTATIVE in MVP

**Readiness:** Ready for architecture diagram and research briefs
