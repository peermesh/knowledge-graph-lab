# Backend Module - Requirements

**Date:** 2025-10-09
**Distilled from:** PRD.md, Backend-Architecture-Spec.md, BASIC-RESEARCH.md, fall-2025-backend-architecture-phase-1-review.md

---

## Functional Requirements

### Core Capabilities (MVP - Must Have)

#### FR-1: RSS Feed Management
**Requirement:** System must fetch content from RSS feeds automatically
- Add RSS feed URLs (admin function)
- List all configured sources
- Fetch feeds on schedule (hourly)
- Store fetched content in database
- Handle RSS parsing errors gracefully

**Source:** PRD.md lines 20-23, Backend-Architecture-Spec.md lines 49-54

---

#### FR-2: Content Storage
**Requirement:** System must store and retrieve content
- Store sources (URL, type, status, last_checked)
- Store content (title, text, URL, fetched_at, source_id)
- Store entities (mock data for MVP)
- Query content by various filters
- Support pagination

**Source:** PRD.md lines 60-87 (database schema), lines 26-30 (user stories)

---

#### FR-3: REST API Endpoints
**Requirement:** Provide 5 REST API endpoints for module integration
1. `POST /api/sources` - Add a source
2. `GET /api/sources` - List sources
3. `GET /api/content?limit=10` - Get latest content
4. `GET /api/entities` - Get entities (mock data initially)
5. `GET /api/dashboard` - Dashboard stats

**Source:** PRD.md lines 41-58

---

#### FR-4: Scheduled Tasks
**Requirement:** Execute periodic background jobs
- Fetch RSS feeds every hour
- Update last_checked timestamps
- Handle failures with retry logic
- Log fetch results

**Source:** Backend-Architecture-Spec.md lines 50-53, PRD.md line 22

---

#### FR-5: Docker Deployment
**Requirement:** Run as containerized service
- Single `docker run` command to start
- Docker Compose for local development
- Environment variable configuration
- Health check endpoint
- No manual setup required

**Source:** PRD.md lines 14, 92-95, 173-186

---

### User Interactions (Module Interfaces)

#### UI-1: AI Module Can Retrieve Content
**As the AI module, I can:**
- Query content via REST API
- Receive JSON responses
- Filter by date, source, type
- Get paginated results

**Acceptance:** AI module successfully retrieves 100 content items for processing

**Source:** PRD.md line 23, Backend-Architecture-Spec.md lines 86-95

---

#### UI-2: Frontend Can Display Data
**As the frontend module, I can:**
- List all sources
- Display latest content
- Show dashboard statistics
- Query entities

**Acceptance:** Frontend displays data from all 5 API endpoints

**Source:** PRD.md line 24, Backend-Architecture-Spec.md lines 74-85

---

#### UI-3: Admin Can Manage Sources
**As an admin, I can:**
- Add new RSS feed URLs
- View list of configured sources
- See fetch status and timestamps

**Acceptance:** Admin successfully adds 5 RSS feeds and sees them fetching

**Source:** PRD.md lines 20-21

---

## Non-Functional Requirements

### Performance

#### NFR-1: API Response Time
**Requirement:** API endpoints respond within acceptable time
- Dashboard: < 500ms
- Content list: < 1 second
- Source operations: < 200ms

**Rationale:** Good developer experience for module integration

**Source:** Inferred from PRD success criteria (lines 125-130), vision.md system metrics (line 116)

**Status:** ⚠️ **GAP** - No specific benchmarks defined in PR research

---

#### NFR-2: Fetch Performance
**Requirement:** RSS fetching completes efficiently
- Process 5 feeds within 5 minutes
- Parallel fetching where possible
- Timeout handling for slow feeds

**Source:** PRD.md (hourly schedule implies reasonable completion time)

---

### Scale (MVP Targets)

#### NFR-3: Data Volume
**Requirement:** Handle expected MVP data load
- 5 RSS feeds
- 100+ content items stored
- 100 items per feed retention
- Hourly fetch rate

