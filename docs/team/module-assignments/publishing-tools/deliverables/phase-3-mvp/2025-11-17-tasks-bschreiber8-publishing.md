# Task List for bschreiber8 - Publishing Module

**Module:** Publishing System (publishing-tools)

**Developer:** bschreiber8

**Review Date:** 2025-11-17

**Total Gaps Identified:** 7

**Overall Status:** Good documentation (README, QUICKSTART), needs migrations and standardization

---

## Critical Priority (Must Complete) - 2 tasks

### 1. Implement Migration System
- **Gap:** No Alembic migrations directory found
- **Files:**
  - Initialize: `alembic init alembic`
  - Configure: `alembic.ini`
  - Create migration: `alembic revision --autogenerate -m "Initial schema"`
  - Update startup code (remove any create_all calls)
  - Update Dockerfile (copy alembic directory)
  - Update README (add migration instructions)
- **Reference:** AI module has good Alembic setup - use as example
- **Effort:** 3 hours
- **Why:** Cannot safely manage database changes without migrations

### 2. Verify and Fix API Paths
- **Gap:** Need to verify all endpoints use `/api/v1` prefix
- **Files:**
  - Check and update all router files
  - Ensure health endpoint at root `/health`
  - Update all tests
  - Verify OpenAPI spec location
- **Reference:** Standalone Module Requirements - API Standards
- **Effort:** 2 hours
- **Why:** API contract compliance

**Critical Total:** 5 hours

---

## High Priority (Should Complete) - 3 tasks

### 3. Implement Database Schema Naming
- **Gap:** Likely using default `public` schema
- **Files:**
  - Add `__table_args__ = {"schema": "publishing_publications"}` to publication models
  - Add `__table_args__ = {"schema": "publishing_subscribers"}` to subscriber models
  - Add `__table_args__ = {"schema": "publishing_channels"}` to channel models
  - Add `__table_args__ = {"schema": "publishing_analytics"}` to analytics models
  - Alembic migration (create schemas)
- **Effort:** 1 hour
- **Why:** Prevents schema collision with other modules

### 4. Standardize Response Format
- **Gap:** Likely using direct responses instead of standard envelope
- **Files:**
  - Create: `src/responses.py` (StandardResponse wrapper)
  - Update: All API endpoint files
  - Update: All tests
- **Effort:** 3 hours
- **Why:** API consistency across all modules

### 5. Implement RFC7807 Error Handling
- **Gap:** Likely using standard FastAPI exceptions
- **Files:**
  - Create: `src/errors.py` (ProblemDetail class, exception handler)
  - Update: Main application file (register handler)
  - Update: All tests
- **Effort:** 2 hours
- **Why:** Standardized error responses

**High Priority Total:** 6 hours

---

## Medium Priority (Configuration) - 2 tasks

### 6. Verify Port Configuration
- **Gap:** Using port 8080 (within range but could standardize)
- **Files:** Consider changing to 8003 for consistency (optional)
- **Effort:** 5 minutes
- **Why:** Consistency across modules (Backend=8000, Frontend=3000, AI=8001, Publishing=8003?)

### 7. Set Container Name
- **Files:** Root `docker-compose.yml` (add `container_name: publishing-module`)
- **Effort:** 5 minutes
- **Why:** Service discovery in Docker Compose

**Medium Priority Total:** 10 minutes

---

## Summary

**Total Effort Estimate:** ~11 hours (~1.5 days)

**Recommended Phasing:**
1. **This Week:** Critical items (5 hours) - migrations and API paths
2. **Next Week:** High priority (6 hours) - schemas, response format, errors
3. **Polish:** Medium priority (10 minutes) - port and container name

---

## Starting Point

**Start with these 3 tasks in order:**

1. **Implement migrations** (3 hours) - Foundation for all database work
   - Look at AI module's `alembic/` directory as example
   - Copy the pattern they used

2. **Verify API paths** (2 hours) - Ensure `/api/v1` prefix everywhere
   - Check main.py and all router files
   - Make sure health is at `/health` root

3. **Schema naming** (1 hour) - Quick database organization fix
   - Add `__table_args__` to all models
   - Create schemas in first migration

This gets you to 6 hours and covers the most critical foundation items.

---

## Strengths

✅ **Excellent Documentation:**
- README.md with comprehensive info
- QUICKSTART.md for quick setup
- IMPLEMENTATION-STATUS.md tracking progress
- Docker healthcheck configured
- Python 3.11 used

⭐ **Your documentation is top-notch!** Keep that up.

---

## Notes

💡 **Use AI Module as Example:** The AI module already has Alembic migrations set up. Look at:
- `modules/standalone/ai/alembic/` directory structure
- `modules/standalone/ai/alembic.ini` configuration
- How they organize migrations

💡 **Use Frontend for Best Practices:** Frontend has excellent examples of documentation and structure.

💡 **Ask for Help:** If Alembic setup is unclear, ask for guidance - it's important to get right!

---

## Database Organization

When you add schema naming, organize like this:

- `publishing_publications` - Publication records
- `publishing_subscribers` - Subscriber management
- `publishing_channels` - Email/Slack/Discord integrations
- `publishing_analytics` - Metrics and tracking

This keeps your data separate from other modules.

---

## References

- **Gap Analysis:** `.dev/ai/reports/2025-11-17-publishing-gap-analysis.md`
- **Standalone Requirements:** `docs/modules/shared/standalone-modules/README.md`
- **AI Module Migrations:** `modules/standalone/ai/alembic/` (example to follow)
- **Frontend Documentation:** `modules/standalone/frontend/` (reference for docs quality)
