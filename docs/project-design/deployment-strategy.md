---
title: "Deployment Strategy"
version: "v1.0"
updated: 2025-09-09
author: "@project-lead"
status: approved
doc_id: "deployment-strategy"
---

# Deployment Strategy

**Status**: Complete - Ready for implementation
**Purpose**: Define the development and deployment approach for the Knowledge Graph Lab
**Audience**: CS students learning production deployment practices

---

## Overview

This document outlines how we deploy the Knowledge Graph Lab from your laptop to production servers. Think of deployment as the bridge between "code that works on my machine" and "code that serves real users reliably."

Deployment isn't just about copying files to a server. It's about ensuring your application runs consistently, scales with demand, recovers from failures, and provides visibility into its behavior. This guide teaches you real-world deployment practices using our four-module system as a concrete example.

---

## Development Environment

### Why Local Development Matters

Before deploying to production, you need a local environment that closely mimics production behavior. This prevents the classic "but it worked on my laptop!" problem. We use Docker to create isolated, reproducible environments that run the same way on every developer's machine.

### Complete Local Development Setup

#### System Requirements

Your development machine needs these minimum specifications:

| Component | Minimum | Recommended | Why It Matters |
| :-------- | :------ | :---------- | :------------- |
| **OS** | Windows 10/11, macOS 10.15+, Ubuntu 20.04+ | Latest stable OS version | Docker support and compatibility |
| **RAM** | 8 GB | 16 GB | Running 4+ containers simultaneously |
| **CPU** | Dual-core 2.0 GHz | Quad-core 2.5 GHz+ | Parallel container execution |
| **Disk Space** | 20 GB free | 50 GB free | Docker images, volumes, and logs |
| **Docker Desktop** | v4.20+ | Latest stable | Critical bug fixes and features |

#### Step 1: Install Docker Desktop

Docker creates lightweight virtual environments (containers) that package your code with all its dependencies. Think of containers as consistent, portable boxes that run your application the same way everywhere.

**For macOS:**
```bash
# Download Docker Desktop from docker.com
# Or use Homebrew (package manager for macOS)
brew install --cask docker
```

**For Windows:**
```bash
# Enable WSL2 first (Windows Subsystem for Linux)
wsl --install

# Then download Docker Desktop from docker.com
# Ensure "Use WSL 2 based engine" is checked during installation
```

**For Ubuntu/Linux:**
```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Step 2: Verify Docker Installation

After installation, verify Docker works correctly:

```bash
# Check Docker version (should show 24.0+)
docker --version

# Verify Docker daemon is running
docker ps

# Test with hello-world container
docker run hello-world
```

If you see "Hello from Docker!" your installation succeeded.

#### Step 3: Configure Environment Variables

Environment variables store configuration that changes between environments (development vs production). Never hardcode sensitive values like API keys directly in code.

Create a `.env` file in your project root:

```bash
# Database Configuration
POSTGRES_HOST=localhost          # Database server address
POSTGRES_PORT=5432               # Standard PostgreSQL port
POSTGRES_DB=knowledge_graph      # Database name
POSTGRES_USER=kg_user            # Database username
POSTGRES_PASSWORD=dev_password   # CHANGE IN PRODUCTION!

# Redis Configuration (for caching and queues)
REDIS_HOST=localhost             # Cache server address
REDIS_PORT=6379                  # Standard Redis port
REDIS_PASSWORD=                  # Optional, set in production

# Application Settings
APP_ENV=development              # Environment (development/staging/production)
DEBUG=true                       # Enable detailed error messages
LOG_LEVEL=DEBUG                  # Logging verbosity (DEBUG/INFO/WARNING/ERROR)

# API Keys (get your own for production)
OPENAI_API_KEY=sk-...            # Your OpenAI key
ANTHROPIC_API_KEY=sk-ant-...     # Your Anthropic key

# Module Ports (for inter-service communication)
MODULE1_PORT=8001                # Data ingestion service
MODULE2_PORT=8002                # Graph construction service  
MODULE3_PORT=8003                # Intelligence service
MODULE4_PORT=8004                # User interface service