**Source:** PRD.md lines 11, 127, 189-190

**Note:** Production scale (10,000+ sources) is OUT OF MVP SCOPE

---

#### NFR-4: Concurrent Users
**Requirement:** Support small team usage
- 5-10 concurrent API requests
- No complex load balancing required
- Single container sufficient

**Source:** Inferred from MVP context - junior developer buildable, 100-hour effort

---

### Security

#### NFR-5: Basic Authentication
**Requirement:** Implement JWT-based auth
- Token-based authentication
- Stateless design
- Refresh token support (desirable)

**Source:** Backend-Architecture-Spec.md lines 38-41, BASIC-RESEARCH.md auth discussion

**Status:** ⚠️ **GAP** - No implementation details in PR research

---

#### NFR-6: Docker Security
**Requirement:** Follow Docker security best practices
- Non-root user execution
- No hardcoded secrets
- Environment variable configuration
- Minimal base images

**Source:** BASIC-RESEARCH.md lines 62-83, PR review security gap (fall-2025-backend-architecture-phase-1-review.md lines 69-70)

**Status:** ⚠️ **GAP** - Intern's Docker POC has security issues

---

#### NFR-7: API Key Management
**Requirement:** Secure external service authentication
- API keys for integrations
- Rotation support
- Encrypted storage

**Source:** Backend-Architecture-Spec.md line 41

**Status:** ⚠️ **GAP** - No design exists

---

### Reliability

#### NFR-8: Error Handling
**Requirement:** Graceful degradation and error recovery
- RSS fetch failures don't crash system
- Invalid data handled gracefully
- Retry logic for transient failures
- Detailed error logging

**Source:** PRD.md lines 108, 113, Backend-Architecture-Spec.md line 52

---

#### NFR-9: Uptime
**Requirement:** System remains operational
- No crashes during 1-hour operation
- Restarts after failures
- Health check endpoint

**Source:** PRD.md line 130

---

#### NFR-10: Data Integrity
**Requirement:** Data remains consistent and valid
- Foreign key constraints
- Duplicate detection (URL-based)
- Transaction support

**Source:** Backend-Architecture-Spec.md line 13, PRD.md line 192

---

## Integration Requirements

### Frontend Module

#### INT-1: REST API Contract
**Requirement:** Provide OpenAPI-documented REST APIs
- OpenAPI/Swagger specification
- JSON response format
- Standard HTTP status codes
- CORS configuration

**Source:** Backend-Architecture-Spec.md lines 36, 76-79

**Status:** ❌ **CRITICAL GAP** - No OpenAPI spec exists (PR review line 36)

---

#### INT-2: Authentication Integration
**Requirement:** JWT tokens for frontend requests
- Token validation
- Authorization headers
- Token expiration handling

**Source:** Backend-Architecture-Spec.md line 78

**Status:** ⚠️ **GAP** - Implementation details missing

---

### AI Module

#### INT-3: Content Access API
**Requirement:** AI module can retrieve content for processing
- Batch content retrieval
- Filter by processing status
- Mark content as processed

**Source:** Backend-Architecture-Spec.md lines 88-90, PRD.md line 23

**Status:** ⚠️ **GAP** - No detailed integration design

---

#### INT-4: Message Queue (Future)
**Requirement:** Async job processing support
- Queue for processing jobs
- Job status tracking
- Result storage

**Source:** Backend-Architecture-Spec.md line 89

**Status:** ⏸️ **DEFERRED** - Mock for MVP, real implementation Phase 2

---

### Publishing Module

#### INT-5: User Preferences API
**Requirement:** Store and retrieve user preferences
- Preference CRUD operations
- Digest content queries

**Source:** Backend-Architecture-Spec.md lines 98-99, PRD.md line 135

**Status:** ⚠️ **GAP** - No schema or API design

---

## Data Requirements

### Database Schema (MVP)

