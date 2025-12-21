# MVP vs Future Scope Guide

**Topic:** What to Build Now vs. What to Defer

**Reading Time:** 15 minutes

**Skill Level:** All levels

**Version:** 1.0 (2025-10-09)

---

## 🎯 What You'll Learn

After reading this guide, you'll understand:

- **What** 10 components are in MVP scope (must build)
- **What** 10 components are future scope (defer/document only)
- **Why** certain features are explicitly out of scope
- **When** deferred features should be revisited (v2.0, v3.0)
- **How** to prevent scope creep during implementation

---

## 📖 Reading Path (Follow This Order)

This guide curates content across **4 different files** to clearly separate MVP from future work.

---

### Part 1: The 100-Hour Constraint (2 minutes)

**Understanding the Budget**

📄 **File:** `distilled/constraints.md`

**Lines:** 8-25

**Read This Section:**
```
## Budget Constraints

Development Budget:
- MVP: 100 hours total (documented in PRD)
- No prior backend implementation exists
- Starting from scratch
- Source: PRD.md:194

Skill Level Constraint:
- Junior developer (limited backend experience)
- Docker fundamentals (demonstrated in POC)
- Python basics (FastAPI/Flask)
- Database basics (PostgreSQL, SQLite)
```

**Key Insight:** 100 hours is ~2.5 weeks of full-time work. Every feature choice must fit this constraint.

---

### Part 2: MVP Scope - What to Build (5 minutes)

**The 10 Must-Build Components**

📄 **File:** `component-map.md`

**Lines:** 9-86

**Read This Section (all 10 components):**

| # | Component | Technology | Why MVP | Hours Est. |
|---|-----------|-----------|---------|------------|
| MVP-1 | Database | SQLite | File-based, zero setup, SQLAlchemy compatible | ~10h |
| MVP-2 | API Framework | FastAPI | Async, OpenAPI auto-gen, type hints | ~15h |
| MVP-3 | Authentication | JWT | Stateless, REST-friendly, module-compatible | ~8h |
| MVP-4 | Container Platform | Docker | Local-first, consistent env, K8s migration path | ~5h |
| MVP-5 | API Design | REST (5 endpoints) | Simple CRUD, no GraphQL complexity | ~20h |
| MVP-6 | Scheduler | Python `schedule` | Hourly RSS fetch, no external cron | ~5h |
| MVP-7 | Health Checks | `/health` endpoint | Container probes, monitoring hook | ~3h |
| MVP-8 | Configuration | Environment variables | No hardcoded secrets, 12-factor app | ~4h |
| MVP-9 | API Documentation | FastAPI OpenAPI | Auto-generated `/docs` endpoint | ~2h |
| MVP-10 | Logging | Python `logging` | Stdout logs (Docker captures) | ~3h |

**Total MVP:** ~75 hours (25-hour buffer for testing/debugging)

**Key Insight:** These 10 components are the MINIMUM for a functional backend. Everything else is deferred.

---

**Detailed MVP Scope**

📄 **File:** `distilled/vision-statement.md`

**Lines:** 82-147

**Read This Section:**
```
## MVP Approach (What We Build First)

Goal: Working backend in 100 hours

Minimal Scope:
- 5 RSS feeds (hardcoded URLs for MVP)
- SQLite database (local file, no server)
- 5 REST API endpoints (CRUD operations)
- Docker containerization
- JWT authentication (basic)
- Health monitoring (simple /health endpoint)
```

**Key Insight:** MVP is deliberately minimal. RSS feeds are hardcoded. No admin UI. No complex features.

---

### Part 3: Future Scope - What to Defer (5 minutes)

**The 10 Must-NOT-Build Components**

📄 **File:** `component-map.md`

**Lines:** 89-162

**Read This Section (all 10 future components):**

