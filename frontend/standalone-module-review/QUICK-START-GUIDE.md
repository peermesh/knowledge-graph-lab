# Quick Start Guide
## Get Started with Production Readiness Implementation

**Date:** October 28, 2025  
**For:** Development Team  
**Purpose:** Fast-track guide to begin implementation

---

## 📚 Document Overview

This proposal consists of 4 key documents:

1. **PRODUCTION-READINESS-PROPOSAL.md** ← START HERE
   - Executive summary and phase breakdown
   - What needs to change and why
   - Acceptance criteria and success metrics

2. **TECHNICAL-IMPLEMENTATION-SPEC.md**
   - Detailed file-by-file implementation
   - Complete code examples
   - Integration points

3. **DEPENDENCIES-AND-CONFIG.md** (this file)
   - All dependencies to install
   - Environment variables
   - Docker configurations
   - Installation commands

4. **QUICK-START-GUIDE.md** (this document)
   - Fast implementation path
   - Common pitfalls
   - Troubleshooting

---

## 🚀 30-Minute Setup (Development Environment)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL client tools
- Git

### Step 1: Clone and Setup (5 min)

```bash
# Already in project directory
cd knowledge-graph-lab-new

# Backend setup
cd src/backend-architecture
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Frontend setup (new terminal)
cd frontend
npm install
```

### Step 2: Start Infrastructure (10 min)

```bash
# In src/backend-architecture/
docker-compose up -d postgres redis rabbitmq qdrant

# Wait for health checks (check with):
docker-compose ps

# Should see all services "healthy"
```

### Step 3: Configure Environment (5 min)

```bash
# Backend .env
cd src/backend-architecture
cp .env.example .env  # Or create from template in DEPENDENCIES-AND-CONFIG.md

# Frontend .env
cd frontend
cp .env.example .env  # Or create from template
```

### Step 4: Database Setup (5 min)

```bash
# In src/backend-architecture/ with venv activated
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Verify
psql -h localhost -U kglab -d knowledge_graph_lab -c "\dt"
```

### Step 5: Start Development Servers (5 min)

```bash
# Terminal 1: Backend
cd src/backend-architecture
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Verify:
# Backend: http://localhost:8000/docs
# Frontend: http://localhost:5173
```

✅ **You now have a running development environment!**

---

## 📋 Implementation Checklist by Phase

### PHASE 1: Authentication (Weeks 1-3)

#### Week 1: Backend Auth Foundation

**Day 1-2: Install Dependencies**
```bash
cd src/backend-architecture
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 bcrypt==4.1.1
pip freeze > requirements.txt
```

**Day 3-4: Create Files**
- [ ] Create `app/core/security.py`
- [ ] Create `app/core/auth_middleware.py`
- [ ] Create `app/models/user_auth.py`
- [ ] Create `app/schemas/auth.py`

**Day 5: Database Migration**
```bash
# Create migration
alembic revision -m "add_authentication_tables"

# Edit the generated file in alembic/versions/
# Copy migration code from TECHNICAL-IMPLEMENTATION-SPEC.md

# Run migration
alembic upgrade head
```

#### Week 2: Auth Endpoints

**Day 1-3: Implement Endpoints**
- [ ] Create `app/api/api_v1/endpoints/auth.py`
- [ ] Add router to `app/api/api_v1/api.py`
- [ ] Test with Swagger UI at http://localhost:8000/docs

**Day 4-5: Protect Existing Endpoints**
```python
# Add to existing endpoints:
from ....core.auth_middleware import get_current_user

@router.get("/entities")
async def get_entities(
    current_user: User = Depends(get_current_user),  # ADD THIS
    db: AsyncSession = Depends(get_db)
):
    # existing code...
```

#### Week 3: Frontend Auth

**Day 1-2: Create Auth Pages**
- [ ] Create `frontend/src/pages/Login/LoginPage.tsx`
- [ ] Create `frontend/src/pages/Register/RegisterPage.tsx`
- [ ] Add routes in `frontend/src/App.tsx`

**Day 3: Implement Protected Routes**
- [ ] Create `frontend/src/components/Auth/ProtectedRoute.tsx`
- [ ] Wrap protected pages

**Day 4-5: Testing**
- [ ] Write unit tests for auth utilities
- [ ] Write integration tests for login flow
- [ ] Manual testing

**✅ Phase 1 Complete When:**
- You can register a new user
- You can login and receive JWT token
- Token is automatically added to API requests
- Protected endpoints return 401 without token

---

### PHASE 2: WebSocket & Data (Weeks 4-6)

#### Week 4: WebSocket Implementation

**Day 1: Install Dependencies**
```bash
# Already have redis and aioredis
# Verify in docker-compose.yml
docker-compose ps redis
```

