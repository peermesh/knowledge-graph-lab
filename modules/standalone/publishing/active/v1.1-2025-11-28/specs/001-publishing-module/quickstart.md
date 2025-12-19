# Publishing Module - Quickstart Guide

**Feature**: Publishing Module
**Created**: 2025-10-23
**Status**: Ready for Development

## Overview

The Publishing Module enables multi-channel content delivery with AI-powered personalization and comprehensive analytics. It transforms research insights into personalized newsletters, alerts, and digests delivered through email, Slack, Discord, and webhook channels.

## Integration Scenarios

### Scenario 1: Newsletter Publishing Workflow

**Context**: Content creator wants to publish 5 research insights to 2,000 subscribers

```python
# 1. Create publication with content selection
publication_data = {
    "content_ids": ["uuid1", "uuid2", "uuid3", "uuid4", "uuid5"],
    "channels": ["email-channel-uuid", "slack-channel-uuid"],
    "publication_type": "newsletter",
    "scheduled_time": "2025-10-24T09:00:00Z"
}

# Note: Authentication handled by Backend module JWT system
headers = {"Authorization": "Bearer your-jwt-token"}

response = requests.post("/api/v1/publications", json=publication_data, headers=headers)
publication_data = response.json()["data"]
publication_id = publication_data["id"]

# 2. Monitor publication status
status_response = requests.get(f"/api/v1/publications/{publication_id}", headers=headers)
status_data = status_response.json()["data"]
print(f"Status: {status_data['status']}")
print(f"Channel Results: {status_data['channel_results']}")
```

**Expected Results**:
- Newsletter delivered to 2,000 subscribers within 2 minutes of scheduled time
- Email and Slack channels both receive formatted content
- Personalization applied based on user interests and engagement history
- Real-time engagement tracking begins immediately

---

### Scenario 2: Real-Time Alert Distribution

**Context**: High-priority AI research breakthrough needs immediate distribution

```python
# 1. Configure alert for high-priority content
subscriber_data = {
    "email": "researcher@university.edu",
    "topic_interests": {"artificial_intelligence": 0.95, "machine_learning": 0.88},
    "preferred_channels": ["email", "slack", "discord"],
    "frequency_settings": {
        "alerts": "real-time",
        "newsletter": "daily"
    }
}

headers = {"Authorization": "Bearer your-jwt-token"}
subscriber_response = requests.post("/api/v1/subscribers", json=subscriber_data, headers=headers)
subscriber_data = subscriber_response.json()["data"]
subscriber_id = subscriber_data["id"]

# 2. Publish high-priority alert
alert_data = {
    "content_ids": ["breakthrough-article-uuid"],
    "channels": ["email-channel-uuid", "slack-channel-uuid", "discord-channel-uuid"],
    "publication_type": "alert",
    "personalization_rules": {"priority_threshold": 0.9}
}

alert_response = requests.post("/api/v1/publications", json=alert_data, headers=headers)
alert_data = alert_response.json()["data"]
alert_id = alert_data["id"]
```

**Expected Results**:
- Alert delivered to all configured channels within 30 seconds
- Content personalized based on researcher's specific AI/ML interests
- Engagement tracking captures immediate response metrics
- No duplicate alerts sent for same content

---

### Scenario 3: Channel Configuration and Testing

**Context**: Setting up new Slack workspace for team communications

```python
# 1. Configure Slack channel
slack_config = {
    "name": "AI Research Team",
    "channel_type": "slack",
    "configuration": {
        "bot_token": "xoxb-your-bot-token",
        "channel_id": "#ai-research",
        "workspace_name": "Knowledge Graph Lab"
    },
    "is_active": True
}

headers = {"Authorization": "Bearer your-jwt-token"}
channel_response = requests.post("/api/v1/channels", json=slack_config, headers=headers)
channel_data = channel_response.json()["data"]
channel_id = channel_data["id"]

# 2. Test channel configuration
test_response = requests.post(f"/api/v1/channels/{channel_id}/test", headers=headers)
test_data = test_response.json()["data"]
print(f"Test Status: {test_data['success']}")
print(f"Message: {test_data['message']}")
```

**Expected Results**:
- Slack channel configured successfully with bot authentication
- Test message delivered to #ai-research channel
- Channel status shows active and ready for publishing
- Error details provided if configuration issues exist

---

### Scenario 4: Analytics and Optimization

**Context**: Content strategist analyzing publishing performance and optimizing delivery

