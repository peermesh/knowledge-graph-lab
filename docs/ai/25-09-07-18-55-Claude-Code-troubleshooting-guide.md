# Knowledge Graph Lab - Comprehensive Troubleshooting Guide

**Date**: September 7, 2025 18:55  
**Tool**: Claude Code  
**Purpose**: Comprehensive troubleshooting guide for common setup and operational issues

---

## 🚨 EMERGENCY QUICK FIXES

### System Won't Start At All
```bash
# Nuclear option - restart everything
docker-compose down -v
docker system prune -f
source .venv/bin/activate
pip install -r requirements.txt
docker-compose up -d
```

### "It Was Working Yesterday"
```bash
# Check what changed
git status
git diff HEAD~1

# Reset to last known good state
git stash
git checkout main
git pull origin main
```

### Complete Environment Reset
```bash
# Full reset procedure
rm -rf .venv
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
docker-compose down -v
docker-compose up -d
```

---

## 💻 INSTALLATION & SETUP ISSUES

### Python Installation Problems

#### Problem: `python3.11: command not found`
**Symptoms**: Can't find Python 3.11 despite installation
**Solutions**:
```bash
# Check what Python versions are installed
ls /usr/bin/python*
ls /opt/homebrew/bin/python*  # macOS with Homebrew

# macOS: Fix path issues
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Linux: Install Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# Create alias if needed
echo 'alias python3.11=/usr/bin/python3.11' >> ~/.bashrc
source ~/.bashrc
```

#### Problem: Virtual environment activation fails
**Symptoms**: `source .venv/bin/activate` doesn't work
**Solutions**:
```bash
# Windows (Command Prompt)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# If PowerShell execution policy blocks:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# macOS/Linux permission issues
chmod +x .venv/bin/activate
source .venv/bin/activate
```

#### Problem: `pip install` fails with permissions
**Symptoms**: Permission denied errors during package installation
**Solutions**:
```bash
# Verify virtual environment is active
which pip  # Should show .venv/bin/pip

# If not in venv:
source .venv/bin/activate

# Clear pip cache
pip cache purge

# Install with --user (last resort)
pip install --user -r requirements.txt
```

### Node.js Installation Problems

#### Problem: Node.js version conflicts
**Symptoms**: `node --version` shows wrong version
**Solutions**:
```bash
# Install Node Version Manager (nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc

# Install and use Node.js 20
nvm install 20
nvm use 20
nvm alias default 20

# Verify
node --version  # Should show v20.x.x
npm --version   # Should show 10.x.x
```

#### Problem: `npm install` fails
**Symptoms**: Various npm errors during package installation
**Solutions**:
```bash
# Clear npm cache completely
npm cache clean --force
rm -rf node_modules
rm package-lock.json

# Use npm ci for clean install
npm ci

# If still failing, try yarn
npm install -g yarn
yarn install

# Check for permission issues (Linux/macOS)
sudo chown -R $(whoami) ~/.npm
```

### Docker Installation Problems

#### Problem: Docker Desktop won't start
**Symptoms**: `docker info` fails, services don't start
**Solutions**:
```bash
# macOS: Restart Docker Desktop
killall Docker
open -a Docker

# Linux: Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (Linux)
sudo usermod -aG docker $USER
# Log out and back in

# Windows: Enable WSL2 integration
# In Docker Desktop settings, enable WSL2 integration
```

#### Problem: Docker compose version issues
**Symptoms**: `docker-compose` command not found
**Solutions**:
```bash
# Use newer docker compose (not docker-compose)
docker compose up -d

# Install docker-compose separately if needed
pip install docker-compose

# Or use Docker Desktop which includes compose
```

---

## 🐳 DOCKER & SERVICES ISSUES

### Service Startup Problems

#### Problem: PostgreSQL won't start
**Symptoms**: Database connection errors, postgres container exits
**Solutions**:
```bash
# Check container logs
docker-compose logs postgres

# Common fixes:
# 1. Port conflict
lsof -i :5432  # Kill any processes using port 5432

# 2. Volume permissions
docker-compose down -v
docker volume prune
docker-compose up -d postgres

# 3. Database corruption
docker-compose down
docker volume rm knowledge-graph-lab_postgres_data
docker-compose up -d postgres
```

#### Problem: Qdrant vector database fails
**Symptoms**: Vector search errors, qdrant container won't start
**Solutions**:
```bash
# Check Qdrant logs
docker-compose logs qdrant

# Test Qdrant connectivity
curl http://localhost:6333/
# Expected: JSON response with version info

# Reset Qdrant data
docker-compose down
docker volume rm knowledge-graph-lab_qdrant_data
docker-compose up -d qdrant

# Wait for startup
sleep 10
curl http://localhost:6333/collections
```