# Security (generate new values for production)
SECRET_KEY=dev-secret-key-change-this
JWT_SECRET=jwt-secret-change-this
```

**Security Note**: The `.env` file contains secrets. Add it to `.gitignore` to prevent committing sensitive data:

```bash
echo ".env" >> .gitignore
```

#### Step 4: Set Up Development Workflow

Create this directory structure for organized development:

```
knowledge-graph-lab/
├── docker/                    # Docker configuration
│   ├── docker-compose.yml    # Multi-container orchestration
│   ├── Dockerfile.module1    # Module 1 container definition
│   ├── Dockerfile.module2    # Module 2 container definition
│   ├── Dockerfile.module3    # Module 3 container definition
│   └── Dockerfile.module4    # Module 4 container definition
├── modules/                  # Application code
│   ├── ingestion/           # Module 1: Data ingestion
│   ├── graph/               # Module 2: Graph construction
│   ├── intelligence/        # Module 3: AI reasoning
│   └── interface/           # Module 4: User interface
├── data/                    # Persistent data (not in Git)
│   ├── postgres/           # Database files
│   ├── redis/              # Cache data
│   └── uploads/            # User uploads
├── scripts/                 # Automation scripts
│   ├── setup.sh            # Initial setup script
│   ├── start.sh            # Start all services
│   └── reset.sh            # Reset to clean state
└── .env                    # Environment configuration
```

#### Step 5: Verification Steps

After setup, verify everything works:

```bash
# 1. Check Docker daemon status
docker version

# 2. Verify Docker Compose
docker compose version

# 3. Test environment variables
source .env && echo $POSTGRES_HOST

# 4. Check port availability (nothing should use our ports)
lsof -i :8001-8004  # macOS/Linux
netstat -an | findstr "8001"  # Windows

# 5. Test database connection (after starting services)
docker compose up -d postgres
docker exec -it postgres psql -U kg_user -d knowledge_graph
```

### CI/CD Pipeline
- GitHub Actions for automated testing
- Pre-commit hooks for code quality
- Automated dependency updates
- Branch protection rules

---

## Docker Compose Configuration

### Understanding Docker Compose

Docker Compose orchestrates multiple containers as a single application. Think of it as a conductor coordinating an orchestra - each musician (container) plays their part, but Compose ensures they work together harmoniously.

### Complete docker-compose.yml

Create `docker/docker-compose.yml` with this production-ready configuration:

```yaml
version: '3.9'  # Compose file format version

# Define named networks for isolation
networks:
  frontend:     # User-facing services
    driver: bridge
  backend:      # Internal services
    driver: bridge
  data:         # Database layer
    driver: bridge

# Named volumes for data persistence
volumes:
  postgres_data:    # Database files survive container restart
  redis_data:       # Cache persistence
  minio_data:       # Object storage
  app_logs:         # Centralized logging

