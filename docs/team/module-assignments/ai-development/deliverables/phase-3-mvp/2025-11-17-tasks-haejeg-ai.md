# Task List for haejeg - AI Module

**Module:** AI Development (ai-development)

**Developer:** haejeg

**Review Date:** 2025-11-17

**Total Gaps Identified:** 7

**Overall Status:** ⚠️ INFRASTRUCTURE ONLY - No application service found during testing

**🧪 Test Results:** ⚠️ Infrastructure operational but missing AI application service

---

## 🧪 Module Testing Results

**Testing Date:** 2025-11-17 16:36:00

**Status:** ⚠️ INFRASTRUCTURE ONLY

**What Works:**
- ✅ PostgreSQL database running and healthy
- ✅ Qdrant vector database operational
- ✅ RabbitMQ message queue running

**Critical Issue:**
❌ **NO APPLICATION SERVICE FOUND**
- docker-compose.yml defines infrastructure services only
- No FastAPI application container configured
- No AI module API endpoints accessible
- Cannot test API functionality

**Impact:**
- Cannot verify API path structure
- Cannot test endpoints
- Cannot validate response formats
- Module incomplete for standalone testing

**Recommendation:**
Add application service to docker-compose.yml following this pattern:
```yaml
services:
  app:
    build: .
    container_name: ai-module
    ports:
      - "8001:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - QDRANT_URL=http://qdrant:6333
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
    depends_on:
      - postgres
      - qdrant
      - rabbitmq
```

**Note:** The gaps identified below assume an application service exists. Priority should be adding the application service first.

---

## Critical Priority (Must Complete) - 3 tasks

### 0. Add Application Service to docker-compose.yml ⏱️ 1 hour

**What's Missing:**
The AI module docker-compose.yml only defines infrastructure services (PostgreSQL, Qdrant, RabbitMQ) but no application service to run the FastAPI API.

**Testing Evidence:**
During integration testing, only infrastructure containers were found running. No API endpoints were accessible.

**What You Need to Do:**

**Step 1: Verify Dockerfile Exists** (5 minutes)
```bash
cd modules/standalone/ai
ls -l Dockerfile  # Should exist from your development work
```

**Step 2: Add App Service to docker-compose.yml** (30 minutes)

Add this service to your `docker-compose.yml`:
```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ai-module
    ports:
      - "8001:8000"  # External:Internal
    environment:
      - DATABASE_URL=postgresql+psycopg://ai_user:ai_password@postgres:5432/ai_db
      - QDRANT_URL=http://qdrant:6333
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
      - LOG_LEVEL=INFO
      - MODULE_ID=ai
    depends_on:
      postgres:
        condition: service_healthy
      qdrant:
        condition: service_started
      rabbitmq:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    volumes:
      - ./src:/app/src  # For development hot reload
    command: uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Step 3: Test Application Launch** (20 minutes)
```bash
# Start all services
docker compose up -d

# Check all containers running
docker compose ps

# Should see:
# - ai-postgres (healthy)
# - ai-qdrant (up)
# - ai-rabbitmq (up)
# - ai-module (healthy) ← NEW!

# Test health endpoint
curl http://localhost:8001/health

# Test API endpoints
curl http://localhost:8001/api/v1/extraction
```

**Step 4: Update README** (5 minutes)

Document how to run the module:
```markdown
## Quick Start

1. Start all services:
   ```bash
   docker compose up -d
   ```

2. Check health:
   ```bash
   curl http://localhost:8001/health
   ```

3. Access API docs:
   http://localhost:8001/api/v1/docs
