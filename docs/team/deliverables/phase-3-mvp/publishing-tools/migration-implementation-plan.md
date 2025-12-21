# Migration Implementation Plan for Publishing Module

**Date:** 2025-11-17  
**Developer:** bschreiber8  
**Task Reference:** `2025-11-17-tasks-bschreiber8-publishing.md` - Task #2: Implement Migration System

---

## Executive Summary

This plan outlines the implementation of Alembic database migrations for the Publishing Module. Currently, the module uses `Base.metadata.create_all()` to create tables on startup, which works for development but is unsafe for production. We will replace this with a proper Alembic migration system that allows version-controlled schema changes, rollback capability, and safe production deployments.

---

## Current State Analysis

### Current Database Setup

**Location:** `src/publishing/core/database.py`

**Current Implementation:**
- Line 52-68: `create_db_and_tables()` function calls `Base.metadata.create_all` on startup
- Line 172-190: `init_database_for_testing()` also uses `create_all` for test databases
- Called from `src/publishing/main.py` line 46 in the `lifespan` startup function

**Problems:**
1. No version control for schema changes
2. Cannot rollback schema changes
3. Cannot track migration history
4. Unsafe for production (schema changes happen automatically on startup)
5. No way to apply incremental schema updates

### Existing Migration Files

**Location:** `src/publishing/migrations/`

**Files Found:**
- `001_create_publishing_analytics.py`
- `001_initial_schema.py`
- `002_create_publishing_subscribers.py`
- `003_create_publishing_templates.py`

**Status:** These appear to be old migration files, not Alembic migrations. They will need to be reviewed and potentially incorporated into the initial Alembic migration.

### Reference Implementation

**Location:** `modules/standalone/ai/alembic/`

The AI module has a working Alembic setup that we can use as a reference:
- `alembic/env.py` - Configured with proper model imports and database URL
- `alembic/versions/001_initial_schema.py` - Example initial migration
- Uses async SQLAlchemy compatible setup

---

## Implementation Plan

### Phase 1: Initialize Alembic (15 minutes)

#### Step 1.1: Install Alembic (if not already installed)

**Action:** Verify Alembic is in `requirements.txt` or add it.

**Files to Check/Modify:**
- `modules/standalone/publishing/requirements.txt` (or root `requirements.txt`)

**Expected Change:**
```txt
alembic>=1.12.0
```

#### Step 1.2: Initialize Alembic Directory

**Action:** Run `alembic init` command in the appropriate directory.

**Command:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab/src/publishing
alembic init alembic
```

**Expected Result:**
- New directory: `src/publishing/alembic/`
- New file: `src/publishing/alembic.ini`
- New directory: `src/publishing/alembic/versions/`
- New files: `src/publishing/alembic/env.py`, `src/publishing/alembic/script.py.mako`

**Why:** Creates the Alembic directory structure and configuration files.

---

### Phase 2: Configure Alembic (30 minutes)

#### Step 2.1: Update `alembic.ini`

**File:** `src/publishing/alembic.ini`

**Changes Needed:**
- Update `sqlalchemy.url` to use environment variable or remove (will be set in `env.py`)
- Verify `script_location` points to `alembic`

**Expected Configuration:**
```ini
[alembic]
script_location = alembic
# sqlalchemy.url = driver://user:pass@localhost/dbname
# (URL will be set dynamically in env.py)
```

**Why:** Alembic needs to know where migration scripts are located. The database URL will be set dynamically from settings.

#### Step 2.2: Configure `alembic/env.py`

**File:** `src/publishing/alembic/env.py`

**Changes Needed:**

1. **Add path setup for imports:**
```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
```

2. **Import settings and Base:**
```python
from src.publishing.core.config import settings
from src.publishing.core.database import Base
```

3. **Import all models to register with Base:**
```python
# Import all models to ensure they're registered with Base
from src.publishing.models import channel, publication, subscriber, template, analytics  # noqa: F401
```

4. **Set target metadata:**
```python
target_metadata = Base.metadata
```

5. **Set database URL from settings:**
```python
# Set database URL from settings
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
```

6. **Update `run_migrations_online()` for async support:**
   - The AI module uses synchronous engine, but we need async support
   - May need to use `run_sync` wrapper or configure for async SQLAlchemy

**Reference:** `modules/standalone/ai/alembic/env.py` (lines 1-61)

**Why:** Alembic needs to know:
- Where to find the models (Base.metadata)
- What database to connect to (from settings)
- All models must be imported so they register with Base

**Note:** Since we're using async SQLAlchemy, we may need special handling. The AI module uses sync, so we'll need to adapt.

#### Step 2.3: Handle Async SQLAlchemy Compatibility

**Challenge:** Alembic works with synchronous engines by default, but we're using async SQLAlchemy.

**Solution Options:**

**Option A:** Use sync engine for migrations (recommended)
- Create a synchronous engine in `env.py` for migrations only
- Keep async engine for application code
- Migrations don't need async since they're one-off operations

**Option B:** Use async-compatible Alembic
- Requires `alembic[asyncio]` or custom async support
- More complex but keeps everything async

**Recommended:** Option A - Use sync engine for migrations

**Implementation in `env.py`:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Create sync engine for migrations (Alembic doesn't support async directly)
    sync_url = settings.DATABASE_URL.replace('+asyncpg', '').replace('postgresql+asyncpg', 'postgresql')
    connectable = create_engine(
        sync_url,
        poolclass=NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

**Why:** Alembic's migration system works with synchronous connections. We can convert the async URL to sync for migrations.

---

### Phase 3: Create Initial Migration (30 minutes)

#### Step 3.1: Generate Initial Migration

**Action:** Use Alembic's autogenerate feature to create initial migration from existing models.

**Command:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab/src/publishing
alembic revision --autogenerate -m "Initial schema for publications and channels"
```

