# SQLAlchemy Deprecation Warning Fix Plan

**Date:** 2025-11-17  
**Developer:** bschreiber8  
**Task Reference:** `2025-11-17-tasks-bschreiber8-publishing.md` - Task #4: Fix SQLAlchemy Deprecation Warning

---

## Executive Summary

This plan outlines the fix for the SQLAlchemy deprecation warning: "SAWarning: Textual SQL expression should be explicitly declared as text()". The warning occurs when raw SQL strings are passed directly to `session.execute()` without wrapping them in SQLAlchemy's `text()` function. This fix ensures compatibility with current and future SQLAlchemy versions.

---

## Current State Analysis

### Warning Details

**Warning Message:**
```
SAWarning: Textual SQL expression should be explicitly declared as text()
```

**SQLAlchemy Version:** 2.0+  
**Issue:** SQLAlchemy 2.0+ requires explicit declaration of textual SQL using `text()` function  
**Impact:** Deprecation warnings in logs, potential breaking changes in future versions

### Problem Location

**File:** `src/publishing/core/database.py`  
**Function:** `get_table_status()`  
**Line:** 144  
**Issue:** Raw SQL string passed directly to `session.execute()`

**Current Code:**
```python
async def get_table_status() -> dict:
    """Get status of all publishing module tables."""
    try:
        async with async_session_factory() as session:
            # Check which tables exist
            result = await session.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name LIKE 'publishing_%'
                ORDER BY table_name
            """)
```

**Problem:** The SQL string is passed directly without `text()` wrapper.

### Already Fixed

**File:** `src/publishing/core/database.py`  
**Function:** `get_db_health()`  
**Line:** 112  
**Status:** ✅ Already uses `text()`

**Correct Implementation:**
```python
from sqlalchemy import text
result = await session.execute(text("SELECT 1 as health_check"))
```

---

## Implementation Plan

### Phase 1: Identify All Raw SQL Strings (10 minutes)

#### Step 1.1: Search for Raw SQL Executions

**Action:** Find all instances where raw SQL strings are executed.

**Command:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab
grep -rn "session\.execute\([\"']" src/publishing/ --include="*.py"
grep -rn "db\.execute\([\"']" src/publishing/ --include="*.py"
```

**Expected Results:**
- Should find the issue in `database.py` line 144
- May find other instances that need fixing

**Why:** Need to identify all places where raw SQL is used.

#### Step 1.2: Verify Current Implementation

**Action:** Check the exact code that needs fixing.

**File to Review:**
- `src/publishing/core/database.py` lines 139-168

**Current Code:**
```python
async def get_table_status() -> dict:
    """Get status of all publishing module tables."""
    try:
        async with async_session_factory() as session:
            # Check which tables exist
            result = await session.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name LIKE 'publishing_%'
                ORDER BY table_name
            """)
```

**Why:** Need to see the exact context to apply the fix correctly.

---

### Phase 2: Apply the Fix (15 minutes)

#### Step 2.1: Import text() Function

**File:** `src/publishing/core/database.py`

**Action:** Ensure `text` is imported from SQLAlchemy.

**Current State:** Check if `text` is already imported.

**Location:** Top of file, with other SQLAlchemy imports

**Expected Import:**
```python
from sqlalchemy import text
```

**Check:** Line 111 already imports `text` for `get_db_health()`, so it should be available.

**Why:** Need `text()` function to wrap raw SQL strings.

#### Step 2.2: Wrap SQL String with text()

**File:** `src/publishing/core/database.py`  
**Function:** `get_table_status()`  
**Line:** 144

**Current Code:**
```python
result = await session.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name LIKE 'publishing_%'
    ORDER BY table_name
""")
```

**Fixed Code:**
```python
from sqlalchemy import text

# ... later in function ...

