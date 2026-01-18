# KGL Master Pipeline Architecture

**Version:** 1.0.0
**Date:** 2026-01-18
**Status:** AUTHORITATIVE - This is the source of truth for KGL pipeline design

---

## Executive Summary

This document synthesizes three pipeline architecture visions into a unified master design for the Knowledge Graph Lab:

1. **Foundation Architecture** (2026-01-09) - Two-loop reasoning system
2. **Ontology Decomposition Layer** (2026-01-17) - Granular concept extraction
3. **Visual Tuning UI** (pipeline-prototype-1) - Recipe configuration system

The result is a **three-tier architecture** combining autonomous reasoning, granular knowledge extraction, and tunable execution.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OUTER LOOP: REASONING ENGINE                        │
│  ┌─────────┐    ┌─────────┐    ┌─────────────────────────────────────────┐  │
│  │ EVALUATE│ →  │ DECIDE  │ →  │ CONTINUE | OUTPUT | ASK HUMAN | REFINE │  │
│  └─────────┘    └─────────┘    └─────────────────────────────────────────┘  │
│       ↑                                           │                         │
│       │              FEEDBACK LOOPS               │                         │
│       │   (Expansion, Verification, Conflict)     ↓                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    INNER LOOP: PROCESSING PIPELINE                   │   │
│  │                                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │   │
│  │  │ ROW 1: SEARCH & RETRIEVAL                                       │ │   │
│  │  │ QUERY → T1:MAP → GAPS → T2:ROUTE → [PARALLEL SEARCH] → MERGE    │ │   │
│  │  └─────────────────────────────────────────────────────────────────┘ │   │
│  │                              ↓                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │   │
│  │  │ QUEUE (Redis/BullMQ) - Decouples search from processing         │ │   │
│  │  └─────────────────────────────────────────────────────────────────┘ │   │
│  │                              ↓                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │   │
│  │  │ ROW 2: INGESTION & EXTRACTION                                   │ │   │
│  │  │ INGEST → T4:CHUNK → EXTRACT → T5:PAIR → RELATE                  │ │   │
│  │  └─────────────────────────────────────────────────────────────────┘ │   │
│  │                              ↓                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │   │
│  │  │ ROW 3: DECOMPOSITION LAYER (NEW)                                │ │   │
│  │  │ CONCEPTS → T:LENS → ONTOLOGY-MAP → TEMPORAL-TAG → PROVENANCE    │ │   │
│  │  └─────────────────────────────────────────────────────────────────┘ │   │
│  │                              ↓                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │   │
│  │  │ ROW 4: KNOWLEDGE GRAPH & SYNTHESIS                              │ │   │
│  │  │ KG-MERGE → T6:FILTER → SYNTH → OUTPUT                           │ │   │
│  │  └─────────────────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    TUNING LAYER: RECIPE SYSTEM                       │   │
│  │  [COST] [TELEMETRY] [CACHE] [RATE-LIMIT] [RETRY] [DEBUG]            │   │
│  │  Applied per-stage via composable switches with smart defaults       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tier 1: Outer Loop (Reasoning Engine)

**Source:** Foundation Architecture (2026-01-09)

The outer loop wraps the entire pipeline and makes autonomous decisions about when to continue processing, request more information, or output results.

### Control Flow

```
EVALUATE → DECIDE → ACTION
    ↑                  │
    └──────────────────┘
```

### Decision Logic

| State | Condition | Action |
|-------|-----------|--------|
| **Continue** | Confidence < 85% AND Coverage < 90% | Re-enter inner loop |
| **Expand** | Found entity X, need related Y | Queue expansion search |
| **Verify** | Single-source claim | Queue corroboration search |
| **Resolve** | Sources disagree | Queue authoritative source |
| **Refine** | Results too broad/narrow | Adjust query parameters |
| **Output** | Convergence criteria met | Generate final answer |
| **Ask Human** | Ambiguous OR confidence < 50% | Request clarification |

### Convergence Criteria

Exit when ANY condition is met:
- Confidence ≥ 85%
- Coverage ≥ 90%
- Diminishing returns (<5% new info for 2 iterations)
- Budget exhausted
- Max iterations reached (default: 10)
- User interrupt

### Feedback Loop Types

1. **Expansion** — Found entity X, need to search for related Y
2. **Verification** — Single-source claim, need corroboration
3. **Conflict Resolution** — Sources disagree, need authoritative source
4. **Refinement** — Results too broad/narrow, adjust query

