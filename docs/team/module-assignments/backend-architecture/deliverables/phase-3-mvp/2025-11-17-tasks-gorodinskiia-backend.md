# Backend Module - Task List

**📋 What This Document Is:**
This is your prioritized task list for bringing the Backend module into compliance with Standalone Module Requirements. Each task includes specific files to modify, step-by-step guidance, effort estimates, and references to help you complete the work.

**👤 Developer:** gorodinskiia

**📅 Review Date:** 2025-11-17

**📊 Status:** Strong foundation with 21 identified improvements needed

**⏱️ Total Estimated Effort:** ~39 hours (~5 days of focused work)

---

## 📖 How to Use This Document

1. **Start with Critical Priority tasks** - These are required for module compliance
2. **Work through tasks sequentially** - They're ordered by dependency and impact
3. **Check off tasks as you complete them** - Track your progress
4. **Ask for help if stuck** - Don't spend more than 30 minutes stuck on any task
5. **Reference the gap analysis** for technical details: `2025-11-17-backend-gap-analysis.md` (same directory)

**Related Documents:**
- Detailed gap analysis: `./2025-11-17-backend-gap-analysis.md`
- Standalone Module Requirements: `../../../../../modules/shared/standalone-modules/README.md`
- Frontend reference implementation: `../../../frontend-design/` (has excellent examples)
- AI migration examples: `../../../ai-development/` (has Alembic setup working)

---

## ✅ Quick Progress Tracker

**Week 1 (Critical):** [ ] Task 1 | [ ] Task 2 | [ ] Task 3 | [ ] Task 4
**Week 2 (High):** [ ] Task 5 | [ ] Task 6 | [ ] Task 7 | [ ] Task 8 | [ ] Task 9 | [ ] Task 10 | [ ] Task 11
**Week 3 (Medium):** [ ] Task 12 | [ ] Task 13 | [ ] Task 14 | [ ] Task 15 | [ ] Task 16

---

## 🔴 Critical Priority (Must Complete This Week) - 4 tasks

These tasks are required for the module to meet Standalone Module Requirements. Start here.

### Task 1: Implement Migration System ⏱️ 3 hours

**What's Wrong:**
Tables are created directly using `Base.metadata.create_all()` on startup. This works for development but makes it impossible to safely manage schema changes in production.

**What You Need to Do:**

**Step 1: Initialize Alembic** (15 minutes)
```bash
# From your backend module directory
cd modules/standalone/backend
alembic init alembic
```

This creates:
- `alembic/` directory with migration templates
- `alembic.ini` configuration file

**Step 2: Configure Alembic** (30 minutes)

Edit `alembic.ini`:
```ini
# Line ~40: Point to your database
# Change this:
sqlalchemy.url = driver://user:pass@localhost/dbname

# To this:
# sqlalchemy.url is set in env.py from config.Settings
```

Edit `alembic/env.py`:
```python
# Add at top (around line 8):
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

from src.config import settings
from src.models.base import Base

# Line ~20: Set target metadata
target_metadata = Base.metadata

# Line ~40: Set database URL
config.set_main_option('sqlalchemy.url', settings.database_url)
```

**Step 3: Create Initial Migration** (30 minutes)
```bash
# Generate migration from your models
alembic revision --autogenerate -m "Initial schema with users, entities, relationships"

# This creates alembic/versions/001_initial_schema_*.py
# Review the generated file to ensure it looks correct
```

**Step 4: Update Application Startup** (15 minutes)

Edit `src/api/app.py`:
```python
# REMOVE this section:
@app.on_event("startup")
def on_startup() -> None:
    # Create tables for MVP; switch to migrations in production flows
    Base.metadata.create_all(bind=engine)

# REPLACE with comment:
# Database tables managed by Alembic migrations
# Run: alembic upgrade head
```

**Step 5: Test Migrations** (1 hour)
```bash
# Reset your test database
dropdb knowledge_graph_lab_test  # If exists
createdb knowledge_graph_lab_test

# Run migrations
alembic upgrade head

# Verify tables were created
psql knowledge_graph_lab_test -c "\dt"

# Should show: users, entities, entity_relationships, alembic_version
```

