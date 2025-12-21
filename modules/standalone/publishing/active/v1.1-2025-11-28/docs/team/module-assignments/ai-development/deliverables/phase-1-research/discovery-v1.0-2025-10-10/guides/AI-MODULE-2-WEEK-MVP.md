# AI Module - 2 Week MVP Plan

**Developer:** 1 person

**Timeline:** 10 working days (80 hours)

**Goal:** Self-contained Docker module with working entity extraction

**Deliverable:** Docker container that accepts text and returns entities

---

# What This Is

A **self-contained AI module** that:

- Runs in a single Docker container
- Accepts HTTP requests (text in, entities out)
- Uses real entity extraction (not mocks)
- Works standalone without external dependencies
- Can be tested end-to-end in minutes

**Not included:** Vector databases, graph databases, event buses, publishing, multi-model orchestration, production monitoring

---

# Technical Scope

## In Scope (2 Weeks)

**Core Functionality:**

- FastAPI web server
- Entity extraction endpoint (`POST /extract`)
- Basic entity types: organizations, people, amounts, dates
- Simple confidence scoring (rule-based)
- Docker containerization
- Basic error handling
- Health check endpoint

**Technology Stack:**

- Python 3.11
- FastAPI
- spaCy (local NER - no API costs)
- Docker
- Basic logging (stdout)

**Testing:**

- Manual testing with curl/Postman
- 10-20 test documents
- Verify entity extraction works

## Out of Scope (Not in 2 Weeks)

**Excluded:**

- ❌ Vector databases
- ❌ Graph databases
- ❌ RabbitMQ / event bus
- ❌ Redis caching
- ❌ OpenAI/Claude integration (costs money, adds complexity)
- ❌ Relationship extraction
- ❌ News report generation
- ❌ Multi-model selection
- ❌ Advanced confidence scoring
- ❌ Prometheus/Grafana monitoring
- ❌ Integration with other modules
- ❌ Kubernetes deployment
- ❌ Fine-tuning
- ❌ Embedding generation

**Why excluded:** You have 80 hours. Keep it simple.

---

# Architecture (Simplified)

```
┌─────────────────────────────────────┐
│   Docker Container :8002            │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  FastAPI                     │  │
│  │  - POST /extract             │  │
│  │  - GET /health               │  │
│  └──────────────────────────────┘  │
│              ↓                      │
│  ┌──────────────────────────────┐  │
│  │  Entity Extractor            │  │
│  │  - spaCy NER                 │  │
│  │  - Rule-based patterns       │  │
│  └──────────────────────────────┘  │
│              ↓                      │
│  ┌──────────────────────────────┐  │
│  │  Confidence Calculator       │  │
│  │  - Simple scoring            │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
         ↑                    ↓
    HTTP Request         JSON Response
```

**That's it. No databases. No message queues. Just HTTP in, JSON out.**

---

# API Design

## POST /extract

**Request:**
```json
{
  "text": "YouTube announced a $100M creator fund in January 2024.",
  "options": {
    "min_confidence": 50
  }
}
```

**Response:**
```json
{
  "request_id": "uuid",
  "processing_time_ms": 234,
  "entities": [
    {
      "text": "YouTube",
      "type": "organization",
      "confidence": 92,
      "start": 0,
      "end": 7
    },
    {
      "text": "$100M",
      "type": "money",
      "confidence": 95,
      "start": 21,
      "end": 26
    },
    {
      "text": "January 2024",
      "type": "date",
      "confidence": 98,
      "start": 45,
      "end": 57
    }
  ],
  "stats": {
    "total_entities": 3,
    "by_type": {
      "organization": 1,
      "money": 1,
      "date": 1
    }
  }
}
```

## GET /health

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "model": "en_core_web_sm"
}
```

---

# Technology Decisions (Simplified)

## Decision 1: Python + FastAPI
**Why:** Fast to build, FastAPI auto-generates docs, async support

**Alternative:** Could use Flask, but FastAPI is modern and better

## Decision 2: spaCy Only (No OpenAI)
**Why:**

- No API costs (free)
- Fast inference (<100ms)
- Works offline
- Good enough for MVP (70-80% accuracy)

**Trade-off:** Lower accuracy than GPT-4, but saves money and complexity

## Decision 3: Rule-Based Confidence
**Why:** Simple formula based on entity type and text patterns

**Formula:**
```python
confidence = base_score  # 90 for dates, 80 for orgs, 70 for money
if entity in common_entities:
    confidence += 10
if entity.isupper():  # All caps (acronym)
    confidence -= 10
return min(100, max(0, confidence))
```

## Decision 4: Standalone Docker Container
**Why:**

- No external dependencies
- Easy to test
- Easy to deploy anywhere
- Self-contained

**Trade-off:** Can't integrate with other services yet (but that's not the 2-week goal)

---

# File Structure

```
ai-module/
├── Dockerfile
├── requirements.txt
├── README.md
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── models.py            # Pydantic models
│   ├── extractor.py         # Entity extraction logic
│   └── config.py            # Configuration
├── tests/
│   ├── test_extractor.py
│   └── test_api.py
└── docs/
    └── API.md               # API documentation
