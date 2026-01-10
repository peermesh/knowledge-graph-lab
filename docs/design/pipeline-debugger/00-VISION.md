# KGL Pipeline Debugger: Vision Document

**Version:** 0.1.0-draft
**Created:** 2026-01-09
**Status:** Ready for Review

---

## What We're Building

A visual pipeline debugger for knowledge research that lets you:

1. **See** content flowing through processing stages in real-time
2. **Stop** at any point to inspect inputs/outputs
3. **Swap** modules hot (different search backends, extractors, etc.)
4. **Replay** any run with identical results
5. **Extend** with new modules without changing core code

Think: IDE debugger meets Teenage Engineering's minimal-but-information-dense aesthetic.

---

## The Missing Layer: Reasoning & Deduction

The 8-layer pipeline from existing KGL research is **reactive** — data flows in, transforms flow out. But autonomous research requires an **active reasoning layer** that:

| Function | What It Does |
|----------|--------------|
| **Gap Detection** | "I found X but Y is missing" |
| **Query Refinement** | "Results too broad, narrowing to Z" |
| **Convergence Check** | "Sufficient evidence gathered, stopping" |
| **Conflict Resolution** | "Source A says X, Source B says Y — investigating" |
| **Confidence Assessment** | "High confidence on X, low on Y — need more sources" |

This isn't a single pipeline stage. It's an **outer loop** that wraps the entire pipeline.

---

## Architecture: Two Loops

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           REASONING LOOP (Outer)                             │
│                                                                              │
│   ┌─────────┐     ┌─────────────────────────────────────────────────────┐   │
│   │         │     │              PROCESSING LOOP (Inner)                 │   │
│   │ REASON  │────▶│                                                      │   │
│   │         │     │  [Query]→[Search]→[Ingest]→[Extract]→[Merge]→[Store] │   │
│   │ • Gaps? │     │                                                      │   │
│   │ • Done? │◀────│                                                      │   │
│   │ • Next? │     └─────────────────────────────────────────────────────┘   │
│   │         │                                                                │
│   └────┬────┘                                                                │
│        │                                                                     │
│        ▼                                                                     │
│   ┌─────────┐                                                                │
│   │ DECIDE  │                                                                │
│   │         │                                                                │
│   │ • Stop  │───▶ [Output: Synthesized Answer + Knowledge Graph Delta]       │
│   │ • Loop  │───▶ [Back to REASON with new query]                            │
│   │ • Ask   │───▶ [Human input needed]                                       │
│   └─────────┘                                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key insight:** The debugger needs to visualize BOTH loops. The inner loop is the "left-to-right" pipeline. The outer loop is the "why did it decide to search again?" reasoning.

---

## Feedback Paths

```
                                    ┌──────────────────┐
                                    │   USER QUERY     │
                                    └────────┬─────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐     │
│    │  REASON  │─────▶│  SEARCH  │─────▶│  INGEST  │─────▶│ EXTRACT  │     │
│    └──────────┘      └──────────┘      └──────────┘      └──────────┘     │
│         ▲                                                      │           │
│         │                                                      ▼           │
│         │            ┌──────────┐      ┌──────────┐      ┌──────────┐     │
│         │            │ SYNTHESTIC│◀─────│  MERGE   │◀─────│  STORE   │     │
│         │            └──────────┘      └──────────┘      └──────────┘     │
│         │                  │                                               │
│         │                  ▼                                               │
│         │            ┌──────────┐                                          │
│         └────────────│ EVALUATE │                                          │
│                      │          │                                          │
│    Feedback paths:   │ • Gaps?  │                                          │
│    ═══════════════   │ • Done?  │                                          │
│                      │ • Trust? │                                          │
│                      └──────────┘                                          │
│                            │                                               │
│              ┌─────────────┼─────────────┐                                 │
│              ▼             ▼             ▼                                 │
│         [CONTINUE]    [REFINE]      [OUTPUT]                               │
│         new sources   new query     to user                                │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘

FEEDBACK LOOP TYPES:

1. REFINEMENT LOOP (Query → Search → Evaluate → Query)
   "Results too broad, adding constraint"
   
2. EXPANSION LOOP (Store → Reason → Search)  
   "Found entity X, searching for related Y"
   
3. VERIFICATION LOOP (Extract → Search → Extract)
   "Claim needs verification from second source"
   
4. CONFLICT LOOP (Merge → Reason → Search)
   "Sources disagree, seeking authoritative source"
```

---