**Day 2-3: Create WebSocket Files**
- [ ] Create `app/api/websocket/__init__.py`
- [ ] Create `app/api/websocket/manager.py`
- [ ] Create `app/api/websocket/handlers.py`

**Day 4: Integrate with Main App**
- [ ] Modify `app/main.py` to include WebSocket router
- [ ] Add Redis pub/sub setup in lifespan

**Day 5: Test WebSocket**
```bash
# Install wscat for testing
npm install -g wscat

# Test connection
wscat -c "ws://localhost:8000/ws?token=YOUR_JWT_TOKEN"
```

#### Week 5: Database Seeding

**Day 1: Create Migration**
```bash
alembic revision -m "add_research_items_and_engagement_tables"
# Add SQL from PRODUCTION-READINESS-PROPOSAL.md
alembic upgrade head
```

**Day 2-4: Create Seed Scripts**
- [ ] Create `app/db/seeds/seed_users.py`
- [ ] Create `app/db/seeds/seed_entities.py`
- [ ] Create `app/db/seeds/seed_relationships.py`
- [ ] Create `app/db/seeds/seed_research_items.py`
- [ ] Create `app/db/seeds/run_seeds.py`

**Day 5: Run Seeds**
```bash
python -m app.db.seeds.run_seeds --all
# This will take 5-10 minutes for 10,000 entities

# Verify
psql -h localhost -U kglab -d knowledge_graph_lab
SELECT COUNT(*) FROM entities;
SELECT COUNT(*) FROM research_items;
```

#### Week 6: Feed API & Integration

**Day 1-2: Create Feed Endpoints**
- [ ] Create `app/api/api_v1/endpoints/feed.py`
- [ ] Create `app/api/api_v1/endpoints/engagement.py`

**Day 3-4: Frontend Integration**
- [ ] Update `FeedPage.tsx` to use real API
- [ ] Test WebSocket real-time updates

**Day 5: Testing**
- [ ] Test feed pagination
- [ ] Test real-time updates when entity changes

**✅ Phase 2 Complete When:**
- WebSocket connects successfully
- Feed shows 1000+ research items
- Database has 10,000+ entities
- Real-time updates appear in UI

---

### PHASE 3: GraphQL (Weeks 7-9)

#### Week 7: GraphQL Setup

**Day 1: Install Dependencies**
```bash
pip install strawberry-graphql[fastapi]==0.235.0
npm install graphql graphql-request @urql/core urql
```

**Day 2-3: Create GraphQL Schema**
- [ ] Create `app/api/graphql/__init__.py`
- [ ] Create `app/api/graphql/schema.py`
- [ ] Create `app/api/graphql/resolvers.py`

**Day 4: Mount GraphQL**
```python
# In app/main.py
from strawberry.fastapi import GraphQLRouter
from .api.graphql.schema import schema

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
```

**Day 5: Test GraphQL Playground**
Visit: http://localhost:8000/graphql

#### Week 8-9: Frontend Integration & Testing
- [ ] Create `frontend/src/services/graphql.ts`
- [ ] Create GraphQL queries
- [ ] Migrate graph page to GraphQL
- [ ] Performance testing

**✅ Phase 3 Complete When:**
- GraphQL playground works
- Complex queries return data
- Frontend uses GraphQL for graph view
- Performance improved over REST

---

### PHASE 4: Monitoring & Testing (Weeks 10-12)

#### Week 10: Monitoring Setup

**Day 1-2: Create Monitoring Configs**
- [ ] Create `prometheus/prometheus.yml`
- [ ] Create `grafana/dashboards/` with JSON files
- [ ] Create `loki/loki-config.yml`
- [ ] Create `promtail/promtail-config.yml`

**Day 3: Start Monitoring Stack**
```bash
docker-compose -f docker-compose.monitoring.yml up -d

# Access Grafana
open http://localhost:3001
# Login: admin/admin
```

**Day 4-5: Add Metrics to Backend**
```python
# In app/main.py
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(...)
Instrumentator().instrument(app).expose(app)
```

#### Week 11: Testing

**Day 1-2: Unit Tests**
```bash
# Create tests/unit/ structure
pytest tests/unit/ --cov=app --cov-report=html
```

**Day 3-4: Integration Tests**
```bash
pytest tests/integration/
```

**Day 5: Load Testing**
```bash
locust -f tests/load/locustfile.py --host=http://localhost:8000
# Open http://localhost:8089
```

#### Week 12: Documentation & Polish
- [ ] Complete API documentation
- [ ] Write deployment guide
- [ ] Final integration testing
- [ ] Security audit

**✅ Phase 4 Complete When:**
- Grafana shows live metrics
- Logs searchable in Loki
- Test coverage > 80%
- Load test handles 1000 users