```

**Files to Modify:**
- `docker-compose.yml` (add app service)
- `README.md` (add quick start instructions)
- Verify `Dockerfile` exists and is correct

**Why This Matters:**
Without the application service, the AI module cannot be tested or used in standalone mode. This is a CRITICAL blocker for integration.

**Priority:** CRITICAL - Must be completed before any other tasks

---

### 1. Standardize API Paths to /api/v1
- **Gap:** Routes use `/ai/v1/*` instead of `/api/v1/*`
- **Files:**
  - `src/api/health.py` (change `prefix="/ai/v1"` to `prefix="/api/v1"`)
  - `src/api/extraction.py` (verify prefix)
  - `src/api/graph_query.py` (verify prefix)
  - `src/api/quality.py` (verify prefix)
  - `src/api/websocket.py` (verify prefix)
  - Move root `/health` to `/health` (not `/ai/v1/health`)
  - Update Dockerfile healthcheck (line 48)
  - Update all tests
- **Reference:** Standalone Module Requirements - API Standards
- **Effort:** 2 hours
- **Why:** Breaking change for API contract - must match spec

### 2. Create README.md
- **Gap:** No README in module directory
- **Files:**
  - Create: `modules/standalone/ai/README.md`
  - Sections: Overview, Features, Quick Start, Installation, Running, Tests, API Endpoints, Environment Variables, Migrations, Dependencies, Troubleshooting
  - Include: Mock mode documentation
  - Example API calls
- **Reference:** Frontend `README.md` as template
- **Effort:** 2 hours
- **Why:** Developer onboarding and documentation

**Critical Total:** 4 hours

---

## High Priority (Should Complete) - 3 tasks

### 3. Implement Database Schema Naming
- **Gap:** Models likely using default `public` schema
- **Files:**
  - `src/models/entity.py` (add `__table_args__ = {"schema": "ai_entities"}`)
  - `src/models/relationship.py` (add `__table_args__ = {"schema": "ai_entities"}`)
  - `src/models/knowledge_graph.py` (add schema)
  - `src/models/processing_job.py` (add `__table_args__ = {"schema": "ai_jobs"}`)
  - Alembic migration (create schemas)
- **Effort:** 1 hour
- **Why:** Prevents schema collision with other modules

### 4. Standardize Response Format
- **Gap:** Responses return raw data instead of `{"data": {}, "meta": {}, "errors": []}`
- **Files:**
  - Create: `src/api/responses.py` (StandardResponse wrapper)
  - Update: `src/api/extraction.py` (use wrapper)
  - Update: `src/api/graph_query.py` (use wrapper)
  - Update: `src/api/quality.py` (use wrapper)
  - Update: All tests
- **Effort:** 3 hours
- **Why:** API consistency across all modules

### 5. Implement RFC7807 Error Handling
- **Gap:** Errors use standard FastAPI exceptions
- **Files:**
  - Create: `src/api/errors.py` (ProblemDetail class, exception handler)
  - `src/api/main.py` (register handler)
  - Update: All tests
- **Effort:** 2 hours
- **Why:** Standardized error responses

**High Priority Total:** 6 hours

---

## Medium Priority (Configuration) - 2 tasks

### 6. Configure CORS via Environment Variable
- **Gap:** CORS allows all origins (`allow_origins=["*"]`)
- **Files:**
  - `src/config.py` (add `cors_origins` setting)
  - `src/api/main.py` (update CORS middleware, line 116)
- **Effort:** 30 minutes
- **Why:** Security - should be configurable, not wide open

### 7. Set Container Name
- **Files:** Root `docker-compose.yml` (add `container_name: ai-module`)
- **Effort:** 5 minutes
- **Why:** Service discovery in Docker Compose

**Medium Priority Total:** 35 minutes

---

## Summary

**Total Effort Estimate:** ~10.5 hours (~1.5 days)

**Recommended Phasing:**
1. **This Week:** Critical items (4 hours) - API paths and README
2. **Next Week:** High priority (6 hours) - schemas, response format, errors
3. **Polish:** Medium priority (35 minutes) - CORS and container name

---

## Starting Point

**Start with these 3 tasks in order:**

1. **Fix API paths** (2 hours) - Biggest breaking change, do first
2. **Create README** (2 hours) - Helps others understand your work
3. **Schema naming** (1 hour) - Quick database organization fix

This gets you to 5 hours and covers the most critical items.

---

## Strengths

✅ **Well Implemented:**
- Alembic migrations already in place!
- Structured logging with production/dev modes
- Comprehensive health checks (database, vector DB, LLM, message queue)
- Rate limiting middleware
- WebSocket support
- Multi-stage Docker build
- Good testing setup

⭐ **You're ahead of Backend on migrations!** Great work.

---

## Notes

💡 **Use Frontend as Reference:** The Frontend module has excellent examples of:
- README structure
- Environment variable documentation
- Testing patterns

💡 **Ask for Help:** If the response format standardization is unclear, check how Frontend handles API responses or ask for examples.

---

## References

- **Gap Analysis:** `.dev/ai/reports/2025-11-17-ai-gap-analysis.md`
- **Standalone Requirements:** `docs/modules/shared/standalone-modules/README.md`
- **Frontend Example:** `modules/standalone/frontend/` (reference for README and best practices)