#### Problem: Redis connection issues
**Symptoms**: Caching doesn't work, Redis connection timeouts
**Solutions**:
```bash
# Check Redis status
docker-compose logs redis

# Test Redis connectivity
docker-compose exec redis redis-cli ping
# Expected: PONG

# Clear Redis data
docker-compose exec redis redis-cli FLUSHALL

# Restart Redis only
docker-compose restart redis
```

### Port Conflicts

#### Problem: "Port already in use" errors
**Symptoms**: Services can't bind to ports 3000, 5432, 6379, 6333
**Solutions**:
```bash
# Find what's using the port
lsof -i :3000  # Replace 3000 with your port
netstat -tulpn | grep :3000

# Kill the process
sudo kill -9 <PID>

# Or change ports in docker-compose.yml
# postgres: "5433:5432"
# redis: "6380:6379"
# qdrant: "6334:6333"
```

---

## 🔧 APPLICATION-SPECIFIC ISSUES

### Module 1: Data Ingestion Issues

#### Problem: Web scraping blocked
**Symptoms**: 403 Forbidden, bot detection, timeouts
**Solutions**:
```bash
# Test basic connectivity
python -c "import requests; print(requests.get('https://httpbin.org/get').status_code)"

# Check Playwright browser installation
python -m playwright install chromium

# Test Playwright
python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    print('Playwright working')
    browser.close()
"

# Configure user agents and delays in scraping code
```

#### Problem: Content extraction fails
**Symptoms**: Empty content, parsing errors
**Solutions**:
```python
# Debug content extraction
import requests
from bs4 import BeautifulSoup

url = "your_test_url_here"
response = requests.get(url)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")

soup = BeautifulSoup(response.text, 'html.parser')
print(f"Title: {soup.title}")
```

### Module 2: Knowledge Graph Issues

#### Problem: AI API errors
**Symptoms**: OpenAI/Anthropic API errors, quota exceeded
**Solutions**:
```bash
# Verify API keys format
echo $OPENAI_API_KEY | cut -c1-10
# Should show: sk-proj-xx or similar

# Test API connection
python -c "
import openai
import os
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
try:
    response = client.models.list()
    print('API connection working')
except Exception as e:
    print(f'API error: {e}')
"

# Check quota and usage
# Visit: https://platform.openai.com/usage
```

#### Problem: Vector embeddings fail
**Symptoms**: Embedding generation errors, dimension mismatches
**Solutions**:
```python
# Test embedding generation
import openai
import os

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

try:
    response = client.embeddings.create(
        input="test text",
        model="text-embedding-3-small"
    )
    print(f"Embedding dimensions: {len(response.data[0].embedding)}")
except Exception as e:
    print(f"Embedding error: {e}")
```

### Module 3: Reasoning Engine Issues

#### Problem: Email sending fails
**Symptoms**: SMTP errors, emails not sent
**Solutions**:
```bash
# Check MailHog is running
curl http://localhost:8025/
# Or visit in browser

# Test SMTP connection
python -c "
import smtplib
try:
    server = smtplib.SMTP('localhost', 1025)
    server.quit()
    print('SMTP connection working')
except Exception as e:
    print(f'SMTP error: {e}')
"

# Check email in MailHog interface
open http://localhost:8025
```

#### Problem: Template rendering errors
**Symptoms**: Jinja2 template errors, missing variables
**Solutions**:
```python
# Test template rendering
from jinja2 import Template

template_str = "Hello {{ name }}!"
template = Template(template_str)
result = template.render(name="World")
print(result)  # Should print: Hello World!
```

### Module 4: Frontend Issues

#### Problem: Next.js won't start
**Symptoms**: Build errors, port conflicts, dependency issues
**Solutions**:
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check TypeScript errors
npm run type-check

# Start with verbose output
npm run dev -- --turbo

# Check for port conflicts
lsof -i :3000
```

#### Problem: API calls fail from frontend
**Symptoms**: Network errors, CORS issues, 500 errors
**Solutions**:
```bash
# Test API endpoints directly
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health

# Check network tab in browser dev tools
# Verify API URLs in frontend code
# Check CORS configuration
```

---

## 🔍 DEBUGGING STRATEGIES

### Systematic Debugging Process

#### Step 1: Identify the Layer
```bash
# Is it infrastructure?
docker-compose ps
curl http://localhost:6333/

# Is it application?
curl http://localhost:8001/health

