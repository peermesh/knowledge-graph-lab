# Backend Module - Vision Statement

**Date:** 2025-10-09
**Distilled from:** vision.md, Backend-Architecture-Spec.md, PRD.md

---

## Problem Statement

The creator economy suffers from fragmented information. Creators waste 10+ hours weekly searching for grants, partnerships, and opportunities across hundreds of disconnected sources. The system is failing them—not because they lack research skills, but because no intelligent layer exists to filter signal from noise.

**Why This Matters for Backend:**
Without reliable infrastructure to **continuously collect, store, and serve** this scattered information, the vision of an intelligent research system remains theoretical. The backend module is the foundation that makes everything else possible.

**Sources:**
- vision.md: Creator time waste statistics (line 23-29)
- vision.md: "Automatically scans hundreds of sources" (line 37-38)
- Backend-Architecture-Spec.md: "Foundational systems that support all other modules" (line 5)

---

## Target Users

### Primary: Other System Modules
The backend serves **internal consumers**:
- **AI Module**: Needs content to process, databases to query, queues for async work
- **Frontend Module**: Needs REST APIs, WebSockets for real-time updates, authentication
- **Publishing Module**: Needs user preferences, content retrieval APIs

**Note:** Backend does NOT serve end users directly. It's infrastructure.

### Secondary: Development Team
Backend provides:
- Local development environment (Docker Compose)
- Clear API contracts (OpenAPI docs)
- Health monitoring endpoints

**Sources:**
- Backend-Architecture-Spec.md: "Interfaces with Other Modules" (lines 72-100)
- PRD.md: Dependencies section (lines 132-136)

---

## Solution Approach

### MVP: Standalone Module Foundation (100 hours)
Build the **minimum viable backend** that enables other modules to function:

**What it does:**
1. **Fetches content**: Monitors 5 RSS feeds hourly
2. **Stores data**: SQLite database with structured schema (sources, content, entities)
3. **Serves APIs**: 5 REST endpoints for source management, content retrieval, dashboard stats
4. **Runs isolated**: Docker container, no external dependencies
5. **Mocks integration**: Returns placeholder data for AI module (real integration later)

**Why this approach:**
- **Simplicity**: SQLite, not PostgreSQL—get it working first
- **Independence**: Junior developer can build standalone module
- **Validation**: Proves infrastructure patterns before scaling
- **Speed**: 100 hours to working system vs months for "perfect" solution

**Sources:**
- PRD.md: Executive Summary (lines 7-8)
- PRD.md: Goals (lines 10-15)
- PRD.md: Technical Stack (lines 34-39)

### Future: Production-Scale Infrastructure
After MVP proves patterns:
- **PostgreSQL + pgvector**: For production structured data + embeddings
- **Neo4j**: For graph relationships (creator-to-grant connections)
- **Kubernetes**: For production deployment
- **Real auth**: Keycloak or Auth0 vs simple JWT
- **Complex integration**: Multi-module orchestration

**Critical:** These are OUT OF MVP SCOPE. Document them, don't build them yet.

**Sources:**
- Backend-Architecture-Spec.md: PostgreSQL/Neo4j mentioned (lines 10-11)
- Backend-Architecture-Spec.md: Kubernetes configs (line 46)
- intake.md: Scope Boundaries (lines 340-365)

---

## Key Success Metrics

### For MVP (Minimum Viable Product)
**Functional Success:**
- ✅ Fetches from 5 RSS feeds successfully
- ✅ Stores 100+ content items without errors
- ✅ All 5 API endpoints return valid data
- ✅ Runs with single `docker run` command
- ✅ No crashes for 1-hour continuous operation

**Integration Success:**
- ✅ AI module can retrieve content via API
- ✅ Frontend can display data from APIs
- ✅ Publishing module can query for digest content