---

## Tier 2: Inner Loop (Processing Pipeline)

**Source:** Visual Tuning UI (pipeline-prototype-1) + Foundation Architecture

The inner loop processes data through discrete stages, each with defined inputs, outputs, and tunable parameters.

### Row 1: Search & Retrieval

```
QUERY → T1:MAP → GAPS → T2:ROUTE → [PARALLEL SEARCH] → MERGE
```

| Stage | Type | Purpose | Cost | Latency |
|-------|------|---------|------|---------|
| P1: QUERY | stage | Parse NL into structured intent | $0.0002 | <50ms |
| T1: MAP | transform | Map intent to gap analysis input | $0 | <5ms |
| P2: GAPS | stage | Identify knowledge gaps via LLM | $0.003 | <200ms |
| T2: ROUTE | transform | Fan out to search backends | $0 | <10ms |
| P3: SEARCH | parallel | Execute multiple search strategies | varies | varies |
| MERGE | merge | Combine results via RRF | $0 | <100ms |

### Parallel Search Tools (P3)

| Tool | Type | Best For | Default |
|------|------|----------|---------|
| Meilisearch | Full-text | Typo tolerance, facets | ✓ ON |
| Qdrant | Vector | Semantic similarity | ✓ ON |
| Tavily | Web API | Real-time web search | OFF |
| Algolia | Hosted | Enterprise search | OFF |
| Elasticsearch | Boolean | Complex BM25 queries | OFF |
| Pinecone | Managed | Cloud vector DB | OFF |

### Queue (Decoupling Layer)

```
MERGE → [QUEUE] → INGEST
```

- **Technology:** Redis + BullMQ
- **Strategy:** FIFO with priority levels
- **Purpose:** Decouples search phase from processing phase
- **Throughput:** ~120 jobs/sec

### Row 2: Ingestion & Extraction

```
INGEST → T4:CHUNK → EXTRACT → T5:PAIR → RELATE
```

| Stage | Type | Purpose | Cost | Latency |
|-------|------|---------|------|---------|
| P4: INGEST | stage | Fetch & normalize documents | $0 | <5000ms |
| T4: CHUNK | transform | Prepare for extraction | $0 | <10ms |
| P5: EXTRACT | stage | Extract entities & facts via LLM | $0.005/doc | <2000ms |
| T5: PAIR | transform | Generate entity pairs | $0 | <20ms |
| P6: RELATE | stage | Build typed relationships | $0.003/batch | <1500ms |

### Row 3: Decomposition Layer (NEW)

**Source:** Ontology Decomposition Architecture (R-001, R-002)

This is the **critical missing layer** that transforms coarse topics into granular, connected concepts.

```
CONCEPTS → T:LENS → ONTOLOGY-MAP → TEMPORAL-TAG → PROVENANCE
```

| Stage | Type | Purpose | Cost | Latency |
|-------|------|---------|------|---------|
| CONCEPTS | stage | Extract atomic concepts (Cloud of Words) | $0.004 | <1500ms |
| T:LENS | transform | Apply perspective filter | $0 | <10ms |
| ONTOLOGY-MAP | stage | Induce relationships (is-a, causes, etc.) | $0.003 | <1000ms |
| TEMPORAL-TAG | stage | Add time dimension to relationships | $0.002 | <500ms |
| PROVENANCE | stage | Link concepts to source sentences | $0 | <100ms |

#### Concept Extraction

**Input:** High-level topic (e.g., "Regenerative Agriculture")
**Output:** Atomic concepts with relationships

```typescript
interface ConceptNode {
  id: string;                    // "soil_health"
  label: string;                 // "Soil Health"
  type: 'CONCEPT' | 'ENTITY' | 'PROCESS';
  layerId: string;               // "lens_ecological"
  provenance: {
    sourceVectorId: string;
    sourceText: string;          // Exact sentence
    confidence: number;
    lens: string;
  }
}
```

#### Multi-Lens System

Same data can be viewed through multiple perspectives:

| Lens | Focus | Example Concepts |
|------|-------|------------------|
| Default | General | All concepts |
| Ecological | Environment | Succession, Carbon Cycle, Biodiversity |
| Economic | Business | Insurance Risk, Timber Value, ROI |
| Social | Human | Displacement, Public Health, Policy |
| Technical | Implementation | Equipment, Processes, Standards |

