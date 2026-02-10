# Knowledge Graph Lab - Gemini Architecture Report

**Generated**: 2026-01-18
**Source**: `/Users/grig/work/peermesh/repo/knowledge-graph-lab-alpha/ext-repos/Knowledge-Graph-Lab-mark-26-01`

---

## EXECUTIVE SUMMARY

**Project Name**: Knowledge Graph Lab (Cognos)
**Status**: Active Development (Phase 7+)
**Technology Stack**: React 19, TypeScript, TailwindCSS, Google Gemini API
**Architecture Pattern**: Context-based React with Service layer for AI integration
**Key Phase**: Post-MVP with focus on Intelligence Upgrade (Sprint 2)

---

## 1. PROJECT VISION & MISSION

### Core Purpose
The Knowledge Graph Lab is a **self-replicating, recursive knowledge engine** that maps the latent space of human understanding into a navigable, visual ontology. It functions as a **proactive Life Consultant** for users.

### Five Core Pillars

1. **Autonomy**: The system traverses knowledge graphs, identifies gaps, and hypothesizes connections without user direction
2. **Consultancy (Wizard Mode)**: Interactive interviews with users to uncover "unknown unknowns" and propose Due Diligence Roadmaps
3. **Contextual Intelligence (Domains)**: Knowledge siloed into "Life Contexts" (Projects/Aspirations) for relevance
4. **Profile-Driven**: Deep psychological and goal-oriented user profiling to steer research
5. **Visualization**: Structure-as-meaning through ontology maps enabling dependency navigation

---

## 2. CURRENT ARCHITECTURE

### High-Level Data Flow

```
User Input (Text/Voice)
    ↓
[Semantic Refinement Stage 0]
    ↓ (normalized title)
[Deep Research Pipeline - 3 Stages]
    ├─ Stage 1: Deep Research Agent (gemini-3-pro-preview)
    │  └─ Output: Raw ~800-1000 word markdown notes
    ├─ Stage 2: Gap Analysis Agent (gemini-3-pro-preview)
    │  └─ Output: Missing link candidates with predicates
    └─ Stage 3: Synthesis/Report Generation (gemini-3-flash-preview)
       └─ Output: Structured JSON report with score
    ↓
[Graph Visualization & Interaction]
    └─ Force-directed graph + Modal Details
    ↓
[User Feedback Loop]
    └─ Approval/Flagging → Validation History
```

### Core Components Architecture

**State Management (React Context)**:
- `KnowledgeContext`: Topics, Domains, Reports, Roadmaps, Ontology Triples
- `WizardContext`: Session state, candidates, snapshots, tuning board
- `SystemContext`: Engine state, settings, logs, notifications, recipes
- `UIContext`: Modal states, active tab, selected items
- `AuthContext`: User authentication and profiles

**Service Layer**:
- `geminiService.ts`: All Gemini API integrations (8+ pipeline functions)
- `databaseService.ts`: Supabase/cloud persistence
- `storageService.ts`: localStorage with migration logic
- `audioService.ts`: Web Speech API & audio handling
- `restService.ts`: General REST utilities

**UI Components** (15+ components):
- `WizardModal.tsx` (50KB+): Interactive consultant with chat, voice, tuning board
- `DetailModal.tsx` (50KB+): Rich report viewer with tabs
- `GraphView.tsx`: Force-directed graph visualization
- `RoadmapView.tsx`: DAG-based roadmap rendering
- `ProfileModal.tsx`: User psychology & preferences
- `Sidebar.tsx`: Navigation and domain switching
- `SettingsView.tsx`: Configuration and recipe management

---

## 3. CORE CONCEPTS

### 3.1 LENSES (Topics)
**What they are**: Individual units of knowledge in the Vault

**Data Structure**:
```typescript
interface Topic {
  id: string (UUID v4)
  title: string
  status: TopicStatus (PENDING|PROCESSING|REFINING|COMPLETED|FAILED)
  priority: number (0-100)
  depth: number (hierarchy level)
  weight?: number (1-100, user-defined importance)
  contextDescription?: string (user's reasoning override)
  domainId?: string (which domain it belongs to)
  provenance?: any (research metadata)
  researchData?: string (raw research notes)
  groundingMetadata?: GroundingMetadata (search citations)
  recipeSnapshot?: Recipe (provenance of AI settings used)
}
```

**States & Transitions**:
- `PENDING` → `REFINING` → `PROCESSING` → `COMPLETED`
- `SUGGESTED` (from Wizard) → `COMMITTED` (user acceptance)
- `FAILED` or `HIDDEN` (user-driven dismissal)

---

### 3.2 RESEARCH PIPELINE (3-Stage)
**Purpose**: Transform raw topic into validated intelligence artifact