| # | Component | Technology | Why Future | When |
|---|-----------|-----------|-----------|------|
| FUTURE-1 | Relational Database | PostgreSQL + pgvector | Production scale, multi-user | v3.0 (Production) |
| FUTURE-2 | Graph Database | Neo4j | Complex relationship queries | v3.0 (Production) |
| FUTURE-3 | Cache Layer | Redis | Performance optimization | v2.0 (When measured bottleneck) |
| FUTURE-4 | GraphQL API | GraphQL endpoint | Complex client queries | v2.0 (If needed) |
| FUTURE-5 | Message Queue | NATS/Kafka/RabbitMQ | Async processing, event-driven | v3.0 (Distributed) |
| FUTURE-6 | Kubernetes | K8s manifests | Production orchestration, auto-scaling | v3.0 (Production) |
| FUTURE-7 | Advanced Auth | Keycloak/Auth0 | OAuth2, SSO, RBAC | v2.0 (Multi-tenant) |
| FUTURE-8 | Distributed Tracing | Jaeger/Zipkin | Performance debugging | v3.0 (Production) |
| FUTURE-9 | Metrics & Monitoring | Prometheus/Grafana | Production observability | v3.0 (Production) |
| FUTURE-10 | CI/CD Pipeline | GitHub Actions | Automated testing/deployment | v2.0 (Post-MVP) |

**Key Insight:** Document future components (in spec or ADRs) but don't build them. They're validated ideas, not current work.

---

**Explicitly Out of Scope**

📄 **File:** `distilled/vision-statement.md`

**Lines:** 187-215

**Read This Section:**
```
## What's Explicitly OUT of Scope

The following are NOT in MVP:

Technology Scope:
- ❌ PostgreSQL + pgvector (use SQLite for MVP)
- ❌ Neo4j graph database (defer to future phase)
- ❌ Real AI integration (mock responses for MVP)
- ❌ Kubernetes deployment (Docker Compose sufficient)
- ❌ Enterprise auth (Keycloak) - simple JWT OK
- ❌ GraphQL endpoint (REST only for MVP)
- ❌ WebSocket real-time updates (defer to Phase 2)
- ❌ Redis caching (premature optimization)
- ❌ Message queues (NATS/Kafka) - sync processing for MVP
- ❌ Event-driven architecture (NATS/Kafka) - defer to Phase 2
- ❌ Distributed P2P capabilities (CRDT integration) - future vision
- ❌ Permission propagation layer - defer to Phase 2
- ❌ Production-scale optimizations
- ❌ Full abstraction scaffold architecture
```

**Why This Matters:** Multiple sources reference advanced capabilities (graph databases, complex auth, K8s). **These inform long-term direction but would prevent MVP completion.**

**Rule:** If it's in abstraction scaffold or spark chat, it's probably future vision. If it's in PRD.md with 100-hour constraint, it's MVP.

---

### Part 4: Technology Decisions by Status (3 minutes)

**FIRM, TENTATIVE, OPEN, REJECTED**

📄 **File:** `distilled/decisions-made.md`

**Lines:** 8-240

**FIRM Decisions (Build These - Lines 8-123):**

- SQLite, FastAPI, JWT, Docker, REST, Python `schedule`, Health checks, Environment vars, OpenAPI, Logging
- **Status:** ✅ FIRM - proceed with this

