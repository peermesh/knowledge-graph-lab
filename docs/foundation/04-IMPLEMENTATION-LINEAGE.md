# Knowledge Graph Lab: Implementation Lineage

**Version:** 1.0.0
**Created:** 2026-01-09
**Status:** Foundational (source of truth)

---

## Overview

KGL exists across multiple implementations at different stages of maturity. This document tracks their relationships, what transfers between them, and the path to production.

---

## Implementation Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            PRODUCTION TARGET                                 │
│                                                                              │
│   knowledge-graph-lab-alpha                                                  │
│   ~/work/peermesh/repo/knowledge-graph-lab-alpha/                           │
│                                                                              │
│   • Full 8-layer pipeline                                                    │
│   • LLM abstraction layer                                                    │
│   • Multi-backend search                                                     │
│   • Visual debugger                                                          │
│   • Production deployment                                                    │
│                                                                              │
└────────────────────────────────────────┬────────────────────────────────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         │                               │
                         ▼                               ▼
┌────────────────────────────────────┐   ┌────────────────────────────────────┐
│        UI PROTOTYPE                │   │      ARCHITECTURE RESEARCH         │
│                                    │   │                                    │
│   Knowledge-Graph-Lab---mark-26-01 │   │   docs/research/ai-pipeline/       │
│   ~/work/peermesh/repo/...         │   │   RESEARCH-SYNTHESIS.md            │
│                                    │   │                                    │
│   • React 19 + TypeScript          │   │   • 8-layer pipeline design        │
│   • Gemini API integration         │   │   • Tool recommendations           │
│   • 3-stage pipeline               │   │   • 13 research tracks             │
│   • Force-directed graph           │   │   • ~154K words analyzed           │
│   • Working UX patterns            │   │                                    │
│                                    │   │                                    │
└────────────────────────────────────┘   └────────────────────────────────────┘
```

---

## UI Prototype: mark-26-01

**Location:** `~/work/peermesh/repo/Knowledge-Graph-Lab---mark-26-01/`
**Purpose:** Validate UX patterns, test Gemini integration, prove concept
**Status:** Working, actively developed

### Technology Stack

| Layer | Choice |
|-------|--------|
| Framework | React 19 |
| Language | TypeScript |
| Styling | TailwindCSS |
| AI Provider | Google Gemini API (`@google/genai`) |
| State | React useState/useRef + localStorage |
| Visualization | D3-like force simulation (raw SVG/Canvas) |

### Implemented Features

| Feature | Status | Notes |
|---------|--------|-------|
| 3-stage pipeline | ✅ Complete | Research → Gap Analysis → Report |
| Force-directed graph | ✅ Complete | Jittery with >50 nodes |
| Safety rails (quota) | ✅ Complete | Prevents runaway costs |
| Modal detail views | ✅ Complete | |
| Bookmarks (bulk ops) | ✅ Complete | Export, delete |
| Notification system | ✅ Complete | Badges, event panel |
| Circular progress | 🔄 In progress | Refinement needed |
| Custom prompts UI | ⬜ Planned | |
| Local LLM (WebGPU) | ⬜ Planned | |
| 3D visualization | ⬜ Planned | |

### Data Model

```typescript
interface Topic {
  id: string;
  name: string;
  status: TopicStatus;
  // Saved to localStorage: cognos_topics
}

interface Report {
  id: string;
  topicId: string;
  content: string;
  // Saved to localStorage: cognos_reports
}

