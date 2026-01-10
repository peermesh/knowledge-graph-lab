# KGL Pipeline Debugger: Sprint Plan

**Version:** 0.1.0-draft
**Created:** 2026-01-09
**Target:** Working prototype in 2 weeks

---

## Sprint Goal

**Deliver a working prototype that demonstrates:**

1. Visual pipeline with breakpoints
2. At least 2 swappable search backends
3. Reasoning loop visible (even if simplified)
4. Run replay capability
5. Clean, TE-inspired UI

**NOT in scope for this sprint:**
- All 8 pipeline layers (just search → ingest → extract)
- All search backends (just 2)
- Production-grade reasoning (simplified decision logic)
- Full knowledge graph merge (mock or SQLite)

---

## Phase 0: Foundation (Days 1-2)

### P0.1: Project Scaffolding

```bash
# Create monorepo structure
kgl-pipeline-debugger/
├── api/          # FastAPI
├── ui/           # React + Vite
├── modules/      # Pipeline modules
└── docker/       # Compose files
```

**Deliverables:**
- [ ] FastAPI skeleton with health endpoint
- [ ] React + Vite + Tailwind skeleton
- [ ] Docker Compose for Postgres + Redis
- [ ] Basic CI (lint, typecheck)

### P0.2: Core Data Models

**Deliverables:**
- [ ] Pydantic models for all pipeline stages
- [ ] TypeScript types (generated from Pydantic)
- [ ] Run manifest schema
- [ ] Event types for WebSocket

---

## Phase 1: Module Abstraction (Days 3-4)

### P1.1: Base Module Interface

```python
# modules/base.py
class PipelineModule(ABC):
    id: str
    name: str
    version: str
    category: str
    
    @abstractmethod
    def config_schema(self) -> dict: ...
    
    @abstractmethod
    async def process(self, input, context) -> output: ...
    
    def snapshot(self, input, output) -> Snapshot: ...
```

**Deliverables:**
- [ ] Base classes for all module types
- [ ] Module registry with auto-discovery
- [ ] Config schema to UI form generator

### P1.2: First Search Backends

Implement two backends to prove the abstraction:

**Meilisearch Adapter:**
- [ ] Connection management
- [ ] Query translation
- [ ] Result normalization

**Qdrant Adapter:**
- [ ] Connection management
- [ ] Vector search
- [ ] Result normalization

**Merge Strategy:**
- [ ] RRF (Reciprocal Rank Fusion)
- [ ] Merge audit log

---

## Phase 2: Orchestration API (Days 5-7)

### P2.1: Run Management

```
POST /api/v1/runs                 Create run
GET  /api/v1/runs/{id}            Get status
POST /api/v1/runs/{id}/start      Start
POST /api/v1/runs/{id}/pause      Pause
POST /api/v1/runs/{id}/step       Step once
```

**Deliverables:**
- [ ] Run state machine (created → running → paused → completed)
- [ ] Persistence to Postgres
- [ ] Basic error handling

### P2.2: Breakpoint System

```
POST /api/v1/breakpoints/{run}/{stage}   Set
DELETE /api/v1/breakpoints/{run}/{stage} Clear
```

**Deliverables:**
- [ ] Breakpoint storage
- [ ] Pipeline executor checks breakpoints
- [ ] State capture at breakpoint

### P2.3: WebSocket Streaming

```
WS /api/v1/runs/{id}/stream
```

**Deliverables:**
- [ ] Event broadcasting
- [ ] Client reconnection handling
- [ ] Backpressure management

---

## Phase 3: Simplified Reasoning (Days 8-9)

### P3.1: Minimal Reasoning Loop

For prototype, reasoning is rule-based (no LangGraph yet):

```python
def simple_reasoner(state: ReasoningState) -> Decision:
    if state.iteration >= state.max_iterations:
        return Decision.OUTPUT
    
    if state.confidence >= 0.85:
        return Decision.OUTPUT
    
    if len(state.gaps) == 0:
        return Decision.OUTPUT
    
    return Decision.CONTINUE
```

**Deliverables:**
- [ ] Simple gap detector (missing entities only)
- [ ] Basic confidence calculator
- [ ] Iteration loop with decision logging

### P3.2: State Visibility

**Deliverables:**
- [ ] Reasoning state endpoint
- [ ] Gap list with priorities
- [ ] Iteration history

---

## Phase 4: UI Implementation (Days 10-12)

### P4.1: Pipeline Visualization

```
┌────┐   ┌────┐   ┌────┐   ┌────┐
│ Q  │──▶│ S  │──▶│ I  │──▶│ E  │
└────┘   └────┘   └────┘   └────┘
```

**Deliverables:**
- [ ] Stage nodes with status indicators
- [ ] Connection lines with data flow animation
- [ ] Breakpoint markers (clickable)
- [ ] Progress indicators per stage

### P4.2: Inspector Panel

**Deliverables:**
- [ ] Input/Output toggle
- [ ] JSON tree viewer
- [ ] Search/filter in data
- [ ] Copy to clipboard

### P4.3: Config Panel

