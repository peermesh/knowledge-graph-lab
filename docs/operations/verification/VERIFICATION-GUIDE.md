# Verification Guide: PostgreSQL & Redis Implementation

This guide shows you how to verify that PostgreSQL and Redis are working correctly and that all placeholder APIs are functioning.

---

## 1. Verify Docker Services

### Check Service Status
```bash
docker-compose ps
```

**Expected Output:**
```
NAME                STATUS              PORTS
postgres            Up (healthy)        0.0.0.0:5432->5432/tcp
redis               Up (healthy)        0.0.0.0:6379->6379/tcp
api                 Up (healthy)        0.0.0.0:8080->8080/tcp
frontend            Up (healthy)        0.0.0.0:3000->80/tcp
```

### Check Service Logs
```bash
# All services
docker-compose logs --tail=50

# Just API
docker-compose logs api --tail=50

# Just PostgreSQL
docker-compose logs postgres --tail=20

# Just Redis
docker-compose logs redis --tail=20
```

---

## 2. Verify PostgreSQL

### Test Database Connection
```bash
docker-compose exec postgres pg_isready -U publishing_user -d publishing_db
```

**Expected Output:**
```
/var/run/postgresql:5432 - accepting connections
```

### Connect to Database
```bash
docker-compose exec postgres psql -U publishing_user -d publishing_db
```

### Check Tables
```sql
-- List all publishing tables
\dt publishing_*

-- Should show:
-- publishing_analytics
-- publishing_channels
-- publishing_publications
-- publishing_subscribers
-- publishing_templates
```

### Check Subscriber Table Structure
```sql
\d publishing_subscribers

-- Should show columns:
-- id, user_id, email, preferred_channels (JSON),
-- topic_interests (JSON), frequency_settings (JSON),
-- personalization_data (JSON), subscription_status,
-- created_at, updated_at
```

### Sample Queries
```sql
-- Count subscribers
SELECT COUNT(*) FROM publishing_subscribers;

-- View sample subscriber
SELECT 
  email, 
  personalization_data->>'name' as name,
  personalization_data->>'frequency' as frequency
FROM publishing_subscribers 
LIMIT 1;

-- Exit
\q
```

---

## 3. Verify Redis

### Test Redis Connection
```bash
docker-compose exec redis redis-cli ping
```

**Expected Output:**
```
PONG
```

### Connect to Redis
```bash
docker-compose exec redis redis-cli
```

### Check Keys
```bash
# List all keys
KEYS *

# Should see keys like:
# subscriber:uuid
# template:uuid
# alert:uuid
# engagement:uuid

# Get a subscriber cache entry
GET subscriber:some-uuid

# Get engagement data
GET engagement:some-publication-id

# Exit
exit
```

---

## 4. Verify API Health

### Health Check Endpoint
```bash
curl http://localhost:8080/health | jq
```

**Expected Output:**
```json
{
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "timestamp": "2025-10-28T12:00:00Z",
    "services": {
      "database": {
        "status": "connected",
        "database": "publishing_db"
      },
      "redis": {
        "status": "connected",
        "host": "redis"
      }
    }
  },
  "meta": {
    "timestamp": "2025-10-28T12:00:00Z",
    "request_id": "..."
  },
  "errors": []
}
```

### API Documentation
```bash
# OpenAPI docs
open http://localhost:8080/api/v1/docs

# Or with curl
curl http://localhost:8080/api/v1/openapi.json | jq
```

---

## 5. Verify Mock Data Loading

### Load Mock Data
```bash
python scripts/init_mock_data.py
```

**Expected Output:**
```
✅ Mock data loaded successfully!
  • Subscribers: 10
  • Content items: 20
  • Sample batch: batch-uuid-here

Sample subscriber emails:
  - alice.smith@example.com (daily)
  - bob.johnson@test.com (weekly)
  - charlie.williams@demo.org (daily)
  - diana.brown@sample.net (bi-weekly)
  - ethan.jones@mock.io (monthly)
```

### Verify Mock Subscribers in Database
```bash
docker-compose exec postgres psql -U publishing_user -d publishing_db -c "
SELECT 
  email,
  personalization_data->>'name' as name,
  personalization_data->>'dispatch_type' as dispatch_type,
  personalization_data->>'frequency' as frequency
FROM publishing_subscribers 
LIMIT 5;
"
```

**Expected Output:**
```
          email          |      name       | dispatch_type | frequency
-------------------------+-----------------+---------------+-----------
 alice.smith@example.com | Alice Smith     | email         | daily
 bob.johnson@test.com    | Bob Johnson     | email         | weekly
 ...
```

### Verify Mock Data Structure
```bash
python -c "
from src.publishing.ai.mock_data_generator import create_mock_user
import json

user = create_mock_user()
print('User Name:', user['name'])
print('Email:', user['email'])
print('Dispatch Type:', user['dispatch_type'])
print('Frequency:', user['frequency'])
print('AI Prompts:', user['ai_metadata']['prompts'])
print('Topics:', user['ai_metadata']['refined_requests']['topics'])
"
```

