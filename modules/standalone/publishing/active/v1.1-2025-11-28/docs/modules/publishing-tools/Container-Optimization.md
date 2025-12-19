# Publishing Module - Container Optimization

## Overview

Container optimization strategies for production deployment of the Publishing Module.

## Multi-Stage Build

### Current Dockerfile

Located at repository root: `Dockerfile`

```dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -fsS http://localhost:8080/health || exit 1
CMD ["uvicorn", "src.publishing.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Optimization Opportunities

1. **Multi-stage builds**: Separate build and runtime stages
2. **Distroless images**: Reduce attack surface with minimal runtime
3. **Layer caching**: Optimize COPY order for better cache hits
4. **Security scanning**: Automated vulnerability scanning in CI/CD

## Recommended Production Dockerfile

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY src ./src

# Non-root user for security
RUN useradd -m -u 1000 publishing && chown -R publishing:publishing /app
USER publishing

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -fsS http://localhost:8080/health || exit 1

CMD ["uvicorn", "src.publishing.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
```

## Container Configuration

### Environment Variables

Required for production:
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://host:6379/0
REDIS_POOL_SIZE=10

# Celery
CELERY_BROKER_URL=redis://host:6379/1
CELERY_RESULT_BACKEND=redis://host:6379/2

# AWS SES
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_REGION=us-east-1

# Slack/Discord
SLACK_BOT_TOKEN=xxx
DISCORD_BOT_TOKEN=xxx

# Application
DEBUG=false
LOG_LEVEL=INFO
```

### Resource Limits

Kubernetes deployment:
```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

### Health Checks

- **Liveness probe**: GET `/health` (30s interval)
- **Readiness probe**: GET `/health` with database connectivity check
- **Startup probe**: GET `/health` (60s timeout for initialization)

## Image Optimization

### Size Reduction

- Current image size: ~400MB (python:3.11-slim base)
- Optimized target: ~200MB (multi-stage with distroless)
- Remove unnecessary packages
- Use `.dockerignore` to exclude test files and docs

### Security Hardening

- Run as non-root user (UID 1000)
- Read-only root filesystem
- Drop unnecessary capabilities
- Use distroless or alpine base for minimal attack surface
- Automated vulnerability scanning with Trivy/Snyk

## Docker Compose for Development

Located at: `docker-compose.yml` (if exists)

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DEBUG=true
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/publishing
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=publishing
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
  
  worker:
    build: .
    command: celery -A src.publishing.workers.celery_app worker --loglevel=info
    environment:
      - DEBUG=true
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/publishing
      - CELERY_BROKER_URL=redis://redis:6379/1
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  redis_data:
```

## CI/CD Integration

### Build Pipeline

1. **Lint and test**: Run pytest with coverage
2. **Build image**: Multi-stage Docker build
3. **Security scan**: Trivy/Snyk vulnerability scanning
4. **Push to registry**: Tag with commit SHA and version
5. **Deploy**: Rolling update to Kubernetes cluster

### Image Tagging Strategy

- `latest`: Latest production release
- `v1.0.0`: Semantic version tags
- `sha-abc123`: Git commit SHA for traceability
- `dev`: Development builds

## Production Deployment

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: publishing-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: publishing-api
  template:
    metadata:
      labels:
        app: publishing-api
    spec:
      containers:
      - name: api
        image: registry.example.com/publishing-api:v1.0.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: publishing-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
```

### Horizontal Pod Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: publishing-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: publishing-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Monitoring

### Container Metrics

- CPU usage
- Memory usage
- Network I/O
- Disk I/O
- Container restart count

### Application Metrics

- Request rate and latency
- Database connection pool usage
- Redis cache hit/miss ratio
- Celery queue depth
- Error rates by endpoint

## Backup and Recovery

- Database backups: Automated daily snapshots
- Redis persistence: RDB snapshots + AOF logs
- Disaster recovery: Multi-region replication
- RTO: < 1 hour, RPO: < 5 minutes

## Notes

- Current implementation uses DEBUG mode with in-memory stores
- Production requires PostgreSQL, Redis, and Celery infrastructure
- Container optimization assumes standard Kubernetes deployment
- Security hardening follows OWASP container security best practices

