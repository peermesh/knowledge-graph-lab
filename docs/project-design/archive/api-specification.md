# API Specification

## Overview

This document defines the complete API contracts between all Knowledge Graph Lab modules. Each module exposes a RESTful API that other modules and external clients can consume. All APIs follow consistent patterns for authentication, error handling, and response formats to simplify integration.

<!-- DIAGRAM NOTE: Add an API architecture diagram showing all four modules with their ports and the main API endpoints between them -->

## Common Standards

### Response Format

All API responses follow a consistent structure for predictability and ease of parsing.

```json
{
  "success": true,
  "data": {
    // Response payload specific to endpoint
  },
  "metadata": {
    "timestamp": "2025-09-09T10:00:00Z",
    "version": "1.0.0",
    "request_id": "req_abc123"
  },
  "errors": []
}
```

Error responses maintain the same structure with details about what went wrong.

```json
{
  "success": false,
  "data": null,
  "metadata": {
    "timestamp": "2025-09-09T10:00:00Z",
    "version": "1.0.0",
    "request_id": "req_abc123"
  },
  "errors": [
    {
      "code": "ENTITY_NOT_FOUND",
      "message": "The requested entity does not exist",
      "field": "entity_id",
      "details": {}
    }
  ]
}
```

### Authentication

During development, we use simple API key authentication passed in the header. Production deployments should upgrade to OAuth 2.0 or similar.

```
Authorization: Bearer <api_key>
```

### Status Codes

APIs use standard HTTP status codes to indicate success or failure.

- 200 OK - Request succeeded
- 201 Created - Resource created successfully
- 400 Bad Request - Invalid request parameters
- 401 Unauthorized - Missing or invalid authentication
- 404 Not Found - Resource doesn't exist
- 429 Too Many Requests - Rate limit exceeded
- 500 Internal Server Error - Server-side error

### Rate Limiting

Each API enforces rate limiting to prevent abuse and ensure fair usage.

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1625097600
```

---

## Module 1: Ingestion API

**Base URL**: `http://localhost:8001`  
**Purpose**: Manages data source configuration, ingestion pipelines, and content retrieval

### GET /api/sources

Returns configured data sources and their current status.

**Response Example**:
```json
{
  "success": true,
  "data": {
    "sources": [
      {
        "id": "source_techcrunch_001",
        "name": "TechCrunch Creator Economy Feed",
        "type": "rss",
        "url": "https://techcrunch.com/category/creator-economy/feed/",
        "status": "active",
        "last_fetched": "2025-09-09T09:30:00Z",
        "fetch_frequency": "hourly",
        "items_retrieved": 1247,
        "error_count": 0
      },
      {
        "id": "source_youtube_api_001",
        "name": "YouTube Data API",
        "type": "api",
        "status": "active",
        "last_fetched": "2025-09-09T09:45:00Z",
        "fetch_frequency": "daily",
        "items_retrieved": 523,
        "error_count": 2
      }
    ],
    "total_sources": 2,
    "active_sources": 2
  }
}
```

**Test Command**:
```bash
curl -H "Authorization: Bearer your_api_key" \
     http://localhost:8001/api/sources
```

### POST /api/sources

Adds a new data source to the ingestion pipeline.

**Request Body**:
```json
{
  "name": "Creator Economy Newsletter",
  "type": "rss",
  "url": "https://creatoreconomy.report/feed/",
  "fetch_frequency": "daily",
  "config": {
    "parse_full_content": true,
    "follow_redirects": true
  }
}
```

**Response Example**:
```json
{
  "success": true,
  "data": {
    "source": {
      "id": "source_newsletter_001",
      "name": "Creator Economy Newsletter",
      "status": "pending_validation",
      "created_at": "2025-09-09T10:00:00Z"
    }
  }
}
```

### GET /api/content/{content_id}

Retrieves a specific piece of ingested content.

**Response Example**:
```json
{
  "success": true,
  "data": {
    "content": {
      "id": "content_789",
      "source_id": "source_techcrunch_001",
      "title": "Patreon Launches New Creator Tools",
      "url": "https://techcrunch.com/patreon-creator-tools",
      "author": "Sarah Perez",
      "published_date": "2025-09-08T14:00:00Z",
      "ingested_date": "2025-09-08T14:30:00Z",
      "raw_text": "Full article text here...",
      "metadata": {
        "word_count": 850,
        "language": "en",
        "tags": ["patreon", "creator-tools", "monetization"]
      },
      "status": "processed"
    }
  }
}
```

### POST /api/ingest/trigger

Manually triggers ingestion for specific sources.

**Request Body**:
```json
{
  "source_ids": ["source_techcrunch_001", "source_youtube_api_001"],
  "force": true
}
```