**Files Modified:**
- `alembic.ini` (created)
- `alembic/env.py` (created & configured)
- `alembic/versions/001_*.py` (created)
- `src/api/app.py` (removed create_all)

**How to Verify It Works:**
```bash
# Migrations should run without errors
alembic upgrade head

# Check migration history
alembic history

# Try downgrade/upgrade
alembic downgrade -1
alembic upgrade head
```

**Reference Example:**
Look at `modules/standalone/ai/alembic/` - they have this working correctly.

**Why This Matters:**
Production databases need controlled schema evolution. Without migrations, you can't safely add columns, change types, or update schemas without downtime or data loss.

**Get Help If:**
- Alembic commands fail with errors
- Generated migration doesn't match your models
- You're unsure if migration is safe to run

---

### Task 2: Add /api/v1 Prefix to All Routes ⏱️ 2 hours

**What's Wrong:**
Your routes are `/auth/token`, `/entities/`, etc. The spec requires all API endpoints under `/api/v1/` prefix.

**What You Need to Do:**

**Step 1: Update Router Includes** (30 minutes)

Edit `src/api/app.py`:
```python
# BEFORE:
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(entities_router)
app.include_router(admin_router)

# AFTER:
# Health stays at root /health (not under /api/v1)
app.include_router(health_router)

# All API routes go under /api/v1
app.include_router(auth_router, prefix="/api/v1")
app.include_router(entities_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
```

**Step 2: Verify Router Prefixes** (15 minutes)

Check each router file - they should NOT have `/api/v1` in their own prefix:

`src/api/auth.py`:
```python
# Should be:
router = APIRouter(prefix="/auth", tags=["auth"])
# NOT: prefix="/api/v1/auth"
```

`src/api/entities.py`:
```python
# Should be:
router = APIRouter(prefix="/entities", tags=["entities"])
```

`src/api/admin.py`:
```python
# Should be:
router = APIRouter(prefix="/admin", tags=["admin"])
```

**Step 3: Update Tests** (1 hour)

Update all test files to use new paths:

```python
# BEFORE:
response = client.post("/auth/token", json={"email": "test@example.com", "password": "test"})

# AFTER:
response = client.post("/api/v1/auth/token", json={"email": "test@example.com", "password": "test"})
```

Files to update:
- `tests/contract/test_auth.py`
- `tests/contract/test_entities.py`
- `tests/integration/test_auth_entities.py`
- `tests/integration/test_roles.py`
- Any other test files making API calls

**Step 4: Update OpenAPI Configuration** (15 minutes)

Edit `src/api/app.py`:
```python
app = FastAPI(
    title="Backend Module API (MVP)",
    openapi_url="/api/v1/openapi.json",  # Add this line
    docs_url="/api/v1/docs",              # Add this line
    redoc_url="/api/v1/redoc"             # Add this line
)
```

**How to Verify It Works:**
```bash
# Start your dev server
uvicorn src.api.app:app --reload

# Check endpoints:
curl http://localhost:8000/health  # Should work (no /api/v1)
curl http://localhost:8000/api/v1/auth/token  # Should work
curl http://localhost:8000/api/v1/openapi.json  # Should show OpenAPI spec

# Run tests
pytest tests/
```

**Files Modified:**
- `src/api/app.py`
- `tests/contract/test_auth.py`
- `tests/contract/test_entities.py`
- `tests/integration/test_auth_entities.py`
- `tests/integration/test_roles.py`

**Why This Matters:**
All 4 modules must use the same API path structure (`/api/v1`) to integrate properly. This is a contract requirement.

**⚠️ Breaking Change:**
This changes all your API URLs. Make sure to update any documentation or scripts that call these endpoints.

---

### Task 3: Implement Structured JSON Logging ⏱️ 4 hours

**What's Wrong:**
Using standard Python logging which outputs plain text. Production systems need structured JSON logs for monitoring, alerting, and debugging.

**What You Need to Do:**

**Step 1: Add Dependency** (5 minutes)

