# PRD: Living Knowledge Collections

**Version:** 0.1.0 (Draft)
**Author:** AI-Assisted Design Session
**Date:** 2026-01-25
**Status:** Proposal

---

## Executive Summary

Introduce **Collections** as a first-class object in KGL - structured, evolving knowledge artifacts that hydrate research into visual, interconnected data presentations. Collections are self-improving through continuous verification, citation tracking, and assumption challenging.

**Vision Statement:**
> Every piece of researched knowledge becomes a living, breathing entity that grows more accurate over time, presents itself through modular visual components, and connects to everything it touches.

---

## Problem Statement

### Current State
- Research outputs are static documents or flat graphs
- No structured way to represent "Top 10 AI Papers" or "Music Career Tech Stack"
- Insights don't improve after initial capture
- No visual templates for presenting knowledge consistently
- Connections between data points lack presentation context

### User Pain Points
1. **Research dies after capture** - No mechanism for continuous refinement
2. **Presentation is manual** - Every insight needs custom formatting
3. **No confidence tracking** - Can't tell if data is verified or assumed
4. **Disconnected knowledge** - Related collections don't link meaningfully
5. **Static snapshots** - Knowledge frozen at time of creation

---

## Solution: Living Knowledge Collections

### Core Concept

A **Collection** is a structured container for related knowledge that:
- **Evolves** - Accuracy improves through verification cycles
- **Hydrates** - Granular data fills in over time
- **Visualizes** - Modular infographic widgets present data
- **Connects** - Links to other collections through typed relationships
- **Challenges** - Actively questions assumptions and seeks citations

### First-Class Object: Collection

```typescript
interface Collection {
  id: string;
  title: string;
  type: CollectionType;
  schema: CollectionSchema;      // Structure definition
  items: CollectionItem[];       // The actual data
  presentation: PresentationConfig;
  evolution: EvolutionState;
  connections: CollectionLink[];
  metadata: CollectionMetadata;
}

type CollectionType =
  | 'ranking'        // Top 10 X
  | 'comparison'     // X vs Y vs Z
  | 'ecosystem'      // Tech stack / platform suite
  | 'timeline'       // Historical progression
  | 'network'        // People / organizations
  | 'taxonomy'       // Hierarchical classification
  | 'custom';

interface CollectionItem {
  id: string;
  data: Record<string, any>;     // Schema-conformant data
  confidence: ConfidenceScore;
  citations: Citation[];
  assumptions: Assumption[];
  lastVerified: string;
  hydrationLevel: number;        // 0-100% completeness
}

interface ConfidenceScore {
  overall: number;               // 0-1
  breakdown: {
    cited: number;               // % backed by citations
    verified: number;            // % manually verified
    assumed: number;             // % assumptions
    stale: number;               // % needs refresh
  };
}
```

---

## Feature Specifications

### F1: Collection Types & Schemas

**Purpose:** Define the structure of knowledge for consistent hydration.

**Supported Types:**

| Type | Use Case | Example Schema Fields |
|------|----------|----------------------|
| `ranking` | Ordered lists | rank, name, score, trend, citations |
| `comparison` | Side-by-side analysis | dimensions[], items[], scores[][] |
| `ecosystem` | Connected platforms/tools | nodes[], categories[], integrations[] |
| `timeline` | Temporal progression | events[], dates[], impacts[] |
| `network` | People/org relationships | entities[], relationships[], influence[] |
| `taxonomy` | Hierarchical classification | root, children[], depth, leafCount |

**Schema Definition:**
```typescript
interface CollectionSchema {
  type: CollectionType;
  fields: SchemaField[];
  requiredFields: string[];
  validations: ValidationRule[];
  defaultPresentation: string;  // Widget type
}

interface SchemaField {
  name: string;
  type: 'string' | 'number' | 'date' | 'entity' | 'citation' | 'array';
  description: string;
  citationRequired: boolean;
  evolutionStrategy: 'manual' | 'auto-refresh' | 'ai-verify';
}
```

---

### F2: Modular Visual Widgets (Infographics)

**Purpose:** Reusable visual components that render collection data.

**Widget Library:**

| Widget | Renders | Best For |
|--------|---------|----------|
| `RankingCard` | Single ranked item | Top 10 lists |
| `ComparisonMatrix` | Multi-dimensional comparison | Tool selection |
| `EcosystemMap` | Node-link diagram | Tech stacks |
| `TimelineStrip` | Horizontal timeline | History |
| `NetworkGraph` | Force-directed people graph | Influence maps |
| `StatBlock` | Key metrics highlight | Quick facts |
| `CitationStack` | Sources with confidence | Verification |
| `AssumptionFlag` | Unverified claims | Transparency |

