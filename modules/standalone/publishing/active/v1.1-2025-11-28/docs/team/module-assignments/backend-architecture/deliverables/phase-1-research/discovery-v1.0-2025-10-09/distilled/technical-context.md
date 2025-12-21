# Backend Module - Technical Context

**Date:** 2025-10-09

**Distilled from:** BASIC-RESEARCH.md, WHAT-SERVICES-TO-CHOOSE.md, my-docker-app-test/, Backend-Architecture-Spec.md

---

## Architecture Discussions

### Approach A: Simple Standalone Backend (MVP Focus)
**Discussed in:** PRD.md, intern research summary

**Description:**

- Single Python/FastAPI service
- SQLite database
- Docker container
- 5 RSS feeds, 5 APIs
- Mock integrations

**Pros:**

- Fastest path to working system
- Junior developer buildable (100 hours)
- Low operational complexity
- Easy local development
- Validates core patterns

**Cons:**

- Not production-scale
- SQLite limits (concurrent writes, size)
- Mock AI integration (needs replacement later)
- Missing observability
- No redundancy/HA

**Status:** ✅ Recommended for MVP

**Source:** PRD.md Executive Summary, lines 7-8

---

### Approach B: Multi-Database Architecture (Production Vision)
**Discussed in:** Backend-Architecture-Spec.md, BASIC-RESEARCH.md

**Description:**

- PostgreSQL for structured data + pgvector for embeddings
- Neo4j for graph relationships
- Redis for caching
- Multiple services
- Complex data synchronization

**Pros:**

- Production-scale capable
- Specialized databases for specific use cases
- Graph traversal performance (Neo4j)
- Vector similarity search (pgvector)

**Cons:**

- Operational complexity (3 databases)
- Data consistency challenges
- Higher infra costs
- Steep learning curve
- Longer development time

**Status:** ⏸️ Considered but deferred to Phase 2+

**Source:** Backend-Architecture-Spec.md lines 10-11, BASIC-RESEARCH.md lines 153-200

---

### Approach C: Microservices with Message Queues
**Discussed in:** Backend-Architecture-Spec.md, abstraction scaffold

**Description:**

- Separate services: API, Ingestion, Processing
- Message queue (RabbitMQ or Redis) for async work
- Event-driven architecture
- Service mesh for inter-service communication

**Pros:**

- Scalable independently
- Fault isolation
- Technology flexibility per service
- Async processing patterns

**Cons:**

- Distributed system complexity
- Network latency between services
- Monitoring challenges
- Development/testing difficulty
- Overkill for MVP

**Status:** ❌ Rejected for MVP (too complex)

**Source:** Backend-Architecture-Spec.md lines 89-90, abstraction scaffold (future vision)

---

## Technology Options Discussed

### Category: Database

**Options Mentioned:**

1. **SQLite** (MVP choice)
2. **PostgreSQL + pgvector** (production)
3. **Neo4j** (graph relationships)
4. **MongoDB** (document + vector search)
5. **Redis** (caching)

**Discussion Summary:**

**SQLite:**

- ✅ Zero-config, single file, perfect for MVP
- ✅ No server setup required
- ❌ Limited concurrent writes
- ❌ Not production-scale
- **When:** MVP development, testing, edge deployments
- **Source:** PRD.md line 37, BASIC-RESEARCH.md lines 183-189

**PostgreSQL + pgvector:**

- ✅ ACID compliance, mature SQL
- ✅ `pgvector` extension for embeddings
- ✅ Handles medium-scale vector workloads
- ❌ Requires server management
- ❌ Scaling to millions of vectors needs sharding
- **When:** Production deployment, need transactional integrity
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 3-10, Backend-Architecture-Spec.md line 10

**Neo4j:**

- ✅ Optimized graph traversals (Cypher query language)
- ✅ Graph algorithms built-in
- ❌ Slower bulk inserts (transactional mode)
- ❌ Requires tuning for high-volume writes
- **When:** Complex relationship queries, multi-hop traversals
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 22-28

**Decision Pending:** SQLite for MVP confirmed, PostgreSQL + Neo4j for production (needs architecture diagram)

---

### Category: API Framework

**Options Mentioned:**