#### Stage 0: Semantic Refinement
- **Model**: `gemini-3-flash-preview`
- **Goal**: Normalize user input to canonical ontology node title
- **Input**: Raw user text + domain context
- **Output**: `{ refinedTitle: string }`
- **Logic**: Removes conversational filler, enforces noun-oriented naming

#### Stage 1: Deep Research (The Miner)
- **Model**: `gemini-3-pro-preview` (high reasoning)
- **Goal**: Gather raw, hallucination-resistant data
- **Input**: Refined title + Deep Research prompt template
- **Output**: ~800-1000 words unstructured markdown
- **Provenance**: Logs seed, temperature, model version
- **Key Constraint**: Must be dense academic notes, not fluff

#### Stage 2: Gap Analysis (The Architect)
- **Model**: `gemini-3-pro-preview`
- **Goal**: Auto-expand graph by finding missing links
- **Input**: Array of existing topic titles
- **Output**: JSON array of `{ title, connectedToId, predicate, reason }`
- **Predicates Used**: IS_A, CAUSES, PRECEDES, REQUIRES, RELATES_TO
- **Constraint**: Must avoid duplicates (fuzzy matching in client)

#### Stage 3: Synthesis (The Reporter)
- **Model**: `gemini-3-flash-preview`
- **Goal**: Generate UI artifact (The Report)
- **Input**: Raw research data + Report Generation prompt
- **Output**: JSON `{ title, content, summary, overview, takeaways[], score }`
- **Logic**: Applies strict rubric for scoring (0-100) based on novelty/utility

---

### 3.3 ONTOLOGY (Semantic Graph)
**Evolution**: From simple "Links" → Semantic Triples with typed predicates

**Data Structure**:
```typescript
interface OntologyTriple {
  id: string (UUID)
  sourceId: string (Subject Topic ID)
  targetId: string (Object Topic ID)
  predicate: PredicateType
  weight: number (0-1 confidence)
  temporalContext?: { startTime?, endTime?, isSequential }
  metadata?: {
    discoverySource: 'USER' | 'AI_INFERENCE' | 'LITERATURE'
    confidence: number
  }
}

type PredicateType = 'IS_A' | 'CAUSES' | 'PRECEDES' | 'REQUIRES' | 'RELATES_TO'
```

**Predicate Semantics**:
- **IS_A** (Taxonomy): "React IS_A JavaScript Library" → Enables domain bundling
- **CAUSES** (Causality): "Latency CAUSES User Churn" → Enables warning logic
- **PRECEDES** (Temporal): "Research PRECEDES Development" → Enables roadmap generation
- **REQUIRES** (Dependency): "Advanced Physics REQUIRES Calculus" → Prevents premature research
- **RELATES_TO** (General): Default association when relationship is unclear

---

### 3.4 GROUNDING LAYER (Truth Integration)
**Purpose**: Fact-check raw research against live web data, reduce hallucinations, provide citations

**Current Status**: In-flight (Work Order WO-015 - Active)

**Architecture**:
- **Tool Integration**: `tools: [{ googleSearch: {} }]` in Gemini config
- **Flow**: Research Agent triggers Google Search during `performResearch`
- **Output**: Text + `groundingMetadata` from Gemini
- **Data Capture**:
  ```typescript
  interface GroundingMetadata {
    searchEntryPoint?: { renderedContent: string }
    groundingChunks: GroundingChunk[]
    groundingSupports: GroundingSupport[]
  }
  ```

---

### 3.5 DOMAINS (Life Contexts)
**Vision**: Not just folder labels, but **Context Containers** representing projects/goals/personas

**Data Model**:
```typescript
interface Domain {
  id: string
  ownerId: string
  title: string
  subtitle?: string (quick read)
  detailedDescription?: string (SOURCE OF TRUTH)
  color?: string
  icon?: string
  stats?: { topicCount, roadmapProgress }
  contextFilters?: { includedPredicates, priorityKeywords }
  isSystem?: boolean
}
```

**The "Source of Truth" Pattern**:
- `detailedDescription` acts as system instruction for all research in this domain
- Example: "We are building B2B SaaS. Prioritize speed over quality. Target: non-technical founders."
- This description is injected into Deep Research and Gap Analysis prompts
- Enables automatic reasoning biasing toward domain-specific goals

---

### 3.6 ROADMAP (Due Diligence DAG)
**Vision**: Branching roadmaps for knowledge mastery, not linear checklists

**Architecture** (Directed Acyclic Graph):
```typescript
interface RoadmapNode {
  id: string
  title: string
  description?: string
  status: 'LOCKED' | 'AVAILABLE' | 'IN_PROGRESS' | 'COMPLETED'
  dependencies: string[] (IDs of parent nodes)
  linkedTopicId?: string (maps to a Topic)
  type: 'MILESTONE' | 'TASK' | 'KNOWLEDGE'
}
```

