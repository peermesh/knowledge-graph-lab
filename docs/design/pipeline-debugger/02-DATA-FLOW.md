# KGL Pipeline Debugger: Data Flow & Feedback Loops

**Version:** 0.1.0-draft
**Created:** 2026-01-09
**Parent:** [00-VISION.md](./00-VISION.md)

---

## Complete System Flow

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              USER INTERFACE                                    ║
║                                                                                ║
║   [Query Input]  [Pipeline View]  [Inspector]  [Config]  [Controls]           ║
╚════════════════════════════════════╤══════════════════════════════════════════╝
                                     │
                        WebSocket ◄──┴──► REST API
                                     │
╔════════════════════════════════════╧══════════════════════════════════════════╗
║                           ORCHESTRATION LAYER                                  ║
║                                                                                ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                         RUN CONTROLLER                                   │ ║
║   │                                                                          │ ║
║   │   • Manages run lifecycle (create → start → pause → complete)           │ ║
║   │   • Enforces breakpoints                                                 │ ║
║   │   • Emits events to UI                                                   │ ║
║   │   • Handles config hot-swap                                              │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                     │                                          ║
║                                     ▼                                          ║
║   ┌─────────────────────────────────────────────────────────────────────────┐ ║
║   │                         REASONING ENGINE                                 │ ║
║   │                                                                          │ ║
║   │   Inputs:                        Outputs:                                │ ║
║   │   • Original query               • Next action (CONTINUE/OUTPUT/ASK)    │ ║
║   │   • Current knowledge state      • Refined query (if continuing)        │ ║
║   │   • Gap analysis                 • Synthesis (if outputting)            │ ║
║   │   • Iteration count              • Question (if asking)                 │ ║
║   │   • Cost accumulator                                                     │ ║
║   │                                                                          │ ║
║   │   ┌─────────────────────────────────────────────────────────────┐       │ ║
║   │   │              DECISION FUNCTIONS                              │       │ ║
║   │   │                                                              │       │ ║
║   │   │   detect_gaps()      → What's missing?                       │       │ ║
║   │   │   assess_confidence()→ How certain are we?                   │       │ ║
║   │   │   check_convergence()→ Are we done?                          │       │ ║
║   │   │   resolve_conflicts()→ Contradictions found?                 │       │ ║
║   │   │   plan_next_query()  → What to search next?                  │       │ ║
║   │   └─────────────────────────────────────────────────────────────┘       │ ║
║   └─────────────────────────────────────────────────────────────────────────┘ ║
║                                     │                                          ║
╚═════════════════════════════════════╪══════════════════════════════════════════╝
                                      │
                                      ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║                          PROCESSING PIPELINE                                   ║
║                                                                                ║
║   ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐       ║
║   │QUERY │───▶│SEARCH│───▶│INGEST│───▶│EXTRACT───▶│MERGE │───▶│STORE │       ║
║   │      │    │      │    │      │    │      │    │      │    │      │       ║
║   │Parse │    │Multi │    │Parse │    │Entity│    │Dedup │    │Graph │       ║
║   │Intent│    │Backend    │Docs  │    │Relation   │Resolve    │Update│       ║
║   │      │    │Merge │    │Chunk │    │Claims│    │Merge │    │      │       ║
║   └──────┘    └──────┘    └──────┘    └──────┘    └──────┘    └──────┘       ║
║       │           │           │           │           │           │           ║
║       ▼           ▼           ▼           ▼           ▼           ▼           ║
║   ┌──────────────────────────────────────────────────────────────────────┐   ║
║   │                        SNAPSHOT CAPTURE                               │   ║
║   │                                                                       │   ║
║   │   Every stage captures: input_hash, output_hash, config, metrics     │   ║
║   │   Stored in: /runs/{run_id}/snapshots/{stage}_{iteration}.json       │   ║
║   └──────────────────────────────────────────────────────────────────────┘   ║
║                                                                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
                                      │
                                      ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║                            DATA LAYER                                          ║