## Debugger UI: Full Vision

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ KGL Pipeline Debugger                              RUN: r_2026-01-09_001    │
│ ══════════════════════════════════════════════════════════════════════════ │
│                                                                             │
│ REASONING STATE                          ITERATION: 3 of max 10            │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ Goal: "What are the best OSS vector databases for RAG?"                 ││
│ │ Status: SEARCHING (2 gaps remaining)                                    ││
│ │                                                                         ││
│ │ Confidence: ████████░░ 78%    Coverage: ██████░░░░ 62%                  ││
│ │                                                                         ││
│ │ Known: Qdrant, Weaviate, Milvus, Chroma, pgvector                      ││
│ │ Gaps:  [Benchmark data for 1M+ vectors] [Cost comparison at scale]     ││
│ │ Next:  Searching for benchmark studies...                               ││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ PIPELINE FLOW                                                    [◀][▶][●] │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │                                                                         ││
│ │  ┌────┐   ┌────┐   ┌────┐   ┌────┐   ┌────┐   ┌────┐   ┌────┐        ││
│ │  │ Q  │══▶│ S  │══▶│ I  │══▶│ E  │══▶│ M  │══▶│ ST │══▶│ SY │        ││
│ │  │ ✓  │   │ ✓  │   │ ●  │   │    │   │    │   │    │   │    │        ││
│ │  └────┘   └────┘   └────┘   └────┘   └────┘   └────┘   └────┘        ││
│ │  Query    Search   Ingest   Extract  Merge    Store    Synth         ││
│ │                      ▲                                                ││
│ │                      │ BREAKPOINT                                     ││
│ │                                                                         ││
│ │  Data Volume: ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ││
│ │               Q:1  S:47  I:12/47  E:0  M:0  ST:0  SY:0                ││
│ │                                                                         ││
│ │  ◀──────────────── LOOP 3 ────────────────▶                            ││
│ │  [Loop 1: initial] [Loop 2: expanded] [Loop 3: current]               ││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ STAGE INSPECTOR                                          [INPUT] [OUTPUT]  │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ INGEST (processing 12 of 47 documents)                                  ││
│ │                                                                         ││
│ │  ┌─ arxiv:2401.15884 ──────────────────────────────────────────────┐   ││
│ │  │ Title: "Benchmarking Vector Databases at Scale"                  │   ││
│ │  │ Status: ████████████████████░░░░ 78% (extracting tables)         │   ││
│ │  │ Size: 2.3MB | Pages: 12 | Tables: 4 | Figures: 7                │   ││
│ │  └──────────────────────────────────────────────────────────────────┘   ││
│ │                                                                         ││
│ │  ┌─ github:qdrant/benchmarks ──────────────────────────────────────┐   ││
│ │  │ Status: ✓ Complete                                               │   ││
│ │  │ Extracted: 3 markdown files, 2 JSON configs                     │   ││
│ │  └──────────────────────────────────────────────────────────────────┘   ││
│ │                                                                         ││
│ │  + 10 more documents queued                                             ││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ MODULE CONFIG                                              [Apply] [Reset] │
│ ┌─────────────────────────────────────────────────────────────────────────┐│
│ │ EXTRACT (next stage)                                                    ││
│ │                                                                         ││
│ │ Backend      ○ DeepSeek V3      ● Claude Haiku      ○ spaCy NER        ││
│ │              ○ Hybrid (spaCy → LLM fallback)                            ││
│ │                                                                         ││
│ │ Entities     ☑ Organization  ☑ Product  ☑ Metric  ☐ Person             ││
│ │              ☑ Technology    ☐ Location ☑ Claim   ☐ Date               ││
│ │                                                                         ││
│ │ Confidence   [0.85] ─────────●──────────                                ││
│ │                                                                         ││
│ │ ┌─ Advanced ──────────────────────────────────────────────────────────┐││
│ │ │ Batch size: [10]   Timeout: [30s]   Retry: [3]                     │││
│ │ │ Cache: ● Enabled  ○ Disabled   TTL: [24h]                          │││
│ │ └─────────────────────────────────────────────────────────────────────┘││
│ └─────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
│ ─────────────────────────────────────────────────────────────────────────  │
│ [▶ Resume] [⏭ Step] [⏹ Stop] [↻ Restart Loop] [💾 Save State] [📋 Export] │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Reasoning Layer: Detailed Design

The REASON module is not just another pipeline stage. It's the **orchestrator** with its own decision logic.

### Inputs to Reasoner

| Input | Source | Purpose |
|-------|--------|---------|
| Original query | User | Goal to satisfy |
| Current knowledge state | Store | What we know |
| Gap analysis | Merge | What's missing |
| Confidence scores | Extract | Certainty levels |
| Iteration count | Self | Prevent infinite loops |
| Cost accumulator | All stages | Budget enforcement |

