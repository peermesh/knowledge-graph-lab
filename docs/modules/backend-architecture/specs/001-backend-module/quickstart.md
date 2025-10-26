# Quickstart: Backend Architecture

**Feature**: Backend Architecture | **Date**: 2025-10-26
**Purpose**: Setup and development guide for the Knowledge Graph Backend implementation

## Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 22.04+ recommended), macOS, or Windows with WSL2
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 20GB free space for Docker images and databases
- **Network**: Internet connection for downloading dependencies

### Software Dependencies
- **Docker**: Version 20.10+ with Docker Compose
- **Python**: Version 3.11+ (for local development)
- **PostgreSQL**: Version 15+ (Docker container or local installation)
- **Git**: For version control and development workflow

## Environment Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Configure Environment
```bash
# Copy environment template
cp .dev/ai/speckit-output/backend-module/.env.example .dev/ai/speckit-output/backend-module/.env

# Edit configuration (important settings)
nano .dev/ai/speckit-output/backend-module/.env
```

**Critical Configuration**:
- `JWT_SECRET_KEY`: Generate a secure 32+ character secret key
- `POSTGRES_PASSWORD`: Set a strong database password
- `RABBITMQ_PASSWORD`: Set message queue password
- `ALLOWED_ORIGINS`: Update for your frontend URLs

### 3. Start Infrastructure Services
```bash
cd .dev/ai/speckit-output/backend-module
make docker-up
```

This starts:
- PostgreSQL database with pgvector extension
- Redis for caching and sessions
- RabbitMQ for message processing
- (Optional) AI worker service

### 4. Initialize Database
```bash
# Run database migrations
make migrate-up

# Verify database connectivity
make health
```

### 5. Start Development Server
```bash
# Using Makefile
make dev

# Or directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Development Workflow

### Code Structure
```
.dev/ai/speckit-output/backend-module/
├── app/                    # Application source code
│   ├── main.py            # FastAPI application entry point
│   ├── core/              # Core infrastructure
│   ├── models/            # Database models
│   ├── api/               # API endpoints
│   ├── schemas/           # Request/response models
│   └── services/          # Business logic
├── tests/                 # Test suite
├── database/migrations/   # Database migrations
└── docs/                  # Documentation
```

### Running Tests
```bash
# All tests
make test

# With coverage
make test-cov

# Specific test category
pytest tests/test_auth.py -v
pytest tests/test_models.py -v
```

### Database Management
```bash
# Create new migration
make migrate-create MESSAGE="Add user profile fields"

# Run migrations
make migrate-up

# Rollback last migration
make migrate-down
```

### API Development
```bash
# Start server with auto-reload
make dev

# Access documentation
open http://localhost:8000/docs

# Test endpoints
curl http://localhost:8000/health
```

## API Endpoints

### Authentication
```bash
# Register new user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'

# Get current user (with token)
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Health Monitoring
```bash
# Basic health check
curl http://localhost:8000/health

# Detailed health with service status
curl http://localhost:8000/health/detailed

# Kubernetes readiness probe
curl http://localhost:8000/health/readiness

# Kubernetes liveness probe
curl http://localhost:8000/health/liveness
```

## Docker Commands

### Service Management
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f postgres
```

### Database Access
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U knowledge_user -d knowledge_graph

# Run database backup
docker-compose exec postgres pg_dump -U knowledge_user knowledge_graph > backup.sql

# Restore database
docker-compose exec -T postgres psql -U knowledge_user -d knowledge_graph < backup.sql
```

## Monitoring and Debugging

### Application Logs
```bash
# View all logs
docker-compose logs -f

# View API logs only
docker-compose logs -f api

# View database logs
docker-compose logs -f postgres
```

### Health Checks
```bash
# Check API health
curl http://localhost:8000/health

# Check database connectivity
docker-compose exec api python -c "
from app.core.database import engine
import asyncio

async def check_db():
    async with engine.begin() as conn:
        await conn.execute('SELECT 1')

asyncio.run(check_db())
print('Database connected successfully')
"
```

### Performance Monitoring
```bash
# Check API performance
curl http://localhost:8000/health/detailed

# Monitor database performance
docker-compose exec postgres psql -U knowledge_user -d knowledge_graph -c "
SELECT * FROM api_access_logs
WHERE timestamp > NOW() - INTERVAL '1 hour'
ORDER BY response_time_ms DESC
LIMIT 10;
"
```

## Production Deployment

### Environment Variables
```bash
# Production environment
export NODE_ENV=production
export DEBUG=false
export JWT_SECRET_KEY="your-production-secret-key"
export DATABASE_URL="postgresql://user:pass@prod-db:5432/db"
```

### Docker Production
```bash
# Build production image
docker build -t knowledge-graph-api:latest .

# Run with production config
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@db:5432/db" \
  -e JWT_SECRET_KEY="your-secret" \
  knowledge-graph-api:latest
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: knowledge-graph-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: knowledge-graph-api
  template:
    metadata:
      labels:
        app: knowledge-graph-api
    spec:
      containers:
      - name: api
        image: knowledge-graph-api:latest
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Verify connection string in .env
cat .env | grep DATABASE_URL
```

**Authentication Issues**
```bash
# Check JWT secret key
cat .env | grep JWT_SECRET_KEY

# Verify user exists in database
docker-compose exec postgres psql -U knowledge_user -d knowledge_graph -c "
SELECT id, email, role, is_active FROM users LIMIT 5;
"
```

**API Not Responding**
```bash
# Check API logs
docker-compose logs api

# Verify port binding
docker-compose ps

# Test health endpoint
curl http://localhost:8000/health
```

**Migration Errors**
```bash
# Check current migration status
docker-compose exec api alembic current

# Show migration history
docker-compose exec api alembic history

# Force rollback if needed
docker-compose exec api alembic downgrade base
```

### Performance Issues
```bash
# Check slow queries
docker-compose exec postgres psql -U knowledge_user -d knowledge_graph -c "
SELECT * FROM api_access_logs
WHERE response_time_ms > 1000
ORDER BY response_time_ms DESC
LIMIT 10;
"

# Monitor database connections
docker-compose exec postgres psql -U knowledge_user -d knowledge_graph -c "
SELECT state, count(*) FROM pg_stat_activity GROUP BY state;
"
```

## Development Best Practices

### Code Standards
- Follow PEP 8 for Python code style
- Use type hints throughout the codebase
- Write comprehensive docstrings
- Implement proper error handling

### Testing
- Write tests before implementation (TDD approach)
- Run tests before committing changes
- Maintain high test coverage (>90%)
- Test both positive and negative scenarios

### Database Changes
- Never modify database schema directly in production
- Use migrations for all schema changes
- Test migrations on development database first
- Always provide rollback scripts

### Security
- Never commit secrets to version control
- Use environment variables for all configuration
- Regularly rotate JWT secret keys
- Monitor API access logs for suspicious activity

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review application logs for error details
3. Verify environment configuration
4. Check database connectivity and migrations
5. Consult the constitutional requirements for compliance

## Next Steps

1. ✅ Complete setup using this quickstart guide
2. 🚧 Implement user stories in priority order (P1 → P2 → P3)
3. 🧪 Run comprehensive test suite
4. 🔄 Validate against constitutional requirements
5. 🚀 Deploy to staging environment
6. 📊 Monitor production metrics and performance

This implementation follows all constitutional principles and provides a solid foundation for the Knowledge Graph Lab System backend architecture.
