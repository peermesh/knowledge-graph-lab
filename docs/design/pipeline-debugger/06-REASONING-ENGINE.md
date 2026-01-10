# Reasoning Engine: Outer Loop Control

**Version:** 0.1.0  
**Created:** 2026-01-10  
**Status:** Design  
**Purpose:** Orchestrate research iteration and decide when to continue, output, or ask

---

## Overview

The Reasoning Engine is the "outer loop" that wraps the research pipeline. It monitors progress, evaluates answer quality, and decides whether to continue researching, output the current answer, or ask the user for clarification.

---

## Architecture

```
                    ResearchQuestion[]
                    (from Exploration)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       REASONING ENGINE                                   │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      STATE MONITOR                                 │  │
│  │  confidence: 0.72  │  coverage: 0.85  │  iteration: 3  │  $0.034  │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                           │                                              │
│                           ▼                                              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐  │
│  │  EVALUATE   │──▶│   DECIDE    │──▶│   REFINE    │──▶│  (next      │  │
│  │             │   │             │   │   (if       │   │   iteration)│  │
│  │ Score       │   │ CONTINUE?   │   │  CONTINUE)  │   │             │  │
│  │ answer      │   │ OUTPUT?     │   │             │   │             │  │
│  │ quality     │   │ ASK?        │   │ Adjust      │   │             │  │
│  │             │   │             │   │ strategy    │   │             │  │
│  └─────────────┘   └──────┬──────┘   └─────────────┘   └─────────────┘  │
│                           │                                              │
│           ┌───────────────┼───────────────┐                             │
│           ▼               ▼               ▼                             │
│       CONTINUE         OUTPUT           ASK                             │
│           │               │               │                             │
│           ▼               │               │                             │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      INNER LOOP                                  │   │
│  │  QUERY → GAPS → SEARCH → INGEST → EXTRACT → RELATE → KG → SYNTH │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
                   SynthesizedAnswer
                   (to Output Gate)
```

---

## Components

### 1. State Monitor

**Purpose:** Track pipeline state across iterations

The State Monitor maintains a complete picture of the current research state, enabling informed decisions about when to stop.

**State Schema:**

```typescript
interface PipelineState {
  // Iteration tracking
  iteration: number;
  max_iterations: number;
  current_stage: string;
  
  // Quality metrics
  confidence: number;      // 0-1, how confident in current answer
  coverage: number;        // 0-1, how much of query is addressed
  gaps_remaining: string[];
  
  // Resource tracking
  cost_spent: number;
  cost_budget: number;
  time_elapsed_ms: number;
  
  // History
  iterations: IterationSummary[];
  convergence_trend: number[];  // confidence deltas
}

interface IterationSummary {
  iteration: number;
  confidence_before: number;
  confidence_after: number;
  sources_added: number;
  entities_added: number;
  cost: number;
}
```

**Confidence Calculation:**

```python
confidence = weighted_average([
  source_quality * 0.30,      # How authoritative are sources
  entity_coverage * 0.25,     # How many expected entities found
  citation_density * 0.20,    # How well-supported are claims
  consistency_score * 0.15,   # Do sources agree
  recency_score * 0.10        # How fresh is the information
])
```

**Coverage Calculation:**

```python
coverage = aspects_addressed / aspects_required

# aspects_required comes from query decomposition
# aspects_addressed comes from entity/fact extraction
```

**Configuration:**

```yaml
state_monitor:
  track_confidence: true
  track_coverage: true
  track_cost: true
  track_time: true
  history_depth: 10  # iterations to keep
  confidence_model: weighted_average  # or: ml_model
  coverage_method: aspect_ratio       # or: entity_ratio
```

---

### 2. Evaluate

**Purpose:** Score current answer quality and identify gaps

After each iteration, Evaluate assesses whether the current answer is good enough.

**Evaluation Dimensions:**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 0.30 | Does answer address all aspects of query? |
| Accuracy | 0.25 | Are claims well-supported by sources? |
| Relevance | 0.20 | Is content actually relevant to query? |
| Freshness | 0.15 | Is information current enough? |
| Coherence | 0.10 | Does answer flow logically? |

**Gap Detection:**

