# Pipeline Prototype-1: Visual Tuning UI Report

**Generated**: 2026-01-18
**Source**: `/Users/grig/work/peermesh/repo/knowledge-graph-lab-alpha/ext-repos/pipeline-prototype-1`

---

## Overview: What is This Prototype?

A **Visual AI Pipeline Tuning UI** for Knowledge Graph Lab deep research. A React/TypeScript web application providing an interactive, visual interface for configuring and managing a multi-stage AI pipeline for semantic search, knowledge extraction, and answer synthesis.

**Vision**: Modular, highly-configurable pipeline where each stage can be individually tuned with "switches" (cross-cutting concerns like cost control, caching, telemetry) that modify behavior without changing core stage logic.

---

## Pipeline Architecture

### Row 1: Feedback Loop Context (Search Phase)
```
QUERY → T1: MAP → GAPS → T2: ROUTE → [P3: PARALLEL SEARCH] → MERGE
```

### Row 2: Ingestion & Knowledge Graph Build (Processing Phase)
```
[QUEUE] → INGEST → T4: CHUNK → EXTRACT → T5: PAIR → RELATE → KG-MERGE → T6: FILTER → SYNTH → OUTPUT
```

---

## 1. Pipeline Stages Defined (16 Nodes)

### Primary Processing Stages (Type: "stage")

| Stage ID | Name | Purpose | Cost | Latency |
|----------|------|---------|------|---------|
| `query` | P1: QUERY | Parse natural language into structured intent | $0.0002/query | <50ms |
| `gaps` | P2: GAPS | Identify knowledge gaps via LLM | $0.003/query | <200ms |
| `ingest` | P4: INGEST | Fetch & chunk documents from URLs | $0.000 | <5000ms |
| `extract` | P5: EXTRACT | Extract entities & facts via LLM | $0.005/doc | <2000ms |
| `relate` | P6: RELATE | Build typed relationships between entities | $0.003/batch | <1500ms |
| `kg-merge` | P7: KG-MERGE | Merge new knowledge with conflict resolution | $0.000 | <500ms |
| `synth` | P8: SYNTH | Generate final answer with citations | $0.008/answer | <3000ms |

### Transform Stages (Type: "transform")

| Stage ID | Name | Purpose | Latency |
|----------|------|---------|---------|
| `t1` | T1: MAP | Map query intent to gap analysis input | <5ms |
| `t2` | T2: ROUTE | Fan out priorities to different search backends | <10ms |
| `t4` | T4: CHUNK | Prepare documents for entity extraction | <10ms |
| `t5` | T5: PAIR | Generate entity pairs for relationship extraction | <20ms |
| `t6` | T6: FILTER | Extract relevant subgraph for synthesis | <50ms |

### Parallel Search (P3) - 6 Configurable Tools

| Tool | Type | Best For |
|------|------|----------|
| Meilisearch | Full-text | Typo tolerance |
| Qdrant | Vector | Semantic similarity (HNSW) |
| Tavily | Web API | Real-time web search |
| Algolia | Hosted | Enterprise search |
| Elasticsearch | Boolean | Complex BM25 queries |
| Pinecone | Managed Vector | Cloud vector DB |

### Other Node Types
- **Merge**: Combines parallel search results using RRF
- **Queue**: Redis/BullMQ job queue (FIFO with priority)
- **Endpoint**: Final answer output

---

## 2. Recipe/Tuning Variables (6 Switches)

### Switch #1: Cost Control ($)
**Applied to**: Paid API stages (query, gaps, extract, relate, synth, tavily)
- Budget Tier: free | standard | pro | unlimited
- Max Cost: $0.001-$0.1 per call
- Soft Cap Alert: Toggle

### Switch #2: Telemetry (⏱)
**Applied to**: All stages by default
- Log Level: error | warn | info | debug | trace
- Sampling Rate: 0-100%

### Switch #3: Persist/Cache (📦)
**Applied to**: Search tools, expensive stages, external APIs
- Time-to-Live: 60s-24h
- Strategy: LRU | FIFO | permanent

### Switch #4: Rate Limit/Throttle (🚦)
**Applied to**: Search tools, external stages
- Max Requests/Sec: 1-1000 req/s
- Queue Size: 0-100 concurrent jobs

### Switch #5: Retry/Recovery (🔄)
**Applied to**: External stages, search tools
- Max Retries: 0-10 attempts
- Backoff Strategy: linear | exponential | static

