# Knowledge Graph Lab - Development Environment Setup

**Target Time**: 30 minutes setup + 15 minutes verification  
**Prerequisites**: Basic command line familiarity  
**Support**: If you get stuck, check Troubleshooting section below or ask for help

---

## 🎯 Quick Setup Checklist

Copy and paste the commands in your terminal. Check off each step as you complete it:

- [ ] **Python 3.11+** installed and verified
- [ ] **Node.js 20+** installed and verified  
- [ ] **Docker Desktop** running
- [ ] **Git** configured with your credentials
- [ ] **Repository cloned** and environment variables set
- [ ] **Dependencies installed** for your module
- [ ] **Services started** and health checks passing
- [ ] **"Hello World" test** working for your module

---

## 💻 System Requirements

### Minimum Hardware
- **RAM**: 8GB (16GB recommended for smooth Docker operation)
- **Storage**: 5GB free space for project + dependencies + Docker images
- **OS**: macOS, Windows (with WSL2), or Linux

### Required Software Versions
- **Python**: 3.11.0+ (not 3.10 or earlier)
- **Node.js**: 20.10.0+ (LTS version)
- **Docker Desktop**: Latest stable version (includes Docker Compose v2)
- **Git**: Latest version
- **VS Code**: Latest (recommended with Python and TypeScript extensions)

---

## 🚀 Step-by-Step Setup

### Step 1: Install Core Dependencies

#### macOS Setup
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11
python3.11 --version  # Should show 3.11.x

# Install Node.js 20 LTS
brew install node@20
node --version  # Should show v20.x.x
npm --version   # Should show 10.x.x

# Install Docker Desktop
brew install --cask docker
# Start Docker Desktop from Applications
```

#### Windows Setup (WSL2 Recommended)
```powershell
# Install Windows Subsystem for Linux 2 (if not already)
wsl --install Ubuntu

# Switch to WSL2 Ubuntu terminal for remaining steps
# Install Python 3.11
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 python3.11-pip python3.11-venv
python3.11 --version

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs
node --version
npm --version

# Download and install Docker Desktop for Windows
# Make sure WSL2 integration is enabled in Docker settings
```

#### Linux Setup
```bash
# Install Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv
python3.11 --version

# Install Node.js 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs
node --version
npm --version

# Install Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
# Log out and back in for group changes to take effect
```

### Step 2: Clone Repository and Initial Setup

```bash
# Clone the repository
git clone https://github.com/your-username/knowledge-graph-lab.git
cd knowledge-graph-lab

# Verify project structure
ls -la
# You should see: modules/, shared/, mock-data/, docs/, docker-compose.yml

# Create and activate Python virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows WSL: source .venv/bin/activate
# On Windows Command Prompt: .venv\Scripts\activate

# Verify virtual environment
which python  # Should show path to .venv/bin/python
python --version  # Should show Python 3.11.x
```

### Step 3: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Required: Add your API keys (instructions in .env file)
nano .env  # or use your preferred editor
```

**Required .env Configuration:**
```bash
# Database
DATABASE_URL=sqlite:///./kgl.db
VECTOR_DB_URL=http://localhost:6333

# AI Services (get API keys from providers)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Email Service (for development)
SMTP_HOST=localhost
SMTP_PORT=1025

# Frontend
NEXTAUTH_SECRET=your_nextauth_secret_here
NEXTAUTH_URL=http://localhost:3000

# Development mode
DEBUG=True
LOG_LEVEL=INFO
```

### Step 4: Module-Specific Setup

Choose your assigned module and follow the specific setup:

#### Module 1: Data Ingestion Setup
```bash
cd modules/module-1-ingestion

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi; print('FastAPI installed successfully')"
python -c "import playwright; print('Playwright installed successfully')"

# Install Playwright browsers (for web scraping)
python -m playwright install chromium

# Test basic functionality
python src/main.py --test
# Should output: "Module 1 setup successful"
```

#### Module 2: Knowledge Graph Setup
```bash
cd modules/module-2-knowledge-graph

# Install Python dependencies
pip install -r requirements.txt

# Test AI service connections
python -c "
import openai
import os
print('OpenAI library installed')
# Verify API key format (but don't expose it)
if os.getenv('OPENAI_API_KEY', '').startswith('sk-'):
    print('OpenAI API key format looks correct')
else:
    print('⚠️  OpenAI API key not set or incorrect format')
"

# Test vector database connection (will start automatically with docker-compose)
python src/test_setup.py
# Should output: "Module 2 setup successful"
```

#### Module 3: Reasoning Engine Setup
```bash
cd modules/module-3-reasoning

# Install Python dependencies
pip install -r requirements.txt

# Test template engine and content generation
python -c "
import jinja2
from datetime import datetime
print('Template engine ready')
print(f'Current time: {datetime.now()}')
"

# Test email functionality
python src/test_setup.py
# Should output: "Module 3 setup successful"
```

#### Module 4: Frontend Setup
```bash
cd modules/module-4-frontend

# Install Node.js dependencies
npm install

# Verify Next.js installation
npx next --version
# Should show: Next.js 14.x.x

# Test TypeScript compilation
npm run type-check

# Start development server (test)
npm run dev
# Should start on http://localhost:3000
# Press Ctrl+C to stop
```