1. **FastAPI** (async, modern)
2. **Django REST Framework** (batteries-included)
3. **Flask** (lightweight)

**Discussion Summary:**

**FastAPI:**

- ✅ Async-first design (high performance)
- ✅ Automatic OpenAPI/Swagger docs (0-1 manual steps)
- ✅ Type hints → automatic validation
- ❌ Less batteries-included (must add auth, admin yourself)
- **Benchmark:** API docs generation in <5 steps - FastAPI wins (0-1 steps)
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 40-45, PRD.md line 36

**Django REST Framework:**

- ✅ Full-stack features (auth, admin, ORM)
- ✅ Mature ecosystem, battle-tested
- ✅ Opinionated structure (faster prototyping)
- ❌ Heavier, slower performance
- ❌ More ceremony/setup
- **When:** Large apps needing full ecosystem
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 49-54

**Flask:**

- ✅ Lightweight, minimal boilerplate
- ✅ Maximum flexibility
- ❌ No built-in async
- ❌ No automatic docs (need plugins)
- **When:** Microservices, small APIs
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 58-63

**Decision:** FastAPI chosen for MVP (automatic docs, async, performance)

---

### Category: Deployment & Orchestration

**Options Mentioned:**

1. **Docker Compose** (local dev)
2. **Kubernetes** (production scale)
3. **Docker Swarm** (simple clustering)

**Discussion Summary:**

**Docker Compose:**

- ✅ Extremely simple (`docker-compose.yml`)
- ✅ One command to start everything (`docker compose up`)
- ✅ Perfect for dev/test
- ❌ Not for production scaling
- ❌ Limited orchestration features
- **Benchmark:** Services start in <10 seconds
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 81-86, PRD.md lines 92-95

**Kubernetes:**

- ✅ Production-grade orchestration
- ✅ Auto-scaling, self-healing
- ✅ Cloud-native ecosystem
- ❌ Steep learning curve
- ❌ Complex YAML/config
- ❌ Slower iteration for small teams
- **Benchmark:** Services start in 20-30s (slower than Compose)
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 90-95

**Decision:** Docker Compose for MVP, Kubernetes for production (deferred)

---

### Category: Authentication

**Options Mentioned:**

1. **JWT** (stateless)
2. **Session Cookies** (server state)
3. **OAuth** (third-party)

**Discussion Summary:**

**JWT:**

- ✅ Stateless (no server storage)
- ✅ Easy horizontal scaling
- ✅ Works across microservices
- ❌ Token revocation is hard
- ❌ Must secure signing keys
- **Benchmark:** <10ms per request overhead
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 121-126, Backend-Architecture-Spec.md line 39

**OAuth:**

- ✅ Standardized, secure delegation
- ✅ Social login + enterprise SSO
- ❌ Implementation complexity
- ❌ More moving parts
- **When:** Third-party identity providers
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 139-144

**Decision:** JWT for MVP (simplicity), OAuth consideration for Phase 2

---

### Category: Message Queue

**Options Mentioned:**

1. **Redis** (simple, fast)
2. **RabbitMQ** (reliable, enterprise)
3. **Database Table** (MVP minimal)

**Discussion Summary:**

**Redis:**

- ✅ Extremely fast (in-memory)
- ✅ Simple commands (`LPUSH`/`BRPOP`)
- ❌ Persistence optional (may lose jobs)
- **Benchmark:** >50 jobs/minute easily
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 161-166

**RabbitMQ:**

- ✅ Guaranteed delivery, acknowledgments
- ✅ Battle-tested, durable queues
- ❌ More operational complexity
- ❌ Slower than Redis
- **Benchmark:** 50 jobs/minute with reliability
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 170-175

**Database Table:**

- ✅ Leverages existing infra
- ✅ Easy to implement (just a table)
- ❌ Poor performance at scale
- ❌ DB contention risk
- **When:** MVP with minimal setup
- **Source:** WHAT-SERVICES-TO-CHOOSE.md lines 179-184

**Decision:** Mock for MVP (no queue needed initially), Database Table if needed, RabbitMQ for production

---

## Trade-offs Analyzed

### Trade-off 1: Simplicity vs Future-Proofing

**Discussion:**

