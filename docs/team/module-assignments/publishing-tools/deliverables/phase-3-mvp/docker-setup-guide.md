# Docker Setup Guide for Migration Testing

**Date:** 2025-11-17  
**Purpose:** Set up Docker environment to test Alembic migrations

---

## Issue

Docker Desktop is running, but the `docker` command is not available in the terminal PATH.

---

## Solution Options

### Option 1: Restart Terminal (Recommended)

Docker Desktop adds the Docker binaries to your PATH, but existing terminal sessions don't pick up the change.

**Steps:**
1. Close your current terminal/IDE terminal
2. Open a new terminal window
3. Verify Docker is available:
   ```bash
   docker --version
   docker compose version
   ```

### Option 2: Add Docker to PATH Manually

If restarting doesn't work, add Docker to your PATH:

**For zsh (default on macOS):**
```bash
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

### Option 3: Use Full Path

You can use the full path to Docker commands:

```bash
/Applications/Docker.app/Contents/Resources/bin/docker --version
/Applications/Docker.app/Contents/Resources/bin/docker compose version
```

---

## Verification Steps

Once Docker is accessible, verify everything is set up:

### 1. Check Docker is Running
```bash
docker ps
```
Should show running containers (or empty list if none running).

### 2. Check Docker Compose
```bash
docker compose version
```
Should show version (e.g., `Docker Compose version v2.x.x`).

### 3. Verify Docker Desktop Connection
```bash
docker info
```
Should show Docker system information without errors.

---

## Running Migration Tests

Once Docker is accessible, follow these steps:

### Step 1: Navigate to Publishing Module
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab/modules/standalone/publishing
```

### Step 2: Clean Start (Remove Old Volumes)
```bash
docker compose down -v
```
This removes any existing database data for a clean test.

### Step 3: Start Database Services
```bash
docker compose up -d postgres redis
```
This starts only PostgreSQL and Redis (not the API yet).

### Step 4: Wait for Services to be Healthy
```bash
docker compose ps
```
Wait until both `postgres` and `redis` show `healthy` status.

### Step 5: Install Dependencies (if needed)
If dependencies aren't installed in the container, you may need to:
```bash
# Option A: Build the container (includes requirements.txt)
docker compose build api

# Option B: Install in running container
docker compose exec api pip install -r requirements.txt
```

### Step 6: Run Migration
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab/src/publishing
alembic upgrade head
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial schema for publications and channels
```

### Step 7: Verify Tables Created
```bash
docker exec -it publishing-postgres-1 psql -U publishing_user -d publishing_db -c "\dt"
```

**Expected Output:**
```
                    List of relations
 Schema |            Name             | Type  |     Owner
--------+-----------------------------+-------+------------------
 public | alembic_version             | table | publishing_user
 public | publishing_analytics       | table | publishing_user
 public | publishing_channels         | table | publishing_user
 public | publishing_publications    | table | publishing_user
 public | publishing_subscribers     | table | publishing_user
 public | publishing_templates        | table | publishing_user
```

### Step 8: Start Application
```bash
cd /Users/benschreiber/Desktop/knowledge-graph-lab/modules/standalone/publishing
docker compose up -d
```

### Step 9: Check Application Logs
```bash
docker compose logs api
```

Look for:
- ✅ "Database initialization complete (migrations managed by Alembic)"
- ✅ No errors about missing tables
- ✅ Application started successfully

### Step 10: Test Health Endpoint
```bash
curl http://localhost:8080/health
```

Should return JSON with health status.

---

## Troubleshooting

### Issue: "docker: command not found"
**Solution:** Restart terminal or add Docker to PATH (see Option 2 above).

### Issue: "Cannot connect to Docker daemon"
**Solution:** 
- Ensure Docker Desktop is running
- Check Docker Desktop status in menu bar
- Try restarting Docker Desktop

### Issue: "ModuleNotFoundError" when running alembic
**Solution:**
- Install dependencies: `pip install -r requirements.txt`
- Or run inside Docker container: `docker compose exec api alembic upgrade head`

### Issue: "Connection refused" to database
**Solution:**
- Wait for postgres to be healthy: `docker compose ps`
- Check postgres logs: `docker compose logs postgres`
- Verify DATABASE_URL in environment

### Issue: Migration says "Target database is not up to date"
**Solution:**
- Check current version: `alembic current`
- If needed, stamp the database: `alembic stamp head`

---

## Quick Test Script

Save this as `test-migration.sh`:

```bash
#!/bin/bash
set -e

echo "1. Starting database services..."
cd /Users/benschreiber/Desktop/knowledge-graph-lab/modules/standalone/publishing
docker compose down -v
docker compose up -d postgres redis

echo "2. Waiting for services to be healthy..."
sleep 10
docker compose ps

echo "3. Running migration..."
cd /Users/benschreiber/Desktop/knowledge-graph-lab/src/publishing
alembic upgrade head

echo "4. Verifying tables..."
docker exec -it publishing-postgres-1 psql -U publishing_user -d publishing_db -c "\dt"

echo "5. Starting application..."
cd /Users/benschreiber/Desktop/knowledge-graph-lab/modules/standalone/publishing
docker compose up -d

echo "6. Checking logs..."
sleep 5
docker compose logs api | tail -20

echo "✅ Migration test complete!"
```

Make it executable:
```bash
chmod +x test-migration.sh
./test-migration.sh
```

---

## Next Steps After Successful Migration

1. ✅ Verify all 5 tables exist
2. ✅ Test application endpoints
3. ✅ Test migration rollback: `alembic downgrade -1`
4. ✅ Test re-apply: `alembic upgrade head`
5. ✅ Update documentation with migration workflow

---

**Note:** If you're using Cursor's integrated terminal, you may need to restart Cursor or open a new terminal tab for PATH changes to take effect.

