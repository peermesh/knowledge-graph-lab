**Non-canonical during concept phase — authoritative conceptual PRDs live in .dev/peermesh-canvases/**

# Backend Module PRD - MVP Version

## Module Owner: Developer 1

## Executive Summary
Build a Python/FastAPI backend that fetches content from RSS feeds, stores it in SQLite, and provides REST APIs for other modules. Total time: 100 hours.

## Goals (MVP)
1. Fetch content from 5 RSS feeds
2. Store content in SQLite database
3. Provide 5 REST API endpoints
4. Run in Docker container
5. Work with mock AI responses

## User Stories

### Phase 1 (Weeks 1-6): Core Features
- As an admin, I can add RSS feed URLs to monitor
- As an admin, I can see a list of all sources
- As the system, I fetch RSS feeds every hour
- As the AI module, I can retrieve content for processing
- As the frontend, I can query entities via API

### Phase 2 (Weeks 7-10): Enhancements
- Add pagination to API responses
- Add basic search functionality
- Improve error handling
- Add logging

## Technical Requirements

### Stack
- Python 3.11
- FastAPI
- SQLite (SQLAlchemy ORM)
- Docker
- schedule (for periodic tasks)

### API Endpoints (Minimal)
```python
# 1. Add a source
POST /api/sources
{"url": "https://example.com/feed.rss", "type": "rss"}

# 2. List sources
GET /api/sources

# 3. Get latest content
GET /api/content?limit=10

# 4. Get entities (returns mock data initially)
GET /api/entities

# 5. Dashboard stats
GET /api/dashboard
```

### Database Schema
```sql
CREATE TABLE sources (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL,
    type TEXT DEFAULT 'rss',
    active BOOLEAN DEFAULT true,
    last_checked TIMESTAMP
);

CREATE TABLE content (
    id INTEGER PRIMARY KEY,
    source_id INTEGER,
    title TEXT,
    text TEXT,
    url TEXT,
    fetched_at TIMESTAMP,
    FOREIGN KEY(source_id) REFERENCES sources(id)
);

CREATE TABLE entities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    description TEXT,
    created_at TIMESTAMP
);
```

## Implementation Plan

### Week 1-2: Setup
- [ ] Create Docker container
- [ ] Setup FastAPI project
- [ ] Create SQLite database
- [ ] Implement basic health check endpoint

### Week 3-4: Core Features
- [ ] Implement source management (add/list)
- [ ] Add RSS feed fetcher
- [ ] Setup hourly fetch schedule
- [ ] Create content storage

### Week 5-6: APIs and Integration
- [ ] Implement all 5 API endpoints
- [ ] Add mock entity data
- [ ] Test with Postman
- [ ] Write basic documentation

### Week 7-8: Enhancement
- [ ] Add pagination
- [ ] Implement basic search
- [ ] Improve error handling
- [ ] Add logging

### Week 9-10: Integration
- [ ] Test with other modules
- [ ] Fix integration issues
- [ ] Performance improvements

### Week 11-12: Demo Prep
- [ ] End-to-end testing
- [ ] Bug fixes
- [ ] Demo preparation

## Success Criteria
- [ ] Fetches from 5 RSS feeds
- [ ] Stores 100+ content items
- [ ] All 5 APIs return data
- [ ] Runs with `docker run`
- [ ] No crashes in 1 hour

## Dependencies
- AI Module: Will consume content via API
- Frontend: Will display data via API
- Publisher: Will query for digest content

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| RSS parsing issues | Use well-tested feedparser library |
| Database performance | Start with SQLite, optimize later |
| API complexity | Keep it simple, 5 endpoints only |
| Time overrun | Focus on core features first |

## Resources Provided
1. Dockerfile template
2. FastAPI starter code
3. SQLite schema
4. Sample RSS feeds for testing
5. Postman collection

## Example Code Structure
```
backend/
├── Dockerfile
├── requirements.txt
├── app/
│   ├── main.py          # FastAPI app
│   ├── database.py      # SQLite setup
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── routers/
│   │   ├── sources.py   # Source endpoints
│   │   ├── content.py   # Content endpoints
│   │   └── dashboard.py # Dashboard endpoint
│   └── tasks/
│       └── fetcher.py   # RSS fetcher
└── tests/
    └── test_api.py      # Basic tests
```

## Getting Started
```bash
# Clone repo
git clone <repo>
cd modules/backend

# Build Docker
docker build -t backend .

# Run
docker run -p 8000:8000 backend

# Test
curl http://localhost:8000/api/dashboard
```

## Questions to Resolve
1. How often to fetch RSS feeds? (Default: hourly)
2. How many items to store per feed? (Default: 100)
3. How to handle duplicate content? (Default: URL-based)

## Notes
- Keep it simple - this is an MVP
- Mock the AI integration for now
- Focus on getting something working
- Ask for help if blocked > 30 minutes