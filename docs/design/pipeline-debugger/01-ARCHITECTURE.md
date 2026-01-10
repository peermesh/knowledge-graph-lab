# KGL Pipeline Debugger: Architecture

**Version:** 0.1.0-draft
**Created:** 2026-01-09
**Parent:** [00-VISION.md](./00-VISION.md)

---

## System Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│                                                                              │
│   React + TypeScript + Tailwind                                             │
│   Real-time WebSocket updates                                                │
│   Teenage Engineering aesthetic                                              │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    │ WebSocket / REST
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            ORCHESTRATION API                                 │
│                                                                              │
│   FastAPI + Pydantic                                                         │
│   Run management, breakpoints, config updates                                │
│   Event streaming to UI                                                      │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    │ Internal calls
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            REASONING ENGINE                                  │
│                                                                              │
│   LangGraph state machine                                                    │
│   Gap detection, convergence, decision making                                │
│   Iteration control                                                          │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    │ Module interface
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MODULE ABSTRACTION LAYER                            │
│                                                                              │
│   Unified interface for all pipeline stages                                  │
│   Hot-swap support, config injection                                         │
│   Snapshot/replay capability                                                 │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────────────────┤
│   SEARCH    │   INGEST    │   EXTRACT   │   MERGE     │   STORE             │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────────────┤
│ Meilisearch │ PyMuPDF     │ DeepSeek    │ RRF         │ Neo4j               │
│ Qdrant      │ Docling     │ Claude      │ Weighted    │ PostgreSQL          │
│ Typesense   │ Trafilatura │ spaCy       │ Union       │ SQLite (debug)      │
│ Zoekt       │ Unstructured│ Hybrid      │ Custom      │                     │
│ Weaviate    │             │             │             │                     │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────────────┘
                                    │
                                    │ Storage
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                      │
│                                                                              │
│   Run artifacts: /runs/{run_id}/                                            │
│   Module configs: /configs/                                                  │
│   Knowledge graph: Neo4j / PostgreSQL                                        │
│   Cache: Redis                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Orchestration API

```
/api/v1/
├── runs/
│   ├── POST   /                    Create new run
│   ├── GET    /{run_id}            Get run status
│   ├── POST   /{run_id}/start      Start/resume run
│   ├── POST   /{run_id}/pause      Pause at current stage
│   ├── POST   /{run_id}/stop       Stop run
│   ├── POST   /{run_id}/step       Execute one stage
│   ├── GET    /{run_id}/state      Get full state
│   └── WS     /{run_id}/stream     Real-time updates
│
├── breakpoints/
│   ├── POST   /{run_id}/set        Set breakpoint at stage
│   ├── DELETE /{run_id}/{stage}    Remove breakpoint
│   └── GET    /{run_id}            List breakpoints
│
├── modules/
│   ├── GET    /                    List available modules
│   ├── GET    /{module_id}/schema  Get config schema
│   └── POST   /{run_id}/{stage}/config  Update stage config
│
├── snapshots/
│   ├── GET    /{run_id}/{stage}    Get stage snapshot
│   └── POST   /{run_id}/replay     Replay from snapshot
│
└── inspect/
    ├── GET    /{run_id}/{stage}/input   Stage input data
    └── GET    /{run_id}/{stage}/output  Stage output data
```

### 2. Reasoning Engine (LangGraph)

