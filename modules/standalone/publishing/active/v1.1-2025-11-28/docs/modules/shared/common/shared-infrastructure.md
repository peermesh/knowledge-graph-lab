# Shared Infrastructure

**Document:** Shared Infrastructure Requirements  
**Version:** 1.0  
**Date:** 2025-10-20  
**Status:** DEFINITIVE

---

## Database Architecture

### Universal Requirements
**REQUIRED:** Shared PostgreSQL instance with module-specific schemas

**Database Standards:**
- **Primary Database:** PostgreSQL 15+ with JSONB support
- **Vector Database:** Qdrant for vector embeddings and similarity search
- **Naming Convention:** `{module}_{problem}` pattern (e.g., `ai_entities`, `be_authentication`)
- **Connection Management:** Connection pooling and retry logic required
- **Migration Strategy:** Version-controlled schema migrations across all modules
- **Backup Strategy:** Daily automated backups with 14-day retention
- **Access Control:** Module-specific database users with limited permissions

### Schema Separation
```sql
-- Backend Module Schema
CREATE SCHEMA backend_auth;
CREATE SCHEMA backend_content;

-- AI Module Schema  
CREATE SCHEMA ai_entities;
CREATE SCHEMA ai_processing;

-- Publishing Module Schema
CREATE SCHEMA publishing_subscribers;
CREATE SCHEMA publishing_campaigns;
```

### Database Configuration
```yaml
# PostgreSQL Configuration
postgresql:
  version: "15+"
  extensions:
    - "uuid-ossp"
    - "pg_trgm"
    - "btree_gin"
  
  # Connection Pooling
  connection_pool:
    min_connections: 5
    max_connections: 100
    connection_timeout: 30s
    
  # Backup Configuration
  backup:
    schedule: "0 2 * * *"  # Daily at 2 AM
    retention_days: 14
    compression: true
```

### Qdrant Vector Database
```yaml
# Qdrant Configuration
qdrant:
  version: "1.7+"
  host: "qdrant"
  port: 6333
  
  # Collection Configuration
  collections:
    - name: "entity_embeddings"
      vector_size: 1536
      distance: "Cosine"
      
    - name: "content_embeddings"
      vector_size: 1536
      distance: "Cosine"
```

## Message Queue Architecture

### RabbitMQ Configuration
**REQUIRED:** RabbitMQ for asynchronous communication between modules

**Messaging Standards:**
- **Technology:** RabbitMQ with topic exchanges for flexible routing
- **Queue Naming:** `{module}.{operation}` pattern for clarity
- **Durability:** Persistent queues and messages for reliability
- **Error Handling:** Dead letter queues with exponential backoff retry
- **Event Schema:** JSON Schema validation for all message types
- **Delivery Guarantees:** At-least-once delivery with idempotency

### Exchange and Queue Configuration
```yaml
# RabbitMQ Configuration
rabbitmq:
  version: "3.12+"
  
  # Exchanges
  exchanges:
    - name: "kgl.events"
      type: "topic"
      durable: true
      
    - name: "kgl.events.dlq"
      type: "topic"
      durable: true
      
  # Queues
  queues:
    - name: "ai.processing"
      durable: true
      arguments:
        x-dead-letter-exchange: "kgl.events.dlq"
        x-message-ttl: 300000  # 5 minutes
        
    - name: "publishing.distribution"
      durable: true
      arguments:
        x-dead-letter-exchange: "kgl.events.dlq"
        
    - name: "backend.notifications"
      durable: true
```

### Event Types
```
content.submitted    # Backend → AI (new content ready)
ai.extracted        # AI → Backend (processing complete)
publishing.triggered # Backend → Publishing (content ready)
user.authenticated  # Backend → All (auth events)
```

## Authentication & Authorization

### JWT-Based Authentication
**REQUIRED:** JWT-based authentication with Role-Based Access Control (RBAC)

**Auth Standards:**
- **Provider:** Backend module owns and implements authentication system
- **Token Format:** JWT with standard claims (`sub`, `role`, `iss`, `aud`, `iat`, `exp`)
- **Roles:** `user`, `admin`, `moderator` (extensible)
- **Refresh Tokens:** Long-lived refresh tokens for session management
- **Service Accounts:** API key authentication for service-to-service communication
- **Security:** HTTPS-only, secure token storage, token expiration