**UI Control:** Toggle lenses on/off to filter visible connections

#### Temporal Ontology

Relationships gain time dimension for prediction:

```
STATIC:   A is related to B
TEMPORAL: A leads_to B (t+1) | A precedes B | A causes B (t+2y)
```

**Predictive Use Case:**
- Graph typically shows: `[Deforestation] → (t+2y) → [Soil Erosion] → (t+5y) → [Landslide]`
- New topic contains `[Deforestation]`
- System predicts `[Landslide]` as future topic node

### Row 4: Knowledge Graph & Synthesis

```
KG-MERGE → T6:FILTER → SYNTH → OUTPUT
```

| Stage | Type | Purpose | Cost | Latency |
|-------|------|---------|------|---------|
| P7: KG-MERGE | stage | Merge with conflict resolution | $0 | <500ms |
| T6: FILTER | transform | Extract relevant subgraph | $0 | <50ms |
| P8: SYNTH | stage | Generate answer with citations | $0.008 | <3000ms |
| OUTPUT | endpoint | Format and deliver | $0 | <10ms |

---

## Tier 3: Tuning Layer (Recipe System)

**Source:** Visual Tuning UI (pipeline-prototype-1)

Every stage can be tuned with composable "switches" — cross-cutting concerns that modify behavior without changing core logic.

### Available Switches

| Switch | Icon | Purpose | Applied To |
|--------|------|---------|------------|
| Cost Control | $ | Budget limits, tier selection | Paid API stages |
| Telemetry | ⏱ | Log level, sampling rate | All stages |
| Persist/Cache | 📦 | TTL, eviction strategy | Search, expensive stages |
| Rate Limit | 🚦 | Max req/sec, queue size | External APIs |
| Retry/Recovery | 🔄 | Attempts, backoff strategy | External stages |
| Debug/Snapshot | 📸 | Capture format, trigger | Complex stages |

### Switch Configurations

#### Cost Control
```yaml
budget_tier: free | standard | pro | unlimited
max_cost_per_call: $0.001 - $0.100
soft_cap_alert: true | false
```

#### Telemetry
```yaml
log_level: error | warn | info | debug | trace
sampling_rate: 0% - 100%
```

#### Persist/Cache
```yaml
ttl: 60s - 24h
strategy: LRU | FIFO | permanent
```

#### Rate Limit
```yaml
max_requests_per_sec: 1 - 1000
queue_size: 0 - 100
```

#### Retry/Recovery
```yaml
max_retries: 0 - 10
backoff_strategy: linear | exponential | static
```

#### Debug/Snapshot
```yaml
format: JSON | binary | text
trigger: on_error | always
```

### Smart Defaults

Switches auto-enable based on stage characteristics:

| Condition | Auto-Enabled |
|-----------|--------------|
| All stages | Telemetry |
| cost !== '$0.000' | Cost Control |
| type === 'search_tool' | Cache, Rate Limit |
| type === 'external' | Retry |
| stage in [query, gaps, extract, synth] | Debug |

### Global Settings

Override defaults across all applicable stages:

```yaml
global:
  cost_mode: unlimited | funded | broke | free
  telemetry_level: verbose | standard | critical
  cache_ttl: 3600  # seconds
```

---

## Data Flow Integration

### Complete Pipeline Flow

```
USER INPUT
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ OUTER LOOP evaluates state, decides action                      │
└─────────────────────────────────────────────────────────────────┘
    ↓ (if CONTINUE)
┌─────────────────────────────────────────────────────────────────┐
│ ROW 1: Query parsed, gaps identified, searches executed         │
│ QUERY → MAP → GAPS → ROUTE → [SEARCH x N] → MERGE               │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ QUEUE: Jobs buffered for processing                             │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ ROW 2: Documents ingested, entities extracted, relations built  │
│ INGEST → CHUNK → EXTRACT → PAIR → RELATE                        │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ ROW 3: Concepts decomposed, lenses applied, ontology mapped     │
│ CONCEPTS → LENS → ONTOLOGY-MAP → TEMPORAL-TAG → PROVENANCE      │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ ROW 4: Knowledge merged, filtered, synthesized                  │
│ KG-MERGE → FILTER → SYNTH → OUTPUT                              │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ OUTER LOOP evaluates result, decides next action                │
│ → CONTINUE (feedback loop) | OUTPUT (final) | ASK HUMAN         │
└─────────────────────────────────────────────────────────────────┘
    ↓ (if OUTPUT)
FINAL ANSWER WITH CITATIONS
```

