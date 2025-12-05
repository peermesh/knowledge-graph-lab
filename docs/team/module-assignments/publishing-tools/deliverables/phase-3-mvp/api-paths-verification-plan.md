# API Paths Verification and Standardization Plan

**Date:** 2025-11-17  
**Developer:** bschreiber8  
**Task Reference:** `2025-11-17-tasks-bschreiber8-publishing.md` - Task #3: Verify and Standardize API Paths

---

## Executive Summary

This plan outlines the verification and standardization of API paths in the Publishing Module to ensure compliance with Standalone Module Requirements. All API endpoints must use the `/api/v1` prefix, while the health endpoint remains at `/health` (root level).

---

## Current State Analysis

### Current Implementation

**Main Router Configuration:**
- **File:** `src/publishing/main.py`
- **Line 149:** `app.include_router(api_router, prefix="/api/v1")` ✅ Already configured
- **Line 81-83:** OpenAPI docs configured at `/api/v1/docs`, `/api/v1/redoc`, `/api/v1/openapi.json` ✅ Correct
- **Line 156:** Health endpoint at `/health` ✅ Correct (should not be under `/api/v1`)

**API Router Structure:**
- **File:** `src/publishing/api/__init__.py`
- **Line 48:** Main router created: `router = APIRouter()`
- **Line 54:** Root endpoint: `@router.get("/")` → Will be `/api/v1/` ✅
- **Lines 74-123:** All sub-routers included with relative prefixes:
  - `/publications` → `/api/v1/publications` ✅
  - `/channels` → `/api/v1/channels` ✅
  - `/subscribers` → `/api/v1/subscribers` ✅
  - `/analytics` → `/api/v1/analytics` ✅
  - `/alerts` → `/api/v1/alerts` ✅
  - `/dashboard` → `/api/v1/dashboard` ✅
  - `/email` (from email_test) → `/api/v1/email` ✅
  - `/ws` (from ws) → `/api/v1/ws` ✅

**Individual Router Files:**
- All routers use `APIRouter()` without prefix (prefixes added in main router)
- `email_test.py` has `prefix="/email"` which is correct (relative to `/api/v1`)

**Test Files:**
- Tests already use `/api/v1` prefix ✅
- Found in: `test_multichannel_publishing.py`, `test_publications.py`, `test_subscribers.py`, etc.

### Requirements from Standalone Module Spec

**File:** `docs/modules/shared/standalone-modules/README.md`

**API Standards (Lines 193-198):**
- **Base Path:** `/api/v1` for all endpoints ✅
- **Response Format:** `{"data": {}, "meta": {}, "errors": []}` (separate verification)
- **Error Handling:** RFC7807 Problem Details format (separate verification)
- **Documentation:** OpenAPI/Swagger at `/api/v1/openapi.json` ✅
- **Health Endpoint:** `/health` (not under `/api/v1`) ✅

---

## Implementation Plan

### Phase 1: Verify Current Routes (30 minutes)

#### Step 1.1: Start Application and Check OpenAPI Spec

**Action:** Start the application and retrieve the OpenAPI specification to see all actual routes.

**Commands:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab/modules/standalone/publishing
docker compose up -d

# Wait for application to start
sleep 5

# Get OpenAPI spec
curl http://localhost:8080/api/v1/openapi.json | python3 -m json.tool > /tmp/openapi-spec.json