```python
from langgraph.graph import StateGraph, END

class ResearchState(TypedDict):
    query: str
    intent: QueryIntent
    knowledge: KnowledgeGraph
    gaps: list[Gap]
    confidence: float
    coverage: float
    iteration: int
    cost: float
    history: list[IterationRecord]

def build_reasoning_graph():
    graph = StateGraph(ResearchState)
    
    # Nodes
    graph.add_node("analyze_query", analyze_query)
    graph.add_node("detect_gaps", detect_gaps)
    graph.add_node("plan_search", plan_search)
    graph.add_node("execute_pipeline", execute_pipeline)
    graph.add_node("evaluate_results", evaluate_results)
    graph.add_node("synthesize_output", synthesize_output)
    
    # Edges
    graph.add_edge("analyze_query", "detect_gaps")
    graph.add_edge("detect_gaps", "plan_search")
    graph.add_edge("plan_search", "execute_pipeline")
    graph.add_edge("execute_pipeline", "evaluate_results")
    
    # Conditional edges (the reasoning)
    graph.add_conditional_edges(
        "evaluate_results",
        decide_next_action,
        {
            "continue": "detect_gaps",      # Loop back
            "output": "synthesize_output",  # Done
            "ask_user": END                 # Need input
        }
    )
    
    graph.add_edge("synthesize_output", END)
    
    graph.set_entry_point("analyze_query")
    
    return graph.compile(checkpointer=PostgresSaver())
```

### 3. Module Abstraction Layer

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TInput = TypeVar('TInput')
TOutput = TypeVar('TOutput')
TConfig = TypeVar('TConfig')

class PipelineModule(ABC, Generic[TInput, TOutput, TConfig]):
    """Base class for all pipeline modules."""
    
    id: str
    name: str
    version: str
    category: str
    
    @property
    @abstractmethod
    def config_schema(self) -> dict:
        """JSON Schema for configuration."""
        pass
    
    @abstractmethod
    def configure(self, config: TConfig) -> None:
        """Apply configuration."""
        pass
    
    @abstractmethod
    async def process(self, input: TInput, context: ProcessContext) -> TOutput:
        """Process input and return output."""
        pass
    
    def snapshot(self, input: TInput, output: TOutput) -> Snapshot:
        """Create reproducible snapshot."""
        return Snapshot(
            module_id=self.id,
            module_version=self.version,
            config=self.get_config(),
            input=input,
            output=output,
            input_hash=hash_data(input),
            output_hash=hash_data(output)
        )
    
    async def replay(self, snapshot: Snapshot) -> TOutput:
        """Replay from snapshot for verification."""
        self.configure(snapshot.config)
        output = await self.process(snapshot.input, ProcessContext(replay=True))
        
        if hash_data(output) != snapshot.output_hash:
            raise ReplayMismatchError(
                f"Output hash mismatch: expected {snapshot.output_hash}, "
                f"got {hash_data(output)}"
            )
        
        return output


class SearchModule(PipelineModule[SearchInput, SearchOutput, SearchConfig]):
    """Search module with multi-backend support."""
    
    category = "search"
    backends: list[SearchBackend]
    merge_strategy: MergeStrategy
    
    async def process(self, input: SearchInput, context: ProcessContext) -> SearchOutput:
        # Execute all backends in parallel
        backend_tasks = [
            backend.search(input.query, input.filters)
            for backend in self.backends
            if backend.enabled
        ]
        
        backend_results = await asyncio.gather(*backend_tasks)
        
        # Merge without LLM (pure algorithm)
        merged = self.merge_strategy.merge(backend_results)
        
        return SearchOutput(
            results=merged,
            backend_results={
                backend.id: results
                for backend, results in zip(self.backends, backend_results)
            },
            merge_log=self.merge_strategy.get_log()
        )
```

### 4. Module Registry

```python
from typing import Type
import importlib
import pkgutil

class ModuleRegistry:
    """Auto-discovers and manages pipeline modules."""
    
    _modules: dict[str, Type[PipelineModule]] = {}
    
    @classmethod
    def register(cls, module_id: str):
        """Decorator to register a module."""
        def decorator(module_class: Type[PipelineModule]):
            cls._modules[module_id] = module_class
            return module_class
        return decorator
    
    @classmethod
    def discover(cls, package: str = "kgl.modules"):
        """Auto-discover modules in package."""
        pkg = importlib.import_module(package)
        for _, name, _ in pkgutil.walk_packages(pkg.__path__, f"{package}."):
            importlib.import_module(name)
    
    @classmethod
    def get(cls, module_id: str) -> Type[PipelineModule]:
        return cls._modules[module_id]
    
    @classmethod
    def list_by_category(cls, category: str) -> list[ModuleInfo]:
        return [
            ModuleInfo(id=mid, name=m.name, version=m.version, schema=m.config_schema)
            for mid, m in cls._modules.items()
            if m.category == category
        ]


