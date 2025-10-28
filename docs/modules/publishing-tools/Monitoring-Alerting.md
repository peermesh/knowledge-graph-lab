# Publishing Module - Monitoring and Alerting

## Overview

Comprehensive monitoring and alerting setup for the Publishing Module to ensure production reliability and performance.

## Metrics Collection

### Prometheus Integration

**Metrics Endpoint**: `/metrics` (to be implemented)

Key metrics categories:
- **Request Metrics**: HTTP request rate, latency (p50/p95/p99), error rates
- **Business Metrics**: Publications created, newsletters sent, alerts delivered
- **Database Metrics**: Connection pool usage, query latency, transaction rates
- **Cache Metrics**: Redis hit/miss ratio, connection pool, memory usage
- **Worker Metrics**: Celery queue depth, task execution time, failure rates

### Application Metrics

```python
# Example metrics (to be implemented in src/publishing/core/metrics.py)
from prometheus_client import Counter, Histogram, Gauge

publications_created = Counter('publishing_publications_created_total', 'Publications created', ['type'])
newsletters_sent = Counter('publishing_newsletters_sent_total', 'Newsletters sent successfully')
api_latency = Histogram('publishing_api_latency_seconds', 'API endpoint latency', ['endpoint'])
active_subscribers = Gauge('publishing_active_subscribers', 'Number of active subscribers')
queue_depth = Gauge('publishing_queue_depth', 'Celery queue depth', ['queue'])
```

## Structured Logging

### Current Implementation

Located in: `src/publishing/core/logging.py`

- JSON-formatted logs with correlation IDs
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Correlation ID tracking across services
- Request/response logging middleware

### Log Aggregation

**Recommended Stack**: ELK (Elasticsearch, Logstash, Kibana) or Grafana Loki

- Centralized log collection from all containers
- Log parsing and indexing for search
- Log retention: 30 days for INFO, 90 days for ERROR
- Correlation ID tracking for request tracing

### Key Log Events

- Publication creation and status changes
- Channel delivery success/failure
- Authentication failures
- Rate limit violations
- External service errors
- Database connection issues

## Dashboards

### Grafana Dashboards

#### 1. Overview Dashboard

- **Request Rate**: Requests per second by endpoint
- **Error Rate**: 4xx and 5xx errors percentage
- **Latency**: p50/p95/p99 response times
- **Active Subscribers**: Current subscriber count
- **Publications**: Created/completed/failed by type

#### 2. Performance Dashboard

- **API Response Times**: Histogram by endpoint
- **Database Query Performance**: Slow query log, connection pool
- **Cache Performance**: Hit/miss ratio, memory usage
- **Worker Performance**: Queue depth, task execution time

#### 3. Business Metrics Dashboard

- **Newsletter Delivery**: Success rate, volume trends
- **Alert Delivery**: <30 second delivery rate
- **Engagement Metrics**: Open/click rates by channel
- **Subscriber Growth**: New/active/unsubscribed trends

#### 4. Infrastructure Dashboard

- **Container Health**: CPU/memory usage, restarts
- **Database Health**: Connection pool, replication lag
- **Redis Health**: Memory usage, eviction rate
- **External Services**: AWS SES/Slack/Discord API latency

## Alerting Rules

### Critical Alerts (PagerDuty/Slack)

1. **API Availability**
   - Alert if: Error rate > 5% for 5 minutes
   - Severity: Critical
   - Action: Page on-call engineer

2. **Database Down**
   - Alert if: Database connection failures
   - Severity: Critical
   - Action: Page on-call engineer

3. **Worker Queue Backed Up**
   - Alert if: Queue depth > 10,000 for 10 minutes
   - Severity: Critical
   - Action: Scale workers, investigate bottleneck

4. **Alert Delivery SLA Breach**
   - Alert if: >10% of alerts take >30 seconds
   - Severity: High
   - Action: Investigate delivery pipeline

### Warning Alerts (Slack)

1. **High Latency**
   - Alert if: p95 latency > 300ms for 5 minutes
   - Severity: Warning
   - Action: Investigate performance

2. **Cache Hit Ratio Low**
   - Alert if: Redis hit ratio < 70%
   - Severity: Warning
   - Action: Review caching strategy

3. **Channel Delivery Failures**
   - Alert if: >5% delivery failures for any channel
   - Severity: Warning
   - Action: Check external service status

