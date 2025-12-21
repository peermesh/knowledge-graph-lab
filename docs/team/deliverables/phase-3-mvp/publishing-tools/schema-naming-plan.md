# Database Schema Naming Implementation Plan

**Date:** 2025-11-17  
**Developer:** bschreiber8  
**Task Reference:** `2025-11-17-tasks-bschreiber8-publishing.md` - Task #5: Implement Database Schema Naming

---

## Executive Summary

This plan outlines the implementation of PostgreSQL schema organization for the publishing module. Currently, all tables use the default `public` schema with `publishing_` prefixed table names. This change will organize tables into dedicated PostgreSQL schemas to prevent collisions with other modules and improve database organization.

---

## Current State Analysis

### Current Table Structure

**All tables are in the `public` schema with prefixed names:**

1. **Channel Model** (`src/publishing/models/channel.py`)
   - Table: `publishing_channels`
   - Schema: `public` (default)

2. **Publication Model** (`src/publishing/models/publication.py`)
   - Table: `publishing_publications`
   - Schema: `public` (default)

3. **Subscriber Model** (`src/publishing/models/subscriber.py`)
   - Table: `publishing_subscribers`
   - Schema: `public` (default)

4. **Template Model** (`src/publishing/models/template.py`)
   - Table: `publishing_templates`
   - Schema: `public` (default)

5. **Analytics Model** (`src/publishing/models/analytics.py`)
   - Table: `publishing_analytics`
   - Schema: `public` (default)

### Current Model Structure

**Example (Channel model):**
```python
class Channel(Base):
    __tablename__ = 'publishing_channels'
    # No __table_args__ specified, defaults to 'public' schema
```

### Problem Statement

**Issue:** All tables use the default `public` schema, which can cause:
- Table name collisions when multiple modules share a database
- Difficulty in organizing and managing module-specific tables
- Lack of proper namespace isolation
- Harder to apply module-specific permissions

**Solution:** Organize tables into dedicated PostgreSQL schemas.

---

## Implementation Strategy

### Approach Decision

**Task Description Suggests:** Separate schemas per table type
- `publishing_publications` schema for publications table
- `publishing_channels` schema for channels table
- etc.

**Alternative Approach (More Conventional):** Single `publishing` schema for all tables
- All publishing tables in one `publishing` schema
- Simpler to manage and more conventional

**Decision:** Follow task description exactly, but note the alternative in documentation.

### Schema Organization

**Per Task Description:**
- Schema: `publishing_publications` → Table: `publications`
- Schema: `publishing_channels` → Table: `channels`
- Schema: `publishing_subscribers` → Table: `subscribers`
- Schema: `publishing_templates` → Table: `templates`
- Schema: `publishing_analytics` → Table: `analytics`

**Note:** This creates 5 separate schemas. A single `publishing` schema would be more conventional, but we'll follow the task specification.

---

## Implementation Plan

### Phase 1: Update Model Definitions (20 minutes)

#### Step 1.1: Update Channel Model

**File:** `src/publishing/models/channel.py`

**Current:**
```python
class Channel(Base):
    __tablename__ = 'publishing_channels'
```

**Updated:**
```python
class Channel(Base):
    __tablename__ = 'channels'
    __table_args__ = {"schema": "publishing_channels"}
```

**Changes:**
- Table name: `publishing_channels` → `channels`
- Add `__table_args__` with schema: `publishing_channels`

#### Step 1.2: Update Publication Model

**File:** `src/publishing/models/publication.py`

**Current:**
```python
class Publication(Base):
    __tablename__ = 'publishing_publications'
```

**Updated:**
```python
class Publication(Base):
    __tablename__ = 'publications'
    __table_args__ = {"schema": "publishing_publications"}
```

**Changes:**
- Table name: `publishing_publications` → `publications`
- Add `__table_args__` with schema: `publishing_publications`

#### Step 1.3: Update Subscriber Model

**File:** `src/publishing/models/subscriber.py`

**Current:**
```python
class Subscriber(Base):
    __tablename__ = 'publishing_subscribers'
```

**Updated:**
```python
class Subscriber(Base):
    __tablename__ = 'subscribers'
    __table_args__ = {"schema": "publishing_subscribers"}
```

**Changes:**
- Table name: `publishing_subscribers` → `subscribers`
- Add `__table_args__` with schema: `publishing_subscribers`

#### Step 1.4: Update Template Model

