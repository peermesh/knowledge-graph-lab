# Modular Architecture Guide

**Topic:** How to Design the Backend Modularly

**Reading Time:** 30 minutes

**Skill Level:** Intermediate to Advanced

**Version:** 1.0 (2025-10-09)

---

## 🎯 What You'll Learn

After reading this guide, you'll understand:

- **Why** the backend must be modular (not monolithic)
- **What** modules exist and how they interact
- **How** to design for modularity (6 key patterns)
- **When** to abstract vs. keep simple (pragmatic approach)
- **What** specific integration requirements each module needs

---

## 📖 Reading Path (Follow This Order)

This guide curates content across **5 different files** to tell a coherent story about modular architecture.

---

### Part 1: Why Modular? (5 minutes)

**Philosophy: Why Monolith Was Rejected**

📄 **File:** `distilled/decisions-made.md`

**Lines:** 278-295

**Read This Section:**
```
Rejected 3: Monolithic Application Architecture

Why Rejected:
- Violates "stateless services" design principle
- Harder to scale horizontally
- Poor separation of concerns for multi-module system
- Local-first containerization requires modular services
```

**Key Insight:** The backend is part of a multi-module system (AI, Frontend, Publishing). Modularity isn't a nice-to-have—it's required by the architecture.

---

**Supporting Decision: Why JWT Over Sessions**

📄 **File:** `distilled/decisions-made.md`

**Lines:** 303-309

**Read This Section:**
```
Rejected 4: Session-Based Authentication

Why Rejected:
- Stateful (requires DB/Redis for every request)
- Doesn't scale horizontally as well as JWT
- More complex for multi-module architecture
- JWT standard for microservices
```

**Key Insight:** Technology choices (like JWT) enable modular architecture by supporting stateless, inter-module communication.

---

### Part 2: What Modules Exist? (3 minutes)

**Module Inventory and Integration Requirements**

📄 **File:** `distilled/constraints.md`

**Lines:** 116-139

**Read This Section:**
```
## Integration Constraints

Module Dependencies:
- Must integrate with: AI Module, Frontend Module, Publishing Module
- Interface: REST APIs (primary), GraphQL (future consideration)

Communication Patterns:
- REST APIs for synchronous module communication
- Event-driven architecture for async processing (future)

Data Exchange:
- Must provide entity/relationship data to AI module
- Must supply processed content to Publishing module
- Must serve query results to Frontend module
```

**Key Insight:** Backend is infrastructure for 3 other modules. Design APIs with their needs in mind, not as standalone service.

---

### Part 3: How to Design Modularly? (15 minutes)

**Six Key Architectural Patterns**

📄 **File:** `distilled/vision-statement.md`

**Lines:** 218-350

This is the most important section. Read ALL six subsections in order:

---

#### Pattern 1: Four-Plane Architecture (Lines 222-241)

**Future Vision:**
```
1. Interface Plane: REST + GraphQL dual facade
2. Event Plane: NATS JetStream for async workflows
3. Data Plane: Pluggable storage drivers (Neo4j/Jena, Qdrant/Weaviate)
4. Policy Plane: Permission tags that travel with data
```

**MVP Implication for You:**

- Design REST APIs with future GraphQL compatibility (clear resource boundaries)
- Use stateless JWT tokens (compatible with event-driven systems)
- Keep data access logic separate from business logic (enables pluggable drivers later)
- Document permission requirements even if enforcement is simple

**Why This Matters:** Planes are NOT services. They're architectural layers that cut across services. This prevents tight coupling.

---

#### Pattern 2: Distributed P2P & Local-First Vision (Lines 242-259)

**Future Vision:**
```
- System supports fully distributed operation (Bluetooth mesh, offline-first, P2P sync)
- Private data stays local, connects to centralized services only when needed
- End-to-end encryption for external connections
- CRDT integration for eventual consistency (Yjs/Automerge/AntidoteDB)
```

**MVP Implication for You:**

- Local-first Docker deployment validates this pattern (everything runs on developer machine)
- Design data models with sync in mind (timestamps, version tracking)
- Keep services modular (easier to distribute later)

**Why This Matters:** Local-first MVP is NOT just convenience—it's validating the future distributed architecture.

---