### Step 5: Start All Services

```bash
# Return to project root
cd ../..  # or cd /path/to/knowledge-graph-lab

# Start all backend services with Docker
docker-compose up -d

# Verify services are running
docker-compose ps
# Should show: postgres, redis, qdrant all "Up"

# Check service health
curl http://localhost:6333/collections  # Qdrant vector DB
curl http://localhost:8001/health       # Module 1 API
curl http://localhost:8002/health       # Module 2 API  
curl http://localhost:8003/health       # Module 3 API

# Start frontend (in separate terminal)
cd modules/module-4-frontend
npm run dev
# Should be accessible at http://localhost:3000
```

### Step 6: Verification Tests

Run these tests to confirm everything is working:

```bash
# Database connection test
python shared/db/test_connection.py
# Expected: "✅ Database connection successful"

# Module integration test
python scripts/test_module_communication.py
# Expected: "✅ All modules responding correctly"

# Frontend integration test (open browser)
# Visit: http://localhost:3000
# Should see: KGL homepage with navigation
```

---

## 🔧 Development Workflow

### Daily Startup
```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Start backend services
docker-compose up -d

# 3. Start your module's development server
cd modules/module-X-your-module
# For Python modules:
python src/main.py
# For frontend:
npm run dev
```

### Development Commands
```bash
# Run tests for your module
npm test          # Frontend
python -m pytest # Python modules

# Check code quality
npm run lint      # Frontend
black src/ && flake8 src/  # Python modules

# Database operations
python scripts/migrate.py    # Run migrations
python scripts/seed_data.py  # Load sample data
```

### Daily Shutdown
```bash
# Stop development servers (Ctrl+C)
# Stop Docker services
docker-compose down
```

---

## 🚨 Troubleshooting

### Common Python Issues

**Problem**: `python3.11: command not found`
```bash
# Solution: Verify Python installation
which python3
python3 --version
# If wrong version, reinstall Python 3.11 following setup steps above
```

**Problem**: `pip install` fails with permission errors
```bash
# Solution: Make sure virtual environment is activated
source .venv/bin/activate
which pip  # Should show .venv/bin/pip
```

**Problem**: Import errors with Python packages
```bash
# Solution: Reinstall requirements in virtual environment
pip install --upgrade pip
pip install -r requirements.txt
```

### Common Node.js Issues

**Problem**: `npm install` fails
```bash
# Solution: Clear npm cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Next.js won't start
```bash
# Check port availability
lsof -i :3000  # Kill any existing processes
npm run dev
```

### Common Docker Issues

**Problem**: Docker services won't start
```bash
# Check Docker is running
docker info

# Check for port conflicts
docker-compose down
docker-compose up -d

# View service logs
docker-compose logs postgres
docker-compose logs redis
docker-compose logs qdrant
```

**Problem**: Database connection fails
```bash
# Reset database completely
docker-compose down -v  # Removes volumes
docker-compose up -d
python shared/db/init_db.py  # Recreate tables
```

### Module-Specific Issues

**Module 1**: Web scraping blocked
```bash
# Test with basic requests first
python -c "import requests; print(requests.get('https://httpbin.org/get').status_code)"
# Should print: 200
```

**Module 2**: AI API errors
```bash
# Verify API keys are set
echo $OPENAI_API_KEY | cut -c1-10  # Should show: sk-proj-xx
# Test API connection
python -c "import openai; print('API client ready')"
```

**Module 3**: Email sending issues
```bash
# Check MailHog (development email server)
open http://localhost:8025  # Should show MailHog interface
```

**Module 4**: Build errors
```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

### Getting Help

1. **Check the logs first**:
   ```bash
   # Python modules
   tail -f logs/module-X.log
   
   # Frontend
   npm run dev  # Check terminal output
   
   # Docker services  
   docker-compose logs -f
   ```

2. **Common fixes**:
   - Restart Docker: `docker-compose restart`
   - Reinstall dependencies: `pip install -r requirements.txt` or `npm ci`
   - Clear caches: `npm cache clean --force` or `pip cache purge`

3. **Still stuck?**:
   - Check GitHub Issues for similar problems
   - Ask in Discord/Slack with error message and setup details
   - Schedule office hours with project lead

---

## 🎯 Success Confirmation

**You're ready to start development when:**

✅ **All services running**: `docker-compose ps` shows all services "Up"  
✅ **Your module responds**: Health check endpoint returns 200  
✅ **Database connected**: Test connection script passes  
✅ **Dependencies installed**: No import errors in test scripts  
✅ **Development workflow**: You can start/stop your module successfully  

**Next Steps:**
1. Complete your Week 1 research brief
2. Review module specification and start planning implementation
3. Join daily standup meetings and communicate progress
4. Begin Tier 1 development in Week 3

---

**Setup Time**: Most interns complete setup in 30-45 minutes  
**Support**: Available during office hours or via Discord/Slack  
**Documentation**: This guide will be updated based on common issues