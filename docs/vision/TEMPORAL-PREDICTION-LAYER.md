# Temporal Prediction Layer

**Status:** Vision Document
**Work Order:** WO-VIS-012
**Created:** 2026-01-27
**Related:** [Master Pipeline Architecture](../foundation/05-MASTER-PIPELINE-ARCHITECTURE.md), [Pipeline Layer Experimentation](./PIPELINE-LAYER-EXPERIMENTATION.md), [Vision Index](./VISION_INDEX_TOC.md)

---

## 1. Introduction: Temporal Intelligence in Knowledge Graphs

Knowledge graphs traditionally represent static snapshots of relationships. A concept *is-a* category, an entity *causes* an outcome, a process *requires* a dependency. But the real world is not static. Relationships form, strengthen, weaken, and dissolve over time. Technologies emerge, mature, and become obsolete. Research fields converge, diverge, and spawn new disciplines.

The Knowledge Graph Lab's Temporal Prediction Layer transforms the knowledge graph from a static map into a **living timeline** -- one that remembers the past, understands the present, and forecasts the future.

This document specifies how temporal dimensions enable predictive graph analysis, allowing KGL to "play forward" and predict future relationship states. It covers the theory of time-aware modeling, the mechanics of temporal link prediction (TLP), and the integration of predictive capabilities with the reasoning engine.

### Why Temporal Intelligence Matters

Static graphs answer: "What is connected to what?"
Temporal graphs answer: "What *will be* connected to what, and *when*?"

Consider the difference:
- **Static:** "Kubernetes relates to container orchestration"
- **Temporal:** "Docker (2013) preceded Kubernetes (2015), which preceded service mesh adoption (2018), which is converging with eBPF-based networking (2024+). Predicted: eBPF will subsume traditional service mesh within 3 years."

The temporal layer enables KGL to reason about trajectories, not just positions.

---

## 2. Time-Aware Relationship Modeling

### 2.1 Temporal Attributes on Edges

Every `OntologyTriple` in KGL carries a `temporalContext` that encodes when the relationship holds and how it evolves:

```typescript
interface TemporalContext {
  // When did this relationship begin?
  startTime?: ISO8601;

  // When does/did this relationship end? (null = ongoing)
  endTime?: ISO8601 | null;

  // Is this relationship part of a sequence?
  isSequential: boolean;

  // How is this relationship changing?
  trend: 'strengthening' | 'stable' | 'weakening' | 'emerging' | 'dissolved';

  // Temporal resolution (how granular is our time knowledge?)
  resolution: 'year' | 'quarter' | 'month' | 'week' | 'day' | 'approximate';

  // Confidence that the temporal bounds are accurate
  temporalConfidence: number; // 0.0 - 1.0
}
```

### 2.2 Time-Stamped Entity Properties

Entities themselves evolve. A `ConceptNode` tracks its own temporal state:

```typescript
interface TemporalEntityState {
  // When was this concept first observed in sources?
  firstObserved: ISO8601;

  // When was this concept last referenced?
  lastObserved: ISO8601;

  // Lifecycle phase
  phase: 'emerging' | 'growing' | 'mature' | 'declining' | 'historical';

  // Observation frequency over time (for trend detection)
  observationHistory: Array<{
    period: ISO8601;
    frequency: number;
    sourceCount: number;
  }>;
}
```

### 2.3 Temporal Versioning of Concepts

Concepts change meaning over time. "Machine Learning" in 2010 connoted statistical methods and SVMs. By 2024 it primarily connotes deep learning and transformers. KGL tracks this semantic drift:

```
ConceptNode("Machine Learning")
  ├── version(2010): { associations: ["SVM", "Random Forest", "Feature Engineering"] }
  ├── version(2018): { associations: ["Deep Learning", "CNN", "RNN", "Transfer Learning"] }
  └── version(2024): { associations: ["Transformers", "LLMs", "Foundation Models", "RLHF"] }
```

This enables queries like: "What did 'Machine Learning' mean in 2015 vs 2024?" and "Which associations emerged, which disappeared?"

### 2.4 Historical, Current, and Future States

The temporal model partitions the graph into three regions:

```
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │   HISTORICAL  │    │   CURRENT    │    │   PREDICTED  │
  │               │    │              │    │              │
  │  Dissolved    │───▶│  Active      │───▶│  Forecasted  │
  │  relationships│    │  relationships│   │  relationships│
  │               │    │              │    │              │
  │  confidence:  │    │  confidence: │    │  confidence: │
  │  high (known) │    │  high (obs.) │    │  variable    │
  └──────────────┘    └──────────────┘    └──────────────┘
```

- **Historical:** Relationships that existed but no longer hold. Preserved for pattern learning.
- **Current:** Relationships observed in recent sources. Actively maintained.
- **Predicted:** Relationships forecast by TLP. Tagged with confidence scores and time horizons.

---

## 3. Temporal Link Prediction (TLP)

### 3.1 Definition and Theory

Temporal Link Prediction (TLP) is the task of forecasting which edges will appear (or disappear) in a knowledge graph at a future time step, given the graph's historical evolution.

Formally:

```
Given:  G(t₁), G(t₂), ..., G(tₙ)  -- graph snapshots at times t₁ through tₙ
Predict: G(tₙ₊₁)                    -- the graph at a future time tₙ₊₁
```

TLP leverages three signal categories:

1. **Structural signals:** Nodes that share many neighbors but lack a direct edge are likely to form one (common neighbors, Jaccard similarity, Adamic-Adar index).
2. **Temporal signals:** Relationships that follow recurring temporal patterns (seasonal adoption cycles, technology succession patterns).
3. **Semantic signals:** Concepts whose meanings are converging (detected via embedding drift) are likely to form new edges.

### 3.2 Prediction Approaches

KGL employs a layered prediction strategy, from simple heuristics to learned models:

**Layer 1: Heuristic Predictors (No Training Required)**

| Method | Signal | Example |
|--------|--------|---------|
| Common Neighbors | Structural | If "Rust" and "WebAssembly" share 8 neighbors but no direct edge, predict a link |
| Temporal Recurrence | Temporal | If "Framework X" edges form every Q1, predict Q1 formation |
| Sequence Completion | Temporal | If pattern is A→B→C and we see A→B, predict C |
| Semantic Convergence | Semantic | If embeddings of two concepts drift closer over 3 periods, predict edge |

**Layer 2: Statistical Models (Light Training)**

Pattern matching on historical edge formation rates, using features like:
- Time since last edge formation in neighborhood
- Node degree growth rate
- Reciprocity patterns (if A→B formed, likelihood of B→A)
- Triadic closure rate (how fast open triads close)

**Layer 3: Graph Neural Networks (Future - Out of Scope for This Document)**

Temporal GNN architectures (TGN, TGAT, DyRep) that learn continuous-time representations. These are documented in future implementation work orders.

### 3.3 Training on Historical Patterns

TLP models are trained on the graph's own history using a sliding window approach:

```
Timeline:  ──[t₁]──[t₂]──[t₃]──[t₄]──[t₅]──[t₆]──▶

Training:  [t₁─t₃] → predict [t₄]   ✓ compare with actual
           [t₂─t₄] → predict [t₅]   ✓ compare with actual
           [t₃─t₅] → predict [t₆]   ✓ compare with actual

Inference: [t₄─t₆] → predict [t₇]   ? this is the forecast
```

Each window captures structural evolution, allowing the model to learn domain-specific formation patterns (e.g., in technology domains, "library" → "framework" → "ecosystem" transitions take ~2-4 years).

### 3.4 Forecasting Future Connections

The output of TLP is a ranked list of predicted edges with metadata:

```typescript
interface PredictedEdge {
  sourceId: string;
  targetId: string;
  predictedPredicate: PredicateType;
  confidence: number;           // 0.0 - 1.0
  predictedTimeframe: {
    earliest: ISO8601;
    mostLikely: ISO8601;
    latest: ISO8601;
  };
  evidenceBasis: string[];      // Which historical patterns support this
  predictorLayer: 1 | 2 | 3;   // Which prediction method generated this
}
```

---

## 4. "Play Forward" Simulation Mechanics

### 4.1 Graph State Simulation

