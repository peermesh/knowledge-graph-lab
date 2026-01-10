# Knowledge Graph Lab: Architecture Principles

**Version:** 1.0.0
**Created:** 2026-01-09
**Status:** Foundational (source of truth)

---

## Core Architectural Insight

Traditional AI pipelines are **passive**: data flows in, transforms flow out. KGL requires an **active reasoning layer** that wraps the pipeline and makes decisions about iteration, convergence, and next actions.

This is the fundamental architectural distinction that separates KGL from simple RAG systems.

---

## The Two-Loop Architecture

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

### Inner Loop (Processing Pipeline)

**Purpose:** Transform data through stages
**Nature:** Passive (data-driven)
**Visibility:** Each stage's input/output inspectable

Stages:
1. **Query** — Parse intent, identify expected entities/relations
2. **Search** — Multi-backend retrieval with result merging
3. **Ingest** — Document parsing, chunking, structure extraction
4. **Extract** — Entity, relationship, and claim extraction
5. **Merge** — Deduplication, conflict detection, graph integration
6. **Store** — Knowledge graph persistence

### Outer Loop (Reasoning Engine)

**Purpose:** Decide what happens next
**Nature:** Active (decision-driven)
**Visibility:** Decision rationale exposed

Functions:
- **Gap Detection** — "I found X but Y is missing"
- **Query Refinement** — "Results too broad, narrowing to Z"
- **Convergence Check** — "Sufficient evidence gathered, stopping"
- **Conflict Resolution** — "Source A says X, Source B says Y"
- **Confidence Assessment** — "High confidence on X, low on Y"

---

## Feedback Loop Types

### Type 1: Expansion Loop

**Trigger:** Entity discovered that requires more context

```
EXTRACT ("Found: HNSW") → REASON ("Gap: What is HNSW?") → SEARCH ("HNSW algorithm vector")
```

### Type 2: Verification Loop

**Trigger:** Single-source claim needs corroboration

```
MERGE ("Claim: Qdrant 10x faster", single source) → REASON → SEARCH (seek second source)
```

### Type 3: Conflict Resolution Loop

**Trigger:** Contradictory claims from different sources

```
MERGE ("A: 100K QPS" vs "B: 50K QPS") → REASON → SEARCH (authoritative source)
```

### Type 4: Refinement Loop

**Trigger:** Results too broad or too narrow

```
SEARCH (10,000 docs) → REASON ("Too broad") → QUERY (add filters, constraints)
```

---

## Convergence Criteria

The reasoning loop exits when ANY of these conditions are met:

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| Confidence | ≥ 85% | Claims well-supported by multiple sources |
| Coverage | ≥ 90% | Expected subtopics addressed |
| Diminishing Returns | <5% new info for 2 iterations | Searching is no longer productive |
| Budget | Cost or time limit reached | Resource constraints |
| Max Iterations | Default: 10 | Safety valve |
| User Interrupt | Manual stop | Human override |

### Confidence Calculation

```
confidence = weighted_avg(claim_confidences)

Factors:
- Source count per claim (more = higher)
- Source authority (official > blog > forum)
- Recency (newer = higher for volatile topics)
- Consistency (agreeing sources = higher)
```

### Coverage Calculation

```
coverage = addressed_subtopics / total_subtopics

Subtopics derived from query intent:
- "comparison" → need: products, benchmarks, pros/cons
- "how to" → need: steps, prerequisites, examples
- "what is" → need: definition, uses, alternatives
```

---

## Module Abstraction Layer

Every pipeline module implements a consistent interface:

```python
class PipelineModule(Protocol):
    # Identity
    id: str           # "search.meilisearch"
    name: str         # "Meilisearch"
    version: str      # "1.0.0"
    category: str     # "search" | "ingest" | "extract" | "merge"
    
    # Configuration
    @property
    def config_schema(self) -> dict: ...    # JSON Schema for UI
    def configure(self, config: dict): ...   # Apply config (hot-reload)
    def get_config(self) -> dict: ...        # Current config
    
    # Processing
    async def process(self, input: StageInput, context: ProcessContext) -> StageOutput: ...
    
    # Debugging
    def get_state(self) -> ModuleState: ...
    
    # Reproducibility
    def snapshot(self, input: StageInput, output: StageOutput) -> Snapshot: ...
    async def replay(self, snapshot: Snapshot) -> StageOutput: ...
```

