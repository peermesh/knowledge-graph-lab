# Living Knowledge Collections - Roadmap

**Feature:** Living Knowledge Collections
**PRD:** `proposals/2026-01-25-PRD-LIVING-KNOWLEDGE-COLLECTIONS.md`
**Status:** Planning Complete

---

## Vision Summary

**Collections** are first-class objects that:
- **Evolve** - Accuracy improves through verification cycles
- **Hydrate** - Granular data fills in over time via AI
- **Visualize** - Modular infographic widgets present data
- **Connect** - Link to other collections forming a knowledge network
- **Challenge** - Actively question assumptions and seek citations

---

## Work Order Overview

```
PHASE 0: FOUNDATION
└── WO-000: Data Model & Core Types

PHASE 1: MVP CORE
├── WO-001: Basic UI (List & Detail Views)
├── WO-002: Widget System (Visual Components)
└── WO-003: Evolution Engine (Self-Improvement)

PHASE 2: MVP COMPLETE
├── WO-004: Inter-Collection Links
├── WO-005: Presentation Templates
└── WO-006: Faceted Index

PHASE 3: v1.0 POLISH (Future)
├── WO-007: AI-Powered Discovery
├── WO-008: Export & Sharing
└── WO-009: Collaboration Features
```

---

## Detailed Roadmap

### Phase 0: Foundation (3 days)

| WO | Title | Effort | Dependencies |
|----|-------|--------|--------------|
| **000** | Data Model & Core Types | 2-3 days | None |

**Deliverables:**
- TypeScript interfaces (Collection, CollectionItem, Schema)
- Built-in schemas (ranking, comparison, ecosystem, etc.)
- LocalStorage persistence layer
- Validation utilities

**Exit Criteria:** Types compile, CRUD works, no UI yet.

---

### Phase 1: MVP Core (12-15 days)

| WO | Title | Effort | Dependencies |
|----|-------|--------|--------------|
| **001** | Basic UI | 3-4 days | WO-000 |
| **002** | Widget System | 4-5 days | WO-001 |
| **003** | Evolution Engine | 5-6 days | WO-000, WO-001 |

**Deliverables:**
- Collection index and detail pages
- Create/edit forms with schema-driven fields
- 6 core widgets (RankingCard, StatBlock, etc.)
- Hydration worker (AI fills missing fields)
- Citation verification
- Assumption challenging
- Staleness detection

**Exit Criteria:** User can create collections, add items, see confidence scores, trigger evolution.

---

### Phase 2: MVP Complete (8-11 days)

| WO | Title | Effort | Dependencies |
|----|-------|--------|--------------|
| **004** | Inter-Collection Links | 3-4 days | WO-001 |
| **005** | Presentation Templates | 3-4 days | WO-002 |
| **006** | Faceted Index | 2-3 days | WO-001, WO-004 |

**Deliverables:**
- Link types (contains, references, extends, etc.)
- Link tree navigation
- 6 built-in templates (Top 10, Comparison, Ecosystem, etc.)
- Theme customization
- Faceted filtering (domain, type, confidence, freshness)
- Activity feed
- Quick stats dashboard

**Exit Criteria:** Full MVP - user can build, connect, style, and browse collections.

---

### Phase 3: v1.0 Polish (Future - 10-15 days)

| WO | Title | Effort | Dependencies |
|----|-------|--------|--------------|
| **007** | AI-Powered Discovery | 4-5 days | WO-003 |
| **008** | Export & Sharing | 3-4 days | WO-005 |
| **009** | Collaboration | 3-6 days | All |

**Deliverables:**
- Auto-suggested collections based on research
- Auto-discovered links between collections
- Export to PDF, JSON, embed code
- Public collection sharing
- Multi-user editing
- Comments and annotations

---

## Dependency Graph