```typescript
interface GapAnalysis {
  missing_entities: string[];     // Expected but not found
  weak_coverage: string[];        // Mentioned but thin
  contradictions: Contradiction[];
  unanswered_aspects: string[];   // Query parts not addressed
}

interface Contradiction {
  claim: string;
  source_a: string;
  source_b: string;
  resolution_needed: boolean;
}
```

**Output:**

```typescript
interface EvaluationResult {
  confidence: number;
  coverage: number;
  dimension_scores: {
    completeness: number;
    accuracy: number;
    relevance: number;
    freshness: number;
    coherence: number;
  };
  gaps: GapAnalysis;
  warnings: string[];
  needs_clarification: boolean;
}
```

**Configuration:**

```yaml
evaluate:
  weights:
    completeness: 0.30
    accuracy: 0.25
    relevance: 0.20
    freshness: 0.15
    coherence: 0.10
  gap_detection: true
  contradiction_detection: true
  min_sources_for_confidence: 3
  eval_model: claude-3-haiku  # fast, cheap evaluation
  strictness: medium  # low | medium | high
```

---

### 3. Decide

**Purpose:** Determine next action based on evaluation

The Decision component implements the core convergence logic: when to keep going, when to stop, when to ask.

**Decision Tree:**

```
                    EvaluationResult
                          │
                          ▼
              ┌───────────────────────┐
              │ confidence >= 0.85    │───Yes───▶ OUTPUT
              │ AND coverage >= 0.90  │
              └───────────┬───────────┘
                          │ No
                          ▼
              ┌───────────────────────┐
              │ iteration >= max      │───Yes───▶ OUTPUT (best effort)
              └───────────┬───────────┘
                          │ No
                          ▼
              ┌───────────────────────┐
              │ cost >= budget        │───Yes───▶ OUTPUT (budget constrained)
              └───────────┬───────────┘
                          │ No
                          ▼
              ┌───────────────────────┐
              │ needs_clarification   │───Yes───▶ ASK
              └───────────┬───────────┘
                          │ No
                          ▼
              ┌───────────────────────┐
              │ diminishing_returns   │───Yes───▶ OUTPUT
              └───────────┬───────────┘
                          │ No
                          ▼
                       CONTINUE
```

**Diminishing Returns Detection:**

```python
def is_diminishing_returns(state: PipelineState) -> bool:
    if len(state.convergence_trend) < 3:
        return False
    
    last_3_gains = state.convergence_trend[-3:]
    avg_gain = sum(last_3_gains) / 3
    
    return avg_gain < 0.05  # Less than 5% improvement per iteration
```

**Decision Output:**

```typescript
type Decision = 
  | { action: "CONTINUE"; reason: string; strategy_adjustment?: string }
  | { action: "OUTPUT"; reason: string; confidence: number }
  | { action: "ASK"; question: string; options?: string[] };
```

**Configuration:**

```yaml
decide:
  confidence_threshold: 0.85
  coverage_threshold: 0.90
  max_iterations: 10
  cost_budget: 0.50
  diminishing_returns_window: 3
  diminishing_returns_threshold: 0.05
  decision_mode: deterministic  # deterministic | probabilistic
  ask_threshold: 0.5  # confidence below this triggers ASK
```

---

### 4. Refine

**Purpose:** Adjust strategy for next iteration

When decision is CONTINUE, Refine determines how to improve the next iteration.

**Refinement Strategies:**

| Strategy | When | Action |
|----------|------|--------|
| Expand | Coverage low, confidence high | Broaden search scope |
| Narrow | Coverage high, confidence low | Focus on weak areas |
| Pivot | Stuck after 3 iterations | Try different angle |
| Deepen | Partial coverage of key topic | More detail on specific aspect |

**Strategy Selection:**

```python
def select_strategy(eval: EvaluationResult, state: PipelineState) -> Strategy:
    if eval.coverage < 0.5:
        return Strategy.EXPAND
    
    if eval.confidence < 0.5 and eval.coverage > 0.7:
        return Strategy.NARROW
    
    if is_stuck(state):  # No improvement in 3 iterations
        return Strategy.PIVOT
    
    if has_partial_coverage(eval.gaps):
        return Strategy.DEEPEN
    
    return Strategy.EXPAND  # Default
```

