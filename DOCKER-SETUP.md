# Docker Setup for Publishing Module

## Quick Start with PostgreSQL

Everything runs in Docker - no local installation needed!

### 1. Start All Services (PostgreSQL + Redis + API)

**Option A: Use Docker Desktop's docker binary directly:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab
/Applications/Docker.app/Contents/Resources/bin/docker compose up --build
```

**Option B: Use the helper script:**
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab
./docker-compose-run.sh up --build
```

**Option C: Start just PostgreSQL and Redis (if running API separately):**
```bash
/Applications/Docker.app/Contents/Resources/bin/docker compose up postgres redis -d
```

This will:
- ✅ Start PostgreSQL in a container (port 5432)
- ✅ Start Redis in a container (port 6379)  
- ✅ Build and start the API (port 8080)
- ✅ Start the frontend (port 3000)
- ✅ Auto-create database tables
- ✅ Use your `.env` file for AWS credentials

### 2. Access Services

Once running:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8080/api/v1/docs
- **Health Check**: http://localhost:8080/health

### 3. Stop Services

Press `Ctrl+C` or:
```bash
docker compose down
```

### 4. Stop and Remove Data (Clean Start)

```bash
docker compose down -v  # Removes volumes too
```

---

## Configuration

The `docker-compose.yml` is already configured correctly:

### Database Connection (When Running in Docker)

In Docker, services connect using service names:
- **Database Host**: `postgres` (not `localhost`)
- **Redis Host**: `redis` (not `localhost`)

This is already set in `docker-compose.yml` (lines 44, 51).

### Environment Variables

Your `.env` file will be loaded automatically. Make sure it has:
```bash
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-2
SES_SENDER_EMAIL=noreply@distributedcreatives.org
TEST_EMAIL=bschreibero@icloud.com
```

---

## Troubleshooting

### Docker Not Found Error

If you see `docker: command not found`:

1. **Start Docker Desktop** (macOS):
   - Open Docker Desktop from Applications
   - Wait for it to fully start (whale icon in menu bar should be steady)
   - Try the command again

2. **Check Docker is Running**:
   ```bash
   docker ps
   ```
   Should show running containers (or empty list if nothing running)

3. **If Docker Desktop isn't installed**:
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop
   - Restart terminal

### Port Already in Use

If you see `port is already allocated`:

```bash
# Stop existing containers
docker compose down

# Or kill process using the port
lsof -ti:5432 | xargs kill -9  # PostgreSQL
lsof -ti:6379 | xargs kill -9  # Redis
lsof -ti:8080 | xargs kill -9  # API
lsof -ti:3000 | xargs kill -9  # Frontend
```

### Database Connection Issues

1. **Check PostgreSQL is running**:
   ```bash
   docker compose ps
   ```
   Should show `postgres` as `Up (healthy)`

2. **Check logs**:
   ```bash
   docker compose logs postgres
   ```

3. **Verify database was created**:
   ```bash
   docker compose exec postgres psql -U publishing_user -d publishing_db -c "SELECT 1;"
   ```

---

## How It Works

### When Running in Docker

```
┌─────────────────┐
│   Frontend      │ (nginx, port 3000)
│   localhost:3000│
└────────┬────────┘
         │ HTTP
┌────────▼────────┐
│      API        │ (FastAPI, port 8080)
│  localhost:8080 │
└────┬───────┬────┘
     │       │
     │       └───► Redis (port 6379)
     │
     └───────► PostgreSQL (port 5432)
```

All services communicate using Docker service names (`postgres`, `redis`) when inside the Docker network.

### Data Persistence

- **PostgreSQL data**: Stored in Docker volume `postgres_data` (persists between restarts)
- **Redis data**: Stored in Docker volume `redis_data` (persists between restarts)

Data is **NOT** lost when you restart containers (unless you use `docker compose down -v`).

---

## Development Workflow

### Start Everything
```bash
docker compose up --build
```

### View Logs
```bash
docker compose logs -f api        # API logs
docker compose logs -f postgres   # PostgreSQL logs
docker compose logs -f            # All logs
```

### Restart a Service
```bash
docker compose restart api
```

### Stop Everything
```bash
docker compose down
```

### Full Reset (removes all data)
```bash
docker compose down -v
docker compose up --build
```

---

## Verification

After starting, verify everything works:

1. **Check all services are healthy**:
   ```bash
   docker compose ps
   ```
   All should show `Up (healthy)`

2. **Test database connection**:
   ```bash
   curl http://localhost:8080/health
   ```
   Should show database as connected

3. **Test email endpoint**:
   ```bash
   curl http://localhost:8080/api/v1/email/status
   ```
   Should show `"mode": "aws_ses"`

4. **Test channels endpoint**:
   ```bash
   curl http://localhost:8080/api/v1/channels
   ```
   Should return empty list `[]` (no error)

---

**Everything runs in Docker - nothing installed on your machine!** 🐳

