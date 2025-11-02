# Environment Variables Required for AI Module

## ✅ What You Need

### 🔴 **CRITICAL - Must Have**

```bash
# At least ONE LLM provider API key is REQUIRED
OPENAI_API_KEY=sk-your-openai-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

**Without this**: Entity extraction will fail. The system needs an LLM to extract entities and relationships.

### 🟢 **OPTIONAL - Have Good Defaults**

These work automatically with Docker Compose defaults:

```bash
# Database URLs (Docker Compose handles these)
DATABASE_URL=postgresql://ai_user:password@localhost:5432/ai_module
QDRANT_URL=http://localhost:6333
RABBITMQ_URL=amqp://guest:guest@localhost:5672

# Configuration (has defaults)
ENV=development
LOG_LEVEL=INFO
EMBEDDING_DIMENSIONS=384
```

## 📊 Quick Check: Will Your .env Work?

### ✅ **Minimum Working Configuration**

Your .env needs **at least**:
```bash
OPENAI_API_KEY=sk-your-actual-key
```

That's it! Everything else has defaults that work with `docker-compose up -d`.

### 🎯 **Recommended Configuration**

For best results, add:
```bash
# Required
OPENAI_API_KEY=sk-your-openai-key

# Optional but useful
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key  # Fallback
LOG_LEVEL=DEBUG  # For development
EMBEDDING_DIMENSIONS=384  # Default, but good to be explicit
```

## 🧪 Test Your Configuration

Run this to verify your environment:

```bash
python test_rebuild.py
```

If you see "Configuration loaded" with your embedding dimensions, your .env is working!

## 🐳 Docker Services

When you run `docker-compose up -d`, these services start with default credentials:

- **PostgreSQL**: `postgresql://ai_user:password@localhost:5432/ai_module`
- **Qdrant**: `http://localhost:6333`
- **RabbitMQ**: `amqp://guest:guest@localhost:5672`

**No additional configuration needed** - the defaults in `config.py` match Docker Compose!

## 🔍 What Won't Work Without Proper .env

| Feature | Needs | Will It Work? |
|---------|-------|---------------|
| API Server | Nothing special | ✅ Yes |
| Health Checks | Nothing special | ✅ Yes |
| API Documentation | Nothing special | ✅ Yes |
| **Entity Extraction** | **OPENAI_API_KEY or ANTHROPIC_API_KEY** | ❌ **No** |
| Relationship Mapping | LLM API Key | ❌ No |
| Database Persistence | Docker running | ✅ Yes (auto) |
| Vector Search | Docker running | ✅ Yes (auto) |
| Message Queue | Docker running | ✅ Yes (auto) |

## 🚦 Based on Your Current Setup

If your current `.env` has:

- ✅ **`OPENAI_API_KEY=sk-...`** → **Everything will work!**
- ❌ **No LLM API key** → API will start but extraction will fail
- ✅ **Docker is running** → Database/Qdrant/RabbitMQ will work
- ❌ **Docker not running** → API will start but can't persist data

## 💡 Recommendation

Your `.env` should work **IF** you have:

```bash
OPENAI_API_KEY=sk-proj-...your-actual-key...
```

All other variables are optional and will use sensible defaults!

## 🔧 Quick Test

Test if your environment is properly configured:

```bash
# Test 1: Check if config loads
python -c "from src.ai.config import settings; print(f'OpenAI Key: {\"SET\" if settings.openai_api_key else \"MISSING\"}')"

# Test 2: Run full rebuild test
python test_rebuild.py

# Test 3: Check LLM client
python -c "from src.ai.integrations.llm_client import llm_client; print('LLM client loaded')"
```

If these pass, your `.env` is good! 🎉

