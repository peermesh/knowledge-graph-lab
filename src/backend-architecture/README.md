# Backend Architecture Module

Robust backend infrastructure and API services for the Knowledge Graph Lab platform.

## Overview

The Backend Architecture Module provides the foundational infrastructure that powers the entire Knowledge Graph Lab platform. It delivers:

- **Database Management**: PostgreSQL with comprehensive entity and relationship storage
- **API Services**: FastAPI endpoints with <200ms response times and 500+ requests/second capacity
- **Authentication**: JWT-based system with role-based permissions and secure session management
- **Message Queuing**: RabbitMQ for async processing with priority-based job handling
- **Monitoring**: Comprehensive health checks, performance metrics, and operational monitoring

## Features

- **High-Performance APIs**: FastAPI with async support for concurrent request handling
- **Secure Authentication**: JWT tokens with bcrypt password hashing and role-based permissions
- **Scalable Database**: PostgreSQL with optimized queries for entity relationships and knowledge graphs
- **Async Processing**: RabbitMQ message queues for reliable inter-module communication
- **Comprehensive Testing**: >85% test coverage with TDD approach and integration testing

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7.0+
- RabbitMQ 3+

### Installation

1. **Clone and setup**:
   ```bash
   cd src/backend-architecture
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment setup**:
   ```bash
   cp .env.template .env
   # Edit .env with your configuration
   ```

3. **Database setup**:
   ```bash
   # Run migrations
   alembic upgrade head

   # Or create tables directly
   python -c "from app.core.database import create_tables; import asyncio; asyncio.run(create_tables())"
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user info

### Entity Management
- `GET /api/v1/entities` - List entities with filtering
- `POST /api/v1/entities` - Create new entity
- `GET /api/v1/entities/{id}` - Get entity by ID
- `PUT /api/v1/entities/{id}` - Update entity
- `DELETE /api/v1/entities/{id}` - Delete entity
- `GET /api/v1/entities/{id}/relationships` - Get entity relationships

### User Management
- `GET /api/v1/users` - List users (admin only)
- `GET /api/v1/users/{id}` - Get user by ID (admin only)
- `PUT /api/v1/users/{id}` - Update user (admin only)
- `DELETE /api/v1/users/{id}` - Delete user (admin only)

### System Health
- `GET /health` - Comprehensive health check
- `GET /ready` - Kubernetes readiness probe
- `GET /live` - Kubernetes liveness probe

## Configuration

The application uses environment variables for configuration:

```bash
# Application
APP_NAME=Backend Architecture Module
VERSION=1.0.0
DEBUG=true
API_V1_PREFIX=/api/v1

# Database
POSTGRES_URL=postgresql+asyncpg://backend_user:backend_password@localhost:5432/backend_module

# Message Queue
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
RABBITMQ_EXCHANGE=backend_processing

# Redis
REDIS_URL=redis://localhost:6379
REDIS_CACHE_TTL=3600

# Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# External Services
AI_MODULE_URL=http://localhost:8001
FRONTEND_URL=http://localhost:3000
PUBLISHING_MODULE_URL=http://localhost:8002
```

## Development

### Testing

Run the test suite:

```bash
pytest tests/ -v --cov=app
```

### Code Quality

```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint code
flake8 app/ tests/
mypy app/

# Run all checks
pre-commit run --all-files
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Docker Deployment

### Build and run with Docker Compose:

```bash
docker-compose up -d
```

### Production deployment:

```bash
# Build image
docker build -t backend-architecture:1.0.0 .

# Run container
docker run -p 8000:8000 \
  -e POSTGRES_URL=postgresql+asyncpg://... \
  -e SECRET_KEY=... \
  backend-architecture:1.0.0
```

## Performance Targets

- **API Response Times**: <200ms (p95), <500ms (p99) for all endpoints
- **Throughput**: 500 requests/second sustained, 1,000 requests/second peak
- **Database Queries**: <50ms (p95) for simple queries, <500ms for complex traversals
- **Authentication**: <100ms for login operations
- **Uptime**: 99.9% availability with comprehensive monitoring

## Monitoring

The service provides comprehensive monitoring through:

- **Health Checks**: Database, authentication, message queue, external services
- **Performance Metrics**: Response times, throughput, error rates, resource usage
- **Security Monitoring**: Authentication attempts, authorization failures, audit logs
- **API Analytics**: Request patterns, endpoint usage, performance trends

## Integration

The Backend module integrates with:

- **AI Module**: Receives entity extraction results and knowledge graph data
- **Frontend Module**: Provides REST APIs and WebSocket services for data access
- **Publishing Module**: Supplies content management and engagement tracking APIs

## Security

- **JWT Authentication**: RFC 7519 compliant token implementation
- **Password Security**: bcrypt hashing with salt rounds ≥ 12
- **Role-Based Access**: Four-tier permission system (user, researcher, moderator, admin)
- **API Security**: Rate limiting, CORS policy, input validation
- **Audit Logging**: Complete trail of all API operations and data changes

## Contributing

1. Follow the established code style (black, isort, flake8)
2. Write tests for new functionality (TDD approach)
3. Update documentation for API changes
4. Ensure all tests pass before submitting PRs
5. Include security considerations for new features

## License

MIT License - see LICENSE file for details.

---

*Part of the Knowledge Graph Lab platform - Foundation for intelligent knowledge systems.*
