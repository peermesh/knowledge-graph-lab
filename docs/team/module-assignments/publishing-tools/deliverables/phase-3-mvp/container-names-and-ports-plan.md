# Set Container Names and Verify Port Configuration - Implementation Plan

**Date:** 2025-12-21  
**Developer:** bschreiber8  
**Task Reference:** `2025-11-17-tasks-bschreiber8-publishing.md` - Tasks #9 & #10

---

## Executive Summary

This plan combines two related Docker configuration tasks: setting container names for easier identification and verifying/optionally updating port configuration for consistency across modules.

---

## Current State Analysis

### Container Names

**File:** `modules/standalone/publishing/docker-compose.yml`

**Current State:**
- No `container_name` defined for any service
- Services: `postgres`, `redis`, `api`, `frontend`
- Docker Compose generates random container names

**Issue:**
- Hard to identify containers in `docker ps` output
- Difficult to reference containers in scripts
- No service discovery support

### Port Configuration

**Current Ports:**
- **API:** `8080:8080` (external:internal)
  - Status: ✅ Within range 8000-8999 (compliant)
  - Note: Could change to `8003:8080` for consistency with other modules
  
- **Frontend:** `3000:80` (external:internal)
  - Status: ✅ Within range 3000-3999 (compliant)
  
- **PostgreSQL:** `5432:5432`
  - Status: ✅ Standard PostgreSQL port
  
- **Redis:** `6379:6379`
  - Status: ✅ Standard Redis port

**Module Port Comparison:**
- Backend: 8000
- AI: 8001
- Publishing: 8080 (could be 8003 for consistency)

**Decision:** Keep 8080 (already compliant) or change to 8003 for consistency?

---

## Implementation Plan

### Phase 1: Set Container Names (5 minutes)

**File:** `modules/standalone/publishing/docker-compose.yml`

**Action:** Add `container_name` to each service

**Services to Update:**
1. `postgres` → `container_name: publishing-postgres`
2. `redis` → `container_name: publishing-redis`
3. `api` → `container_name: publishing-api`
4. `frontend` → `container_name: publishing-frontend`

**Implementation:**

```yaml
services:
  # PostgreSQL Database
  postgres:
    container_name: publishing-postgres
    image: postgres:15-alpine
    # ... rest of config ...

  # Redis Cache and Pub/Sub
  redis:
    container_name: publishing-redis
    image: redis:7-alpine
    # ... rest of config ...

  # Publishing Module API
  api:
    container_name: publishing-api
    build: .
    # ... rest of config ...

  # Simple Frontend (Nginx serving demo HTML)
  frontend:
    container_name: publishing-frontend
    image: nginx:alpine
    # ... rest of config ...
```

**Why:**
- Makes container identification easier
- Enables service discovery
- Consistent naming pattern across services
- Easier to reference in scripts and commands

### Phase 2: Verify and Optionally Update Port Configuration (5 minutes)

**File:** `modules/standalone/publishing/docker-compose.yml`

**Action:** 
1. Verify current port configuration (already compliant)
2. **Optional:** Change API port from 8080 to 8003 for consistency
3. Update documentation if port changes

**Decision Point:** Keep 8080 or change to 8003?

**Option 1: Keep 8080 (Recommended)**
- Already compliant with range requirements
- No breaking changes
- Port is already documented in QUICKSTART.md
- Less work required

**Option 2: Change to 8003**
- More consistent with other modules (8000, 8001, 8003)
- Requires updating:
  - docker-compose.yml
  - QUICKSTART.md (all curl examples)
  - Any documentation referencing port 8080
  - Health check URLs

**Recommendation:** Keep 8080 unless consistency is critical. The task says "VERIFY ONLY" and port is already compliant.

**If Changing to 8003:**

```yaml
services:
  api:
    container_name: publishing-api
    build: .
    ports:
      - "8003:8080"  # External:Internal - changed for consistency
    # ... rest of config ...
```

**Files to Update if Port Changes:**
- `docker-compose.yml` - Port mapping
- `QUICKSTART.md` - All curl examples (8080 → 8003)
- `README.md` or documentation - Port references

### Phase 3: Update Documentation (if port changes) (5 minutes)

**If port is changed to 8003:**

1. **Update QUICKSTART.md:**
   - Replace all `localhost:8080` with `localhost:8003`
   - Update health check examples
   - Update API endpoint examples

2. **Update README.md or create port documentation:**
   - Document the port configuration
   - Note consistency with other modules

**If port stays 8080:**
- Add note in documentation that port 8080 is used
- Document that it's compliant with range requirements
- Note that other modules use 8000, 8001 (for reference)

---

## Files to Modify

### Primary File

**File:** `modules/standalone/publishing/docker-compose.yml`

**Changes:**
1. Add `container_name: publishing-postgres` to postgres service
2. Add `container_name: publishing-redis` to redis service
3. Add `container_name: publishing-api` to api service
4. Add `container_name: publishing-frontend` to frontend service
5. **(Optional)** Change API port from `8080:8080` to `8003:8080`

### Documentation Files (if port changes)

**Files:**
- `modules/standalone/publishing/QUICKSTART.md` - Update port references
- `modules/standalone/publishing/README.md` - Document port configuration

---

## Detailed Code Changes

### Change 1: Add Container Names