```

**Total files:** ~10 Python files, ~500-800 lines of code

---

# 2-Week Timeline

## Week 1: Core Functionality

### Day 1-2: Setup (16 hours)
- [ ] Create project structure
- [ ] Set up FastAPI skeleton
- [ ] Create Dockerfile
- [ ] Install spaCy and download model
- [ ] Test basic "hello world" endpoint
- [ ] Docker build and run works

**Deliverable:** Docker container runs, responds to HTTP requests

### Day 3-4: Entity Extraction (16 hours)
- [ ] Implement entity extraction with spaCy
- [ ] Support: organizations, people, money, dates
- [ ] Add confidence scoring (simple)
- [ ] Create `/extract` endpoint
- [ ] Test with 5 example documents

**Deliverable:** Entity extraction works, returns JSON

### Day 5: Error Handling & Testing (8 hours)
- [ ] Add input validation (Pydantic)
- [ ] Handle malformed requests
- [ ] Add basic logging (stdout)
- [ ] Write 5-10 unit tests
- [ ] Test with curl/Postman

**Deliverable:** Robust error handling, tests pass

## Week 2: Polish & Documentation

### Day 6-7: Confidence & Stats (16 hours)
- [ ] Improve confidence scoring
- [ ] Add entity position tracking (start/end)
- [ ] Add stats (count by type)
- [ ] Add health check endpoint
- [ ] Test with 10 more documents

**Deliverable:** Better output quality, health checks

### Day 8: Docker Optimization (8 hours)
- [ ] Optimize Docker image size
- [ ] Add environment variables
- [ ] Create docker-compose.yml for easy testing
- [ ] Document build/run process

**Deliverable:** Easy Docker deployment

### Day 9: Documentation (8 hours)
- [ ] Write README with setup instructions
- [ ] Document API endpoints (API.md)
- [ ] Create example requests/responses
- [ ] Add troubleshooting section

**Deliverable:** Complete documentation

### Day 10: Testing & Demo (8 hours)
- [ ] End-to-end testing with 20 documents
- [ ] Fix any bugs found
- [ ] Prepare demo
- [ ] Performance test (how many requests/sec?)

**Deliverable:** Working demo, ready to show

---

# Success Criteria

**Must Have:**

- ✅ Docker container builds and runs
- ✅ `/extract` endpoint works
- ✅ Extracts: organizations, people, money, dates
- ✅ Returns confidence scores
- ✅ Processes at least 10 documents/minute
- ✅ Accuracy: 60-70% (acceptable for MVP)
- ✅ Complete documentation

**Nice to Have (if time):**

- ⚠️ Handle multiple languages
- ⚠️ More entity types (locations, events)
- ⚠️ Better confidence scoring
- ⚠️ Batch processing endpoint

**Explicitly NOT Required:**

- ❌ 90%+ accuracy (that's Phase 2+)
- ❌ Integration with other modules
- ❌ Production monitoring
- ❌ Advanced features

---

# Component List (Minimal)

## Required

1. **Python 3.11** - Runtime
2. **FastAPI** - Web framework
3. **spaCy** - Entity extraction
4. **spaCy model** - `en_core_web_sm` (small, fast)
5. **Pydantic** - Request/response validation
6. **uvicorn** - ASGI server
7. **Docker** - Containerization

## Optional (if time permits)

8. **pytest** - Testing (nice to have)
9. **httpx** - Testing client (nice to have)

**Total dependencies:** 7-9 packages

---

# Requirements (Simplified)

## Functional Requirements

### 1. Entity Extraction
**Input:** Text (string, max 10,000 characters)

**Output:** List of entities with type, confidence, position

**Supported Types:**

- `organization` (YouTube, Google, Meta)
- `person` (MrBeast, creators)
- `money` ($100M, €50K)
- `date` (January 2024, 2024-01-15)

**Accuracy Target:** 60-70% (good enough for MVP)

### 2. Confidence Scoring
**Method:** Rule-based

**Score Range:** 0-100

**Factors:**

- Entity type (dates = high, orgs = medium)
- Capitalization (proper nouns = higher)
- Common entity list (YouTube, Google = higher)

### 3. API Response
**Format:** JSON

**Max Response Time:** 2 seconds

**Include:** Entity list, stats, processing time

### 4. Error Handling
**Invalid Input:** Return 400 with error message

**Processing Error:** Return 500 with error details

**Timeout:** Return 504 if processing takes >5 seconds

### 5. Health Check
**Endpoint:** GET /health

**Purpose:** Verify service is running

**Response:** Status, version, model name

## Non-Functional Requirements

### Performance
- **Throughput:** 10+ documents/minute (single instance)
- **Latency:** <2 seconds per document
- **Startup:** <30 seconds (Docker container)

### Reliability
- **Uptime:** Runs continuously without crashes
- **Error Rate:** <5% on valid inputs
- **Recovery:** Restarts automatically if crashes

### Usability
- **Setup Time:** <10 minutes (clone → docker run)
- **Documentation:** Complete README + API docs
- **Examples:** 5+ example requests provided

---

# Constraints

## Timeline
- **Total:** 10 working days
- **Daily:** 8 hours max
- **Buffer:** 1-2 days for unexpected issues

## Scope
- **One developer:** No team coordination
- **No integration:** Standalone module only
- **No production:** MVP/demo quality, not production-ready

## Technology
- **Free only:** No API costs (no OpenAI/Claude)
- **Minimal deps:** Keep dependencies <10 packages
- **Standard tools:** Use well-known libraries

## Quality
- **Accuracy:** 60-70% acceptable
- **Tests:** Nice to have, not critical
- **Monitoring:** Basic logging only

---

# Testing Plan

## Manual Testing (Primary)

**Test Documents (10-20 examples):**

1. "YouTube announced a $100M creator fund."
2. "MrBeast partnered with Google in January 2024."
3. "TikTok launched a €50M program for European creators."
4. (Add 7-17 more examples)

**Test Process:**
```bash
# Build Docker container
docker build -t ai-module .

