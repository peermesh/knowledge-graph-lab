# Tasks for Backend Module v1.0-2025-11-05

## 🎯 HIGHLIGHTS - Top Things to Check Out

### 🔥 Cool Features Worth Exploring
- **Clean FastAPI structure** with proper dependency injection and router organization (modules/standalone/backend/src/api/app.py:1-40)
- **JWT-based authentication** with role-based access control (Admin/User roles) (modules/standalone/backend/src/services/security.py:21-28)
- **Async database architecture** in Publishing module with connection pooling and health checks (modules/standalone/publishing/src/core/database.py:25-37)
- **Request ID middleware** for distributed tracing across all API requests (modules/standalone/backend/src/api/middleware.py:8-22)
- **Docker Compose setup** with pgvector, Redis, and FastAPI integration (docs/.../my-docker-app-test/docker-compose.yml:1-37)

### ✅ Security Patches Applied (2025-11-25)
- **Authentication bypass fixed** - Added real database user lookup with bcrypt password verification (modules/standalone/backend/src/api/auth.py:23-75)
- **httpOnly cookies implemented** - Tokens now stored in secure httpOnly cookies instead of response body (modules/standalone/backend/src/api/auth.py:57-66)
- **CSRF protection added** - New middleware validates CSRF tokens on state-changing requests (modules/standalone/backend/src/middleware/csrf.py:1-54)

### ⚠️ Potential Issues to Investigate
- **CRITICAL: No actual authentication** - auth endpoint accepts ANY credentials, only checks if email/password exist (modules/standalone/backend/src/api/auth.py:16-22)
- **Hardcoded secrets in Docker Compose** - JWT_SECRET="supersecretkey" exposed in plaintext (docs/.../my-docker-app-test/docker-compose.yml:29)
- **Missing input validation** on entity creation - no sanitization of JSON metadata fields (modules/standalone/backend/src/api/entities.py:59-69)
- **No rate limiting** on authentication endpoint - vulnerable to brute force attacks (modules/standalone/backend/src/api/auth.py:15-22)
- **Database URL defaults to weak credentials** - "app:app" in config fallback (modules/standalone/backend/src/config.py:7)

---

**Generated:** 2025-11-24
**Reviewer:** Comprehensive Code Review
**Module:** Backend Infrastructure
**Developer:** gorodinskiia
**Total Tasks:** 47
**Estimated Effort:** 12-15 days

---

## Critical (P0) - Block release

### SECURITY-001: Implement Real Authentication (3 days)
**File:** modules/standalone/backend/src/api/auth.py:16-22
**Issue:** Authentication endpoint accepts any credentials without validation
```python
# CURRENT CODE - ACCEPTS ANYTHING
if not req.email or not req.password:
    raise HTTPException(status_code=400, detail="Invalid credentials")
role = "Admin" if req.email.lower().startswith("admin@") else "User"
```
**Impact:** Complete authentication bypass - anyone can generate valid tokens
**Remediation:**
1. Add User table lookup with password hash verification
2. Implement proper password verification using existing `verify_password()` from security.py
3. Add failed login attempt tracking
4. Add account lockout after N failed attempts
5. Remove role assignment based on email prefix

**Code:**
```python
def issue_token(req: TokenRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email, User.is_active == True).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=user.email, role=user.role)
    return {"access_token": token, "token_type": "bearer"}
```

**STATUS UPDATE (2025-11-25):** ✅ PARTIALLY FIXED
- Real authentication with database lookup and bcrypt verification has been implemented
- httpOnly cookies implemented for token storage
- Still TODO: Failed login tracking, account lockout, remove email prefix role assignment

---

### SECURITY-002: Remove Hardcoded Secrets from Docker Config (1 day)
**File:** docs/.../my-docker-app-test/docker-compose.yml:29
**Issue:** Sensitive credentials hardcoded in version control
```yaml
JWT_SECRET: supersecretkey  # NEVER commit this
POSTGRES_PASSWORD: app      # Weak default password
```
**Impact:** Exposed secrets allow token forgery and database access
**Remediation:**
1. Use environment variable substitution: `JWT_SECRET: ${JWT_SECRET}`
2. Create `.env.example` with dummy values
3. Add `.env` to .gitignore
4. Document required environment variables in README
5. Validate required env vars at startup