### Reasoner Decision Tree

```
                         ┌─────────────────┐
                         │ EVALUATE STATE  │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
              [SUFFICIENT]   [GAPS EXIST]   [CONFLICT]
                    │             │             │
                    ▼             ▼             ▼
               ┌────────┐   ┌────────┐    ┌────────┐
               │ OUTPUT │   │ EXPAND │    │RESOLVE │
               └────────┘   └────────┘    └────────┘
                                │             │
                    ┌───────────┼─────────────┤
                    ▼           ▼             ▼
              [REFORMULATE] [NEW ENTITY] [AUTHORITATIVE]
              narrow query  search for   seek primary
              add filters   related      source
              
                         ┌─────────────────┐
                         │ CHECK LIMITS    │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
              [UNDER BUDGET] [OVER BUDGET]  [MAX ITERS]
                    │             │             │
                    ▼             ▼             ▼
               [CONTINUE]    [ASK USER]    [FORCE OUT]
                             "spend more?"  best effort
```

### Convergence Criteria

The reasoner decides "done" when ANY of:

1. **Coverage threshold met** — 90%+ of identified subtopics addressed
2. **Confidence threshold met** — 85%+ average confidence on claims
3. **Diminishing returns** — last 2 loops added <5% new information
4. **Budget exhausted** — cost limit reached
5. **Iteration limit** — max loops (default 10)
6. **User interrupt** — manual stop

### Gap Detection Logic

```python
def detect_gaps(query_intent, knowledge_graph):
    """
    Returns list of gaps to fill.
    
    Gap types:
    - MISSING_ENTITY: Referenced but not defined
    - MISSING_RELATION: Entity exists, relationship unknown  
    - LOW_CONFIDENCE: Claim exists but single-source
    - STALE_DATA: Information older than threshold
    - CONFLICTING: Multiple contradictory claims
    """
    gaps = []
    
    # Check entity completeness
    for entity in query_intent.expected_entities:
        if entity not in knowledge_graph:
            gaps.append(Gap(type=MISSING_ENTITY, target=entity))
    
    # Check relationship completeness
    for relation in query_intent.expected_relations:
        if not knowledge_graph.has_path(relation.source, relation.target):
            gaps.append(Gap(type=MISSING_RELATION, target=relation))
    
    # Check confidence levels
    for claim in knowledge_graph.claims:
        if claim.source_count < 2:
            gaps.append(Gap(type=LOW_CONFIDENCE, target=claim))
    
    # Check for conflicts
    for entity in knowledge_graph.entities:
        claims = knowledge_graph.claims_about(entity)
        if has_contradiction(claims):
            gaps.append(Gap(type=CONFLICTING, target=entity, claims=claims))
    
    return prioritize(gaps)  # Sort by importance to query
```

---

## Module Interface Contract

Every module implements:

```typescript
interface PipelineModule {
  // Identity
  id: string;           // unique, e.g., "search.meilisearch"
  name: string;         // display name
  version: string;      // semver
  category: ModuleCategory;  // "search" | "ingest" | "extract" | "merge" | "reason"
  
  // Configuration
  configSchema: JSONSchema;   // For UI generation
  configure(config: object): void;
  getConfig(): object;
  
  // Processing
  process(input: StageInput): Promise<StageOutput>;
  
  // Debugging
  getState(): ModuleState;
  
  // Reproducibility
  snapshot(): Snapshot;
  replay(snapshot: Snapshot): Promise<StageOutput>;
}

interface StageInput {
  data: any;              // Typed per category
  metadata: {
    runId: string;
    iteration: number;
    timestamp: string;
    previousStage: string;
  };
}

interface StageOutput {
  data: any;              // Typed per category
  metrics: {
    latencyMs: number;
    itemsProcessed: number;
    cost: number;          // In USD
  };
  errors: Error[];
  warnings: Warning[];
}

interface Snapshot {
  moduleId: string;
  moduleVersion: string;
  config: object;
  inputHash: string;
  outputHash: string;
  input: StageInput;      // Full input for replay
  output: StageOutput;    // Full output for comparison
}
```

---

## Search Module: Multi-Backend Merge

When multiple search backends are active, results merge algorithmically (no LLM):