Add to `requirements.txt`:
```
python-json-logger>=2.0.7
```

Install:
```bash
pip install python-json-logger
```

**Step 2: Create Logging Config** (1 hour)

Create `src/logging_config.py`:
```python
"""Structured JSON logging configuration"""
import logging
import sys
from pythonjsonlogger import jsonlogger
from src.config import settings


def setup_json_logging():
    """Configure JSON structured logging for production"""

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)

    # Create JSON formatter
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s %(module_id)s %(user_id)s %(request_id)s',
        rename_fields={
            'levelname': 'level',
            'asctime': 'timestamp'
        },
        datefmt='%Y-%m-%dT%H:%M:%S'
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Example usage:
# logger.info("User logged in", extra={
#     "module_id": "backend",
#     "user_id": "123",
#     "request_id": "abc-def"
# })
```

**Step 3: Add Config Settings** (15 minutes)

Update `src/config.py`:
```python
@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://app:app@localhost:5432/app")
    jwt_secret: str = os.getenv("JWT_SECRET", "devsecret")
    jwt_alg: str = os.getenv("JWT_ALG", "HS256")

    # Add these:
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    module_id: str = os.getenv("MODULE_ID", "backend")
```

**Step 4: Enable in Application** (15 minutes)

Update `src/api/app.py`:
```python
# Add at top
from src.logging_config import setup_json_logging

# After app creation
app = FastAPI(title="Backend Module API (MVP)")

# Add this
setup_json_logging()
logger = logging.getLogger(__name__)
logger.info("Backend module starting", extra={"module_id": "backend"})
```

**Step 5: Update Logging Calls** (2 hours)

Update all logging to include structured fields:

**Before:**
```python
logger.info("health_ready", extra={"status": status, "dependencies": deps})
```

**After:**
```python
logger.info("Health check completed", extra={
    "module_id": "backend",
    "status": status,
    "dependencies": deps
})
```

Find and update logging in:
- `src/api/health.py`
- `src/api/auth.py`
- `src/api/entities.py`
- `src/api/admin.py`
- Any other files with logging

**Key fields to include:**
- `module_id`: Always "backend"
- `user_id`: From authenticated user (if available)
- `request_id`: From request headers (if available)

**Step 6: Test Logging** (30 minutes)

```bash
# Run server
uvicorn src.api.app:app --reload

# Make requests and check logs are JSON:
curl http://localhost:8000/health

# You should see JSON output like:
# {"timestamp": "2025-11-17T14:30:00", "level": "INFO", "message": "Health check completed", "module_id": "backend", ...}
```

**Files Modified:**
- `requirements.txt`
- `src/logging_config.py` (created)
- `src/config.py`
- `src/api/app.py`
- `src/api/health.py`
- `src/api/auth.py`
- `src/api/entities.py`
- `src/api/admin.py`

**Why This Matters:**
JSON logs can be ingested by monitoring systems (DataDog, CloudWatch, ELK), making it easy to search, alert, and debug production issues.

**Example Good Log:**
```json
{
  "timestamp": "2025-11-17T14:30:00Z",
  "level": "INFO",
  "module_id": "backend",
  "user_id": "user-123",
  "request_id": "req-abc-def",
  "message": "Entity created successfully",
  "entity_id": "ent-456"
}
```

---

### Task 4: Implement Real Authentication ⏱️ 4 hours

**What's Wrong:**
Authentication currently accepts any email/password combination (placeholder implementation).

**Priority Note:**
This can be deferred for MVP but MUST be completed before any production deployment. Mark with TODO comments if deferring.

**What You Need to Do:**

**Step 1: Create Password Hashing Utilities** (1 hour)

Create `src/services/security.py`:
```python
"""Security utilities for password hashing and JWT"""
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from src.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain text password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, role: str) -> str:
    """Create a JWT access token"""
    expire = datetime.utcnow() + timedelta(hours=24)

    to_encode = {
        "sub": subject,
        "role": role,
        "exp": expire
    }

    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_alg)
    return encoded_jwt
```

**Step 2: Update User Model** (30 minutes)