# Usage
@ModuleRegistry.register("search.meilisearch")
class MeilisearchBackend(SearchBackend):
    id = "meilisearch"
    name = "Meilisearch"
    version = "1.0.0"
    # ...
```

---

## Data Flow Schemas

### SearchInput / SearchOutput

```typescript
interface SearchInput {
  query: string;
  filters?: {
    sources?: string[];        // Limit to specific sources
    dateRange?: DateRange;
    contentTypes?: string[];   // pdf, html, markdown, etc.
  };
  limit?: number;              // Max results per backend
  includeRaw?: boolean;        // Include raw backend responses
}

interface SearchOutput {
  results: SearchResult[];
  
  // Debugging data
  backendResults: Record<string, {
    backend: string;
    results: SearchResult[];
    latencyMs: number;
    query: string;              // Actual query sent (may differ)
    rawResponse?: any;
  }>;
  
  mergeLog: {
    strategy: string;
    inputCounts: Record<string, number>;
    outputCount: number;
    deduped: number;
    steps: MergeStep[];
  };
  
  metrics: {
    totalLatencyMs: number;
    cost: number;
  };
}

interface SearchResult {
  id: string;                   // Unique across all backends
  content: string;              // Text content or snippet
  score: number;                // Normalized 0-1
  
  source: {
    backend: string;            // Which backend found it
    originalId: string;         // ID in that backend
    originalScore: number;      // Score from backend
  };
  
  metadata: {
    url?: string;
    title?: string;
    contentType?: string;
    publishedDate?: string;
    author?: string;
    [key: string]: any;
  };
}
```

### IngestInput / IngestOutput

```typescript
interface IngestInput {
  documents: DocumentRef[];     // References from search
}

interface DocumentRef {
  id: string;
  url: string;
  contentType: string;
  size?: number;
}

interface IngestOutput {
  documents: IngestedDocument[];
  
  errors: {
    documentId: string;
    error: string;
    recoverable: boolean;
  }[];
  
  metrics: {
    totalDocuments: number;
    successCount: number;
    failedCount: number;
    totalBytes: number;
    latencyMs: number;
    cost: number;
  };
}

interface IngestedDocument {
  id: string;
  
  content: {
    text: string;               // Extracted text
    chunks: Chunk[];            // Semantic chunks
  };
  
  structure: {
    sections?: Section[];
    tables?: Table[];
    figures?: Figure[];
    references?: Reference[];
  };
  
  metadata: {
    title?: string;
    authors?: string[];
    publishedDate?: string;
    pageCount?: number;
    wordCount: number;
    language: string;
  };
}

interface Chunk {
  id: string;
  text: string;
  position: { start: number; end: number };
  embedding?: number[];         // If pre-computed
}
```

### ExtractInput / ExtractOutput

```typescript
interface ExtractInput {
  documents: IngestedDocument[];
  entityTypes: string[];        // What to extract
  confidenceThreshold: number;
}

interface ExtractOutput {
  entities: Entity[];
  relations: Relation[];
  claims: Claim[];
  
  // Per-document breakdown for debugging
  documentExtractions: Record<string, {
    entities: Entity[];
    relations: Relation[];
    claims: Claim[];
    processingLog: string[];
  }>;
  
  metrics: {
    entitiesExtracted: number;
    relationsExtracted: number;
    claimsExtracted: number;
    avgConfidence: number;
    latencyMs: number;
    cost: number;
  };
}