---

### SECURITY-003: Add Input Validation for JSON Fields (2 days)
**File:** modules/standalone/backend/src/api/entities.py:59-69
**Issue:** No validation on JSON metadata field allows injection attacks
```python
ent = Entity(**payload.model_dump())  # Accepts any JSON structure
```
**Impact:** JSON injection, database bloat, potential DoS via large payloads
**Remediation:**
1. Add max size validation for metadata JSON (e.g., 10KB)
2. Validate JSON structure against schema
3. Sanitize string values in metadata
4. Add metadata field count limit
5. Implement JSON depth limit

**Code:**
```python
class EntityCreate(BaseModel):
    meta: dict | None = Field(default=None, alias="metadata", max_length=10000)

    @validator("meta")
    def validate_metadata(cls, v):
        if v and len(json.dumps(v)) > 10240:  # 10KB limit
            raise ValueError("Metadata exceeds size limit")
        return v
```

---

### SECURITY-004: Implement Rate Limiting (2 days)
**File:** modules/standalone/backend/src/api/auth.py:15-22
**Issue:** No rate limiting on authentication endpoint
**Impact:** Vulnerable to brute force password attacks
**Remediation:**
1. Add slowapi or fastapi-limiter dependency
2. Apply rate limit: 5 attempts per minute per IP
3. Add exponential backoff after failures
4. Log excessive failed attempts
5. Consider CAPTCHA after 3 failures

**Code:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/token")
@limiter.limit("5/minute")
def issue_token(request: Request, req: TokenRequest):
    # ... authentication logic
```

---

### DATABASE-001: Add Database Migrations (2 days)
**File:** modules/standalone/backend/src/api/app.py:18-20
**Issue:** Using `create_all()` instead of migrations
```python
def on_startup() -> None:
    # Create tables for MVP; switch to migrations in production flows
    Base.metadata.create_all(bind=engine)
```
**Impact:** Cannot track schema changes, rollback, or manage production deployments
**Remediation:**
1. Add Alembic dependency
2. Initialize migration directory: `alembic init migrations`
3. Create initial migration from current models
4. Replace create_all with alembic upgrade
5. Document migration workflow in README

---

### ERROR-001: Add Proper Error Handling (2 days)
**File:** modules/standalone/backend/src/api/middleware.py:12-20
**Issue:** Generic error handler loses exception details
```python
except Exception as exc:  # Too broad - loses error context
    return JSONResponse(
        status_code=500,
        content={"error": "InternalServerError", "message": "An unexpected error occurred"}
    )