Do we build for current needs (SQLite, simple stack) or design for future scale (PostgreSQL, multiple databases, queues)?

**Arguments for Simplicity:**

- Get to working system faster (100-hour constraint)
- Validate assumptions before investing in complexity
- Junior developer can complete
- Easier to debug/test

**Arguments for Future-Proofing:**

- Avoid costly migrations later
- Design decisions matter (schema compatibility)
- Some complexity is unavoidable (will need PostgreSQL eventually)

**Resolution:**

✅ **Simplicity for MVP, with migration path designed**

- Use SQLite now
- Design schema compatible with PostgreSQL
- Plan migration strategy (documented, not implemented)
- Accept that some refactoring will be needed

**Source:** PRD.md "Keep it simple - this is an MVP" (line 194), PR review minimal effort critique

---

### Trade-off 2: Real Integration vs Mocking

**Discussion:**

Should MVP integrate with real AI module or use mock responses?

**Arguments for Real Integration:**

- Tests integration patterns early
- More realistic demo
- Less throwaway work

**Arguments for Mocking:**

- Enables parallel development (doesn't wait for AI module)
- Reduces complexity
- Faster MVP completion
- Clear API contract (forces interface design)

**Resolution:**

✅ **Mock for MVP, design API contract carefully**

- Return placeholder/mock data from `/api/entities`
- Document expected API contract
- Design for real integration later (queues, webhooks)

**Source:** PRD.md line 15, Backend-Architecture-Spec.md lines 86-95

---

### Trade-off 3: Docker Security vs Development Speed

**Discussion:**

Intern's Docker POC has security issues (hardcoded secrets, no non-root user). Fix now or later?

**Security Concerns:**

- Hardcoded database passwords in docker-compose.yml
- Running as root user
- No health checks
- No resource limits

**Arguments for Fixing Now:**

- Security should be default
- Good habits early
- Not significantly slower

**Arguments for Later:**

- MVP is local dev only
- Can fix before production
- Don't over-engineer

**Resolution:**

⚠️ **Fix critical issues now, defer advanced security**

- ✅ Use `.env` file for secrets (don't hardcode)
- ✅ Non-root user in Dockerfile
- ⏸️ Defer: Vault/secret managers, advanced network isolation

**Source:** BASIC-RESEARCH.md lines 62-83, PR review security gap (lines 69-70)

---

## Patterns and Prior Art

### Pattern: Schedule-Based RSS Fetching

**Mentioned in:** BASIC-RESEARCH.md, PRD.md

**Pattern Description:**

- Use Python `schedule` library for periodic tasks
- Hourly fetch schedule
- Simple cron-like syntax

**Example:**
```python
import schedule
import time

def fetch_rss_feeds():
    # Fetch logic here
    pass

schedule.every().hour.do(fetch_rss_feeds)

while True:
    schedule.run_pending()
    time.sleep(60)
```

**Relevance:** Simple pattern for MVP, proven in many projects

**Alternative Considered:** Celery Beat (too complex for MVP)

**Source:** PRD.md line 39, BASIC-RESEARCH.md (scheduler discussion)

---

### Pattern: Docker Multi-Stage Builds

**Mentioned in:** BASIC-RESEARCH.md Docker patterns

**Pattern Description:**

- Separate build stage from runtime stage
- Smaller final image (only runtime dependencies)
- Security benefit (no build tools in production image)

**Relevance:** Best practice for Docker deployment

**Status:** Recommended for implementation

**Source:** BASIC-RESEARCH.md Docker patterns discussion

---

### Pattern: Database Migrations on Startup

**Mentioned in:** BASIC-RESEARCH.md lines 130-150

**Pattern Description:**

- Option 1: Dedicated migration container
- Option 2: Run migrations at app startup
- Option 3: CI/CD pipeline integration

**Discussion:**

- **Dev:** Auto-run migrations for convenience
- **Prod:** Separate migration step for safety/rollback

**Relevance:** Critical for database version control

**Status:** ❌ GAP - No migration strategy defined yet

**Source:** BASIC-RESEARCH.md migration discussion

---

## Open Technical Questions

### Question 1: RSS Feed Parsing Robustness
**Question:** How to handle malformed RSS feeds?

**Considerations:**

- Different RSS/Atom formats
- Invalid XML
- Encoding issues
- Missing required fields

**Needs:** Error handling strategy, feed validation

**Source:** PRD.md risk mitigation (line 140)

---

### Question 2: Duplicate Content Detection
**Question:** What algorithm for detecting duplicates?

**Options Discussed:**

- URL-based (simple, PRD default)
- Content hashing (more robust)
- Title + date matching

**Considerations:**

- Same content, different URLs?
- URL variations (http vs https, query params)?
- Performance implications?

**Needs:** Algorithm specification

**Source:** PRD.md question 3 (line 192)

---

### Question 3: Vector Embedding Strategy
**Question:** When to add vector embeddings?

**Context:**

- pgvector mentioned in spec
- Not in MVP scope
- But schema design matters now

**Considerations:**

- Add embedding column to content table later?
- Separate embeddings table?
- How to backfill existing content?

**Needs:** Future-compatible schema design

**Source:** Backend-Architecture-Spec.md, BASIC-RESEARCH.md pgvector discussion

---

### Question 4: API Versioning Strategy
**Question:** How to handle API changes?

**Context:**

- `/api/v1/` prefix suggested
- But no versioning strategy defined

**Considerations:**

- URL versioning vs header versioning?
- Deprecation policy?
- Breaking vs non-breaking changes?

**Needs:** API evolution strategy

**Source:** Backend-Architecture-Spec.md line 33 (mentions `/api/v1/`)

---

## Technology Stack Recommendations (from Research)

### Intern's "CHOOSE THIS" Recommendations

**From WHAT-SERVICES-TO-CHOOSE.md:**

1. **Database:** PostgreSQL + pgvector ✅
   - For production (not MVP)
   - Rationale: Mature, ACID, handles vectors

2. **API Framework:** Django REST or FastAPI ✅
   - PRD chose FastAPI
   - Rationale: Modern, async, auto docs

3. **Orchestration:** Kubernetes ✅
   - For production (not MVP)
   - Rationale: Standard for cloud-native

4. **Auth:** OAuth ✅
   - For production (not MVP)
   - Rationale: SSO, third-party identity

5. **Message Queue:** RabbitMQ ✅
   - For production (not MVP)
   - Rationale: Reliable, battle-tested

**Analysis:** Reasonable recommendations but mostly beyond MVP scope. Shows understanding of production requirements but didn't distinguish MVP vs production well.

**Source:** WHAT-SERVICES-TO-CHOOSE.md (all "CHOOSE THIS" markers)

---

## Docker Configuration Analysis

### Intern's Docker POC

**Files Reviewed:**

- `my-docker-app-test/docker-compose.yml`
- `my-docker-app-test/api/` (incomplete)

**What Works:**

- ✅ Basic multi-service setup (PostgreSQL, Redis, API)
- ✅ Includes pgvector extension
- ✅ Service dependencies defined

**Security Issues Found (PR Review):**

- ❌ Hardcoded secrets in docker-compose.yml
- ❌ No health checks
- ❌ No restart policies
- ❌ No non-root user
- ❌ No resource limits
- ❌ No network isolation

**Operational Issues:**

- ❌ Missing volume backups
- ❌ No environment separation (dev/prod)
- ❌ Over-commented (style issue)

**Status:** Good starting point, needs hardening

**Source:** PR review lines 69-70, my-docker-app-test/ directory

---

## Sources Consulted

**Technology Research:**

1. `00-context-intake/sources/pr-1-backend-research/BASIC-RESEARCH.md` - Docker patterns, database selection, security, migrations
2. `00-context-intake/sources/pr-1-backend-research/WHAT-SERVICES-TO-CHOOSE.md` - Technology comparisons, recommendations
3. `00-context-intake/sources/pr-1-backend-research/my-docker-app-test/` - Docker POC example

**Architecture References:**

4. `docs/modules/backend-architecture/Backend-Architecture-Spec.md` - Production architecture vision
5. `docs/modules/backend-architecture/PRD.md` - MVP technical stack

**Gap Analysis:**

6. `.dev/team/intern-management/pr-reviews/fall-2025-backend-architecture-phase-1-review.md` - Technical gaps identified