**Widget Architecture:**
```typescript
interface Widget {
  id: string;
  type: WidgetType;
  dataBinding: DataBinding;      // Maps collection fields to widget props
  styling: WidgetStyle;
  interactions: Interaction[];   // Click, hover, drill-down
  childWidgets?: Widget[];       // Nested widgets
}

interface DataBinding {
  source: 'collection' | 'item' | 'computed';
  field: string;
  transform?: (value: any) => any;
}
```

**Visual Hierarchy:**
```
Collection View
├── Header Widget (title, confidence, last updated)
├── Summary Widget (key stats, trends)
├── Items Grid
│   ├── Item Card Widget
│   │   ├── Rank Badge
│   │   ├── Title + Description
│   │   ├── Metric Bars
│   │   ├── Citation Indicators
│   │   └── Drill-Down Arrow → Sub-Collection
│   └── ... more items
├── Connection Widget (related collections)
└── Evolution Widget (verification status, next actions)
```

---

### F3: Evolution Engine (Self-Improvement)

**Purpose:** Collections actively improve their accuracy over time.

**Evolution Mechanisms:**

#### 3a. Citation Verification
```typescript
interface CitationVerification {
  schedule: 'daily' | 'weekly' | 'monthly' | 'on-access';
  actions: [
    'check-link-alive',
    'extract-updated-data',
    'compare-to-stored',
    'flag-if-changed'
  ];
}
```

#### 3b. Assumption Challenging
```typescript
interface AssumptionChallenge {
  assumption: string;
  confidence: number;
  challengePrompt: string;        // AI prompt to find counter-evidence
  researchActions: [
    'search-contradictions',
    'find-newer-sources',
    'check-expert-opinions'
  ];
  resolution: 'confirmed' | 'refuted' | 'updated' | 'pending';
}
```

#### 3c. Hydration Queue
```typescript
interface HydrationTask {
  collectionId: string;
  itemId: string;
  field: string;
  currentValue: any;
  targetCompleteness: number;
  researchStrategy: 'web-search' | 'citation-follow' | 'ai-inference';
  priority: number;
}

// Hydration runs in background, filling empty fields
async function hydrateCollection(collection: Collection) {
  const emptyFields = findEmptyFields(collection);
  for (const field of emptyFields) {
    const value = await researchField(field);
    if (value.confidence > 0.7) {
      updateField(field, value);
      addCitation(field, value.source);
    } else {
      flagAsAssumption(field, value);
    }
  }
}
```

#### 3d. Staleness Detection
```typescript
interface StalenessConfig {
  maxAge: number;                 // Days before considered stale
  triggerRefresh: boolean;
  notifyUser: boolean;
  autoArchive: boolean;           // If stale > 1 year
}
```

---

### F4: Inter-Collection Connections

**Purpose:** Collections link to each other, forming a knowledge network.

**Connection Types:**

| Connection | Meaning | Example |
|------------|---------|---------|
| `contains` | Parent-child | "AI Ecosystem" contains "Top LLMs" |
| `references` | Citation link | "Music Career Guide" references "DAW Comparison" |
| `contradicts` | Conflicting data | Two sources disagree |
| `extends` | Adds depth | "LLM Benchmarks" extends "Top LLMs" |
| `supersedes` | Newer version | "2026 Rankings" supersedes "2025 Rankings" |

**Navigation Model:**
```
Collection A
├── [contains] → Sub-Collection A1
│               ├── [contains] → Sub-Collection A1a
│               └── [references] → Collection B
├── [references] → Collection C
└── [extends] → Collection D
```

**Link Tree Rendering:**
```typescript
interface CollectionTreeNode {
  collection: Collection;
  connectionType: ConnectionType;
  children: CollectionTreeNode[];
  isExpanded: boolean;
  widgetOverride?: Widget;        // Custom presentation for this node
}

// Infinite drill-down through connected collections
function renderCollectionTree(root: CollectionTreeNode): JSX.Element {
  return (
    <TreeNode>
      <CollectionWidget collection={root.collection} />
      {root.isExpanded && root.children.map(child => (
        <ConnectionLabel type={child.connectionType} />
        {renderCollectionTree(child)}  // Recursive
      ))}
    </TreeNode>
  );
}
```

---

### F5: Presentation Templates

**Purpose:** Pre-built visual configurations for common use cases.

**Template Library:**