Ensure `src/models/user.py` has password hash field:
```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)  # Ensure this exists
    role = Column(String, default="user")
    # ... other fields
```

**Step 3: Update Auth Endpoint** (1.5 hours)

Update `src/api/auth.py`:
```python
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from src.services.security import verify_password, create_access_token
from src.services.db import get_db
from src.models.user import User


router = APIRouter(prefix="/auth", tags=["auth"])


class TokenRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/token")
def issue_token(req: TokenRequest, db: Session = Depends(get_db)):
    """Authenticate user and issue JWT token"""

    # Look up user by email
    user = db.query(User).filter(User.email == req.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create token
    token = create_access_token(subject=user.email, role=user.role)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
```

**Step 4: Add User Registration** (1 hour)

Add to `src/api/auth.py`:
```python
from src.services.security import hash_password


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    # Password should be validated (length, complexity) in production


@router.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""

    # Check if user exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user with hashed password
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role="user"  # Default role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully", "email": user.email}
```

**Step 5: Update Tests** (1 hour)

Update `tests/contract/test_auth.py` to create real users:
```python
def test_auth_flow(client, db):
    # Register user
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200

    # Login with correct credentials
    response = client.post("/api/v1/auth/token", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Login with wrong credentials should fail
    response = client.post("/api/v1/auth/token", json={
        "email": "test@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
```

**Files Modified:**
- `src/services/security.py` (created)
- `src/models/user.py` (verify password_hash field)
- `src/api/auth.py`
- `tests/contract/test_auth.py`

**How to Verify:**
```bash
# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Login with correct password (should work)
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Login with wrong password (should fail with 401)
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "wrongpass"}'
```

**Why This Matters:**
Placeholder auth is a security vulnerability. Real systems need to verify credentials against a database.

**⚠️ If Deferring:**
Add this comment to `src/api/auth.py`:
```python
# TODO: Replace placeholder authentication with real user verification
# See task list: 2025-11-17-tasks-gorodinskiia-backend.md, Task 4
```

---

## 🟡 High Priority (Should Complete Next Week) - 7 tasks

These improve production readiness and API consistency. Complete after Critical tasks.

### Task 5: Fix Health Endpoint Path ⏱️ 1 hour

**Current:** `/health/ready`
**Required:** `/health` (simple endpoint) and `/health/ready` (detailed endpoint)

**Quick Fix:**

Edit `src/api/health.py`:
```python
router = APIRouter(prefix="", tags=["health"])  # Changed from prefix="/health"

@router.get("/health")
def health():
    """Simple health check"""
    return {"status": "healthy"}

@router.get("/health/ready")
def readiness():
    # ... existing code ...
```

---

### Task 6: Implement Database Schema Naming ⏱️ 2 hours

**Add schemas to organize tables:**

`src/models/user.py`:
```python
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "backend_auth"}
```

`src/models/entity.py`:
```python
class Entity(Base):
    __tablename__ = "entities"
    __table_args__ = {"schema": "backend_entities"}
```

Then create new migration:
```bash
alembic revision --autogenerate -m "Add schema organization"
```

---

### Task 7: Standardize Response Format ⏱️ 4 hours

**Create response wrapper:**

`src/api/responses.py`:
```python
from typing import Any, Optional
from pydantic import BaseModel
from datetime import datetime


class Meta(BaseModel):
    request_id: Optional[str] = None
    timestamp: str = datetime.utcnow().isoformat()


class StandardResponse(BaseModel):
    data: Any
    meta: Meta = Meta()
    errors: list = []


def success_response(data: Any, request_id: str = None):
    return StandardResponse(
        data=data,
        meta=Meta(request_id=request_id),
        errors=[]
    )
```

Update endpoints to use it:
```python
from src.api.responses import success_response

@router.post("/entities")
def create_entity(entity: EntityCreate):
    # ... create entity ...
    return success_response(entity_data)
```

---

### Task 8: Implement RFC7807 Error Handling ⏱️ 3 hours

**Create error handler:**

`src/api/errors.py`:
```python
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": f"https://httpstatuses.com/{exc.status_code}",
            "title": "HTTP " + str(exc.status_code),
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": str(request.url.path)
        }
    )
```