interface Entity {
  id: string;
  type: string;                 // Organization, Product, Metric, etc.
  name: string;
  aliases: string[];
  confidence: number;
  
  source: {
    documentId: string;
    chunkId: string;
    span: { start: number; end: number };
  };
  
  attributes: Record<string, any>;
}

interface Relation {
  id: string;
  type: string;                 // USES, COMPARES_TO, BENCHMARKS, etc.
  sourceEntity: string;         // Entity ID
  targetEntity: string;         // Entity ID
  confidence: number;
  
  evidence: {
    documentId: string;
    text: string;
  };
}

interface Claim {
  id: string;
  statement: string;
  entities: string[];           // Entity IDs involved
  confidence: number;
  
  evidence: {
    documentId: string;
    text: string;
  };
}
```

### MergeInput / MergeOutput

```typescript
interface MergeInput {
  newEntities: Entity[];
  newRelations: Relation[];
  newClaims: Claim[];
  existingGraph: KnowledgeGraphRef;
}

interface MergeOutput {
  // What changed
  delta: {
    entitiesAdded: Entity[];
    entitiesMerged: EntityMerge[];
    relationsAdded: Relation[];
    claimsAdded: Claim[];
    claimsUpdated: ClaimUpdate[];
    conflictsDetected: Conflict[];
  };
  
  // Deduplication audit
  deduplicationLog: {
    candidates: DedupeCandidate[];
    decisions: DedupeDecision[];
    strategy: string;
  };
  
  metrics: {
    inputEntities: number;
    outputEntities: number;
    deduped: number;
    conflicts: number;
    latencyMs: number;
  };
}

interface EntityMerge {
  sourceIds: string[];          // Original entity IDs
  targetId: string;             // Merged entity ID
  confidence: number;
  reason: string;
}

interface Conflict {
  type: "contradictory_claim" | "attribute_mismatch" | "relation_conflict";
  entities: string[];
  claims: string[];
  description: string;
  suggestedResolution?: string;
}
```

### ReasoningState

```typescript
interface ReasoningState {
  // Query understanding
  query: {
    original: string;
    intent: QueryIntent;
    subtopics: Subtopic[];
  };
  
  // Current knowledge
  knowledge: {
    graphRef: string;           // Reference to KG
    entityCount: number;
    relationCount: number;
    claimCount: number;
  };
  
  // Gap analysis
  gaps: Gap[];
  
  // Quality metrics
  confidence: number;           // 0-1, overall
  coverage: number;             // 0-1, subtopics addressed
  
  // Control
  iteration: number;
  maxIterations: number;
  cost: number;
  costLimit: number;
  
  // History
  history: IterationRecord[];
  
  // Decision
  status: "running" | "paused" | "completed" | "failed" | "awaiting_input";
  nextAction?: NextAction;
}

interface Gap {
  id: string;
  type: "missing_entity" | "missing_relation" | "low_confidence" | "stale" | "conflict";
  priority: number;             // 1-10
  description: string;
  suggestedQuery?: string;
}

interface IterationRecord {
  iteration: number;
  reason: string;
  query: string;
  searchResults: number;
  entitiesAdded: number;
  gapsResolved: string[];
  gapsRemaining: string[];
  cost: number;
  duration: number;
}
```

---

## Real-Time Event Stream

WebSocket messages from server to UI:

```typescript
type PipelineEvent = 
  | { type: "run_started"; runId: string; query: string }
  | { type: "iteration_started"; iteration: number; reason: string }
  | { type: "stage_started"; stage: string; module: string }
  | { type: "stage_progress"; stage: string; progress: number; message: string }
  | { type: "stage_completed"; stage: string; metrics: StageMetrics }
  | { type: "stage_error"; stage: string; error: string; recoverable: boolean }
  | { type: "breakpoint_hit"; stage: string; state: StageState }
  | { type: "reasoning_decision"; decision: string; gaps: Gap[]; confidence: number }
  | { type: "iteration_completed"; iteration: number; metrics: IterationMetrics }
  | { type: "run_completed"; finalState: ReasoningState }
  | { type: "run_failed"; error: string; lastState: ReasoningState }
  | { type: "config_updated"; stage: string; config: object };