<!-- DIAGRAM NOTE: Add a sequence diagram showing the flow of a content item from ingestion trigger through processing -->

---

## Module 2: Knowledge Graph API

**Base URL**: `http://localhost:8002`  
**Purpose**: Manages entity extraction, resolution, and knowledge graph operations

### POST /api/entities/extract

Extracts entities from provided text content.

**Request Body**:
```json
{
  "content_id": "content_789",
  "text": "Patreon announced a new fund for creators...",
  "metadata": {
    "source": "techcrunch",
    "published_date": "2025-09-08"
  }
}
```

**Response Example**:
```json
{
  "success": true,
  "data": {
    "entities": [
      {
        "text": "Patreon",
        "type": "Platform",
        "confidence": 0.98,
        "resolved_id": "platform_patreon_001",
        "positions": [0, 156, 298]
      },
      {
        "text": "new fund",
        "type": "Grant",
        "confidence": 0.85,
        "resolved_id": null,
        "positions": [23]
      }
    ],
    "relationships": [
      {
        "source": "platform_patreon_001",
        "relationship": "OFFERS",
        "target": "grant_new_001",
        "confidence": 0.80
      }
    ]
  }
}
```

### GET /api/entities/{entity_id}

Retrieves detailed information about a specific entity.

**Response Example**:
```json
{
  "success": true,
  "data": {
    "entity": {
      "id": "platform_patreon_001",
      "type": "Platform",
      "name": "Patreon",
      "attributes": {
        "website": "https://patreon.com",
        "founded_date": "2013-05-01",
        "creator_count": 250000,
        "category": "subscription"
      },
      "relationships": {
        "outgoing": [
          {
            "type": "COMPETES_WITH",
            "target_id": "platform_substack_001",
            "target_name": "Substack"
          }
        ],
        "incoming": [
          {
            "type": "CREATES_ON",
            "source_id": "person_casey_001",
            "source_name": "Casey Neistat"
          }
        ]
      },
      "last_updated": "2025-09-09T08:00:00Z"
    }
  }
}
```

### GET /api/graph/query

Executes graph queries to find patterns and relationships.

**Request Body**:
```json
{
  "query_type": "find_grants",
  "filters": {
    "deadline": "future",
    "amount_min": 10000,
    "location": "USA"
  },
  "limit": 10
}
```

**Response Example**:
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "grant_id": "grant_youtube_001",
        "name": "YouTube Black Voices Fund",
        "amount_range": {
          "min": 25000,
          "max": 100000
        },
        "deadline": "2025-10-15",
        "provider": "YouTube",
        "match_score": 0.92
      }
    ],
    "total_results": 3,
    "query_time_ms": 145
  }
}
```

### POST /api/entities/resolve

Attempts to resolve potential duplicate entities.

**Request Body**:
```json
{
  "entity_1": {
    "name": "YouTube Creator Fund",
    "type": "Grant"
  },
  "entity_2": {
    "name": "YouTube's Creator Fund",
    "type": "Grant"
  }
}
```

---

## Module 3: Reasoning API

**Base URL**: `http://localhost:8003`  
**Purpose**: Provides intelligence layer including content generation, recommendations, and insights

### GET /api/frontier/next

Returns the next items the system should research based on priority and user interests.

**Response Example**:
```json
{
  "success": true,
  "data": {
    "frontier_items": [
      {
        "id": "frontier_001",
        "type": "platform_investigation",
        "target": "BeReal",
        "priority": 0.89,
        "reason": "Rapid growth, creator monetization announced",
        "suggested_actions": [
          "Analyze creator monetization model",
          "Compare with similar platforms",
          "Identify early adopter creators"
        ]
      },
      {
        "id": "frontier_002",
        "type": "grant_deadline",
        "target": "grant_meta_001",
        "priority": 0.85,
        "reason": "Deadline in 7 days, high value, many qualify"
      }
    ]
  }
}
```

### POST /api/digest/generate

Generates a personalized digest for a specific user or topic.

**Request Body**:
```json
{
  "user_id": "user_sarah_001",
  "period": "weekly",
  "topics": ["gaming", "grants", "platform-updates"],
  "format": "email"
}
```

**Response Example**:
```json
{
  "success": true,
  "data": {
    "digest": {
      "id": "digest_001",
      "subject": "Your Weekly Creator Economy Update",
      "sections": [
        {
          "title": "New Opportunities",
          "items": [
            {
              "type": "grant",
              "title": "Gaming Creator Fund Now Open",
              "summary": "Applications open for $50k grants...",
              "action_url": "https://example.com/apply",
              "relevance_score": 0.94
            }
          ]
        },
        {
          "title": "Platform Updates",
          "items": [
            {
              "type": "platform_feature",
              "title": "Twitch Launches New Monetization Tools",
              "summary": "Three new ways to earn from streams...",
              "relevance_score": 0.87
            }
          ]
        }
      ],
      "generated_at": "2025-09-09T10:00:00Z"
    }
  }
}
```