# Run container
docker run -p 8002:8002 ai-module

# Test extraction
curl -X POST http://localhost:8002/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "YouTube announced a $100M creator fund."}'

# Check health
curl http://localhost:8002/health
```

**Validation:**

- Does it extract YouTube? ✓
- Does it extract $100M? ✓
- Are confidence scores reasonable? ✓
- Response time <2 seconds? ✓

## Automated Testing (If Time)

**Unit Tests (5-10 tests):**
```python
def test_extract_organization():
    result = extractor.extract("YouTube announced...")
    assert any(e['type'] == 'organization' for e in result)

def test_extract_money():
    result = extractor.extract("$100M fund")
    assert any(e['type'] == 'money' for e in result)
```

**API Tests (5-10 tests):**
```python
def test_extract_endpoint():
    response = client.post("/extract", json={"text": "..."})
    assert response.status_code == 200
    assert "entities" in response.json()
```

---

# Deployment

## Local Development

```bash
# Clone repo
git clone <repo>
cd ai-module

# Setup virtual env
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run locally
uvicorn app.main:app --reload --port 8002
```

## Docker Deployment (Recommended)

```bash
# Build
docker build -t ai-module:0.1.0 .

# Run
docker run -p 8002:8002 ai-module:0.1.0

# Test
curl http://localhost:8002/health
```

## Docker Compose (Easy Testing)

```yaml
version: '3.8'
services:
  ai-module:
    build: .
    ports:
      - "8002:8002"
    environment:
      - LOG_LEVEL=info
```

```bash
docker-compose up
```

---

# Risk Mitigation

## Risk 1: spaCy Accuracy Too Low
**Mitigation:** Acceptable for MVP. If <60%, add simple pattern matching for common entities (YouTube, Google, MrBeast)

## Risk 2: Takes Longer Than 2 Weeks
**Mitigation:** Cut scope further:

- Remove tests
- Remove documentation polish
- Simplify confidence scoring
- Reduce entity types to just organizations + money

## Risk 3: Docker Issues
**Mitigation:** Test Docker build early (Day 1-2). If problems, run as local Python app first, containerize later

## Risk 4: Can't Parse Certain Formats
**Mitigation:** Only support plain text input. No HTML/PDF parsing in MVP.

---

# What Happens After 2 Weeks

**You'll Have:**

- Working Docker container
- Basic entity extraction
- Demonstrable MVP
- Foundation for future work

**Next Steps (Post-MVP):**

- Add OpenAI integration for higher accuracy (Phase 2)
- Add relationship extraction
- Integrate with vector database
- Add production monitoring
- Deploy to staging environment

**But not in the initial 2 weeks.**

---

# Quick Start (After Building)

```bash
# 1. Build Docker image
docker build -t ai-module .

# 2. Run container
docker run -p 8002:8002 ai-module

# 3. Test extraction
curl -X POST http://localhost:8002/extract \
  -H "Content-Type: application/json" \
  -d '{
    "text": "YouTube announced a $100M creator fund in January 2024."
  }'

# 4. See results
{
  "entities": [
    {"text": "YouTube", "type": "organization", "confidence": 92},
    {"text": "$100M", "type": "money", "confidence": 95},
    {"text": "January 2024", "type": "date", "confidence": 98}
  ]
}
```

**That's it. Simple, self-contained, working.**

---

# File Reference

This is the realistic plan. The full discovery report (`AI-MODULE-DISCOVERY-REPORT.md`) describes the eventual vision, but is NOT achievable in 2 weeks by one developer.

**Use this document** for the 2-week MVP.

**Reference the full report** for understanding the eventual architecture.