### Key Data Structures

#### Topic (Lens)
```typescript
interface Topic {
  id: string;
  title: string;
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  domainId: string;
  researchData: string;
  concepts: ConceptNode[];        // From decomposition
  groundingMetadata: Citation[];  // From grounding layer
  recipeSnapshot: Recipe;         // From tuning layer
}
```

#### OntologyTriple
```typescript
interface OntologyTriple {
  id: string;
  sourceId: string;
  targetId: string;
  predicate: 'IS_A' | 'CAUSES' | 'PRECEDES' | 'REQUIRES' | 'RELATES_TO';
  weight: number;                 // 0-1 confidence
  layerId: string;                // Which lens
  temporalContext?: {
    startTime?: Date;
    endTime?: Date;
    isSequential: boolean;
  };
  provenance: {
    sourceText: string;
    discoverySource: 'USER' | 'AI_INFERENCE' | 'LITERATURE';
  };
}
```

#### Recipe
```typescript
interface Recipe {
  id: string;
  name: string;
  globalSettings: GlobalSettings;
  stageConfigs: {
    [stageId: string]: {
      [switchId: string]: {
        enabled: boolean;
        values: Record<string, any>;
      }
    }
  };
}
```

---

## Human-in-the-Loop Integration

### Feedback Capture Points

1. **Topic Approval** — User approves/rejects suggested topics
2. **Link Rejection** — User marks incorrect relationships
3. **Lens Preference** — User toggles preferred perspectives
4. **Quality Flags** — User flags shallow/incorrect content

### Knowledge Graph Tuning (KGT)

Feedback improves future runs without model retraining:

1. Store "Golden Tuples" (user-verified best connections)
2. Retrieve top 5 Golden Tuples during new extraction
3. Insert as few-shot examples in LLM prompts
4. System mimics user's preferred style and depth

### Negative Constraint Log

```typescript
interface Constraint {
  type: 'REJECTED_LINK' | 'WRONG_PREDICATE' | 'HALLUCINATION';
  sourceId: string;
  targetId: string;
  reason: string;
  timestamp: Date;
}
```

Future prompts include: "Do NOT generate links similar to [Rejected Examples]"

---

## Implementation Priorities

### Phase 1: Core Pipeline (Weeks 1-2)
- [ ] Implement Row 1 (Search & Retrieval)
- [ ] Implement Row 2 (Ingestion & Extraction)
- [ ] Implement Row 4 (KG-Merge & Synthesis)
- [ ] Basic outer loop (convergence only)

### Phase 2: Decomposition Layer (Weeks 3-4)
- [ ] Concept extraction stage
- [ ] Single-lens ontology mapping
- [ ] Provenance tracking
- [ ] Basic graph visualization

### Phase 3: Tuning System (Weeks 5-6)
- [ ] Switch infrastructure
- [ ] Per-stage configuration UI
- [ ] Recipe persistence
- [ ] Smart defaults

### Phase 4: Advanced Features (Weeks 7-8)
- [ ] Multi-lens system
- [ ] Temporal ontology
- [ ] Full feedback loops
- [ ] KGT integration

---

## Related Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Vision Master | `docs/foundation/00-VISION-MASTER.md` | Mission and pillars |
| Architecture Principles | `docs/foundation/01-ARCHITECTURE-PRINCIPLES.md` | Design principles |
| Search Infrastructure | `docs/foundation/02-SEARCH-INFRASTRUCTURE.md` | Tool selection |
| Conversation Synthesis | `docs/foundation/CONVERSATION-SYNTHESIS-2026-01-09.md` | Session decisions |
| Gemini Architecture Report | `docs/vision/KGL-GEMINI-ARCHITECTURE-REPORT.md` | UI implementation |
| Source of Truth Index | `docs/vision/KGL-SOURCE-OF-TRUTH-INDEX.md` | Document map |
| Tuning UI Report | `docs/vision/KGL-PIPELINE-TUNING-UI-REPORT.md` | Recipe system |
| R-001 Ontology | `.dev/ai/gemini-research/R-001-Ontology-Mapping-Architecture.md` | Decomposition |
| R-002 Mechanics | `.dev/ai/gemini-research/R-002-Pipeline-Mechanics.md` | Implementation |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-18 | Initial synthesis of three architecture visions |
