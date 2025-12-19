# Publishing Module - API Documentation

## Overview

Complete API documentation for the Publishing Module, including endpoints, request/response formats, authentication, and examples.

## OpenAPI Specification

**Location**: `specs/001-publishing-module/contracts/api-spec.yaml`

- **Format**: OpenAPI 3.0.3
- **Version**: 1.0.0
- **Interactive Documentation**: Available at `/docs` (FastAPI auto-generated)
- **ReDoc**: Available at `/redoc` (alternative documentation UI)

## Base URLs

- **Production**: `https://api.knowledge-graph-lab.com/v1/publishing`
- **Staging**: `https://staging-api.knowledge-graph-lab.com/v1/publishing`
- **Development**: `http://localhost:8080/api/v1`

## Authentication

All API endpoints require JWT bearer token authentication (except `/health`).

```http
Authorization: Bearer {jwt_token}
```

**Token Acquisition**: Tokens issued by Backend module authentication system.

**Roles**:
- `user`: Standard access to publications and subscriptions
- `admin`: Full access including channel configuration
- `moderator`: Content management and moderation

## Core Endpoints

### Health Check

```http
GET /health
```

**Response**: Service health status

```json
{
  "data": {
    "status": "healthy",
    "timestamp": "2025-10-28T20:00:00Z",
    "version": "1.0.0",
    "uptime_seconds": 3600,
    "database_status": "connected",
    "external_services": {
      "aws_ses": "connected",
      "slack_api": "connected",
      "discord_api": "connected"
    }
  }
}
```

### Publications

#### Create Publication

```http
POST /publications
Content-Type: application/json
Authorization: Bearer {token}

{
  "content_ids": ["uuid1", "uuid2"],
  "channels": ["channel-uuid"],
  "publication_type": "newsletter",
  "scheduled_time": "2025-10-29T09:00:00Z"
}
```

**Response** (201 Created):

```json
{
  "data": {
    "id": "pub-uuid",
    "content_ids": ["uuid1", "uuid2"],
    "channels": ["channel-uuid"],
    "publication_type": "newsletter",
    "scheduled_time": "2025-10-29T09:00:00Z",
    "status": "scheduled",
    "created_at": "2025-10-28T20:00:00Z"
  },
  "meta": {
    "timestamp": "2025-10-28T20:00:00Z",
    "request_id": "req-uuid"
  },
  "errors": []
}
```

#### Schedule Newsletter

```http
POST /publications/newsletter/schedule
Content-Type: application/json
Authorization: Bearer {token}

{
  "content_ids": ["uuid1", "uuid2"],
  "channels": ["channel-uuid"],
  "scheduled_time": "2025-10-29T09:00:00Z",
  "publication_type": "newsletter"
}
```

**Notes**: Timezone-aware scheduling with UTC normalization (T049).

#### List Publications

```http
GET /publications?status=scheduled&limit=20&offset=0
Authorization: Bearer {token}
```

#### Get Publication

```http
GET /publications/{id}
Authorization: Bearer {token}
```

### Subscribers

#### Create Subscriber

```http
POST /subscribers
Content-Type: application/json
Authorization: Bearer {token}

{
  "email": "user@example.com",
  "preferred_channels": ["email", "slack"],
  "topic_interests": {
    "artificial_intelligence": 0.9,
    "machine_learning": 0.8
  },
  "frequency_settings": {
    "newsletter": "daily",
    "alerts": "real-time"
  }
}
```

#### List Subscribers

```http
GET /subscribers?status=active&limit=20&offset=0
Authorization: Bearer {token}
```

#### Get Subscriber

```http
GET /subscribers/{id}
Authorization: Bearer {token}
```

#### Update Subscriber

```http
PUT /subscribers/{id}
Content-Type: application/json
Authorization: Bearer {token}

{
  "topic_interests": {
    "artificial_intelligence": 0.95
  },
  "subscription_status": "active"
}
```

### Channels

#### Create Channel

```http
POST /channels
Content-Type: application/json
Authorization: Bearer {token}

{
  "name": "AI Research Team Slack",
  "channel_type": "slack",
  "configuration": {
    "bot_token": "xoxb-...",
    "channel_id": "#ai-research"
  },
  "is_active": true
}
```

#### Test Channel

```http
POST /channels/{id}/test
Authorization: Bearer {token}
```

**Response**:

```json
{
  "success": true,
  "message": "Test message delivered successfully",
  "delivered_at": "2025-10-28T20:00:00Z"
}
```

### Analytics

#### Get Engagement Metrics

```http
GET /analytics/engagement?start_date=2025-10-01&end_date=2025-10-31&channel_type=email
Authorization: Bearer {token}
```

**Response**:

```json
{
  "data": {
    "summary": {
      "pub-uuid-1": {"open": 150, "click": 45},
      "pub-uuid-2": {"open": 200, "click": 60}
    },
    "totals": {
      "open": 350,
      "click": 105
    }
  }
}
```

#### Track Open Event

```http
POST /analytics/engagement/track/open?publication_id=pub-uuid&user_id=user-uuid
Authorization: Bearer {token}
```

**Response** (T050 implementation):

```json
{
  "data": {
    "tracked": true,
    "type": "open",
    "publication_id": "pub-uuid"
  }
}
```