interface GraphLink {
  source: string;
  target: string;
  // Saved to localStorage: cognos_links
}
```

### Pipeline Stages

```
┌──────────────────────┐
│   RESEARCH STAGE     │
│                      │
│   Input: Topic name  │
│   Output: Raw data   │
│   Agent: Researcher  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   GAP ANALYSIS       │
│                      │
│   Input: Research    │
│   Output: New topics │
│   Agent: Analyst     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   REPORT GENERATION  │
│                      │
│   Input: Analysis    │
│   Output: Report     │
│   Agent: Writer      │
└──────────────────────┘
```

### What Transfers to Production

| Pattern | Transferable? | Notes |
|---------|---------------|-------|
| React + TypeScript | ✅ Yes | Same stack |
| Tailwind styling | ✅ Yes | Same approach |
| Force-directed graph | ✅ Yes | May upgrade to D3 proper |
| 3-stage pipeline | ⚠️ Partial | Expands to 8 stages |
| Gemini API calls | ⚠️ Partial | Wraps in abstraction layer |
| localStorage persistence | ❌ No | Moves to PostgreSQL/Neo4j |
| UX patterns | ✅ Yes | Notifications, badges, modals |

---

## Alpha Project: knowledge-graph-lab-alpha

**Location:** `~/work/peermesh/repo/knowledge-graph-lab-alpha/`
**Purpose:** Production implementation with full architecture
**Status:** Architecture defined, implementation in progress

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│   React + TypeScript + Tailwind                                             │
└───────────────────────────────────────┬─────────────────────────────────────┘
                                        │
┌───────────────────────────────────────┴─────────────────────────────────────┐
│                            ORCHESTRATION API                                 │
│   FastAPI + Pydantic + WebSocket                                            │
└───────────────────────────────────────┬─────────────────────────────────────┘
                                        │
┌───────────────────────────────────────┴─────────────────────────────────────┐
│                            REASONING ENGINE                                  │
│   LangGraph state machine                                                    │
└───────────────────────────────────────┬─────────────────────────────────────┘
                                        │
┌───────────────────────────────────────┴─────────────────────────────────────┐
│                          MODULE ABSTRACTION                                  │
│   Search | Ingest | Extract | Merge | Store                                 │
└───────────────────────────────────────┬─────────────────────────────────────┘
                                        │
┌───────────────────────────────────────┴─────────────────────────────────────┐
│                              DATA LAYER                                      │
│   PostgreSQL | Neo4j | Redis                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| Foundation docs | `docs/foundation/` | Source of truth (this folder) |
| Pipeline debugger | `docs/design/pipeline-debugger/` | Sprint-ready design |
| Research synthesis | `docs/research/ai-pipeline/` | Validated recommendations |
| State of project | `.dev/ai/STATE-OF-THE-PROJECT.md` | Current status |

### Repository Structure

- 13 independent Git repositories (including submodules)
- Main repo uses `alpha` remote (not `origin`)
- Kit system for modular development

---

## Migration Strategy

### Phase 1: Foundation (Current)

**Establish architectural foundations:**
- ✅ Vision documented
- ✅ Two-loop architecture defined
- ✅ Search infrastructure selected
- ✅ LLM abstraction designed
- ⬜ Sprint plan ready for execution

### Phase 2: Core Pipeline

**Build minimal viable pipeline:**
- Implement 2 search backends (Meilisearch, Qdrant)
- Basic reasoning loop (rule-based, not LangGraph)
- Visual debugger prototype
- Integration with existing UI patterns

### Phase 3: Full Pipeline

**Expand to 8 layers:**
- Ingest (PyMuPDF, Docling, Trafilatura)
- Extract (DeepSeek, spaCy hybrid)
- Merge (Neo4j TGFR)
- Full LangGraph reasoning

### Phase 4: Production Hardening

**Prepare for deployment:**
- LLM abstraction with multi-provider support
- Cost tracking and budgets
- Authentication
- Deployment configuration

---

## Why AI Studio for Prototype?

The mark-26-01 prototype uses Google AI Studio because:

1. **Free tier** — No cost during experimentation
2. **Best practices exposure** — Learn Google's tooling patterns
3. **Fast iteration** — Built-in hosting and hot reload
4. **Abstraction prep** — Understanding one provider informs abstraction design

**Not locked in:** The abstraction layer will replace direct Gemini calls with provider-agnostic interface.

---

## Code Transfer Guidelines

### Transferring from mark-26-01 to alpha:

**DO transfer:**
- Component structure and naming
- UX patterns (notifications, badges, modals)
- Graph visualization approach
- TypeScript types (with expansion)

**DO NOT transfer:**
- Direct Gemini API calls (wrap in abstraction)
- localStorage persistence (replace with proper DB)
- 3-stage pipeline (expand to 8)
- Hardcoded prompts (externalize)

**ADAPT:**
- GeminiService → LLMProvider interface
- App.tsx state → Zustand store
- Force simulation → Consider D3 proper or vis.js
- Raw CSS → Component library (shadcn/ui)

---

## Related Documents

- [Vision Master](./00-VISION-MASTER.md) — Product direction
- [Architecture Principles](./01-ARCHITECTURE-PRINCIPLES.md) — Technical design
- [LLM Abstraction](./03-LLM-ABSTRACTION.md) — Provider strategy
- [Pipeline Debugger](../design/pipeline-debugger/) — Sprint plan