**Expected Result:**
- New file: `src/publishing/alembic/versions/XXXX_initial_schema_for_publications_and_channels.py`
- Contains `upgrade()` function with all table creation statements
- Contains `downgrade()` function with all table drop statements

**Why:** Autogenerate creates migration scripts by comparing current models with database state. Since we're starting fresh, this will create all tables.

#### Step 3.2: Review Generated Migration

**Action:** Manually review the generated migration file.

**Things to Check:**
1. All expected tables are created:
   - `publishing_channels`
   - `publishing_subscribers`
   - `publishing_publications`
   - `publishing_templates`
   - `publishing_analytics`
2. All columns, indexes, and constraints are correct
3. Foreign keys are properly defined
4. No unexpected or missing tables

**Files to Review:**
- `src/publishing/alembic/versions/XXXX_initial_schema_for_publications_and_channels.py`
- Compare with model definitions in `src/publishing/models/`

**Why:** Autogenerate can miss some things or include things we don't want. Manual review ensures correctness.

#### Step 3.3: Incorporate Existing Migration Files (if needed)

**Action:** Review old migration files in `src/publishing/migrations/` to see if they contain important schema information not captured by autogenerate.

**Files to Review:**
- `src/publishing/migrations/001_create_publishing_analytics.py`
- `src/publishing/migrations/001_initial_schema.py`
- `src/publishing/migrations/002_create_publishing_subscribers.py`
- `src/publishing/migrations/003_create_publishing_templates.py`

**Decision:** If these contain important schema details, incorporate them into the initial Alembic migration. Otherwise, they can be archived.

**Why:** Ensure we don't lose any important schema definitions from previous work.

---

### Phase 4: Update Application Startup (15 minutes)

#### Step 4.1: Remove `create_all` from Startup

**File:** `src/publishing/core/database.py`

**Current Code (lines 52-68):**
```python
async def create_db_and_tables() -> None:
    """Create database tables from SQLAlchemy models."""
    try:
        logger.info("Creating database tables", database=settings.DATABASE_NAME)

        # Import all models to ensure they're registered with Base
        from ..models import channel, publication, subscriber, template, analytics  # noqa: F401

        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Database tables created successfully")

    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
        raise
```

**New Code:**
```python
async def create_db_and_tables() -> None:
    """
    Database tables are managed by Alembic migrations.
    
    To apply migrations, run:
        alembic upgrade head
    
    This function is kept for backward compatibility but does nothing.
    In production, migrations should be run as part of deployment pipeline.
    """
    logger.info(
        "Database initialization skipped - tables managed by Alembic migrations",
        database=settings.DATABASE_NAME
    )
    logger.info(
        "To apply migrations, run: alembic upgrade head",
        database=settings.DATABASE_NAME
    )
    # No-op: Tables are created via Alembic migrations
    pass
```

**Why:** Remove automatic table creation. Tables will be created/managed by Alembic migrations instead.

#### Step 4.2: Update Test Database Initialization (if needed)

**File:** `src/publishing/core/database.py`

