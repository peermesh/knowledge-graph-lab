# Dependencies and Configuration Checklist

**Date:** October 28, 2025  
**Purpose:** Complete reference for all dependencies, configurations, and environment variables

---

## Backend Dependencies

### Python Packages to Add

#### Phase 1: Authentication
```txt
# requirements.txt additions
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.1
```

#### Phase 2: WebSocket & Real-time
```txt
# Already in requirements.txt but verify:
redis==5.0.1
aioredis==2.0.1
```

#### Phase 3: GraphQL
```txt
strawberry-graphql[fastapi]==0.235.0
strawberry-graphql-django==0.10.0
```

#### Phase 4: Monitoring & Testing
```txt
# Monitoring
prometheus-client==0.19.0
prometheus-fastapi-instrumentator==6.1.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
httpx==0.25.2
faker==20.1.0
locust==2.19.1
```

### Complete requirements.txt
```txt
# src/backend-architecture/requirements.txt

# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.12.1
psycopg2-binary==2.9.9

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.1

# Redis & Caching
redis==5.0.1
aioredis==2.0.1

# GraphQL
strawberry-graphql[fastapi]==0.235.0

# Monitoring
prometheus-client==0.19.0
prometheus-fastapi-instrumentator==6.1.0

# Logging
structlog==23.2.0
python-json-logger==2.0.7

# Message Queue
aio-pika==9.3.1
celery==5.3.4

# Utilities
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
httpx==0.25.2
faker==20.1.0
locust==2.19.1
```

---

## Frontend Dependencies

### npm Packages to Add

#### Phase 1: Authentication
```json
{
  "@tanstack/react-query": "^5.0.0"
}
```

#### Phase 3: GraphQL
```json
{
  "graphql": "^16.8.1",
  "graphql-request": "^6.1.0",
  "@urql/core": "^4.2.0",
  "urql": "^4.0.6"
}
```

#### Phase 4: Testing
```json
{
  "@testing-library/react": "^14.1.2",
  "@testing-library/jest-dom": "^6.1.5",
  "@testing-library/user-event": "^14.5.1",
  "@playwright/test": "^1.40.1",
  "vitest": "^1.0.4",
  "@vitest/ui": "^1.0.4",
  "msw": "^2.0.11"
}
```

### Complete package.json (additions only)
```json
{
  "dependencies": {
    "@tanstack/react-query": "^5.0.0",
    "graphql": "^16.8.1",
    "graphql-request": "^6.1.0",
    "@urql/core": "^4.2.0",
    "urql": "^4.0.6"
  },
  "devDependencies": {
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/user-event": "^14.5.1",
    "@playwright/test": "^1.40.1",
    "vitest": "^1.0.4",
    "@vitest/ui": "^1.0.4",
    "msw": "^2.0.11"
  }
}
```

---

## Environment Variables

### Backend Environment (.env)

```bash
# src/backend-architecture/.env

# Application
APP_NAME="Knowledge Graph Lab - Backend"
VERSION="1.0.0"
DEBUG=true
LOG_LEVEL=INFO
ENVIRONMENT=development

# API
API_V1_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=kglab
POSTGRES_PASSWORD=kglab_password
POSTGRES_DB=knowledge_graph_lab
DATABASE_URL=postgresql+asyncpg://kglab:kglab_password@localhost:5432/knowledge_graph_lab

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_URL=redis://localhost:6379/0

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-change-in-production-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=kglab
RABBITMQ_PASSWORD=kglab_password
RABBITMQ_VHOST=/

# Qdrant Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
LOKI_PORT=3100

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_BURST=20
```

### Frontend Environment (.env)

```bash
# frontend/.env

# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_V1_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_GRAPHQL_URL=http://localhost:8000/graphql

# Environment
VITE_ENV=development
VITE_APP_NAME="Knowledge Graph Lab"
VITE_APP_VERSION=1.0.0

# Features
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_WEBSOCKET=true
VITE_ENABLE_GRAPHQL=true

# Monitoring
VITE_SENTRY_DSN=
```

---

## Docker Compose Configurations

### Main Application Stack

#### File: `src/backend-architecture/docker-compose.yml`
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: kglab-postgres
    environment:
      POSTGRES_USER: kglab
      POSTGRES_PASSWORD: kglab_password
      POSTGRES_DB: knowledge_graph_lab
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U kglab"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  # Redis Cache & Pub/Sub
  redis:
    image: redis:7-alpine
    container_name: kglab-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  # RabbitMQ Message Queue
  rabbitmq:
    image: rabbitmq:3.12-management-alpine
    container_name: kglab-rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: kglab
      RABBITMQ_DEFAULT_PASS: kglab_password
    ports:
      - "5672:5672"   # AMQP
      - "15672:15672" # Management UI
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
  
  # Qdrant Vector Database
  qdrant:
    image: qdrant/qdrant:latest
    container_name: kglab-qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant-data:/qdrant/storage
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 5
  
  # Backend API
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: kglab-backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://kglab:kglab_password@postgres:5432/knowledge_graph_lab
      REDIS_URL: redis://redis:6379/0
      RABBITMQ_URL: amqp://kglab:kglab_password@rabbitmq:5672/
      QDRANT_HOST: qdrant
      QDRANT_PORT: 6333
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres-data:
  redis-data:
  rabbitmq-data:
  qdrant-data:
```

---

### Monitoring Stack

#### File: `src/backend-architecture/docker-compose.monitoring.yml`
```yaml
version: '3.8'

services:
  # Prometheus
  prometheus:
    image: prom/prometheus:v2.48.0
    container_name: kglab-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/alerts.yml:/etc/prometheus/alerts.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'
    restart: unless-stopped
  
  # Grafana
  grafana:
    image: grafana/grafana:10.2.2
    container_name: kglab-grafana
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin
      GF_USERS_ALLOW_SIGN_UP: false
      GF_SERVER_ROOT_URL: http://localhost:3001
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus
      - loki
    restart: unless-stopped
  
  # Loki (Log Aggregation)
  loki:
    image: grafana/loki:2.9.3
    container_name: kglab-loki
    ports:
      - "3100:3100"
    volumes:
      - ./loki/loki-config.yml:/etc/loki/local-config.yaml
      - loki-data:/loki
    command: -config.file=/etc/loki/local-config.yaml
    restart: unless-stopped
  
  # Promtail (Log Collector)
  promtail:
    image: grafana/promtail:2.9.3
    container_name: kglab-promtail
    volumes:
      - ./promtail/promtail-config.yml:/etc/promtail/config.yml
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: -config.file=/etc/promtail/config.yml
    depends_on:
      - loki
    restart: unless-stopped
  
  # Node Exporter (System Metrics)
  node-exporter:
    image: prom/node-exporter:v1.7.0
    container_name: kglab-node-exporter
    ports:
      - "9100:9100"
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:
  loki-data:

networks:
  default:
    name: kglab-monitoring
```

---

## Configuration Files

### Prometheus Configuration

#### File: `src/backend-architecture/prometheus/prometheus.yml`
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'knowledge-graph-lab'
    environment: 'development'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets: []

# Load rules once and periodically evaluate them
rule_files:
  - "alerts.yml"

# Scrape configurations
scrape_configs:
  # Backend API metrics
  - job_name: 'backend-api'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
  
  # Node Exporter (system metrics)
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
  
  # PostgreSQL Exporter (if added)
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
  
  # Redis Exporter (if added)
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

---

### Loki Configuration

#### File: `src/backend-architecture/loki/loki-config.yml`
```yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

limits_config:
  retention_period: 744h  # 31 days
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h

compactor:
  working_directory: /loki/compactor
  shared_store: filesystem
  retention_enabled: true
  retention_delete_delay: 2h
```

---

### Promtail Configuration

#### File: `src/backend-architecture/promtail/promtail-config.yml`
```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # Backend application logs
  - job_name: backend
    static_configs:
      - targets:
          - localhost
        labels:
          job: backend-api
          environment: development
          __path__: /var/log/backend/*.log
  
  # Docker container logs
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
      - source_labels: ['__meta_docker_container_log_stream']
        target_label: 'stream'
```

---

## Database Initialization

### Alembic Configuration

#### File: `src/backend-architecture/alembic.ini` (ensure these settings)
```ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

sqlalchemy.url = postgresql+asyncpg://kglab:kglab_password@localhost:5432/knowledge_graph_lab

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

---

## Installation Commands

### Backend Setup
```bash
# Navigate to backend directory
cd src/backend-architecture

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed database (after seed scripts are created)
python -m app.db.seeds.run_seeds

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Docker Setup
```bash
# Start all services
docker-compose up -d

# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down
```

---

## Testing Commands

### Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_auth.py

# Run integration tests
pytest tests/integration/

# Run load tests
locust -f tests/load/locustfile.py
```

### Frontend Tests
```bash
# Run unit tests
npm run test

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e

# Run tests in watch mode
npm run test:watch
```

---

## Port Reference

| Service | Port | URL |
|---------|------|-----|
| Frontend Dev Server | 5173 | http://localhost:5173 |
| Backend API | 8000 | http://localhost:8000 |
| API Docs (Swagger) | 8000 | http://localhost:8000/docs |
| PostgreSQL | 5432 | postgresql://localhost:5432 |
| Redis | 6379 | redis://localhost:6379 |
| RabbitMQ Management | 15672 | http://localhost:15672 |
| Qdrant | 6333 | http://localhost:6333 |
| Prometheus | 9090 | http://localhost:9090 |
| Grafana | 3001 | http://localhost:3001 |
| Loki | 3100 | http://localhost:3100 |

---

## Security Checklist

### Before Production Deployment:

- [ ] Change default JWT_SECRET_KEY to random 32+ character string
- [ ] Change default database passwords
- [ ] Change default Grafana admin password
- [ ] Enable HTTPS/TLS for all services
- [ ] Configure proper CORS origins (remove localhost)
- [ ] Enable rate limiting on auth endpoints
- [ ] Set up firewall rules
- [ ] Enable database encryption at rest
- [ ] Configure backup strategy
- [ ] Set up SSL certificates
- [ ] Enable audit logging
- [ ] Configure security headers (HSTS, CSP, etc.)
- [ ] Run security vulnerability scan
- [ ] Review and lock down API permissions

---

**This checklist ensures all dependencies and configurations are properly set up before beginning implementation.**

