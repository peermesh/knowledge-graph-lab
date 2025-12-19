# Quick Start Guide - AI Module

## 🚦 **Two Issues to Fix First**

### **Issue 1: Docker Not Running**
```powershell
# Start Docker Desktop on Windows
# Look for Docker Desktop icon in system tray and start it
# Or search for "Docker Desktop" in Start menu
```

### **Issue 2: Python Dependencies Not Installed**

**Option A: Install All Dependencies** (Recommended)
```powershell
# Install all dependencies (requires Python 3.11+)
pip install -r requirements.txt
```

**Option B: Install Minimal Dependencies** (Just to test)
```powershell
# Core dependencies only
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy psycopg2-binary

# For testing without LLM
pip install pytest httpx
```

---

## 🚀 **Simplified Startup (No Docker/LLM Required)**

If you want to test the API without Docker or LLM providers:

```powershell
# 1. Install minimal dependencies
pip install fastapi uvicorn pydantic pydantic-settings python-dotenv

# 2. Create a minimal .env file
echo "ENV=development" > .env
echo "LOG_LEVEL=INFO" >> .env

# 3. Start API server (will run with limited functionality)
uvicorn src.ai.api.main:app --reload --port 8000
```

Then open: http://localhost:8000/docs

**Note**: Entity extraction won't work without LLM API keys, but you can:
- ✅ View API documentation
- ✅ Test API endpoints structure
- ✅ Validate request/response schemas
- ✅ Verify health check endpoints

---

## 🔧 **Full Setup (With All Features)**

### **Step 1: Start Docker Desktop**
1. Open Docker Desktop application
2. Wait for it to fully start (whale icon in system tray)
3. Verify: `docker info` should work without errors

### **Step 2: Install Python Dependencies**
```powershell
# Option A: Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Option B: Install globally
pip install -r requirements.txt
```

### **Step 3: Configure Environment**
```powershell
# Copy template
cp .env.example .env

# Edit .env and add your OpenAI API key
# Required line:
# OPENAI_API_KEY=sk-your-key-here
```

### **Step 4: Start Services**
```powershell
# Start PostgreSQL, Qdrant, RabbitMQ
docker-compose up -d

# Wait for services to start
Start-Sleep -Seconds 10

# Verify services are running
docker-compose ps
```

### **Step 5: Initialize Database**
```powershell
# Run migrations
alembic upgrade head
```

### **Step 6: Start API Server**
```powershell
# Development mode with auto-reload
uvicorn src.ai.api.main:app --reload --port 8000
```

### **Step 7: Test It!**
```powershell
# Open browser to API documentation
start http://localhost:8000/docs

# Or test with curl
curl http://localhost:8000/ai/v1/health
```

---

## 🛠️ **Troubleshooting**

### **"Docker is not running"**
**Solution**: Start Docker Desktop application and wait for it to fully initialize

### **"ModuleNotFoundError: No module named 'langchain_openai'"**
**Solution**: 
```powershell
pip install -r requirements.txt
```

### **"No module named 'pgvector'"**
**Solution**:
```powershell
pip install pgvector
# Or just run: pip install -r requirements.txt
```

### **"Cannot connect to database"**
**Solution**:
```powershell
# Make sure Docker is running
docker-compose ps

# Restart services if needed
docker-compose restart postgres
```

### **"OPENAI_API_KEY not set"**
**Solution**:
```powershell
# Edit .env file and add your key
notepad .env

# Add this line:
OPENAI_API_KEY=sk-your-actual-key-here
```

---

## 📝 **Quick Commands Reference**

```powershell
# Start everything
docker-compose up -d
uvicorn src.ai.api.main:app --reload --port 8000

# Stop everything
# Press CTRL+C to stop uvicorn
docker-compose down

# View logs
docker-compose logs -f postgres
docker-compose logs -f qdrant
docker-compose logs -f rabbitmq

# Run tests
pytest tests/

# Check API health
curl http://localhost:8000/ai/v1/health
```

---

## ✨ **Minimal Working Example**

If you just want to see it work without full setup:

```powershell
# 1. Install core deps
pip install fastapi uvicorn pydantic python-dotenv

# 2. Create minimal config
@"
ENV=development
LOG_LEVEL=INFO
"@ | Out-File -FilePath .env -Encoding utf8

# 3. Start server
uvicorn src.ai.api.main:app --reload --port 8000

# 4. Open docs
start http://localhost:8000/docs
```

The API will start and show documentation, though entity extraction features will be limited without database and LLM configuration.

---

## 🎯 **Recommended Next Steps**

1. **Get Docker Running**: Start Docker Desktop
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Add API Key**: Edit `.env` with your OpenAI key
4. **Use Startup Script**: `.\scripts\start-dev.ps1`

---

**Need help?** Check the full documentation in `specs/001-docs-team-deliverables/quickstart.md`