║                                                                                ║
║   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                  ║
║   │   PostgreSQL   │  │     Redis      │  │     Neo4j      │                  ║
║   │                │  │                │  │                │                  ║
║   │  • Run state   │  │  • Events      │  │  • Knowledge   │                  ║
║   │  • Configs     │  │  • Cache       │  │    Graph       │                  ║
║   │  • Snapshots   │  │  • Pub/Sub     │  │  • Entities    │                  ║
║   │    metadata    │  │                │  │  • Relations   │                  ║
║   └────────────────┘  └────────────────┘  └────────────────┘                  ║
║                                                                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## Feedback Loop Detail

### The Outer Loop (Reasoning)

This is the "infinite feedback" loop that continues until convergence:

```
                              ┌────────────────────────────────────┐
                              │                                    │
                              │         USER QUERY                 │
                              │   "Best OSS vector DBs for RAG"    │
                              │                                    │
                              └─────────────────┬──────────────────┘
                                                │
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│   ITERATION 1                                                                    │
│   ═══════════                                                                    │
│                                                                                  │
│   ┌──────────────┐                                                               │
│   │   REASON     │  Intent: comparison query                                     │
│   │              │  Expected: products, benchmarks, use cases                    │
│   │   Gaps: ALL  │  Query: "open source vector database comparison"              │
│   └──────┬───────┘                                                               │
│          │                                                                       │
│          ▼                                                                       │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │  PIPELINE: Search → Ingest → Extract → Merge → Store                      │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│          │                                                                       │
│          ▼                                                                       │
│   ┌──────────────┐                                                               │
│   │   EVALUATE   │  Found: Qdrant, Weaviate, Milvus, Chroma, pgvector           │
│   │              │  Confidence: 45% (only product names, no benchmarks)         │
│   │  Gaps: 3     │  Missing: performance data, cost comparison, scale limits    │
│   └──────┬───────┘                                                               │
│          │                                                                       │
│          ▼                                                                       │
│   Decision: CONTINUE (confidence < 85%, gaps remain)                             │
│   Next query: "vector database benchmark performance million vectors"            │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                │ LOOP BACK
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│   ITERATION 2                                                                    │
│   ═══════════                                                                    │
│                                                                                  │
│   ┌──────────────┐                                                               │
│   │   REASON     │  Previous: 5 products identified                             │
│   │              │  Gap focus: benchmark data                                    │
│   │   Gaps: 3    │  Query: "vector database benchmark million vectors QPS"      │
│   └──────┬───────┘                                                               │
│          │                                                                       │
│          ▼                                                                       │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │  PIPELINE: Search → Ingest → Extract → Merge → Store                      │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│          │                                                                       │
│          ▼                                                                       │
│   ┌──────────────┐                                                               │
│   │   EVALUATE   │  Found: VectorDBBench results, Qdrant benchmarks             │
│   │              │  Confidence: 68% (have benchmarks, missing cost data)        │
│   │  Gaps: 1     │  Missing: pricing comparison at scale                        │
│   └──────┬───────┘                                                               │
│          │                                                                       │
│          ▼                                                                       │
│   Decision: CONTINUE (confidence < 85%, gap remains)                             │
│   Next query: "vector database pricing cost comparison enterprise"               │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                │ LOOP BACK
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│   ITERATION 3                                                                    │
│   ═══════════                                                                    │
│                                                                                  │
│   ┌──────────────┐                                                               │
│   │   REASON     │  Previous: benchmarks added                                   │
│   │              │  Gap focus: cost data                                         │
│   │   Gaps: 1    │  Query: "qdrant weaviate milvus pricing enterprise"          │
│   └──────┬───────┘                                                               │
│          │                                                                       │
│          ▼                                                                       │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │  PIPELINE: Search → Ingest → Extract → Merge → Store                      │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│          │                                                                       │
│          ▼                                                                       │
│   ┌──────────────┐                                                               │
│   │   EVALUATE   │  Found: Pricing pages, cloud costs, self-hosted estimates    │
│   │              │  Confidence: 87% (all expected data present)                 │
│   │  Gaps: 0     │  Coverage: 95% of subtopics addressed                        │
│   └──────┬───────┘                                                               │
│          │                                                                       │
│          ▼                                                                       │
│   Decision: OUTPUT (confidence ≥ 85%, no gaps)                                   │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                │ EXIT LOOP
                                                ▼
                              ┌────────────────────────────────────┐
                              │                                    │
                              │       SYNTHESIZE OUTPUT            │
                              │                                    │
                              │  • Comparison table                │
                              │  • Benchmark data                  │
                              │  • Pricing analysis                │
                              │  • Recommendations                 │
                              │  • Source citations                │
                              │                                    │
                              └────────────────────────────────────┘
```

