# KGL Pipeline Schematic: Complete Reference

**Version:** 0.2.0
**Created:** 2026-01-09
**Updated:** 2026-01-10
**Purpose:** Complete pipeline specification for UI implementation and flow configuration
**Status:** Iterating — decisions locked, details expanding

---

## Design Decisions (Locked)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Transform visibility | **Visible as nodes** | Team learns by seeing everything in action |
| Parallel execution | **Fully supported** | UI, logic, and tooling for automated + user-edited flows |
| Icon sizing | **Large = major stages, Small = transforms/mixins** | Visual hierarchy |
| Click behavior | **Modal with summary, settings, docs** | Learn-by-doing interface |
| Mixin control | **Per-stage enable/disable** | Fine-grained control |
| Execution model | **Continue from breakpoint** (not re-run) | Like code editor debugging |
| Re-run | **Separate button, works on any pass** | Full replay capability |

---

## Visual Design Specification

### Icon Types

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ICON SIZING AND TYPES                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LARGE ICONS (64x64px) — Major Pipeline Stages                              │
│  ┌────────┐                                                                  │
│  │        │  Unique icon per stage type                                     │
│  │  QUERY │  Shows: name, status indicator, progress bar                    │
│  │        │  Click: Opens full config modal                                 │
│  └────────┘                                                                  │
│                                                                              │
│  SMALL ICONS (24x24px) — Transforms                                         │
│  ┌──┐                                                                        │
│  │T1│  Reused "transform" icon with number/label                            │
│  └──┘  Shows: transform type indicator                                      │
│        Click: Opens transform config modal                                   │
│                                                                              │
│  SMALL ICONS (24x24px) — Mixins (attached to stages)                        │
│  ┌──┐┌──┐┌──┐                                                               │
│  │$ ││⏱ ││📦│  Reused icons: $ = cost, ⏱ = trace, 📦 = cache, etc.         │
│  └──┘└──┘└──┘  Displayed as row below stage icon                            │
│               Click: Opens mixin config modal                                │
│               Toggle: Enable/disable per stage                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Flow Direction

```
LEFT ──────────────────────────────────────────────────────────────────▶ RIGHT

[START] → [STAGE] → [T] → [STAGE] → [T] → [STAGE] → ... → [END]

Parallel paths stack vertically:
                    ┌─→ [SEARCH:academic] → [T3a] →┐
[GAPS] → [T2] →────┼─→ [SEARCH:web]      → [T3b] →┼───→ [INGEST]
                    └─→ [SEARCH:code]     → [T3c] →┘
```