```
                    ┌─────────────────────┐
                    │ WO-000: Foundation  │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           ▼                   ▼                   ▼
   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
   │ WO-001: UI    │   │ WO-003: Evolve│   │               │
   └───────┬───────┘   └───────────────┘   │               │
           │                               │               │
     ┌─────┼─────┐                         │               │
     ▼     ▼     ▼                         │               │
┌────────┐┌────────┐┌────────┐             │               │
│WO-002  ││WO-004  ││WO-006  │             │               │
│Widgets ││Links   ││Index   │             │               │
└────┬───┘└────────┘└────────┘             │               │
     │                                     │               │
     ▼                                     │               │
┌────────┐                                 │               │
│WO-005  │                                 │               │
│Template│                                 │               │
└────────┘                                 │               │
                                           │               │
              MVP COMPLETE ─────────────────┘               │
                                                           │
                    ┌──────────────────────────────────────┘
                    ▼
            ┌───────────────┐
            │ v1.0 (Future) │
            │ WO-007,008,009│
            └───────────────┘
```

---

## Effort Summary

| Phase | Work Orders | Days | Cumulative |
|-------|-------------|------|------------|
| Phase 0 | 1 | 2-3 | 2-3 |
| Phase 1 | 3 | 12-15 | 14-18 |
| Phase 2 | 3 | 8-11 | 22-29 |
| **MVP Total** | **7** | **22-29** | - |
| Phase 3 | 3 | 10-15 | 32-44 |
| **v1.0 Total** | **10** | **32-44** | - |

---

## Parallel Execution Opportunities

These can run concurrently:
- WO-002 (Widgets) + WO-003 (Evolution) after WO-001 starts
- WO-004 (Links) + WO-005 (Templates) after WO-001 and WO-002
- All Phase 3 work orders after MVP

**Optimal path with 2 parallel agents:**
- Agent A: WO-000 → WO-001 → WO-004 → WO-006
- Agent B: (wait) → WO-002 → WO-005 → WO-003

**Elapsed time: ~15-18 days to MVP** (vs 22-29 serial)

---

## Quick Reference: Collection Types

| Type | Description | Example |
|------|-------------|---------|
| `ranking` | Ordered lists | Top 10 LLMs |
| `comparison` | Side-by-side | Claude vs GPT |
| `ecosystem` | Connected tools | Music Production Stack |
| `timeline` | Temporal | History of AI |
| `network` | People/orgs | AI Researchers |
| `taxonomy` | Hierarchical | ML Algorithms Tree |

---

## Quick Reference: Predicates (Collection Links)

| Predicate | Meaning |
|-----------|---------|
| `contains` | Parent has child |
| `references` | Cites/mentions |
| `contradicts` | Conflicting data |
| `extends` | Adds depth |
| `supersedes` | Newer version |
| `relates_to` | Generic |

---

## Quick Reference: Evolution Tasks

| Task | Purpose |
|------|---------|
| `hydrate` | Fill missing fields via AI |
| `verify-citation` | Check link alive, content unchanged |
| `challenge-assumption` | Find counter-evidence |
| `check-staleness` | Flag old data |

---

## Files Created

```
.dev/ai/proposals/
└── 2026-01-25-PRD-LIVING-KNOWLEDGE-COLLECTIONS.md

.dev/ai/workorders/
├── 2026-01-25-WO-COLLECTIONS-000-FOUNDATION.md
├── 2026-01-25-WO-COLLECTIONS-001-BASIC-UI.md
├── 2026-01-25-WO-COLLECTIONS-002-WIDGETS.md
├── 2026-01-25-WO-COLLECTIONS-003-EVOLUTION.md
├── 2026-01-25-WO-COLLECTIONS-004-LINKS.md
├── 2026-01-25-WO-COLLECTIONS-005-TEMPLATES.md
├── 2026-01-25-WO-COLLECTIONS-006-INDEX.md
└── 2026-01-25-WO-COLLECTIONS-ROADMAP.md (this file)
```

---

## Next Action

**Start with WO-COLLECTIONS-000: Foundation**

This establishes the data model that everything else depends on.

---

*Living Knowledge Collections - From brainstorm to build plan.*