---

## Feedback Loop Types

### Type 1: Expansion Loop

**Trigger:** Entity discovered that requires more context

```
┌──────────┐        ┌──────────┐        ┌──────────┐
│ EXTRACT  │───────▶│  REASON  │───────▶│  SEARCH  │
│          │        │          │        │          │
│ Found:   │        │ Gap:     │        │ Query:   │
│ "HNSW"   │        │ "What is │        │ "HNSW    │
│          │        │  HNSW?"  │        │  algorithm│
└──────────┘        └──────────┘        │  vector" │
                                        └──────────┘
                                              │
                                              ▼
                                        [Full pipeline]
```

### Type 2: Verification Loop

**Trigger:** Single-source claim needs corroboration

```
┌──────────┐        ┌──────────┐        ┌──────────┐
│  MERGE   │───────▶│  REASON  │───────▶│  SEARCH  │
│          │        │          │        │          │
│ Claim:   │        │ Gap:     │        │ Query:   │
│ "Qdrant  │        │ Single   │        │ "Qdrant  │
│ 10x      │        │ source   │        │ benchmark│
│ faster"  │        │ only     │        │ comparison
└──────────┘        └──────────┘        │ milvus"  │
                                        └──────────┘
                                              │
                                              ▼
                                        [Full pipeline]
```

### Type 3: Conflict Resolution Loop

**Trigger:** Contradictory claims from different sources

```
┌──────────┐        ┌──────────┐        ┌──────────┐
│  MERGE   │───────▶│  REASON  │───────▶│  SEARCH  │
│          │        │          │        │          │
│ Conflict:│        │ Need:    │        │ Query:   │
│ A: "100K │        │ Authori- │        │ "Qdrant  │
│    QPS"  │        │ tative   │        │ official │
│ B: "50K  │        │ source   │        │ benchmark│
│    QPS"  │        │          │        │  QPS"    │
└──────────┘        └──────────┘        └──────────┘
                                              │
                                              ▼
                                        [Full pipeline]
                                              │
                                              ▼
                                        ┌──────────┐
                                        │  MERGE   │
                                        │          │
                                        │ Resolve: │
                                        │ "100K QPS│
                                        │ (official│
                                        │ source)" │
                                        └──────────┘
```

### Type 4: Refinement Loop

**Trigger:** Results too broad or too narrow

```
┌──────────┐        ┌──────────┐        ┌──────────┐
│  SEARCH  │───────▶│  REASON  │───────▶│  QUERY   │
│          │        │          │        │          │
│ Results: │        │ Too      │        │ Refined: │
│ 10,000   │        │ broad    │        │ +filter: │
│ docs     │        │          │        │ "2024"   │
│          │        │          │        │ +limit:  │
└──────────┘        └──────────┘        │ "RAG"    │
                                        └──────────┘
                                              │
                                              ▼
                                        ┌──────────┐
                                        │  SEARCH  │
                                        │          │
                                        │ Results: │
                                        │ 47 docs  │
                                        │ (focused)│
                                        └──────────┘
```

---

## Convergence Criteria (Exit Conditions)