services:
  # Module 1: Data Ingestion Service
  ingestion:
    build:
      context: ../modules/ingestion
      dockerfile: ../../docker/Dockerfile.module1
    container_name: kg_ingestion
    ports:
      - "${MODULE1_PORT:-8001}:8000"  # Map to host port
    environment:
      - APP_ENV=${APP_ENV}
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - LOG_LEVEL=${LOG_LEVEL}
    depends_on:
      postgres:
        condition: service_healthy  # Wait for DB to be ready
      redis:
        condition: service_healthy
    networks:
      - backend
      - data
    volumes:
      - ../modules/ingestion:/app:ro  # Read-only code mount
      - app_logs:/app/logs            # Writable log directory
    restart: unless-stopped           # Auto-restart on failure
    healthcheck:                      # Monitor service health
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '1.0'     # CPU limit
          memory: 1G      # Memory limit
        reservations:
          cpus: '0.5'     # Guaranteed CPU
          memory: 512M    # Guaranteed memory

  # Module 2: Graph Construction Service
  graph:
    build:
      context: ../modules/graph
      dockerfile: ../../docker/Dockerfile.module2
    container_name: kg_graph
    ports:
      - "${MODULE2_PORT:-8002}:8000"
    environment:
      - APP_ENV=${APP_ENV}
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=${NEO4J_PASSWORD:-graphpass}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      neo4j:
        condition: service_healthy
      ingestion:
        condition: service_healthy
    networks:
      - backend
      - data
    volumes:
      - ../modules/graph:/app:ro
      - app_logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G

  # Module 3: Intelligence & Reasoning Service
  intelligence:
    build:
      context: ../modules/intelligence
      dockerfile: ../../docker/Dockerfile.module3
    container_name: kg_intelligence
    ports:
      - "${MODULE3_PORT:-8003}:8000"
    environment:
      - APP_ENV=${APP_ENV}
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - GRAPH_SERVICE_URL=http://graph:8000
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/1
    depends_on:
      graph:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend
      - data
    volumes:
      - ../modules/intelligence:/app:ro
      - app_logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 3G
        reservations:
          cpus: '1.0'
          memory: 2G

  # Module 4: User Interface Service
  interface:
    build:
      context: ../modules/interface
      dockerfile: ../../docker/Dockerfile.module4
      args:
        - NODE_ENV=production
    container_name: kg_interface
    ports:
      - "${MODULE4_PORT:-8004}:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=http://intelligence:8000
      - NEXT_PUBLIC_GRAPH_URL=http://graph:8000
    depends_on:
      intelligence:
        condition: service_healthy
    networks:
      - frontend
      - backend
    volumes:
      - app_logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "node", "healthcheck.js"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

  # PostgreSQL Database with pgvector extension
  postgres:
    image: pgvector/pgvector:pg16
    container_name: kg_postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_INITDB_ARGS=--encoding=UTF8
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    networks:
      - data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G

  # Neo4j Graph Database
  neo4j:
    image: neo4j:5-community
    container_name: kg_neo4j
    ports:
      - "7474:7474"  # Web interface
      - "7687:7687"  # Bolt protocol
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD:-graphpass}
      - NEO4J_PLUGINS=["apoc", "graph-data-science"]
      - NEO4J_dbms_memory_pagecache_size=1G
      - NEO4J_dbms_memory_heap_max__size=1G
    volumes:
      - ./neo4j/data:/data
      - ./neo4j/logs:/logs
    networks:
      - data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "${NEO4J_PASSWORD:-graphpass}", "RETURN 1"]
      interval: 30s
      timeout: 10s
      retries: 5

  # Redis Cache & Queue
  redis:
    image: redis:7-alpine
    container_name: kg_redis
    ports:
      - "6379:6379"
    command: >
      redis-server
      --requirepass ${REDIS_PASSWORD:-""}
      --maxmemory 512mb
      --maxmemory-policy allkeys-lru
      --save 60 100
      --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # MinIO Object Storage (S3-compatible)
  minio:
    image: minio/minio:latest
    container_name: kg_minio
    ports:
      - "9000:9000"  # API
      - "9001:9001"  # Console
    environment:
      - MINIO_ROOT_USER=${MINIO_USER:-minioadmin}
      - MINIO_ROOT_PASSWORD=${MINIO_PASSWORD:-minioadmin}
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data
    networks:
      - data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Understanding the Configuration

#### Service Dependencies

Dependencies ensure services start in the correct order. The `depends_on` with `condition: service_healthy` means a service waits until its dependencies pass health checks before starting. This prevents connection errors during startup.

#### Volume Management

Volumes persist data outside containers. When you stop a container, data in volumes remains intact. This is crucial for databases - you don't want to lose data every time you restart.

- **Named volumes**: Managed by Docker, persist between runs
- **Bind mounts**: Link host directories, useful for development

#### Network Configuration

We use three networks to isolate traffic:
- **frontend**: External-facing services
- **backend**: Internal API communication
- **data**: Database connections only

This isolation improves security - a compromised frontend can't directly access databases.

#### Health Checks

Health checks verify services are actually working, not just running. Docker uses these to:
- Determine when a service is ready for traffic
- Restart unhealthy services automatically
- Enable zero-downtime deployments

#### Resource Limits

Resource limits prevent one service from consuming all available memory/CPU. This ensures stability - a memory leak in one module won't crash the entire system.

### Managing the Stack

Common Docker Compose commands for daily development:

```bash
# Start all services (runs in background with -d)
docker compose up -d

# View logs from all services
docker compose logs -f

# View logs from specific service
docker compose logs -f ingestion

# Stop all services (keeps data)
docker compose down

# Stop and remove all data (fresh start)
docker compose down -v

# Restart a specific service
docker compose restart intelligence

# Scale a service (run multiple instances)
docker compose up -d --scale ingestion=3

# Execute command in running container
docker compose exec postgres psql -U kg_user

# View resource usage
docker compose stats

# Update and rebuild services
docker compose build --no-cache
docker compose up -d
```

---

## Demonstration Environment

### Week 10 Demo Setup
- Single server deployment (all modules)
- Docker containers for each module
- Nginx reverse proxy for routing
- SSL certificates for secure access

### Infrastructure Requirements
- Single cloud VM (4 vCPU, 8GB RAM)
- PostgreSQL database (if needed)
- Redis for caching (optional)
- S3-compatible storage for assets