**Current Code (lines 172-190):**
```python
async def init_database_for_testing() -> None:
    """Initialize database for testing with test-specific configuration."""
    if settings.DEBUG:
        logger.info("Initializing database for testing")

        # Use in-memory SQLite for tests if PostgreSQL not available
        test_engine = create_async_engine(
            "sqlite+aiosqlite:///./test_publishing.db",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Test database initialized")
    else:
        logger.warning("Test database initialization skipped in production mode")
```

**Decision:** For tests, we have two options:

**Option A:** Keep `create_all` for tests (simpler, faster)
- Tests can still use `create_all` for speed
- Production uses migrations

**Option B:** Use migrations in tests too (more realistic)
- Tests run migrations before running
- More realistic but slower

**Recommended:** Option A - Keep `create_all` for tests, use migrations for production.

**Why:** Tests need to be fast. Using `create_all` in tests is acceptable since test databases are ephemeral.

#### Step 4.3: Add Migration Documentation Comment

**File:** `src/publishing/main.py`

**Location:** Near the `create_db_and_tables()` call (line 46)

**Add Comment:**
```python
# Initialize database
# Note: Database tables are managed by Alembic migrations.
# Run 'alembic upgrade head' to apply migrations.
# The create_db_and_tables() function is kept for compatibility but does nothing.
try:
    await create_db_and_tables()
    logger.info("Database initialized successfully")
except Exception as e:
    if settings.DEBUG:
        logger.warning("DEBUG mode: Database init failed, using in-memory stores", error=str(e))
    else:
        raise
```

**Why:** Document that migrations are required and how to run them.

---

### Phase 5: Test Migrations (1 hour)

#### Step 5.1: Reset Test Database

**Action:** Start with a clean database to test migrations.

**Commands:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab/modules/standalone/publishing
docker compose down -v  # Remove volumes to delete database
docker compose up -d postgres redis  # Start only database services
```

**Why:** Need a clean database to test that migrations create tables correctly.

#### Step 5.2: Run Initial Migration

**Action:** Apply the initial migration to create all tables.

**Command:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab/src/publishing
alembic upgrade head
```

**Expected Result:**
- Migration runs successfully
- All tables are created in the database
- No errors in output

**Why:** Verify that migrations work correctly.

#### Step 5.3: Verify Tables Created

**Action:** Check that all expected tables exist in the database.

**Command:**
```bash
docker exec -it publishing-postgres-1 psql -U publishing_user -d publishing_db -c "\dt"
```