### Switch #6: Debug/Snapshot (📸)
**Applied to**: Complex stages (query, gaps, extract, synth)
- Format: JSON | binary | text
- Trigger: On error only vs. always

### Smart Default Logic
```
- Trace (telemetry):  ENABLED on all stages
- Cost control:       ENABLED on paid nodes ($cost !== '$0.000')
- Caching/Throttle:   ENABLED on search tools
- Retry:              ENABLED on external/stage type nodes
```

---

## 3. UI Components

### StageNode.tsx - Visual Pipeline Node
- **Sizes**: Transforms 20x20px, Stages 36x36px
- **Colors**: Transforms (amber), Merges (emerald), Stages (cyan), Endpoints (rose)
- **Features**: Mixin indicator grid, portal tooltips, AI-generated icons

### ControlPanel.tsx - Bottom Configuration Deck
- **Modes**: "IO/Data" vs "Controls" toggle
- **Data Mode**: Input/output schemas, persistence operations
- **Controls Mode**: Switch toggle buttons in 3-4 column grid

### SwitchEditor.tsx - Inline Switch Configuration
- Master enable/disable toggle
- Dynamic fields: sliders, selects, toggles
- Positioned above trigger button

### DataInspector.tsx - I/O & Persistence Viewer
- 3-column layout: Input, Persistence Ops, Output
- Queue special handling with Redis topology

---

## 4. State Management

```typescript
interface PipelineState {
  selectedStageId: string | null;
  generatedIcons: Record<string, base64>;
  isGenerating: boolean;
  nodeConfigurations: {
    [stageId]: {
      [switchId]: {
        enabled: boolean,
        values: Record<fieldKey, value>
      }
    }
  };
  globalSettings: {
    costMode: 'unlimited' | 'funded' | 'broke' | 'free';
    telemetryLevel: 'verbose' | 'standard' | 'critical';
    globalCacheTTL: number;
  };
  panelMode: 'controls' | 'data';
}
```

### Persistence
- localStorage keys: `kgl_pipeline_icons`, `kgl_pipeline_config`, `kgl_pipeline_global`
- Quota overflow protection

---

## 5. User Workflows

### Quick Configuration
1. Click stage node → ControlPanel appears
2. Click "Controls" tab → See switch buttons
3. Click switch → SwitchEditor popover
4. Adjust sliders/options → Auto-saves

### I/O Inspection
1. Click stage → "IO/Data" tab
2. View input schema, persistence ops, output schema

### Global Settings
1. Click ⚙️ in header
2. Adjust Cost Mode, Telemetry Level, Cache TTL

### Search Provider Configuration
1. Click "P3: SEARCH" box
2. Toggle which tools are active in parallel

### Icon Customization
1. Click stage → ControlPanel icon area
2. "Redraw" (Gemini AI) or "Upload" custom

---

## 6. Unique Features

### Smart Defaults
Auto-enable switches based on node characteristics - "batteries included"

### Type-Based Styling
Visual theme per node type for instant recognition

### Mixin Indicators
3x2 grid showing enabled switches without opening panel

### Parallel Search Block
Grid of icon tiles for search tools with toggle modal

### AI Icon Generation
Gemini API with exponential backoff retry

### Queue as First-Class Node
Visual representation with job count, throughput stats

---

## 7. Key Data Structures

### StageData
```typescript
{
  id: string;
  name: string;
  type: 'stage' | 'transform' | 'merge' | 'endpoint' | 'queue';
  summary: string;
  purpose: string;
  latency: string;
  cost: string;
  availableSwitches: string[];
  ioConfig?: IOConfig;
}
```

### IOConfig
```typescript
{
  inputSchema: Record<string, any>;
  outputSchema: Record<string, any>;
  persistence: PersistenceOp[];
  queueConfig?: { name, priority, lifecycle[] }
}
```

### SwitchDefinition
```typescript
{
  id: string;
  icon: string;
  name: string;
  summary: string;
  schema: SwitchField[];
}
```

---

## Integration Value

This prototype provides:

1. **Visual-first design**: Nodes + arrows + colors communicate structure instantly
2. **Composable switches**: 6 reusable cross-cutting concerns applied per-node
3. **Smart defaults**: Auto-enable sensible configs based on stage type/cost
4. **Dual modes**: Visual/schematic view AND detailed controls/data view
5. **Persistent state**: All configurations saved to localStorage
6. **Type-safe architecture**: Comprehensive TypeScript interfaces

The UI layer (React components) is decoupled from the data layer (types, structures), making it ready to merge with other pipeline visions.