## Deployment Phases

### Phase 1: Local Development (Weeks 1-9)
- Individual module development
- Docker Compose for integration testing
- Mock data for development

### Phase 2: Integration Testing (Week 9)
- Deploy to staging environment
- End-to-end testing
- Performance optimization

### Phase 3: Demo Deployment (Week 10)
- Production deployment
- Monitoring setup
- Demo data population

---

## Production Deployment

### Understanding Production Requirements

Production deployment differs from development in critical ways. In development, crashes are learning opportunities. In production, they affect real users and can damage trust. Production systems must handle unexpected load, recover from failures, and provide visibility into problems.

### Cloud Platform Selection

Each major cloud provider offers different strengths for our knowledge graph system:

| Provider | Best For | Key Services | Estimated Cost/Month |
| :------- | :------- | :----------- | :------------------- |
| **AWS** | Scalability & ecosystem | EC2, RDS, EKS, S3, CloudWatch | $150-300 for small production |
| **Google Cloud** | AI/ML workloads | GKE, Cloud SQL, Vertex AI, BigQuery | $140-280 with sustained use discount |
| **Azure** | Enterprise integration | AKS, Cosmos DB, Cognitive Services | $160-320 with reserved instances |
| **DigitalOcean** | Simplicity & cost | Droplets, Managed K8s, Spaces | $60-150 for starter production |

**Recommendation**: Start with DigitalOcean for simplicity, migrate to AWS/GCP when you need advanced features.

### Security Architecture

Production security requires multiple layers of defense. Think of it like a castle - walls, moat, guards, and internal checkpoints all work together.

#### SSL/TLS Configuration

HTTPS encrypts data in transit, preventing eavesdropping:

```nginx
# nginx.conf for SSL termination
server {
    listen 443 ssl http2;
    server_name knowledgegraph.example.com;
    
    # Certificate from Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/knowledgegraph.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/knowledgegraph.example.com/privkey.pem;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    
    # Proxy to application
    location / {
        proxy_pass http://interface:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Secrets Management

Never store secrets in code or environment files in production. Use a secrets manager:

```python
# secrets_manager.py
import boto3
from functools import lru_cache

class SecretsManager:
    """Secure secrets retrieval from AWS Secrets Manager."""
    
    def __init__(self):
        self.client = boto3.client('secretsmanager')
    
    @lru_cache(maxsize=128)
    def get_secret(self, secret_name: str) -> str:
        """Retrieve and cache secret value."""
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return response['SecretString']
        except Exception as e:
            # Log error without exposing secret name
            logger.error(f"Failed to retrieve secret: {e}")
            raise

# Usage in application
secrets = SecretsManager()
database_url = secrets.get_secret("prod/database/url")
api_key = secrets.get_secret("prod/openai/api_key")
```

#### Network Security

Configure firewalls to allow only necessary traffic:

```bash
# ufw firewall configuration (Ubuntu)
# Default policies
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (restrict to your IP in production)
ufw allow from 203.0.113.0/24 to any port 22

# Allow HTTPS
ufw allow 443/tcp

# Allow HTTP (redirects to HTTPS)
ufw allow 80/tcp

# Internal services (not exposed externally)
# PostgreSQL - only from app servers
ufw allow from 10.0.1.0/24 to any port 5432

# Enable firewall
ufw enable
```

### Scaling Strategies

#### Horizontal Scaling (Adding More Servers)

Best for stateless services like our API modules:

```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: intelligence-service
spec:
  replicas: 3  # Run 3 instances
  selector:
    matchLabels:
      app: intelligence
  template:
    metadata:
      labels:
        app: intelligence
    spec:
      containers:
      - name: intelligence
        image: kg/intelligence:v1.0
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: intelligence-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: intelligence-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # Scale up at 70% CPU
```

#### Vertical Scaling (Bigger Servers)

Best for databases that can't easily distribute:

```sql
-- PostgreSQL performance tuning for larger instance
-- Edit postgresql.conf

-- Memory (for 16GB RAM server)
shared_buffers = 4GB              -- 25% of RAM
effective_cache_size = 12GB       -- 75% of RAM
maintenance_work_mem = 1GB
work_mem = 20MB

-- Connections
max_connections = 200
max_prepared_transactions = 100

-- Write performance
checkpoint_segments = 32
checkpoint_completion_target = 0.9
wal_buffers = 16MB

