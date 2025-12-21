# Quick Start Guide: PostgreSQL & Redis Integration

## Overview
The publishing module now uses **PostgreSQL** for persistent data storage and **Redis** for caching and real-time features, replacing all in-memory Python dictionaries.

## Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ (for running scripts outside Docker)
- Git (for version control)

## Step 1: Environment Setup

### 1. Copy the Example Environment File

The `.env.example` file is now included in the repository and contains all necessary configuration templates.

```bash
cp .env.example .env
```

This creates your local `.env` file with placeholder values that work for standalone testing.

### 2. (Optional) Update .env with Real Credentials for Production

For standalone testing, the default placeholder values work fine. You can skip this step if you're just testing locally.

If you need real service integration, edit `.env` and add your actual credentials:

**AWS SES (for email delivery):**
```bash
AWS_ACCESS_KEY_ID=your-actual-access-key
AWS_SECRET_ACCESS_KEY=your-actual-secret-key
SES_SENDER_EMAIL=noreply@yourdomain.com
AWS_REGION=us-east-2
```

**Slack API (for Slack integration):**
```bash
SLACK_BOT_TOKEN=xoxb-your-actual-slack-token
SLACK_CHANNEL_ID=your-channel-id
```

**Discord API (for Discord integration):**
```bash
DISCORD_BOT_TOKEN=your-actual-discord-token
DISCORD_CHANNEL_ID=your-channel-id
```

### 3. For Standalone Testing

The default placeholder values in `.env.example` are sufficient for:
- Local development
- Testing API endpoints
- Database operations
- Redis caching
- Mock email/Slack/Discord operations

**No real credentials are required** for standalone testing. The system will run in placeholder mode for external services.

**Note:** The `.env` file is gitignored, so your local credentials won't be committed to the repository.

## Step 2: Start Services

### Option A: Using Docker Compose (Recommended)
```bash
# Start all services (PostgreSQL, Redis, API, Frontend)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api
```

### Option B: Using Docker (if docker-compose not available)
```bash
# Create network
docker network create publishing-network

# Start PostgreSQL
docker run -d --name postgres \
  --network publishing-network \
  -e POSTGRES_USER=publishing_user \
  -e POSTGRES_PASSWORD=publishing_pass \
  -e POSTGRES_DB=publishing_db \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine

# Start Redis
docker run -d --name redis \
  --network publishing-network \
  -p 6379:6379 \
  -v redis_data:/data \
  redis:7-alpine redis-server --appendonly yes

# Build and start API (from project root)
docker build -t publishing-api .
docker run -d --name api \
  --network publishing-network \
  --env-file .env \
  -p 8080:8080 \
  publishing-api
```

## Step 3: Verify Services

### Check API Health
```bash
curl http://localhost:8080/health
```

Expected response:
```json
{
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "database": "connected",
    "redis": "connected"
  }
}
```

### Check Database
```bash
# Connect to PostgreSQL
docker exec -it postgres psql -U publishing_user -d publishing_db

# List tables
\dt

# Exit
\q
```

### Check Redis
```bash
# Connect to Redis
docker exec -it redis redis-cli

# Test connection
ping

# List keys (should be empty initially)
keys *

# Exit
exit
```

## Step 4: Load Mock Data

The system includes comprehensive mock data for AI module integration:

```bash
# Option A: Using Python directly
python scripts/init_mock_data.py

# Option B: Using Docker
docker-compose exec api python scripts/init_mock_data.py

# Custom counts
python scripts/init_mock_data.py --subscribers 20 --content 50
```

This creates:
- Mock subscribers with AI metadata (prompts, preferences, etc.)
- Mock content items with AI scoring
- Sample dispatch batches

## Step 5: Test the API

### List Subscribers
```bash
curl http://localhost:8080/api/v1/subscribers | jq
```

### Create a Subscriber
```bash
curl -X POST http://localhost:8080/api/v1/subscribers \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "preferred_channels": ["email"],
    "topic_interests": {
      "topics": ["AI", "machine learning"]
    },
    "frequency_settings": {
      "type": "daily",
      "time_of_day": "morning"
    }
  }' | jq
```

### List Channels
```bash
curl http://localhost:8080/api/v1/channels | jq
```

### Create a Channel
```bash
curl -X POST http://localhost:8080/api/v1/channels \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Email Newsletter",
    "channel_type": "email",
    "is_active": true,
    "configuration": {
      "provider": "aws_ses"
    }
  }' | jq
```

## Step 6: Test External Services (Placeholder Mode)

Currently, AWS SES, Slack, and Discord run in **placeholder mode** (simulated):

### Test Email Service (Simulated)
```bash
# This will log to console but not send real email
curl -X POST http://localhost:8080/api/v1/publications \
  -H "Content-Type: application/json" \
  -d '{
    "content_ids": ["content-1", "content-2"],
    "channels": ["channel-email"],
    "publication_type": "newsletter"
  }' | jq
```

