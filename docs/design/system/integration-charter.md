# Integration Charter: Simplified MVP Architecture

**Conceptual source of truth for PRDs/Constitution: .dev/peermesh-canvases/**

## Purpose
Define minimal integration contracts for 4 junior developers to build independent modules that combine into a working prototype within 100 hours each.

## Architecture Overview
```
[Frontend:3000] → [Backend:8000] → [AI:8001]
                         ↓
                 [Publisher:8002]
```

## Module Responsibilities (Simplified for MVP)

### Backend Module (Port 8000)
- **Owner**: Developer 1
- **Core Job**: Fetch content, store data, provide APIs
- **Deliverables**:
  - REST API with 5 core endpoints
  - SQLite database with 4 tables
  - Docker container that starts with one command

### Frontend Module (Port 3000)
- **Owner**: Developer 2
- **Core Job**: Admin dashboard + user signup page
- **Deliverables**:
  - 2-page React app (Dashboard + Signup)
  - Connects to Backend API
  - Docker container with hot-reload

### AI Module (Port 8001)
- **Owner**: Developer 3
- **Core Job**: Extract entities from text (mock first, real later)
- **Deliverables**:
  - REST API with 3 endpoints
  - Mock responses for Phase 1
  - Real AI integration for Phase 2

### Publisher Module (Port 8002)
- **Owner**: Developer 4
- **Core Job**: Manage subscribers and send email digests
- **Deliverables**:
  - REST API with 4 endpoints
  - Email templates
  - Local SMTP for testing

## Integration Contracts (MVP)

### Data Flow
1. User adds RSS feed via Frontend
2. Backend fetches content periodically
3. Backend calls AI module to extract entities
4. Frontend displays entities on dashboard
5. User signs up for digest via Frontend
6. Publisher sends daily email with top entities

### API Contracts
```json
// Backend → AI
POST /api/extract
{
  "text": "article content",
  "source_id": 123
}

// Response
{
  "entities": [
    {"name": "YouTube", "type": "platform"},
    {"name": "Creator Fund", "type": "grant"}
  ]
}
```

### Database Schema (Minimal)
```sql
-- Backend owns these:
CREATE TABLE sources(id, url, active);
CREATE TABLE content(id, source_id, text, date);
CREATE TABLE entities(id, name, type);

-- Publisher owns these:
CREATE TABLE subscribers(id, email, active);
CREATE TABLE sent_digests(id, subscriber_id, sent_at);
```

## Development Phases

### Phase 1: Weeks 1-6 (Prototype)
- Each developer builds their module independently
- Use mock data and mock APIs
- Goal: Each module runs in Docker

### Phase 2: Weeks 7-10 (Enhancement)
- Add real features (real AI, better UI)
- Start integration testing
- Goal: Modules talk to each other

### Phase 3: Weeks 11-12 (Integration)
- Connect all modules via docker-compose
- End-to-end testing
- Goal: Working demo

## Success Metrics (MVP)
- [ ] All 4 modules run with `docker-compose up`
- [ ] Can add an RSS feed and see entities
- [ ] Can sign up for email digest
- [ ] Receives at least one test email
- [ ] No crashes during 10-minute demo

## Simplified State Machine
```
1. ADD_SOURCE → 2. FETCH_CONTENT → 3. EXTRACT_ENTITIES →
4. STORE_DATA → 5. SHOW_ON_DASHBOARD → 6. SEND_DIGEST
```

## Risk Mitigation
- **Integration Risk**: Use mock APIs until Phase 2
- **Complexity Risk**: Start with hardcoded data
- **Time Risk**: Focus on happy path only
- **Skill Risk**: Provide code examples and templates

## Developer Support

### Starter Kit per Module
1. Dockerfile template
2. Basic API server code
3. Mock data files
4. Postman collection for testing
5. Step-by-step setup guide

### Weekly Checkpoints
- Week 1-2: Docker running with hello world
- Week 3-4: Mock APIs working
- Week 5-6: Basic features complete
- Week 7-8: Real features added
- Week 9-10: Integration started
- Week 11-12: Demo ready

## Governance
- Daily standup (15 min) for blockers
- Shared Slack/Discord for questions
- ADRs for any major changes
- Git branches per developer
- PR reviews before merge

## References
- ADR-0002: Simplified MVP Architecture
- ADR-0003: Module Interface Contracts
- ADR-0004: Technology Stack Simplification
- ADR-0005: Data Model Boundaries

## MVP Transport Profile (Explicit)
- Persistence: SQLite for MVP; migration plan to PostgreSQL captured in ADR-0005.
- Communication: REST endpoints + polling; future upgrade path to WebSockets/event bus captured in ADR-0002/0003.
- AI: Mock extraction allowed only for initial integration; define a minimal real extraction path (spaCy or single provider sandbox) and KPIs before implementation (see Assumptions Register A1).

## Interface Agreements (Canonical, Tech-Agnostic)

**During concept phase, authoritative constitutional and core PRD content lives at /.dev/peermesh-canvases/ (see 00_MASTER_INDEX.md).**

Constitutional Decisions:

- [DECISION#1 - Module Manifest Policy](/.dev/peermesh-canvases/01_CONSTITUTION_SKELETON.md#decision1-module-manifest-policy)
- [DECISION#2 - Interaction Model](/.dev/peermesh-canvases/01_CONSTITUTION_SKELETON.md#decision2-interaction-model)
- [DECISION#3 - Abstraction Intents](/.dev/peermesh-canvases/01_CONSTITUTION_SKELETON.md#decision3-abstraction-intents)
- [DECISION#4 - Versioning Model](/.dev/peermesh-canvases/01_CONSTITUTION_SKELETON.md#decision4-versioning-model)
- [DECISION#5 - Lifecycle & Discovery](/.dev/peermesh-canvases/01_CONSTITUTION_SKELETON.md#decision5-lifecycle--discovery)
- [DECISION#6 - Security Stance](/.dev/peermesh-canvases/01_CONSTITUTION_SKELETON.md#decision6-security-stance)
- [DECISION#7 - Configuration Model](/.dev/peermesh-canvases/01_CONSTITUTION_SKELETON.md#decision7-configuration-model)
- [DECISION#8 - Observability Baseline](/.dev/peermesh-canvases/01_CONSTITUTION_SKELETON.md#decision8-observability-baseline)
- [DECISION#9 - Resource Provisioning & Namespacing](/.dev/peermesh-canvases/01_CONSTITUTION_SKELETON.md#decision9-resource-provisioning--namespacing)
- [DECISION#10 - UI Surface Policy](/.dev/peermesh-canvases/01_CONSTITUTION_SKELETON.md#decision10-ui-surface-policy)

Core PRD: [02_CORE_PRD_SKELETON.md](/.dev/peermesh-canvases/02_CORE_PRD_SKELETON.md)

Purpose

- Central source of truth for how modules interact. Tune here; PRDs and trackers reference these sections. Avoid tool/vendor specifics.

#### IA-01 Standard Envelope
Fields: intent, resource_type, payload|criteria, options{deadline_ms, idempotency_key}, meta{correlation_id, contract_version, route, attempt}
ResultEnvelope: status, data|errors[], meta{correlation_id, contract_version, route, attempt}

#### IA-02 Error Taxonomy
invalid | forbidden | not_found | conflict | retriable | fatal

#### IA-03 Sync / Async Rules
Auto sync→async when expected p95 > 250 ms or fan-out > 10; Receipts carry correlation_id and estimate_ms.

#### IA-04 Idempotency
Writes require idempotency_key; consumers MUST be idempotent; dedup on idempotency_key.

#### IA-05 Retry / Backoff / DLQ
Capped exponential retries for retriable; on exhaustion → DLQ with full envelope; redrive allowed within retention.

#### IA-06 Topic & Intent Naming
Topic: org.env.module.intent (lowercase dotted); intents use clear verbs (upsert_*, query_*, submit_*).

#### IA-07 Versioning (C‑SemVer vs I‑SemVer)
Contracts use C‑SemVer with 6‑month deprecation window; implementations use I‑SemVer; breaking changes require deprecation plan.

#### IA-08 Observability
Required: correlation_id, route, attempt; metrics (intent.count, status, latency.ms, retries.count, dlq.count); traces span per intent.

#### IA-09 Security & Scopes
Least‑privilege; deny-by-default outbound; minimal scope set:

data:read, data:write, event:publish, event:subscribe, config:read, config:write, secret:read, net:egress.

#### IA-10 Config Precedence
module → env → org → default; configs are declarative; Core resolves at call time.

#### IA-11 Provisioning & Onboarding
register → validate manifest → grant scopes → provision claims → sandboxed installer hook → conformance self‑test → ready.

**Platform Defaults (reference)**: See Constitution → Platform Defaults.

### API Agreements
- Backend
  - Endpoints: <list endpoints with method and path>
  - Requests/Responses: <JSON shapes with required/optional fields>
- AI
  - Endpoints: <list>
  - Requests/Responses: <shapes>
- Frontend
  - Consumes: <backend/ai/publisher endpoints referenced>
- Publishing
  - Endpoints: <list>
  - Requests/Responses: <shapes>

### Data Agreements
- Canonical Objects (IDs and fields)
  - Entity: { id, name, type, … }
  - Relation: { id, source_entity_id, target_entity_id, relation_type, … }
  - Document: { id, title, url, created_at, … }
  - Chunk: { id, document_id, text, position, … }
  - Subscriber (publishing): { id, email, preferences, … }
- Field requirements: mark required vs optional; avoid storage specifics.

### Interaction Agreements
- Sequences (sync/async TBD)
  - Example: Backend → AI: extract(text) → entities[] (timeout/latency placeholder)
  - Example: Frontend → Backend: fetch dashboard stats (rate/refresh placeholder)
- Error model: standard error structure (code, message, details, correlation_id).

### Auth/Scope Agreements
- Actions → required scopes/roles (provider-agnostic)
  - Example: manage_sources → admin
  - Example: read_entities → analyst|admin

### Message/Event Agreements (Optional)
- If/when events are used, define:
  - Event names and minimal payloads
  - Versioning policy (placeholder)
  - No transport decision here