```

---

## Directory Structure

```
kgl-pipeline-debugger/
├── api/                        # FastAPI backend
│   ├── main.py
│   ├── routers/
│   │   ├── runs.py
│   │   ├── modules.py
│   │   ├── breakpoints.py
│   │   └── inspect.py
│   ├── services/
│   │   ├── orchestrator.py     # Run management
│   │   ├── reasoning.py        # LangGraph engine
│   │   └── streaming.py        # WebSocket handler
│   └── models/
│       ├── schemas.py          # Pydantic models
│       └── events.py           # Event types
│
├── modules/                    # Pipeline modules
│   ├── __init__.py
│   ├── base.py                 # Abstract base classes
│   ├── registry.py             # Module discovery
│   ├── search/
│   │   ├── meilisearch.py
│   │   ├── qdrant.py
│   │   ├── typesense.py
│   │   ├── zoekt.py
│   │   └── merge.py            # Merge strategies
│   ├── ingest/
│   │   ├── pymupdf.py
│   │   ├── docling.py
│   │   ├── trafilatura.py
│   │   └── chunking.py
│   ├── extract/
│   │   ├── deepseek.py
│   │   ├── claude.py
│   │   ├── spacy.py
│   │   └── hybrid.py
│   ├── merge/
│   │   ├── dedup.py
│   │   ├── conflict.py
│   │   └── neo4j.py
│   └── reason/
│       ├── gap_detector.py
│       ├── convergence.py
│       └── strategies.py
│
├── ui/                         # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── PipelineView.tsx
│   │   │   ├── StageNode.tsx
│   │   │   ├── Inspector.tsx
│   │   │   ├── ConfigPanel.tsx
│   │   │   ├── ReasoningState.tsx
│   │   │   └── DataFlow.tsx
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts
│   │   │   └── useRunState.ts
│   │   └── stores/
│   │       └── runStore.ts
│   └── package.json
│
├── runs/                       # Run artifacts (gitignored)
│   └── {run_id}/
│       ├── manifest.yaml
│       ├── snapshots/
│       └── outputs/
│
├── configs/                    # Saved configurations
│   ├── defaults/
│   └── presets/
│
├── docker/
│   ├── docker-compose.yml      # Full stack
│   ├── docker-compose.dev.yml  # Dev with hot reload
│   └── Dockerfile.api
│
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

---

## Docker Services

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: ./docker/Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://kgl:kgl@postgres:5432/kgl
      - REDIS_URL=redis://redis:6379
      - NEO4J_URL=bolt://neo4j:7687
    depends_on:
      - postgres
      - redis
      - neo4j

  ui:
    build: ./ui
    ports:
      - "3000:3000"
    depends_on:
      - api

  postgres:
    image: postgres:16
    environment:
      - POSTGRES_USER=kgl
      - POSTGRES_PASSWORD=kgl
      - POSTGRES_DB=kgl
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  neo4j:
    image: neo4j:5
    environment:
      - NEO4J_AUTH=neo4j/password
    volumes:
      - neo4j_data:/data

  # Search backends (enable as needed)
  meilisearch:
    image: getmeili/meilisearch:v1.6
    profiles: ["search"]
    volumes:
      - meilisearch_data:/meili_data

  qdrant:
    image: qdrant/qdrant:v1.7
    profiles: ["search"]
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  postgres_data:
  redis_data:
  neo4j_data:
  meilisearch_data:
  qdrant_data:
```

---

## Next Document

See [02-DATA-FLOW.md](./02-DATA-FLOW.md) for complete data flow diagrams.