4. **High Memory Usage**
   - Alert if: Container memory > 80% for 10 minutes
   - Severity: Warning
   - Action: Review memory leaks, scale resources

## Health Checks

### Endpoint Implementation

Located in: `src/publishing/api/__init__.py` and `src/publishing/services/health_service.py`

```python
GET /health
Response:
{
  "status": "healthy",
  "timestamp": "2025-10-28T20:00:00Z",
  "version": "1.0.0",
  "uptime_seconds": 3600,
  "database_status": "connected",
  "redis_status": "connected",
  "external_services": {
    "aws_ses": "connected",
    "slack_api": "connected",
    "discord_api": "connected"
  }
}
```

### Kubernetes Probes

- **Liveness Probe**: Basic health check (container running)
- **Readiness Probe**: Full health check (database connectivity, etc.)
- **Startup Probe**: Initial health check with extended timeout

## Distributed Tracing

### OpenTelemetry Integration

**To be implemented**: `src/publishing/core/tracing.py`

- Trace ID propagation across services
- Span creation for database queries, external API calls
- Correlation with logs via trace ID
- Integration with Jaeger or Zipkin for visualization

### Key Traces

- Publication creation → Channel delivery
- Newsletter generation → Personalization → Delivery
- Alert creation → Priority queue → Real-time delivery
- Analytics query → Database → Cache → Response

## SLA Monitoring

### Service Level Objectives (SLOs)

1. **API Availability**: 99.9% uptime
   - Error budget: 43 minutes/month
   - Measurement: % of successful requests

2. **API Latency**: p95 < 150ms
   - Error budget: 5% of requests can exceed
   - Measurement: Response time histogram

3. **Newsletter Delivery**: 99.5% success rate
   - Error budget: 0.5% failed deliveries
   - Measurement: Successful deliveries / total attempts

4. **Alert Delivery**: <30 seconds for 95% of alerts
   - Error budget: 5% can exceed SLA
   - Measurement: Time from creation to delivery

### SLI Dashboards

- Real-time SLI tracking
- Error budget consumption rate
- Historical SLO compliance trends
- Alerting when error budget depleted

## Incident Response

### On-Call Rotation

- Primary and secondary on-call engineers
- PagerDuty integration for critical alerts
- Escalation policy: 5 minutes → 15 minutes → manager
- Post-mortem process for all production incidents

### Runbooks

Located in: `docs/modules/publishing-tools/runbooks/` (to be created)

- Database connection failures
- High API latency investigation
- Worker queue backed up
- External service outages
- Cache performance issues

## Performance Profiling

### Tools

- **py-spy**: CPU profiling for Python applications
- **memory_profiler**: Memory usage profiling
- **pgbadger**: PostgreSQL log analyzer
- **Redis SLOWLOG**: Slow command identification

### Profiling Schedule

- Weekly performance reviews
- Monthly optimization sprints
- Quarterly capacity planning
- Continuous profiling in staging environment

## Cost Monitoring

### Resource Usage Tracking

- Container CPU/memory costs (Kubernetes metrics)
- Database storage and I/O costs
- Redis memory costs
- External service costs (AWS SES, Slack/Discord API)
- Data transfer costs

### Cost Optimization

- Right-sizing container resources
- Database query optimization
- Cache hit ratio improvement
- Worker autoscaling configuration

## Compliance and Audit

### Audit Logs

- All API requests with authentication info
- Data access logs for GDPR compliance
- Configuration changes tracking
- Security events logging

### Compliance Monitoring

- GDPR compliance metrics
- Data retention policy enforcement
- Access control audit trails
- Security vulnerability tracking

## Implementation Checklist

- [ ] Implement Prometheus metrics endpoint
- [ ] Configure Grafana dashboards
- [ ] Set up alerting rules in Prometheus/Alertmanager
- [ ] Integrate with PagerDuty for critical alerts
- [ ] Configure structured logging to ELK/Loki
- [ ] Implement distributed tracing with OpenTelemetry
- [ ] Create runbooks for common incidents
- [ ] Set up SLO tracking dashboards
- [ ] Configure cost monitoring dashboards
- [ ] Establish on-call rotation and escalation policy

## Resources

- Prometheus: https://prometheus.io/
- Grafana: https://grafana.com/
- OpenTelemetry: https://opentelemetry.io/
- PagerDuty: https://www.pagerduty.com/
- Site Reliability Engineering (Google): https://sre.google/