**Time Success:**
- ✅ Completes in 100 hours (junior developer effort)
- ✅ Weeks 1-6: Core features working
- ✅ Weeks 7-10: Enhancements complete
- ✅ Weeks 11-12: Demo ready

**Sources:**
- PRD.md: Success Criteria (lines 125-130)
- PRD.md: Implementation Plan (lines 89-124)

### For Production Vision (Future)
**System-level metrics** (beyond MVP, for context):
- Process 10,000+ sources daily
- Sub-2 second API response times
- 99.9% uptime
- 95% relevance rate for recommendations

**Note:** These inform architecture decisions (design for scale) but aren't MVP requirements.

**Sources:**
- vision.md: Success Criteria - For the System (lines 112-117)

---

## Strategic Rationale

### Why Build Backend Module Now

**1. Other Modules Depend On It**
- AI module needs content to process → Backend provides RSS ingestion
- Frontend needs data to display → Backend provides REST APIs
- Publishing needs user preferences → Backend provides storage

**Without backend, nothing else can function.** It's the foundation.

**2. Validates Core Infrastructure Patterns**
MVP proves:
- Docker deployment works
- API contracts are clear
- Database schema supports use cases
- Integration patterns are viable

**Better to discover issues now** (100 hours, small scope) than after building complex multi-module system.

**3. Junior Developer Can Build It**
- Well-defined scope (5 feeds, 5 APIs, 100 hours)
- Simple tech stack (FastAPI, SQLite, Docker)
- Clear success criteria
- No ambiguous requirements

**This makes it a good starting point** for team learning and momentum.

**Sources:**
- Backend-Architecture-Spec.md: Module Boundaries (lines 61-71)
- PRD.md: Risks & Mitigations (lines 137-143)
- intake.md: Scope Boundaries - MVP (lines 342-350)

### Why MVP Approach vs Full Vision Immediately

**The Problem with Building Everything:**
- Abstraction scaffold (future vision) requires years, not months
- Complex multi-module orchestration has too many unknowns
- Junior developers would be overwhelmed
- High risk of never finishing anything

**The MVP Approach:**
- **Deliverable in 12 weeks** vs "someday"
- **Proves value incrementally**: Working system = team momentum
- **Learns from reality**: Real data informs next phase
- **Defers complexity**: Solve known problems first

**Critical Insight from PR Review:**
Intern attempted "impressive" work (over-commented Docker files) instead of completing deliverables. **MVP approach forces focus on "working" over "perfect".**

**Sources:**
- fall-2025-backend-architecture-phase-1-review.md: Minimal effort vs comprehensive research (lines 13-15)
- intake.md: Notes - Key Insight #2 (lines 372-373)

---

## Scope Boundaries (CRITICAL)

### IN SCOPE for Backend MVP:
- ✅ Python/FastAPI backend
- ✅ SQLite database
- ✅ 5 RSS feeds (hardcoded URLs OK for MVP)
- ✅ 5 REST API endpoints
- ✅ Docker container (local development)
- ✅ Mock AI responses
- ✅ Basic error handling + logging
- ✅ 100 hours total effort

### EXPLICITLY OUT OF MVP SCOPE:
- ❌ PostgreSQL + pgvector (use SQLite for MVP)
- ❌ Neo4j graph database (defer to future phase)
- ❌ Real AI integration (mock responses for MVP)
- ❌ Kubernetes deployment (Docker Compose sufficient)
- ❌ Enterprise auth (Keycloak) - simple JWT OK
- ❌ GraphQL endpoint (REST only for MVP)
- ❌ WebSocket real-time updates (defer to Phase 2)
- ❌ Multi-module orchestration complexity
- ❌ Event-driven architecture (NATS/Kafka) - defer to Phase 2
- ❌ Distributed P2P capabilities (CRDT integration) - future vision
- ❌ Permission propagation layer - defer to Phase 2
- ❌ Production-scale optimizations
- ❌ Full abstraction scaffold architecture