```typescript
interface SearchModule extends PipelineModule {
  category: "search";
  
  // Can enable multiple backends simultaneously
  backends: SearchBackend[];
  
  // Merge strategy for combining results
  mergeStrategy: "rrf" | "interleave" | "union" | "weighted";
  
  process(input: SearchInput): Promise<SearchOutput>;
}

interface SearchInput {
  query: string;
  filters?: SearchFilters;
  limit?: number;
}

interface SearchOutput {
  results: SearchResult[];
  
  // For debugging: results per backend BEFORE merge
  backendResults: {
    [backendId: string]: {
      results: SearchResult[];
      latencyMs: number;
      rawResponse: any;  // Original backend response
    }
  };
  
  // Merge audit trail
  mergeLog: MergeStep[];
}

interface SearchResult {
  id: string;
  content: string;
  score: number;           // Normalized 0-1
  source: string;          // Backend that found it
  sourceScore: number;     // Original backend score
  metadata: object;
}

// Reciprocal Rank Fusion (standard for hybrid search)
function rrf(backendResults: SearchResult[][], k: number = 60): SearchResult[] {
  const scores = new Map<string, number>();
  
  for (const results of backendResults) {
    for (let rank = 0; rank < results.length; rank++) {
      const item = results[rank];
      const rrfScore = 1 / (k + rank + 1);
      scores.set(item.id, (scores.get(item.id) || 0) + rrfScore);
    }
  }
  
  return Array.from(scores.entries())
    .sort((a, b) => b[1] - a[1])
    .map(([id, score]) => ({ ...findById(id), score }));
}
```

---

## Run Reproducibility

Every run saves a complete manifest:

```yaml
# runs/r_2026-01-09_001/manifest.yaml

run_id: r_2026-01-09_001
created: 2026-01-09T14:32:00Z
status: completed  # running | paused | completed | failed

query:
  original: "What are the best OSS vector databases for RAG?"
  intent_parsed:
    type: comparison
    entities: [vector_database, RAG]
    constraints: [open_source]

iterations:
  - iteration: 1
    reason: initial_search
    stages:
      - stage: query
        module: query.claude_haiku
        config_hash: sha256:abc...
        input_hash: sha256:def...
        output_hash: sha256:ghi...
        snapshot_path: snapshots/iter1_query.json
        
      - stage: search
        module: search.multi
        config:
          backends: [meilisearch, qdrant]
          merge: rrf
        # ... hashes and snapshot
        
    reasoning:
      gaps_found: 3
      confidence: 0.45
      decision: expand
      next_query: "vector database benchmarks scale performance"
      
  - iteration: 2
    reason: expand_benchmarks
    # ... stages
    
  - iteration: 3
    reason: resolve_conflict
    # ... stages

final_state:
  confidence: 0.87
  coverage: 0.91
  total_cost: 0.034
  convergence_reason: confidence_threshold_met

artifacts:
  knowledge_graph: outputs/kg_delta.json
  synthesis: outputs/answer.md
  sources: outputs/sources.json
```

To replay:
```bash
kgl replay r_2026-01-09_001 --from-iteration 2
```

---

## Extension Points

### Adding a New Search Backend

```typescript
// modules/search/my_search.ts
import { SearchBackend, register } from '@kgl/pipeline';

@register('search.my_custom')
class MyCustomSearch implements SearchBackend {
  id = 'my_custom';
  name = 'My Custom Search';
  
  configSchema = {
    type: 'object',
    properties: {
      apiKey: { type: 'string', secret: true },
      endpoint: { type: 'string', format: 'uri' }
    }
  };
  
  async search(query: string, config: object): Promise<SearchResult[]> {
    // Implementation
  }
}
```

Pipeline auto-discovers, UI shows in backend dropdown.

### Adding a New Reasoning Strategy

```typescript
// modules/reason/conservative.ts
import { Reasoner, register } from '@kgl/pipeline';

@register('reason.conservative')
class ConservativeReasoner implements Reasoner {
  // Requires 3+ sources for any claim
  // Stops after 5 iterations max
  // Prefers authoritative sources
}
```

---

## Open Questions for Review

1. **Reasoning transparency**: Should the UI show the reasoner's "thinking" (like chain-of-thought) or just decisions?

2. **Human-in-the-loop**: At what points should the system pause for user input vs. continue autonomously?

3. **Cost controls**: Hard stop at budget? Or warn and ask?

4. **Conflict resolution**: When sources disagree, how much effort to resolve vs. report both views?

5. **Source trust hierarchy**: Should some sources be weighted higher? User-configurable?

---

## Next: Sprint Documents

- `01-ARCHITECTURE.md` — Technical architecture detail
- `02-DATA-FLOW.md` — Complete data schemas
- `03-UI-WIREFRAMES.md` — Detailed UI mockups
- `04-SPRINT-PLAN.md` — What to build first
