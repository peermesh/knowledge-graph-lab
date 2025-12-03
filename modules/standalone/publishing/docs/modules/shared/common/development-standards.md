# Development Standards

**Document:** Development Standards and Requirements  
**Version:** 1.0  
**Date:** 2025-10-20  
**Status:** DEFINITIVE

---

## Development Environment

### Docker Compose Requirements
**REQUIRED:** Docker Compose-based local development

**Development Standards:**
- **Hot Reload:** Development-time code reloading for faster iteration
- **Profiles:** Docker Compose profiles for different development scenarios
- **Mock Services:** Pre-configured mock services for independent development
- **Resource Limits:** Development environment resource constraints

### Docker Compose Configuration
```yaml
# docker-compose.yml
version: '3.9'

services:
  # Core Services (Phase 1)
  frontend:
    profiles: ["core", "services", "full"]
    build: ./services/frontend
    ports: ["3000:3000"]
    environment:
      - VITE_API_URL=http://localhost:8000
    volumes:
      - ./services/frontend/src:/app/src  # Hot reload
      
  backend:
    profiles: ["core", "services", "full"]
    build: ./services/backend
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgres://postgres:postgres@postgres:5432/kgl
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./services/backend/src:/app/src  # Hot reload
    depends_on:
      - postgres
      - redis
      
  # Phase 2 Services
  ai:
    profiles: ["services", "full"]
    build: ./services/ai
    ports: ["8001:8000"]
    environment:
      - DATABASE_URL=postgres://postgres:postgres@postgres:5432/kgl
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      - postgres
      - qdrant
      
  publishing:
    profiles: ["services", "full"]
    build: ./services/publishing
    ports: ["8002:8000"]
    environment:
      - DATABASE_URL=postgres://postgres:postgres@postgres:5432/kgl
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
    depends_on:
      - postgres
      - rabbitmq
      
  # Shared Infrastructure
  postgres:
    profiles: ["core", "services", "full"]
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=kgl
    ports: ["5432:5432"]
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    profiles: ["core", "services", "full"]
    image: redis:7
    ports: ["6379:6379"]
    
  qdrant:
    profiles: ["services", "full"]
    image: qdrant/qdrant:latest
    ports: ["6333:6333"]
    
  rabbitmq:
    profiles: ["services", "full"]
    image: rabbitmq:3.12-management
    ports: ["5672:5672", "15672:15672"]
    environment:
      - RABBITMQ_DEFAULT_USER=guest
      - RABBITMQ_DEFAULT_PASS=guest

volumes:
  postgres_data:
```

### Development Profiles
```bash
# Phase 1: Core MVP (5 containers)
docker-compose --profile core up

# Phase 2: Service Expansion (7 containers)
docker-compose --profile services up

# Phase 3: Full Architecture (9+ containers)
docker-compose --profile full up

# Individual Module Development
docker-compose --profile core up postgres redis
docker-compose --profile services up ai  # AI module with mocks
```

## Testing Requirements

### Universal Testing Standards
**REQUIRED:** Comprehensive testing strategy across all modules

**Testing Standards:**
- **Unit Tests:** 80%+ code coverage requirement
- **Integration Tests:** Cross-module integration testing
- **Contract Tests:** API contract validation
- **Mock Testing:** Independent module testing with mocks
- **Performance Tests:** Load testing for critical paths

### Test Structure
```
tests/
├── unit/                    # Unit tests
│   ├── test_auth.py
│   ├── test_entities.py
│   └── test_processing.py
├── integration/             # Integration tests
│   ├── test_api_integration.py
│   ├── test_database_integration.py
│   └── test_message_queue_integration.py
├── contract/                # Contract tests
│   ├── test_api_contracts.py
│   └── test_event_contracts.py
├── performance/             # Performance tests
│   ├── test_load.py
│   └── test_stress.py
└── fixtures/                # Test fixtures
    ├── mock_data.json
    └── test_config.yaml
```

### Testing Configuration
```yaml
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    -v
```

