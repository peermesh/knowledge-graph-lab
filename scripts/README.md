# Scripts Directory - Test Infrastructure

This directory contains essential testing and validation scripts for the Knowledge Graph Lab project.

## 🚀 Quick Start Scripts

### Core System Scripts

#### `health_check.py`
**Purpose**: Comprehensive system health check for all services and dependencies.

```bash
python scripts/health_check.py
```

**What it checks:**
- Docker services (postgres, redis, qdrant)
- Service ports and connectivity
- Module API endpoints (Module 1-4)
- Environment variables and dependencies
- Database connectivity
- File permissions

**Exit codes:**
- `0`: All healthy (green)
- `1`: Some warnings but functional (yellow) 
- `2`: Critical issues need fixing (red)

#### `validate_environment.py`
**Purpose**: Pre-flight environment validation before development.

```bash
python scripts/validate_environment.py
```

**Validates:**
- Required software versions (Docker, Python, Node.js)
- Port availability (3000, 5432, 6333, 6379, 8001-8003)
- Project structure and required files
- Docker configuration
- Python dependencies
- Disk space requirements

## 🔧 Database & Infrastructure Scripts

#### `shared/db/init_db.py`
**Purpose**: Initialize PostgreSQL database schema and tables.

```bash
python shared/db/init_db.py
```

**Features:**
- Executes schema.sql and full-schema.sql
- Creates performance indexes
- Adds default system data
- Safe execution (handles existing objects)

#### `shared/db/test_connection.py`
**Purpose**: Test all database connections (PostgreSQL, Redis, Qdrant).

```bash
python shared/db/test_connection.py
```

**Tests:**
- PostgreSQL: Connection, read/write operations, table counting
- Redis: Connection, caching operations, memory usage
- Qdrant: HTTP API, vector operations, collection management

#### `seed_data.py`
**Purpose**: Load sample data into databases for testing.

```bash
python scripts/seed_data.py
```

**Seeds:**
- PostgreSQL: Documents, entities, relationships
- Redis: Cache entries, counters, session data
- Qdrant: Sample vector embeddings
- Uses mock-data/ files if available, fallback to built-in data

## 🌐 Communication & Integration Scripts

#### `test_module_communication.py`
**Purpose**: Test inter-module API communication and data flow.

```bash
python scripts/test_module_communication.py
```

**Tests:**
- Module health endpoints (8001, 8002, 8003, 3000)
- API endpoint connectivity
- Simulated data flow (Module 1 → 2 → 3 → 4)
- Timeout handling and graceful degradation
- Connection resilience

## 📋 Legacy/Maintenance Scripts

#### `validate_repository.py`
**Purpose**: Validate repository structure and configuration files.

```bash
python scripts/validate_repository.py
```

#### `validate_starter_code.py` 
**Purpose**: Validate module starter code and templates.

```bash
python scripts/validate_starter_code.py
```

#### `run_all_validations.sh`
**Purpose**: Execute all validation scripts in sequence.

```bash
./scripts/run_all_validations.sh
```

## 🏃‍♂️ Common Usage Workflows

### Day 1 Intern Setup Workflow
```bash
# 1. Validate environment is ready
python scripts/validate_environment.py

# 2. Start Docker services  
docker-compose up -d

# 3. Initialize database
python shared/db/init_db.py

# 4. Test all connections
python shared/db/test_connection.py

# 5. Load sample data
python scripts/seed_data.py

# 6. Run health check
python scripts/health_check.py

# 7. Test module communication
python scripts/test_module_communication.py
```

### Development Day Workflow
```bash
# Quick health check
python scripts/health_check.py

# If services are down, start them
docker-compose up -d

# Test specific connections if needed
python shared/db/test_connection.py
```

### Troubleshooting Workflow
```bash
# 1. Check what's wrong
python scripts/health_check.py

# 2. Validate environment
python scripts/validate_environment.py  

# 3. Test database connections
python shared/db/test_connection.py

# 4. Check Docker logs
docker-compose logs [service-name]

# 5. Re-initialize if needed
python shared/db/init_db.py
```

## 🎯 Script Features

### Error Handling
- **Graceful failures**: Scripts continue running even if some services are down
- **Colored output**: Green (success), Yellow (warning), Red (error), Blue (info)
- **Detailed logging**: All scripts log to `logs/` directory with timestamps
- **Exit codes**: Proper exit codes for automation and CI/CD

### Safety Features
- **Read-only operations**: Most scripts avoid making changes unless explicitly designed to
- **Confirmation prompts**: Destructive operations ask for confirmation
- **Rollback support**: Database scripts handle existing data safely
- **Timeout handling**: Network operations have reasonable timeouts

### Automation Ready
- **JSON output**: Health check creates `health_check_results.json` for monitoring
- **Machine readable**: Scripts can be used in CI/CD pipelines
- **Consistent interface**: All scripts follow similar patterns and conventions

## 🔍 Output Interpretation

### Health Check Status Icons
- ✅ **Green**: Service healthy and working correctly
- ⚠️ **Yellow**: Service working but with warnings or suboptimal configuration
- ❌ **Red**: Service failed or not working
- 🔍 **Blue**: Informational messages

### Common Warning Messages
- `"not running (expected during setup)"` - Service not started yet, normal during setup
- `"not executable (chmod +x script)"` - File permissions need fixing
- `"timeout (may be starting up)"` - Service is slow to respond, possibly still starting

### When to be Concerned
- Multiple red (❌) failures in core services (postgres, redis)
- Database connection failures after services are confirmed running
- Missing required files or scripts
- Port conflicts preventing service startup

## 💡 Tips for Interns

1. **Always run health_check.py first** - It gives you the complete system status
2. **Use validate_environment.py before starting** - Saves time by catching issues early
3. **Check logs directory** - All scripts create detailed logs for troubleshooting
4. **Scripts are safe to re-run** - Most scripts handle existing data/services gracefully
5. **Docker services must be running** - Use `docker-compose up -d` to start background services

## 🚨 Troubleshooting Quick Fixes

### "Connection refused" errors
```bash
docker-compose up -d  # Start services
docker-compose ps     # Check service status
```

### "Permission denied" errors  
```bash
chmod +x scripts/*.py shared/db/*.py
```

### "Module not found" errors
```bash
pip install -r requirements.txt  # If requirements.txt exists
# Or install individually: pip install aiohttp psycopg2 redis docker
```

### Database "does not exist" errors
```bash
python shared/db/init_db.py  # Initialize database schema
```

### Port already in use
```bash
docker-compose down  # Stop conflicting services
# Or change ports in docker-compose.yml
```

---

**For more help**: Check the logs in `logs/` directory or run scripts with verbose output to see detailed error messages.