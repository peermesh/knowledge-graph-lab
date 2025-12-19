# ⚡ Shared Module Requirements - Quick Reference

**🔥 CRITICAL:** All modules must implement these requirements for immediate interoperability.

**📍 Two Levels of Requirements:**

### 🚀 **Standalone Module** (MVP - Immediate Implementation)
**[Standalone Module Requirements](shared/standalone-modules/README.md)** - Basic interoperability for immediate team handover
- ✅ **Single PostgreSQL** database with module schemas
- ✅ **Basic Docker containers** with standard ports
- ✅ **Simple REST APIs** with OpenAPI documentation
- ✅ **Basic JWT authentication** managed by Backend module
- ✅ **Development environment** with mocks and offline capability

### 🔬 **PeerMesh Module** (Advanced - Stretch Goals)
**[PeerMesh Module Requirements](shared/peermesh-modules/README.md)** - Advanced features building into PeerMesh Abstraction Program
- ✅ **Multi-database architecture** (PostgreSQL + Qdrant + OpenSearch + TimescaleDB)
- ✅ **Parallel search** across specialized backends
- ✅ **Event-driven architecture** with NATS JetStream
- ✅ **Dual-layer authorization** (SpiceDB + OPA)
- ✅ **Advanced observability** (OpenTelemetry, Prometheus, Grafana)
- ✅ **Backend abstraction** with swappable implementations

**📖 Implementation Guide:**
**[Shared Module Overview](shared/README.md)** - Complete guide on how to use both levels of the shared module system.

## 🔍 How to Find This Document
- **From docs/modules/ directory** - This file is in the modules root
- **From project root** - `docs/modules/SHARED-MODULE-REQUIREMENTS-QUICK-REF.md`
- **Main README reference** - Linked in the Architecture Overview section
- **Docs index** - Listed in the Shared Module Requirements section

## 🎯 What This Ensures
- ✅ All modules run in Docker containers with same setup
- ✅ Shared PostgreSQL database integration
- ✅ Consistent REST API contracts
- ✅ JWT authentication system integration
- ✅ Development environment setup for all team members

## 🚨 Override Authority
This specification **OVERRIDES** any conflicting requirements in individual module specifications. When in doubt, these requirements take precedence.

## 🛠️ Quick Commands

### Validate Any Module
```bash
python3 scripts/validate-standalone-compliance.py docs/modules/backend-architecture/Backend-Architecture-Spec.md
```

### Use Agent Prompt
Copy the complete agent prompt from the bottom of `docs/modules/shared/standalone-modules/README.md` and give it to any AI agent to apply these requirements to any module specification.

## 📋 Requirements Checklists

### 🚀 Standalone Module Checklist (MVP - REQUIRED)
**Container Architecture (REQUIRED)**
- [ ] Docker containers with Python 3.11+ or Node.js 18+
- [ ] Container names: `{module}-module`
- [ ] Unique ports (3000-3999 web, 8000-8999 API)
- [ ] `/health` endpoint returning 200 OK
- [ ] Environment variables for all configuration

**Database Standards (REQUIRED)**
- [ ] Shared PostgreSQL 15+ with JSONB support
- [ ] Schema pattern: `{module}_{problem}`
- [ ] Connection pooling with retry logic
- [ ] Version-controlled schema migrations

**API Standards (REQUIRED)**
- [ ] REST APIs with `/api/v1` base path
- [ ] Standard JSON response format
- [ ] RFC7807 Problem Details error handling
- [ ] OpenAPI documentation at `/api/v1/openapi.json`

**Authentication Integration (REQUIRED)**
- [ ] JWT-based auth managed by Backend module
- [ ] Standard JWT claims (sub, role, iss, aud, iat, exp)
- [ ] Roles: user, admin, moderator (extensible)
- [ ] HTTPS-only, secure token storage

**Development Setup (REQUIRED)**
- [ ] Mock implementations for development
- [ ] Offline mode capability
- [ ] Docker Compose setup for local development
- [ ] Contract-first API development

### 🔬 PeerMesh Module Checklist (Advanced - OPTIONAL)
**Multi-Database Architecture (OPTIONAL)**
- [ ] Qdrant for vector embeddings and similarity search
- [ ] OpenSearch for full-text search capabilities
- [ ] TimescaleDB for analytics and trend data
- [ ] Parallel query execution across all backends

**Event-Driven Architecture (OPTIONAL)**
- [ ] NATS JetStream for asynchronous communication
- [ ] Event schema validation and dead letter queues
- [ ] Correlation IDs and message tracing

**Advanced Authorization (OPTIONAL)**
- [ ] SpiceDB (ReBAC) for relationship-based access control
- [ ] OPA (ABAC) for policy-based authorization
- [ ] Dual-layer authorization system