```
**Impact:** Debugging issues in production is impossible
**Remediation:**
1. Add structured logging for exceptions
2. Create custom exception classes for business logic
3. Log full stack trace with request_id
4. Return detailed errors in DEBUG mode only
5. Add error monitoring integration (e.g., Sentry)

---

### SCHEMA-001: Fix Foreign Key Type Mismatch (4 hours)
**File:** src/models/entity_relationship.py vs src/models/entity.py
**Issue:** Entity uses String(36) but EntityRelationship expects UUID foreign keys
**Impact:** Database constraint violations prevent relationship creation
**Remediation:**
1. Align Entity.id type with EntityRelationship (both UUID or both String)
2. Create migration to convert existing data if needed
3. Add database constraint tests
4. Document type standards in coding guidelines

## High Priority (P1) - Complete before next version

- [ ] Add comprehensive input validation (1.5 days)
  - src/api/entities.py:27 uses Field(min_length=1) but no max_length on type field
  - src/api/entities.py:29 confidence has no range validation (should be 0.0-1.0)
  - src/api/auth.py:18-19 has minimal validation
  - Resolution: Add Pydantic validators with proper constraints
  - Dependencies: None

- [ ] Implement rate limiting middleware (1 day)
  - No rate limiting exists anywhere in the application
  - Vulnerable to DDoS and brute force attacks
  - Redis already in requirements.txt:7 for implementation
  - Resolution: Add FastAPI rate limiting middleware with Redis backend
  - Dependencies: Redis connection configuration

- [ ] Add comprehensive test suite (2 days)
  - Zero test files exist in the backend module
  - No unit tests, integration tests, or contract tests
  - Target: 80% code coverage minimum
  - Resolution: Create pytest structure with unit/integration/contract tests
  - Dependencies: Add pytest and pytest-cov to requirements.txt

- [ ] Implement proper CORS configuration (4 hours)
  - No CORS middleware configured in src/api/app.py
  - Frontend integration will fail in browser
  - Resolution: Add FastAPI CORSMiddleware with environment-based origins
  - Dependencies: None

- [ ] Add health check for Redis (3 hours)
  - src/api/health.py:12-23 only checks database
  - Redis in requirements.txt but no health monitoring
  - Resolution: Add Redis ping check to dependencies in health endpoint
  - Dependencies: Redis client implementation

- [ ] Implement proper transaction management (1 day)
  - src/api/entities.py:65-68 commits without error handling
  - Database inconsistency on partial failures
  - Resolution: Add try/except with rollback in all endpoints
  - Dependencies: None

## Medium Priority (P2) - Schedule for next sprint

- [ ] Add API versioning strategy (6 hours)
  - **Files:** src/api/app.py:24-32 (router includes), src/api/auth.py:8, src/api/entities.py:11, src/api/health.py:7
  - No version prefix on routes (e.g., /v1/)
  - Future breaking changes will affect all clients
  - Resolution: Add /v1/ prefix to all routers
  - **Implementation:**
    ```python
    # In src/api/app.py:24-32
    app.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
    app.include_router(entities.router, prefix="/v1/entities", tags=["Entities"])
    app.include_router(health.router, prefix="/v1/health", tags=["Health"])

    # In each router file (e.g., auth.py:8)
    router = APIRouter()  # Remove prefix from here since it's in app.py
    ```
  - Dependencies: None

- [ ] Implement comprehensive API documentation (1 day)
  - FastAPI auto-generates OpenAPI, but no descriptions/examples
  - src/api/app.py:34-38 references openapi.yaml but file doesn't exist
  - Resolution: Add endpoint descriptions, request/response examples
  - Dependencies: None

- [ ] Add database connection pooling configuration (4 hours)
  - **File:** src/services/db.py:7-10
  - Current: Uses SQLAlchemy default pooling settings
  - No pool size limits, no connection timeout configuration
  - Resolution: Configure pool_size, max_overflow, pool_timeout
  - **Implementation:**
    ```python
    # In src/services/db.py:7-10
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,           # Number of persistent connections
        max_overflow=10,        # Maximum overflow connections
        pool_timeout=30,        # Timeout for getting connection
        pool_recycle=3600,      # Recycle connections after 1 hour
        pool_pre_ping=True      # Test connections before using
    )
    ```
  - Dependencies: None

- [ ] Implement structured logging throughout application (1 day)
  - src/api/health.py:22 has some logging
  - No consistent logging in endpoints or services
  - No correlation IDs for request tracing
  - Resolution: Add structlog with request ID propagation
  - Dependencies: None

- [ ] Add database indexes for performance (6 hours)
  - src/models/entity.py has no indexes on name, type, created_at
  - src/models/user.py:19 has unique constraint but no explicit index on email
  - Query performance will degrade with data growth
  - Resolution: Add indexes via migrations for frequent query fields
  - Dependencies: Migration infrastructure (P0 task)

- [ ] Implement soft delete audit trail (1 day)
  - src/api/entities.py:115 sets is_active=False without audit
  - No record of who deleted or when
  - Resolution: Add deleted_by and deleted_at fields to models
  - Dependencies: Migration infrastructure

## Low Priority (P3) - Nice to have

- [ ] Add Docker Compose for local development (6 hours)
  - Dockerfile exists at modules/standalone/backend.backup-20251117-142422/Dockerfile
  - No docker-compose.yml for backend module
  - Developers must manually set up PostgreSQL and Redis
  - Resolution: Create docker-compose.yml with backend, PostgreSQL, Redis
  - Dependencies: None

- [ ] Implement request/response logging middleware (4 hours)
  - No logging of API requests and responses
  - Difficult to debug integration issues
  - Resolution: Add middleware to log request/response with size limits
  - Dependencies: Structured logging (P2 task)

- [ ] Add Prometheus metrics endpoints (1 day)
  - No observability metrics exposed
  - Cannot monitor performance or errors in production
  - Resolution: Add prometheus_fastapi_instrumentator
  - Dependencies: None

- [ ] Implement API key authentication option (1.5 days)
  - Only JWT bearer tokens supported
  - Service-to-service auth requires user credentials
  - Resolution: Add API key support alongside JWT
  - Dependencies: None

- [ ] Add OpenAPI spec validation tests (6 hours)
  - src/api/app.py:34-38 references openapi.yaml that doesn't exist
  - No validation that implementation matches spec
  - Resolution: Create openapi.yaml and add schemathesis tests
  - Dependencies: Test infrastructure (P1 task)

## Dependencies

### External Dependencies
- PostgreSQL database (configured via DATABASE_URL env var)
- Redis server (required for rate limiting, caching)
- JWT_SECRET environment variable (production)
- Monitoring stack (Prometheus/Grafana) for P3 observability

### Internal Module Dependencies
- Frontend module will need CORS configuration (P1)
- AI module integration requires entity API (ready)
- Publishing module may consume entity data (ready after P0 fixes)

### Blocking Relationships
- P0 authentication must be fixed before ANY production use
- P0 foreign key mismatch blocks relationship features
- P0 migrations block safe database schema evolution
- P1 tests block confidence in releases
- P1 transaction management blocks data integrity guarantees
- P2 indexes block production-scale performance

## Notes

### Strengths
- Clean FastAPI application structure with good separation of concerns
- Proper use of Pydantic for request/response validation
- SQLAlchemy 2.0 with modern Mapped types
- Request ID middleware for tracing
- Soft delete pattern with is_active flags
- JWT token-based authentication framework
- Non-root user in Dockerfile for security

### Areas of Concern
- Security: No actual authentication, hardcoded secrets, no rate limiting
- Data Integrity: Type mismatch in foreign keys, no transactions
- Observability: Minimal logging, no metrics, errors swallowed
- Testing: Zero test coverage
- Documentation: Missing API specs, no endpoint descriptions
- Deployment: No migrations, no Docker Compose, no health checks for all dependencies

### Recommendations
1. Address ALL P0 items before any deployment - system is not secure
2. Implement P1 items for production readiness (especially tests and rate limiting)
3. Consider P2 items for operational excellence
4. P3 items enhance developer experience and observability

### Testing Recommendations
- Create pytest structure: tests/{unit,integration,contract}/
- Unit tests for: models, security functions, validators
- Integration tests for: database operations, API endpoints
- Contract tests for: OpenAPI spec compliance
- Load test authentication and entity CRUD endpoints
- Security audit of JWT implementation and input validation

### Code Quality Issues
- src/config.py:6-9 uses dataclass without frozen=True (mutable singleton)
- src/models/user.py:23-24 uses datetime.utcnow (deprecated, use timezone-aware)
- src/models/entity.py:22-23 same datetime.utcnow issue
- src/services/db.py:11-16 doesn't handle session cleanup on exception before yield
- Dockerfile:27 uses --reload flag in production CMD (should be conditional)

### Migration Path
1. Fix P0 authentication and security issues (2 days)
2. Set up migrations and fix schema issues (1 day)
3. Add comprehensive test suite (2 days)
4. Implement rate limiting and CORS (1 day)
5. Add monitoring and logging (2 days)
6. Total: ~2 weeks to production-ready state