**Why This Matters:**
Multiple sources reference advanced capabilities (graph databases, complex auth, K8s). **These inform long-term direction but would prevent MVP completion.**

**Rule:** If it's in abstraction scaffold or spark chat, it's probably future vision. If it's in PRD.md with 100-hour constraint, it's MVP.

**Sources:**
- PRD.md: "Keep it simple - this is an MVP" (line 194)
- intake.md: Scope Boundaries (lines 340-365)
- Abstraction scaffold (external reference - future vision)

---

## Future Architectural Vision (Context for MVP Decisions)

**Purpose of This Section:** Explain WHY certain MVP design choices matter for long-term compatibility, even though advanced features are out of MVP scope.

### Four-Plane Architecture Model

**Future Vision:**
The system will be organized around four complementary planes (not traditional service boundaries):

1. **Interface Plane**: REST + GraphQL dual facade for client/module communication
2. **Event Plane**: NATS JetStream (or Kafka) for async event-driven workflows
3. **Data Plane**: Pluggable storage drivers (Neo4j/Jena for graph, Qdrant/Weaviate for vector, MinIO for objects)
4. **Policy Plane**: Permission tags that travel with data through transformations

**MVP Implication:**
- Design REST APIs with future GraphQL compatibility in mind (clear resource boundaries)
- Use stateless JWT tokens (compatible with event-driven systems)
- Keep data access logic separate from business logic (enables pluggable drivers later)
- Document permission requirements even if enforcement is simple for MVP

**Sources:**
- canonical-synth-from-chat+build-out-plans/canonical synth-chatGPT-1of3.md:88-95
- SPARK-DISTILLATION-EVALUATION.md: Four-Plane Architecture insight

### Distributed P2P & Local-First Vision

**Future Vision:**
- System must support fully distributed operation (Bluetooth mesh, offline-first, P2P sync)
- Private data stays local, connects to centralized services only when needed
- End-to-end encryption for external connections
- CRDT integration for eventual consistency (requires external library: Yjs/Automerge/AntidoteDB)

**MVP Implication:**
- Local-first Docker deployment validates this pattern (everything runs on developer machine)
- Design data models with sync in mind (timestamps, version tracking)
- Keep services modular (easier to distribute later)
- Note: AWS lacks managed CRDT service—will need integration work in future

**Sources:**
- spark-chat.md:349, 372-374, 406-410, 429-431
- canonical-synth-from-chat/canonical synth-chatGPT-0-analysis.md:92-98

### Permission Propagation Architecture

**Future Vision:**
- All incoming data tagged with PermissionTag (similar to AWS ACL but custom)
- Permissions flow through entire pipeline: raw data → chunks → vectors → graph
- Query-time enforcement at access point (knowledge graph queries, vector search)
- Revocation cascades through derived artifacts

**MVP Implication:**
- Design database schema with user/ownership columns from start
- Implement basic auth/authorization (JWT + user context)
- Document which endpoints need permission checks (even if simple for MVP)
- Avoid hardcoded global access patterns

**Sources:**
- spark-chat.md:356-359, 376-379, 494-502
- canonical-synth-from-chat+build-out-plans/canonical synth-chatGPT-1of3.md:362-365

### Graph-as-Module Design Pattern

**Future Vision:**
- Knowledge graph is THE central module (not a service among many)
- Other services orbit the graph rather than owning isolated data
- Eliminates tight coupling between publishing/AI/frontend modules
- Multiple interlinked graphs (personal/team/public/derived) with dynamic weight rebalancing

**MVP Implication:**
- Design database schema with graph-compatible relationships (even in SQLite)
- Use foreign keys and join tables (easier migration to Neo4j later)
- Keep business logic separate from storage details
- Document entity relationships explicitly

**Sources:**
- canonical-synth-from-chat/canonical synth-chatGPT-1of3.md:108-109, 375-379
- abstraction-scaffold: Graph-as-Module design principle

