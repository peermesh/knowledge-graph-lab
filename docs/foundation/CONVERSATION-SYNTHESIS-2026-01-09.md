# Conversation Synthesis: KGL Architecture Session

**Date:** 2026-01-09
**Session:** OSS Code Search → Knowledge Vault Architecture → Pipeline Debugger Design
**Status:** Complete, actionable

---

## Session Overview

This document captures the complete thread of architectural decisions and insights from the 2026-01-09 conversation that established KGL's foundational direction.

---

## Topic 1: Sourcegraph and OSS Alternatives

### Question
Is Sourcegraph open source?

### Finding
**No longer.** Sourcegraph went fully proprietary in August 2024. It was Apache 2.0 licensed from 2018-2024.

### OSS Alternatives Identified

**Code-specific tools:**
| Tool | License | Mechanism | Best For |
|------|---------|-----------|----------|
| Zoekt | Apache 2.0 | Trigram | Fast code grep (Sourcegraph's actual backend) |
| OpenGrok | CDDL | Lucene + AST | Code intelligence (symbols, cross-refs) |
| Hound | MIT | Trigram | Simple self-hosted |
| Livegrep | BSD | Trigram | Extreme scale |
| SeaGOAT | MIT | Vectors | Semantic code search |

**General search tools:**
| Tool | License | Type | Best For |
|------|---------|------|----------|
| Meilisearch | MIT | Hybrid | Full-text + vectors, excellent DX |
| Qdrant | Apache 2.0 | Vector | Pure vector performance |
| Typesense | GPL-3.0 | Hybrid | Strong faceted search |
| Weaviate | BSD-3 | Vector + Graph | Integrated knowledge graph |

### Key Insight: Overlap Analysis

Code tools and general tools overlap significantly for "grep but faster" use cases. The differentiation is **structural intelligence**:

- Code tools parse through language grammars (understand what a function IS)
- General tools see text patterns (match strings)
- OpenGrok resolves "show me all callers of this method"
- Meilisearch cannot

---

## Topic 2: Tool Selection for KGL

### Question
Which tools should KGL use?

### Decision
**General-purpose tools (Meilisearch + Qdrant), not code-specific tools.**

### Rationale
KGL indexes *knowledge about* domains (research, documentation, specifications), not the domains themselves. When indexing knowledge about vector databases, we're not parsing vector database source code — we're treating articles and docs as text to understand.

Code-specific tools provide structural intelligence (symbols, cross-references) that's irrelevant when treating files as documents.

### Exception
If KGL needs actual code intelligence ("find all callers of this function"), code tools become relevant. For now, general tools are primary.

---

## Topic 3: Topology Observation

### Insight
Code tools' structural intelligence (symbols, cross-refs, first declaration) is domain-specific **topology**. The same concept could theoretically apply to other domains:

| Code Domain | Equivalent in Other Domains |
|-------------|----------------------------|
| First declaration | First mention in a book |
| All callers | All references to a concept |
| Class hierarchy | Taxonomic structure |
| Import graph | Citation graph |

### Status
Interesting research direction, but not blocking for current KGL work. Filed for future consideration.

---

## Topic 4: The Missing Reasoning Layer

### Problem
The 8-layer pipeline from KGL research is **passive** — data flows in, transforms flow out. But autonomous research requires decisions about:

- When to search again
- What gaps remain
- When confidence is sufficient
- How to resolve conflicts

### Solution: Two-Loop Architecture

**Outer Loop (Reasoning Engine):**
```
Evaluate → Decide → (Continue | Output | Ask Human)
```

**Inner Loop (Processing Pipeline):**
```
Query → Search → Ingest → Extract → Merge → Store
```

The outer loop **wraps** the inner loop and makes active decisions. This is the critical architectural insight.

### Feedback Loop Types

1. **Expansion** — Found entity X, need to search for related Y
2. **Verification** — Single-source claim, need corroboration
3. **Conflict Resolution** — Sources disagree, need authoritative source
4. **Refinement** — Results too broad/narrow, adjust query

### Convergence Criteria

System exits when ANY of:
- Confidence ≥ 85%
- Coverage ≥ 90%
- Diminishing returns (<5% new info for 2 iterations)
- Budget exhausted
- Max iterations (default: 10)
- User interrupt

---

## Topic 5: Visual Pipeline Debugger

### Requirements
- See content flowing through stages in real-time
- Stop at any point to inspect inputs/outputs
- Swap modules hot (different backends, extractors)
- Replay any run with identical results
- Extend with new modules without changing core code

### UI Aesthetic
Teenage Engineering style:
- Information density without clutter
- Monospace where data matters
- Limited color palette (grayscale + accent orange)
- Functional animations (data flow, not decoration)

### Key Features
- Pipeline view with stage nodes and status
- Breakpoint insertion (click to set)
- Inspector panel (input/output toggle, JSON tree)
- Config panel (auto-generated from schema)
- Reasoning state display (confidence, coverage, gaps)
- Controls (run, pause, step, restart, save)

---

## Topic 6: Module Abstraction

### Interface Contract
Every module implements:
```python
configure(config) → None      # Hot-reload
process(input, context) → output  # Transform
snapshot(input, output) → Snapshot  # Reproducibility
replay(snapshot) → output     # Verification
```

### Search Merging (Algorithmic, No LLM)
When multiple backends active, merge strategies:
- `reciprocal_rank_fusion` — Standard hybrid scoring
- `interleave_by_score` — Normalize and sort
- `round_robin` — Alternate sources
- `union_dedupe` — Combine and deduplicate

### Source-Type Routing
```yaml
"*.py|*.ts": zoekt       # Code gets AST-aware
"*.md|*.pdf": meilisearch  # Prose gets full-text
"*": qdrant              # Everything gets vectors
```

---

## Topic 7: Implementation Relationship

### Two Implementations

**UI Prototype (mark-26-01):**
- Location: `~/work/peermesh/repo/Knowledge-Graph-Lab---mark-26-01/`
- Stack: React 19 + TypeScript + Tailwind + Gemini API
- Purpose: Validate UX, test concepts
- Why AI Studio: Free tier, exposes Google tooling patterns

**Production Target (knowledge-graph-lab-alpha):**
- Location: `~/work/peermesh/repo/knowledge-graph-lab-alpha/`
- Stack: Full architecture with abstraction layers
- Purpose: Production implementation

### LLM Abstraction Priority

Must swap providers without pipeline rewrite:
- Local models (Ollama, llama.cpp)
- API providers (OpenAI, Anthropic, Google)
- Embedded SDKs (Claude Code SDK)

Current prototype uses Gemini directly. Production wraps in abstraction layer.

---

## Topic 8: Sprint Plan

### Scope (14 days)
- Visual pipeline with breakpoints
- 2 search backends (Meilisearch, Qdrant)
- Simple reasoning loop (rule-based, not LangGraph)
- Run replay capability
- Clean UI

### NOT in Scope
- All 8 layers (just search → ingest → extract)
- All backends
- Production-grade reasoning
- Full knowledge graph merge

### Build Philosophy
Incremental, not big bang. Full 8-layer at once would overwhelm.

---

## Documents Created

### Foundation (`docs/foundation/`)
| File | Purpose |
|------|---------|
| `README.md` | Index and governance |
| `00-VISION-MASTER.md` | Mission, pillars, direction |
| `01-ARCHITECTURE-PRINCIPLES.md` | Two-loop, convergence, modules |
| `02-SEARCH-INFRASTRUCTURE.md` | Tool selection, OSS analysis |
| `03-LLM-ABSTRACTION.md` | Provider swapping strategy |
| `04-IMPLEMENTATION-LINEAGE.md` | Prototype relationship |

### Pipeline Debugger (`docs/design/pipeline-debugger/`)
| File | Purpose |
|------|---------|
| `README.md` | Index, review checklist |
| `00-VISION.md` | UI mockup, reasoning layer |
| `01-ARCHITECTURE.md` | System layers, API, Docker |
| `02-DATA-FLOW.md` | Feedback loops, stage I/O |
| `04-SPRINT-PLAN.md` | 14-day build plan |

### Updated
| File | Changes |
|------|---------|
| `.dev/ai/STATE-OF-THE-PROJECT.md` | Version 3.0.0 with foundation docs |

---

## Key Quotes / Insights

> "KGL is not a chatbot. It is not a search tool. It is a **persistent research organism** that continuously expands, validates, and refines a knowledge graph."

> "The pipeline as described is **passive** (data flows through). What you're describing needs an **active reasoning layer**."

> "Code tools' structural intelligence is essentially **topology** over code. The same concept could apply to other domains."

> "General tools work fine when treating code files as documents to understand. Code tools only matter when you need jump-to-definition/find-usages."

> "Every pixel earns its place." (TE aesthetic)

---

## Action Items

1. **Review foundation documents** — Ensure alignment with vision
2. **Decide open questions:**
   - Reasoning transparency (show thinking or just decisions?)
   - Human-in-the-loop (at which confidence thresholds?)
   - Cost controls (hard stop or warn?)
   - Source trust (user-configurable weights?)
3. **Kick off sprint** — 14 days to working prototype
4. **Address git status** — Push commits, fix detached HEADs

---

## Session Metadata

- **Duration:** Extended session with context compaction
- **Artifacts:** 11 documents created/updated
- **Decision count:** 4 major architectural decisions
- **Research:** Sourcegraph history, 10+ OSS tools analyzed