### Key Principles

1. **Hot-swappable** — Change module without restarting pipeline
2. **Self-describing** — Config schema enables auto-generated UI
3. **Reproducible** — Snapshot/replay enables debugging and verification
4. **Observable** — State inspection at any point

---

## Multi-Backend Search Merging

When multiple search backends are active, results merge algorithmically (no LLM):

### Merge Strategies

| Strategy | Description | Use When |
|----------|-------------|----------|
| `reciprocal_rank_fusion` | Standard hybrid search scoring | Default, balanced results |
| `interleave_by_score` | Normalize 0-1, sort combined | Similar result quality |
| `round_robin` | Alternate from each backend | Equal representation |
| `union_dedupe` | Combine all, dedupe by hash | Maximum recall |
| `weighted` | Apply weights per backend | Known quality differences |

### RRF Algorithm

```python
def rrf(backend_results: list[list[Result]], k: int = 60) -> list[Result]:
    scores = {}
    for results in backend_results:
        for rank, item in enumerate(results):
            scores[item.id] = scores.get(item.id, 0) + 1 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: -x[1])
```

### Source-Type Routing

Route different content types to appropriate backends:

```yaml
source_routing:
  "*.py|*.ts|*.rs": zoekt      # Code gets AST-aware indexing
  "*.md|*.pdf|*.html": meilisearch  # Prose gets full-text
  "*": qdrant                   # Everything gets vectors
```

---

## Run Reproducibility

Every run produces a complete manifest:

```yaml
run_id: r_2026-01-09_001
created: 2026-01-09T14:32:00Z
status: completed

query:
  original: "What are the best OSS vector databases for RAG?"
  intent: { type: comparison, entities: [vector_database, RAG] }

iterations:
  - iteration: 1
    reason: initial_search
    stages:
      - stage: search
        module: search.multi
        config_hash: sha256:abc...
        input_hash: sha256:def...
        output_hash: sha256:ghi...
    reasoning:
      gaps_found: 3
      confidence: 0.45
      decision: continue
      
  - iteration: 2
    # ...

final_state:
  confidence: 0.87
  coverage: 0.91
  convergence_reason: confidence_threshold_met

artifacts:
  knowledge_graph: outputs/kg_delta.json
  synthesis: outputs/answer.md
```

**Replay:** Load manifest, restore configs, re-execute from any iteration.

---

## Extensibility Model

### Adding New Modules

```python
from kgl.registry import register

@register("search.my_backend")
class MySearchBackend(SearchModule):
    id = "my_backend"
    name = "My Custom Search"
    
    config_schema = {
        "type": "object",
        "properties": {
            "endpoint": { "type": "string" },
            "api_key": { "type": "string", "secret": True }
        }
    }
    
    async def search(self, query: str, config: dict) -> list[SearchResult]:
        # Implementation
```

Registry auto-discovers. UI auto-generates config form from schema.

### Adding New Reasoning Strategies

```python
@register("reason.conservative")
class ConservativeReasoner(Reasoner):
    # Requires 3+ sources per claim
    # Max 5 iterations
    # Prefers authoritative sources
```

---

## Debugger Requirements

The visual debugger must expose:

### Pipeline View
- Stage nodes with status (pending/running/complete/error)
- Data flow connections
- Breakpoint markers (clickable to set)
- Progress indicators per stage

### Reasoning View
- Confidence meter (0-100%)
- Coverage meter (0-100%)
- Gap list with priorities
- Iteration timeline
- Decision log ("why did it loop back?")

### Inspector
- Input/output toggle for any stage
- JSON tree viewer with search
- Copy to clipboard
- Diff view for replay comparison

### Controls
- Run / Pause / Stop
- Step (single stage)
- Restart iteration
- Save / Load state

---

## Non-Negotiables

1. **Both loops visible** — Cannot debug pipeline without seeing reasoning decisions
2. **Algorithmic merging** — No LLM in the merge path (deterministic)
3. **Complete snapshots** — Every run fully reproducible
4. **Hot-swap modules** — Change config without restart
5. **Resource limits** — Never infinite loops

---

## Related Documents

- [Vision Master](./00-VISION-MASTER.md) — Mission and pillars
- [Search Infrastructure](./02-SEARCH-INFRASTRUCTURE.md) — Backend selection
- [Pipeline Debugger Design](../design/pipeline-debugger/) — Implementation details