**Deliverables:**
- [ ] Dynamic form from JSON Schema
- [ ] Backend selector (multi-select)
- [ ] Apply button (hot-swap)
- [ ] Reset to defaults

### P4.4: Reasoning State Display

**Deliverables:**
- [ ] Confidence/coverage meters
- [ ] Gap list with status
- [ ] Iteration timeline
- [ ] Decision log

### P4.5: Controls

**Deliverables:**
- [ ] Run/Pause/Stop buttons
- [ ] Step button
- [ ] Restart iteration button
- [ ] Save/Load state

---

## Phase 5: Replay System (Days 13-14)

### P5.1: Snapshot Storage

**Deliverables:**
- [ ] Save snapshots per stage
- [ ] Manifest with all hashes
- [ ] Artifact storage (local filesystem for now)

### P5.2: Replay Execution

**Deliverables:**
- [ ] Load manifest
- [ ] Restore config
- [ ] Execute from specific stage
- [ ] Compare output hashes

### P5.3: Diff View

**Deliverables:**
- [ ] Side-by-side output comparison
- [ ] Highlight differences
- [ ] Hash verification status

---

## Technical Decisions (Locked for Sprint)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backend Framework | FastAPI | Async, Pydantic integration, WebSocket support |
| Frontend Framework | React + Vite | Fast dev, good TypeScript support |
| Styling | Tailwind | Rapid prototyping, consistent look |
| State Management | Zustand | Simple, TypeScript-friendly |
| Database | PostgreSQL | Reliable, JSON support for configs |
| Cache | Redis | Pub/sub for events, caching |
| Real-time | WebSocket | Native support in both frameworks |

---

## UI Aesthetic: Teenage Engineering Reference

**Core principles:**
- Information density without clutter
- Monospace where data matters
- Limited color palette (mostly grayscale + accent)
- Functional animations (show data flow, not decoration)
- Every pixel earns its place

**Colors:**
```css
:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #1a1a1a;
  --bg-elevated: #2a2a2a;
  --text-primary: #ffffff;
  --text-secondary: #888888;
  --accent: #ff6b00;          /* TE orange */
  --success: #00ff88;
  --warning: #ffcc00;
  --error: #ff4444;
}
```

**Typography:**
```css
font-family: 'JetBrains Mono', 'SF Mono', monospace;
```

**Component style:**
- Sharp corners (no border-radius)
- 1px borders, subtle
- Dense padding
- Uppercase labels, small

---

## Definition of Done

**Prototype is complete when:**

1. [ ] Can create a run with a query
2. [ ] Can see pipeline stages with status
3. [ ] Can set breakpoint, run pauses there
4. [ ] Can inspect input/output at breakpoint
5. [ ] Can swap search backend and resume
6. [ ] Can see reasoning state (gaps, confidence)
7. [ ] Can replay a completed run
8. [ ] UI is clean and responsive
9. [ ] README documents how to run locally
10. [ ] Demo video recorded

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Search backend integration takes too long | Mock backend as fallback |
| WebSocket complexity | Start with polling, upgrade later |
| UI takes too long | Use shadcn/ui components, customize later |
| Reasoning logic unclear | Hard-code simple rules, iterate |
| Docker orchestration issues | Run services locally for dev |

---

## Post-Sprint Backlog

Items deferred to future sprints:

- [ ] LangGraph integration for real reasoning
- [ ] Additional search backends (Typesense, Zoekt, Weaviate)
- [ ] Ingest module (PyMuPDF, Docling)
- [ ] Extract module (DeepSeek, Claude, spaCy)
- [ ] Full knowledge graph merge (Neo4j)
- [ ] Cost tracking and budgets
- [ ] User authentication
- [ ] Saved configurations/presets
- [ ] Batch runs
- [ ] API rate limiting
- [ ] Production deployment

---

## Daily Targets

| Day | Focus | Deliverable |
|-----|-------|-------------|
| 1 | Setup | Monorepo, Docker, CI |
| 2 | Models | Pydantic schemas, TS types |
| 3 | Modules | Base classes, registry |
| 4 | Search | Meilisearch + Qdrant adapters |
| 5 | API | Run CRUD, state machine |
| 6 | API | Breakpoints, stepping |
| 7 | API | WebSocket streaming |
| 8 | Reasoning | Simple loop, gap detection |
| 9 | Reasoning | State endpoints, history |
| 10 | UI | Pipeline viz, stage nodes |
| 11 | UI | Inspector, config panel |
| 12 | UI | Reasoning display, controls |
| 13 | Replay | Snapshot storage |
| 14 | Replay | Replay execution, diff view |

---

## Start Command

```bash
# Day 1 kickoff
mkdir kgl-pipeline-debugger
cd kgl-pipeline-debugger
git init

# Create structure
mkdir -p api/routers api/services api/models
mkdir -p modules/search modules/ingest modules/extract
mkdir -p ui/src/components ui/src/hooks ui/src/stores
mkdir -p docker runs configs

# Initialize Python
cd api
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic redis sqlalchemy asyncpg websockets

# Initialize React
cd ../ui
npm create vite@latest . -- --template react-ts
npm install tailwindcss @tanstack/react-query zustand
```

Ready to execute?
