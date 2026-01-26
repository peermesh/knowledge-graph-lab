# Pipeline Layer Experimentation & Hot-Swap Architecture

**Status:** Vision Document
**Related:** WO-005, Infinite Layers Philosophy

---

## Core Concept

The KGL pipeline should support **parallel layer experimentation** - running multiple versions of a layer simultaneously to learn what works, while maintaining operational stability.

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION PATH                          │
│  Input → [Layer A v1] → [Layer B v1] → [Layer C v1] → Out  │
└─────────────────────────────────────────────────────────────┘
                ↓ shadow traffic
┌─────────────────────────────────────────────────────────────┐
│                   EXPERIMENT PATH                           │
│  Input → [Layer A v2] → [Layer B v1] → [Layer C v1] → Log  │
└─────────────────────────────────────────────────────────────┘
```

---

## Why This Matters

### 1. Learn What Works Without Breaking Production

Traditional approach: Build → Deploy → Hope
KGL approach: Build → Shadow Run → Compare → Promote if better

**Example:** Testing a new predicate extraction prompt
- Production: Uses current `gapAnalysis` prompt (80% accuracy)
- Experiment: Uses new prompt with few-shot examples
- Both run on same input, results compared
- If experiment > production, swap layers

### 2. Rebuild Layers Without Downtime

When upgrading a layer (like the Ontology Mapper), the system continues running on the old layer while the new one is being built and validated.

```typescript
interface LayerConfig {
  id: string;
  version: string;
  status: 'production' | 'experiment' | 'rebuilding' | 'deprecated';
  fallbackTo?: string;  // Which layer to use if this one fails
}
```

### 3. Multi-Map Parallel Processing

Run the same input through **multiple ontology configurations** simultaneously:

```
                    ┌→ [Ecological Lens] → Eco-Ontology
                    │
Input → Decompose → ├→ [Economic Lens]   → Econ-Ontology
                    │
                    └→ [Temporal Lens]   → Time-Ontology
```

Each lens produces its own layer of the graph. User can:
- View one lens at a time
- Overlay multiple lenses
- See where lenses agree/disagree (consensus nodes)

---

## Implementation Patterns

### Pattern 1: Shadow Layer Execution

```typescript
interface ShadowConfig {
  production: LayerConfig;
  experiments: LayerConfig[];
  compareMetrics: string[];  // ['accuracy', 'latency', 'coverage']
}

async function executeWithShadow(input: any, config: ShadowConfig) {
  // Always run production
  const prodResult = await runLayer(config.production, input);

  // Shadow run experiments (don't block)
  config.experiments.forEach(exp => {
    runLayer(exp, input).then(expResult => {
      logComparison(prodResult, expResult, config.compareMetrics);
    });
  });

  return prodResult;  // Return production result immediately
}
```

### Pattern 2: Layer Health & Auto-Fallback

```typescript
interface LayerHealth {
  layerId: string;
  successRate: number;      // Rolling 100 requests
  avgLatency: number;
  lastError?: string;
  status: 'healthy' | 'degraded' | 'failed';
}

async function executeWithFallback(input: any, primary: LayerConfig) {
  const health = getLayerHealth(primary.id);

  if (health.status === 'failed' && primary.fallbackTo) {
    console.warn(`Layer ${primary.id} failed, falling back to ${primary.fallbackTo}`);
    return executeWithFallback(input, getLayer(primary.fallbackTo));
  }

  try {
    return await runLayer(primary, input);
  } catch (error) {
    updateHealth(primary.id, { lastError: error.message });
    if (primary.fallbackTo) {
      return executeWithFallback(input, getLayer(primary.fallbackTo));
    }
    throw error;
  }
}
```

### Pattern 3: A/B Layer Testing

```typescript
interface ABTest {
  id: string;
  layerA: LayerConfig;
  layerB: LayerConfig;
  trafficSplit: number;  // 0.0 - 1.0 (% to layer B)
  metrics: ABMetrics;
}