**Current (postgres service):**
```yaml
  postgres:
    image: postgres:15-alpine
    environment:
```

**Updated:**
```yaml
  postgres:
    container_name: publishing-postgres
    image: postgres:15-alpine
    environment:
```

**Repeat for:** redis, api, frontend services

### Change 2: Port Configuration (Optional)

**Current:**
```yaml
  api:
    build: .
    ports:
      - "8080:8080"
```

**If changing to 8003:**
```yaml
  api:
    container_name: publishing-api
    build: .
    ports:
      - "8003:8080"  # External:Internal - changed for consistency
```

**Note:** Internal port (8080) stays the same, only external port changes.

---

## Verification Steps

### Step 1: Container Names
- [ ] All 4 services have `container_name` set
- [ ] Container names follow `publishing-{service}` pattern
- [ ] No conflicts with existing containers

### Step 2: Port Configuration
- [ ] Current ports verified (all compliant)
- [ ] Decision made: keep 8080 or change to 8003
- [ ] If changed, all references updated

### Step 3: Documentation
- [ ] QUICKSTART.md updated (if port changed)
- [ ] README.md or docs updated with port info
- [ ] All curl examples use correct port

### Step 4: Testing
- [ ] Containers start with correct names
- [ ] Ports are accessible on expected ports
- [ ] Health checks work
- [ ] API endpoints accessible

---

## Expected Outcome

### Container Names

**Before:**
```bash
$ docker ps
CONTAINER ID   IMAGE                    NAMES
abc123def456   publishing-api:latest   publishing_api_1
def456ghi789   nginx:alpine            publishing_frontend_1
```

**After:**
```bash
$ docker ps
CONTAINER ID   IMAGE                    NAMES
abc123def456   publishing-api:latest   publishing-api
def456ghi789   nginx:alpine            publishing-frontend
ghi789jkl012   postgres:15-alpine      publishing-postgres
jkl012mno345   redis:7-alpine          publishing-redis
```

### Port Configuration

**Current (Compliant):**
- API: `8080:8080` ✅
- Frontend: `3000:80` ✅
- PostgreSQL: `5432:5432` ✅
- Redis: `6379:6379` ✅

**If Changed to 8003:**
- API: `8003:8080` (external:internal)
- All other ports remain the same

---

## Benefits

### Container Names

1. **Easier Identification** ✅
   - Predictable container names
   - Easy to find in `docker ps`
   - Better for scripts and automation

2. **Service Discovery** ✅
   - Containers can be referenced by name
   - Works with Docker networking
   - Better for multi-container setups

3. **Consistency** ✅
   - Follows naming pattern
   - Matches service names
   - Professional configuration

### Port Configuration

1. **Compliance** ✅
   - All ports within required ranges
   - Meets standalone module requirements

2. **Consistency (if changed)** ✅
   - Matches other module patterns
   - Easier to remember (8000, 8001, 8003)

3. **Documentation** ✅
   - Ports clearly documented
   - Users know what to expect

---

## Decision: Port Configuration

### Recommendation: Keep 8080

**Reasons:**
1. Already compliant with range requirements
2. No breaking changes needed
3. Port is already documented in QUICKSTART.md
4. Task says "VERIFY ONLY" - suggests no change needed
5. Less work, lower risk

**If Consistency is Critical: Change to 8003**

**Reasons:**
1. Matches pattern: 8000 (Backend), 8001 (AI), 8003 (Publishing)
2. More predictable port allocation
3. Better for multi-module development

**Implementation Decision:** 
- **Default:** Keep 8080 (verify only)
- **Optional:** Change to 8003 if consistency is desired

---

## Testing Checklist

### Container Names
- [ ] All services have container_name set
- [ ] Containers start with correct names
- [ ] `docker ps` shows predictable names
- [ ] Containers can be referenced by name

### Port Configuration
- [ ] All ports verified as compliant
- [ ] API accessible on expected port
- [ ] Frontend accessible on port 3000
- [ ] Database accessible on port 5432
- [ ] Redis accessible on port 6379
- [ ] Health checks work
- [ ] Documentation updated (if port changed)

---

## Estimated Time

- Phase 1 (Set Container Names): 5 minutes
- Phase 2 (Verify/Update Ports): 5 minutes
- Phase 3 (Update Documentation): 5 minutes (if port changes)
- **Total: ~10-15 minutes**

---

## Special Considerations

### Container Name Conflicts

**Risk:** If containers with these names already exist, Docker Compose may fail

**Mitigation:**
- Check for existing containers: `docker ps -a | grep publishing-`
- Stop/remove old containers if needed
- Use `docker-compose down` before starting

### Port Conflicts

**Risk:** Port 8080 or 8003 may be in use

**Mitigation:**
- Check port usage: `lsof -i :8080` or `netstat -an | grep 8080`
- Change port if conflict exists
- Document the port choice

### Backward Compatibility

**If Port Changes:**
- Breaking change for existing users
- Need to update all documentation
- May break existing scripts/tests

**If Port Stays:**
- No breaking changes
- Existing documentation remains valid
- Lower risk

---

## References

- **Task File:** `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/2025-11-17-tasks-bschreiber8-publishing.md`
- **Docker Compose:** `modules/standalone/publishing/docker-compose.yml`
- **Standalone Module Requirements:** `docs/modules/shared/standalone-modules/README.md`

---

**End of Plan**