### Mock Services
```python
# Mock AI Service for Backend Testing
class MockAIService:
    def extract_entities(self, content: str) -> dict:
        return {
            "entities": [
                {"name": "OpenAI", "type": "organization", "confidence": 0.95},
                {"name": "GPT-4", "type": "product", "confidence": 0.90}
            ],
            "relationships": [
                {"from": "OpenAI", "to": "GPT-4", "type": "develops", "confidence": 0.95}
            ]
        }
```

## CI/CD Pipeline

### Pipeline Requirements
**REQUIRED:** Automated testing and deployment pipeline

**Pipeline Standards:**
- **Build:** Automated Docker image building
- **Test:** Automated test execution on all commits
- **Deploy:** Automated deployment to staging/production
- **Rollback:** Automated rollback capability
- **Monitoring:** Deployment monitoring and alerting

### GitHub Actions Configuration
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        module: [backend, frontend, ai, publishing]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          cd services/${{ matrix.module }}
          pip install -r requirements.txt
          
      - name: Run tests
        run: |
          cd services/${{ matrix.module }}
          pytest tests/ --cov=src --cov-report=xml
          
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: services/${{ matrix.module }}/coverage.xml
```

### Docker Build Pipeline
```yaml
# .github/workflows/build.yml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker images
        run: |
          docker build -t kgl-backend:latest services/backend
          docker build -t kgl-frontend:latest services/frontend
          docker build -t kgl-ai:latest services/ai
          docker build -t kgl-publishing:latest services/publishing
          
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push kgl-backend:latest
          docker push kgl-frontend:latest
          docker push kgl-ai:latest
          docker push kgl-publishing:latest
```

## Code Quality Standards

### Code Style Requirements
```yaml
# Python (Backend, AI, Publishing)
black:
  line-length: 88
  target-version: py311

flake8:
  max-line-length: 88
  ignore: E203, W503

mypy:
  strict: true
  python-version: 3.11
```

```json
// TypeScript/JavaScript (Frontend)
{
  "eslint": {
    "extends": ["@typescript-eslint/recommended"],
    "rules": {
      "@typescript-eslint/no-unused-vars": "error",
      "@typescript-eslint/explicit-function-return-type": "warn"
    }
  },
  "prettier": {
    "semi": true,
    "trailingComma": "es5",
    "singleQuote": true,
    "printWidth": 80
  }
}
```

### Documentation Requirements
- **API Documentation:** OpenAPI/Swagger documentation for all endpoints
- **Code Documentation:** Docstrings for all functions and classes
- **README Files:** Comprehensive README for each module
- **Architecture Documentation:** Clear architecture diagrams and explanations

## Development Workflow

### Git Workflow
```bash
# Feature Development
git checkout -b feature/entity-extraction
git add .
git commit -m "feat: add entity extraction endpoint"
git push origin feature/entity-extraction

# Create Pull Request
# After review and approval:
git checkout main
git pull origin main
git merge feature/entity-extraction
git push origin main
```

### Branch Naming Convention
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `refactor/description` - Code refactoring
- `docs/description` - Documentation updates

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Validation Requirements

### Development Environment Compliance
- [ ] Docker Compose configuration working
- [ ] Hot reload functionality enabled
- [ ] Mock services configured
- [ ] Resource limits appropriate
- [ ] Development profiles functional

### Testing Compliance
- [ ] Unit tests achieve 80%+ coverage
- [ ] Integration tests cover cross-module communication
- [ ] Contract tests validate API specifications
- [ ] Mock services enable independent testing
- [ ] Performance tests validate critical paths

### CI/CD Compliance
- [ ] Automated build pipeline configured
- [ ] Test execution automated on all commits
- [ ] Deployment pipeline functional
- [ ] Rollback capability implemented
- [ ] Monitoring and alerting configured

### Code Quality Compliance
- [ ] Code style standards enforced
- [ ] Documentation requirements met
- [ ] Git workflow followed
- [ ] Branch naming convention used
- [ ] Commit message format followed

---

**Related Documentation:**
- [Architecture Overview](./architecture-overview.md)
- [Shared Infrastructure](./shared-infrastructure.md)
- [Security & Compliance](./security-compliance.md)
