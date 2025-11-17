# PostgreSQL Setup in Docker - Complete Guide

## ✅ Current Status

**PostgreSQL and Redis are now running in Docker containers!**

```bash
# Check status
/Applications/Docker.app/Contents/Resources/bin/docker compose ps
```

Should show:
- ✅ `postgres` - Up (healthy) on port 5432
- ✅ `redis` - Up (healthy) on port 6379

---

## 🎯 Two Ways to Run the API

### Option 1: Everything in Docker (Recommended)

**Start all services including API in Docker:**

```bash
/Applications/Docker.app/Contents/Resources/bin/docker compose up --build
```

**This runs:**
- PostgreSQL (port 5432)
- Redis (port 6379)
- API (port 8080)
- Frontend (port 3000)

**Configuration:**
- API connects to `postgres:5432` (Docker service name)
- API connects to `redis:6379` (Docker service name)
- Set automatically by `docker-compose.yml`

**Advantages:**
- ✅ Everything containerized - nothing on your machine
- ✅ Consistent environment
- ✅ Easy to start/stop everything

---

### Option 2: API Standalone, Database in Docker

**Start just PostgreSQL and Redis:**

```bash
/Applications/Docker.app/Contents/Resources/bin/docker compose up postgres redis -d
```

**Run API separately:**

```bash
python3 -m uvicorn src.publishing.main:app --host 0.0.0.0 --port 8080 --reload
```

**Configuration:**
- API connects to `localhost:5432` (Docker exposed port)
- API connects to `localhost:6379` (Docker exposed port)
- Set in `.env` file: `DATABASE_HOST=localhost`, `REDIS_HOST=localhost`

**Advantages:**
- ✅ Faster development (no Docker rebuild)
- ✅ Hot reload works better
- ✅ Easier debugging

---

## 📝 Configuration Details

### When Running in Docker

The `docker-compose.yml` sets these environment variables for the API container:
```yaml
environment:
  - DATABASE_HOST=postgres    # Docker service name
  - REDIS_HOST=redis          # Docker service name
```

These **override** any values in `.env` file.

### When Running Standalone

Update your `.env` file:
```bash
# For standalone API connecting to Docker PostgreSQL/Redis
DATABASE_HOST=localhost      # Connects to Docker's exposed port 5432
DATABASE_PORT=5432
DATABASE_NAME=publishing_db
DATABASE_USER=publishing_user
DATABASE_PASSWORD=publishing_pass

REDIS_HOST=localhost         # Connects to Docker's exposed port 6379
REDIS_PORT=6379
```

---

## 🔧 Quick Setup Commands

### Start Everything (All in Docker)
```bash
/Applications/Docker.app/Contents/Resources/bin/docker compose up --build
```

### Start Just Database Services
```bash
/Applications/Docker.app/Contents/Resources/bin/docker compose up postgres redis -d
```

### Stop Everything
```bash
/Applications/Docker.app/Contents/Resources/bin/docker compose down
```

### View Logs
```bash
/Applications/Docker.app/Contents/Resources/bin/docker compose logs -f postgres
/Applications/Docker.app/Contents/Resources/bin/docker compose logs -f api
```

### Verify Database Connection
```bash
# Test PostgreSQL
/Applications/Docker.app/Contents/Resources/bin/docker compose exec postgres psql -U publishing_user -d publishing_db -c "SELECT version();"

# Test API can connect
curl http://localhost:8080/health
```

---

## ✅ Verification Checklist

After starting PostgreSQL and Redis:

- [ ] PostgreSQL container is running: `docker compose ps | grep postgres`
- [ ] Redis container is running: `docker compose ps | grep redis`
- [ ] PostgreSQL is healthy: Status shows `(healthy)`
- [ ] Database is accessible: Can run SQL queries
- [ ] API can connect: `/health` endpoint shows database connected
- [ ] Channels endpoint works: `/api/v1/channels` returns without error

---

## 🐛 Troubleshooting

### Database Connection Failed

**If API is in Docker:**
- Check `docker-compose.yml` sets `DATABASE_HOST=postgres`
- Verify `depends_on: postgres` with `condition: service_healthy`

**If API is standalone:**
- Check `.env` has `DATABASE_HOST=localhost`
- Verify PostgreSQL container exposes port 5432: `docker compose ps`
- Test connection: `psql -h localhost -U publishing_user -d publishing_db`

### Port Already in Use

```bash
# Check what's using the port
lsof -i:5432  # PostgreSQL
lsof -i:6379  # Redis

# Stop containers
/Applications/Docker.app/Contents/Resources/bin/docker compose down
```

### Database Not Initialized

The API automatically creates tables on startup. To manually initialize:

```bash
# Connect to database
/Applications/Docker.app/Contents/Resources/bin/docker compose exec postgres psql -U publishing_user -d publishing_db

# Or use Python
python3 -c "
import asyncio
from src.publishing.core.database import create_db_and_tables
asyncio.run(create_db_and_tables())
print('✅ Tables created!')
"
```

---

## 🎯 Recommended Setup (All in Docker)

**Everything runs in Docker - nothing on your machine!**

### Start All Services

```bash
/Applications/Docker.app/Contents/Resources/bin/docker compose up --build
```

This starts:
1. ✅ PostgreSQL (port 5432)
2. ✅ Redis (port 6379)
3. ✅ API (port 8080) - auto-connects to postgres/redis
4. ✅ Frontend (port 3000)

### Access Services

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8080/api/v1/docs
- **Health**: http://localhost:8080/health

### Everything is Containerized

- Database runs in Docker container
- API runs in Docker container
- Frontend runs in Docker container
- No local installation needed

---

## Alternative: Database Only in Docker

If you prefer to run API separately for faster development:

1. **Start PostgreSQL and Redis:**
   ```bash
   /Applications/Docker.app/Contents/Resources/bin/docker compose up postgres redis -d
   ```

2. **Update .env for standalone API:**
   ```bash
   DATABASE_HOST=localhost  # Connect to Docker's exposed port
   REDIS_HOST=localhost     # Connect to Docker's exposed port
   ```

3. **Run API separately:**
   ```bash
   python3 -m uvicorn src.publishing.main:app --host 0.0.0.0 --port 8080 --reload
   ```

---

**Everything runs in Docker containers - nothing installed locally!** 🐳