**TENTATIVE Decisions (Document, Don't Build - Lines 126-196):**

- PostgreSQL, Neo4j, Redis, Keycloak, Kubernetes
- **Status:** ⏳ TENTATIVE - validate during production planning
- **Action for MVP:** Document in spec/ADRs, don't implement

**OPEN Decisions (Needs Team Input - Lines 199-240):**

- GraphQL?, Message Queue?, CRDT?, Authorization model?, Vector DB scaling?
- **Status:** ❓ OPEN - needs discovery or team decision
- **Action for MVP:** Flag for discussion, defer to v2.0

**REJECTED Approaches (Never Build - Lines 243-335):**

- Django, Monolith, Hardcoded config, Sessions, Social login only, Flask, SQLAlchemy-only
- **Status:** ❌ REJECTED - don't reconsider
- **Action for MVP:** Avoid these patterns

**Key Insight:** FIRM = build. TENTATIVE = document. OPEN = flag. REJECTED = avoid.

---

## 🎯 Decision Framework: Is This In Scope?

Use this flowchart during implementation:

```
Feature request comes in
    ↓
Q1: Is it in the 10 MVP components? (component-map.md)
    ├─ YES → Build it
    └─ NO → Continue to Q2

Q2: Is it marked FIRM in decisions-made.md?
    ├─ YES → Build it
    └─ NO → Continue to Q3

Q3: Is it in "Out of Scope" section? (vision-statement.md lines 187-215)
    ├─ YES → Reject (defer to v2.0/v3.0)
    └─ NO → Continue to Q4

Q4: Can it be done in <5 hours AND is it critical for MVP?
    ├─ YES → Escalate to product owner for decision
    └─ NO → Reject (defer to v2.0)
```

**Rule of thumb:** When in doubt, defer to future version. MVP should be MINIMAL.

---

## 📅 Version Roadmap: When Deferred Items Return

📄 **File:** `VERSION.md`

**Lines:** 147-174

### Version 2.0 (Expected: After MVP Implementation, 2-4 weeks)
**Scope:** Post-MVP retrospective and refinements

**What Gets Added:**

- Answers to OPEN decisions (GraphQL?, Message queue?, CRDT?)
- Performance benchmarks from MVP testing
- Updated constraints based on real timeline/effort data
- Filled-in architecture diagram with real component relationships
- CI/CD pipeline (if needed for iteration speed)
- Redis caching (if MVP shows bottlenecks)

**What's Still Deferred:**

- Kubernetes (not needed until production scale)
- PostgreSQL (SQLite sufficient until multi-user)
- Neo4j (no complex graph queries yet)

---

### Version 3.0 (Expected: Production Architecture Phase)
**Scope:** Production-scale architecture discovery

**What Gets Added:**

- PostgreSQL + pgvector migration (multi-user, ACID compliance)
- Neo4j graph database integration (complex relationship queries)
- Redis caching strategy (measured performance optimization)
- Kubernetes deployment architecture (horizontal scaling)
- Prometheus/Grafana monitoring (production observability)
- Distributed architecture planning (Four-Plane Architecture)
- Advanced auth (Keycloak/OAuth2/RBAC)

**What Might Still Be Deferred:**

- Full P2P distributed sync (depends on product roadmap)
- Permission propagation layer (depends on multi-tenancy needs)
- Event-driven architecture (depends on scale requirements)

---

## 🚨 Scope Creep Warning Signs

Watch for these patterns during implementation:

### ❌ Red Flags (Scope Creep)
- "Let's just add PostgreSQL now since we'll need it eventually"
- "Redis is easy to set up, might as well do it"
- "We should build admin UI for managing RSS feeds"
- "Let's make the auth system production-ready with OAuth2"
- "We need GraphQL for flexible queries"

### ✅ Green Lights (On Track)
- "SQLite works for MVP, PostgreSQL documented for v3.0"
- "No caching yet, but we're logging query times to measure later"
- "RSS feeds are hardcoded in config, admin UI deferred to v2.0"
- "JWT tokens sufficient for MVP, Keycloak noted for production"
- "REST endpoints cover CRUD, GraphQL is an open question for v2.0"

**Rule:** If it's not in the 10 MVP components, it's scope creep unless explicitly approved by product owner.

---

## 💡 Common Questions

**Q: Why SQLite? It's not production-ready.**

A: MVP doesn't need production scale. SQLite validates the data model and API design. PostgreSQL migration is documented for v3.0 (when production scale is needed).

**Q: Why not build Kubernetes configs now?**

A: MVP runs locally in Docker. Kubernetes is for production deployment (v3.0). Docker Compose → Kubernetes migration is well-documented and low-risk.

**Q: What if we discover we need caching during MVP?**

A: Measure first. If response times exceed 200ms target, add to v2.0 scope. Don't pre-optimize.

**Q: Can I add a "nice-to-have" feature if it only takes 2 hours?**

A: No. The 25-hour buffer is for testing/debugging, not new features. Defer to v2.0 backlog.

**Q: What if the 10 MVP components take longer than 75 hours?**

A: Reduce scope within MVP components (e.g., 3 REST endpoints instead of 5). Don't add time.

---

## 🔗 Related Guides

- **Modular Architecture Guide** - How to design for future modularity in MVP
- **Technology Migration Guide** - Upgrade paths from MVP to production

---

## 📚 Full Reading List

If you followed this guide, you read:

1. `constraints.md` (lines 8-25)
2. `component-map.md` (lines 9-86, 89-162)
3. `vision-statement.md` (lines 82-147, 187-215)
4. `decisions-made.md` (lines 8-240)
5. `VERSION.md` (lines 147-174)

**Total:** ~200 lines across 5 files, curated into coherent 15-minute reading path.

---

**Last Updated:** 2025-10-09

**Bundle Version:** v1.0

**Guide Version:** 1.0