---

## 6. Verify API Endpoints

### List Subscribers
```bash
curl http://localhost:8080/api/v1/subscribers | jq .
```

**Expected Output:**
```json
{
  "data": {
    "subscribers": [
      {
        "id": "uuid",
        "email": "alice.smith@example.com",
        "preferred_channels": ["email"],
        "subscription_status": "active",
        ...
      }
    ]
  },
  "meta": {
    "timestamp": "2025-10-28T12:00:00Z"
  },
  "errors": []
}
```

### Create New Subscriber
```bash
curl -X POST http://localhost:8080/api/v1/subscribers \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
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

**Expected Output:**
```json
{
  "data": {
    "id": "new-uuid",
    "email": "newuser@example.com",
    ...
  },
  "meta": {
    "timestamp": "2025-10-28T12:00:00Z"
  },
  "errors": []
}
```

### List Channels
```bash
curl http://localhost:8080/api/v1/channels | jq
```

### Create Channel
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

---

## 7. Verify External Service Placeholder Mode

### Check Placeholder Detection
```bash
docker-compose logs api | grep "Placeholder mode" | tail -5
```

**Expected Output:**
```
Email service running in placeholder mode
Slack service running in placeholder mode
Discord service running in placeholder mode
```

### Test Email Service (Simulated)
Create a publication to trigger email:
```bash
curl -X POST http://localhost:8080/api/v1/publications \
  -H "Content-Type: application/json" \
  -d '{
    "content_ids": ["content-1"],
    "channels": ["channel-id"],
    "publication_type": "newsletter"
  }' | jq
```

Check logs for placeholder email:
```bash
docker-compose logs api | grep "PLACEHOLDER EMAIL"
```

**Expected Output:**
```
📧 PLACEHOLDER EMAIL (not actually sent)
To: [user@example.com]
Subject: Newsletter
Note: Email not sent - running in placeholder mode. Configure AWS SES credentials in .env
```

### Test Slack Service (Simulated)
```bash
# This would be triggered by creating a publication with Slack channel
# Check logs:
docker-compose logs api | grep "PLACEHOLDER SLACK"
```

**Expected Output:**
```
💬 PLACEHOLDER SLACK MESSAGE (not actually sent)
Channel: #general
Message: ...
Note: Message not sent - running in placeholder mode. Configure Slack credentials in .env
```

### Test Discord Service (Simulated)
```bash
# This would be triggered by creating a publication with Discord channel
# Check logs:
docker-compose logs api | grep "PLACEHOLDER DISCORD"
```

**Expected Output:**
```
🎮 PLACEHOLDER DISCORD MESSAGE (not actually sent)
Channel: 123456
Content: ...
Note: Message not sent - running in placeholder mode. Configure Discord credentials in .env
```

---

## 8. Verify Data Persistence

### Test Data Survives Restart
```bash
# 1. Create a subscriber
curl -X POST http://localhost:8080/api/v1/subscribers \
  -H "Content-Type: application/json" \
  -d '{"email": "persistence-test@example.com", "preferred_channels": ["email"]}'

# 2. Note the subscriber ID from response

# 3. Restart services
docker-compose restart

# 4. Wait for services to come up
sleep 10

# 5. Check subscriber still exists
curl http://localhost:8080/api/v1/subscribers | jq '.data.subscribers[] | select(.email=="persistence-test@example.com")'
```

**Expected:** Subscriber still exists after restart

---

## 9. Verify Caching (Redis)

### Check Template Caching
```bash
# 1. Create a template
curl -X POST http://localhost:8080/api/v1/templates \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Template",
    "template_type": "email",
    "content_structure": {"body": "Hello {{name}}"}
  }' | jq

# 2. Note the template ID

# 3. Check Redis for cached template
docker-compose exec redis redis-cli GET "template:TEMPLATE_ID"
```

**Expected:** Template data in JSON format

### Check Engagement Tracking
```bash
# Simulate engagement event (this would normally come from email opens/clicks)
# Check Redis:
docker-compose exec redis redis-cli KEYS "engagement:*"
```

---

## 10. Verify AI Mock Data Structure

### Generate and Inspect Mock User
```bash
python -c "
from src.publishing.ai.mock_data_generator import create_mock_user
import json

user = create_mock_user()

print('=== User Profile ===')
print('Name:', user['name'])
print('Email:', user['email'])
print()

print('=== Dispatch Configuration ===')
print('Type:', user['dispatch_type'])
print('Frequency:', user['frequency'])
print('Time:', user['frequency_settings']['time_of_day'])
print('Timezone:', user['frequency_settings']['timezone'])
print()

print('=== AI Metadata ===')
print('Prompts:')
for prompt in user['ai_metadata']['prompts']:
    print(' -', prompt)
print()

print('Topics:', user['ai_metadata']['refined_requests']['topics'])
print('Keywords:', user['ai_metadata']['refined_requests']['keywords'][:3])
print()