### POST /api/insights/generate

Generates insights based on patterns in the knowledge graph.

**Request Body**:
```json
{
  "insight_type": "trend_analysis",
  "domain": "platform_competition",
  "timeframe": "last_quarter"
}
```

### GET /api/recommendations/{user_id}

Returns personalized recommendations for a specific user.

**Response Example**:
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "type": "grant_opportunity",
        "confidence": 0.91,
        "entity_id": "grant_adobe_001",
        "reason": "Matches your content type and audience size",
        "action": "Apply before September 30"
      },
      {
        "type": "platform_suggestion",
        "confidence": 0.85,
        "entity_id": "platform_beehiiv_001",
        "reason": "Growing platform for newsletter creators",
        "action": "Consider for email list management"
      }
    ]
  }
}
```

---

## Module 4: Frontend API Requirements

Module 4 doesn't expose its own API but consumes APIs from Modules 1-3. Here are the key integration patterns it uses.

### Dashboard Data Aggregation

The frontend aggregates data from all modules to build the dashboard.

```javascript
// Frontend aggregation pattern
async function loadDashboard() {
  const [sources, entities, insights] = await Promise.all([
    fetch('http://localhost:8001/api/sources/stats'),
    fetch('http://localhost:8002/api/entities/recent'),
    fetch('http://localhost:8003/api/insights/latest')
  ]);
  
  return {
    ingestion: await sources.json(),
    knowledge: await entities.json(),
    intelligence: await insights.json()
  };
}
```

### Real-time Updates

The frontend subscribes to Server-Sent Events for real-time updates.

```javascript
// SSE subscription pattern
const events = new EventSource('http://localhost:8001/api/events');

events.addEventListener('new_content', (e) => {
  const content = JSON.parse(e.data);
  updateContentList(content);
});

events.addEventListener('entity_extracted', (e) => {
  const entity = JSON.parse(e.data);
  updateKnowledgeGraph(entity);
});
```

### Search Integration

The frontend provides unified search across all modules.

```javascript
// Unified search pattern
async function search(query) {
  const results = await fetch('http://localhost:8002/api/search', {
    method: 'POST',
    body: JSON.stringify({
      query: query,
      types: ['Platform', 'Grant', 'Person'],
      limit: 20
    })
  });
  
  return results.json();
}
```

---

## Integration Patterns

### Module Communication Flow

The typical flow of data through the system follows this pattern:

1. Module 1 ingests content and notifies Module 2
2. Module 2 extracts entities and updates the knowledge graph
3. Module 3 analyzes changes and generates insights
4. Module 4 displays updates to users

<!-- DIAGRAM NOTE: Add a sequence diagram showing a complete flow from content ingestion to user display -->

### Error Handling

When modules communicate, they should handle errors gracefully.

```python
# Python error handling pattern
import requests
from time import sleep

def call_with_retry(url, data, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=data, timeout=5)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limited
                sleep(2 ** attempt)  # Exponential backoff
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise
            sleep(1)
    return None
```

### Testing APIs

Each module should include API tests that other modules can run.

```bash
# Module 1 health check
curl http://localhost:8001/api/health

# Module 2 health check
curl http://localhost:8002/api/health

# Module 3 health check
curl http://localhost:8003/api/health

# Test full pipeline
./scripts/test_integration.sh
```

---

## Development Guidelines

### API Versioning

APIs should include version information to enable backward compatibility.

```
http://localhost:8001/api/v1/sources
http://localhost:8001/api/v2/sources  # Future version
```

### Documentation

Every endpoint must include:
- Purpose description
- Request parameters with types
- Response format with examples
- Error codes and meanings
- curl command for testing

### Security Considerations

During development, security is simplified. For production:
- Implement proper authentication (OAuth 2.0)
- Add input validation on all endpoints
- Sanitize user-provided content
- Implement CORS properly
- Use HTTPS for all communication
- Add request signing for service-to-service calls

---

## Next Steps

With these API specifications, each module team can:
1. Implement their endpoints according to the specification
2. Create mock responses for early integration testing
3. Build API clients for consuming other modules' services
4. Write integration tests that verify the contracts
5. Document any deviations or extensions needed

Remember that these specifications will evolve during Week 2 planning as teams discover additional requirements. The key is maintaining compatibility at the documented interfaces while allowing flexibility in implementation details.