# Integration Contracts

**Document:** Module Integration Contracts  
**Version:** 1.0  
**Date:** 2025-10-20  
**Status:** DEFINITIVE

---

## API Contract Standards

### Universal Requirements
**REQUIRED:** REST APIs with OpenAPI documentation for all modules

**API Standards:**
- **Framework:** FastAPI for Python modules, Express.js for Node.js modules
- **Base Path:** `/api/v1` for all endpoints
- **Documentation:** OpenAPI/Swagger documentation at `/api/v1/openapi.json`
- **Pagination:** Standard pagination (`page`, `limit`, `total`)
- **Error Handling:** RFC7807 Problem Details format
- **Idempotency:** `Idempotency-Key` header for write operations

### Standard Response Format
```json
{
  "data": {},
  "meta": {
    "page": 1,
    "limit": 50,
    "total": 100
  },
  "errors": []
}
```

### Error Response Format
```json
{
  "type": "https://example.com/problems/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "Invalid input provided",
  "instance": "/api/v1/entities",
  "correlation_id": "req-123456"
}
```

## Module-Specific Interfaces

### Backend ↔ AI Integration

#### Backend → AI (Request Interfaces)
```typescript
// Entity Extraction
POST /api/ai/extract-entities
{
  "content": "string",
  "extraction_type": "entities|relationships|both",
  "confidence_threshold": 0.7
}

// Content Analysis
POST /api/ai/analyze-content
{
  "content": "string",
  "analysis_type": "sentiment|topics|quality",
  "parameters": {}
}
```

#### AI → Backend (Event Interfaces)
```typescript
// Content Submitted Event
content.submitted: {
  "content_id": "uuid",
  "source_url": "string",
  "content_type": "article|pdf|rss",
  "processing_priority": "high|medium|low"
}

// AI Extracted Event
ai.extracted: {
  "content_id": "uuid",
  "entities": [],
  "relationships": [],
  "confidence_scores": {},
  "processing_time_ms": 1500
}
```

### Backend ↔ Frontend Integration

#### REST APIs
```typescript
// Entity Management
GET /api/v1/entities
POST /api/v1/entities
GET /api/v1/entities/{id}
PUT /api/v1/entities/{id}
DELETE /api/v1/entities/{id}

// Dashboard Data
GET /api/v1/dashboard
{
  "entities_count": 1250,
  "relationships_count": 3400,
  "last_updated": "2025-10-20T19:00:00Z",
  "processing_status": "active"
}

// Search Interface
POST /api/v1/search
{
  "query": "string",
  "filters": {},
  "limit": 50,
  "offset": 0
}
```

#### WebSocket Connections
```typescript
// Real-time Updates
ws://backend:8000/ws/updates
{
  "type": "entity_created|entity_updated|processing_complete",
  "data": {},
  "timestamp": "2025-10-20T19:00:00Z"
}
```

### Publishing ↔ All Modules Integration

#### Content Distribution
```typescript
// Content Ready for Distribution
GET /api/v1/content/ready
{
  "content_items": [],
  "distribution_channels": ["email", "webhook", "api"],
  "personalization_data": {}
}

// Distribution Request
POST /api/v1/distribute
{
  "content_id": "uuid",
  "channels": ["email", "webhook"],
  "target_audience": "all|subscribed|custom",
  "schedule": "immediate|scheduled"
}

// Analytics and Metrics
GET /api/v1/analytics
{
  "engagement_metrics": {},
  "distribution_stats": {},
  "user_behavior": {}
}
```

## Data Flow Architecture

### Event-Driven Data Flow
**REQUIRED:** Event-driven data flow with clear module boundaries

**Data Flow Pattern:**
```
1. Backend (content.submitted) → AI (processing)
2. AI (ai.extracted) → Backend (storage)  
3. Backend (content.ready) → Publishing (distribution)
4. Publishing (publishing.completed) → All Modules (notification)
```

### Event Schema Standards
```typescript
interface BaseEvent {
  event_id: string;
  event_type: string;
  timestamp: string;
  source_module: string;
  correlation_id: string;
  data: any;
}

interface ContentSubmittedEvent extends BaseEvent {
  event_type: "content.submitted";
  source_module: "backend";
  data: {
    content_id: string;
    source_url: string;
    content_type: string;
    processing_priority: string;
  };
}
```

## Authentication Integration

### JWT Token Standards
```typescript
interface JWTPayload {
  sub: string;        // User ID
  role: string;       // User role
  iss: string;        // Issuer
  aud: string;        // Audience
  iat: number;        // Issued at
  exp: number;        // Expiration
  permissions: string[]; // User permissions
}
```

### Service-to-Service Authentication
```typescript
interface ServiceAuth {
  service_id: string;
  api_key: string;
  permissions: string[];
  expires_at: string;
}
```

## Message Queue Integration

### RabbitMQ Configuration
```yaml
# Exchange Configuration
exchanges:
  - name: "kgl.events"
    type: "topic"
    durable: true
    
# Queue Configuration
queues:
  - name: "ai.processing"
    durable: true
    arguments:
      x-dead-letter-exchange: "kgl.events.dlq"
      
# Routing Keys
routing_keys:
  - "content.submitted"
  - "ai.extracted"
  - "publishing.triggered"
  - "user.authenticated"
```

### Message Format
```typescript
interface MessageEnvelope {
  message_id: string;
  correlation_id: string;
  timestamp: string;
  source_module: string;
  event_type: string;
  payload: any;
  retry_count: number;
  max_retries: number;
}
```

## Validation Requirements

### API Contract Compliance
- [ ] OpenAPI specification complete and valid
- [ ] All endpoints documented with examples
- [ ] Error responses follow RFC7807 format
- [ ] Pagination implemented consistently
- [ ] Idempotency headers supported

### Event Schema Compliance
- [ ] All events follow BaseEvent interface
- [ ] Event schemas validated with JSON Schema
- [ ] Correlation IDs propagated correctly
- [ ] Dead letter queue handling implemented
- [ ] Retry logic with exponential backoff

### Authentication Integration
- [ ] JWT tokens validated on all protected endpoints
- [ ] Service-to-service authentication implemented
- [ ] Role-based access control enforced
- [ ] Token refresh flow implemented
- [ ] Security headers configured correctly

---

**Related Documentation:**
- [Architecture Overview](./architecture-overview.md)
- [Shared Infrastructure](./shared-infrastructure.md)
- [Security & Compliance](./security-compliance.md)