"Play Forward" is KGL's ability to project the knowledge graph into the future. Given the current graph state and TLP predictions, the system generates a simulated future graph:

```
┌─────────────────────────────────────────────────────────┐
│                    PLAY FORWARD ENGINE                    │
│                                                          │
│  Current Graph ──▶ TLP Predictions ──▶ Simulated Graph  │
│  G(t=now)          ΔG(Δt)              G(t=now+Δt)      │
│                                                          │
│  Parameters:                                             │
│  ├── Time horizon: how far ahead to simulate             │
│  ├── Confidence threshold: min prediction confidence     │
│  ├── Scenario: optimistic / baseline / conservative      │
│  └── Focus area: subgraph to simulate (optional)         │
└─────────────────────────────────────────────────────────┘
```

The simulation applies predicted edges incrementally, respecting temporal ordering and dependency chains.

### 4.2 Scenario Exploration

Play Forward supports multiple scenario modes that apply different filters to predictions:

**Optimistic Scenario:** Include all predictions with confidence >= 0.3. Shows the maximum possible evolution -- useful for identifying opportunities.

**Baseline Scenario:** Include predictions with confidence >= 0.6. Shows the most likely evolution -- useful for planning.

**Conservative Scenario:** Include only predictions with confidence >= 0.8. Shows near-certain changes -- useful for risk assessment.

**Custom Scenario:** User-defined confidence thresholds per predicate type. For example: high threshold for CAUSES predictions (need strong evidence), lower threshold for RELATES_TO (more exploratory).

### 4.3 Confidence-Weighted Futures

Each simulated future state carries aggregate confidence:

```
Simulated Graph Confidence = Π(edge_confidence) for all predicted edges

But this product would approach 0 for large graphs.
Instead, KGL uses:

  Graph Confidence = mean(edge_confidence) × coverage_factor

  where coverage_factor = predicted_edges / expected_edges
```

This yields a single metric for how "trustworthy" a given simulated future is.

### 4.4 Multiple Timeline Branching

For high-impact predictions, Play Forward can generate branching timelines:

```
                              ┌── Timeline A: "Rust displaces C++ in systems"
                              │   (confidence: 0.45, horizon: 5yr)
                              │
Current Graph ── fork point ──├── Timeline B: "C++ evolves with safe subset"
                              │   (confidence: 0.35, horizon: 3yr)
                              │
                              └── Timeline C: "Both coexist, domain-split"
                                  (confidence: 0.65, horizon: 2yr)
```

Users can explore each timeline independently, compare outcomes, and identify which early signals would indicate which timeline is materializing.

---

## 5. Integration with Reasoning Engine

### 5.1 Outer Loop Decision-Making with Predictions

The KGL reasoning engine (Outer Loop) uses temporal predictions as an additional signal when making decisions:

```
┌─────────────────────────────────────────────────────────┐
│                    OUTER LOOP (Reasoning)                 │
│                                                          │
│  Evaluate ──▶ Consider Predictions ──▶ Decide ──▶ Act   │
│                                                          │
│  Standard signals:          Temporal signals:            │
│  ├── Confidence (85%)       ├── Predicted gaps           │
│  ├── Coverage (90%)         ├── Emerging connections     │
│  ├── Diminishing returns    ├── Weakening relationships  │
│  └── Budget limits          └── Convergence forecasts    │
└─────────────────────────────────────────────────────────┘
```

The reasoning engine can now make decisions like:
- "This topic area is predicted to converge with field X in 6 months -- proactively expand research into X"
- "Relationship R is weakening -- flag for re-verification before next report"
- "New edge predicted between A and B with high confidence -- prioritize exploration of the connection"

### 5.2 Uncertainty Handling in Reasoning

Predictions carry inherent uncertainty. The reasoning engine handles this through tiered response:

| Confidence Range | Reasoning Action |
|-----------------|------------------|
| 0.8 - 1.0 | Treat as likely fact. Include in reports with temporal qualifier. |
| 0.6 - 0.8 | Treat as strong hypothesis. Flag for verification. Auto-queue supporting research. |
| 0.4 - 0.6 | Treat as speculation. Present only when user requests "exploratory" mode. |
| 0.0 - 0.4 | Treat as weak signal. Log for pattern tracking but do not surface. |

