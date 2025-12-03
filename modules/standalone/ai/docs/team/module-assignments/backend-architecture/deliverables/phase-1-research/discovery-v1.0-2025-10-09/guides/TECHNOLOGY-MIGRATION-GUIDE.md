# Technology Migration Guide

**Topic:** Upgrade Paths from MVP to Production
**Reading Time:** 20 minutes
**Skill Level:** Intermediate to Advanced
**Version:** 1.0 (2025-10-09)

---

## 🎯 What You'll Learn

After reading this guide, you'll understand:
- **What** technology migrations are planned (SQLite→PostgreSQL, Docker→K8s, etc.)
- **When** each migration should happen (v2.0, v3.0, production)
- **Why** MVP choices were made with migration in mind
- **How** to design MVP for smooth migration paths
- **What** compatibility considerations matter now

---

## 📖 Reading Path (Follow This Order)

This guide curates content across **4 different files** to explain upgrade paths.

---

## 🗺️ Migration Roadmap Overview

**MVP (v1.0)** → **Post-MVP (v2.0)** → **Production (v3.0)**

| Technology Category | MVP (Now) | v2.0 (2-4 weeks) | v3.0 (Production) |
|---------------------|-----------|------------------|-------------------|
| **Database** | SQLite | SQLite | PostgreSQL + pgvector |
| **Graph Storage** | SQLite (FK/join) | SQLite | Neo4j |
| **Cache** | None | Redis (if needed) | Redis |
| **Auth** | JWT (basic) | JWT | Keycloak/OAuth2 |
| **API** | REST | REST | REST + GraphQL |
| **Deployment** | Docker Compose | Docker Compose | Kubernetes |
| **Monitoring** | Logging | Logging | Prometheus/Grafana |
| **Message Queue** | Sync processing | Sync/DB queue | NATS/Kafka |
| **CI/CD** | Manual | GitHub Actions | GitHub Actions |

---

## Migration 1: Database (SQLite → PostgreSQL)

### Current State (MVP)

📄 **File:** `distilled/decisions-made.md`
**Lines:** 11-21

**Read This Section:**
```
Decision 1: SQLite with SQLAlchemy ORM

What: Use SQLite with SQLAlchemy ORM for MVP development
Why:
- No separate database server required (local-first principle)
- Zero configuration for developer onboarding
- Sufficient for MVP scope (5 feeds, limited data volume)
- Clear migration path to PostgreSQL for production
```

**Key Insight:** SQLite is deliberately chosen for MVP, but PostgreSQL is already planned.

---

### Future State (Production)

📄 **File:** `distilled/decisions-made.md`
**Lines:** 131-143

**Read This Section:**
```
Decision 11: PostgreSQL with pgvector (Production)

What: Migrate from SQLite to PostgreSQL with pgvector extension for production
Why:
- ACID compliance for multi-user production
- pgvector extension for AI embedding storage
- Proven scalability for relational data
- Supports JSON columns for flexible schemas
- Compatible with SQLAlchemy (same ORM code)

When: Production deployment (Phase 2+)
Timeline: After MVP validates data model
```

**Key Insight:** Same ORM (SQLAlchemy), different engine. Migration path is well-documented.

---

### Migration Considerations (Design for Compatibility NOW)

📄 **File:** `distilled/technical-context.md`
**Lines:** 274-296

**Read This Section:**
```
Trade-off 1: Simplicity vs Future-Proofing

Resolution:
✅ Simplicity for MVP, with migration path designed
- Use SQLite now
- Design schema compatible with PostgreSQL
- Plan migration strategy (documented, not implemented)
- Accept that some refactoring will be needed
```

**What to Do in MVP:**
1. **Use SQLAlchemy ORM** (not raw SQL) - makes engine swap trivial
2. **Avoid SQLite-specific features** (like `datetime('now', 'localtime')`)
3. **Use standard SQL types** (INTEGER, TEXT, REAL, BLOB)
4. **Test with PostgreSQL-compatible constraints** (foreign keys, unique constraints)
5. **Document schema migrations** using Alembic from day one

**Migration Process (v3.0):**
1. Export SQLite data to CSV/JSON
2. Create PostgreSQL database with same schema (via Alembic)
3. Import data using PostgreSQL COPY
4. Change SQLAlchemy connection string
5. Test all queries (should work unchanged if ORM used correctly)