async function executeABTest(input: any, test: ABTest) {
  const useB = Math.random() < test.trafficSplit;
  const layer = useB ? test.layerB : test.layerA;

  const result = await runLayer(layer, input);

  recordABMetric(test.id, {
    variant: useB ? 'B' : 'A',
    latency: result.latency,
    quality: await evaluateQuality(result)
  });

  return result;
}
```

### Pattern 4: Rebuild-in-Place

```typescript
interface RebuildConfig {
  currentLayer: LayerConfig;
  newLayer: LayerConfig;
  validationThreshold: number;  // Min quality score to promote
  validationSamples: number;    // How many samples to test
}

async function rebuildLayer(config: RebuildConfig) {
  // Mark new layer as rebuilding
  setLayerStatus(config.newLayer.id, 'rebuilding');

  // Get validation dataset
  const samples = await getHistoricalSamples(config.validationSamples);

  // Run both layers on samples
  const results = await Promise.all(samples.map(async sample => {
    const [current, rebuilt] = await Promise.all([
      runLayer(config.currentLayer, sample.input),
      runLayer(config.newLayer, sample.input)
    ]);
    return {
      sample,
      currentScore: evaluateAgainst(current, sample.expectedOutput),
      rebuiltScore: evaluateAgainst(rebuilt, sample.expectedOutput)
    };
  }));

  // Calculate improvement
  const avgCurrentScore = avg(results.map(r => r.currentScore));
  const avgRebuiltScore = avg(results.map(r => r.rebuiltScore));

  if (avgRebuiltScore >= config.validationThreshold &&
      avgRebuiltScore > avgCurrentScore) {
    // Promote new layer
    setLayerStatus(config.newLayer.id, 'production');
    setLayerStatus(config.currentLayer.id, 'deprecated');
    return { promoted: true, improvement: avgRebuiltScore - avgCurrentScore };
  }

  return { promoted: false, gap: config.validationThreshold - avgRebuiltScore };
}
```

---

## Application to KGL Pipeline

### Current Pipeline Layers

```
ROW 1: SIGNAL      → Input capture, intent detection
ROW 2: GENERATION  → Candidate topic generation (Wizard)
ROW 3: DECOMPOSE   → Topic → Atomic concepts
ROW 4: MAPPING     → Ontology induction (predicates)
ROW 5: INTEGRATION → Merge into global graph
ROW 6: REASONING   → Gap analysis, convergence check
ROW 7: OUTPUT      → Reports, visualizations
```

### Which Layers Can Be Swapped/Experimented

| Row | Layer | Hot-Swap? | Experiment Priority |
|-----|-------|-----------|---------------------|
| 1 | Signal | ✅ Yes | Low - stable |
| 2 | Generation | ✅ Yes | Medium - prompt tuning |
| 3 | Decompose | ✅ Yes | **HIGH - core upgrade** |
| 4 | Mapping | ✅ Yes | **HIGH - predicate quality** |
| 5 | Integration | ⚠️ Careful | Medium - merge strategies |
| 6 | Reasoning | ✅ Yes | High - convergence logic |
| 7 | Output | ✅ Yes | Low - presentation only |

### WO-005 Experiment Opportunity

During WO-005, we can:

1. **Keep old GraphLink layer running** as fallback
2. **Shadow run new OntologyTriple layer** on same inputs
3. **Compare predicate accuracy** between old (all RELATES_TO) and new (typed predicates)
4. **Gradually shift traffic** as confidence grows

```typescript
const WO005_MIGRATION_CONFIG: ABTest = {
  id: 'wo005-ontology-upgrade',
  layerA: { id: 'ontology-v1-graphlink', version: '1.0' },
  layerB: { id: 'ontology-v2-triples', version: '2.0' },
  trafficSplit: 0.1,  // Start with 10% to new layer
  metrics: {
    predicateAccuracy: [],
    userSatisfaction: [],
    graphCoherence: []
  }
};
```

---

## Multi-Lens Parallel Execution

Each lens can have its own layer configuration:

```typescript
interface LensLayerConfig {
  lensId: string;
  decompositionLayer: LayerConfig;
  mappingLayer: LayerConfig;
  integrationLayer: LayerConfig;
}