Register in `src/api/app.py`:
```python
from src.api.errors import http_exception_handler

app.add_exception_handler(HTTPException, http_exception_handler)
```

---

### Task 9: Configure CORS ⏱️ 30 minutes

Add CORS middleware to `src/api/app.py`:
```python
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Add to `src/config.py`:
```python
cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
```

---

### Task 10: Complete JWT Token Claims ⏱️ 2 hours

Update `src/services/security.py` to add missing claims:
```python
def create_access_token(subject: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    iat = datetime.utcnow()

    to_encode = {
        "sub": subject,
        "role": role,
        "iss": settings.jwt_issuer,      # Add issuer
        "aud": settings.jwt_audience,    # Add audience
        "iat": int(iat.timestamp()),     # Add issued at
        "exp": int(expire.timestamp())   # Keep expiration
    }

    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_alg)
```

Add to `src/config.py`:
```python
jwt_issuer: str = os.getenv("JWT_ISSUER", "backend-module")
jwt_audience: str = os.getenv("JWT_AUDIENCE", "kgl-api")
```

---

### Task 11: Create README.md ⏱️ 2 hours

Create `modules/standalone/backend/README.md` with these sections:

```markdown
# Backend Module

## Overview
[What this module does]

## Quick Start
[How to run it]

## Environment Variables
[All config options]

## Database Setup
[How to run migrations]

## API Endpoints
[List of main endpoints]

## Testing
[How to run tests]

## Troubleshooting
[Common issues]
```

**Reference:** Look at `modules/standalone/frontend/README.md` for excellent example.

---

## 🟢 Medium Priority (Polish Phase) - 5 tasks

### Task 12-16: Configuration & Optimization

These are smaller improvements for production polish:

12. **Container Name** (5 min) - Add to docker-compose.yml
13. **Environment Variables** (2 hrs) - Expand config options
14. **Connection Pooling** (2 hrs) - Configure DB pool settings
15. **OpenAPI Location** (30 min) - Move to `/api/v1/openapi.json`
16. **Metrics Collection** (3 hrs) - Add Prometheus metrics

---

## 📚 Resources & References

**Documentation:**
- Standalone Module Requirements: `docs/modules/shared/standalone-modules/README.md`
- Your detailed gap analysis: `./2025-11-17-backend-gap-analysis.md`
- Backend spec: `docs/modules/backend-architecture/Backend-Architecture-Spec.md`

**Reference Implementations:**
- **Frontend module** (`modules/standalone/frontend/`) - Excellent example of:
  - README structure
  - Environment variable documentation
  - Testing patterns
  - Production optimization

- **AI module** (`modules/standalone/ai/`) - Good example of:
  - Alembic migrations setup
  - Structured logging configuration
  - Health checks

**Getting Help:**
- If stuck >30 minutes on any task, ask for help
- Questions about migrations? Check AI module's setup
- Questions about documentation? Check Frontend module's README
- Questions about the spec? Reference Standalone Module Requirements

---

## 💡 Tips for Success

1. **Work incrementally** - Complete one task fully before starting the next
2. **Test as you go** - Run tests after each change to catch issues early
3. **Commit frequently** - Small commits make it easier to undo mistakes
4. **Ask questions** - Don't waste time being stuck
5. **Use examples** - Frontend and AI modules have working implementations to reference

---

## ✅ Completion Checklist

When all tasks are complete, verify:

- [ ] All Critical tasks completed and tested
- [ ] Tests passing (`pytest tests/`)
- [ ] Server starts without errors (`uvicorn src.api.app:app`)
- [ ] Health endpoint works (`curl http://localhost:8000/health`)
- [ ] API endpoints work with `/api/v1` prefix
- [ ] Migrations run successfully (`alembic upgrade head`)
- [ ] README.md created and comprehensive
- [ ] Logging outputs JSON format
- [ ] Authentication validates real credentials

---

**Questions or Issues?** Contact the team or check the references above.

**Good luck! Your foundation is solid - this is about adding the production-ready polish.** 🚀