**Expected Output:**
- `publishing_channels`
- `publishing_subscribers`
- `publishing_publications`
- `publishing_templates`
- `publishing_analytics`
- `alembic_version` (Alembic's version tracking table)

**Why:** Confirm that all tables were created correctly.

#### Step 5.4: Test Application Startup

**Action:** Start the application and verify it works without `create_all`.

**Commands:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab/modules/standalone/publishing
docker compose up -d
```

**Expected Result:**
- Application starts successfully
- No errors about missing tables
- Health endpoint returns success
- API endpoints work correctly

**Why:** Ensure the application works correctly with migrations instead of `create_all`.

#### Step 5.5: Test Migration Rollback (Optional but Recommended)

**Action:** Test that we can rollback migrations if needed.

**Command:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab/src/publishing
alembic downgrade -1  # Rollback one migration
alembic upgrade head   # Apply again
```

**Expected Result:**
- Rollback succeeds (tables are dropped)
- Re-apply succeeds (tables are recreated)

**Why:** Verify that rollback works for safety in production.

#### Step 5.6: Test on Fresh Database

**Action:** Test the full workflow from scratch.

**Commands:**
```bash
# Reset everything
docker compose down -v
docker compose up -d postgres redis

# Run migrations
cd src/publishing
alembic upgrade head

# Start application
cd ../../modules/standalone/publishing
docker compose up -d
```

**Expected Result:**
- Everything works from a completely fresh start
- No manual table creation needed

**Why:** Simulate a production deployment scenario.

---

## Files to Create/Modify

### New Files to Create

1. **`src/publishing/alembic.ini`**
   - Alembic configuration file
   - Created by `alembic init`

2. **`src/publishing/alembic/env.py`**
   - Alembic environment configuration
   - Created by `alembic init`, then modified

3. **`src/publishing/alembic/script.py.mako`**
   - Migration script template
   - Created by `alembic init` (usually no changes needed)

4. **`src/publishing/alembic/versions/XXXX_initial_schema_for_publications_and_channels.py`**
   - Initial migration script
   - Created by `alembic revision --autogenerate`

### Files to Modify

1. **`src/publishing/core/database.py`**
   - Modify `create_db_and_tables()` to be a no-op
   - Add documentation about migrations
   - Keep `init_database_for_testing()` as-is (for test speed)

2. **`src/publishing/main.py`**
   - Add comment about migrations near `create_db_and_tables()` call
   - No functional changes needed

3. **`modules/standalone/publishing/requirements.txt`** (or root `requirements.txt`)
   - Add `alembic>=1.12.0` if not present

### Files to Review (No Changes)

1. **`src/publishing/migrations/*.py`**
   - Review old migration files
   - Archive or incorporate into Alembic migration

---

## Configuration Changes

### Environment Variables

**No new environment variables needed.** Alembic will use the existing `DATABASE_URL` from `src/publishing/core/config.py`.

### Docker Configuration

**No changes to `docker-compose.yml` needed.** However, we may want to add a migration service in the future for automated migrations on container startup (not in this phase).

---

## Migration Workflow for Future Changes

After this implementation, future schema changes will follow this workflow:

1. **Modify Models:** Update SQLAlchemy models in `src/publishing/models/`
2. **Generate Migration:** Run `alembic revision --autogenerate -m "Description of changes"`
3. **Review Migration:** Check the generated migration file
4. **Test Migration:** Run `alembic upgrade head` and test application
5. **Commit:** Commit both model changes and migration file
6. **Deploy:** Run `alembic upgrade head` as part of deployment

---

## Rollback Strategy

If something goes wrong:

1. **Rollback Migration:** `alembic downgrade -1` (rollback one migration)
2. **Fix Issue:** Correct the migration file or models
3. **Re-apply:** `alembic upgrade head`

For production:
- Always test migrations on staging first
- Have database backups before running migrations
- Use `alembic upgrade head --sql` to preview SQL before applying

---

## Testing Checklist

- [ ] Alembic initialized successfully
- [ ] `alembic.ini` configured correctly
- [ ] `alembic/env.py` configured with models and database URL
- [ ] Initial migration generated successfully
- [ ] Migration file reviewed and correct
- [ ] Migration applies successfully (`alembic upgrade head`)
- [ ] All tables created in database
- [ ] Application starts without errors
- [ ] API endpoints work correctly
- [ ] Migration rollback works (`alembic downgrade -1`)
- [ ] Full workflow tested from fresh database
- [ ] Documentation updated

---

## Success Criteria

1. ✅ Alembic is initialized and configured
2. ✅ Initial migration creates all required tables
3. ✅ Application no longer uses `create_all` on startup
4. ✅ Migrations can be applied and rolled back
5. ✅ Application works correctly with migrations
6. ✅ All tests pass
7. ✅ Documentation is updated

---

## Estimated Time

**Total: ~3 hours**

- Phase 1 (Initialize): 15 minutes
- Phase 2 (Configure): 30 minutes
- Phase 3 (Create Migration): 30 minutes
- Phase 4 (Update Startup): 15 minutes
- Phase 5 (Test): 1 hour
- Buffer for issues: 30 minutes

---

## Risks and Mitigations

### Risk 1: Async SQLAlchemy Compatibility
**Risk:** Alembic doesn't natively support async SQLAlchemy  
**Mitigation:** Use synchronous engine in `env.py` for migrations only. This is standard practice.

### Risk 2: Missing Models in Migration
**Risk:** Autogenerate might miss some models  
**Mitigation:** Manually review migration file and compare with all model files.

### Risk 3: Existing Data Loss
**Risk:** If database already has data, migration might fail  
**Mitigation:** This is for initial setup. If database has data, we'll need to handle it differently (data migration).

### Risk 4: Test Failures
**Risk:** Tests might fail if they expect `create_all` behavior  
**Mitigation:** Keep `init_database_for_testing()` using `create_all` for test speed.

---

## References

- **Task File:** `docs/team/deliverables/phase-3-mvp/publishing-tools/2025-11-17-tasks-bschreiber8-publishing.md`
- **AI Module Reference:** `modules/standalone/ai/alembic/`
- **Alembic Documentation:** https://alembic.sqlalchemy.org/
- **SQLAlchemy Async Guide:** https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

---

## Next Steps After Implementation

1. Update `QUICKSTART.md` to include migration instructions
2. Add migration step to deployment documentation
3. Consider adding automated migration service to docker-compose (future enhancement)
4. Document migration workflow for team

---

**End of Plan**