#### Pattern 3: Permission Propagation Architecture (Lines 260-277)

**Future Vision:**
```
- All incoming data tagged with PermissionTag (similar to AWS ACL)
- Permissions flow through pipeline: raw data → chunks → vectors → graph
- Query-time enforcement at access point
- Revocation cascades through derived artifacts
```

**MVP Implication for You:**

- Design database schema with user/ownership columns from start
- Implement basic auth/authorization (JWT + user context)
- Document which endpoints need permission checks (even if simple for MVP)
- Avoid hardcoded global access patterns

**Why This Matters:** Retrofitting permissions is expensive. Add hooks now even if logic is simple.

---

#### Pattern 4: Graph-as-Module Design Pattern (Lines 278-295)

**Future Vision:**
```
- Knowledge graph is THE central module (not a service among many)
- Other services orbit the graph rather than owning isolated data
- Eliminates tight coupling between publishing/AI/frontend modules
- Multiple interlinked graphs (personal/team/public/derived)
```

**MVP Implication for You:**

- Design database schema with graph-compatible relationships (even in SQLite)
- Use foreign keys and join tables (easier migration to Neo4j later)
- Keep business logic separate from storage details
- Document entity relationships explicitly

**Why This Matters:** Backend isn't just "API for data storage"—it's graph data infrastructure. Design schema accordingly.

---

#### Pattern 5: Event-Driven Integration Pattern (Lines 296-313)

**Future Vision:**
```
- NATS JetStream or Kafka for intra-cluster async messaging
- libp2p/GossipSub for peer-to-peer event distribution
- SWIM/Serf for membership gossip in distributed deployments
- Modules added/removed via subscription changes (no code coupling)
```

**MVP Implication for You:**

- Keep API endpoints stateless (easier to add event publishing later)
- Use clear resource actions (POST/PUT/DELETE map cleanly to events)
- Document "what happened" semantics for each endpoint
- Consider simple database-table queue as stepping stone to message broker

**Why This Matters:** Event-driven architecture decouples modules. Design REST APIs with future event semantics in mind.

---

#### Pattern 6: Pluggable Storage Driver Pattern (Lines 314-332)

**Future Vision:**
```
- Swap storage implementation without changing module code
- Graph: Neo4j vs Apache Jena vs AWS Neptune
- Vector: Qdrant vs Weaviate vs Milvus vs pgvector
- Object: S3 vs MinIO vs IPFS
```

**MVP Implication for You:**

- Use abstraction layer for database access (SQLAlchemy ORM, repository pattern)
- Keep queries simple and standard (avoid database-specific features)
- Test with SQLite but design for PostgreSQL compatibility
- Document data access patterns explicitly

**Why This Matters:** Technology landscape changes fast. Design for swappability from day one.

---

### Part 4: When to Abstract? (5 minutes)

**Trade-Offs: Pragmatic Abstraction vs. Over-Engineering**

📄 **File:** `distilled/technical-context.md`

**Lines:** 274-318

**Read This Section:**
```
Trade-off 1: Simplicity vs Future-Proofing

Arguments for Simplicity:
- Get to working system faster (100-hour constraint)
- Validate assumptions before investing in complexity
- Junior developer can complete

Arguments for Future-Proofing:
- Avoid costly migrations later
- Design decisions matter (schema compatibility)
- Some complexity is unavoidable (will need PostgreSQL eventually)

Resolution:
✅ Simplicity for MVP, with migration path designed
- Use SQLite now
- Design schema compatible with PostgreSQL
- Plan migration strategy (documented, not implemented)
- Accept that some refactoring will be needed
```

**Key Insight:** Don't build the future architecture now, but design MVP with future compatibility.

---

📄 **File:** `distilled/technical-context.md`

**Lines:** 319-339

**Read This Section:**
```
Trade-off 2: Flexibility vs Complexity

Do we design abstract interfaces (swappable components) or hard-code current choices?

Resolution:
✅ Pragmatic abstraction (repository pattern, ORM)
- Use SQLAlchemy ORM (enables database swaps)
- Keep business logic separate from storage details
- Don't abstract too early (YAGNI principle applies)
```

**Key Insight:** Use proven abstraction patterns (ORM, repository) but don't create custom frameworks.

