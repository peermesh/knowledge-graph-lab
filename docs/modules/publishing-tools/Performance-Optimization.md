# Publishing Module - Performance Optimization

## Overview

This document outlines performance optimization strategies for the Publishing Module to meet targets:
- API response: <150ms (p95)
- Newsletter generation: 1,000/minute
- Real-time alerts: <30 seconds end-to-end
- Analytics queries: <500ms

## Caching Strategy

### Redis Cache Configuration

- **Subscriber preferences**: 15-minute TTL with background refresh
- **Content metadata**: 1-hour TTL with cache warming
- **Personalization results**: 5-minute TTL for real-time accuracy
- **Analytics aggregations**: 10-minute TTL with sliding window

### Implementation Notes

- Use `src/publishing/clients/redis_client.py` for cache operations
- Configure TTLs in `src/publishing/core/config.py`
- Implement cache warming for frequently accessed data

## Database Optimization

### Indexing Strategy

- Composite indexes on `user_id + subscription_status + topic_interests`
- Partial indexes on active subscribers and recent publications
- JSONB path indexes for personalization queries
- Partitioning by month for analytics tables

### Query Optimization

- Use async queries with connection pooling (asyncpg)
- Batch operations for bulk newsletter generation
- Read replicas for analytics queries
- Pagination with cursor-based approach for large result sets

## Application-Level Optimization

### Async Processing

- Celery workers for background publication delivery
- Async FastAPI endpoints for non-blocking I/O
- Connection pooling for external services (AWS SES, Slack, Discord)

### Resource Management

- Worker process scaling based on queue depth
- Circuit breakers for external service failures
- Rate limiting to prevent API abuse
- Request batching for analytics aggregation

## Monitoring & Profiling

### Key Metrics

- API endpoint response times (p50, p95, p99)
- Database query execution times
- Cache hit/miss ratios
- Worker queue depths and processing times

### Tools

- Prometheus for metrics collection
- Grafana for visualization
- Structured logging with correlation IDs for tracing
- APM integration for production monitoring

## Load Testing

See `tests/publishing/performance/` for benchmark implementations:
- `test_newsletter_generation.py`: 2,000 subscriber throughput
- `test_alert_delivery_speed.py`: <30 second delivery validation
- `test_analytics_queries.py`: Complex query performance
- `test_benchmarks.py`: Overall system benchmarks

## Future Optimizations

- CDN integration for static assets and templates
- Read replica scaling for analytics workloads
- Message queue optimization for high-volume alerts
- ML model caching for personalization predictions

## Notes

- All performance targets validated in DEBUG mode with in-memory stores
- Production optimization requires actual DB/Redis/Celery infrastructure
- Horizontal scaling via stateless API design and Redis cluster