#### DATA-1: Sources Table
```sql
CREATE TABLE sources (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL,
    type TEXT DEFAULT 'rss',
    active BOOLEAN DEFAULT true,
    last_checked TIMESTAMP
);
```

**Source:** PRD.md lines 62-68

---

#### DATA-2: Content Table
```sql
CREATE TABLE content (
    id INTEGER PRIMARY KEY,
    source_id INTEGER,
    title TEXT,
    text TEXT,
    url TEXT,
    fetched_at TIMESTAMP,
    FOREIGN KEY(source_id) REFERENCES sources(id)
);
```

**Source:** PRD.md lines 70-78

---

#### DATA-3: Entities Table (Mock)
```sql
CREATE TABLE entities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    description TEXT,
    created_at TIMESTAMP
);
```

**Source:** PRD.md lines 80-86

**Note:** Returns mock data for MVP, real AI-extracted entities in Phase 2

---

### Migration Strategy

#### DATA-4: Database Migrations
**Requirement:** Version-controlled schema changes
- Migration scripts for schema updates
- Rollback capability
- CI/CD integration (production)

**Source:** Backend-Architecture-Spec.md line 12, BASIC-RESEARCH.md lines 130-150

**Status:** ❌ **CRITICAL GAP** - No migration strategy defined (PR review)

---

#### DATA-5: SQLite → PostgreSQL Path
**Requirement:** Plan for production database upgrade
- Schema compatibility design
- Migration script from SQLite to PostgreSQL
- Data export/import process

**Source:** PRD.md (SQLite for MVP), Backend-Architecture-Spec.md (PostgreSQL mentioned for production)

**Status:** ⏸️ **DEFERRED** - Design awareness, implement Phase 2

---

## MVP Scope Definition

### Phase 1: Core Features (Weeks 1-6)

#### Iteration 1: Setup (Weeks 1-2)
- [x] Create Docker container
- [x] Setup FastAPI project
- [x] Create SQLite database
- [x] Implement health check endpoint

**Source:** PRD.md lines 91-95

---

#### Iteration 2: Core Features (Weeks 3-4)
- [ ] Implement source management (add/list)
- [ ] Add RSS feed fetcher
- [ ] Setup hourly fetch schedule
- [ ] Create content storage

**Source:** PRD.md lines 97-101

---

#### Iteration 3: APIs (Weeks 5-6)
- [ ] Implement all 5 API endpoints
- [ ] Add mock entity data
- [ ] Test with Postman
- [ ] Write basic documentation

**Source:** PRD.md lines 103-107

---

### Phase 2: Enhancement (Weeks 7-10)

- [ ] Add pagination to APIs
- [ ] Implement basic search functionality
- [ ] Improve error handling
- [ ] Add comprehensive logging

**Source:** PRD.md lines 26-30, 109-113

**Status:** Enhancement phase, not critical for demo

---

### Phase 3: Integration & Demo (Weeks 11-12)

- [ ] Test with other modules
- [ ] Fix integration issues
- [ ] Performance improvements
- [ ] End-to-end testing
- [ ] Bug fixes
- [ ] Demo preparation

**Source:** PRD.md lines 115-124

---

## Conflicts & Open Questions

### Conflicts Identified

#### CONFLICT-1: Database Choice
**Source A (PRD.md):** SQLite for MVP simplicity
**Source B (Backend-Architecture-Spec.md):** PostgreSQL + Neo4j for production
**Source C (BASIC-RESEARCH.md):** Recommends PostgreSQL + pgvector

**Resolution:** ✅ Use SQLite for MVP (simpler, faster start), design schema compatible with PostgreSQL migration

**Rationale:** PRD's 100-hour constraint requires simplicity. Intern's research validates PostgreSQL for production.

---

#### CONFLICT-2: Real vs Mock AI Integration
**Source A (PRD.md):** "Work with mock AI responses" (line 15)
**Source B (Backend-Architecture-Spec.md):** "Message queue for processing jobs" (line 89)

**Resolution:** ✅ Mock for MVP, design API contract for real integration later

