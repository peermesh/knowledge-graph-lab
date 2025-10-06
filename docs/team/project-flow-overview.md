# Knowledge Graph Lab: Complete Project Flow

**Version**: 1.0
**Date**: October 6, 2025
**Status**: Source of Truth for Project Process

## Document Purpose

This document maps the complete journey from project kickoff to production deployment. It serves as the single source of truth for understanding:

- What we're building and why
- How we're getting from concept to production
- What happens at each phase
- How modules work independently then integrate
- Team coordination and deliverables

## Table of Contents

1. [Project Vision & Context](#project-vision--context)
2. [What We're Building](#what-were-building)
3. [Team Structure](#team-structure)
4. [The 5-Phase Development Journey](#the-5-phase-development-journey)
5. [Phase-by-Phase Breakdown](#phase-by-phase-breakdown)
6. [Module Independence → Integration](#module-independence--integration)
7. [Key Principles & Constraints](#key-principles--constraints)
8. [Success Criteria](#success-criteria)
9. [Timeline & Coordination](#timeline--coordination)

---

## Project Vision & Context

### The Problem

The creator economy is drowning in information chaos:

- Creators spend 10+ hours/week searching for opportunities across fragmented sources
- Grant deadlines are missed because information is scattered
- Partnership opportunities expire buried in noise
- No central intelligence layer to filter what matters

**Example**: A gaming creator manually checks dozens of brand websites, newsletters, and platform blogs weekly—only to miss relevant funding deadlines because the signal is lost in the noise.

### The Solution

**Knowledge Graph Lab** is an AI-powered research platform that transforms scattered information into actionable intelligence by:

1. **Discovering**: Monitoring hundreds of sources (RSS, APIs, websites) to find grants, partnerships, and opportunities
2. **Understanding**: Building knowledge graphs that map entities (YouTube, MrBeast, Google) and relationships (Google owns YouTube)
3. **Reasoning**: Identifying patterns like seasonal grant cycles and collaboration opportunities
4. **Delivering**: Distributing personalized insights via web, email, API, and webhooks

### Why Now

Three converging factors make this possible:

1. **LLMs** can extract structured data from unstructured text automatically
2. **Graph databases** can handle millions of relationships at production scale
3. **Compute costs** have dropped, making continuous automated research viable

---

## What We're Building

### Four Integrated Modules

The system consists of four modules that work together: Backend Architecture, Frontend Design, AI Development, and Publishing Tools. Each module runs independently in Docker and communicates through well-defined APIs.

#### 1. Backend Architecture
**Core Job**: Fetch content, store data, provide APIs

**Responsibilities**:

- Docker containerization and infrastructure
- Database architecture (PostgreSQL, Redis, Vector DB)
- REST API design and implementation
- Authentication and authorization
- Data pipeline for content ingestion
- System monitoring and logging

**Key Deliverables**:

- REST API with core endpoints
- Database schemas and migrations
- Docker container with one-command startup
- API documentation (Swagger/OpenAPI)

#### 2. Frontend Design

**Core Job**: Admin dashboard + user signup interface

**Responsibilities**:

- React UI with component architecture
- D3.js graph visualizations
- Redux state management
- Real-time updates (WebSocket in Phase 2+)
- Authentication UI flow
- Responsive design

**Key Deliverables**:

- 2+ page React application (Dashboard + Signup)
- Graph visualization components
- Connects to Backend API
- Docker container with hot-reload

#### 3. AI Development

**Core Job**: Extract entities from text, build knowledge graphs

**Responsibilities**:

- LLM integration (OpenAI, Anthropic, or open source)
- Entity extraction from unstructured text
- Knowledge graph construction
- Vector embeddings for similarity search
- RAG (Retrieval Augmented Generation)
- Cost optimization

**Key Deliverables**:

- REST API with extraction endpoints
- Mock responses for Phase 1
- Real AI integration for Phase 2+
- Vector database integration

#### 4. Publishing Tools

**Core Job**: Manage subscribers and send personalized digests

**Responsibilities**:

- Multi-channel distribution (email, API, webhooks)
- Subscriber management
- Email template system
- Content personalization engine
- Distribution scheduling
- Analytics tracking

**Key Deliverables**:

- REST API with subscriber/distribution endpoints
- Email templates
- Local SMTP for testing
- Distribution queue system

---

## Team Structure

### Module Ownership

| Module | Owner | Focus Area |
|--------|-------|------------|
| **Backend Architecture** | Ivan G. ([@gorodinskiia](https://github.com/gorodinskiia)) | Database & API design |
| **Frontend Design** | Dante S. ([@D-JSimpson](https://github.com/D-JSimpson)) | UI & data visualization |
| **AI Development** | Haesoe J. ([@haejeg](https://github.com/haejeg)) | ML systems & knowledge graphs |
| **Publishing Tools** | Ben S. ([@bschreiber8](https://github.com/bschreiber8)) | Content delivery systems |
| **Project Lead** | Grig B. ([@grigb](https://github.com/grigb)) | Direction & coordination |

### Coordination Points

**Critical Integration Points** (documented in Integration Charter):

- **Frontend ↔ Backend**: API contracts, authentication flow, real-time updates
- **Backend ↔ AI**: Vector database strategy, data pipeline integration, async processing
- **Backend ↔ Publishing**: User data management, content storage, analytics
- **All Modules**: Shared data formats, error handling, Docker networking

---

## The 5-Phase Development Journey

### High-Level Flow

```
PHASE 1: Research (Weeks 1-X)
    ↓ Research briefs with tech recommendations
PHASE 2: Planning (Weeks X-Y)
    ↓ PRDs with complete specifications (SpecKit-ready)
PHASE 3: MVP Development (Weeks Y-Z)
    ↓ Working standalone modules in Docker
PHASE 4: Enhancement (Weeks Z-W)
    ↓ Polished features, demo-ready presentation
DEMO DAY: Show & Tell
    ↓ Each module presented independently
PHASE 5: Integration (Weeks W+)
    ↓ Unified production system
PRODUCTION: Live deployment
```

### Phase Overview

| Phase | Duration | Key Deliverable | Gate Requirement |
|-------|----------|-----------------|------------------|
| **1: Research** | Flexible | 5-page research brief | Technology recommendations with rationale |
| **2: Planning** | Flexible | 10-15 page PRD | SpecKit validation passes |
| **3: MVP** | ~6 weeks | Working Docker module | Module runs independently, core features work |
| **4: Enhancement** | ~4 weeks | Polished module | Demo-ready presentation |
| **5: Integration** | ~2 weeks | Unified system | All modules connected, end-to-end tests pass |

---

## Phase-by-Phase Breakdown

### Phase 1: Research & Discovery

**Objective**: Research and select technologies that meet project requirements

**What You'll Do**:

1. Research specific technologies for your module
   - Backend: Docker strategy, database selection, API framework, auth approach
   - Frontend: React tooling, graph viz libraries, state management
   - AI: LLM integration, vector DB, knowledge graph approach, cost optimization
   - Publishing: Email providers, distribution tools, analytics platforms
2. Understand the creator economy problem your module solves
3. Explore 3 solution approaches with pros/cons
4. Create 5-page research brief with recommendations

**Deliverables**:

- **Research Brief** (5 pages)
  - Technology comparison matrix
  - Selected approach with rationale
  - Risk assessment
  - Implementation plan
- **Key Decisions Document**
  - Database choices (if applicable)
  - Framework selection
  - Library dependencies
  - Integration approach
- **Questions & Concerns**
  - Technical blockers
  - Integration uncertainties
  - Resource needs
  - Timeline risks

**Success Criteria**:

✅ Research brief contains exactly 3 technology options per decision with detailed comparison table

✅ Each recommendation includes specific quantified pros/cons (performance metrics, cost analysis with numbers)

✅ All choices backed by verifiable evidence (benchmarks, case studies, official docs)

**Team Sync**: Present research findings at Phase 2 kickoff

**Submission**:

- Save to: `docs/team/module-assignments/[your-module]/deliverables/phase-1-research/`
- Filename: `phase-1-research-brief.md`
- Submit via PR following [Git Workflow](git-workflow.md)

---

### Phase 2: Planning & Design (PRD Creation)

**Objective**: Create comprehensive Product Requirements Documents that enable automated code generation

**What You'll Do**:

1. Create 10-15 page PRD for your module
2. Define module scope and REST API endpoints with example requests/responses
3. Make specific technology decisions based on Phase 1 research
4. Document dependencies and integration points
5. Participate in planning discussions and get feedback
6. **CRITICAL**: Coordinate with Backend owner to validate API contracts

**Deliverables**:

#### 1. Product Requirements Document (10-15 pages)

**MUST follow SpecKit-compatible format with these sections**:

1. **System Overview** - Purpose, users, integration points
2. **Functional Requirements** - What each feature does
3. **Data Models** - Entities with specific field types
4. **API Specifications** - Endpoints with request/response schemas
5. **UI Specifications** - User interface requirements (Frontend only)
6. **Integration Requirements** - How modules connect
7. **Acceptance Criteria** - Testable success conditions
8. **Technical Constraints** - Performance, security, scalability

**Key Requirements for SpecKit Compatibility**:

- Be specific about types: `string(255)` not just "text"
- Include complete JSON schemas
- Define all states: loading, error, success, empty
- Mark uncertainties: `[NEEDS CLARIFICATION: question]`
- No placeholder text or TODOs

#### 2. Integration Contracts

Document how your module connects with others:

- **Shared data formats** - Exact schemas
- **API endpoints** - What you provide/consume
- **Events** - Published/subscribed events
- **Dependencies** - What you need from other modules

#### 3. Technical Decisions

Document key choices from Phase 1 research:

- **Technology stack** - Languages, frameworks, libraries
- **Database design** - Schema, indexes, relationships
- **Architecture patterns** - Design patterns to follow
- **Security approach** - Auth, authorization, encryption

**Integration Outreach Requirement**:

- Schedule working session with Backend owner
- Validate data shapes, endpoints, error handling
- Document decisions and open questions in PRD
- Obtain explicit sign-off from Backend owner

**Success Criteria**:

✅ **PRD is SpecKit-ready**: All required sections present, types and schemas specified

✅ **Integration defined**: API contracts documented, shared data formats agreed

✅ **Decisions documented**: Technology choices explained, trade-offs acknowledged

✅ **Quality verified**: Peer reviewed, no missing information, uncertainties clearly marked

**SpecKit Validation Checklist**:

- [ ] All 8 required sections complete
- [ ] Data types specified for every field
- [ ] API schemas include examples
- [ ] Acceptance criteria are testable
- [ ] Integration points documented
- [ ] No placeholder text or TODOs

**Team Sync**: Share PRD and get feedback at Phase 3 kickoff

**Submission**:

- Save to: `docs/team/module-assignments/[your-module]/deliverables/phase-2-planning/`
- Filename: `PRD.md`
- Submit via PR following [Git Workflow](git-workflow.md)

**Example**: See `docs/team/module-assignments/publishing-tools/deliverables/phase-2-planning/examples/PRD-example.md`

---

### Phase 3: MVP Development

**Objective**: Build minimal viable product as standalone module in Docker

**What You'll Do**:

1. Set up development environment and configuration
2. Create Docker container for your standalone module
3. Install development tools
4. Run basic tests to verify setup
5. Build minimal viable product
6. Implement core functionality
7. Ensure module runs independently in Docker

**Important**: Your module must work **without** dependencies on other team members' code. Use mock data and mock APIs for integration points.

**Deliverables**:

- **Working Standalone Module in Docker**
  - Docker container starts without errors
  - All core features implemented
  - Module runs independently
  - Documentation/README included

**Success Criteria**:

✅ Docker container starts without errors in under 30 seconds on standard hardware

✅ All CREATE/READ/UPDATE/DELETE operations complete in under 500ms for typical payloads

✅ Module successfully processes test data with 99% uptime over 24-hour test period

**Module-Specific Targets**:

- **Backend**: Module ingests data from exactly 10 different RSS feeds
- **Frontend**: Dashboard displays mock data with graph visualization
- **AI**: Entity extraction returns structured results (mock or real)
- **Publishing**: Email digest sends to test subscriber list

**Team Sync**: Demo MVP at Phase 4 kickoff

**Submission**:

- Save to: `docs/team/module-assignments/[your-module]/deliverables/phase-3-mvp/`
- Include: Code, Docker files, README, test results
- Submit via PR following [Git Workflow](git-workflow.md)

---

### Phase 4: Enhancement

**Objective**: Add feature improvements and polish for demo presentation

**What You'll Do**:

1. Add feature improvements to standalone module
2. Optimize performance
3. Polish and refine user experience
4. Extend functionality beyond MVP
5. Prepare demo presentation

**Deliverables**:

- **Enhanced Standalone Module**
  - Performance improvements implemented
  - Polished user experience
  - Extended features beyond MVP
  - Updated documentation
  - Demo-ready presentation

**Team Sync**: Full presentation at Demo Day

**Submission**:

- Save to: `docs/team/module-assignments/[your-module]/deliverables/phase-4-enhancement/`
- Include: Enhanced code, performance metrics, demo script
- Submit via PR following [Git Workflow](git-workflow.md)

---

### Demo Day

**Timing**: When Phase 4 completes

**Format**:

- Zoom call with screen sharing
- Each person presents their standalone module
- Show MVP with enhancements
- Q&A about each module
- Review what everyone built independently

**Presentation Structure** (10-15 minutes per module):

1. Module purpose and role in system
2. Live demo of core features
3. Show key technical decisions
4. Discuss challenges and solutions
5. Q&A

---

### Phase 5: Integration

**Objective**: Merge individual modules into unified production system

**What You'll Do**:

1. Plan integration based on demo learnings
2. Merge individual modules together
3. Implement cross-module integration
4. Create unified API or integration layer
5. Conduct end-to-end testing
6. Assemble final system

**Integration Flow**:
```
1. User adds RSS feed via Frontend
   ↓
2. Backend fetches content periodically
   ↓
3. Backend calls AI module to extract entities
   ↓
4. Frontend displays entities on dashboard
   ↓
5. User signs up for digest via Frontend
   ↓
6. Publisher sends daily email with top entities
```

**Deliverables**:

- **Integration-Ready Modules**
  - Documented API endpoints
  - Integration tests passing
  - Docker Compose configuration
  - Unified production system

**Success Criteria**:

✅ Load test passes with exactly 100 concurrent users sustained for 10 minutes without failures

✅ Integrated system maintains 99.9% uptime during continuous 72-hour test period

✅ 95th percentile response time stays under 1 second for all API endpoints during peak load

**Integration Checklist**:

- [ ] All 4 modules run with `docker-compose up`
- [ ] Can add an RSS feed and see entities
- [ ] Can sign up for email digest
- [ ] Receives at least one test email
- [ ] No crashes during 10-minute demo
- [ ] End-to-end tests pass
- [ ] Load tests meet performance targets

**Team Sync**: Show integrated system at final review

**Submission**:

- Save to: `docs/team/module-assignments/[your-module]/deliverables/phase-5-integration/`
- Include: Integration code, docker-compose.yml, test results, deployment docs
- Submit via PR following [Git Workflow](git-workflow.md)

---

## Module Independence → Integration

### Critical Concept: Standalone Development

**Through Phase 4**: Each module works **completely independently**

- No shared databases or services
- No dependencies on other team members' code
- Complete functionality demonstrable in isolation
- Use mock APIs for integration points

**Benefits**:

- Parallel development without blocking
- Each person can demo their work independently
- Reduced coordination overhead
- Clear ownership and accountability

### Integration Strategy

**Phase 5 Only**: Modules connect together

- Backend provides real APIs
- Frontend consumes real data
- AI processes actual content
- Publishing sends real emails

**Integration Points** (from Integration Charter):
```json
// Backend → AI
POST /api/extract
{
  "text": "article content",
  "source_id": 123
}

Response:
{
  "entities": [
    {"name": "YouTube", "type": "platform"},
    {"name": "Creator Fund", "type": "grant"}
  ]
}
```

---

## Key Principles & Constraints

### 1. Documentation-First Approach

- All specifications written before code
- PRDs are SpecKit-compatible for code generation
- Clear API contracts documented upfront
- Changes tracked through git and PRs

### 2. Local-First Development

- Everything runs on a developer's machine in Docker
- No cloud services required for development
- One-command startup: `docker-compose up`
- Complete local testing capability

### 3. Progressive Enhancement

- Start simple, add complexity only when needed
- MVP first, then enhance
- Avoid over-engineering in early phases

### 4. API-Driven Architecture

- Clear contracts between all components
- RESTful API design
- Standard error handling
- Comprehensive API documentation (Swagger/OpenAPI)

### 5. Stateless Services

- Horizontal scaling from day one
- No session state in application servers
- Database for persistence, Redis for caching

### 6. Security by Default

- Authentication, authorization, audit logging built-in
- Least-privilege access controls
- Deny-by-default outbound permissions
- Input validation at all boundaries

---

## Success Criteria

### For the System

**Phase 3 (MVP) Targets**:

- Docker container starts in under 30 seconds
- API operations complete in under 500ms
- 99% uptime over 24-hour test period

**Phase 5 (Integration) Targets**:

- 100 concurrent users sustained for 10 minutes
- 99.9% uptime during 72-hour test
- Sub-1-second p95 response time

### For Users

**Creator Transformation**:

- **Before**: 10+ hours/week searching for opportunities
- **After**: <2 hours/week reviewing curated insights
- **Result**: 8+ hours saved for content creation

**System Performance**:

- Processing 10,000+ sources daily
- 95% relevance rate for recommendations
- Sub-2-second query response times
- 99.9% uptime

### For the Project

**Research Impact**:

- Comprehensive intelligence layer for creator economy
- Significant reduction in time-to-opportunity discovery
- Improved creator success rates through better information access
- Sustainable research infrastructure

---

## Timeline & Coordination

### Phase Rhythm

**Phase Start**:

- Kickoff meeting
- Review previous progress
- Set priorities for phase

**Mid-Phase**:

- Sync meeting
- Resolve blockers
- Check progress

**Phase End**:

- Deliverable due
- Phase wrap-up
- Preview next phase

### Communication Schedule

**Daily**:

- Async updates in team channel
- Report blockers immediately

**Per Phase**:

- Phase kickoff meeting
- Mid-phase sync
- Phase review and handoff

**Weekly Checkpoints** (Phase 3-4):

- Week 1-2: Docker running with hello world
- Week 3-4: Mock APIs working
- Week 5-6: Basic features complete
- Week 7-8: Real features added
- Week 9-10: Integration started
- Week 11-12: Demo ready

### Meeting Schedule

See [schedule.md](schedule.md) for complete meeting schedule including in-person and virtual patterns.

---

## Quick Reference

### Key Documents by Phase

**Phase 1 - Research**:

- Read: [Phase 1 Deliverables](project-plan/phase-1-deliverables.md)
- Your module: `module-assignments/[module]/02-phase-1-research/`

**Phase 2 - Planning**:

- Read: [Phase 2 Deliverables](project-plan/phase-2-deliverables.md)
- Your module: `module-assignments/[module]/03-phase-2-prd+plan/`
- Example: [Publishing PRD Example](module-assignments/publishing-tools/deliverables/phase-2-planning/examples/PRD-example.md)

**Phase 3-5**:

- Submit to: `module-assignments/[module]/deliverables/phase-[N]/`

### Essential Resources

- **System Overview**: [design/product/system-overview.md](../design/product/system-overview.md)
- **Vision**: [design/strategy/vision.md](../design/strategy/vision.md)
- **Architecture**: [design/system/architecture.md](../design/system/architecture.md)
- **Integration Charter**: [design/system/integration-charter.md](../design/system/integration-charter.md)
- **Git Workflow**: [git-workflow.md](git-workflow.md)
- **Module Ownership**: [module-ownership.md](module-ownership.md)
- **Research Methodology**: [../design/research/methodology.md](../design/research/methodology.md)

### Getting Help

- **Technical questions**: Ask in `#kgl-[your-module]` channel
- **Integration issues**: Discuss in `#kgl-integration` channel
- **Process questions**: Check with @grig
- **Git/PR help**: See [git-workflow.md](git-workflow.md)

---

## Appendix: Data Flow Example

### Complete System Flow (Phase 5)

```
┌──────────────────────────────────────────────────────────┐
│ 1. Creator visits dashboard (Frontend)                  │
│    → Authenticates via Backend API                      │
│    → Views personalized dashboard                       │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ 2. Creator adds RSS feed URL (Frontend)                 │
│    → POST to Backend /api/sources                       │
│    → Backend validates and stores source                │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ 3. Backend fetches content (Scheduled Job)              │
│    → Retrieves new articles from RSS feed               │
│    → Stores raw content in database                     │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ 4. Backend calls AI for entity extraction               │
│    → POST to AI /api/extract with article text          │
│    → AI extracts entities (YouTube, Creator Fund, etc.) │
│    → Returns structured entity data                     │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ 5. Backend stores entities and relationships            │
│    → Saves entities to database                         │
│    → Updates knowledge graph connections                │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ 6. Frontend displays updated dashboard                  │
│    → GET from Backend /api/entities                     │
│    → Renders graph visualization with D3.js             │
│    → Shows new entities and relationships               │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ 7. Creator signs up for email digest (Frontend)         │
│    → POST to Backend /api/subscribers                   │
│    → Backend validates and stores subscription          │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ 8. Publishing sends personalized digest (Scheduled)     │
│    → GET subscriber preferences from Backend            │
│    → GET relevant entities based on preferences         │
│    → Generate personalized email content                │
│    → Send via SMTP                                      │
│    → POST delivery analytics to Backend                 │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ 9. Creator receives email and clicks link               │
│    → Tracking records engagement                        │
│    → Backend updates recommendation algorithm           │
│    → System learns from user behavior                   │
└──────────────────────────────────────────────────────────┘
```

---

**Document Maintenance**:

- Review quarterly or when major process changes occur
- Update version number and date when modified
- Notify team of significant changes
- Keep aligned with other planning documents

**Questions or Suggestions**: Contact @grig or open an issue for discussion
