# Docker-First Development Policy

**Effective Date**: October 28, 2025  
**Status**: **MANDATORY**

---

## 🎯 Core Principle

**ALL development work on this project MUST be done inside Docker containers.**  
No exceptions unless explicitly approved and documented.

---

## 📋 Policy Rules

### ✅ Required Practices

1. **Use Docker Compose for all services**
   - API development: Always use `docker-compose up api`
   - Full stack: Always use `docker-compose up`
   - Never run `uvicorn`, `python`, or similar commands directly on the host

2. **Build in Docker**
   - All builds must happen in Docker containers
   - Use `docker-compose build` or `docker-compose up --build`
   - Never install project dependencies on the host system

3. **Testing in Docker**
   - Run tests inside containers: `docker-compose exec api pytest`
   - Performance tests must run in containerized environment
   - Integration tests must use docker-compose services

4. **Database and Services**
   - All databases (PostgreSQL, Redis, etc.) run in containers
   - External service mocks run in containers
   - No localhost databases or services on host

### ❌ Prohibited Practices

1. **Never** run `uvicorn` directly on host
2. **Never** run `python -m http.server` on host for project files
3. **Never** install project dependencies with `pip install` on host
4. **Never** run database migrations outside containers
5. **Never** use host-installed Redis, PostgreSQL, or other services

---

## 🚀 Standard Commands

### Starting the Project

```bash
# Start everything (recommended)
cd /Users/benschreiber/Desktop/knowledge-graph-lab
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f
```

### Development Workflow

```bash
# Rebuild after code changes
docker-compose up --build

# Restart a specific service
docker-compose restart api

# Run commands inside container
docker-compose exec api python -m pytest
docker-compose exec api black src/
docker-compose exec api ruff check src/
```

### Debugging

```bash
# View API logs
docker-compose logs -f api

# Access container shell
docker-compose exec api /bin/bash

# Check container health
docker-compose ps
docker ps
```

### Cleanup

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Remove all containers and rebuild
docker-compose down -v
docker-compose up --build
```

---

## 🔧 Configuration

### Environment Variables

All environment variables should be defined in:
1. `docker-compose.yml` (for container config)
2. `.env` file (for secrets, not committed)
3. Never set environment variables in host shell for project use

### Port Mappings

Current port mappings (defined in docker-compose.yml):
- **API**: `8080:8080`
- **Frontend**: `3000:80`

---

## 📊 Benefits of Docker-First Approach

1. **Consistency**: Same environment for all developers and CI/CD
2. **Isolation**: Project dependencies don't pollute host system
3. **Reproducibility**: Easy to reset and rebuild clean environment
4. **Production Parity**: Dev environment matches production containers
5. **Onboarding**: New developers just need `docker-compose up`

---

## 🚨 Emergency Procedures

### If Docker Won't Start

```bash
# Check Docker Desktop is running
open -a Docker

# Wait for Docker to start (takes 30-60 seconds)
docker info

# If stuck, restart Docker Desktop
killall Docker && open -a Docker
```

### If Containers Won't Start

```bash
# Check for port conflicts
lsof -i :8080
lsof -i :3000

# Kill conflicting processes
lsof -ti:8080 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### If Database Is Corrupted

```bash
# Reset everything
docker-compose down -v
docker-compose up --build

# Note: In DEBUG mode, we use in-memory stores, so this is quick
```

---

## 🎓 For AI Assistants / Automated Tools

When working on this codebase:

1. **ALWAYS check if Docker is running** before starting work
2. **ALWAYS use docker-compose commands** for running services
3. **NEVER suggest** running Python commands directly on host
4. **NEVER install** dependencies outside Docker
5. **ALWAYS verify** containers are healthy: `docker-compose ps`

### Quick Pre-Flight Check

```bash
# Before any work, verify Docker setup:
cd /Users/benschreiber/Desktop/knowledge-graph-lab
docker info || echo "Start Docker first!"
docker-compose ps
```

---

## 📝 Exceptions Log

If an exception to this policy is required, document it here:

| Date | Reason | Approved By | Duration |
|------|--------|-------------|----------|
| _None_ | _None_ | _None_ | _None_ |

---

## ✅ Verification Checklist

Before starting work on this project:

- [ ] Docker Desktop is running
- [ ] `docker info` returns successfully
- [ ] No services running on ports 8080 or 3000 on host
- [ ] Latest changes pulled: `git pull`
- [ ] Containers built: `docker-compose build`
- [ ] All services healthy: `docker-compose ps`

---

## 📚 Additional Resources

- [Docker Compose Quickstart](./DEMO-QUICKSTART.md)
- [Docker Compose File](./docker-compose.yml)
- [Dockerfile](./Dockerfile)
- [Project README](./README.md)

---

**Remember**: If it's not in a container, it's not part of this project! 🐳