```python
# 1. Retrieve engagement analytics
analytics_params = {
    "start_date": "2025-10-17",
    "end_date": "2025-10-23",
    "channel_type": "email",
    "metric_type": "open",
    "group_by": "day"
}

headers = {"Authorization": "Bearer your-jwt-token"}
analytics_response = requests.get("/api/v1/analytics/engagement", params=analytics_params, headers=headers)
analytics_data = analytics_response.json()["data"]
print(f"Open Rates: {analytics_data['summary']}")

# 2. Get performance recommendations
perf_response = requests.get("/api/v1/analytics/performance",
                           params={"start_date": "2025-10-17", "end_date": "2025-10-23"},
                           headers=headers)
perf_data = perf_response.json()["data"]
recommendations = perf_data["recommendations"]

for rec in recommendations:
    print(f"Priority: {rec['priority']}, Type: {rec['type']}")
    print(f"Description: {rec['description']}")
    print(f"Expected Impact: {rec['expected_impact']}")
```

**Expected Results**:
- Comprehensive engagement metrics across all channels
- Performance trends analysis with actionable insights
- Specific recommendations for timing and content optimization
- Channel-specific performance comparisons

## API Authentication

All API requests require JWT authentication managed by the **Backend module**:

```python
headers = {
    "Authorization": "Bearer your-jwt-token",  # Obtained from Backend module auth system
    "Content-Type": "application/json"
}
```

**Authentication Flow:**
1. Authenticate with Backend module to obtain JWT token
2. Use token in Authorization header for all Publishing module requests
3. Backend module manages user roles: `user`, `admin`, `moderator`

## Error Handling

**Common HTTP Status Codes**:
- `201`: Resource created successfully
- `200`: Request processed successfully
- `400`: Invalid request data or parameters
- `401`: Authentication required or invalid
- `404`: Resource not found
- `409`: Resource conflict (duplicate, invalid state)
- `500`: Internal server error

**Error Response Format (RFC7807 Problem Details)**:
```json
{
    "data": {},
    "meta": {
        "timestamp": "2025-10-23T14:30:00Z",
        "request_id": "req-12345"
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

## Rate Limiting

- **Standard endpoints**: 1000 requests/minute
- **Analytics endpoints**: 100 requests/minute
- **Channel testing**: 10 requests/minute per channel

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1634567890
```

## Webhook Integration Example

For custom channel integrations:

```python
# Webhook payload format
webhook_payload = {
    "content_id": "uuid-of-published-content",
    "publication_id": "uuid-of-publication",
    "channel_type": "webhook",
    "delivered_at": "2025-10-23T14:30:00Z",
    "personalization": {
        "user_interests": ["artificial_intelligence", "machine_learning"],
        "content_score": 0.94
    },
    "engagement_url": "https://api.knowledge-graph-lab.com/track/click/{tracking_id}"
}
```

## Performance Benchmarks

**Response Times** (p95):
- Publication creation: <150ms
- Content personalization: <200ms
- Newsletter generation: <5 seconds for 100 articles
- Analytics queries: <500ms
- Real-time alerts: <30 seconds end-to-end

**Throughput**:
- Newsletter publishing: 1,000 subscribers/minute
- Real-time alerts: 500 alerts/second
- Engagement tracking: 10,000 events/second
- Analytics queries: 100 complex queries/second

## Monitoring and Alerts

**Health Check Endpoints**:
- `GET /health`: Overall service health (container orchestration)
- `GET /metrics`: Prometheus metrics (if configured)
- `GET /api/v1/channels/{id}/status`: Channel connectivity

**Health Check Response Format**:
```json
{
    "data": {
        "status": "healthy",
        "timestamp": "2025-10-23T14:30:00Z",
        "version": "1.0.0",
        "uptime_seconds": 3600,
        "database_status": "connected",
        "external_services": {
            "aws_ses": "connected",
            "slack_api": "connected",
            "discord_api": "connected"
        }
    },
    "meta": {
        "timestamp": "2025-10-23T14:30:00Z",
        "request_id": "req-health-123"
    },
    "errors": []
}
```

**Alert Conditions**:
- Channel delivery success rate <95%
- Publication queue depth >1000
- Average response time >500ms
- External service integration failures

## Support and Troubleshooting

**Common Issues**:
1. **Channel configuration errors**: Verify API credentials and permissions
2. **Personalization failures**: Check AI module availability and content quality scores
3. **Delivery delays**: Monitor external service status and rate limits
4. **Analytics discrepancies**: Verify timezone settings and engagement tracking

**Debugging Tools**:
- Publication status API for delivery tracking
- Channel test endpoints for configuration validation
- Analytics API for performance monitoring
- Structured logging with correlation IDs

**Getting Help**:
- Check API documentation at `/docs`
- Review error logs in admin dashboard
- Contact publishing module team for integration issues
- Monitor system status at `status.knowledge-graph-lab.com`