The reasoning loop exits when ANY of these conditions are met:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CONVERGENCE CHECK                                    │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ CHECK 1: CONFIDENCE THRESHOLD                                        │   │
│   │                                                                      │   │
│   │   confidence = weighted_avg(claim_confidences)                       │   │
│   │   IF confidence >= 0.85: EXIT with OUTPUT                            │   │
│   │                                                                      │   │
│   │   Confidence factors:                                                │   │
│   │   • Source count per claim (more = higher)                          │   │
│   │   • Source authority (official > blog > forum)                      │   │
│   │   • Recency (newer = higher for volatile topics)                    │   │
│   │   • Consistency (agreeing sources = higher)                         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ CHECK 2: COVERAGE THRESHOLD                                          │   │
│   │                                                                      │   │
│   │   coverage = addressed_subtopics / total_subtopics                  │   │
│   │   IF coverage >= 0.90: EXIT with OUTPUT                              │   │
│   │                                                                      │   │
│   │   Subtopics derived from query intent:                              │   │
│   │   • "comparison" → need: products, benchmarks, pros/cons            │   │
│   │   • "how to" → need: steps, prerequisites, examples                 │   │
│   │   • "what is" → need: definition, uses, alternatives                │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ CHECK 3: DIMINISHING RETURNS                                         │   │
│   │                                                                      │   │
│   │   info_gain = new_entities + new_relations + resolved_gaps          │   │
│   │   IF last_2_iterations_gain < 5%: EXIT with OUTPUT                   │   │
│   │                                                                      │   │
│   │   "We're not learning anything new"                                 │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ CHECK 4: RESOURCE LIMITS                                             │   │
│   │                                                                      │   │
│   │   IF iteration >= max_iterations (default: 10): EXIT with OUTPUT     │   │
│   │   IF cost >= cost_limit: EXIT with OUTPUT (best effort)              │   │
│   │   IF time >= time_limit: EXIT with OUTPUT (best effort)              │   │
│   │                                                                      │   │
│   │   "Stop even if not perfect"                                        │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ CHECK 5: NO GAPS REMAINING                                           │   │
│   │                                                                      │   │
│   │   IF gaps.length == 0: EXIT with OUTPUT                              │   │
│   │                                                                      │   │
│   │   "Nothing left to search for"                                      │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ CHECK 6: USER INTERRUPT                                              │   │
│   │                                                                      │   │
│   │   IF user_pressed_stop: EXIT with OUTPUT (current state)             │   │
│   │                                                                      │   │
│   │   "User said stop"                                                  │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Stage-Level Data Flow

### QUERY Stage

```
INPUT                          PROCESS                         OUTPUT
─────                          ───────                         ──────

{                              ┌─────────────────────┐         {
  query: "Best OSS             │                     │           intent: {
    vector DBs                 │  1. Parse query     │             type: "comparison",
    for RAG"                   │  2. Detect intent   │             entities: ["vector_db", "RAG"],
}                              │  3. Extract         │             modifiers: ["best", "OSS"]
                               │     constraints     │           },
                               │  4. Identify        │           subtopics: [
                               │     subtopics       │             "product_list",
                               │                     │             "benchmarks",
                               └─────────────────────┘             "use_cases",
                                                                   "pricing"
                                                                 ],
                                                                 searchQuery: "open source 
                                                                   vector database comparison
                                                                   RAG retrieval"
                                                               }
```

### SEARCH Stage

```
INPUT                          PROCESS                         OUTPUT
─────                          ───────                         ──────

{                              ┌─────────────────────┐         {
  query: "open source          │                     │           results: [
    vector database            │  FOR EACH backend:  │             { id: "r1", 
    comparison RAG",           │    1. Translate     │               content: "...",
  backends: [                  │       query         │               score: 0.92,
    "meilisearch",             │    2. Execute       │               source: "meilisearch" },
    "qdrant"                   │    3. Normalize     │             { id: "r2", ... },
  ],                           │       results       │             ...
  limit: 50                    │                     │           ],
}                              │  THEN:              │           backendResults: {
                               │    4. Merge with    │             meilisearch: { ... },
                               │       RRF           │             qdrant: { ... }
                               │    5. Dedupe        │           },
                               │                     │           mergeLog: { ... },
                               └─────────────────────┘           metrics: {
                                                                   latencyMs: 234,
                                                                   cost: 0.002
                                                                 }
                                                               }
```

### INGEST Stage

```
INPUT                          PROCESS                         OUTPUT
─────                          ───────                         ──────

{                              ┌─────────────────────┐         {
  documents: [                 │                     │           documents: [
    { url: "arxiv...",         │  FOR EACH doc:      │             {
      type: "pdf" },           │    1. Fetch         │               id: "d1",
    { url: "github...",        │    2. Parse         │               content: {
      type: "md" },            │       (PyMuPDF/     │                 text: "...",
    ...                        │        Trafilatura) │                 chunks: [...]
  ]                            │    3. Extract       │               },
}                              │       structure     │               structure: {
                               │    4. Chunk         │                 sections: [...],
                               │       semantically  │                 tables: [...]
                               │                     │               },
                               └─────────────────────┘               metadata: { ... }
                                                                   },
                                                                   ...
                                                                 ],
                                                                 metrics: { ... }
                                                               }
```