---

## 🔥 Common Pitfalls & Solutions

### Issue: "Connection refused" to PostgreSQL

**Solution:**
```bash
# Check Docker status
docker-compose ps

# Restart PostgreSQL
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

### Issue: JWT token errors

**Solution:**
```bash
# Verify JWT_SECRET_KEY is set
echo $JWT_SECRET_KEY

# Generate new secret if needed
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Issue: WebSocket won't connect

**Solution:**
```bash
# Check if Redis is running
docker-compose ps redis

# Test WebSocket endpoint exists
curl http://localhost:8000/docs
# Look for /ws endpoint

# Check CORS settings
# Ensure WS_URL in frontend .env matches backend URL
```

### Issue: Database migrations fail

**Solution:**
```bash
# Check current version
alembic current

# See migration history
alembic history

# Rollback one version
alembic downgrade -1

# Try upgrade again
alembic upgrade head
```

### Issue: Seed script is slow

**Solution:**
```python
# Use bulk inserts instead of individual inserts
# In seed scripts:
entities = [Entity(...) for i in range(1000)]
db.add_all(entities)  # Bulk insert
await db.commit()
```

---

## 🧪 Testing Your Implementation

### Quick Smoke Tests

#### 1. Authentication Flow
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Save the access_token from response
export TOKEN="your_access_token_here"

# Test protected endpoint
curl http://localhost:8000/api/v1/entities \
  -H "Authorization: Bearer $TOKEN"
```

#### 2. WebSocket Connection
```javascript
// In browser console on http://localhost:5173
const ws = new WebSocket('ws://localhost:8000/ws?token=YOUR_TOKEN');
ws.onopen = () => console.log('Connected');
ws.onmessage = (event) => console.log('Message:', event.data);
ws.send(JSON.stringify({type: 'ping'}));
```

#### 3. GraphQL Query
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "query": "{ entities(limit: 5) { id name type confidence } }"
  }'
```

#### 4. Monitoring Check
```bash
# Check Prometheus
curl http://localhost:9090/api/v1/targets

# Check metrics endpoint
curl http://localhost:8000/metrics

# Check Grafana
curl http://localhost:3001/api/health
```

---

## 📊 Progress Tracking

### Daily Standup Template

**What I completed yesterday:**
- [ ] Task 1
- [ ] Task 2

**What I'm working on today:**
- [ ] Task 3
- [ ] Task 4

**Blockers:**
- None / Issue description

**Current Phase:** Phase X, Week Y, Day Z

---

## 🆘 Getting Help

### Debugging Steps
1. Check service logs: `docker-compose logs -f SERVICE_NAME`
2. Check database connections: `psql -h localhost -U kglab -d knowledge_graph_lab`
3. Test API directly: Use Swagger UI at http://localhost:8000/docs
4. Check frontend console: Browser DevTools → Console
5. Check network requests: Browser DevTools → Network

### Key Log Locations
- Backend logs: Terminal running uvicorn
- PostgreSQL logs: `docker-compose logs postgres`
- Redis logs: `docker-compose logs redis`
- Frontend logs: Browser console
- Prometheus logs: `docker-compose -f docker-compose.monitoring.yml logs prometheus`

---

## ✅ Daily Verification Checklist

Before ending each day, verify:

- [ ] All Docker containers running: `docker-compose ps`
- [ ] Backend API responding: `curl http://localhost:8000/health`
- [ ] Frontend loading: Visit http://localhost:5173
- [ ] Database accessible: `psql -h localhost -U kglab -l`
- [ ] Changes committed: `git status`
- [ ] Tests passing: `pytest` or `npm test`

---

## 🎯 Success Indicators

### After Phase 1:
- ✅ Can login and logout
- ✅ Token appears in API requests
- ✅ Protected routes redirect to login

### After Phase 2:
- ✅ Feed shows 1000+ items
- ✅ WebSocket status shows "connected"
- ✅ Entity changes update in real-time

### After Phase 3:
- ✅ GraphQL playground accessible
- ✅ Complex queries work
- ✅ Page loads faster

### After Phase 4:
- ✅ Grafana dashboards show data
- ✅ Tests pass with >80% coverage
- ✅ Load test succeeds

---

## 📞 Next Steps

1. ✅ Read PRODUCTION-READINESS-PROPOSAL.md (overview)
2. ✅ Review TECHNICAL-IMPLEMENTATION-SPEC.md (details)
3. ✅ Setup environment using DEPENDENCIES-AND-CONFIG.md
4. ▶️ **Start Phase 1, Week 1, Day 1** (this guide)
5. ▶️ Daily: Update progress, commit code, verify checklist

---

**Ready to start? Begin with Phase 1, Week 1, Day 1 above!** 🚀