**Query Rewriting:**

```typescript
interface RefinedQuery {
  original_query: string;
  refined_query: string;
  strategy_used: string;
  focus_areas: string[];      // What to emphasize
  exclude_areas: string[];    // What to skip (already covered)
  source_preferences: string[]; // Prefer certain source types
}
```

**Configuration:**

```yaml
refine:
  strategy_selection: automatic  # automatic | manual
  allow_query_rewrite: true
  allow_source_preference: true
  pivot_after_iterations: 3
  refinement_model: claude-3-haiku
  query_diversity: medium  # low | medium | high
```

---

## Convergence Criteria

The system stops iterating when ANY of these conditions is met:

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| Confidence | ≥ 0.85 | Answer is reliable enough |
| Coverage | ≥ 0.90 | Query is substantially addressed |
| Diminishing returns | < 5% gain/iter | Further research won't help |
| Max iterations | 10 | Prevent infinite loops |
| Budget exhausted | $0.50 default | Cost control |
| User interrupt | Any | User override |

---

## State Machine

```
         ┌──────────────────────────────────────────────────────────┐
         │                                                          │
         ▼                                                          │
┌─────────────┐                                                     │
│    START    │                                                     │
└──────┬──────┘                                                     │
       │                                                            │
       ▼                                                            │
┌─────────────┐     ┌─────────────┐     ┌─────────────┐            │
│ RESEARCHING │────▶│  EVALUATE   │────▶│   DECIDE    │            │
└─────────────┘     └─────────────┘     └──────┬──────┘            │
       ▲                                       │                    │
       │                    ┌──────────────────┼──────────────────┐│
       │                    │                  │                  ││
       │                    ▼                  ▼                  ▼│
       │            ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
       │            │  CONTINUE   │    │   OUTPUT    │    │    ASK      │
       │            └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                   │                  │                  │
       │                   ▼                  ▼                  ▼
       │            ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
       └────────────│   REFINE    │    │  COMPLETE   │    │   WAITING   │
                    └─────────────┘    └─────────────┘    └──────┬──────┘
                                                                 │
                                                                 ▼
                                                          ┌─────────────┐
                                                          │   RESUME    │
                                                          └──────┬──────┘
                                                                 │
                                                                 └─────────┘
```

---

## Integration

**Input from Exploration Layer:**

```typescript
interface ExplorationOutput {
  questions: ResearchQuestion[];
  profile: UserProfile;
  context: ContextMap;
}
```

**Output to Inner Loop:**

```typescript
interface PipelineInput {
  query: QueryIntent;
  constraints: QueryConstraint[];
  focus_areas: string[];
  source_preferences: SourcePreference[];
}
```

**Output to User:**

```typescript
interface FinalOutput {
  answer: SynthesizedAnswer;
  confidence: number;
  coverage: number;
  iterations_used: number;
  cost: number;
  gaps_remaining: string[];
  sources_used: number;
}
```

---

## Configuration Reference

```yaml
reasoning_engine:
  enabled: true
  
  state_monitor:
    track_confidence: true
    track_coverage: true
    track_cost: true
    confidence_model: weighted_average
    coverage_method: aspect_ratio
  
  evaluate:
    weights:
      completeness: 0.30
      accuracy: 0.25
      relevance: 0.20
      freshness: 0.15
      coherence: 0.10
    gap_detection: true
    contradiction_detection: true
    strictness: medium
  
  decide:
    confidence_threshold: 0.85
    coverage_threshold: 0.90
    max_iterations: 10
    cost_budget: 0.50
    diminishing_returns_window: 3
    diminishing_returns_threshold: 0.05
  
  refine:
    strategy_selection: automatic
    allow_query_rewrite: true
    pivot_after_iterations: 3
```

---

## Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Avg iterations | Mean iterations to convergence | < 5 |
| Convergence rate | % queries that converge vs timeout | > 80% |
| Early exit accuracy | Quality of early-exit answers | > 90% |
| Cost per quality point | $ per 0.1 confidence | < $0.01 |
| Decision reversal rate | % of CONTINUE→OUTPUT reversals | < 5% |