### EXTRACT Stage

```
INPUT                          PROCESS                         OUTPUT
─────                          ───────                         ──────

{                              ┌─────────────────────┐         {
  documents: [...],            │                     │           entities: [
  entityTypes: [               │  FOR EACH chunk:    │             { id: "e1",
    "Organization",            │    1. NER pass      │               type: "Organization",
    "Product",                 │       (spaCy)       │               name: "Qdrant",
    "Metric"                   │    2. LLM pass      │               confidence: 0.94 },
  ],                           │       (DeepSeek)    │             ...
  confidenceThreshold: 0.85    │    3. Relation      │           ],
}                              │       extraction    │           relations: [
                               │    4. Claim         │             { type: "BENCHMARKS",
                               │       extraction    │               source: "e1",
                               │    5. Dedup within  │               target: "e5",
                               │       document      │               confidence: 0.89 },
                               │                     │             ...
                               └─────────────────────┘           ],
                                                                 claims: [...],
                                                                 metrics: { ... }
                                                               }
```

### MERGE Stage

```
INPUT                          PROCESS                         OUTPUT
─────                          ───────                         ──────

{                              ┌─────────────────────┐         {
  newEntities: [...],          │                     │           delta: {
  newRelations: [...],         │  1. Load existing   │             entitiesAdded: [...],
  newClaims: [...],            │     graph state     │             entitiesMerged: [
  existingGraph: "ref:..."     │  2. Fuzzy match     │               { sourceIds: ["e1","e7"],
}                              │     entities        │                 targetId: "e1",
                               │  3. Semantic match  │                 reason: "same product" }
                               │     (embeddings)    │             ],
                               │  4. LLM verify      │             conflictsDetected: [
                               │     uncertain       │               { type: "contradictory",
                               │     matches         │                 claims: ["c1", "c5"] }
                               │  5. Merge with      │             ]
                               │     conflict log    │           },
                               │                     │           deduplicationLog: { ... },
                               └─────────────────────┘           metrics: { ... }
                                                               }
```

### STORE Stage

```
INPUT                          PROCESS                         OUTPUT
─────                          ───────                         ──────

{                              ┌─────────────────────┐         {
  delta: { ... }               │                     │           graphRef: "neo4j://...",
}                              │  1. Begin           │           stats: {
                               │     transaction     │             totalEntities: 127,
                               │  2. Apply entity    │             totalRelations: 243,
                               │     changes         │             totalClaims: 89
                               │  3. Apply relation  │           },
                               │     changes         │           metrics: {
                               │  4. Update claim    │             latencyMs: 45,
                               │     confidences     │             nodesWritten: 12,
                               │  5. Commit          │             edgesWritten: 18
                               │                     │           }
                               └─────────────────────┘         }
```

---

## Breakpoint Inspection

When a breakpoint is hit, the UI receives:

```json
{
  "event": "breakpoint_hit",
  "stage": "extract",
  "iteration": 2,
  "state": {
    "input": {
      "documents": [ /* full ingest output */ ],
      "entityTypes": ["Organization", "Product", "Metric"],
      "confidenceThreshold": 0.85
    },
    "config": {
      "backend": "claude_haiku",
      "batchSize": 10,
      "timeout": 30
    },
    "previousStages": {
      "query": { "status": "completed", "metrics": {...} },
      "search": { "status": "completed", "metrics": {...} },
      "ingest": { "status": "completed", "metrics": {...} }
    },
    "reasoning": {
      "iteration": 2,
      "confidence": 0.68,
      "coverage": 0.75,
      "gaps": [
        { "type": "missing_data", "description": "No pricing information" }
      ]
    }
  }
}
```

User can now:
1. Inspect input data
2. Change config (e.g., switch to DeepSeek)
3. Resume (continues with new config)
4. Step (run just this stage, pause again)

---

## Next Document

See [04-SPRINT-PLAN.md](./04-SPRINT-PLAN.md) for implementation phases.