-- Query optimization
random_page_cost = 1.1            -- For SSD storage
effective_io_concurrency = 200    -- For SSD storage
```

### Monitoring & Observability

You can't fix what you can't see. Monitoring provides visibility into system behavior:

#### Prometheus + Grafana Setup

```yaml
# docker-compose.monitoring.yml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_INSTALL_PLUGINS=redis-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
```

#### Application Metrics

Instrument your code to expose metrics:

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
request_count = Counter('app_requests_total', 
                       'Total requests', 
                       ['method', 'endpoint', 'status'])

request_duration = Histogram('app_request_duration_seconds',
                            'Request duration',
                            ['method', 'endpoint'])

active_users = Gauge('app_active_users', 'Currently active users')

# Use in application
@app.route('/api/entities')
def get_entities():
    start = time.time()
    
    try:
        # Your logic here
        result = fetch_entities()
        request_count.labels('GET', '/api/entities', '200').inc()
        return result
    except Exception as e:
        request_count.labels('GET', '/api/entities', '500').inc()
        raise
    finally:
        duration = time.time() - start
        request_duration.labels('GET', '/api/entities').observe(duration)
```

### Backup & Disaster Recovery

Backups are insurance for your data. You hope to never need them, but when you do, they're invaluable.

#### Automated PostgreSQL Backups

```bash
#!/bin/bash
# backup.sh - Run daily via cron

# Configuration
DB_NAME="knowledge_graph"
DB_USER="kg_user"
BACKUP_DIR="/backups/postgres"
S3_BUCKET="s3://kg-backups"
RETENTION_DAYS=30

# Create timestamped backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}.sql.gz"

# Perform backup with compression
pg_dump -U ${DB_USER} -d ${DB_NAME} | gzip > ${BACKUP_FILE}

# Upload to S3 for off-site storage
aws s3 cp ${BACKUP_FILE} ${S3_BUCKET}/postgres/

# Clean old local backups
find ${BACKUP_DIR} -name "backup_*.sql.gz" -mtime +${RETENTION_DAYS} -delete

# Verify backup integrity
gunzip -t ${BACKUP_FILE}
if [ $? -eq 0 ]; then
    echo "Backup successful: ${BACKUP_FILE}"
else
    echo "Backup corrupted: ${BACKUP_FILE}" >&2
    exit 1
fi
```

#### Disaster Recovery Plan

Document your recovery procedure:

1. **Detection** (< 5 minutes)
   - Monitoring alerts trigger
   - On-call engineer notified

2. **Assessment** (< 15 minutes)
   - Identify failure scope
   - Determine recovery strategy

3. **Recovery** (< 1 hour for critical services)
   ```bash
   # Restore from backup
   gunzip < backup_20240115_120000.sql.gz | psql -U kg_user -d knowledge_graph_restore
   
   # Verify data integrity
   psql -U kg_user -d knowledge_graph_restore -c "SELECT COUNT(*) FROM entities;"
   
   # Switch traffic to restored database
   kubectl set image deployment/graph-service graph=kg/graph:rollback
   ```

4. **Validation** (< 30 minutes)
   - Run smoke tests
   - Monitor error rates
   - Verify user access

### CI/CD Pipeline

Continuous Integration/Continuous Deployment automates the path from code to production:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Tests
        run: |
          docker compose -f docker-compose.test.yml up --abort-on-container-exit
          
      - name: Security Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'kg/intelligence:latest'
          
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to Production
        run: |
          # Build and tag images
          docker build -t kg/intelligence:${{ github.sha }} .
          docker tag kg/intelligence:${{ github.sha }} kg/intelligence:latest
          
          # Push to registry
          docker push kg/intelligence:${{ github.sha }}
          docker push kg/intelligence:latest
          
          # Deploy via kubectl
          kubectl set image deployment/intelligence intelligence=kg/intelligence:${{ github.sha }}
          kubectl rollout status deployment/intelligence
```

---

## Troubleshooting Guide

### Common Issues and Solutions

Production issues follow patterns. Recognizing these patterns speeds resolution:

#### Issue: Service Won't Start

**Symptoms**: Container exits immediately, health checks fail

**Diagnosis**:
```bash
# Check container logs
docker logs kg_intelligence --tail 100

# Inspect container exit code
docker inspect kg_intelligence --format='{{.State.ExitCode}}'