**Enhanced Observability (OPTIONAL)**
- [ ] OpenTelemetry for distributed tracing
- [ ] Prometheus for metrics collection
- [ ] Grafana for visualization dashboards
- [ ] ELK Stack for centralized logging

**Backend Abstraction (OPTIONAL)**
- [ ] Swappable backend implementations
- [ ] Interface abstraction layer
- [ ] Health monitoring and graceful migration

## 📚 Agent Prompts for Implementation

### 🚀 Standalone Module Agent Prompt (MVP)
**Complete agent prompt available at:** `docs/modules/shared/standalone-modules/README.md` (bottom section)

**Purpose:** Implement basic interoperability requirements
**Scope:** Container architecture, basic APIs, authentication, development setup
**Copy the prompt** and give it to any agent for immediate implementation

### 🔬 PeerMesh Module Agent Prompt (Advanced)
**Complete agent prompt available at:** `docs/modules/shared/peermesh-modules/README.md` (bottom section)

**Purpose:** Implement advanced features and sophisticated interoperability
**Scope:** Parallel search, event-driven architecture, dual authorization, observability
**Copy the prompt** and give it to any agent for Phase 2+ implementation

Both prompts include:
- 6-step implementation process
- Module identification and reading
- Requirements comparison and gap analysis
- Implementation plan generation
- Change implementation and validation

## ✅ Current Compliance Status

### 🚀 Standalone Module Compliance (MVP - Required)
| Module | Status | Issues |
|--------|--------|---------|
| **Backend** | ✅ **COMPLIANT** | All basic requirements implemented |
| **Frontend** | ❌ **NON-COMPLIANT** | Missing container, database, observability requirements |
| **AI** | ❌ **NON-COMPLIANT** | Missing container, database, authentication requirements |
| **Publishing** | ❌ **NON-COMPLIANT** | Missing container, database, API, observability requirements |

### 🔬 PeerMesh Module Compliance (Advanced - Optional)
| Module | Status | Notes |
|--------|--------|-------|
| **Backend** | ❌ **NOT IMPLEMENTED** | Advanced features not yet added |
| **Frontend** | ❌ **NOT IMPLEMENTED** | Advanced features not yet added |
| **AI** | ❌ **NOT IMPLEMENTED** | Advanced features not yet added |
| **Publishing** | ❌ **NOT IMPLEMENTED** | Advanced features not yet added |

## 🔄 Implementation Priority

### 🚀 Standalone Module Priority (MVP - Required)
1. **Phase 1 (Immediate - 2-4 weeks):** Get all modules running in Docker containers
2. **Phase 2 (Short-term - 4-8 weeks):** Enhanced observability and API documentation
3. **Phase 3 (Medium-term - 8-12 weeks):** Testing integration and performance optimization

### 🔬 PeerMesh Module Priority (Advanced - Optional)
1. **Phase 2 (4-8 weeks):** Parallel search implementation across multiple backends
2. **Phase 3 (8-12 weeks):** Event-driven architecture with NATS JetStream
3. **Phase 4 (12-16 weeks):** Dual-layer authorization and advanced observability
4. **Phase 5 (16-20 weeks):** Backend abstraction and service mesh integration

## 🎉 Success Criteria

### 🚀 Standalone Module Success (MVP - Required)
- ✅ All 4 modules pass standalone compliance validation
- ✅ Basic interoperability working across all modules
- ✅ Development teams can implement independently
- ✅ Specifications are clear and actionable
- ✅ Docker containers start reliably in under 30 seconds
- ✅ Shared PostgreSQL database accessible to all modules
- ✅ JWT authentication functional across modules

### 🔬 PeerMesh Module Success (Advanced - Optional)
- ✅ Parallel search across Neo4j, Qdrant, and OpenSearch functional
- ✅ Event-driven pipeline processing documents end-to-end
- ✅ Dual authorization system enforcing complex policies
- ✅ Complete observability with distributed tracing
- ✅ Backend swapping without service interruption
- ✅ All PeerMesh Abstraction Program requirements implemented

---

**Next Steps:**

### 🚀 For MVP Implementation (Immediate)
1. **Read Standalone Module specification:** `docs/modules/shared/standalone-modules/README.md`
2. **Copy the Standalone agent prompt** (bottom section)
3. **Apply to non-compliant modules:** Frontend, AI, Publishing
4. **Run validation:** `python3 scripts/validate-standalone-compliance.py [module-spec]`

### 🔬 For Advanced Implementation (Stretch Goals)
1. **Read PeerMesh Module specification:** `docs/modules/shared/peermesh-modules/README.md`
2. **Copy the PeerMesh agent prompt** (bottom section)
3. **Plan Phase 2+ enhancements** with backward compatibility
4. **Ensure compatibility** with standalone module requirements

**Hierarchy:** Standalone Module (MVP) → PeerMesh Module (Advanced). Advanced features must maintain backward compatibility with basic functionality.**
