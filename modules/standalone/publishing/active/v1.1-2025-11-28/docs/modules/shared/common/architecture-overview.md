# Architecture Overview

**Document:** Universal Module Architecture  
**Version:** 1.0  
**Date:** 2025-10-20  
**Status:** DEFINITIVE

---

## Container Architecture

### Universal Requirements
**REQUIRED:** All modules run as independent Docker containers

**Implementation Standards:**
- **Base Images:** Ubuntu-based Docker images for consistency
- **Health Checks:** All modules must implement `/health` endpoint returning 200 OK
- **Metrics:** All modules must implement `/metrics` endpoint (Prometheus format)
- **Port Strategy:** Each module exposes specific ports (80/443 for web, module-specific for APIs)
- **Non-root User:** All containers run as non-root user for security
- **Resource Limits:** Standardized memory and CPU limits per module

### Docker Compose Profiles
```yaml
# Phase 1: Core MVP (5 containers)
core: [frontend, backend, postgres, redis, mailhog]

# Phase 2: Service Expansion (7 containers)  
services: [frontend, bff, backend, publishing, ai, postgres, redis]

# Phase 3: Full Architecture (9+ containers)
full: [frontend, gateway, backend, ai, publishing, postgres, redis, nats, traefik]
```

## Module Independence Requirements

### Critical Standards
**CRITICAL:** Each module must be independently deployable and testable

**Independence Standards:**
- **Separate Containers:** One container per module (Backend, Frontend, AI, Publishing)
- **Mock Interfaces:** Each module must provide mock implementations for development
- **Contract-First Development:** OpenAPI specifications define all module interfaces
- **Database Isolation:** Separate schemas per module (`{module}_{problem}` pattern)
- **Independent Scaling:** Each module scales based on its own load requirements

### Module Boundaries
Each module has clear responsibilities and boundaries:

**Backend Module:**
- Authentication and authorization system
- Database management and migrations
- Content APIs and data storage
- Event production for cross-module workflows

**AI Module:**
- Entity extraction and relationship mapping
- Knowledge graph construction
- Vector operations and similarity search
- Document processing pipeline

**Frontend Module:**
- User interface components and interactions
- State management and real-time updates
- API consumption from Backend
- No direct database access

**Publishing Module:**
- Multi-channel content distribution
- Personalization and engagement tracking
- Content formatting and analytics
- User behavior analysis

## Implementation Phases

### Phase 1: Core MVP (5 containers)
```
Frontend → Backend+Auth → [PostgreSQL, Redis, Mailhog]
```
- Basic functionality with embedded authentication
- 2GB RAM requirement
- Quick startup for junior developers

### Phase 2: Service Expansion (7 containers)
```
Frontend → BFF → [Backend, Publishing, AI] → [PostgreSQL, Redis]
```
- Specialized services with webhook communication
- 2.5GB RAM requirement
- Independent module development

### Phase 3: Full Architecture (9+ containers)
```
Frontend → Gateway → Services → NATS → [Databases]
```
- Event-driven architecture with extracted auth service
- Full production capabilities
- Complete microservices architecture

## Resource Requirements

### Development Environment
- **Individual Developer:** 2-2.5GB RAM (3-5 containers)
- **Full Stack:** 3-3.5GB RAM (all 8+ containers)
- **With Mocks:** Lower resource usage than real services

### Production Environment
- **Minimum:** 4GB RAM per module container
- **Recommended:** 8GB RAM per module container
- **Scaling:** Horizontal scaling capability for all modules

## Validation Requirements

### Container Compliance
- [ ] Docker container runs successfully
- [ ] Health check endpoint responds correctly
- [ ] Metrics endpoint provides Prometheus format
- [ ] Non-root user execution
- [ ] Resource limits configured

### Module Independence
- [ ] Can run independently with mocks
- [ ] OpenAPI specification complete
- [ ] Database schema isolated
- [ ] No direct dependencies on other modules
- [ ] Independent scaling configuration

---

**Related Documentation:**
- [Integration Contracts](./integration-contracts.md)
- [Shared Infrastructure](./shared-infrastructure.md)
- [Development Standards](./development-standards.md)