**Estimated Effort:** 8-16 hours (mostly testing)

---

## Migration 2: Graph Storage (SQLite → Neo4j)

### Current State (MVP)

📄 **File:** `distilled/vision-statement.md`
**Lines:** 278-295

**Read This Section:**
```
Graph-as-Module Design Pattern

MVP Implication:
- Design database schema with graph-compatible relationships (even in SQLite)
- Use foreign keys and join tables (easier migration to Neo4j later)
- Keep business logic separate from storage details
- Document entity relationships explicitly
```

**Key Insight:** Use relational database NOW, but design schema as if it were a graph.

---

### Future State (Production)

📄 **File:** `distilled/decisions-made.md`
**Lines:** 145-159

**Read This Section:**
```
Decision 12: Neo4j for Graph Relationships (Future)

What: Add Neo4j as dedicated graph database for complex relationship queries
Why:
- Native graph traversal (multi-hop relationships)
- Pattern matching (Cypher queries)
- Relationship-first data model
- Better performance for "find all connected entities" queries

When: Production phase (when graph queries are proven bottleneck)
Timeline: After MVP validates graph use cases
```

**What to Do in MVP:**
1. **Design entity relationships explicitly** (creator → opportunity, source → feed)
2. **Use many-to-many tables** for relationships (not JSON arrays)
3. **Document graph patterns** in comments (e.g., "this will be Neo4j relationship")
4. **Keep queries simple** (no complex joins yet)
5. **Log slow queries** (>100ms) to identify future graph migration candidates

**Migration Process (v3.0):**
1. Analyze which queries are slow (multi-hop traversals)
2. Migrate those entities/relationships to Neo4j
3. Keep transactional data in PostgreSQL
4. Use PostgreSQL for writes, Neo4j for graph reads (dual-write pattern)
5. Sync data via change data capture (CDC) or event stream

**Estimated Effort:** 40-80 hours (schema design + sync logic)

---

## Migration 3: Deployment (Docker Compose → Kubernetes)

### Current State (MVP)

📄 **File:** `distilled/decisions-made.md`
**Lines:** 48-58

**Read This Section:**
```
Decision 4: Docker with Docker Compose

What: Use Docker containers orchestrated by Docker Compose for MVP
Why:
- Local-first requirement mandates containerization
- Consistent development environment across team
- Easy multi-service orchestration (db, cache, api)
- Clear migration path to Kubernetes for production
```

**Key Insight:** Docker Compose is for local dev. Kubernetes is for production. Both use same Docker images.

---

### Future State (Production)

📄 **File:** `distilled/decisions-made.md`
**Lines:** 185-197

**Read This Section:**
```
Decision 15: Kubernetes for Production Deployment (Future)

What: Migrate from Docker Compose to Kubernetes for production orchestration
Why:
- Horizontal scaling and load balancing
- Self-healing and rolling updates
- Service discovery and configuration management
- Cloud-native ecosystem standard
- Production monitoring integration (Prometheus/Grafana)

When: Production deployment phase (after MVP validation)
```

**What to Do in MVP:**
1. **Use environment variables** (not hardcoded config) - K8s ConfigMaps compatible
2. **Implement health checks** (/health endpoint) - K8s liveness/readiness probes use these
3. **Log to stdout** (not files) - K8s captures stdout automatically
4. **Single process per container** - K8s manages processes, not supervisord
5. **Stateless services** - K8s scales stateless pods easily

**Migration Process (v3.0):**
1. Convert docker-compose.yml to Kubernetes manifests (use kompose or manual)
2. Create Deployment, Service, ConfigMap, Secret resources
3. Configure HorizontalPodAutoscaler for auto-scaling
4. Set up Ingress for external access
5. Configure persistent volumes for SQLite → PostgreSQL migration

**Estimated Effort:** 16-24 hours (K8s learning curve + configuration)

---

## Migration 4: Caching (None → Redis)

### Current State (MVP)

📄 **File:** `distilled/vision-statement.md`
**Lines:** 198-199

**Read This Section:**
```
Out of Scope:
- ❌ Redis caching (premature optimization)
```