# Common exit codes:
# 0 - Success (container stopped normally)
# 1 - General errors
# 125 - Docker daemon error
# 126 - Container command not executable
# 127 - Container command not found
```

**Solutions**:
1. **Missing environment variables**: Check `.env` file completeness
2. **Port conflicts**: Use `lsof -i :8000` to find conflicting processes
3. **Dependency issues**: Ensure all services in `depends_on` are healthy
4. **Resource limits**: Increase memory/CPU limits in compose file

#### Issue: Database Connection Errors

**Symptoms**: "Connection refused" or "timeout" errors

**Diagnosis**:
```bash
# Test direct connection
docker exec -it kg_postgres psql -U kg_user -d knowledge_graph

# Check network connectivity
docker exec kg_intelligence ping postgres

# Verify credentials
docker exec kg_intelligence env | grep DATABASE_URL
```

**Solutions**:
1. **Network isolation**: Ensure services share a network
2. **Firewall rules**: Check if database port is open
3. **Connection pool exhaustion**: Increase `max_connections`
4. **DNS resolution**: Use IP address instead of hostname temporarily

#### Issue: High Memory Usage

**Symptoms**: OOM (Out of Memory) kills, slow response times

**Diagnosis**:
```bash
# Monitor memory usage
docker stats --no-stream

# Check for memory leaks in Python
docker exec kg_intelligence python -c "
import tracemalloc
import psutil
print(f'Memory: {psutil.Process().memory_info().rss / 1024 / 1024:.2f} MB')
"

# Analyze memory allocation
docker exec kg_intelligence py-spy dump --pid 1
```

**Solutions**:
1. **Increase limits**: Adjust `deploy.resources.limits.memory`
2. **Fix memory leaks**: Profile code, fix circular references
3. **Optimize queries**: Add indexes, limit result sets
4. **Cache effectively**: Use Redis for repeated computations

#### Performance Debugging

When services are slow, systematic investigation finds bottlenecks:

```bash
# 1. Check CPU usage
docker exec kg_intelligence top -bn1

# 2. Monitor disk I/O
docker exec kg_intelligence iostat -x 1

# 3. Analyze slow queries (PostgreSQL)
docker exec kg_postgres psql -U kg_user -c "
SELECT query, calls, mean_exec_time, total_exec_time 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;"

# 4. Profile Python code
docker exec kg_intelligence python -m cProfile -o profile.stats app.py

# 5. Network latency
docker exec kg_intelligence curl -w "@curl-format.txt" -o /dev/null -s http://graph:8000/health
```

### Log Analysis

Logs tell the story of what happened. Learn to read them effectively:

```bash
# Aggregate logs from all services
docker compose logs --timestamps --tail=1000 > system.log

# Search for errors
grep -i error system.log | head -20

# Find slow requests
grep "duration" system.log | awk '{print $NF}' | sort -rn | head -10

# Track specific request
grep "request_id=abc123" system.log

# Watch logs in real-time with filtering
docker compose logs -f | grep --line-buffered ERROR
```

### Recovery Procedures

When things break, follow these recovery steps:

1. **Stabilize** - Stop the bleeding
   ```bash
   # Scale down to stop errors
   docker compose scale intelligence=0
   
   # Or switch to maintenance mode
   docker compose up -d maintenance-page
   ```

2. **Diagnose** - Understand the problem
   ```bash
   # Recent changes
   git log --oneline -10
   
   # System state
   docker compose ps
   docker compose logs --tail=100
   ```

3. **Fix** - Apply the solution
   ```bash
   # Rollback to last known good
   git checkout HEAD~1
   docker compose build
   docker compose up -d
   ```

4. **Verify** - Ensure it's fixed
   ```bash
   # Run health checks
   ./scripts/healthcheck.sh
   
   # Monitor metrics
   watch -n 5 'docker compose ps'
   ```

5. **Document** - Learn from the incident
   ```markdown
   ## Incident Report: 2024-01-15
   
   **Duration**: 14:30 - 15:15 (45 minutes)
   **Impact**: API responses delayed by 10+ seconds
   **Root Cause**: Database connection pool exhausted
   **Fix**: Increased max_connections from 100 to 200
   **Prevention**: Add connection pool monitoring alert
   ```

---

## Next Steps

With deployment strategy defined, the team should:

1. **Week 1**: Set up local development environment
2. **Week 2**: Create Dockerfiles for each module
3. **Week 3-8**: Develop and test modules locally
4. **Week 9**: Deploy to staging environment
5. **Week 10**: Production deployment and demo

Remember: Start simple, iterate based on real needs. Perfect is the enemy of good - a working system you can improve beats a perfect plan you never implement.