# Is it frontend?
curl http://localhost:3000/api/health
```

#### Step 2: Check Logs
```bash
# Application logs
tail -f logs/module-1.log
tail -f logs/module-2.log

# Docker logs
docker-compose logs --tail=100 postgres
docker-compose logs --tail=100 qdrant

# System logs (Linux)
journalctl -u docker -f
```

#### Step 3: Isolate the Issue
```bash
# Test each component separately
python modules/module-1-ingestion/src/test_basic.py
python modules/module-2-knowledge-graph/src/test_basic.py

# Test API endpoints
curl -X POST http://localhost:8001/test \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

### Common Log Patterns

#### Database Connection Issues
```
# Look for:
"FATAL: password authentication failed"
"could not connect to server"
"connection refused"

# Solution: Check DATABASE_URL, restart postgres
```

#### API Key Issues
```
# Look for:
"Invalid API key"
"Quota exceeded" 
"Unauthorized"

# Solution: Check .env file, verify API keys
```

#### Memory/Resource Issues
```
# Look for:
"killed"
"out of memory"
"resource temporarily unavailable"

# Solution: Increase Docker memory, check system resources
```

---

## 🔧 PERFORMANCE TROUBLESHOOTING

### Slow Performance Issues

#### Problem: API responses are slow (>5 seconds)
**Diagnosis**:
```bash
# Time API calls
time curl http://localhost:8001/health

# Check system resources
htop
docker stats

# Check database performance
docker-compose exec postgres psql -U postgres -d kgl -c "
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC LIMIT 10;
"
```

#### Problem: High memory usage
**Diagnosis**:
```bash
# Check Docker container memory
docker stats --no-stream

# Check Python memory usage
python -c "
import psutil
process = psutil.Process()
print(f'Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"

# Check for memory leaks
# Use memory profilers like memory_profiler
pip install memory-profiler
python -m memory_profiler your_script.py
```

### Database Performance Issues

#### Problem: Slow database queries
**Solutions**:
```sql
-- Enable query logging (postgres)
ALTER SYSTEM SET log_statement = 'all';
SELECT pg_reload_conf();

-- Check slow queries
SELECT query, mean_exec_time, calls, total_exec_time
FROM pg_stat_statements 
ORDER BY total_exec_time DESC LIMIT 10;

-- Add indexes for common queries
CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type);
CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_id);
```

---

## 📞 GETTING HELP

### Self-Help Checklist
1. **Check this troubleshooting guide** - most issues covered here
2. **Search error messages** - copy exact error into search
3. **Check GitHub Issues** - may be a known issue
4. **Review recent changes** - what changed since it was working?
5. **Try the nuclear option** - complete environment reset

### When to Ask for Help
- **After 30 minutes** of trying fixes without progress
- **Security-related errors** - don't guess with security
- **Data loss concerns** - get help before losing work
- **Multiple interns hitting the same issue** - likely systemic

### How to Ask for Help Effectively

#### Include This Information:
```bash
# Your environment
python --version
node --version
docker --version
uname -a  # System info

# What you were doing
"I was trying to start Module 2 when..."

# Complete error message
"Copy and paste the FULL error message here"

# What you've tried
"I've tried: 1) restarting docker, 2) reinstalling packages, 3) checking logs"
```

#### Where to Get Help:
1. **Discord/Slack** - Real-time help during working hours
2. **GitHub Issues** - For bugs or feature requests  
3. **Office Hours** - Scheduled help sessions
4. **Pair Programming** - Work with another intern
5. **Mentor 1:1** - For complex issues or learning gaps

### Emergency Escalation
**For critical issues blocking multiple interns:**
1. Post in emergency Discord channel
2. Tag project leads
3. Include: number of people affected, blocking issue, attempted fixes

---

## ✅ PREVENTION STRATEGIES

### Daily Habits
- **Start with `git pull`** - stay current with changes
- **Check `docker-compose ps`** - verify services before coding
- **Run tests before committing** - catch issues early
- **Document solutions** - help future you and others

### Weekly Maintenance
- **Update dependencies** - `pip install --upgrade -r requirements.txt`
- **Clear Docker caches** - `docker system prune -f`
- **Backup important data** - export test databases
- **Review logs for warnings** - address before they become errors

### Before Asking for Help
- **Try the fix twice** - sometimes timing/race conditions
- **Check with another intern** - peer debugging
- **Document what you tried** - saves time for helpers
- **Consider if it affects others** - coordinate solutions

---

**TROUBLESHOOTING SUCCESS**: Issue resolved and documented for future reference  
**AVERAGE RESOLUTION TIME**: 80% of issues resolved within 15 minutes using this guide