**Key Insight:** No caching in MVP. Measure performance first, optimize later.

---

### Future State (When Needed)

📄 **File:** `distilled/decisions-made.md`
**Lines:** 161-171

**Read This Section:**
```
Decision 13: Redis for Caching (When Needed)

What: Add Redis for caching frequently accessed data
Why:
- Fast in-memory lookups (<1ms)
- Reduces database load
- Simple key-value API
- Widely adopted standard

When: When performance measurements show bottleneck
Timeline: Add when P95 response time exceeds 200ms target
```

**What to Do in MVP:**
1. **Log all query times** (use middleware to measure endpoint latency)
2. **Identify hot paths** (which endpoints are called most frequently?)
3. **Design cache-friendly APIs** (GET endpoints should be idempotent)
4. **Avoid premature caching** (don't add Redis until measured need)

**Migration Process (v2.0 or v3.0):**
1. Analyze logs to find slow endpoints (P95 >200ms)
2. Add Redis container to docker-compose.yml
3. Implement cache-aside pattern (check cache, fallback to DB)
4. Set TTLs based on data freshness requirements (e.g., 5 min for dashboard, 1 hour for entities)
5. Monitor cache hit rate (aim for >80%)

**Estimated Effort:** 8-12 hours (Redis setup + cache logic)

---

## Migration 5: Authentication (JWT Basic → Keycloak/OAuth2)

### Current State (MVP)

📄 **File:** `distilled/decisions-made.md`
**Lines:** 33-44

**Read This Section:**
```
Decision 3: JWT Token-Based Authentication

What: Implement JWT (JSON Web Tokens) for authentication
Why:
- Stateless authentication (supports horizontal scaling)
- Standard for REST APIs and microservices
- Works across module boundaries
- 15-minute access tokens + 7-day refresh tokens recommended
```

**Key Insight:** Simple JWT for MVP (email/password or mock). Advanced auth deferred.

---

### Future State (Production)

📄 **File:** `distilled/decisions-made.md`
**Lines:** 173-183

**Read This Section:**
```
Decision 14: Keycloak for Advanced Authentication (Future)

What: Migrate to Keycloak for production authentication/authorization
Why:
- OAuth2/OIDC standard support
- SSO (Single Sign-On) across modules
- Social login integrations (Google, GitHub)
- RBAC (Role-Based Access Control)
- User management UI

When: Production deployment (multi-tenant requirements)
```

**What to Do in MVP:**
1. **Use standard JWT claims** (sub, iat, exp, aud) - Keycloak compatible
2. **Implement token refresh** (short-lived access tokens) - OAuth2 pattern
3. **Add user context to requests** (user ID in JWT payload)
4. **Design APIs with auth in mind** (which endpoints need auth?)

**Migration Process (v2.0 or v3.0):**
1. Deploy Keycloak instance
2. Configure realm and clients (backend, frontend, AI module)
3. Migrate users from SQLite to Keycloak
4. Change JWT issuer from backend to Keycloak
5. Backend verifies Keycloak-issued tokens (no code change if claims are standard)

**Estimated Effort:** 16-24 hours (Keycloak learning + integration)

---

## Migration 6: API Design (REST → REST + GraphQL)

### Current State (MVP)

📄 **File:** `distilled/decisions-made.md`
**Lines:** 60-72

**Read This Section:**
```
Decision 5: REST API (5 Endpoints)

What: Design RESTful API with 5 core endpoints
Why:
- Simple CRUD operations (no complex query needs yet)
- Standard HTTP methods (GET/POST/PUT/DELETE)
- Easy to document with OpenAPI/Swagger
- Well-understood by junior developers
- GraphQL adds complexity not justified for MVP
```

**Key Insight:** REST is sufficient for MVP. GraphQL is open question for future.

---

### Future State (If Needed)

📄 **File:** `distilled/decisions-made.md`
**Lines:** 199-214

**Read This Section:**
```
Open Decision 1: GraphQL Endpoint

What: Should we add GraphQL alongside REST?
Why Consider:
- Complex frontend query needs (fetch entities + relationships in one call)
- Reduce over-fetching (mobile clients)
- Type-safe queries (generated TypeScript types)

Why Defer:
- REST working fine for MVP
- GraphQL adds complexity
- Need to validate query patterns first
```

**What to Do in MVP:**
1. **Design REST resources clearly** (GET /api/entities, GET /api/sources) - maps to GraphQL types
2. **Use structured responses** (JSON with clear schema) - GraphQL schema compatible
3. **Avoid deep nesting** (flat resources, use IDs for relationships) - GraphQL-friendly
4. **Log slow queries** (identify candidates for GraphQL optimization)

**Migration Process (v2.0, if needed):**
1. Analyze REST usage patterns (are clients making multiple requests to build one view?)
2. Define GraphQL schema (maps from REST resources)
3. Add GraphQL endpoint alongside REST (don't remove REST)
4. Migrate clients gradually (REST → GraphQL endpoint by endpoint)

**Estimated Effort:** 24-40 hours (GraphQL learning + schema design)

---

## Migration 7: Monitoring (Logging → Prometheus/Grafana)

### Current State (MVP)

📄 **File:** `distilled/decisions-made.md`
**Lines:** 106-114

**Read This Section:**
```
Decision 10: Python `logging` to stdout

What: Use Python's built-in logging module with stdout output
Why:
- Docker captures stdout logs automatically
- Structured logging (JSON format)
- No file management complexity
- CloudWatch/Datadog compatible (future)
```

**Key Insight:** Logging sufficient for MVP. Metrics/monitoring for production.

---

### Future State (Production)

📄 **File:** `component-map.md`
**Lines:** 144-153

**Read This Section:**
```
FUTURE-9: Metrics & Monitoring

Technology: Prometheus + Grafana
Why Future:
- Production observability (dashboards, alerts)
- Time-series metrics (request rate, latency, errors)
- Resource monitoring (CPU, memory, disk)
- Business metrics (entities processed, feeds fetched)

When: Production deployment (operational visibility)
```

**What to Do in MVP:**
1. **Log structured data** (JSON format: `{"timestamp": "...", "level": "INFO", "message": "..."}`)
2. **Include request IDs** (correlation across services)
3. **Log key metrics** (query time, feed fetch duration, API response time)
4. **Use log levels correctly** (DEBUG/INFO/WARNING/ERROR)

**Migration Process (v3.0):**
1. Add Prometheus exporter to application (`prometheus_client` Python library)
2. Instrument code with metrics (counters, histograms, gauges)
3. Deploy Prometheus to scrape metrics
4. Configure Grafana dashboards
5. Keep logging for detailed debugging (metrics for aggregates)

**Estimated Effort:** 12-16 hours (instrumentation + dashboard setup)

---

## 🎯 Summary: MVP Design Principles for Easy Migration

### 1. **Use Standard Abstractions**
- SQLAlchemy ORM (not raw SQL) → easy database swap
- Standard JWT claims → Keycloak compatible
- Environment variables → Kubernetes ConfigMaps
- Stdout logging → K8s log aggregation

### 2. **Avoid Technology-Specific Features**
- No SQLite-specific SQL (use ORM)
- No Docker Compose-specific scripts (use standard Docker)
- No hardcoded localhost URLs (use environment variables)

### 3. **Design for Compatibility**
- Schema compatible with PostgreSQL
- Foreign keys/join tables (Neo4j migration ready)
- Stateless services (horizontal scaling ready)
- Health checks (K8s probes ready)

### 4. **Measure Before Migrating**
- Log query times (identify caching candidates)
- Log API usage (identify GraphQL candidates)
- Track error rates (identify monitoring needs)

### 5. **Document Migration Paths**
- Write ADRs (Architecture Decision Records) for each technology choice
- Note "why chosen for MVP" and "planned migration for production"
- Keep migration estimates up to date

---

## 📚 Full Reading List

If you followed this guide, you read:
1. `decisions-made.md` (lines 11-21, 33-44, 48-58, 60-72, 106-114, 131-143, 145-159, 161-171, 173-183, 185-197, 199-214)
2. `vision-statement.md` (lines 198-199, 278-295)
3. `technical-context.md` (lines 274-296)
4. `component-map.md` (lines 144-153)

**Total:** ~250 lines across 4 files, curated into coherent 20-minute reading path.

---

**Last Updated:** 2025-10-09
**Bundle Version:** v1.0
**Guide Version:** 1.0
