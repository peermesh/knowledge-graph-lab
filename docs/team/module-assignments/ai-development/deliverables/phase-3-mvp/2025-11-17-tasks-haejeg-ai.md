# Task List for haejeg - AI Module

**Module:** AI Development (ai-development)

**Developer:** haejeg

**Review Date:** 2025-11-17

**Total Gaps Identified:** 7

**Overall Status:** Strong architecture with Alembic, structured logging, health checks - needs standardization

---

## Critical Priority (Must Complete) - 2 tasks

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
