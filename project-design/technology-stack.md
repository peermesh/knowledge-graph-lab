# Module Integration Guide

## Overview
The Knowledge Graph Lab consists of four independent modules that work together to create an intelligent research system. This guide explains how these modules communicate, their dependencies, and integration patterns following PeerMesh architecture principles.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     Module 4: Frontend                        │
│                    (Next.js Application)                      │
│                        Port: 3000                             │
└────────────┬───────────────┬──────────────┬──────────────────┘
             │               │              │
             ▼               ▼              ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│    Module 1      │ │    Module 2    │ │    Module 3      │
│   Ingestion      │ │ Knowledge Graph│ │   Reasoning      │
│   Port: 8001     │ │   Port: 8002   │ │   Port: 8003     │
└──────────────────┘ └────────────────┘ └──────────────────┘
         │                    ▲                  ▲
         └────────────────────┴──────────────────┘
```

## Module Communication Patterns

### 1. Data Flow Pipeline
**Primary Flow**: Module 1 → Module 2 → Module 3 → Module 4

1. **Ingestion (M1)** fetches and normalizes content
2. **Knowledge Graph (M2)** extracts entities and builds relationships
3. **Reasoning (M3)** generates insights and content
4. **Frontend (M4)** presents information to users

### 2. Feedback Loops
- **M3 → M1**: Reasoning engine suggests new sources to ingest
- **M4 → M3**: User preferences influence digest generation
- **M2 → M1**: Knowledge gaps trigger targeted ingestion

## Inter-Module APIs

### Module 1 → Module 2
**Entity Extraction Request**
```json
POST http://localhost:8002/api/entities/extract
{
  "content_id": "content_789",
  "text": "Article content here...",
  "metadata": {
    "source": "techcrunch",
    "ingested_at": "2025-09-08T10:00:00Z"
  }
}
```

### Module 2 → Module 3
**Knowledge Context Request**
```json
GET http://localhost:8003/api/research/context/creator-economy
```

### Module 3 → Module 1
**Research Priority Feedback**
```json
POST http://localhost:8001/api/sources/suggest
{
  "priority_entities": ["Beehiiv", "ConvertKit"],
  "suggested_sources": ["beehiiv.com/blog", "convertkit.com/resources"]
}
```

### Module 4 → All Modules
The frontend aggregates data from all backend modules:
```javascript
// Frontend API aggregation example
const getDashboardData = async () => {
  const [ingestion, knowledge, reasoning] = await Promise.all([
    fetch('http://localhost:8001/api/sources/stats'),
    fetch('http://localhost:8002/api/knowledge/stats'),
    fetch('http://localhost:8003/api/frontier/next?count=5')
  ]);
  
  return {
    ingestionStats: await ingestion.json(),
    knowledgeStats: await knowledge.json(),
    researchQueue: await reasoning.json()
  };
};
```

## Dependency Management

### Required Services Order
1. **Start Order**: Database → Module 1 → Module 2 → Module 3 → Module 4
2. **Shutdown Order**: Reverse of start order

### Service Dependencies
```yaml
# docker-compose.yml structure
services:
  database:
    image: postgres:15
    # No dependencies
  
  ingestion:
    depends_on:
      - database
    
  knowledge-graph:
    depends_on:
      - database
      - ingestion
    
  reasoning:
    depends_on:
      - database
      - knowledge-graph
    
  frontend:
    depends_on:
      - ingestion
      - knowledge-graph
      - reasoning
```

## Configuration Synchronization

### Shared Configuration
Create a `shared/config.json` for cross-module settings:
```json
{
  "domain": "creator-economy",
  "location": "Boulder, CO",
  "entity_types": ["Platform", "Organization", "Person", "Grant", "Policy", "Event"],
  "api_keys": {
    "openai": "${OPENAI_API_KEY}",
    "anthropic": "${ANTHROPIC_API_KEY}",
    "perplexity": "${PERPLEXITY_API_KEY}"
  },
  "rate_limits": {
    "ingestion": 60,
    "llm_calls": 100,
    "graph_queries": 1000
  }
}
```

### Environment Variables
Use a shared `.env` file at the repository root:
```bash
# Shared API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PERPLEXITY_API_KEY=pplx-...

# Module URLs (for inter-service communication)
INGESTION_URL=http://localhost:8001
KNOWLEDGE_URL=http://localhost:8002
REASONING_URL=http://localhost:8003
FRONTEND_URL=http://localhost:3000

# Shared Database
DATABASE_URL=postgresql://user:pass@localhost:5432/kgl
```

## Error Handling Across Modules

### Cascade Failure Prevention
Each module should handle failures gracefully:

```python
# Example: Module 2 handling Module 1 unavailability
async def get_content(content_id: str):
    try:
        response = await fetch(f"{INGESTION_URL}/api/content/{content_id}")
        return response.json()
    except ConnectionError:
        # Fall back to cached data
        return get_cached_content(content_id)
    except TimeoutError:
        # Use mock data for development
        return get_mock_content(content_id)
```

### Circuit Breaker Pattern
Implement circuit breakers for inter-module calls:
```python
from circuit_breaker import CircuitBreaker