result = await session.execute(text("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name LIKE 'publishing_%'
    ORDER BY table_name
"""))
```

**Why:** SQLAlchemy 2.0+ requires explicit `text()` wrapper for raw SQL strings.

#### Step 2.3: Verify Import Location

**Action:** Check if `text` import needs to be moved or if it's already in the right place.

**Current Import Location:** Line 111 (inside `get_db_health()` function)

**Decision:** Move import to top of file for better code organization.

**Why:** Imports should be at module level, not inside functions.

---

### Phase 3: Test the Fix (5 minutes)

#### Step 3.1: Verify No Syntax Errors

**Action:** Check Python syntax is correct.

**Command:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab
python3 -m py_compile src/publishing/core/database.py
```

**Expected Result:** No syntax errors

**Why:** Ensure the fix doesn't introduce syntax errors.

#### Step 3.2: Test Function Execution (if possible)

**Action:** Verify the function works correctly with the fix.

**Test Script:**
```python
# Quick test to verify function works
import asyncio
from src.publishing.core.database import get_table_status

async def test():
    result = await get_table_status()
    print(result)

# Run if database is available
# asyncio.run(test())
```

**Why:** Ensure the fix doesn't break functionality.

#### Step 3.3: Check for Warnings

**Action:** Run application and check logs for deprecation warnings.

**Command:**
```bash
# When application is running
docker compose logs api | grep -i "sawarning\|textual sql"
```

**Expected Result:** No warnings about textual SQL expressions

**Why:** Verify the warning is eliminated.

---

## Files to Modify

### Primary File

**File:** `src/publishing/core/database.py`

**Changes:**
1. **Line 111:** Move `text` import to top of file (if not already there)
2. **Line 144:** Wrap SQL string with `text()`

**Before:**
```python
result = await session.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name LIKE 'publishing_%'
    ORDER BY table_name
""")
```

**After:**
```python
result = await session.execute(text("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_name LIKE 'publishing_%'
    ORDER BY table_name
"""))
```

---

## Code Changes Details

### Import Statement

**Location:** Top of `src/publishing/core/database.py`

**Current (if text is imported inside function):**
```python
# Inside get_db_health() function
from sqlalchemy import text
```

**Should Be:**
```python
# At top of file with other imports
from sqlalchemy import text
```

**Check Current Imports:**
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
import structlog
from typing import AsyncGenerator

from .config import settings
```

**Add:**
```python
from sqlalchemy import text
```

### Function Fix

**Function:** `get_table_status()`

**Location:** Lines 139-168

**Change:**
- Wrap the SQL string in `text()` function
- Ensure `text` is imported at module level

---

## Verification Steps

### Step 1: Code Review
- [ ] `text` is imported at module level
- [ ] SQL string in `get_table_status()` is wrapped with `text()`
- [ ] No other raw SQL strings found in codebase
- [ ] Code follows same pattern as `get_db_health()`

### Step 2: Syntax Check
- [ ] Python syntax is valid
- [ ] No import errors
- [ ] File compiles without errors

### Step 3: Runtime Verification
- [ ] Application starts without errors
- [ ] Health check works correctly
- [ ] `get_table_status()` function works (if called)
- [ ] No deprecation warnings in logs

### Step 4: Log Verification
- [ ] Check application logs for warnings
- [ ] Verify no "SAWarning: Textual SQL" messages
- [ ] Confirm function executes successfully

---

## Expected Outcome

### Before Fix
```
SAWarning: Textual SQL expression should be explicitly declared as text()
```

### After Fix
- ✅ No deprecation warnings
- ✅ Function works correctly
- ✅ Code follows SQLAlchemy 2.0+ best practices
- ✅ Future-proof for SQLAlchemy updates

---

## Testing Checklist

- [ ] Code compiles without syntax errors
- [ ] `text` import is at module level
- [ ] SQL string wrapped with `text()`
- [ ] Function executes without errors
- [ ] No deprecation warnings in logs
- [ ] Health check still works
- [ ] No other raw SQL strings found

---

## Success Criteria

1. ✅ No SQLAlchemy deprecation warnings in logs
2. ✅ `get_table_status()` function works correctly
3. ✅ Code follows SQLAlchemy 2.0+ standards
4. ✅ Import statements properly organized
5. ✅ No breaking changes to functionality

---

## Estimated Time

**Total: ~30 minutes**

- Phase 1 (Identify Issues): 10 minutes
- Phase 2 (Apply Fix): 15 minutes
- Phase 3 (Test): 5 minutes

---

## Risks and Mitigations

### Risk 1: Breaking Existing Functionality
**Risk:** Wrapping SQL in `text()` might change behavior  
**Mitigation:** `text()` is a wrapper that doesn't change SQL execution, only makes it explicit. This is a safe change.

### Risk 2: Other Raw SQL Strings
**Risk:** There might be other places with raw SQL  
**Mitigation:** Comprehensive grep search will find all instances.

### Risk 3: Import Conflicts
**Risk:** Moving import might cause issues  
**Mitigation:** `text` is a standard SQLAlchemy function, no conflicts expected.

---

## SQLAlchemy 2.0+ Best Practices

### Correct Pattern
```python
from sqlalchemy import text

# For raw SQL strings
result = await session.execute(text("SELECT 1"))

# For ORM queries (preferred)
result = await session.execute(select(Model).where(Model.id == 1))
```

### Incorrect Pattern (Deprecated)
```python
# Raw SQL without text() - generates warning
result = await session.execute("SELECT 1")
```

### Why This Matters

1. **Explicit Intent:** `text()` makes it clear the string is raw SQL
2. **Security:** Helps prevent SQL injection by making raw SQL explicit
3. **Future Compatibility:** Required for SQLAlchemy 2.0+
4. **Type Safety:** Better type checking and IDE support

---

## References

- **Task File:** `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/2025-11-17-tasks-bschreiber8-publishing.md`
- **SQLAlchemy Documentation:** https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Connection.execute
- **SQLAlchemy 2.0 Migration Guide:** https://docs.sqlalchemy.org/en/20/changelog/migration_20.html

---

## Additional Notes

### Why This Warning Exists

SQLAlchemy 2.0 introduced stricter typing and explicit SQL declaration to:
- Prevent accidental SQL injection vulnerabilities
- Improve type checking
- Make code intent clearer
- Support better IDE autocomplete

### Migration Path

The fix is straightforward:
1. Import `text` from `sqlalchemy`
2. Wrap raw SQL strings with `text()`
3. No other changes needed

### Performance Impact

**None.** `text()` is a lightweight wrapper that doesn't affect query performance.

---

**End of Plan**