### 5.3 Human-in-the-Loop for High-Uncertainty Predictions

When predictions have high impact but moderate confidence (0.4 - 0.7), the system escalates to the human:

```
System: "I predict that [Quantum Computing] will form a REQUIRES
         relationship with [Post-Quantum Cryptography] within 2 years
         (confidence: 0.62). Should I expand research into this
         connection?"

User options:
  [Expand] - Queue research into the predicted connection
  [Watch]  - Track the prediction but don't act yet
  [Dismiss] - Mark prediction as unlikely (feeds back to TLP)
```

This creates a feedback loop: human responses improve future prediction quality through the Knowledge Graph Tuning (KGT) system.

### 5.4 Prediction-Driven Expansion Triggers

Temporal predictions create a new type of expansion trigger for the reasoning engine:

```yaml
Traditional triggers:
  - Gap detected: "Topic X has no subtopics"
  - Conflict detected: "Sources disagree on X→Y"
  - Low coverage: "Only 2 of 8 subtopics explored"

Temporal triggers (NEW):
  - Convergence predicted: "Fields A and B predicted to merge"
  - Emergence detected: "New concept C appearing in A's neighborhood"
  - Dissolution warning: "Relationship X→Y weakening, may dissolve"
  - Succession pattern: "Technology X following same trajectory as deprecated Y"
```

---

## 6. Temporal Ontology Structure

### 6.1 Time as an Ontological Dimension

In KGL's ontology, time is not metadata -- it is a **first-class dimension** alongside the multi-lens system (Ecological, Economic, Social, Technical):

```
                    Ecological    Economic    Social    Technical
                    ──────────    ────────    ──────    ─────────
  Past (t-n)    │     ●            ●          ●          ●
                │
  Present (t)   │     ●            ●          ●          ●
                │
  Future (t+n)  │     ◐            ◐          ◐          ◐
                │
                ▼ time

  ● = observed relationship    ◐ = predicted relationship
```

This creates a 3D space: **Concept x Lens x Time** -- enabling queries like "Show me the Economic lens view of this topic, projected 2 years forward."

### 6.2 Temporal Provenance Tracking

Every temporal assertion in the graph carries provenance that answers: "Why do we believe this temporal relationship?"

```typescript
interface TemporalProvenance {
  // What source asserted this temporal relationship?
  sourceType: 'observation' | 'inference' | 'prediction' | 'user_assertion';

  // If observation: which document/source?
  sourceDocuments?: string[];

  // If inference: which pattern was applied?
  inferencePattern?: string;

  // If prediction: which TLP method and what evidence?
  predictionMethod?: {
    layer: 1 | 2 | 3;
    evidenceEdges: string[];
    modelVersion: string;
  };

  // When was this provenance last verified?
  lastVerified: ISO8601;

  // Has this been human-reviewed?
  humanReviewed: boolean;
}
```

### 6.3 Concept Evolution Over Time

KGL tracks how concepts evolve through lifecycle phases, enabling the system to reason about maturity:

```
  Emerging ──▶ Growing ──▶ Mature ──▶ Declining ──▶ Historical
     │            │           │           │             │
   Few refs    Rapid      Stable      Fewer new     Archival
   High        growth     Many refs   references    references
   novelty     in refs    Stable      Replacement   only
               New edges  topology    concepts
                                      emerging
```