ingestion_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=60,
    expected_exception=ConnectionError
)

@ingestion_breaker
def call_ingestion_api(endpoint):
    return requests.get(f"{INGESTION_URL}{endpoint}")
```

## Data Consistency

### Event-Driven Updates
Use events to maintain consistency across modules:

```python
# Module 2: After entity extraction
async def after_entity_extraction(entities):
    # Notify Module 3 about new entities
    await notify_reasoning_module({
        "event": "entities_added",
        "entities": entities,
        "timestamp": datetime.now()
    })
    
    # Update Module 1 with entity feedback
    await update_ingestion_priorities({
        "discovered_entities": entities,
        "suggest_related": True
    })
```

### Eventual Consistency
Accept that data may be temporarily inconsistent:
- Use timestamps for versioning
- Implement retry mechanisms
- Queue failed updates for later processing

## Testing Integration

### Integration Test Setup
```bash
# Start all services in test mode
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/integration/

# Test specific integration
pytest tests/integration/test_m1_m2_integration.py
```

### Mock Services for Development
Each module can run with mocked dependencies:
```bash
# Run Module 2 with mock Module 1
cd modules/module-2-knowledge-graph
python src/main.py --mock-ingestion

# Run Module 4 with all mocked backends
cd modules/module-4-frontend
npm run dev:mock
```

## Monitoring Integration Health

### Health Check Endpoints
Each module exposes health checks including dependency status:
```json
GET http://localhost:8002/health
{
  "status": "healthy",
  "dependencies": {
    "database": "connected",
    "ingestion_service": "connected",
    "openai_api": "connected"
  }
}
```

### Distributed Tracing
Implement request tracing across modules:
```python
# Add trace headers to inter-module requests
headers = {
    "X-Trace-ID": generate_trace_id(),
    "X-Parent-Span": current_span_id(),
    "X-Source-Module": "knowledge-graph"
}
```

## Performance Optimization

### Caching Strategy
- **Module 1**: Cache ingested content for 24 hours
- **Module 2**: Cache entity embeddings permanently
- **Module 3**: Cache reasoning results for 1 hour
- **Module 4**: Use React Query for client-side caching

### Batch Operations
Batch requests between modules to reduce overhead:
```python
# Instead of individual requests
for content in content_list:
    extract_entities(content)  # Bad: N requests

# Use batch endpoints
extract_entities_batch(content_list)  # Good: 1 request
```

### Async Communication
Use message queues for non-critical updates:
```python
# Module 1: Publish content to queue
async def publish_content(content):
    await redis_queue.publish("new_content", content)

# Module 2: Subscribe to content updates
async def consume_content():
    async for content in redis_queue.subscribe("new_content"):
        await process_content(content)
```

## Security Considerations

### API Key Management
- Never expose internal API keys between modules
- Use service-to-service authentication for production
- Implement rate limiting on all endpoints

### Data Validation
Validate data at module boundaries:
```python
from pydantic import BaseModel

class ContentRequest(BaseModel):
    content_id: str
    text: str
    metadata: dict
    
    class Config:
        max_anystr_length = 50000  # Prevent DoS
```

## Troubleshooting Integration Issues

### Common Problems and Solutions

#### Module Communication Timeout
**Problem**: Requests between modules timing out
**Solution**: 
- Increase timeout values in HTTP clients
- Check network connectivity between containers
- Verify services are running on correct ports

#### Data Inconsistency
**Problem**: Different modules showing different data
**Solution**:
- Check timestamp synchronization
- Verify event propagation is working
- Clear caches and force refresh

#### Cascade Failures
**Problem**: One module failure brings down others
**Solution**:
- Implement circuit breakers
- Add fallback mechanisms
- Use mock data for non-critical operations

#### Performance Degradation
**Problem**: System slows down with scale
**Solution**:
- Add caching layers
- Implement pagination
- Use batch operations
- Consider horizontal scaling

## Development Workflow

### Local Development
```bash
# Start core services
docker-compose up database redis

# Start each module in development mode
# Terminal 1
cd modules/module-1-ingestion && python src/main.py --dev

# Terminal 2
cd modules/module-2-knowledge-graph && python src/main.py --dev

# Terminal 3
cd modules/module-3-reasoning && python src/main.py --dev

# Terminal 4
cd modules/module-4-frontend && npm run dev
```

### Testing Changes
1. Make changes in your module
2. Test with mock data first
3. Test with one real dependency
4. Test with all dependencies
5. Run integration test suite

## Best Practices

1. **Keep modules truly independent** - Each should provide value alone
2. **Use standardized API contracts** - OpenAPI/Swagger documentation
3. **Version your APIs** - Support backward compatibility
4. **Monitor everything** - Logs, metrics, traces
5. **Fail gracefully** - Degraded service is better than no service
6. **Document integration points** - Keep this document updated
7. **Test integration regularly** - Automated tests prevent drift

## Next Steps

1. Implement service mesh for production (Istio/Linkerd)
2. Add distributed tracing (Jaeger/Zipkin)
3. Create integration test suite
4. Build admin dashboard for monitoring
5. Implement blue-green deployments
6. Add automated rollback capabilities