**State Machine** (Unlock Logic):
- **LOCKED**: Any dependency NOT COMPLETED → greyscale, non-clickable
- **AVAILABLE**: All dependencies COMPLETED → colored, pulsing, clickable
- **IN_PROGRESS**: User started this node (linked a Topic to it)
- **COMPLETED**: User marked done OR linked Topic COMPLETED

---

## 4. THE WIZARD INTERFACE (Interactive Consultant)

### Session Lifecycle
1. **Idle** → **Onboarding** (Welcome message + TTS) → **Active** → **Committed** → Clears

### Interaction Modes

#### A. Text Mode (Chat)
1. User types intent
2. System adds to transcript
3. Calls `chatWithWizard` (Gemini Flash)
4. Model returns: `{ response, inferredGoals, candidateTopics, planHierarchy, structuredFacts }`
5. **UI**: Chat bubble + Tuning Board populates with candidates

#### B. Voice Mode (Live - Realtime)
1. User clicks Mic → `ai.live.connect` (Native Audio)
2. Protocol: 16kHz PCM input → 24kHz PCM output
3. Model: `gemini-2.5-flash-native-audio-preview`
4. **Tools**: Model can call `propose_topic(title, reason)` to manipulate UI mid-conversation
5. **Visuals**: Chat fades to vignette, volume visualizer pulses

### The Tuning Board (Right Panel)
**Purpose**: Shared workspace between user and AI

**Generation**:
- Conversational: Model suggests topics from chat
- Infinite: User clicks "Load 3 More" → System prompts for novel vectors

**Selection & Commit**:
- Topics start pre-selected (`isSelected: true`)
- User toggles checkboxes
- Commit action: `knowledge.addTopic()` for every selected candidate
- Transition: Close Wizard → Dashboard

---

## 5. CURRENT IMPLEMENTATION STATUS

### Completed Features

**Sprint 1** (MVP):
- [x] Recursive Pipeline (3-stage research)
- [x] Force-Directed Graph
- [x] Safety Rails (quota management)
- [x] Modal Detail Views
- [x] Bookmarks & Bulk Operations
- [x] Notification System
- [x] Dashboard Refactor (Home/Hierarchy/Activity)
- [x] Manual Entry & Filtering
- [x] Wizard Onboarding (Auto-TTS, Visualizer)
- [x] Domain System (Context Switching)
- [x] Voice Mode (Web Speech API)
- [x] Deep Research Pipeline
- [x] Seed Data Injection
- [x] Data Persistence (localStorage + Supabase)

### In-Flight / Partially Implemented

- [ ] **WO-011 Smart Onboarding**: Domain generation detected but not fully wired
- [ ] **WO-015 Grounding Layer** (High Priority): Google Search tool integration started
- [ ] **Ontology Migration** (WO-005): Triple system implemented, graph visualization needs predicate-based styling
- [ ] **V2 Data Model** (Research Bundles): Conceptual structure defined, storage needs upgrade

### Planned/Future Features

**Sprint 2** (Intelligence Upgrade):
- [ ] Context Engine (FileSearch) - RAG integration
- [ ] MediaPipe WebGPU for local vector storage
- [ ] Recipe/Persona system for prompt variations
- [ ] Multi-Agent Debate (Skeptic vs. Believer)
- [ ] Advanced Psychometric Inference
- [ ] Mobile Companion app

---

## 6. KEY FILES REFERENCE

| File | Purpose | Size |
|------|---------|------|
| `App.tsx` | Main layout shell, processing loop | 38KB |
| `types/core.ts` | Core data structures | 5KB |
| `services/geminiService.ts` | All Gemini API integrations | 15KB |
| `contexts/KnowledgeContext.tsx` | Global knowledge state | 22KB |
| `contexts/WizardContext.tsx` | Wizard session + candidate tuning | 20KB |
| `components/WizardModal.tsx` | Interactive consultant UI | 51KB |
| `components/DetailModal.tsx` | Report viewer + editor | 50KB |
| `components/GraphView.tsx` | Force-directed visualization | 10KB |
| `constants.ts` | Prompts, SEED_DATA, defaults | 18KB |

---

## CONCLUSION

The Knowledge Graph Lab is a sophisticated, well-architected system designed to act as a **Recursive Knowledge Engine & Life Consultant**. It successfully integrates:

- **AI-driven research automation** (3-stage pipeline with Gemini)
- **Interactive consultation** (Wizard with text/voice modes)
- **Semantic knowledge representation** (Ontology triples with typed predicates)
- **Contextual reasoning** (Domains as "source of truth" for research biasing)
- **Structured planning** (Roadmaps as DAGs with dependency logic)
- **User profiling** (Psychometric inference + preference vectors)

The architecture is **modular, extensible, and governance-focused**. Most core features are implemented; remaining work is primarily UX polish, data model V2 migration, and grounding layer completion.