**Rationale:** Reduces complexity, enables parallel development

---

### Open Questions (Flagged for Discovery)

#### QUESTION-1: Fetch Frequency
**Question:** How often to fetch RSS feeds?
**Default:** Hourly (PRD.md line 189)
**Consideration:** Some feeds update more/less frequently
**Needs:** Configuration per-source?

---

#### QUESTION-2: Content Retention
**Question:** How many items to store per feed?
**Default:** 100 (PRD.md line 190)
**Consideration:** Storage limits, query performance
**Needs:** Cleanup strategy?

---

#### QUESTION-3: Duplicate Handling
**Question:** How to handle duplicate content?
**Default:** URL-based deduplication (PRD.md line 192)
**Consideration:** Same content, different URLs?
**Needs:** Content hashing?

---

#### QUESTION-4: Integration Testing Approach
**Question:** How to test module integration without other modules ready?
**Consideration:** Mock other modules? Postman collections?
**Needs:** Integration test strategy

**Source:** PRD.md lines 115-117 mentions integration testing but no approach defined

---

## Requirements Not in MVP (Explicitly Deferred)

### Deferred to Phase 2+

**Database:**
- PostgreSQL with pgvector
- Neo4j graph database
- Complex indexing strategies

**APIs:**
- GraphQL endpoint
- WebSocket real-time updates
- Advanced query filtering

**Authentication:**
- Keycloak/Auth0 integration
- OAuth2 flows
- Advanced RBAC

**Deployment:**
- Kubernetes manifests
- Production monitoring (Prometheus/Grafana)
- Auto-scaling

**Integration:**
- Real AI module connection
- Multi-module orchestration
- Event-driven architecture

**Source:** Backend-Architecture-Spec.md (full production capabilities), Abstraction Scaffold (future vision), PRD.md "Keep it simple - this is an MVP" (line 194)

---

## Critical Gaps from PR Review

**The following were MISSING from intern's Phase 1 research and must be addressed:**

### GAP-1: Integration Architecture
❌ **No documentation** of how Backend connects to AI, Frontend, Publishing modules
- No integration diagram
- No API contract specifics
- No data flow documentation
- No error handling across modules

**Impact:** HIGH - Other modules can't integrate without this

**Source:** fall-2025-backend-architecture-phase-1-review.md lines 73, 179-180

---

### GAP-2: Database Schema Detail
❌ **Basic schema exists but missing:**
- Entity-Relationship Diagram (ERD)
- Index design
- Migration strategy
- Query optimization plan

**Impact:** MEDIUM - Will need this before implementation

**Source:** fall-2025-backend-architecture-phase-1-review.md line 71, 181

---

### GAP-3: Performance Benchmarks
❌ **No performance analysis:**
- No load testing
- No API response time targets
- No database query benchmarks
- No scalability analysis

**Impact:** LOW for MVP, HIGH for production

**Source:** fall-2025-backend-architecture-phase-1-review.md line 182

---

### GAP-4: Security Implementation
❌ **JWT mentioned but no implementation details:**
- Token generation/validation
- Secret management
- Token expiration/refresh
- Docker security hardening

**Impact:** MEDIUM - Security is important even for MVP

**Source:** fall-2025-backend-architecture-phase-1-review.md lines 69-70, 183

---

## Sources Consulted

**Requirements Specifications:**
1. `docs/modules/backend-architecture/PRD.md` - MVP requirements, user stories, API endpoints, database schema
2. `docs/modules/backend-architecture/Backend-Architecture-Spec.md` - Module responsibilities, interfaces, non-functional requirements

**Technical Research:**
3. `00-context-intake/sources/pr-1-backend-research/BASIC-RESEARCH.md` - Docker patterns, database selection, security practices

**Gaps Analysis:**
4. `.dev/team/intern-management/pr-reviews/fall-2025-backend-architecture-phase-1-review.md` - Critical gaps in deliverables

**Vision Context:**
5. `01-distilled/vision-statement.md` - Overall product vision, success metrics