### Modal Structure (On Click)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SEARCH: Meilisearch                                              [×]       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ TABS:  [ Summary ]  [ Settings ]  [ Docs ]  [ Metrics ]                 ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════════│
│  SUMMARY TAB                                                                 │
│  ───────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  Purpose: Full-text and hybrid search using Meilisearch engine              │
│                                                                              │
│  Status: ✅ Ready                                                            │
│  Last Run: 2026-01-10 14:32:00 (245ms)                                      │
│  Cost This Run: $0.0000 (local)                                              │
│                                                                              │
│  Input:  SearchPriority[] (from T2 transform)                               │
│  Output: SearchResult[] (to T3 transform)                                   │
│                                                                              │
│  Quality Metrics (from research):                                            │
│  • Latency target: <2000ms ✅                                                │
│  • Validated accuracy: 95%+                                                  │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════════│
│  SETTINGS TAB                                                                │
│  ───────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  Endpoint:     [ http://localhost:7700      ]                               │
│  Index:        [ kgl_knowledge              ]                               │
│  API Key:      [ ••••••••••••               ] [Show]                        │
│                                                                              │
│  Searchable Attributes:                                                      │
│  [✓] title  [✓] content  [✓] summary  [ ] metadata                          │
│                                                                              │
│  Filterable Attributes:                                                      │
│  [✓] type  [✓] source  [✓] date  [✓] confidence                            │
│                                                                              │
│  Max Results: [ 50 ]                                                         │
│  Timeout (ms): [ 2000 ]                                                      │
│                                                                              │
│  [ Apply ] [ Reset to Defaults ]                                             │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════════│
│  DOCS TAB                                                                    │
│  ───────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  ## Meilisearch Search Module                                                │
│                                                                              │
│  Meilisearch is a lightning-fast search engine that provides:               │
│  - Full-text search with typo tolerance                                     │
│  - Faceted filtering                                                        │
│  - Hybrid vector search (since v1.3)                                        │
│                                                                              │
│  ### When to Use                                                             │
│  - Primary full-text search for prose documents                             │
│  - Hybrid search combining keywords + vectors                               │
│                                                                              │
│  ### Configuration Guide                                                     │
│  [Link to full docs...]                                                      │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════════│
│  METRICS TAB                                                                 │
│  ───────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  Last 10 Runs:                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ Latency (ms)                                                            ││
│  │ 500 ┤                                                                   ││
│  │ 400 ┤    ╭─╮                                                            ││
│  │ 300 ┤ ╭──╯ ╰──╮   ╭──╮                                                  ││
│  │ 200 ┤─╯       ╰───╯  ╰──────                                            ││
│  │ 100 ┤                                                                   ││
│  │   0 ┴─────────────────────────────────────                              ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  Avg Latency: 287ms | P95: 412ms | P99: 489ms                               │
│  Total Queries: 47 | Cache Hits: 23 (49%)                                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Execution Controls

### Toolbar

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ▶ Run  │  ⏸ Pause  │  ⏹ Stop  │  ⏭ Step  │  ↻ Re-run  │  💾 Save  │  📂 Load │
├─────────────────────────────────────────────────────────────────────────────┤
│  Iteration: 3/10  │  Confidence: 72%  │  Coverage: 85%  │  Cost: $0.023     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Button Behaviors

| Button | Behavior |
|--------|----------|
| **▶ Run** | Start execution from current position (beginning or breakpoint) |
| **⏸ Pause** | Pause at next stage boundary (completes current stage) |
| **⏹ Stop** | Halt immediately, preserve state |
| **⏭ Step** | Execute single stage, then pause |
| **↻ Re-run** | Opens modal: "Re-run from: [Beginning ▾] [Iteration 1 ▾] [Stage: QUERY ▾]" |
| **💾 Save** | Save complete pipeline state (config + data + position) |
| **📂 Load** | Load saved state, option to load config-only or config+data |

### Breakpoint Behavior

**Setting breakpoints:**
- Click on stage edge (left = before, right = after)
- Visual indicator: red dot on edge
- Multiple breakpoints allowed

**When breakpoint hit:**
- Execution pauses BEFORE that stage executes
- Inspector shows: previous stage output (which is next stage input)
- Status bar shows: "Paused at breakpoint: SEARCH"
- Options: Continue (▶), Step (⏭), or Inspect

**Continue from breakpoint:**
- Does NOT re-run previous stages
- Picks up exactly where paused
- Maintains all accumulated state

---

## Complete Pipeline Flow

### Full 8-Layer Pipeline with All Nodes

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                      │
│  REASONING ENGINE (Outer Loop) ─────────────────────────────────────────────────────────────────────│
│  Monitors: confidence, coverage, iteration_count, cost_budget, convergence_criteria                 │
│  Decides: CONTINUE (with refined query) | OUTPUT (synthesize answer) | ASK (human input needed)    │
│                                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                                                                                                  ││
│  │  PROCESSING PIPELINE (Inner Loop) ──────────────────────────────────────────────────────────────││
│  │                                                                                                  ││
│  │  [START]                                                                                         ││
│  │     │                                                                                            ││
│  │     ▼                                                                                            ││
│  │  ┌────────┐     ┌──┐     ┌────────┐     ┌──┐                                                    ││
│  │  │   L1   │     │  │     │   L2   │     │  │                                                    ││
│  │  │ QUERY  │────▶│T1│────▶│  GAPS  │────▶│T2│────┐                                               ││
│  │  │        │     │  │     │        │     │  │    │                                               ││
│  │  └────────┘     └──┘     └────────┘     └──┘    │                                               ││
│  │   mixins:        ▲        mixins:               │                                               ││
│  │   [$][⏱][📦]     │        [$][⏱][📦]            │                                               ││
│  │                  │                              │                                               ││
│  │                  │                              ▼                                               ││
│  │                  │        ┌─────────────────────────────────────────────┐                       ││
│  │                  │        │           PARALLEL SEARCH PATHS             │                       ││
│  │                  │        │                                             │                       ││
│  │                  │        │  ┌────────────┐     ┌──┐                    │                       ││
│  │                  │        │  │ L3:search  │     │  │                    │                       ││
│  │                  │        │  │ meilisearch│────▶│T3│──┐                 │                       ││
│  │                  │        │  └────────────┘     └──┘  │                 │                       ││
│  │                  │        │                           │                 │                       ││
│  │                  │        │  ┌────────────┐     ┌──┐  │  ┌──┐           │                       ││
│  │                  │        │  │ L3:search  │     │  │  ├─▶│  │           │                       ││
│  │                  │        │  │   qdrant   │────▶│T3│──┤  │M │           │                       ││
│  │                  │        │  └────────────┘     └──┘  │  │E │           │                       ││
│  │                  │        │                           │  │R │           │                       ││
│  │                  │        │  ┌────────────┐     ┌──┐  │  │G │           │                       ││
│  │                  │        │  │ L3:search  │     │  │  │  │E │           │                       ││
│  │                  │        │  │   tavily   │────▶│T3│──┘  │  │           │                       ││
│  │                  │        │  └────────────┘     └──┘     └──┘           │                       ││
│  │                  │        │                               │             │                       ││
│  │                  │        └───────────────────────────────┼─────────────┘                       ││
│  │                  │                                        │                                     ││
│  │                  │                                        ▼                                     ││
│  │                  │     ┌──┐     ┌────────┐     ┌──┐     ┌────────┐                              ││
│  │                  │     │  │     │   L4   │     │  │     │   L5   │                              ││
│  │                  │     │T4│◀────│ INGEST │◀────│  │◀────│EXTRACT │                              ││
│  │                  │     │  │     │        │     │  │     │        │                              ││
│  │                  │     └──┘     └────────┘     └──┘     └────────┘                              ││
│  │                  │               mixins:                  mixins:                               ││
│  │                  │               [$][⏱][📦]               [$][⏱][📦]                            ││
│  │                  │                                                                              ││
│  │                  │                                        │                                     ││
│  │                  │                                        ▼                                     ││
│  │                  │     ┌──┐     ┌────────┐     ┌──┐     ┌────────┐                              ││
│  │                  │     │  │     │   L6   │     │  │     │   L7   │                              ││
│  │                  └─────│  │◀────│ RELATE │◀────│T5│◀────│ MERGE  │                              ││
│  │   (feedback to         │  │     │        │     │  │     │        │                              ││
│  │    QUERY on next       └──┘     └────────┘     └──┘     └────────┘                              ││
│  │    iteration)                    mixins:                  mixins:                               ││
│  │                                  [$][⏱][📦]               [$][⏱][📦]                            ││
│  │                                                                                                  ││
│  │                                                           │                                     ││
│  │                                                           ▼                                     ││
│  │                                                    ┌──┐  ┌────────┐                             ││
│  │                                                    │  │  │   L8   │                             ││
│  │                                                    │T6│─▶│ SYNTH  │───▶ [OUTPUT]                ││
│  │                                                    │  │  │        │                             ││
│  │                                                    └──┘  └────────┘                             ││
│  │                                                           mixins:                               ││
│  │                                                           [$][⏱][📦]                            ││
│  │                                                                                                  ││
│  └─────────────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

Legend:
  [Lx STAGE] = Major pipeline stage (large icon, 64x64)
  [Tx]       = Transform node (small icon, 24x24)
  [MERGE]    = Result merger node (small icon, 24x24)
  [$][⏱][📦] = Mixin indicators (toggleable per-stage)
```

---

## Stage Specifications (From Validated Research)

### L1: QUERY — Parse & Plan

**Purpose:** Parse user query into structured intent with expected entities and relations

**Validated Approach:** Hybrid spaCy + LLM (Claude Haiku fallback)
**Quality Target:** 85%+ intent detection
**Latency Target:** <50ms
**Cost:** $0.0002/query (Claude Haiku, 50-100 tokens)
**Confidence:** Medium (specific benchmarks pending)

**Input Schema:**
```typescript
interface QueryInput {
  raw_query: string;                    // User's natural language query
  conversation_context?: Message[];     // Previous turns if multi-turn
  user_preferences?: UserPreferences;   // Preferred sources, depth, etc.
}
```

**Output Schema:**
```typescript
interface QueryOutput {
  query_id: string;
  original_query: string;
  
  intent: {
    type: "comparison" | "explanation" | "how_to" | "what_is" | "research" | "verification";
    confidence: number;                 // 0.0-1.0
    subtypes?: string[];                // e.g., ["benchmark", "pros_cons"] for comparison
  };
  
  entities: {
    name: string;
    type: string;                       // person, organization, concept, technology, etc.
    importance: "required" | "optional";
    aliases?: string[];
  }[];
  
  relations: {
    source_type: string;
    target_type: string;
    relation_type: string;              // is_a, part_of, competes_with, etc.
    importance: "required" | "optional";
  }[];
  
  constraints: {
    type: "date_range" | "source_type" | "domain" | "language" | "recency";
    value: any;
  }[];
  
  expected_output: {
    format: "prose" | "bullet_points" | "table" | "comparison_matrix";
    max_length?: number;
    include_citations: boolean;
    include_confidence: boolean;
  };
  
  search_hints: {
    suggested_queries: string[];
    suggested_sources: string[];
    depth: "shallow" | "moderate" | "deep";
  };
}
```

**Available Modules:**
| Module ID | Name | Description | Latency | Cost |
|-----------|------|-------------|---------|------|
| `query.spacy` | spaCy NLP | Fast local NER + dependency parsing | 5-15ms | $0 |
| `query.haiku` | Claude Haiku | LLM-based intent classification | 30-50ms | $0.0002 |
| `query.hybrid` | Hybrid | spaCy first, Haiku fallback for complex | 5-50ms | $0-0.0002 |
| `query.deberta` | DeBERTa Zero-shot | Transformer intent classification | 20-40ms | $0 |

**Configuration:**
```yaml
query:
  module: query.hybrid
  config:
    spacy_model: en_core_web_trf        # Best accuracy, needs GPU
    spacy_model_fallback: en_core_web_sm # CPU fallback
    llm_provider: anthropic
    llm_model: claude-3-haiku-20240307
    llm_fallback_threshold: 0.7         # Use LLM if spaCy confidence < this
    max_entities: 20
    max_relations: 30
    timeout_ms: 50
```

---

### L2: GAPS — Analyze Knowledge State

**Purpose:** Compare query requirements against current knowledge graph to identify gaps

**Validated Approach:** Hybrid Cypher + Graph Algorithms
**Quality Target:** 85%+ precision
**Achieved:** 87% precision, 82% recall
**Latency Target:** <100ms
**Achieved:** 65ms
**Cost:** $0.0003/query
**Confidence:** High (12 approaches benchmarked, 12 test cases)

**Input Schema:**
```typescript
interface GapsInput {
  query: QueryOutput;
  kg_snapshot: {
    entity_count: number;
    relationship_count: number;
    last_updated: string;
    
    // Pre-computed matches against query
    matched_entities: {
      query_entity: string;
      kg_entity_id: string;
      match_confidence: number;
      last_updated: string;
      source_count: number;
    }[];
    
    matched_relations: {
      query_relation: string;
      kg_relation_id: string;
      match_confidence: number;
      evidence_count: number;
    }[];
  };
}
```

**Output Schema:**
```typescript
interface GapsOutput {
  analysis_id: string;
  query_id: string;
  
  coverage: {
    entity_coverage: number;            // 0.0-1.0
    relation_coverage: number;          // 0.0-1.0
    overall_coverage: number;           // Weighted average
    by_importance: {
      required_coverage: number;
      optional_coverage: number;
    };
  };
  
  gaps: {
    id: string;
    type: "missing_entity" | "missing_relation" | "stale_data" | "low_confidence" | "single_source" | "conflict";
    priority: number;                   // 1-10, higher = more important
    description: string;
    
    // For missing_entity
    entity_name?: string;
    entity_type?: string;
    
    // For missing_relation
    source_entity?: string;
    target_entity?: string;
    relation_type?: string;
    
    // For stale_data
    entity_id?: string;
    last_updated?: string;
    staleness_days?: number;
    
    // For low_confidence
    claim_id?: string;
    current_confidence?: number;
    target_confidence?: number;
    
    // For single_source
    claim_id?: string;
    current_source_count?: number;
    
    // For conflict
    claim_ids?: string[];
    conflicting_values?: any[];
    
    suggested_queries: string[];
    estimated_search_cost: number;
  }[];
  
  search_plan: {
    total_gaps: number;
    addressable_gaps: number;           // Gaps we can search for
    estimated_searches: number;
    estimated_cost: number;
    
    priorities: {
      gap_id: string;
      search_queries: string[];
      target_sources: string[];
      expected_docs: number;
    }[];
  };
  
  recommendation: {
    action: "search" | "sufficient" | "ask_user";
    reason: string;
    confidence: number;
  };
}
```

**Available Modules:**
| Module ID | Name | Description | Latency | Cost |
|-----------|------|-------------|---------|------|
| `gaps.cypher` | Pure Cypher | Direct Neo4j queries only | 20-40ms | $0 |
| `gaps.graph_algo` | Graph Algorithms | PageRank, community detection | 40-80ms | $0 |
| `gaps.hybrid` | Hybrid | Cypher + algorithms + LLM reasoning | 50-100ms | $0.0003 |
| `gaps.llm` | LLM-based | Claude analyzes graph dump | 200-500ms | $0.002 |

**Configuration:**
```yaml
gaps:
  module: gaps.hybrid
  config:
    neo4j_uri: bolt://localhost:7687
    neo4j_user: neo4j
    neo4j_password: ${NEO4J_PASSWORD}
    
    # Gap detection thresholds
    staleness_threshold_days: 30
    low_confidence_threshold: 0.7
    min_source_count: 2
    
    # Algorithm weights
    use_pagerank: true
    use_community_detection: true
    use_llm_reasoning: true
    llm_provider: anthropic
    llm_model: claude-3-haiku-20240307
    
    # Limits
    max_gaps: 20
    max_search_queries_per_gap: 3
    timeout_ms: 100
```

---

### L3: SEARCH — Multi-Source Retrieval

**Purpose:** Execute searches across multiple backends, merge results

**Validated Approach:** LangGraph + Tavily + Exa + academic APIs
**Quality Target:** Relevant documents for gaps
**Latency Target:** <2000ms
**Cost:** $0.005-0.025/query (highly variable based on search count)
**Confidence:** High

**Parallel Execution Model:**
- Multiple search backends execute simultaneously
- Results merge after all complete (or timeout)
- Configurable: wait-for-all vs first-N-results

**Input Schema:**
```typescript
interface SearchInput {
  search_plan: GapsOutput["search_plan"];
  
  config: {
    backends: {
      id: string;
      enabled: boolean;
      weight: number;                   // For weighted merge
      max_results: number;
      timeout_ms: number;
    }[];
    
    merge_strategy: "rrf" | "interleave" | "weighted" | "union";
    
    routing: {
      pattern: string;                  // Glob pattern: "*.pdf", "academic:*"
      backends: string[];               // Which backends handle this pattern
    }[];
    
    global_max_results: number;
    global_timeout_ms: number;
    min_backends_required: number;      // Fail if fewer respond
  };
}
```

**Output Schema:**
```typescript
interface SearchOutput {
  search_id: string;
  
  results: {
    id: string;
    backend: string;
    
    // Source identification
    url?: string;
    title: string;
    source_type: "web" | "academic" | "code" | "documentation" | "news";
    
    // Content
    snippet: string;                    // 200-500 chars
    full_content?: string;              // If available
    
    // Scoring
    backend_score: number;              // Original backend score
    merged_score: number;               // After merge algorithm
    relevance_to_gaps: {
      gap_id: string;
      relevance: number;
    }[];
    
    // Metadata
    published_date?: string;
    author?: string;
    domain?: string;
    language?: string;
    
    retrieved_at: string;
  }[];
  
  backend_stats: {
    backend_id: string;
    status: "success" | "timeout" | "error" | "disabled";
    latency_ms: number;
    results_count: number;
    error_message?: string;
  }[];
  
  merge_log: {
    strategy: string;
    input_counts: Record<string, number>;
    output_count: number;
    dedup_removed: number;
    decisions: {
      result_id: string;
      action: "included" | "deduped" | "filtered";
      reason: string;
    }[];
  };
  
  cost: {
    total: number;
    by_backend: Record<string, number>;
  };
}
```

**Available Search Backends:**

| Module ID | Name | Type | Latency | Cost/Search | Notes |
|-----------|------|------|---------|-------------|-------|
| `search.meilisearch` | Meilisearch | Full-text + Hybrid | 20-100ms | $0 (self-hosted) | Primary for prose |
| `search.qdrant` | Qdrant | Vector | 10-50ms | $0 (self-hosted) | Primary for semantic |
| `search.tavily` | Tavily | Web Search | 500-2000ms | $0.01 | Web content |
| `search.exa` | Exa | Neural Search | 500-2000ms | $0.01 | High quality web |
| `search.arxiv` | arXiv API | Academic | 200-500ms | $0 | Academic papers |
| `search.semantic_scholar` | Semantic Scholar | Academic | 200-500ms | $0 | Citation-aware |
| `search.github` | GitHub Search | Code | 300-800ms | $0 | Code search |
| `search.google` | Google Search API | Web | 200-500ms | $0.005 | Broad web |

**Merge Strategies:**

| Strategy | Algorithm | Best For |
|----------|-----------|----------|
| `rrf` | Reciprocal Rank Fusion: `score = Σ(1/(k + rank))` | Default, balanced |
| `interleave` | Normalize 0-1, sort combined | Similar quality backends |
| `weighted` | `score = backend_weight × normalized_score` | Known quality differences |
| `union` | Combine all, dedupe by content hash | Maximum recall |

**RRF Implementation (k=60 standard):**
```python
def rrf_merge(backend_results: dict[str, list[Result]], k: int = 60) -> list[Result]:
    scores: dict[str, float] = {}
    result_map: dict[str, Result] = {}
    
    for backend, results in backend_results.items():
        for rank, result in enumerate(results):
            result_id = result.content_hash  # Dedupe by content
            result_map[result_id] = result
            scores[result_id] = scores.get(result_id, 0) + 1 / (k + rank + 1)
    
    sorted_ids = sorted(scores.keys(), key=lambda x: -scores[x])
    return [result_map[id] for id in sorted_ids]
```

**Configuration:**
```yaml
search:
  parallel_execution: true
  wait_for_all: false                   # Return when min_backends respond
  min_backends_required: 2
  global_timeout_ms: 3000
  global_max_results: 100
  
  merge_strategy: rrf
  rrf_k: 60
  
  backends:
    - id: meilisearch
      module: search.meilisearch
      enabled: true
      weight: 1.0
      max_results: 50
      timeout_ms: 500
      config:
        endpoint: http://localhost:7700
        index: kgl_knowledge
        api_key: ${MEILI_API_KEY}
        
    - id: qdrant
      module: search.qdrant
      enabled: true
      weight: 0.9
      max_results: 50
      timeout_ms: 500
      config:
        endpoint: http://localhost:6333
        collection: kgl_embeddings
        embedding_model: text-embedding-3-small
        embedding_dim: 1536
        
    - id: tavily
      module: search.tavily
      enabled: true
      weight: 0.8
      max_results: 20
      timeout_ms: 2000
      config:
        api_key: ${TAVILY_API_KEY}
        search_depth: advanced
        include_raw_content: true
        
    - id: arxiv
      module: search.arxiv
      enabled: true
      weight: 0.7
      max_results: 20
      timeout_ms: 1000
      config:
        max_results: 20
        sort_by: relevance
        
  routing:
    - pattern: "academic:*"
      backends: [arxiv, semantic_scholar]
    - pattern: "code:*"
      backends: [github, meilisearch]
    - pattern: "*.pdf"
      backends: [meilisearch]
    - pattern: "*"
      backends: [meilisearch, qdrant, tavily]
```

---

### L4: INGEST — Document Processing

**Purpose:** Parse documents, extract text, chunk for processing

**Validated Approach:** PyMuPDF + Docling + Trafilatura
**Quality Target:** 90%+ extraction accuracy
**Achieved:** 95%+ accuracy
**Latency Target:** <5s per document
**Achieved:** <5s (0.1s for PyMuPDF)
**Cost:** $0.005-0.01/query ($0.001-0.002 per doc, 5 docs avg)
**Confidence:** High

**Input Schema:**
```typescript
interface IngestInput {
  documents: SearchOutput["results"];
  
  config: {
    chunking: {
      strategy: "semantic" | "fixed" | "sentence" | "paragraph";
      chunk_size: number;               // Target tokens per chunk
      chunk_overlap: number;            // Overlap tokens
      respect_boundaries: boolean;      // Don't split mid-sentence
    };
    
    extraction: {
      extract_tables: boolean;
      extract_images: boolean;
      extract_metadata: boolean;
      preserve_formatting: boolean;
      
      // Parser selection by format
      parsers: {
        pdf: "pymupdf" | "docling" | "marker" | "unstructured";
        html: "trafilatura" | "beautifulsoup" | "readability";
        docx: "docling" | "python-docx";
        markdown: "native";
      };
    };
    
    filtering: {
      min_chunk_tokens: number;
      max_chunk_tokens: number;
      remove_boilerplate: boolean;
      language_filter?: string[];
    };
  };
}
```

**Output Schema:**
```typescript
interface IngestOutput {
  ingest_id: string;
  
  documents: {
    doc_id: string;
    source_result_id: string;
    
    metadata: {
      title: string;
      url?: string;
      author?: string;
      published_date?: string;
      language: string;
      format: string;
      original_size_bytes: number;
      extracted_size_bytes: number;
    };
    
    status: "success" | "partial" | "failed";
    error_message?: string;
    parser_used: string;
    extraction_time_ms: number;
  }[];
  
  chunks: {
    chunk_id: string;
    doc_id: string;
    
    content: string;
    token_count: number;
    chunk_index: number;
    total_chunks_in_doc: number;
    
    // Position in original
    start_char: number;
    end_char: number;
    page_number?: number;
    
    // Embeddings (if computed)
    embedding?: number[];
    embedding_model?: string;
    
    // Extracted structures
    tables?: {
      table_id: string;
      headers: string[];
      rows: string[][];
      caption?: string;
    }[];
    
    images?: {
      image_id: string;
      caption?: string;
      alt_text?: string;
      ocr_text?: string;
    }[];
  }[];
  
  stats: {
    total_documents: number;
    successful: number;
    partial: number;
    failed: number;
    total_chunks: number;
    total_tokens: number;
    avg_chunk_size: number;
    total_tables: number;
    total_images: number;
  };
}
```

**Available Parsers:**

| Parser | Formats | Accuracy | Latency | Notes |
|--------|---------|----------|---------|-------|
| PyMuPDF | PDF | 98% | 0.1s/page | Fast, reliable |
| Docling | PDF, DOCX | 97.9% tables | 0.5s/page | Best for tables |
| Trafilatura | HTML | 93.7% | 0.2s/page | Best boilerplate removal |
| Marker | PDF | 95% | 1s/page | Good for academic |
| Unstructured | Many | 90% | Variable | Most flexible |
| Google Vision | Scanned | 97% | 0.5s/page | OCR for images |

**Chunking Strategies:**

| Strategy | Description | Best For |
|----------|-------------|----------|
| `semantic` | Split at topic boundaries using embeddings | General use (87-89% F1) |
| `fixed` | Fixed token count with overlap | Consistent processing |
| `sentence` | Split at sentence boundaries | Short documents |
| `paragraph` | Split at paragraph boundaries | Well-structured docs |

**Configuration:**
```yaml
ingest:
  parallel_documents: 5
  compute_embeddings: true
  embedding_model: text-embedding-3-small
  embedding_batch_size: 100
  
  chunking:
    strategy: semantic
    chunk_size: 512
    chunk_overlap: 50                   # ~10% overlap
    respect_boundaries: true
    
  extraction:
    extract_tables: true
    extract_images: false               # Expensive, enable when needed
    extract_metadata: true
    preserve_formatting: false
    
    parsers:
      pdf: pymupdf
      html: trafilatura
      docx: docling
      markdown: native
      
  filtering:
    min_chunk_tokens: 50
    max_chunk_tokens: 1000
    remove_boilerplate: true
    language_filter: [en]               # English only for now
```

---

### L5: EXTRACT — Entity Extraction

**Purpose:** Identify entities in chunks with type and confidence

**Validated Approach:** Hybrid NER + LLM
**Quality Target:** 85%+ F1
**Achieved:** 92% F1 (hybrid), 96% F1 (DeepSeek pure)
**Latency Target:** <1s per chunk
**Cost:** $0.0003/query (DeepSeek V3)
**Confidence:** High (11 providers benchmarked)

**Input Schema:**
```typescript
interface ExtractInput {
  chunks: IngestOutput["chunks"];
  query_context: QueryOutput;           // To prioritize relevant entity types
  
  config: {
    entity_types: string[];             // Types to extract
    
    extraction: {
      use_ner: boolean;                 // spaCy/Flair first pass
      use_llm: boolean;                 // LLM for complex entities
      llm_provider: string;
      llm_model: string;
      
      ner_model: string;                // spaCy model
      ner_threshold: number;            // Min NER confidence
      llm_threshold: number;            // When to invoke LLM
    };
    
    deduplication: {
      enabled: boolean;
      strategy: "exact" | "fuzzy" | "semantic" | "hybrid";
      fuzzy_threshold: number;          // 0.0-1.0
      semantic_threshold: number;       // 0.0-1.0
    };
    
    limits: {
      max_entities_per_chunk: number;
      max_total_entities: number;
    };
  };
}
```

**Output Schema:**
```typescript
interface ExtractOutput {
  extraction_id: string;
  
  entities: {
    entity_id: string;
    
    // Core identification
    name: string;
    canonical_name: string;             // After normalization
    type: string;
    
    // Confidence and provenance
    confidence: number;
    extraction_method: "ner" | "llm" | "hybrid";
    source_chunks: string[];
    mention_count: number;
    
    // Variations
    aliases: string[];
    mentions: {
      chunk_id: string;
      text: string;
      start_char: number;
      end_char: number;
    }[];
    
    // Attributes (type-specific)
    attributes: Record<string, {
      value: any;
      confidence: number;
      source_chunk: string;
    }>;
    
    // Deduplication
    is_duplicate: boolean;
    canonical_entity_id?: string;       // If merged with another
    merge_reason?: string;
  }[];
  
  stats: {
    total_extracted: number;
    after_dedup: number;
    by_type: Record<string, number>;
    by_method: Record<string, number>;
    avg_confidence: number;
    processing_time_ms: number;
  };
}
```

**Available Entity Types (Core 8 from research):**

| Type | Description | Example |
|------|-------------|---------|
| `person` | Human individuals | "Yann LeCun" |
| `organization` | Companies, institutions | "Anthropic" |
| `concept` | Abstract ideas | "transformer architecture" |
| `technology` | Tools, frameworks, protocols | "PyTorch", "HTTPS" |
| `metric` | Quantitative measures | "F1 score", "latency" |
| `location` | Geographic entities | "San Francisco" |
| `event` | Named events | "NeurIPS 2024" |
| `artifact` | Papers, products, datasets | "GPT-4", "ImageNet" |

**Available Modules:**

| Module ID | Name | F1 Score | Cost/1M entities | Latency |
|-----------|------|----------|------------------|---------|
| `extract.spacy` | spaCy NER | 85% | $0 | 2.6ms |
| `extract.flair` | Flair NER | 88% | $0 | 15ms |
| `extract.deepseek` | DeepSeek V3 | 96% | $2.80 | 200ms |
| `extract.claude` | Claude Haiku | 92% | $12.50 | 150ms |
| `extract.hybrid` | NER + LLM | 92% | $2.63 | 50ms |

**Configuration:**
```yaml
extract:
  module: extract.hybrid
  
  entity_types:
    - person
    - organization
    - concept
    - technology
    - metric
    - artifact
    
  extraction:
    use_ner: true
    use_llm: true
    
    ner_model: en_core_web_trf          # GPU recommended
    ner_threshold: 0.7
    llm_threshold: 0.5                  # Use LLM if NER < 0.5
    
    llm_provider: deepseek
    llm_model: deepseek-chat
    llm_batch_size: 10                  # Chunks per LLM call
    
  deduplication:
    enabled: true
    strategy: hybrid
    fuzzy_threshold: 0.85
    semantic_threshold: 0.90
    
  limits:
    max_entities_per_chunk: 50
    max_total_entities: 1000
```

---

### L6: RELATE — Relationship Extraction

**Purpose:** Identify relationships between extracted entities

**Validated Approach:** Hybrid spaCy + selective LLM
**Quality Target:** 85%+ precision
**Achieved:** 93% precision
**Latency Target:** <500ms per entity pair
**Achieved:** 170ms
**Cost:** $0.0005/query (80% reduction vs pure LLM)
**Confidence:** High (5 methods compared, 12 entity pairs tested)

**Input Schema:**
```typescript
interface RelateInput {
  entities: ExtractOutput["entities"];
  chunks: IngestOutput["chunks"];       // For context
  query_context: QueryOutput;           // To prioritize relevant relations
  
  config: {
    relationship_types: string[];
    
    extraction: {
      use_dependency_parsing: boolean;  // spaCy dep parse
      use_pattern_matching: boolean;    // Rule-based patterns
      use_llm: boolean;                 // LLM for complex
      
      llm_provider: string;
      llm_model: string;
      
      cross_sentence: boolean;          // Look across sentences
      max_sentence_distance: number;    // Max sentences apart
    };
    
    validation: {
      min_confidence: number;
      require_evidence: boolean;
      max_relations_per_pair: number;
    };
  };
}
```

**Output Schema:**
```typescript
interface RelateOutput {
  relation_id: string;
  
  relationships: {
    relationship_id: string;
    
    // Endpoints
    source_entity_id: string;
    target_entity_id: string;
    
    // Relation type
    type: string;
    direction: "directed" | "bidirectional";
    
    // Confidence and evidence
    confidence: number;
    extraction_method: "dependency" | "pattern" | "llm" | "hybrid";
    
    evidence: {
      chunk_id: string;
      text: string;                     // The sentence(s) containing relation
      start_char: number;
      end_char: number;
    }[];
    
    // Attributes
    attributes: Record<string, any>;    // e.g., temporal info, strength
  }[];
  
  conflicts: {
    conflict_id: string;
    relationship_ids: string[];
    conflict_type: "contradictory" | "duplicate" | "subsumption";
    description: string;
    resolution_suggestion?: string;
  }[];
  
  stats: {
    total_extracted: number;
    by_type: Record<string, number>;
    by_method: Record<string, number>;
    conflicts_found: number;
    avg_confidence: number;
    processing_time_ms: number;
  };
}
```

**Core Relationship Types (10 from research):**

| Type | Description | Example |
|------|-------------|---------|
| `is_a` | Type hierarchy | "GPT-4 is_a LLM" |
| `part_of` | Composition | "Attention is part_of Transformer" |
| `created_by` | Authorship | "PyTorch created_by Meta" |
| `uses` | Utilization | "LangChain uses OpenAI" |
| `competes_with` | Competition | "Claude competes_with GPT-4" |
| `related_to` | General association | "NLP related_to linguistics" |
| `preceded_by` | Temporal sequence | "GPT-4 preceded_by GPT-3" |
| `located_in` | Geographic | "Anthropic located_in SF" |
| `works_for` | Employment | "Dario works_for Anthropic" |
| `measured_by` | Metrics | "Quality measured_by F1" |

**Configuration:**
```yaml
relate:
  module: relate.hybrid
  
  relationship_types:
    - is_a
    - part_of
    - created_by
    - uses
    - competes_with
    - related_to
    
  extraction:
    use_dependency_parsing: true
    use_pattern_matching: true
    use_llm: true
    
    llm_provider: anthropic
    llm_model: claude-3-haiku-20240307
    llm_threshold: 0.6                  # Use LLM if dep parse < 0.6
    
    cross_sentence: true
    max_sentence_distance: 3
    
  validation:
    min_confidence: 0.7
    require_evidence: true
    max_relations_per_pair: 3
```

---

### L7: MERGE — Knowledge Graph Integration

**Purpose:** Deduplicate and merge new entities/relations into knowledge graph

**Validated Approach:** TGFR Framework + Neo4j
**Quality Target:** 99%+ precision, 98%+ recall
**Achieved:** 100% precision, 100% recall
**Latency Target:** <60s for 100K entities
**Achieved:** 48-90s batch, <2s with UNWIND
**Cost:** $0.0004/query ($20-40 per 10K entities for dedup)
**Confidence:** High (24 algorithm configs tested)

**Input Schema:**
```typescript
interface MergeInput {
  entities: ExtractOutput["entities"];
  relationships: RelateOutput["relationships"];
  
  config: {
    deduplication: {
      strategy: "fuzzy" | "semantic" | "llm" | "hybrid";
      
      fuzzy: {
        algorithm: "levenshtein" | "jaro_winkler" | "token_sort";
        threshold: number;
      };
      
      semantic: {
        embedding_model: string;
        threshold: number;
      };
      
      llm: {
        provider: string;
        model: string;
        batch_size: number;
      };
    };
    
    conflict_resolution: {
      strategy: "newest" | "highest_confidence" | "most_sources" | "ask_human";
      auto_resolve_threshold: number;   // Above this, auto-resolve
    };
    
    neo4j: {
      uri: string;
      user: string;
      password: string;
      database: string;
      
      batch_size: number;
      use_unwind: boolean;              // Critical for performance
    };
  };
}
```

**Output Schema:**
```typescript
interface MergeOutput {
  merge_id: string;
  
  graph_delta: {
    entities_added: number;
    entities_merged: number;
    entities_updated: number;
    relationships_added: number;
    relationships_updated: number;
  };
  
  dedup_decisions: {
    decision_id: string;
    action: "added" | "merged" | "skipped";
    
    entity_id: string;
    merged_with?: string;               // If merged
    
    method: string;                     // Which algorithm decided
    confidence: number;
    reason: string;
  }[];
  
  conflict_resolutions: {
    resolution_id: string;
    conflict_type: string;
    entities_involved: string[];
    
    resolved: boolean;
    resolution_method?: string;
    resolution_value?: any;
    
    needs_human_review: boolean;
    human_review_reason?: string;
  }[];
  
  pending_conflicts: {
    conflict_id: string;
    description: string;
    options: {
      option_id: string;
      value: any;
      confidence: number;
      source: string;
    }[];
  }[];
  
  stats: {
    processing_time_ms: number;
    neo4j_operations: number;
    dedup_comparisons: number;
    conflicts_auto_resolved: number;
    conflicts_pending: number;
  };
}
```

**TGFR Algorithm (Validated 100% precision/recall):**
```
TGFR = Token + Graph + Fuzzy + Reasoning

1. Token matching: Exact string match on normalized names
2. Graph context: Same neighbors = likely same entity
3. Fuzzy matching: Jaro-Winkler > 0.85 on names
4. LLM reasoning: For edge cases, ask LLM to compare
```

**Configuration:**
```yaml
merge:
  module: merge.tgfr
  
  deduplication:
    strategy: hybrid
    
    fuzzy:
      algorithm: jaro_winkler
      threshold: 0.85
      
    semantic:
      embedding_model: text-embedding-3-small
      threshold: 0.90
      
    llm:
      provider: anthropic
      model: claude-3-haiku-20240307
      batch_size: 20
      
  conflict_resolution:
    strategy: highest_confidence
    auto_resolve_threshold: 0.9
    
  neo4j:
    uri: bolt://localhost:7687
    user: neo4j
    password: ${NEO4J_PASSWORD}
    database: kgl
    
    batch_size: 1000
    use_unwind: true                    # 2-3x performance gain
    
    # Index configuration (critical for performance)
    indexes:
      - label: Entity
        property: canonical_name
        type: unique
      - label: Entity
        properties: [type, name]
        type: composite
```

---

### L8: SYNTH — Answer Synthesis

**Purpose:** Generate final answer from knowledge graph with citations

**Validated Approach:** Hybrid template + LLM + GraphRAG
**Quality Target:** 85%+ relevance
**Achieved:** 94% user satisfaction (4.7/5)
**Citation Target:** 98%+ accuracy
**Achieved:** 96-97% citation accuracy
**Latency Target:** <2000ms
**Achieved:** 850-1050ms
**Cost:** $0.0004/query
**Confidence:** High

**Input Schema:**
```typescript
interface SynthInput {
  query: QueryOutput;
  merge_result: MergeOutput;
  
  kg_query: {
    // Cypher query results
    entities: any[];
    relationships: any[];
    paths: any[];
  };
  
  config: {
    style: "academic" | "conversational" | "technical" | "executive";
    
    format: {
      structure: "prose" | "bullet_points" | "numbered" | "qa";
      max_length: number;               // Tokens
      include_summary: boolean;
      include_details: boolean;
    };
    
    citations: {
      style: "inline" | "footnote" | "endnote";
      include_urls: boolean;
      max_citations_per_claim: number;
    };
    
    confidence: {
      include_scores: boolean;
      highlight_low_confidence: boolean;
      low_confidence_threshold: number;
    };
    
    llm: {
      provider: string;
      model: string;
      temperature: number;
    };
  };
}
```

**Output Schema:**
```typescript
interface SynthOutput {
  synthesis_id: string;
  
  answer: {
    summary: string;                    // 2-3 sentence overview
    body: string;                       // Full answer
    format: string;
    
    sections?: {
      title: string;
      content: string;
      confidence: number;
    }[];
  };
  
  citations: {
    citation_id: string;
    reference_number: number;           // [1], [2], etc.
    
    source: {
      title: string;
      url?: string;
      author?: string;
      date?: string;
      type: string;
    };
    
    claims_supported: string[];         // Which claims cite this
    relevance: number;
  }[];
  
  confidence: {
    overall: number;
    
    by_claim: {
      claim_id: string;
      claim_text: string;
      confidence: number;
      source_count: number;
      citation_ids: string[];
    }[];
    
    low_confidence_items: {
      item: string;
      confidence: number;
      reason: string;
    }[];
  };
  
  metadata: {
    query_coverage: number;
    entities_referenced: number;
    relationships_used: number;
    sources_cited: number;
    generation_time_ms: number;
  };
}
```

**Configuration:**
```yaml
synth:
  module: synth.hybrid
  
  style: conversational
  
  format:
    structure: prose
    max_length: 2000
    include_summary: true
    include_details: true
    
  citations:
    style: inline
    include_urls: true
    max_citations_per_claim: 3
    
  confidence:
    include_scores: true
    highlight_low_confidence: true
    low_confidence_threshold: 0.7
    
  llm:
    provider: anthropic
    model: claude-3-5-sonnet-20241022
    temperature: 0.3
    
  templates:
    comparison: "prompts/synth/comparison.md"
    explanation: "prompts/synth/explanation.md"
    how_to: "prompts/synth/how_to.md"
```

---

## Transform Specifications

### T1: Query → Gaps

**Purpose:** Add knowledge graph state to query for gap analysis

**Input:** `QueryOutput`
**Output:** `GapsInput`

**Logic:**
```python
def transform_query_to_gaps(query: QueryOutput, kg: KnowledgeGraph) -> GapsInput:
    # Match query entities against KG
    matched_entities = []
    for qe in query.entities:
        matches = kg.find_entities(
            name=qe.name,
            type=qe.type,
            threshold=0.7
        )
        for match in matches:
            matched_entities.append({
                "query_entity": qe.name,
                "kg_entity_id": match.id,
                "match_confidence": match.similarity,
                "last_updated": match.updated_at,
                "source_count": match.source_count
            })
    
    # Match query relations against KG
    matched_relations = []
    for qr in query.relations:
        matches = kg.find_relations(
            source_type=qr.source_type,
            target_type=qr.target_type,
            relation_type=qr.relation_type
        )
        # ... similar matching logic
    
    return GapsInput(
        query=query,
        kg_snapshot={
            "entity_count": kg.entity_count,
            "relationship_count": kg.relationship_count,
            "last_updated": kg.last_updated,
            "matched_entities": matched_entities,
            "matched_relations": matched_relations
        }
    )
```

**Configuration:**
```yaml
transform_t1:
  entity_match_threshold: 0.7
  relation_match_threshold: 0.6
  include_neighbor_context: true
  max_matches_per_entity: 5
```

---

### T2: Gaps → Search

**Purpose:** Convert gap analysis into search execution plan

**Input:** `GapsOutput`
**Output:** `SearchInput`

**Logic:**
```python
def transform_gaps_to_search(gaps: GapsOutput, config: PipelineConfig) -> SearchInput:
    # Build search priorities from gaps
    priorities = []
    for gap in gaps.gaps:
        priority = SearchPriority(
            gap_id=gap.id,
            queries=gap.suggested_queries,
            target_sources=select_sources_for_gap(gap, config),
            max_results=calculate_results_needed(gap),
            importance=gap.priority
        )
        priorities.append(priority)
    
    # Sort by priority
    priorities.sort(key=lambda p: -p.importance)
    
    # Select backends based on gap types
    backends = select_backends_for_gaps(gaps.gaps, config)
    
    return SearchInput(
        priorities=priorities[:config.search.max_parallel_queries],
        config={
            "backends": backends,
            "merge_strategy": config.search.merge_strategy,
            "max_results_per_backend": config.search.max_results,
            "source_routing": config.search.routing
        }
    )
```

**Configuration:**
```yaml
transform_t2:
  max_parallel_queries: 5
  min_gap_priority: 3                   # Ignore gaps below this priority
  source_selection:
    missing_entity: [tavily, meilisearch]
    stale_data: [tavily, arxiv]
    low_confidence: [arxiv, semantic_scholar]
    conflict: [arxiv, semantic_scholar]
```

---

### T3: Search → Ingest (Per Backend)

**Purpose:** Prepare search results for document ingestion

**Input:** `SearchResult[]` (from one backend)
**Output:** `IngestInput` (partial, one backend's contribution)

**Logic:**
```python
def transform_search_to_ingest(
    results: list[SearchResult],
    config: PipelineConfig
) -> IngestInput:
    # Filter by relevance
    filtered = [r for r in results if r.relevance_score >= config.ingest.min_relevance]
    
    # Deduplicate by URL
    seen_urls = set()
    deduped = []
    for r in filtered:
        if r.url and r.url not in seen_urls:
            seen_urls.add(r.url)
            deduped.append(r)
        elif not r.url:
            deduped.append(r)
    
    return IngestInput(
        documents=deduped,
        config={
            "chunking_strategy": config.ingest.chunking,
            "chunk_size": config.ingest.chunk_size,
            "chunk_overlap": config.ingest.overlap,
            "extract_tables": config.ingest.extract_tables,
            "extract_images": config.ingest.extract_images
        }
    )
```

**Configuration:**
```yaml
transform_t3:
  min_relevance: 0.3
  deduplicate_urls: true
  max_documents: 50
```

---

### MERGE: Search Result Merger

**Purpose:** Combine results from parallel search backends

**Input:** `SearchOutput[]` (from all backends)
**Output:** `SearchOutput` (merged)

**Logic:**
```python
def merge_search_results(
    backend_outputs: list[SearchOutput],
    strategy: str,
    k: int = 60
) -> SearchOutput:
    if strategy == "rrf":
        return rrf_merge(backend_outputs, k)
    elif strategy == "weighted":
        return weighted_merge(backend_outputs)
    elif strategy == "interleave":
        return interleave_merge(backend_outputs)
    elif strategy == "union":
        return union_merge(backend_outputs)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

def rrf_merge(outputs: list[SearchOutput], k: int) -> SearchOutput:
    scores = {}
    result_map = {}
    
    for output in outputs:
        for rank, result in enumerate(output.results):
            content_hash = hash_content(result.snippet)
            result_map[content_hash] = result
            scores[content_hash] = scores.get(content_hash, 0) + 1 / (k + rank + 1)
    
    sorted_ids = sorted(scores.keys(), key=lambda x: -scores[x])
    merged_results = [result_map[id] for id in sorted_ids]
    
    # Update merged scores
    for i, result in enumerate(merged_results):
        result.merged_score = scores[hash_content(result.snippet)]
    
    return SearchOutput(
        results=merged_results,
        backend_stats=aggregate_stats(outputs),
        merge_log=create_merge_log(outputs, merged_results)
    )
```

---

### T4: Ingest → Extract

**Purpose:** Prepare chunks for entity extraction

**Input:** `IngestOutput`
**Output:** `ExtractInput`

**Logic:**
```python
def transform_ingest_to_extract(
    ingest: IngestOutput,
    query: QueryOutput,
    config: PipelineConfig
) -> ExtractInput:
    # Derive entity types from query intent
    entity_types = derive_entity_types(query)
    
    # Filter chunks (skip very short or very long)
    valid_chunks = [
        c for c in ingest.chunks
        if config.extract.min_tokens <= c.token_count <= config.extract.max_tokens
    ]
    
    return ExtractInput(
        chunks=valid_chunks,
        config={
            "entity_types": entity_types,
            "use_ner": config.extract.use_ner,
            "use_llm": config.extract.use_llm,
            "llm_provider": config.extract.llm_provider,
            "confidence_threshold": config.extract.confidence_threshold
        }
    )

def derive_entity_types(query: QueryOutput) -> list[str]:
    """Map query intent to relevant entity types."""
    base_types = ["concept", "technology"]
    
    if query.intent.type == "comparison":
        return base_types + ["organization", "metric", "artifact"]
    elif query.intent.type == "how_to":
        return base_types + ["artifact", "person"]
    elif query.intent.type == "research":
        return base_types + ["person", "organization", "artifact", "event"]
    else:
        return base_types + ["person", "organization"]
```

---

### T5: Extract → Relate

**Purpose:** Prepare entities and chunks for relationship extraction

**Input:** `ExtractOutput` + `IngestOutput.chunks`
**Output:** `RelateInput`

**Logic:**
```python
def transform_extract_to_relate(
    extract: ExtractOutput,
    chunks: list[DocumentChunk],
    query: QueryOutput,
    config: PipelineConfig
) -> RelateInput:
    # Filter to non-duplicate entities
    active_entities = [e for e in extract.entities if not e.is_duplicate]
    
    # Derive relationship types from query
    relation_types = derive_relation_types(query)
    
    return RelateInput(
        entities=active_entities,
        chunks=chunks,
        config={
            "relationship_types": relation_types,
            "use_dependency_parsing": config.relate.use_parsing,
            "use_llm": config.relate.use_llm,
            "cross_sentence": config.relate.cross_sentence
        }
    )

def derive_relation_types(query: QueryOutput) -> list[str]:
    """Map query intent to relevant relationship types."""
    base_relations = ["is_a", "related_to"]
    
    if query.intent.type == "comparison":
        return base_relations + ["competes_with", "uses", "part_of"]
    elif query.intent.type == "how_to":
        return base_relations + ["uses", "part_of", "created_by"]
    else:
        return base_relations + ["created_by", "uses", "part_of"]
```

---

### T6: Relate → Merge

**Purpose:** Package extraction results for knowledge graph merge

**Input:** `ExtractOutput` + `RelateOutput`
**Output:** `MergeInput`

**Logic:**
```python
def transform_relate_to_merge(
    extract: ExtractOutput,
    relate: RelateOutput,
    config: PipelineConfig
) -> MergeInput:
    # Filter entities: only non-duplicates with sufficient confidence
    valid_entities = [
        e for e in extract.entities
        if not e.is_duplicate and e.confidence >= config.merge.min_confidence
    ]
    
    # Filter relationships: only those with valid endpoints
    valid_entity_ids = {e.entity_id for e in valid_entities}
    valid_relationships = [
        r for r in relate.relationships
        if (r.source_entity_id in valid_entity_ids and
            r.target_entity_id in valid_entity_ids and
            r.confidence >= config.merge.min_confidence)
    ]
    
    return MergeInput(
        new_entities=valid_entities,
        new_relationships=valid_relationships,
        config={
            "dedup_strategy": config.merge.dedup_strategy,
            "confidence_threshold": config.merge.confidence_threshold,
            "conflict_resolution": config.merge.conflict_resolution
        }
    )
```

---

## Mixin Specifications

### M1: Tracing Mixin

**Purpose:** Distributed tracing for observability

**Applies to:** All stages

**Interface:**
```typescript
interface TracingMixin {
  // Called before stage execution
  onStageStart(context: {
    stage_name: string;
    stage_id: string;
    run_id: string;
    iteration: number;
    input_summary: object;
  }): TraceSpan;
  
  // Called after successful execution
  onStageEnd(span: TraceSpan, context: {
    output_summary: object;
    duration_ms: number;
  }): void;
  
  // Called on error
  onStageError(span: TraceSpan, error: Error): void;
  
  // Called for sub-operations within stage
  onSubOperation(span: TraceSpan, operation: string): TraceSpan;
}

interface TraceSpan {
  trace_id: string;
  span_id: string;
  parent_span_id?: string;
  start_time: string;
  end_time?: string;
  status: "running" | "success" | "error";
  tags: Record<string, string>;
  logs: { timestamp: string; message: string }[];
}
```

**Configuration:**
```yaml
mixin_tracing:
  enabled: true
  
  export:
    backend: jaeger                     # jaeger | zipkin | otlp | console
    endpoint: http://localhost:14268/api/traces
    
  sampling:
    strategy: always                    # always | probabilistic | rate_limiting
    rate: 1.0                          # For probabilistic
    
  tags:
    service: kgl-pipeline
    environment: development
```

---

### M2: Cost Mixin

**Purpose:** Track and control costs across pipeline

**Applies to:** All stages

**Interface:**
```typescript
interface CostMixin {
  // Estimate cost before execution
  estimateCost(stage: string, input: any): CostEstimate;
  
  // Record actual cost after execution
  recordCost(stage: string, cost: CostBreakdown): void;
  
  // Check budget status
  checkBudget(): BudgetStatus;
  
  // Get cost report
  getCostReport(): CostReport;
}

interface CostEstimate {
  estimated_usd: number;
  confidence: number;                   // How confident in estimate
  breakdown: {
    llm_cost: number;
    api_cost: number;
    compute_cost: number;
  };
}

interface CostBreakdown {
  stage: string;
  timestamp: string;
  
  llm: {
    provider: string;
    model: string;
    input_tokens: number;
    output_tokens: number;
    cost_usd: number;
  }[];
  
  api_calls: {
    service: string;
    calls: number;
    cost_usd: number;
  }[];
  
  compute: {
    cpu_seconds: number;
    gpu_seconds: number;
    cost_usd: number;
  };
  
  total_usd: number;
}

interface BudgetStatus {
  budget_usd: number;
  spent_usd: number;
  remaining_usd: number;
  percentage_used: number;
  exceeded: boolean;
  projected_total: number;              // Based on current trajectory
}
```

**Configuration:**
```yaml
mixin_cost:
  enabled: true
  
  budget:
    per_query_usd: 0.10
    per_iteration_usd: 0.05
    total_run_usd: 1.00
    
  alerts:
    warn_at_percentage: 80
    stop_at_percentage: 100
    
  tracking:
    log_all_costs: true
    aggregate_interval: 1m
    
  pricing:                              # Override default pricing
    anthropic:
      claude-3-5-sonnet-20241022:
        input_per_1m: 3.00
        output_per_1m: 15.00
    deepseek:
      deepseek-chat:
        input_per_1m: 0.14
        output_per_1m: 0.28
```

---

### M3: Cache Mixin

**Purpose:** Reduce redundant computation and API calls

**Applies to:** SEARCH, EXTRACT, SYNTH

**Interface:**
```typescript
interface CacheMixin {
  // Try to get cached result
  get<T>(key: string): CacheResult<T> | null;
  
  // Store result in cache
  set<T>(key: string, value: T, options?: CacheOptions): void;
  
  // Invalidate cache entries
  invalidate(pattern: string): number;
  
  // Semantic cache: find similar cached queries
  findSimilar(query: string, threshold: number): SimilarCacheHit[];
}

interface CacheResult<T> {
  value: T;
  cached_at: string;
  ttl_remaining_seconds: number;
  hit_count: number;
}

interface CacheOptions {
  ttl_seconds?: number;
  tags?: string[];
  semantic_key?: string;                // For semantic cache lookup
}

interface SimilarCacheHit {
  key: string;
  similarity: number;
  value: any;
}
```

**ROI Note:** Semantic caching provides 872% ROI per research.

**Configuration:**
```yaml
mixin_cache:
  enabled: true
  
  backend: redis                        # redis | memory | disk
  redis:
    host: localhost
    port: 6379
    db: 0
    
  default_ttl_seconds: 3600            # 1 hour
  max_memory_mb: 1024
  
  semantic:
    enabled: true
    embedding_model: text-embedding-3-small
    similarity_threshold: 0.92
    
  per_stage:
    search:
      enabled: true
      ttl_seconds: 7200                # 2 hours
    extract:
      enabled: true
      ttl_seconds: 86400               # 24 hours
    synth:
      enabled: true
      ttl_seconds: 3600
```

---

### M4: Rate Limit Mixin

**Purpose:** Prevent API throttling and manage quotas

**Applies to:** SEARCH, EXTRACT, RELATE, SYNTH

**Interface:**
```typescript
interface RateLimitMixin {
  // Check if operation is allowed
  checkLimit(resource: string): RateLimitStatus;
  
  // Record usage
  recordUsage(resource: string, units: number): void;
  
  // Wait until limit clears (blocking)
  waitForLimit(resource: string): Promise<void>;
  
  // Get current status for all resources
  getStatus(): Record<string, RateLimitStatus>;
}

interface RateLimitStatus {
  resource: string;
  allowed: boolean;
  remaining: number;
  limit: number;
  reset_at: string;
  wait_ms?: number;                     // If not allowed, how long to wait
}
```

**Configuration:**
```yaml
mixin_rate_limit:
  enabled: true
  
  strategy: token_bucket               # token_bucket | sliding_window | fixed_window
  
  limits:
    anthropic:
      requests_per_minute: 50
      tokens_per_minute: 100000
      
    deepseek:
      requests_per_minute: 60
      tokens_per_minute: 200000
      
    tavily:
      requests_per_minute: 100
      requests_per_day: 1000
      
    openai:
      requests_per_minute: 60
      tokens_per_minute: 150000
      
  behavior:
    on_limit: wait                     # wait | error | fallback
    max_wait_seconds: 60
    fallback_provider: null
```

---

### M5: Retry Mixin

**Purpose:** Handle transient failures with exponential backoff

**Applies to:** All stages with external calls

**Interface:**
```typescript
interface RetryMixin {
  // Wrap an operation with retry logic
  withRetry<T>(
    operation: () => Promise<T>,
    options?: RetryOptions
  ): Promise<T>;
  
  // Check if error is retryable
  isRetryable(error: Error): boolean;
  
  // Get fallback for stage
  getFallback(stage: string): StageModule | null;
}

interface RetryOptions {
  max_attempts?: number;
  backoff?: "exponential" | "linear" | "constant";
  initial_delay_ms?: number;
  max_delay_ms?: number;
  retryable_errors?: string[];
}
```

**Configuration:**
```yaml
mixin_retry:
  enabled: true
  
  default:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 1000
    max_delay_ms: 30000
    jitter: true
    
  retryable_errors:
    - "RateLimitError"
    - "TimeoutError"
    - "ServiceUnavailable"
    - "ConnectionError"
    
  non_retryable_errors:
    - "AuthenticationError"
    - "InvalidInput"
    - "NotFound"
    
  fallbacks:
    search.tavily: search.exa
    extract.deepseek: extract.claude
    synth.claude: synth.gpt4
```

---

### M6: Snapshot Mixin

**Purpose:** Enable reproducibility and debugging through state capture

**Applies to:** All stages

**Interface:**
```typescript
interface SnapshotMixin {
  // Capture state before/after stage
  capture(context: {
    stage: string;
    run_id: string;
    iteration: number;
    input: any;
    output: any;
    config: any;
    metrics: any;
  }): Snapshot;
  
  // Restore from snapshot
  restore(snapshot_id: string): Snapshot;
  
  // Compare two snapshots
  diff(snapshot_a: string, snapshot_b: string): SnapshotDiff;
  
  // List snapshots for a run
  list(run_id: string): SnapshotSummary[];
}

interface Snapshot {
  snapshot_id: string;
  run_id: string;
  stage: string;
  iteration: number;
  created_at: string;
  
  input_hash: string;
  output_hash: string;
  config_hash: string;
  
  input: any;
  output: any;
  config: any;
  
  metrics: {
    duration_ms: number;
    cost_usd: number;
    tokens_used: number;
  };
}

interface SnapshotDiff {
  input_diff: JsonDiff;
  output_diff: JsonDiff;
  config_diff: JsonDiff;
  metrics_diff: {
    duration_delta_ms: number;
    cost_delta_usd: number;
  };
}
```

**Configuration:**
```yaml
mixin_snapshot:
  enabled: true
  
  storage:
    backend: postgresql                # postgresql | s3 | filesystem
    connection: ${DATABASE_URL}
    table: pipeline_snapshots
    
  capture:
    on_success: true
    on_error: true
    include_full_input: true
    include_full_output: true
    max_payload_size_mb: 10
    
  retention:
    keep_days: 30
    keep_last_n: 100
    archive_to_s3: true
```

---

## Reasoning Engine Specification

### State Machine

```
                         ┌────────────────────────────────┐
                         │                                │
                         ▼                                │
┌──────────┐      ┌──────────────┐      ┌──────────┐     │
│  START   │─────▶│   EVALUATE   │─────▶│  DECIDE  │─────┤
└──────────┘      └──────────────┘      └──────────┘     │
                         ▲                    │          │
                         │                    │          │
                         │              ┌─────┴─────┐    │
                         │              ▼           ▼    │
                         │         ┌────────┐  ┌────────┐│
                         │         │CONTINUE│  │ OUTPUT ││
                         │         └────┬───┘  └────────┘│
                         │              │                 │
                         └──────────────┘                 │
                                                          │
                                        ┌────────┐        │
                                        │  ASK   │────────┘
                                        │ HUMAN  │
                                        └────────┘
```

### Evaluation Function

```python
def evaluate(state: ReasoningState) -> EvaluationResult:
    """Evaluate current state against convergence criteria."""
    
    # Calculate confidence (weighted average of claim confidences)
    claim_confidences = [c.confidence for c in state.claims]
    weights = [c.importance for c in state.claims]
    confidence = weighted_average(claim_confidences, weights)
    
    # Calculate coverage (addressed subtopics / total subtopics)
    total_subtopics = len(state.query.expected_subtopics)
    addressed = len([s for s in state.subtopics if s.addressed])
    coverage = addressed / total_subtopics if total_subtopics > 0 else 1.0
    
    # Check diminishing returns (new info in last 2 iterations)
    if len(state.iteration_history) >= 2:
        last_two = state.iteration_history[-2:]
        new_info = sum(i.new_entities + i.new_relations for i in last_two)
        total_info = state.total_entities + state.total_relations
        diminishing = (new_info / total_info) < 0.05 if total_info > 0 else True
    else:
        diminishing = False
    
    return EvaluationResult(
        confidence=confidence,
        coverage=coverage,
        diminishing_returns=diminishing,
        iteration_count=state.iteration,
        cost_spent=state.total_cost,
        
        gaps=detect_gaps(state),
        conflicts=detect_conflicts(state),
        
        convergence_criteria={
            "confidence_met": confidence >= 0.85,
            "coverage_met": coverage >= 0.90,
            "diminishing_returns": diminishing,
            "max_iterations": state.iteration >= state.max_iterations,
            "budget_exhausted": state.total_cost >= state.budget,
        }
    )
```

### Decision Function

```python
def decide(evaluation: EvaluationResult) -> Decision:
    """Decide next action based on evaluation."""
    
    # Check if any convergence criterion is met
    criteria = evaluation.convergence_criteria
    
    if criteria["budget_exhausted"]:
        return Decision(
            action="OUTPUT",
            reason="Budget exhausted",
            force_output=True
        )
    
    if criteria["max_iterations"]:
        return Decision(
            action="OUTPUT",
            reason="Maximum iterations reached",
            force_output=True
        )
    
    if criteria["confidence_met"] and criteria["coverage_met"]:
        return Decision(
            action="OUTPUT",
            reason="Confidence and coverage thresholds met",
            force_output=False
        )
    
    if criteria["diminishing_returns"]:
        return Decision(
            action="OUTPUT",
            reason="Diminishing returns detected",
            force_output=False
        )
    
    # Check if human input needed
    if len(evaluation.conflicts) > 3:
        return Decision(
            action="ASK_HUMAN",
            reason=f"{len(evaluation.conflicts)} unresolved conflicts",
            conflicts=evaluation.conflicts
        )
    
    # Continue searching
    refined_query = refine_query(evaluation.gaps)
    return Decision(
        action="CONTINUE",
        reason=f"{len(evaluation.gaps)} gaps remaining",
        refined_query=refined_query,
        priority_gaps=evaluation.gaps[:5]
    )
```

### Convergence Criteria (Validated)

| Criterion | Threshold | Measurement |
|-----------|-----------|-------------|
| Confidence | ≥ 85% | Weighted average of claim confidences |
| Coverage | ≥ 90% | Subtopics addressed / total subtopics |
| Diminishing Returns | <5% new info for 2 iterations | (new entities + relations) / total |
| Max Iterations | 10 (configurable) | Simple counter |
| Budget | Configurable | Total cost in USD |
| User Interrupt | Manual | Flag set by user |

---

## Parallel Execution Model

### Fork-Join Pattern for Search

```
                    T2 (Gaps→Search)
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
         ┌────────┐  ┌────────┐  ┌────────┐
         │search:1│  │search:2│  │search:3│
         │meili   │  │qdrant  │  │tavily  │
         └────┬───┘  └────┬───┘  └────┬───┘
              │           │           │
              ▼           ▼           ▼
         ┌────────┐  ┌────────┐  ┌────────┐
         │  T3a   │  │  T3b   │  │  T3c   │
         └────┬───┘  └────┬───┘  └────┬───┘
              │           │           │
              └───────────┼───────────┘
                          │
                          ▼
                     ┌─────────┐
                     │  MERGE  │
                     └────┬────┘
                          │
                          ▼
                       INGEST
```

### Execution Semantics

**Fork:** T2 dispatches search requests to all enabled backends simultaneously

**Parallel execution:** Each backend runs independently with its own:
- Timeout
- Rate limiting
- Retry logic
- Error handling

**Join:** MERGE node waits according to strategy:
- `wait_for_all`: Wait until all backends respond or timeout
- `wait_for_n`: Wait until N backends respond
- `first_response`: Return as soon as any backend responds

**Failure handling:**
- If backend fails, mark as `status: error` in stats
- Continue if `min_backends_required` still met
- Fail entire search if below minimum

### UI Representation of Parallel Execution

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PARALLEL SEARCH EXECUTION                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ meilisearch │  │   qdrant    │  │   tavily    │  │    arxiv    │     │
│  │  ✓ 245ms    │  │  ✓ 189ms    │  │  ⏳ 1.2s    │  │  ✓ 456ms    │     │
│  │  32 results │  │  28 results │  │  pending    │  │  15 results │     │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                                          │
│  Strategy: RRF (k=60)  │  Min backends: 2  │  Timeout: 3000ms           │
│  Status: 3/4 complete, waiting for tavily                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## User-Editable Flow Configuration

### Flow Definition Format

```yaml
# User can create custom flows by combining stages
flow:
  name: "Deep Academic Research"
  description: "Prioritizes academic sources with thorough extraction"
  
  stages:
    - id: query
      module: query.hybrid
      enabled: true
      
    - id: gaps
      module: gaps.hybrid
      enabled: true
      
    - id: search
      parallel: true
      branches:
        - id: search_academic
          module: search.arxiv
          weight: 1.0
        - id: search_scholar
          module: search.semantic_scholar
          weight: 0.9
        - id: search_local
          module: search.meilisearch
          weight: 0.5
      merge_strategy: weighted
      
    - id: ingest
      module: ingest.docling
      enabled: true
      
    - id: extract
      module: extract.hybrid
      enabled: true
      config:
        use_llm: true
        llm_provider: deepseek
        
    - id: relate
      module: relate.hybrid
      enabled: true
      
    - id: merge
      module: merge.tgfr
      enabled: true
      
    - id: synth
      module: synth.hybrid
      enabled: true
      config:
        style: academic
        
  # Per-stage mixin overrides
  mixins:
    search_academic:
      cache:
        enabled: true
        ttl_seconds: 86400              # Cache academic results longer
    extract:
      cost:
        per_stage_budget_usd: 0.05      # Limit extraction cost
```

### Flow Editor UI

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  FLOW EDITOR: Deep Academic Research                           [Save] [Run] │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STAGES (drag to reorder)                    AVAILABLE MODULES              │
│  ─────────────────────────                   ─────────────────               │
│  ┌────────────────────────┐                  Search:                         │
│  │ ☰ QUERY    [hybrid ▾] │                  • meilisearch                   │
│  └────────────────────────┘                  • qdrant                        │
│           │                                  • tavily                        │
│           ▼                                  • arxiv ✓                       │
│  ┌────────────────────────┐                  • semantic_scholar ✓            │
│  │ ☰ GAPS     [hybrid ▾] │                  • github                        │
│  └────────────────────────┘                                                  │
│           │                                  Extract:                        │
│           ▼                                  • spacy                         │
│  ┌────────────────────────┐                  • deepseek ✓                    │
│  │ ☰ SEARCH   [parallel] │                  • claude                        │
│  │   ├─ arxiv      w:1.0 │                  • hybrid ✓                      │
│  │   ├─ scholar    w:0.9 │                                                  │
│  │   └─ meili      w:0.5 │                  [+ Add Branch]                  │
│  │   Merge: weighted     │                                                  │
│  └────────────────────────┘                                                  │
│           │                                                                  │
│           ▼                                                                  │
│  ┌────────────────────────┐                  MIXINS (per stage)              │
│  │ ☰ INGEST  [docling ▾] │                  ─────────────────               │
│  └────────────────────────┘                  [✓] Tracing                     │
│           │                                  [✓] Cost Tracking               │
│           ▼                                  [✓] Caching                     │
│         ...                                  [✓] Rate Limiting               │
│                                              [✓] Retry                       │
│                                              [✓] Snapshot                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Complete Configuration Reference

```yaml
# Complete pipeline configuration
pipeline:
  name: "KGL Default Pipeline"
  version: "1.0.0"
  
  # Reasoning engine settings
  reasoning:
    max_iterations: 10
    confidence_threshold: 0.85
    coverage_threshold: 0.90
    diminishing_returns_threshold: 0.05
    diminishing_returns_iterations: 2
    budget_usd: 1.00
    human_interrupt_enabled: true
    
  # Stage configurations (see individual stage specs above)
  stages:
    query:
      module: query.hybrid
      # ... full config
    gaps:
      module: gaps.hybrid
      # ... full config
    search:
      parallel: true
      # ... full config
    ingest:
      module: ingest.hybrid
      # ... full config
    extract:
      module: extract.hybrid
      # ... full config
    relate:
      module: relate.hybrid
      # ... full config
    merge:
      module: merge.tgfr
      # ... full config
    synth:
      module: synth.hybrid
      # ... full config
      
  # Transform configurations
  transforms:
    t1:
      entity_match_threshold: 0.7
    t2:
      max_parallel_queries: 5
    t3:
      min_relevance: 0.3
    t4:
      # passthrough with config injection
    t5:
      # passthrough with config injection
    t6:
      min_confidence_for_merge: 0.7
      
  # Mixin configurations (global defaults, can override per-stage)
  mixins:
    tracing:
      enabled: true
      # ... full config
    cost:
      enabled: true
      # ... full config
    cache:
      enabled: true
      # ... full config
    rate_limit:
      enabled: true
      # ... full config
    retry:
      enabled: true
      # ... full config
    snapshot:
      enabled: true
      # ... full config
      
  # Execution settings
  execution:
    parallel_backends: true
    wait_strategy: wait_for_all
    min_backends_required: 2
    global_timeout_ms: 30000
    
  # Storage settings
  storage:
    neo4j:
      uri: bolt://localhost:7687
      database: kgl
    postgresql:
      uri: postgresql://localhost/kgl
    redis:
      uri: redis://localhost:6379
```

---

## Related Documents

- [Research Synthesis](../../research/ai-pipeline/RESEARCH-SYNTHESIS.md) — Validated metrics and recommendations
- [Architecture Principles](../foundation/01-ARCHITECTURE-PRINCIPLES.md) — Two-loop design
- [Data Flow](./02-DATA-FLOW.md) — Feedback loop patterns
- [Sprint Plan](./04-SPRINT-PLAN.md) — Implementation timeline
