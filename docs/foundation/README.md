# Knowledge Graph Lab: Foundational Documents

**Purpose:** Source of truth for KGL vision, architecture, and critical path decisions.
**Created:** 2026-01-09
**Status:** Active foundation for all development

---

## Document Index

| # | Document | Purpose | Status |
|---|----------|---------|--------|
| 00 | [VISION-MASTER.md](./00-VISION-MASTER.md) | Core mission, pillars, and product direction | ✅ Complete |
| 01 | [ARCHITECTURE-PRINCIPLES.md](./01-ARCHITECTURE-PRINCIPLES.md) | Two-loop system, feedback patterns, convergence | ✅ Complete |
| 02 | [SEARCH-INFRASTRUCTURE.md](./02-SEARCH-INFRASTRUCTURE.md) | OSS alternatives, tool selection, abstraction layer | ✅ Complete |
| 03 | [LLM-ABSTRACTION.md](./03-LLM-ABSTRACTION.md) | Provider swapping strategy, local-to-API-to-SDK | ✅ Complete |
| 04 | [IMPLEMENTATION-LINEAGE.md](./04-IMPLEMENTATION-LINEAGE.md) | Relationship between prototypes and production | ✅ Complete |
| **05** | [**MASTER-PIPELINE-ARCHITECTURE.md**](./05-MASTER-PIPELINE-ARCHITECTURE.md) | **🚨 AUTHORITATIVE: Unified 3-tier pipeline design** | ✅ **NEW** |

### Session Records

| Document | Purpose |
|----------|---------|
| [CONVERSATION-SYNTHESIS-2026-01-09.md](./CONVERSATION-SYNTHESIS-2026-01-09.md) | Complete record of architectural decisions session |

---

## Related Documentation

### Pipeline Debugger Design (Sprint-Ready)
Location: `docs/design/pipeline-debugger/`
- Vision, architecture, data flow, sprint plan
- Ready for 2-week prototype sprint

### Research Synthesis (Completed)
Location: `docs/research/ai-pipeline/RESEARCH-SYNTHESIS.md`
- 8-layer pipeline validated recommendations
- 13 research tracks, ~154K words analyzed

### UI Prototype (Working)
Location: `ext-repos/Knowledge-Graph-Lab-mark-26-01/`
- React 19 + TypeScript + Tailwind
- 3-stage pipeline working with Gemini API
- Force-directed graph visualization

### Pipeline Tuning UI (NEW)
Location: `ext-repos/pipeline-prototype-1/`
- Visual pipeline configuration interface
- 6 composable switches (Cost, Telemetry, Cache, Rate Limit, Retry, Debug)
- Recipe persistence and smart defaults

### Vision Documents (NEW)
Location: `docs/vision/`
- Comprehensive reports on all 3 pipeline architectures
- Source of truth index for KGL documentation
- Knowledge enhancement resources from ~/.agents/

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-01-09 | Two-loop architecture | Processing pipeline needs active reasoning wrapper |
| 2026-01-09 | General search over code search | KGL indexes knowledge *about* code, not code itself |
| 2026-01-09 | LLM abstraction layer priority | Must swap providers without rewriting pipeline |
| 2026-01-09 | Incremental build approach | Full 8-layer at once would overwhelm |
| 2026-01-17 | Decomposition layer critical | Granular concept extraction enables cross-topic connections |
| 2026-01-17 | Multi-lens system | Same data viewed through multiple perspectives (Ecological, Economic, Social) |
| 2026-01-17 | Temporal ontology for prediction | Time-tagged relationships enable pattern detection |
| 2026-01-18 | **Master Pipeline Synthesis** | Unified 3 architectures: Foundation + Decomposition + Tuning UI |

---

## How to Use These Documents

**Starting a sprint?** Read VISION-MASTER → ARCHITECTURE-PRINCIPLES → relevant sprint docs

**Making a tool choice?** Read SEARCH-INFRASTRUCTURE → check research synthesis for validation

**Adding LLM provider?** Read LLM-ABSTRACTION → follow interface contract

**Understanding prototype relationship?** Read IMPLEMENTATION-LINEAGE

---

## Governance

These documents are foundational. Changes require:
1. Clear rationale documented in Decision Log
2. Update to affected downstream docs
3. Notification in project tracking