# Extract all paths
cat /tmp/openapi-spec.json | python3 -c "import json, sys; data=json.load(sys.stdin); [print(path) for path in data['paths'].keys()]"
```

**Expected Output:**
All paths should start with `/api/v1/` except:
- `/health` (should be at root)
- `/api/v1/docs` (documentation)
- `/api/v1/redoc` (documentation)
- `/api/v1/openapi.json` (spec)

**Files to Check:**
- OpenAPI spec JSON
- Application logs

**Why:** The OpenAPI spec is the source of truth for what routes are actually registered.

#### Step 1.2: Verify Health Endpoint Location

**Action:** Confirm health endpoint is at root level, not under `/api/v1`.

**Command:**
```bash
curl http://localhost:8080/health
curl http://localhost:8080/api/v1/health  # Should return 404
```

**Expected Result:**
- `/health` returns 200 OK with health status
- `/api/v1/health` returns 404 Not Found

**Why:** Health endpoint must be at root for container orchestration tools (Kubernetes, Docker Swarm).

#### Step 1.3: List All Registered Routes Programmatically

**Action:** Use FastAPI's route inspection to list all routes.

**Create Test Script:** `scripts/verify_routes.py`
```python
#!/usr/bin/env python3
"""Verify all API routes have correct prefixes."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.publishing.main import app

# Get all routes
routes = []
for route in app.routes:
    if hasattr(route, 'path'):
        routes.append({
            'path': route.path,
            'methods': list(route.methods) if hasattr(route, 'methods') else []
        })

# Sort by path
routes.sort(key=lambda x: x['path'])

# Print all routes
print("Registered Routes:")
print("=" * 60)
for route in routes:
    methods = ', '.join(route['methods']) if route['methods'] else 'N/A'
    print(f"{route['path']:40} {methods}")

# Verify compliance
print("\n" + "=" * 60)
print("Compliance Check:")
print("=" * 60)

issues = []
for route in routes:
    path = route['path']
    # Health endpoint should be at root
    if path == '/health':
        continue
    # Documentation endpoints are OK
    if path in ['/api/v1/docs', '/api/v1/redoc', '/api/v1/openapi.json']:
        continue
    # All other paths should start with /api/v1
    if not path.startswith('/api/v1/'):
        issues.append(f"❌ {path} - Missing /api/v1 prefix")
    else:
        print(f"✅ {path}")

if issues:
    print("\nIssues Found:")
    for issue in issues:
        print(issue)
    sys.exit(1)
else:
    print("\n✅ All routes comply with /api/v1 prefix requirement!")
```

**Why:** Programmatic verification ensures we catch all routes, including dynamically registered ones.

---

### Phase 2: Update Routes if Needed (1 hour)

#### Step 2.1: Review Router Prefixes

**Action:** Check each router file to ensure no hardcoded prefixes conflict with `/api/v1`.

**Files to Review:**
1. `src/publishing/api/__init__.py` - Main router
2. `src/publishing/api/publications.py` - Publications router
3. `src/publishing/api/channels.py` - Channels router
4. `src/publishing/api/subscribers.py` - Subscribers router
5. `src/publishing/api/analytics.py` - Analytics router
6. `src/publishing/api/alerts.py` - Alerts router
7. `src/publishing/api/dashboard.py` - Dashboard router
8. `src/publishing/api/email_test.py` - Email test router (has `/email` prefix)
9. `src/publishing/api/ws.py` - WebSocket router

**What to Check:**
- No router should have `prefix="/api/v1"` (already added in main.py)
- Sub-routers should use relative prefixes (e.g., `/publications`, `/channels`)
- `email_test.py` has `prefix="/email"` which is correct (relative)

**Expected State:**
```python
# In individual router files (e.g., publications.py)
router = APIRouter()  # No prefix here

# In main.py
app.include_router(api_router, prefix="/api/v1")  # Prefix added here

# In api/__init__.py
router.include_router(
    publications.router,
    prefix="/publications",  # Relative prefix
    tags=["publications"]
)
```

**Why:** Prefixes should be added at the top level (main.py) to ensure consistency.

#### Step 2.2: Fix Any Incorrect Prefixes

**If Issues Found:**

**Scenario A: Router has hardcoded `/api/v1` prefix**
```python
# WRONG:
router = APIRouter(prefix="/api/v1/publications")

# CORRECT:
router = APIRouter()  # No prefix, added in main.py
```

**Scenario B: Router missing from main router**
```python
# In api/__init__.py, ensure all routers are included:
router.include_router(
    new_router.router,
    prefix="/new-endpoint",
    tags=["new"]
)
```

**Scenario C: Health endpoint under `/api/v1`**
```python
# WRONG:
app.include_router(health_router, prefix="/api/v1")

# CORRECT:
@app.get("/health")  # Direct on app, no router
async def health_check(request: Request):
    ...
```

**Files to Modify (if needed):**
- Individual router files if they have incorrect prefixes
- `src/publishing/api/__init__.py` if routers are missing
- `src/publishing/main.py` if health endpoint is incorrectly placed

**Why:** Ensures all routes follow the standard pattern.

---

### Phase 3: Update Tests (30 minutes)

#### Step 3.1: Find All Test Files with API Calls

**Action:** Search for all test files that make API calls.

**Command:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab
grep -r "client\.\(get\|post\|put\|delete\|patch\)" tests/publishing/ --include="*.py"
```

**Expected Files:**
- `tests/publishing/contract/test_publications.py`
- `tests/publishing/contract/test_subscribers.py`
- `tests/publishing/contract/test_analytics.py`
- `tests/publishing/integration/test_multichannel_publishing.py`
- `tests/publishing/integration/test_personalized_newsletters.py`
- `tests/publishing/contract/test_newsletter_scheduling.py`
- `tests/publishing/contract/test_publication_status.py`

**Why:** Need to verify all tests use correct paths.

#### Step 3.2: Verify Test Paths

**Action:** Check each test file to ensure all API calls use `/api/v1` prefix.

**Pattern to Look For:**
```python
# CORRECT:
client.get("/api/v1/publications")
client.post("/api/v1/subscribers", json={...})

# WRONG:
client.get("/publications")  # Missing /api/v1
client.post("/api/subscribers", json={...})  # Wrong version
```

**Files Already Verified (from grep):**
- ✅ `test_multichannel_publishing.py` - Uses `/api/v1/channels`, `/api/v1/publications`
- ✅ `test_publications.py` - Uses `/api/v1/channels`, `/api/v1/publications`
- ✅ `test_subscribers.py` - Uses `/api/v1/subscribers`
- ✅ `test_newsletter_scheduling.py` - Uses `/api/v1/publications`
- ✅ `test_publication_status.py` - Uses `/api/v1/publications`

**Why:** Tests should match actual API paths.

#### Step 3.3: Update Tests if Needed

**If Issues Found:**

**Pattern:**
```python
# BEFORE:
response = client.get("/publications")

# AFTER:
response = client.get("/api/v1/publications")
```

**Files to Modify (if needed):**
- Any test file with incorrect paths
- Update all HTTP method calls (get, post, put, delete, patch)

**Why:** Tests must match the actual API structure.

---

### Phase 4: Verify OpenAPI Documentation (15 minutes)

#### Step 4.1: Check OpenAPI Spec Endpoints

**Action:** Verify OpenAPI documentation is accessible at correct paths.

**Commands:**
```bash
# Check OpenAPI JSON
curl http://localhost:8080/api/v1/openapi.json | python3 -m json.tool | head -50

# Check Swagger UI
curl http://localhost:8080/api/v1/docs | head -20

# Check ReDoc
curl http://localhost:8080/api/v1/redoc | head -20
```

**Expected Results:**
- `/api/v1/openapi.json` - Returns OpenAPI 3.0 spec
- `/api/v1/docs` - Returns Swagger UI HTML
- `/api/v1/redoc` - Returns ReDoc HTML

**Why:** Documentation must be accessible for API consumers.

#### Step 4.2: Verify All Paths in OpenAPI Spec

**Action:** Extract and verify all paths in the OpenAPI spec start with `/api/v1`.

**Command:**
```bash
curl -s http://localhost:8080/api/v1/openapi.json | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
paths = list(data['paths'].keys())
print('Paths in OpenAPI spec:')
for path in sorted(paths):
    if path.startswith('/api/v1/') or path in ['/health', '/api/v1/docs', '/api/v1/redoc', '/api/v1/openapi.json']:
        print(f'✅ {path}')
    else:
        print(f'❌ {path} - Does not comply')
"
```

**Expected Output:**
All paths should show ✅ except documentation endpoints.

**Why:** OpenAPI spec is the contract - it must be accurate.

---

### Phase 5: Integration Testing (15 minutes)

#### Step 5.1: Test All Major Endpoints

**Action:** Make actual HTTP requests to verify endpoints work.

**Test Script:**
```bash
#!/bin/bash
BASE_URL="http://localhost:8080"

echo "Testing API Endpoints..."
echo "========================="

# Health endpoint (should be at root)
echo -n "Health endpoint: "
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health"
echo ""

# API root
echo -n "API root: "
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/"
echo ""

# Publications
echo -n "Publications list: "
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/publications"
echo ""

# Subscribers
echo -n "Subscribers list: "
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/subscribers"
echo ""

# Channels
echo -n "Channels list: "
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/channels"
echo ""

# Analytics
echo -n "Analytics: "
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/analytics/engagement"
echo ""

# Dashboard
echo -n "Dashboard: "
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/dashboard/overview"
echo ""

# Email test
echo -n "Email test status: "
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/email/status"
echo ""

# Verify non-prefixed paths return 404
echo ""
echo "Verifying non-prefixed paths return 404:"
echo -n "/publications (should be 404): "
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/publications"
echo ""

echo -n "/api/publications (should be 404): "
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/publications"
echo ""

echo "========================="
echo "Testing complete!"
```

**Expected Results:**
- All `/api/v1/*` endpoints return 200 or appropriate status codes
- `/health` returns 200
- Non-prefixed paths return 404

**Why:** End-to-end verification ensures everything works correctly.

---

## Files to Review/Modify

### Files to Review (No Changes Expected)

1. **`src/publishing/main.py`**
   - Line 149: `app.include_router(api_router, prefix="/api/v1")` ✅
   - Line 156: `@app.get("/health")` ✅
   - Lines 81-83: OpenAPI docs configuration ✅

2. **`src/publishing/api/__init__.py`**
   - All router includes with relative prefixes ✅

3. **Individual Router Files:**
   - All use `APIRouter()` without hardcoded `/api/v1` ✅

### Files to Verify (May Need Updates)

1. **Test Files:**
   - `tests/publishing/contract/test_publications.py`
   - `tests/publishing/contract/test_subscribers.py`
   - `tests/publishing/contract/test_analytics.py`
   - `tests/publishing/integration/test_multichannel_publishing.py`
   - `tests/publishing/integration/test_personalized_newsletters.py`
   - `tests/publishing/contract/test_newsletter_scheduling.py`
   - `tests/publishing/contract/test_publication_status.py`

### Files to Create

1. **`scripts/verify_routes.py`** - Route verification script
2. **`scripts/test_api_paths.sh`** - Integration test script

---

## Expected Route Structure

### Correct Route Patterns

```
✅ /health                          (Health check - root level)
✅ /api/v1/                         (API root)
✅ /api/v1/publications             (Publications list)
✅ /api/v1/publications/{id}       (Publication detail)
✅ /api/v1/subscribers              (Subscribers list)
✅ /api/v1/channels                 (Channels list)
✅ /api/v1/analytics/engagement     (Analytics endpoints)
✅ /api/v1/alerts                   (Alerts endpoints)
✅ /api/v1/dashboard/overview       (Dashboard endpoints)
✅ /api/v1/email/test               (Email test endpoints)
✅ /api/v1/ws                       (WebSocket stub)
✅ /api/v1/docs                     (Swagger UI)
✅ /api/v1/redoc                    (ReDoc)
✅ /api/v1/openapi.json             (OpenAPI spec)
```

### Incorrect Patterns (Should Not Exist)

```
❌ /publications                    (Missing /api/v1)
❌ /api/publications                (Missing /v1)
❌ /api/v1/health                   (Health should be at root)
❌ /v1/publications                 (Missing /api)
```

---

## Validation Checklist

- [ ] All routes in OpenAPI spec start with `/api/v1/`
- [ ] Health endpoint is at `/health` (not `/api/v1/health`)
- [ ] All test files use `/api/v1` prefix
- [ ] No router has hardcoded `/api/v1` prefix (added in main.py)
- [ ] OpenAPI documentation accessible at `/api/v1/docs`
- [ ] All endpoints return correct status codes
- [ ] Non-prefixed paths return 404
- [ ] Route verification script passes

---

## Success Criteria

1. ✅ All API endpoints use `/api/v1` prefix
2. ✅ Health endpoint at `/health` (root level)
3. ✅ OpenAPI spec shows all paths correctly
4. ✅ All tests use correct paths
5. ✅ Integration tests pass
6. ✅ Documentation accessible

---

## Estimated Time

**Total: ~2 hours**

- Phase 1 (Verify Current Routes): 30 minutes
- Phase 2 (Update Routes if Needed): 1 hour
- Phase 3 (Update Tests): 30 minutes
- Phase 4 (Verify OpenAPI): 15 minutes
- Phase 5 (Integration Testing): 15 minutes

---

## Risks and Mitigations

### Risk 1: Routes Already Correct
**Risk:** All routes may already be correct, making this a verification-only task  
**Mitigation:** This is actually good - verification confirms compliance without changes needed.

### Risk 2: Hidden Routes
**Risk:** Some routes might be registered dynamically or conditionally  
**Mitigation:** Use OpenAPI spec and route inspection to find all routes.

### Risk 3: Test Failures
**Risk:** Updating test paths might reveal existing test issues  
**Mitigation:** Run tests before and after changes to identify issues.

### Risk 4: Breaking Changes
**Risk:** Changing routes could break external integrations  
**Mitigation:** This is a standardization task - routes should already be correct. If changes are needed, document them clearly.

---

## References

- **Task File:** `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/2025-11-17-tasks-bschreiber8-publishing.md`
- **Standalone Module Requirements:** `docs/modules/shared/standalone-modules/README.md`
- **Current Implementation:** `src/publishing/main.py`, `src/publishing/api/__init__.py`

---

## Next Steps After Implementation

1. Document any route changes in CHANGELOG
2. Update API documentation if routes changed
3. Notify team if breaking changes were made
4. Add route verification to CI/CD pipeline (future enhancement)

---

**End of Plan**

