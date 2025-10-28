# Publishing Module - Load Testing

## Overview

Load testing strategy and scenarios for validating the Publishing Module at 100,000+ subscriber scale.

## Testing Goals

- Validate throughput: 1,000 newsletters/minute
- Verify latency: API p95 < 150ms
- Confirm scalability: Support 100,000+ active subscribers
- Test failure scenarios: Circuit breakers, rate limiting
- Measure resource usage: CPU, memory, database connections

## Testing Tools

### Locust

**Installation**:
```bash
pip install locust
```

**Location**: `tests/publishing/performance/locustfile.py` (to be implemented)

### k6

**Installation**:
```bash
# macOS
brew install k6

# Docker
docker pull grafana/k6
```

**Location**: `tests/publishing/performance/k6_test.js` (to be implemented)

## Load Test Scenarios

### Scenario 1: Newsletter Generation at Scale

**Goal**: Generate 1,000 newsletters/minute for 2,000 subscribers each

```python
# locustfile.py
from locust import HttpUser, task, between

class NewsletterUser(HttpUser):
    wait_time = between(1, 2)
    
    def on_start(self):
        # Authenticate
        response = self.client.post("/auth/login", json={
            "username": "test@example.com",
            "password": "password"
        })
        self.token = response.json()["token"]
    
    @task
    def schedule_newsletter(self):
        self.client.post("/api/v1/publications/newsletter/schedule",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "content_ids": ["uuid1", "uuid2", "uuid3"],
                "channels": ["channel-uuid"],
                "scheduled_time": "2025-10-29T09:00:00Z"
            }
        )
```

**Run**:
```bash
locust -f tests/publishing/performance/locustfile.py --host http://localhost:8080 --users 100 --spawn-rate 10
```

### Scenario 2: Real-Time Alert Distribution

**Goal**: Deliver 500 alerts/second with <30 second latency

```javascript
// k6_test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '1m', target: 100 },  // Ramp up
    { duration: '5m', target: 500 },  // Peak load
    { duration: '1m', target: 0 },    // Ramp down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<150'],  // 95% under 150ms
    'http_req_failed': ['rate<0.01'],    // Error rate < 1%
  }
};

export default function () {
  const payload = JSON.stringify({
    content_id: 'alert-uuid',
    priority: 'high',
    channels: ['channel-uuid']
  });
  
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  };
  
  let response = http.post('http://localhost:8080/api/v1/alerts', payload, params);
  
  check(response, {
    'status is 201': (r) => r.status === 201,
    'response time < 150ms': (r) => r.timings.duration < 150,
  });
  
  sleep(1);
}
```

**Run**:
```bash
k6 run tests/publishing/performance/k6_test.js
```

### Scenario 3: Concurrent Publication Management

**Goal**: 100,000 subscribers updating preferences simultaneously

```python
@task(3)
def create_publication(self):
    self.client.post("/api/v1/publications",
        headers={"Authorization": f"Bearer {self.token}"},
        json={
            "content_ids": ["uuid1", "uuid2"],
            "channels": ["channel-uuid"],
            "publication_type": "newsletter"
        }
    )

@task(2)
def list_publications(self):
    self.client.get("/api/v1/publications?limit=20",
        headers={"Authorization": f"Bearer {self.token}"}
    )

@task(1)
def get_publication(self):
    self.client.get(f"/api/v1/publications/{self.publication_id}",
        headers={"Authorization": f"Bearer {self.token}"}
    )
```

### Scenario 4: Analytics Query Load

**Goal**: 100 complex analytics queries/second

```python
@task
def get_engagement_analytics(self):
    self.client.get("/api/v1/analytics/engagement?" + 
        "start_date=2025-10-01&end_date=2025-10-31&channel_type=email",
        headers={"Authorization": f"Bearer {self.token}"}
    )

@task
def get_performance_analytics(self):
    self.client.get("/api/v1/analytics/performance?" +
        "start_date=2025-10-01&end_date=2025-10-31",
        headers={"Authorization": f"Bearer {self.token}"}
    )
```

## Test Execution

### Local Testing

```bash
# 1. Start local services
docker-compose up -d db redis

# 2. Start API server
uvicorn src.publishing.main:app --host 0.0.0.0 --port 8080 --workers 4

# 3. Run load test
locust -f tests/publishing/performance/locustfile.py --host http://localhost:8080 --users 1000 --spawn-rate 100

# 4. Monitor results
open http://localhost:8089
```

### Staging Environment Testing

```bash
# Run against staging environment
locust -f tests/publishing/performance/locustfile.py \
  --host https://staging-api.knowledge-graph-lab.com \
  --users 10000 \
  --spawn-rate 100 \
  --run-time 10m \
  --headless \
  --csv=results/staging_test
```

## Performance Targets

### API Endpoints

| Endpoint | Target p95 | Target p99 | Max RPS |
|----------|-----------|-----------|---------|
| POST /publications | <150ms | <300ms | 100 |
| GET /publications | <100ms | <200ms | 1000 |
| POST /subscribers | <150ms | <300ms | 100 |
| GET /analytics/engagement | <500ms | <1000ms | 100 |
| POST /alerts | <150ms | <300ms | 500 |

### System-Wide Metrics

- **Newsletter Generation**: 1,000/minute (2,000 subscribers each)
- **Alert Delivery**: 500/second with <30 second end-to-end
- **Concurrent Users**: 100,000+ active subscribers
- **Database Connections**: <200 concurrent connections
- **Cache Hit Ratio**: >80% for subscriber preferences
- **Error Rate**: <1% for all endpoints

## Resource Monitoring

### During Load Tests

Monitor the following metrics:

1. **Application Metrics**
   - Request rate and latency distribution
   - Error rate by endpoint
   - Concurrent connections
   - Worker queue depth

2. **Database Metrics**
   - Connection pool usage (should stay <80%)
   - Query execution time
   - Slow query log
   - Transaction rate

3. **Redis Metrics**
   - Memory usage (should stay <80%)
   - Hit/miss ratio (target >80%)
   - Connection count
   - Eviction rate

4. **System Metrics**
   - CPU usage by container
   - Memory usage by container
   - Network I/O
   - Disk I/O

### Monitoring Commands

```bash
# Docker stats
docker stats

# PostgreSQL connections
docker exec -it db psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Redis info
docker exec -it redis redis-cli INFO

# API logs
docker logs -f api

# Worker queue depth
docker exec -it redis redis-cli LLEN celery
```

## Bottleneck Analysis

### Common Bottlenecks

1. **Database Connection Pool Exhausted**
   - Symptom: Timeout errors, high queue depth
   - Solution: Increase pool size, optimize queries
   
2. **Redis Memory Full**
   - Symptom: Evictions, cache misses
   - Solution: Increase memory, adjust TTLs
   
3. **Worker Queue Backed Up**
   - Symptom: Slow newsletter delivery, high queue depth
   - Solution: Scale workers, optimize tasks
   
4. **External Service Rate Limits**
   - Symptom: 429 errors, slow delivery
   - Solution: Implement backoff, request batching

## Optimization Recommendations

Based on load test results:

1. **If API latency exceeds target**:
   - Enable caching for frequently accessed data
   - Optimize database queries (add indexes)
   - Increase connection pool size
   - Scale API containers horizontally

2. **If newsletter generation is slow**:
   - Scale Celery workers
   - Optimize personalization queries
   - Batch database operations
   - Use read replicas for analytics

3. **If alert delivery exceeds 30 seconds**:
   - Optimize priority queue processing
   - Implement connection pooling for external APIs
   - Use async delivery with circuit breakers
   - Scale alert workers separately

## Test Data Generation

### Seed Script

```python
# scripts/seed_test_data.py
import requests
import uuid

BASE_URL = "http://localhost:8080/api/v1"
TOKEN = "test-token"

def create_subscribers(count=100000):
    for i in range(count):
        requests.post(f"{BASE_URL}/subscribers",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={
                "email": f"test{i}@example.com",
                "preferred_channels": ["email"],
                "topic_interests": {
                    "artificial_intelligence": 0.9,
                    "machine_learning": 0.8
                }
            }
        )
        if i % 1000 == 0:
            print(f"Created {i} subscribers")

if __name__ == "__main__":
    create_subscribers(100000)
```

## Results Analysis

### Metrics to Track

1. **Throughput**: Requests per second achieved
2. **Latency**: p50, p95, p99 response times
3. **Error Rate**: % of failed requests
4. **Resource Usage**: CPU, memory, database connections
5. **Scalability**: Performance degradation with increasing load

### Report Format

```markdown
## Load Test Results

**Date**: 2025-10-28
**Environment**: Staging
**Duration**: 10 minutes
**Peak Users**: 10,000

### Results

- **Total Requests**: 500,000
- **Success Rate**: 99.5%
- **Throughput**: 833 req/s
- **Latency p95**: 142ms
- **Latency p99**: 285ms

### Resource Usage

- **API CPU**: 65% average, 85% peak
- **API Memory**: 1.2GB average, 1.8GB peak
- **DB Connections**: 45 average, 78 peak
- **Redis Memory**: 512MB average, 650MB peak

### Bottlenecks Identified

1. Database query optimization needed for analytics endpoints
2. Redis cache hit ratio at 75% (target: 80%)
3. Worker queue backed up during peak load

### Recommendations

1. Add composite index on (user_id, subscription_status)
2. Increase Redis cache TTL for subscriber preferences
3. Scale Celery workers from 4 to 8
```

## CI/CD Integration

### Automated Load Tests

```yaml
# .github/workflows/load-test.yml
name: Load Test

on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday 2 AM
  workflow_dispatch:

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: |
          pip install locust
      
      - name: Run load test
        run: |
          locust -f tests/publishing/performance/locustfile.py \
            --host ${{ secrets.STAGING_URL }} \
            --users 1000 \
            --spawn-rate 100 \
            --run-time 5m \
            --headless \
            --csv=results/weekly_test
      
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: load-test-results
          path: results/
```

## Production Load Testing

**⚠️ WARNING**: Never run full load tests against production

### Gradual Load Increase

```bash
# Stage 1: 10% of target load
locust --users 1000 --spawn-rate 10 --run-time 2m

# Stage 2: 50% of target load
locust --users 5000 --spawn-rate 50 --run-time 5m

# Stage 3: 100% of target load
locust --users 10000 --spawn-rate 100 --run-time 10m
```

### Blue-Green Deployment Testing

1. Deploy new version to green environment
2. Run load tests against green
3. Validate performance meets targets
4. Switch traffic to green
5. Monitor production metrics

## Resources

- Locust Documentation: https://docs.locust.io/
- k6 Documentation: https://k6.io/docs/
- Load Testing Best Practices: https://www.nginx.com/blog/load-testing-best-practices/
- Performance Testing Guide: https://martinfowler.com/bliki/PerformanceTest.html

## Notes

- Current implementation uses DEBUG mode with in-memory stores
- Production load testing requires full PostgreSQL, Redis, Celery infrastructure
- Load tests should be run in isolated staging environment
- Monitor external service rate limits (AWS SES, Slack, Discord)
- Gradual load increase prevents cascading failures