| Template | Layout | Best For |
|----------|--------|----------|
| `top-10-listicle` | Ranked cards with metrics | "Top AI Papers" |
| `comparison-showdown` | Side-by-side matrix | "Claude vs GPT vs Gemini" |
| `ecosystem-map` | Radial node diagram | "Music Production Stack" |
| `timeline-story` | Horizontal scroll | "History of Neural Networks" |
| `people-network` | Force graph with photos | "AI Research Influencers" |
| `decision-tree` | Flowchart | "Which DAW Should I Use?" |

**Template Definition:**
```typescript
interface PresentationTemplate {
  id: string;
  name: string;
  applicableTypes: CollectionType[];
  layout: LayoutConfig;
  widgets: WidgetPlacement[];
  colorScheme: ColorScheme;
  typography: TypographyConfig;
  animations: AnimationConfig;
}
```

---

### F6: Faceted Index (Master Navigation)

**Purpose:** Entry point to all collections, organized by facets.

**Facet Dimensions:**

| Facet | Description |
|-------|-------------|
| Domain | AI, Music, Finance, Health, etc. |
| Type | Rankings, Comparisons, Ecosystems, etc. |
| Confidence | Verified, Partially Verified, Assumed |
| Freshness | Updated Today, This Week, Stale |
| Completeness | 100%, 75%+, Needs Hydration |
| Creator | AI-Generated, User-Created, Imported |

**Index View:**
```
┌─────────────────────────────────────────────────────────┐
│ KNOWLEDGE INDEX                          [+] New Collection │
├─────────────────────────────────────────────────────────┤
│ Facets: [AI ▼] [Rankings ▼] [Verified ▼] [This Week ▼]   │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│ │ Top LLMs    │ │ AI Papers   │ │ ML Frameworks│        │
│ │ 🟢 98%     │ │ 🟡 76%     │ │ 🟢 92%      │        │
│ │ 15 items    │ │ 50 items    │ │ 23 items     │        │
│ │ [Expand →] │ │ [Expand →] │ │ [Expand →]  │        │
│ └─────────────┘ └─────────────┘ └─────────────┘        │
│                                                         │
│ Recently Updated:                                        │
│ • "Claude 4 Opus" added to Top LLMs (2 hours ago)       │
│ • "DAW Comparison" challenged assumption #3 (verified)   │
└─────────────────────────────────────────────────────────┘
```

---

## User Journeys

### Journey 1: Create "Top AI White Papers" Collection

1. User clicks "+ New Collection"
2. Selects type: `ranking`
3. Names it: "Top AI White Papers 2026"
4. System suggests schema: title, authors, year, citations, impact_score, summary
5. User adds first 3 papers manually with citations
6. User clicks "Hydrate" - AI researches remaining papers
7. AI adds 7 more papers with confidence scores
8. User verifies 2, flags 1 as questionable
9. Collection shows: 90% confidence, 10 items, 8 verified

### Journey 2: Build "Perfect Music Career Stack"

1. User creates `ecosystem` collection
2. Defines categories: DAW, Plugins, Distribution, Marketing, Analytics
3. Adds known tools (Ableton, DistroKid, Spotify for Artists)
4. AI suggests missing pieces (mastering services, social tools)
5. User accepts some, rejects others
6. System creates sub-collections for each category
7. Connections auto-generated: "DistroKid" → [integrates_with] → "Spotify"
8. Template: `ecosystem-map` renders interactive diagram

### Journey 3: Navigate the Link Tree

1. User opens "AI Research Landscape" collection
2. Sees top-level nodes: LLMs, Computer Vision, Robotics, etc.
3. Clicks "LLMs" → expands to show "Top LLMs", "LLM Benchmarks", "LLM Safety"
4. Each sub-node renders as a widget card
5. Clicks "Top LLMs" → full collection view opens
6. Sees connection: "Top LLMs" → [references] → "Transformer Architecture"
7. Clicks connection → navigates to related collection
8. Infinite drill-down through knowledge graph

### Journey 4: Watch Collection Evolve

1. User created "AI Startup Landscape" 3 months ago
2. Returns today - sees "12 updates available"
3. Review panel shows:
   - 3 new startups discovered (AI suggested)
   - 2 funding amounts updated (citations refreshed)
   - 1 assumption challenged (conflicting source found)
4. User approves updates → confidence rises to 94%
5. Stale items flagged for removal

---

## Technical Architecture

### Data Model