### Authentication Configuration
```yaml
# JWT Configuration
jwt:
  algorithm: "RS256"
  access_token_expiry: "15m"
  refresh_token_expiry: "7d"
  
  # Claims
  required_claims:
    - "sub"    # Subject (User ID)
    - "role"   # User Role
    - "iss"    # Issuer
    - "aud"    # Audience
    - "iat"    # Issued At
    - "exp"    # Expiration
    
  # Roles and Permissions
  roles:
    user:
      permissions: ["read:content", "read:entities"]
    admin:
      permissions: ["*"]
    moderator:
      permissions: ["read:*", "write:content", "moderate:users"]
```

### Service-to-Service Authentication
```yaml
# Service Authentication
service_auth:
  api_keys:
    - service_id: "ai-module"
      key: "${AI_SERVICE_API_KEY}"
      permissions: ["read:content", "write:entities"]
      
    - service_id: "publishing-module"
      key: "${PUBLISHING_SERVICE_API_KEY}"
      permissions: ["read:content", "write:analytics"]
```

## Redis Caching

### Cache Configuration
```yaml
# Redis Configuration
redis:
  version: "7+"
  host: "redis"
  port: 6379
  
  # Cache Configuration
  cache:
    default_ttl: "1h"
    max_memory: "512mb"
    eviction_policy: "allkeys-lru"
    
  # Session Storage
  sessions:
    ttl: "24h"
    key_prefix: "session:"
    
  # Rate Limiting
  rate_limiting:
    window: "1m"
    max_requests: 100
```

## Observability Infrastructure

### Logging Configuration
```yaml
# Logging Configuration
logging:
  format: "json"
  level: "INFO"
  
  # Standard Fields
  fields:
    - "timestamp"
    - "level"
    - "message"
    - "module_id"
    - "trace_id"
    - "user_id"
    
  # Retention
  retention:
    logs: "7d"
    metrics: "30d"
```

### Metrics Configuration
```yaml
# Metrics Configuration
metrics:
  format: "prometheus"
  port: 9090
  
  # Standard Metrics
  metrics:
    - "requests_total"
    - "request_duration_seconds"
    - "errors_total"
    - "active_connections"
    - "queue_depth"
```

## Configuration Management

### Environment Variables
```bash
# Database Configuration
DATABASE_URL=postgres://user:pass@postgres:5432/dbname
QDRANT_URL=http://qdrant:6333

# Message Queue Configuration
RABBITMQ_URL=amqp://user:pass@rabbitmq:5672

# Authentication Configuration
JWT_SECRET=your-secret-key
JWT_EXPIRATION=3600

# Redis Configuration
REDIS_URL=redis://redis:6379

# Observability Configuration
LOG_LEVEL=INFO
METRICS_ENABLED=true
```

### Secrets Management
```yaml
# Secrets Configuration
secrets:
  # Database Secrets
  database:
    password: "${DB_PASSWORD}"
    
  # JWT Secrets
  jwt:
    private_key: "${JWT_PRIVATE_KEY}"
    public_key: "${JWT_PUBLIC_KEY}"
    
  # Service API Keys
  services:
    ai_api_key: "${AI_SERVICE_API_KEY}"
    publishing_api_key: "${PUBLISHING_SERVICE_API_KEY}"
```

## Validation Requirements

### Database Compliance
- [ ] PostgreSQL schemas created with proper naming convention
- [ ] Connection pooling configured correctly
- [ ] Migration scripts version controlled
- [ ] Backup strategy implemented
- [ ] Access control configured

### Message Queue Compliance
- [ ] RabbitMQ exchanges and queues configured
- [ ] Dead letter queues implemented
- [ ] Event schemas validated
- [ ] Retry logic with exponential backoff
- [ ] Message durability enabled

### Authentication Compliance
- [ ] JWT tokens generated and validated correctly
- [ ] Role-based access control implemented
- [ ] Service-to-service authentication configured
- [ ] Token refresh flow implemented
- [ ] Security headers configured

### Infrastructure Compliance
- [ ] Redis caching configured
- [ ] Observability endpoints implemented
- [ ] Configuration validation on startup
- [ ] Secrets management implemented
- [ ] Health checks configured

---

**Related Documentation:**
- [Architecture Overview](./architecture-overview.md)
- [Integration Contracts](./integration-contracts.md)
- [Development Standards](./development-standards.md)