const LENS_CONFIGS: LensLayerConfig[] = [
  {
    lensId: 'ecological',
    decompositionLayer: { id: 'decompose-eco-v1', ... },
    mappingLayer: { id: 'map-eco-v1', emphasis: ['CAUSES', 'REQUIRES'] },
    ...
  },
  {
    lensId: 'economic',
    decompositionLayer: { id: 'decompose-econ-v1', ... },
    mappingLayer: { id: 'map-econ-v1', emphasis: ['CAUSES', 'PRECEDES'] },
    ...
  }
];

async function processWithAllLenses(input: any) {
  // Run all lenses in parallel
  const results = await Promise.all(
    LENS_CONFIGS.map(config => runLensPipeline(input, config))
  );

  // Each result is an ontology layer
  return {
    layers: results,
    consensus: findConsensusNodes(results),
    conflicts: findConflicts(results)
  };
}
```

---

## Learning from Experiments

### Metrics to Track

| Metric | What It Measures | Used For |
|--------|------------------|----------|
| Predicate Accuracy | % correct predicates vs human judgment | Layer promotion |
| Coverage | % of concepts connected | Gap detection |
| Coherence | Graph structure quality | Integration tuning |
| Latency | Processing time | Performance gating |
| User Corrections | How often users fix AI output | Feedback loop |

### Feedback Loop

```
Experiment → Metrics → Analysis → Hypothesis → New Experiment
     ↑                                              ↓
     └──────────── Improved Layer ←─────────────────┘
```

### Auto-Learning Pattern

```typescript
interface LayerLearning {
  layerId: string;
  feedbackHistory: Feedback[];
  promptVariants: PromptVariant[];
  currentBest: string;
}

async function learnFromFeedback(learning: LayerLearning, feedback: Feedback) {
  learning.feedbackHistory.push(feedback);

  // Every N feedbacks, generate new prompt variant
  if (learning.feedbackHistory.length % 50 === 0) {
    const newVariant = await generateImprovedPrompt(
      learning.currentBest,
      learning.feedbackHistory.slice(-50)
    );

    // Add to A/B test
    addExperimentVariant(learning.layerId, newVariant);
  }
}
```

---

## Key Principles

1. **Never break production** - Always have a working fallback
2. **Shadow before swap** - Test new layers on real traffic without serving results
3. **Measure everything** - Can't improve what you can't measure
4. **Gradual rollout** - 10% → 25% → 50% → 100%
5. **Learn continuously** - Feedback drives next experiment
6. **Lenses are parallel** - They don't replace each other, they coexist

---

## Implementation Priority

### Phase 1 (With WO-005)
- [ ] Add layer health tracking
- [ ] Implement simple fallback (OntologyTriple → GraphLink)
- [ ] Log metrics for predicate accuracy

### Phase 2 (Post WO-005)
- [ ] Shadow execution framework
- [ ] A/B testing infrastructure
- [ ] Multi-lens parallel processing

### Phase 3 (Future)
- [ ] Auto-learning from feedback
- [ ] Prompt variant generation
- [ ] Autonomous layer optimization

---

## Related Documents

- [Infinite Layers Vision](./VISION_INFINITE_LAYERS.md)
- [Master Pipeline Architecture](../foundation/05-MASTER-PIPELINE-ARCHITECTURE.md)
- [WO-005 Integration Strategy](../../.dev/context/WO_005_INTEGRATION_STRATEGY.md)

---

*The pipeline should be a living, learning system - not a static artifact.*