print('=== Personalization ===')
print('Style:', user['ai_metadata']['personalization']['style'])
print('Tone:', user['ai_metadata']['personalization']['tone'])
print('Summarization:', user['ai_metadata']['personalization']['summarization'])
"
```

### Generate Mock Dispatch Batch
```bash
python -c "
from src.publishing.ai.mock_data_generator import create_mock_dispatch_batch
import json

batch = create_mock_dispatch_batch(user_count=2, content_per_user=2)

print('=== Dispatch Batch ===')
print('Batch ID:', batch['batch_id'])
print('Recipients:', batch['total_recipients'])
print()

for i, recipient in enumerate(batch['recipients'], 1):
    print(f'Recipient {i}:')
    print('  Name:', recipient['user']['name'])
    print('  Email:', recipient['user']['email'])
    print('  Frequency:', recipient['user']['frequency'])
    print('  Content Items:', len(recipient['content']))
    print('  Topics:', recipient['user']['ai_metadata']['refined_requests']['topics'][:2])
    print()
"
```

---

## 11. Common Verification Checks

### Check All Services Are Using PostgreSQL (Not In-Memory)
```bash
# Check API logs for database initialization
docker-compose logs api | grep "Database initialized"

# Should see:
# Database initialized successfully
# NOT: DEBUG mode: Skipping database initialization
```

### Check All Services Are Using Redis
```bash
# Check Redis connection logs
docker-compose logs api | grep "Redis"

# Should see:
# Redis connection established successfully
```

### Verify No In-Memory Stores Being Used
```bash
# Search for IN_MEMORY usage in logs (should be none)
docker-compose logs api | grep "IN_MEMORY" || echo "✅ No in-memory stores detected"
```

---

## 12. Performance Verification

### Test Database Connection Pool
```bash
# Make multiple concurrent requests
for i in {1..10}; do
  curl http://localhost:8080/api/v1/subscribers &
done
wait

# Check connection pool in PostgreSQL
docker-compose exec postgres psql -U publishing_user -d publishing_db -c "
SELECT 
  count(*) as active_connections 
FROM pg_stat_activity 
WHERE datname = 'publishing_db';
"
```

### Test Redis Performance
```bash
docker-compose exec redis redis-cli --latency

# Press Ctrl+C after a few seconds
# Should show sub-millisecond latency
```

---

## 13. Troubleshooting Verification

### If Health Check Fails
```bash
# Check database connection
docker-compose exec postgres pg_isready

# Check Redis connection
docker-compose exec redis redis-cli ping

# Check API logs
docker-compose logs api --tail=50

# Restart services
docker-compose restart
```

### If Mock Data Loading Fails
```bash
# Check database is accessible
docker-compose exec postgres psql -U publishing_user -d publishing_db -c "SELECT 1"

# Check Redis is accessible
docker-compose exec redis redis-cli ping

# Try loading with verbose output
python scripts/init_mock_data.py 2>&1 | tee mock_data_load.log
```

### If Placeholder Mode Not Activating
```bash
# Check .env file
cat .env | grep -E "(AWS|SLACK|DISCORD)"

# Should see placeholder values like:
# AWS_ACCESS_KEY_ID=placeholder-aws-access-key
# SLACK_BOT_TOKEN=placeholder-slack-bot-token
# DISCORD_BOT_TOKEN=placeholder-discord-bot-token
```

---

## ✅ Verification Checklist

Run through this checklist to verify everything is working:

- [ ] PostgreSQL service is running and healthy
- [ ] Redis service is running and healthy
- [ ] API service is running and healthy
- [ ] Database tables are created (`publishing_*`)
- [ ] Can connect to PostgreSQL
- [ ] Can connect to Redis
- [ ] API health endpoint returns "healthy"
- [ ] Mock data script runs successfully
- [ ] Subscribers are in database (not in-memory)
- [ ] Subscribers are cached in Redis
- [ ] API endpoints return data from PostgreSQL
- [ ] Data persists across service restarts
- [ ] Placeholder mode detected for AWS SES
- [ ] Placeholder mode detected for Slack
- [ ] Placeholder mode detected for Discord
- [ ] Mock users have proper structure (name, email, dispatch_type, frequency)
- [ ] Mock users have AI metadata (prompts, refined_requests)
- [ ] No IN_MEMORY stores being used

---

## 📊 Success Criteria

Your implementation is verified if:

1. ✅ All services start without errors
2. ✅ PostgreSQL contains data in `publishing_*` tables
3. ✅ Redis contains cached data
4. ✅ API responds to requests with database data
5. ✅ Data persists across restarts
6. ✅ Placeholder mode logs for external services
7. ✅ Mock data loads successfully
8. ✅ No in-memory stores in use

---

## 🎉 You're All Set!

If all verifications pass, your PostgreSQL and Redis integration is complete and working correctly!

Next steps:
- Add real AWS SES credentials when available
- Add real Slack credentials when available
- Add real Discord credentials when available
- Connect to real AI module when available