#### Track Click Event

```http
POST /analytics/engagement/track/click?publication_id=pub-uuid&url=https://example.com&user_id=user-uuid
Authorization: Bearer {token}
```

#### Get Performance Analytics

```http
GET /analytics/performance?start_date=2025-10-01&end_date=2025-10-31
Authorization: Bearer {token}
```

### Alerts

#### Create Alert

```http
POST /alerts
Content-Type: application/json
Authorization: Bearer {token}

{
  "content_id": "content-uuid",
  "priority": "high",
  "channels": ["channel-uuid-1", "channel-uuid-2"]
}
```

## Error Responses

All errors follow RFC7807 Problem Details format:

```json
{
  "data": {},
  "meta": {
    "timestamp": "2025-10-28T20:00:00Z",
    "request_id": "req-uuid"
  },
  "errors": [{
    "type": "https://api.knowledge-graph-lab.com/errors/validation-error",
    "title": "Validation Error",
    "status": 400,
    "detail": "Invalid channel configuration provided",
    "instance": "/api/v1/channels"
  }]
}
```

### Common Status Codes

- **200**: Success
- **201**: Created
- **204**: No Content (deletion)
- **400**: Bad Request (validation error)
- **401**: Unauthorized (authentication required)
- **404**: Not Found
- **409**: Conflict (duplicate resource)
- **422**: Unprocessable Entity (schema validation)
- **500**: Internal Server Error

## Rate Limiting

- **Standard Endpoints**: 1,000 requests/minute per user
- **Analytics Endpoints**: 100 requests/minute per user
- **Channel Testing**: 10 requests/minute per channel

**Rate Limit Headers**:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1634567890
```

## Request/Response Format

### Standard Response Structure

```json
{
  "data": {
    // Response payload
  },
  "meta": {
    "timestamp": "ISO-8601 datetime",
    "request_id": "correlation-id"
  },
  "errors": [
    // Array of error objects (empty if success)
  ]
}
```

### Pagination

```http
GET /publications?limit=20&offset=40
```

**Response includes**:
- `total_count`: Total number of resources
- `limit`: Page size
- `offset`: Starting position

## Validation Rules

### UUIDs

All ID fields must be valid UUID v4 format.

### Email Addresses

Email validation follows RFC 5322 standard.

### Dates

All timestamps in ISO-8601 format with UTC timezone.

### Content Limits

- Max publications per request: 100
- Max channels per publication: 10
- Max articles per newsletter: 50

## WebSocket Endpoints

### Real-Time Updates

```http
ws://localhost:8080/ws/updates
Authorization: Bearer {token}
```

**Message Format**:

```json
{
  "event": "publication.completed",
  "publication_id": "pub-uuid",
  "timestamp": "2025-10-28T20:00:00Z",
  "data": {
    "status": "completed",
    "channel_results": {}
  }
}
```

## Code Examples

### Python

```python
import requests

headers = {
    "Authorization": "Bearer your-jwt-token",
    "Content-Type": "application/json"
}

# Create publication
response = requests.post(
    "http://localhost:8080/api/v1/publications",
    headers=headers,
    json={
        "content_ids": ["uuid1", "uuid2"],
        "channels": ["channel-uuid"],
        "publication_type": "newsletter"
    }
)

print(response.json())
```

### cURL

```bash
curl -X POST http://localhost:8080/api/v1/publications \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "content_ids": ["uuid1", "uuid2"],
    "channels": ["channel-uuid"],
    "publication_type": "newsletter"
  }'
```

### JavaScript

```javascript
const response = await fetch('http://localhost:8080/api/v1/publications', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your-jwt-token',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    content_ids: ['uuid1', 'uuid2'],
    channels: ['channel-uuid'],
    publication_type: 'newsletter'
  })
});

const data = await response.json();
console.log(data);
```

## Testing

### Interactive API Testing

1. Start development server: `uvicorn src.publishing.main:app --reload`
2. Open browser: http://localhost:8080/docs
3. Click "Authorize" and enter JWT token
4. Try out endpoints interactively

### Contract Tests

Located in: `tests/publishing/contract/`

- `test_publications.py`: Publication endpoints
- `test_subscribers.py`: Subscriber endpoints
- `test_channels.py`: Channel endpoints
- `test_analytics.py`: Analytics endpoints (skipped)

## Production Notes

- DEBUG mode uses in-memory stores for testing
- Production requires PostgreSQL, Redis, and Celery
- All timestamps are UTC-normalized (T049)
- Engagement tracking in-memory for DEBUG (T050)

## Resources

- **OpenAPI Spec**: `specs/001-publishing-module/contracts/api-spec.yaml`
- **Interactive Docs**: http://localhost:8080/docs (FastAPI)
- **ReDoc**: http://localhost:8080/redoc (alternative UI)
- **Quickstart Guide**: `specs/001-publishing-module/quickstart.md`
- **API Endpoints Summary**: `docs/modules/publishing-tools/API-Endpoints.md`

## Validation

✅ OpenAPI spec validated against OpenAPI 3.0.3 standard
✅ All endpoints documented with request/response schemas
✅ Authentication and rate limiting documented
✅ Error formats follow RFC7807 standard
✅ Examples provided for common use cases