```
Collections (PostgreSQL/SQLite)
├── id, title, type, schema_id, owner_id, created_at, updated_at
├── confidence_score, hydration_level, last_verified
└── presentation_config (JSONB)

CollectionItems
├── id, collection_id, data (JSONB), rank/order
├── confidence_score, hydration_level
├── citations (JSONB[]), assumptions (JSONB[])
└── last_verified, verification_history (JSONB)

CollectionConnections
├── source_collection_id, target_collection_id
├── connection_type, strength, bidirectional
└── created_by, created_at

CollectionSchemas
├── id, type, name, fields (JSONB)
├── validations (JSONB), default_presentation
└── is_system (built-in vs custom)

PresentationTemplates
├── id, name, applicable_types[]
├── layout_config (JSONB), widget_placements (JSONB)
└── is_system, created_by
```

### Evolution Engine Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   EVOLUTION ENGINE                       │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Hydration    │  │ Verification │  │ Challenge    │  │
│  │ Worker       │  │ Worker       │  │ Worker       │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │           │
│         ▼                 ▼                 ▼           │
│  ┌─────────────────────────────────────────────────┐   │
│  │              TASK QUEUE (Redis)                  │   │
│  │  • hydrate:collection:123:field:impact_score    │   │
│  │  • verify:citation:456:check-link               │   │
│  │  • challenge:assumption:789:find-counter        │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │           AI RESEARCH SERVICE (Gemini)           │   │
│  │  • Web search for missing data                   │   │
│  │  • Citation extraction from URLs                 │   │
│  │  • Contradiction detection                       │   │
│  │  • Confidence scoring                            │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Widget Rendering Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   WIDGET SYSTEM                          │
├─────────────────────────────────────────────────────────┤
│  Collection Data                                         │
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────┐                                       │
│  │ Data Binder  │ ← Schema + Template                   │
│  └──────┬───────┘                                       │
│         │                                                │
│         ▼                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ RankingCard  │  │ StatBlock    │  │ CitationStack│  │
│  │ Component    │  │ Component    │  │ Component    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                 │                 │           │
│         ▼                 ▼                 ▼           │
│  ┌─────────────────────────────────────────────────┐   │
│  │              COMPOSITE RENDERER                  │   │
│  │  Assembles widgets into collection view          │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│                    React DOM                            │
└─────────────────────────────────────────────────────────┘
```

---

## Success Metrics

### Engagement
- Collections created per user per month
- Drill-down depth (avg clicks before exit)
- Return visits to evolving collections

### Quality
- Avg confidence score across collections
- % of items with citations
- Assumption → Verified conversion rate

### Growth
- Inter-collection connections per collection
- Hydration completion rate
- User corrections per 100 AI suggestions

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Citation rot (dead links) | Data trust | Automated link checking, archive fallback |
| AI hallucination | False confidence | Require citations for high-confidence claims |
| Schema complexity | User confusion | Start with templates, hide complexity |
| Performance at scale | Slow rendering | Virtualized lists, lazy hydration |
| Over-connection | Graph spaghetti | Connection strength thresholds, pruning |

---

## Open Questions

1. **Versioning:** Should collections have explicit versions or continuous evolution?
2. **Collaboration:** Multi-user editing, conflict resolution?
3. **Export:** How to export a collection (PDF, JSON, embed)?
4. **Monetization:** Premium templates? Verified badges?
5. **Privacy:** Public vs private collections?

---

## Appendix: Example Collections

### Example 1: "Top 10 LLMs 2026"

```yaml
type: ranking
schema:
  - name: string (required, cited)
  - organization: string (required)
  - parameters: number (cited)
  - benchmark_score: number (cited)
  - release_date: date
  - open_source: boolean
  - summary: string (ai-generated)

items:
  - rank: 1
    name: "Claude 4 Opus"
    organization: "Anthropic"
    parameters: "Unknown (estimated 1T+)"
    benchmark_score: 94.2
    confidence: 0.92
    citations: [anthropic.com, arxiv:2601.xxxxx]

presentation: top-10-listicle
```

### Example 2: "Music Production Ecosystem"

```yaml
type: ecosystem
schema:
  categories:
    - name: "DAW"
      items: [Ableton, Logic, FL Studio]
    - name: "Distribution"
      items: [DistroKid, TuneCore, CD Baby]
    - name: "Marketing"
      items: [Linktree, Koji, Hypeddit]

  integrations:
    - source: "DistroKid"
      target: "Spotify"
      type: "distributes_to"
    - source: "Ableton"
      target: "Splice"
      type: "integrates_with"

presentation: ecosystem-map
```

---

*End of PRD*