**File:** `src/publishing/models/template.py`

**Current:**
```python
class Template(Base):
    __tablename__ = 'publishing_templates'
```

**Updated:**
```python
class Template(Base):
    __tablename__ = 'templates'
    __table_args__ = {"schema": "publishing_templates"}
```

**Changes:**
- Table name: `publishing_templates` → `templates`
- Add `__table_args__` with schema: `publishing_templates`

#### Step 1.5: Update Analytics Model

**File:** `src/publishing/models/analytics.py`

**Current:**
```python
class Analytics(Base):
    __tablename__ = 'publishing_analytics'
```

**Updated:**
```python
class Analytics(Base):
    __tablename__ = 'analytics'
    __table_args__ = {"schema": "publishing_analytics"}
```

**Changes:**
- Table name: `publishing_analytics` → `analytics`
- Add `__table_args__` with schema: `publishing_analytics`

---

### Phase 2: Create Migration (20 minutes)

#### Step 2.1: Generate Migration

**Action:** Create a new Alembic migration to:
1. Create the new schemas
2. Move existing tables to new schemas (or create new tables in schemas)
3. Handle data migration if needed

**Command:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab
alembic revision -m "Add schema organization for publishing module"
```

**Why:** Need to create a migration that handles schema creation and table movement.

#### Step 2.2: Write Migration Script

**File:** `src/publishing/alembic/versions/002_add_schema_organization.py`

**Migration Steps:**
1. Create schemas:
   - `publishing_publications`
   - `publishing_channels`
   - `publishing_subscribers`
   - `publishing_templates`
   - `publishing_analytics`

2. Move tables to new schemas:
   - Move `public.publishing_publications` → `publishing_publications.publications`
   - Move `public.publishing_channels` → `publishing_channels.channels`
   - Move `public.publishing_subscribers` → `publishing_subscribers.subscribers`
   - Move `public.publishing_templates` → `publishing_templates.templates`
   - Move `public.publishing_analytics` → `publishing_analytics.analytics`

3. Update indexes to reference new schema-qualified table names

**Migration Template:**
```python
"""Add schema organization for publishing module

Revision ID: 002
Revises: 001
Create Date: 2025-11-17

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create schemas
    op.execute('CREATE SCHEMA IF NOT EXISTS publishing_publications')
    op.execute('CREATE SCHEMA IF NOT EXISTS publishing_channels')
    op.execute('CREATE SCHEMA IF NOT EXISTS publishing_subscribers')
    op.execute('CREATE SCHEMA IF NOT EXISTS publishing_templates')
    op.execute('CREATE SCHEMA IF NOT EXISTS publishing_analytics')
    
    # Move tables to new schemas
    # Note: PostgreSQL doesn't support direct schema move, need to:
    # 1. Create new table in target schema
    # 2. Copy data
    # 3. Drop old table
    # 4. Rename new table if needed
    
    # For each table:
    # - Create table in new schema with new name
    # - Copy data from old table
    # - Drop old table
    # - Recreate indexes in new schema


def downgrade() -> None:
    # Reverse the process
    # Move tables back to public schema with old names
    # Drop schemas
    pass
```

**Important Considerations:**
- PostgreSQL doesn't support `ALTER TABLE ... SET SCHEMA` directly for moving tables
- Need to create new tables, copy data, drop old tables
- Must preserve all indexes, constraints, and data
- Handle foreign key relationships if any exist

#### Step 2.3: Handle Data Migration

**Strategy:**
1. Check if tables exist and have data
2. If empty: Create new tables in schemas, drop old ones
3. If has data: Create new tables, copy data, drop old tables

**SQL Pattern:**
```sql
-- Create new table in schema
CREATE TABLE publishing_publications.publications AS 
SELECT * FROM public.publishing_publications;

-- Copy indexes
-- Copy constraints
-- Copy data

-- Drop old table
DROP TABLE public.publishing_publications;
```

---

### Phase 3: Update Code References (15 minutes)

#### Step 3.1: Update Database Queries

**Action:** Search for any hardcoded table names in queries

**Files to Check:**
- `src/publishing/core/database.py` - `get_table_status()` function
- Any raw SQL queries that reference table names
- Service files that might have table name references

**Search Command:**
```bash
grep -rn "publishing_channels\|publishing_publications\|publishing_subscribers\|publishing_templates\|publishing_analytics" src/publishing/ --include="*.py"
```

**Update Pattern:**
- Raw SQL: Update to use schema-qualified names: `publishing_channels.channels`
- ORM queries: Should work automatically with `__table_args__`

#### Step 3.2: Update get_table_status() Function

**File:** `src/publishing/core/database.py`

**Current Query:**
```python
result = await session.execute(text("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name LIKE 'publishing_%'
    ORDER BY table_name
"""))
```

**Updated Query:**
```python
result = await session.execute(text("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema LIKE 'publishing_%'
    ORDER BY table_schema, table_name
"""))
```

**Why:** Need to check new schemas instead of `public` schema.

#### Step 3.3: Update Expected Tables List

**File:** `src/publishing/core/database.py`

**Current:**
```python
expected_tables = [
    'publishing_channels',
    'publishing_subscribers',
    'publishing_publications',
    'publishing_templates',
    'publishing_analytics'
]
```

**Updated:**
```python
expected_tables = [
    ('publishing_channels', 'channels'),
    ('publishing_subscribers', 'subscribers'),
    ('publishing_publications', 'publications'),
    ('publishing_templates', 'templates'),
    ('publishing_analytics', 'analytics')
]
```

**Why:** Tables now have schema-qualified names.

---

### Phase 4: Testing (5 minutes)

#### Step 4.1: Verify Model Definitions

**Action:** Check that all models have correct `__table_args__`

**Command:**
```bash
grep -A 2 "__tablename__" src/publishing/models/*.py
```

**Expected:** All models should have `__table_args__ = {"schema": "..."}`

#### Step 4.2: Test Migration

**Action:** Test migration on a test database

**Steps:**
1. Run migration: `alembic upgrade head`
2. Verify schemas created: `\dn` in psql
3. Verify tables in correct schemas: `\dt publishing_*.*` in psql
4. Verify data preserved: Check row counts
5. Test application: Verify queries work

#### Step 4.3: Test Application

**Action:** Verify application works with new schema structure

**Tests:**
- Health check works
- Database queries work
- All CRUD operations work
- No broken references

---

## Files to Modify

### Model Files (5 files)

1. **`src/publishing/models/channel.py`**
   - Change `__tablename__` from `'publishing_channels'` to `'channels'`
   - Add `__table_args__ = {"schema": "publishing_channels"}`

2. **`src/publishing/models/publication.py`**
   - Change `__tablename__` from `'publishing_publications'` to `'publications'`
   - Add `__table_args__ = {"schema": "publishing_publications"}`

3. **`src/publishing/models/subscriber.py`**
   - Change `__tablename__` from `'publishing_subscribers'` to `'subscribers'`
   - Add `__table_args__ = {"schema": "publishing_subscribers"}`

4. **`src/publishing/models/template.py`**
   - Change `__tablename__` from `'publishing_templates'` to `'templates'`
   - Add `__table_args__ = {"schema": "publishing_templates"}`

5. **`src/publishing/models/analytics.py`**
   - Change `__tablename__` from `'publishing_analytics'` to `'analytics'`
   - Add `__table_args__ = {"schema": "publishing_analytics"}`

### Migration File (1 new file)

6. **`src/publishing/alembic/versions/002_add_schema_organization.py`**
   - Create new migration
   - Create schemas
   - Move tables to new schemas
   - Handle data migration

### Code Files (1 file)

7. **`src/publishing/core/database.py`**
   - Update `get_table_status()` function
   - Update expected tables list
   - Update SQL query to check new schemas

---

## Detailed Code Changes

### Model Changes Example

**Before (Channel model):**
```python
class Channel(Base):
    __tablename__ = 'publishing_channels'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # ... rest of columns
```

**After (Channel model):**
```python
class Channel(Base):
    __tablename__ = 'channels'
    __table_args__ = {"schema": "publishing_channels"}
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # ... rest of columns
```

### Migration Structure

**Migration will:**
1. Create 5 new schemas
2. For each table:
   - Create new table in target schema with new name
   - Copy all data from old table
   - Recreate all indexes
   - Recreate all constraints
   - Drop old table
3. Verify data integrity

---

## Verification Steps

### Step 1: Model Verification
- [ ] All 5 models have `__table_args__` with correct schema
- [ ] All 5 models have simplified table names (no `publishing_` prefix)
- [ ] No syntax errors in model files

### Step 2: Migration Verification
- [ ] Migration file created with correct revision number
- [ ] Migration creates all 5 schemas
- [ ] Migration moves all tables correctly
- [ ] Migration preserves all data
- [ ] Migration preserves all indexes
- [ ] Migration preserves all constraints

### Step 3: Code Verification
- [ ] `get_table_status()` updated to check new schemas
- [ ] No hardcoded table names in queries
- [ ] All ORM queries work correctly

### Step 4: Runtime Verification
- [ ] Application starts without errors
- [ ] Database queries work correctly
- [ ] Health check works
- [ ] All CRUD operations work
- [ ] No broken references

---

## Expected Outcome

### Before
- All tables in `public` schema
- Table names: `publishing_channels`, `publishing_publications`, etc.
- Risk of collisions with other modules

### After
- Tables organized into dedicated schemas
- Table names: `channels`, `publications`, etc. (simplified)
- Schemas: `publishing_channels`, `publishing_publications`, etc.
- Better namespace isolation
- Reduced collision risk

### Schema Structure

```
PostgreSQL Database
├── public (default schema)
│   └── (other module tables)
├── publishing_channels
│   └── channels
├── publishing_publications
│   └── publications
├── publishing_subscribers
│   └── subscribers
├── publishing_templates
│   └── templates
└── publishing_analytics
    └── analytics
```

---

## Testing Checklist

- [ ] All models updated with `__table_args__`
- [ ] Migration file created
- [ ] Migration tested on empty database
- [ ] Migration tested on database with data
- [ ] Data integrity verified after migration
- [ ] Indexes recreated correctly
- [ ] Constraints recreated correctly
- [ ] `get_table_status()` function updated
- [ ] Application works with new schema structure
- [ ] No broken queries or references

---

## Estimated Time

**Total: ~1 hour**

- Phase 1 (Update Models): 20 minutes
- Phase 2 (Create Migration): 20 minutes
- Phase 3 (Update Code References): 15 minutes
- Phase 4 (Testing): 5 minutes

---

## Risks and Mitigations

### Risk 1: Data Loss During Migration
**Risk:** Data might be lost when moving tables  
**Mitigation:** 
- Test migration on copy of database first
- Verify row counts before and after
- Create backup before running migration

### Risk 2: Breaking Existing Queries
**Risk:** Hardcoded table names in queries might break  
**Mitigation:**
- Comprehensive search for all table name references
- Update all hardcoded references
- Test all queries after migration

### Risk 3: Foreign Key Issues
**Risk:** Foreign keys might reference old table names  
**Mitigation:**
- Check for foreign key relationships
- Update foreign key constraints in migration
- Test relationships after migration

### Risk 4: Index Recreation Issues
**Risk:** Indexes might not be recreated correctly  
**Mitigation:**
- List all indexes before migration
- Recreate all indexes in migration
- Verify indexes after migration

### Risk 5: Application Downtime
**Risk:** Migration might require application downtime  
**Mitigation:**
- Plan migration during low-traffic period
- Test migration thoroughly before production
- Have rollback plan ready

---

## Alternative Approach (Noted for Future)

**Single Schema Approach:**
Instead of 5 separate schemas, could use one `publishing` schema:

```python
class Channel(Base):
    __tablename__ = 'channels'
    __table_args__ = {"schema": "publishing"}
```

**Benefits:**
- Simpler to manage
- More conventional PostgreSQL pattern
- Easier permissions management
- Single schema for all publishing tables

**Current Decision:** Follow task specification with separate schemas, but document alternative for future consideration.

---

## PostgreSQL Schema Best Practices

### Schema Naming
- Use lowercase with underscores
- Be descriptive: `publishing_channels` not `pub_chan`
- Keep consistent naming pattern

### Schema Organization
- Group related tables in same schema
- Use schemas for logical separation
- Consider permissions per schema

### Migration Strategy
- Always test migrations on copy first
- Verify data integrity after migration
- Have rollback plan
- Document migration steps

---

## References

- **Task File:** `docs/team/deliverables/phase-3-mvp/publishing-tools/2025-11-17-tasks-bschreiber8-publishing.md`
- **SQLAlchemy Schema Docs:** https://docs.sqlalchemy.org/en/20/core/metadata.html#specifying-the-schema-name
- **PostgreSQL Schema Docs:** https://www.postgresql.org/docs/current/ddl-schemas.html
- **Alembic Migration Docs:** https://alembic.sqlalchemy.org/en/latest/tutorial.html

---

**End of Plan**