Check API logs to see simulated email:
```bash
docker-compose logs api | grep "PLACEHOLDER EMAIL"
```

### When You Have Real Credentials

If you need to send real emails or integrate with real Slack/Discord channels, update your `.env` file with actual credentials (see Step 1 for details).

After updating `.env`:

1. **Restart the API service:**
   ```bash
   docker-compose restart api
   ```

2. **Verify credentials are loaded:**
   ```bash
   # Check email service status
   curl http://localhost:8080/api/v1/email/status | jq
   
   # Should show "mode": "aws_ses" instead of "placeholder"
   ```

3. **Test with real service:**
   ```bash
   # Send test email (now uses real AWS SES)
   curl -X POST http://localhost:8080/api/v1/email/test \
     -H "Content-Type: application/json" \
     -d '{
       "to_email": "your-email@example.com",
       "subject": "Test Email",
       "body": "This is a test email from the publishing module"
     }' | jq
   ```

**Important:** 
- Real credentials are only needed for production or integration testing
- For local development, placeholder mode is recommended
- Never commit `.env` with real credentials to version control

## Step 7: Explore Mock Data

### View Mock Subscriber Data
```bash
# Python script to view generated data
python -c "
from src.publishing.ai.mock_data_generator import create_mock_user
import json
user = create_mock_user()
print(json.dumps(user, indent=2))
"
```

### Mock Data Includes:
- **User Info**: Name, email, created date
- **Dispatch Type**: Email (as requested)
- **Frequency**: Daily, weekly, bi-weekly, monthly
- **AI Metadata**:
  - Original prompts (user queries)
  - Refined requests (AI-processed topics, keywords)
  - Content preferences (sources, reading level, length)
  - Engagement history (open/click rates)
  - Personalization settings (style, tone, summarization)

## Troubleshooting

### Service Won't Start
```bash
# Check logs
docker-compose logs postgres
docker-compose logs redis
docker-compose logs api

# Restart services
docker-compose restart

# Clean rebuild
docker-compose down
docker-compose up -d --build
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection settings in .env
cat .env | grep DATABASE

# Test connection
docker-compose exec postgres pg_isready -U publishing_user
```

### Redis Connection Error
```bash
# Check Redis is running
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli ping

# View Redis logs
docker-compose logs redis
```

### Can't Access API
```bash
# Check API is running
docker-compose ps api

# Check API logs
docker-compose logs api

# Check port binding
netstat -an | grep 8080  # macOS/Linux
netstat -ano | findstr 8080  # Windows
```

## Development Workflow

### Watch Logs
```bash
# All services
docker-compose logs -f

# Just API
docker-compose logs -f api

# Just database
docker-compose logs -f postgres
```

### Restart After Code Changes
```bash
# Rebuild and restart API
docker-compose up -d --build api

# Or restart all
docker-compose restart
```

### Clean Database (Reset)
```bash
# Stop services
docker-compose down

# Remove volumes (WARNING: deletes all data)
docker-compose down -v

# Start fresh
docker-compose up -d

# Reload mock data
python scripts/init_mock_data.py
```

### Direct Database Access
```bash
# SQL queries
docker-compose exec postgres psql -U publishing_user -d publishing_db -c "SELECT * FROM publishing_subscribers;"

# Interactive session
docker-compose exec postgres psql -U publishing_user -d publishing_db
```

### Direct Redis Access
```bash
# Interactive session
docker-compose exec redis redis-cli

# Get all keys
docker-compose exec redis redis-cli keys '*'

# Get specific value
docker-compose exec redis redis-cli get 'template:some-id'
```

## What's Different from Before

### Before (In-Memory)
```python
IN_MEMORY_SUBSCRIBERS = []  # Lost on restart
IN_MEMORY_CHANNELS = []     # Lost on restart
IN_MEMORY_PUBLICATIONS = []  # Lost on restart
```

### Now (PostgreSQL + Redis)
```python
# Persistent in PostgreSQL
async for session in get_async_session():
    result = await session.execute(select(Subscriber))
    subscribers = result.scalars().all()

# Cached in Redis for speed
cached = await redis_client.get_json("subscriber:123")
```

## Next Steps

1. ✅ System is running with PostgreSQL and Redis
2. ✅ Mock data loaded for testing
3. ⏳ Add real AWS SES credentials when available
4. ⏳ Add real Slack credentials when available
5. ⏳ Add real Discord credentials when available
6. ⏳ Connect to real AI module when available

## Support

- Documentation: See `IMPLEMENTATION-STATUS.md` for detailed status
- Issues: Check docker logs first
- Configuration: All settings in `.env`
- Mock Data: Generated by `src/publishing/ai/mock_data_generator.py`

## Summary

✅ **Database**: PostgreSQL for persistent storage  
✅ **Cache**: Redis for performance and real-time features  
✅ **External APIs**: Placeholder mode (ready for real credentials)  
✅ **Mock Data**: Comprehensive AI module mock data  
✅ **Environment**: All configuration in `.env` (gitignored)  

The system is ready for testing and integration!


