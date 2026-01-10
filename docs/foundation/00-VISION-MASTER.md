# Knowledge Graph Lab: Master Vision

**Version:** 1.0.0
**Created:** 2026-01-09
**Status:** Foundational (source of truth)

---

## Mission

Build a **self-replicating, recursive knowledge engine** that maps the latent space of human understanding into a navigable, visual ontology.

KGL is not a chatbot. It is not a search tool. It is a **persistent research organism** that continuously expands, validates, and refines a knowledge graph while the user works on other things.

---

## Core Pillars

### 1. Autonomy

The system traverses knowledge graphs without constant human intervention. It identifies gaps, hypothesizes connections, and decides when to dig deeper or stop.

**Key behaviors:**
- Detects what's missing (gap analysis)
- Decides what to search next (query planning)
- Knows when to stop (convergence detection)
- Handles contradictions (conflict resolution)

### 2. Visualization

Knowledge is structure, not just text. The ontology map is as important as the textual reports.

**Key capabilities:**
- Force-directed graph rendering
- Entity relationships visible at a glance
- Confidence levels indicated visually
- Gap areas highlighted for attention

### 3. Utility

The Knowledge Vault must be exportable, usable, and valuable. Research that can't be acted upon is worthless.

**Key outputs:**
- Structured reports with citations
- Exportable knowledge graphs
- Replayable research sessions
- Actionable recommendations

### 4. Debuggability

Unlike black-box AI systems, KGL exposes its reasoning. Every decision can be inspected, questioned, and corrected.

**Key features:**
- Visual pipeline debugger
- Breakpoint insertion at any stage
- Hot-swappable modules
- Run replay for reproducibility

---

## What KGL Is NOT

**Not a simple RAG pipeline.** RAG retrieves and generates. KGL reasons, expands, and converges.

**Not a one-shot research tool.** KGL runs iteratively until confidence thresholds are met or resources are exhausted.

**Not a black box.** Every stage is inspectable. Every decision is logged. Every run is reproducible.

**Not locked to one LLM provider.** Architecture supports swapping from local models to API to Claude Code SDK.

---

## The Two Loops

KGL operates with two distinct loops:

### Inner Loop: Processing Pipeline

```
Query → Search → Ingest → Extract → Merge → Store
```

This is the "data flows through" pipeline. Each stage transforms input to output. Modules are hot-swappable.

### Outer Loop: Reasoning Engine

```
Evaluate → Decide → (Continue | Output | Ask Human)
```

This wraps the processing pipeline. It decides:
- Are results sufficient?
- What gaps remain?
- Should we search again?
- Is confidence high enough?
- Have we hit resource limits?

**Critical insight:** The inner loop is passive. The outer loop is active. Both must be visible in the debugger.

---

## Convergence Philosophy

KGL doesn't run forever. It stops when ANY of:

1. **Confidence ≥ 85%** — Claims are well-supported
2. **Coverage ≥ 90%** — Subtopics addressed
3. **Diminishing returns** — Last 2 iterations added <5% new info
4. **Budget exhausted** — Cost or time limit reached
5. **Max iterations** — Safety valve (default: 10)
6. **User interrupt** — Human said stop

This prevents infinite loops while ensuring thorough research.

---

## UI Aesthetic: Teenage Engineering

The visual design follows Teenage Engineering principles:
- Information density without clutter
- Monospace where data matters
- Limited color palette (grayscale + accent orange)
- Functional animations (show data flow, not decoration)
- Every pixel earns its place

**Design philosophy:** Professional tools for serious work. No whimsy. No excess.

---

## Technology Strategy

### LLM Abstraction (Critical)

KGL must support multiple LLM providers without pipeline rewrites:
- Local models (Ollama, llama.cpp)
- API providers (OpenAI, Anthropic, Google)
- Embedded SDKs (Claude Code SDK)

**Current prototype:** Gemini API (free tier for development)
**Production target:** Abstraction layer with provider swapping

### Search Infrastructure

General-purpose search tools (not code-specific):
- **Meilisearch** — Primary full-text + hybrid search
- **Qdrant** — Vector embeddings for semantic search
- **Merge strategies** — RRF, weighted, round-robin

Code-specific tools (Zoekt, OpenGrok) available but secondary. KGL indexes *knowledge about* domains, not domain-specific artifacts directly.

### Storage

- **Neo4j** — Knowledge graph storage
- **PostgreSQL** — Run metadata, configs, snapshots
- **Redis** — Event streaming, caching
- **SQLite** — Development/debug mode

---

## Build Philosophy

### Incremental, Not Big Bang

The full 8-layer pipeline would overwhelm if built at once. Instead:

**Phase 1:** Search + Basic Reasoning (current focus)
- 2 search backends (Meilisearch, Qdrant)
- Simple gap detection
- Visual debugger prototype

**Phase 2:** Ingest + Extract
- Document parsing (PyMuPDF, Docling)
- Entity extraction (DeepSeek, spaCy)

**Phase 3:** Full Pipeline
- Knowledge graph merge (Neo4j)
- Answer synthesis
- Complete reasoning engine

### Prototype → Production Path

**AI Studio prototype** (mark-26-01): Validates UX, tests Gemini integration, proves concept
**Alpha project** (knowledge-graph-lab-alpha): Production architecture, abstraction layers, full implementation

The prototype feeds the production build. UI patterns transfer. Pipeline logic evolves.

---

## Success Criteria

**For the prototype sprint:**
- Visual pipeline with breakpoints
- 2 swappable search backends
- Reasoning loop visible in UI
- Run replay working

**For v1.0:**
- Full 8-layer pipeline operational
- Multiple LLM providers supported
- Knowledge vault exportable
- Confidence/coverage metrics accurate

**For long-term:**
- Multi-agent debate (research vs. skeptic)
- Multimodal input (images, PDFs as sources)
- 3D graph visualization
- Federated knowledge graphs

---

## Open Questions (Active)

1. **Reasoning transparency:** Show chain-of-thought or just decisions?
2. **Human-in-the-loop:** At which confidence thresholds?
3. **Cost controls:** Hard stop or warn-and-ask?
4. **Source trust:** User-configurable authority weights?

These will be resolved through prototype iteration.

---

## Related Documents

- [Architecture Principles](./01-ARCHITECTURE-PRINCIPLES.md) — Technical deep dive
- [Search Infrastructure](./02-SEARCH-INFRASTRUCTURE.md) — Tool analysis
- [LLM Abstraction](./03-LLM-ABSTRACTION.md) — Provider strategy
- [Implementation Lineage](./04-IMPLEMENTATION-LINEAGE.md) — Prototype relationship
- [Pipeline Debugger Sprint](../design/pipeline-debugger/) — Build plan