---

### Part 5: Module Integration Specifications (5 minutes)

**Concrete Requirements for Each Module**

📄 **File:** `distilled/requirements-notes.md`

**Lines:** 85-155

**Read These Three Sections:**

---

**UI-1: Integration with AI Module (Lines 85-113)**
```
Backend must expose APIs that:
- Provide content for AI processing
- Accept AI-generated entity extractions
- Support bidirectional data flow

Specific APIs:
- GET /api/content/{id} - Fetch content for AI processing
- POST /api/entities - AI submits extracted entities
- GET /api/entities - AI queries existing entities
```

---

**UI-2: Integration with Frontend Module (Lines 114-136)**
```
Backend must provide:
- Dashboard API (GET /api/dashboard) - Aggregated data for user interface
- Entity query API (GET /api/entities?filter=...) - Search and filter
- Source management (POST /api/sources, GET /api/sources/{id})
```

---

**UI-3: Integration with Publishing Module (Lines 137-155)**
```
Backend must support:
- Content retrieval for digest generation (GET /api/content?published=false)
- Filtering by user preferences
- Batch operations for multi-item processing
```

**Key Insight:** Each module has specific API needs. Design endpoints with these use cases in mind.

---

## 🎯 Summary: Modular Design Principles for MVP

After reading all sections above, here are the actionable principles:

### 1. **Stateless Services**
- Use JWT (not sessions) for authentication
- Avoid server-side state
- Enable horizontal scaling from day one

### 2. **Clear Module Boundaries**
- Backend integrates with: AI Module, Frontend Module, Publishing Module
- Communication via REST APIs (GraphQL future)
- Document integration points explicitly

### 3. **Abstraction Layers**
- Use SQLAlchemy ORM (database swappable)
- Repository pattern for data access
- Keep business logic separate from storage

### 4. **Graph-Friendly Schema**
- Use foreign keys and join tables
- Document entity relationships
- Design for eventual Neo4j migration

### 5. **Permission Hooks**
- Add user/ownership columns now
- Document permission requirements
- Plan for future propagation

### 6. **Event Semantics**
- Design API endpoints with "what happened" clarity
- POST/PUT/DELETE should map to future events
- Keep endpoints stateless

### 7. **Migration Paths**
- SQLite → PostgreSQL (schema compatible)
- Docker Compose → Kubernetes (containerized from day one)
- REST → REST + GraphQL (clear resource boundaries)

### 8. **YAGNI Principle**
- Don't build future architecture now
- Do design for compatibility
- Use proven patterns (ORM, not custom frameworks)

---

## ❓ Common Questions

**Q: Should I build microservices for MVP?**

A: No. Build modular components within a single service. The modularity is in code organization and API design, not deployment architecture.

**Q: Should I use Neo4j for MVP?**

A: No. Use SQLite with graph-friendly schema (foreign keys, join tables). Migrate to Neo4j when graph queries become bottleneck.

**Q: Should I implement event-driven architecture?**

A: Not yet. Design REST endpoints with future event semantics in mind. Use synchronous processing for MVP.

**Q: How much abstraction is too much?**

A: Use standard patterns (ORM, repository). Don't create custom abstraction frameworks. If it's in SQLAlchemy or FastAPI, use it. If you have to build it yourself, defer it.

**Q: What if I find the patterns too complex?**

A: Focus on Part 5 (concrete requirements). Build what's specified, use SQLAlchemy ORM, document entity relationships. The patterns inform design but don't dictate implementation.

---

## 🔗 Related Guides

- **MVP vs Future Scope Guide** - What to build now vs. later
- **Technology Migration Guide** - Upgrade paths (SQLite→PostgreSQL, Docker→K8s)

---

## 📚 Full Reading List

If you followed this guide, you read:

1. `decisions-made.md` (lines 278-317)
2. `constraints.md` (lines 116-139)
3. `vision-statement.md` (lines 218-350)
4. `technical-context.md` (lines 274-339)
5. `requirements-notes.md` (lines 85-155)

**Total:** ~150 lines across 5 files, curated into coherent 30-minute reading path.

---

**Last Updated:** 2025-10-09

**Bundle Version:** v1.0

**Guide Version:** 1.0