### Event-Driven Integration Pattern

**Future Vision:**
- NATS JetStream or Kafka for intra-cluster async messaging
- libp2p/GossipSub for peer-to-peer event distribution
- SWIM/Serf for membership gossip in distributed deployments
- Modules added/removed via subscription changes (no code coupling)

**MVP Implication:**
- Keep API endpoints stateless (easier to add event publishing later)
- Use clear resource actions (POST/PUT/DELETE map cleanly to events)
- Document "what happened" semantics for each endpoint
- Consider simple database-table queue as stepping stone to message broker

**Sources:**
- canonical-synth-from-chat+build-out-plans/canonical synth-chatGPT-1of3.md:217-219
- abstraction-scaffold: Event-Driven Pipeline principle

### Pluggable Storage Driver Pattern

**Future Vision:**
- Swap storage implementation without changing module code
- Graph: Neo4j vs Apache Jena vs AWS Neptune
- Vector: Qdrant vs Weaviate vs Milvus vs pgvector
- Object: S3 vs MinIO vs IPFS
- Time-series: Timestream vs InfluxDB

**MVP Implication:**
- Use abstraction layer for database access (SQLAlchemy ORM, repository pattern)
- Keep queries simple and standard (avoid database-specific features)
- Test with SQLite but design for PostgreSQL compatibility
- Document data access patterns explicitly

**Sources:**
- canonical-synth-from-chat/canonical synth-chatGPT-1of3.md:349-355
- abstraction-scaffold: Parallel Backend Abstraction principle

### Quantitative Performance Targets (Future)

**Future Vision (From Abstraction Scaffold):**
- p95 search latency ≤350ms @ 100K chunks
- Policy check overhead ≤15ms p95
- Ingestion throughput ≥50 docs/min (10 chunks each)
- Offline replay: backlog within 10min after 30min outage

**MVP Implication:**
- Design with performance in mind (indexes, connection pooling)
- Document slow operations for future optimization
- Keep MVP simple enough to measure baseline performance
- Note: MVP won't hit these targets, but should be measurable

**Sources:**
- canonical-synth-from-chat+build-out-plans/canonical synth-chatGPT-1of3.md:91-94
- success-metrics.md:15-18

---

## Open Questions / Gaps Identified

**From PR Review - Still Needs Design:**
1. **Integration architecture**: How does Backend actually connect to AI/Frontend/Publishing? (No diagram exists yet)
2. **Database schema specifics**: PRD has basic schema, but no ERD, no migration strategy, no indexing plan
3. **Performance requirements**: No benchmarks, no load testing plan
4. **Security implementation**: JWT mentioned but no implementation details

**These become inputs for discovery phase** (identifying components, researching approaches).

**Sources:**
- fall-2025-backend-architecture-phase-1-review.md: Critical Gaps (lines 59-74)

---

## Sources Consulted

**Vision & Strategy:**
1. `docs/design/strategy/vision.md` - Overall product vision, creator economy problem
2. `docs/design/strategy/success-metrics.md` - System-level success metrics

**Backend Specification:**
3. `docs/modules/backend-architecture/Backend-Architecture-Spec.md` - Module responsibilities, interfaces
4. `docs/modules/backend-architecture/PRD.md` - MVP goals, technical requirements, implementation plan

**Context & Constraints:**
5. `.dev/team/intern-management/pr-reviews/fall-2025-backend-architecture-phase-1-review.md` - Gaps analysis
6. `00-context-intake/intake.md` - Source catalog with scope boundaries

**External References (Context Only):**
7. Abstraction scaffold - Future vision architecture patterns
8. Spark chat (spark-chat.md lines 300-555) - Distributed architecture discussions
9. Spark distillations (canonical-synth-from-chat+build-out-plans) - Four-Plane Architecture, implementation phases
10. `SPARK-DISTILLATION-EVALUATION.md` - Analysis of distillation variants