The system detects phase transitions by monitoring:
- **Reference frequency changes** (growth rate of incoming edges)
- **Neighborhood stability** (how much the concept's connections are changing)
- **Replacement signals** (new concepts forming edges to the same neighbors)

### 6.4 Temporal Consistency Constraints

The temporal ontology enforces constraints to prevent contradictions:

1. **Causal ordering:** If A CAUSES B, then A.startTime <= B.startTime
2. **Precedence consistency:** If A PRECEDES B and B PRECEDES C, then A PRECEDES C (transitivity)
3. **Existence constraints:** A relationship cannot start before both endpoint entities exist
4. **Dissolution propagation:** If a concept moves to "historical" phase, dependent relationships should be re-evaluated
5. **Prediction decay:** Predicted edges that are not observed within their predicted timeframe have their confidence reduced

---

## 7. Prediction Confidence Modeling

### 7.1 Confidence Scores for Predictions

Each prediction carries a composite confidence score derived from multiple factors:

```
Confidence(predicted_edge) = w₁·structural + w₂·temporal + w₃·semantic + w₄·historical

where:
  structural = commonNeighborScore(source, target)
  temporal   = patternMatchScore(historical_sequences)
  semantic   = embeddingSimilarityTrend(source, target)
  historical = baseRateFormation(predicate_type, domain)

Default weights: w₁=0.3, w₂=0.3, w₃=0.2, w₄=0.2
(Tunable per domain via the Recipe system)
```

### 7.2 Uncertainty Quantification

Beyond point confidence, KGL provides uncertainty bounds:

```typescript
interface PredictionUncertainty {
  // Point estimate
  confidence: number;

  // Confidence interval (e.g., 95%)
  confidenceInterval: {
    lower: number;
    upper: number;
    level: number; // 0.95 for 95% CI
  };

  // Sources of uncertainty
  uncertaintySources: Array<{
    source: 'data_sparsity' | 'pattern_novelty' | 'conflicting_signals' | 'temporal_distance';
    contribution: number; // How much this source contributes to total uncertainty
  }>;

  // How would additional data reduce uncertainty?
  informationGain: {
    additionalSourcesNeeded: number;
    expectedConfidenceWithMoreData: number;
  };
}
```

### 7.3 Error Bounds and Sensitivity

Temporal predictions include sensitivity analysis:

- **Time sensitivity:** How much does confidence change if the predicted timeframe shifts by +/- 1 period?
- **Evidence sensitivity:** If we remove the strongest supporting evidence, does the prediction still hold?
- **Domain sensitivity:** Does this prediction pattern hold across similar domains, or is it domain-specific?

```
Prediction: "WebAssembly will REQUIRE WASI within 2 years"
Confidence: 0.72

Sensitivity:
  ├── Remove strongest evidence (Chrome adoption data): confidence drops to 0.58
  ├── Shift timeframe +1 year: confidence increases to 0.81
  ├── Shift timeframe -1 year: confidence decreases to 0.49
  └── Cross-domain check (similar patterns in Java/JVM): confidence supported at 0.68
```

### 7.4 Confidence Propagation Through the Graph

When predicted edges are added to the simulated graph, downstream reasoning must account for accumulated uncertainty:

```
Known:     A ──(0.95)──▶ B        (observed, high confidence)
Predicted: B ──(0.70)──▶ C        (TLP prediction)
Derived:   A ──(0.67)──▶ C        (transitive, 0.95 × 0.70 = 0.67)
```

**Propagation rule:** Transitive confidence = product of edge confidences along the path, with a floor of 0.1 (to prevent collapse to zero in long chains).

**Attenuation:** Each hop through a predicted (vs observed) edge applies an additional 0.9 attenuation factor to account for compounding uncertainty.

---

## 8. Use Cases and Applications

### 8.1 Market Trend Prediction

**Scenario:** A user is researching "edge computing" and wants to understand where the market is heading.

**How Play Forward helps:**

1. KGL observes historical patterns: cloud computing (2010) → containerization (2014) → edge computing (2018) → ...
2. TLP identifies structural parallels with previous technology adoption curves
3. Play Forward projects: edge computing is predicted to form strong REQUIRES edges with "5G private networks" and "AI inference at edge" within 18 months
4. The reasoning engine flags: "Competitive landscape is predicted to consolidate -- three emerging players share 12 common neighbors but no direct edges. Merger/acquisition predicted with confidence 0.55."

**User value:** Strategic planning informed by graph-derived trend intelligence, not just keyword frequency.

### 8.2 Research Path Forecasting

**Scenario:** A researcher is exploring "CRISPR gene editing" and wants to identify promising interdisciplinary connections.

**How Play Forward helps:**

1. KGL maps the current research landscape: CRISPR connects to genetics, bioethics, agriculture, medicine
2. TLP detects converging embeddings between "CRISPR" and "synthetic biology" and "computational protein design"
3. Play Forward projects: a new cluster is forming at the intersection of these fields, predicted to emerge as "programmable biology" within 2-3 years
4. The system recommends: "Expand research into computational protein design -- predicted convergence with your CRISPR research with confidence 0.68"

**User value:** Early identification of interdisciplinary frontiers before they become established fields.

### 8.3 Technology Stack Evolution

**Scenario:** A technical lead is mapping their organization's technology stack and planning upgrades.

**How Play Forward helps:**

1. KGL maps the current stack: React (frontend) → Express (API) → PostgreSQL (DB) → Docker (deploy)
2. TLP detects that Express is entering "declining" phase -- its neighborhood is losing edges while Fastify and Hono gain them
3. Play Forward projects: Express will lose its REQUIRES relationship with Node.js best practices within 12 months as alternatives mature
4. The system generates a migration timeline: "Based on similar framework succession patterns (jQuery→React took 3 years), plan Express→Fastify migration for Q3"

**User value:** Data-driven technology decisions based on ecosystem evolution patterns.

### 8.4 Organizational Knowledge Growth

**Scenario:** A knowledge manager wants to identify emerging skill gaps in their organization.

**How Play Forward helps:**

1. KGL maps the current organizational knowledge graph: teams, skills, projects, dependencies
2. TLP identifies that the "ML Ops" concept is forming edges to 5 existing projects but has no team-skill edge
3. Play Forward projects: "ML Ops" will become a REQUIRES dependency for 3 active projects within 6 months
4. The system recommends: "Knowledge gap predicted -- no team member has ML Ops skills, but 3 projects will require it by Q3. Recommend training or hiring."

**User value:** Proactive workforce planning driven by knowledge graph trajectory analysis.

---

## 9. Future Evolution of Temporal Capabilities

### Phase 1: Heuristic Predictors (Current Target)
- Common neighbor-based link prediction
- Temporal sequence completion (A→B→? pattern matching)
- Semantic convergence detection via embedding drift
- Basic Play Forward with single-scenario projection

### Phase 2: Statistical Models
- Trained temporal feature models (edge formation rate prediction)
- Multi-scenario Play Forward with branching timelines
- Automated sensitivity analysis
- Integration with KGT feedback loop (human corrections improve predictions)

### Phase 3: Graph Neural Networks (Future)
- Temporal Graph Networks (TGN) for continuous-time prediction
- Attention-based temporal aggregation (TGAT)
- Dynamic representation learning (DyRep)
- Real-time prediction updates as graph evolves

### Phase 4: Causal Temporal Reasoning (Aspirational)
- Causal discovery from temporal patterns (not just correlation)
- Counterfactual reasoning: "What if this edge had NOT formed?"
- Intervention modeling: "If we add this edge, what happens downstream?"
- Integration with external event streams (news, market data) for exogenous shock modeling

---

## 10. Relationship to Other Vision Documents

### Master Pipeline Architecture
The temporal layer corresponds to the **TEMPORAL-TAG** stage in Row 3 (Decomposition Layer) of the [Master Pipeline Architecture](../foundation/05-MASTER-PIPELINE-ARCHITECTURE.md). It processes `ConceptNode` and `OntologyTriple` structures, adding temporal dimensions before provenance linking.

### Pipeline Layer Experimentation
Temporal prediction models are prime candidates for [shadow layer experimentation](./PIPELINE-LAYER-EXPERIMENTATION.md). Different TLP approaches (heuristic vs. statistical) can run in parallel on the same input, with results compared to determine which predictor performs best for a given domain.

### Recursive Ontology (WO-VIS-010)
The temporal layer adds a time dimension to the multi-lens ontology system. Each lens (Ecological, Economic, Social, Technical) can be viewed at different time slices, creating a **4D knowledge space** (concept x lens x time x confidence).

### Infinite Loop Learning (WO-VIS-011)
Temporal predictions feed into the self-improvement loop. When predictions are confirmed or refuted by new observations, this signal flows back to the Knowledge Graph Tuning (KGT) system, creating Golden Tuples for temporal patterns and Negative Constraints for failed predictions.

---

**Document Version:** 1.0.0
**Last Updated:** 2026-01-27
**Maintained By:** Knowledge Graph Lab Core Team
**Next Review:** 2026-02-27
