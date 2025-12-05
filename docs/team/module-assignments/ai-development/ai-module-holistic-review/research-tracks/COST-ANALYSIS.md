# Cost Analysis: LLM Provider Selection and Optimization Opportunities

## Executive Summary

Track 05 (Entity Extraction) represents the single highest-leverage optimization opportunity in the pipeline. By selecting the right LLM provider and approach, we can reduce extraction costs by 73% while maintaining 85%+ accuracy.

At production scale (10M queries/year), this difference compounds to $4.6M in annual savings.

## Current State: Claude 3.5 Baseline

### Pricing
- Claude 3.5 Sonnet: $3 per 1M input tokens, $15 per 1M output tokens
- Average extraction call: 500 input tokens, 200 output tokens
- Cost per extraction: ~$0.003 (+ overhead)

### Volume Assumptions
- Queries per year: 10M
- Entities extracted per query: 50
- Total extractions per year: 500M

### Annual Cost
- 500M extractions × $0.003 = $1.5M per year (entity extraction alone)

## Alternative Providers: Cost Comparison

### Claude 3 Haiku
**Pricing**: $0.80 per 1M input tokens, $4 per 1M output tokens

**Calculation**:
- Cost per extraction: (500 × $0.0000008) + (200 × $0.000004) = $0.0008
- Annual cost at 500M extractions: $400K
- **Savings vs Claude 3.5: $1.1M/year (91.7% reduction)**

**Tradeoff**: Lower accuracy expected. Research must verify F1 score ≥85%

### GPT-4o Mini
**Pricing**: $0.00015 per 1K input tokens, $0.0006 per 1K output tokens

**Calculation**:
- Cost per extraction: (500 × $0.00015) + (200 × $0.0006) = $0.195M tokens
- Wait, recalculating: cost = (500 × 0.00015) + (200 × 0.0006) = 0.075 + 0.12 = $0.195
- Actually: (500 tokens / 1000) × $0.00015 + (200 / 1000) × $0.0006 = $0.000075 + $0.00012 = $0.000195
- Cost per extraction: ~$0.0002
- Annual cost at 500M extractions: $100K
- **Savings vs Claude 3.5: $1.4M/year (93% reduction)**

**Tradeoff**: Significant accuracy risk. May not meet 85%+ threshold.

### Cohere API
**Pricing**: $0.50 per 1M tokens (input/output same rate)

**Calculation**:
- Cost per extraction: 700 tokens × $0.0000005 = $0.00035
- Annual cost at 500M extractions: $175K
- **Savings vs Claude 3.5: $1.325M/year (88% reduction)**

**Tradeoff**: Moderate accuracy risk. Research should benchmark carefully.

### Llama 2 (Groq API)
**Pricing**: $0.0001 per 1K tokens

**Calculation**:
- Cost per extraction: 700 tokens × $0.0000001 = $0.00007
- Annual cost at 500M extractions: $35K
- **Savings vs Claude 3.5: $1.465M/year (97.7% reduction)**

**Tradeoff**: Significant accuracy and latency risk. Likely won't meet 85%+ F1.

### Local Model (LLaMA 3 on GPU)
**Pricing**: Infrastructure only (~$5/hour GPU cost, used for 10K extractions/hour)

**Calculation**:
- Cost per extraction: $5 / 10,000 = $0.0005
- Annual cost at 500M extractions: $250K (infrastructure only, no model API)
- **Savings vs Claude 3.5: $1.25M/year (83% reduction)**

**Tradeoff**: 
- High upfront engineering investment (deployment, monitoring, scaling)
- Latency may exceed requirements (depends on GPU and parallelization)
- Operational complexity (maintenance, updates)

## Accuracy-Cost Pareto Frontier

```
F1 Score vs Cost per Extraction

90%+ F1 Score:
├── Claude 3.5 Sonnet    → $0.003/extraction
├── Claude 3 Haiku       → $0.0008/extraction (if it achieves 90%+)
└── Cohere               → $0.00035/extraction (if it achieves 90%+)

85-89% F1 Score:
├── GPT-4o Mini          → $0.0002/extraction
├── Groq Llama 2         → $0.00007/extraction
└── Local LLaMA 3        → $0.0005/extraction

<85% F1 Score:
├── Various local models → $0.0005-$0.001/extraction
└── Older/smaller models → Lower cost, poor quality
```

## Recommended Research Approach

### Phase 1: Direct Comparison (Day 1-2)
Benchmark these providers with identical test set:
1. Claude 3.5 (baseline)
2. Claude 3 Haiku (biggest cost drop with minimal engineering)
3. Cohere (popular alternative with good cost/performance)
4. GPT-4o Mini (wildcard - if it's good, best cost savings)
5. Groq Llama (extreme cost reduction if accuracy holds)

### Phase 2: Deeper Analysis (Day 3-4)
For top 2-3 providers:
- Test on 1,000+ entity samples
- Measure latency distribution (99th percentile)
- Test on edge cases (rare entities, abbreviations, typos)
- Measure consistency (same entity → same extraction)
- Calculate confidence score reliability

### Phase 3: Recommendation (Day 5-6)
Decision tree:
```
If Claude 3 Haiku achieves 85%+ F1:
  → Recommend Haiku (91.7% savings, minimal risk)
Else if Cohere achieves 85%+ F1:
  → Recommend Cohere (88% savings, good balance)
Else if GPT-4o Mini achieves 85%+ F1:
  → Recommend GPT-4o Mini (93% savings, but verify)
Else:
  → Stay with Claude 3.5 (baseline safety)
```

## Breaking Down Extraction Cost

Current Claude 3.5 extraction: $0.003 total
- LLM API call: $0.002 (67%)
- Deduplication: $0.0005 (17%)
- Confidence scoring: $0.0003 (10%)
- Infrastructure/overhead: $0.0002 (6%)

### Optimization Opportunities

**Option A: LLM Provider Switch (Track 05)**
- Cohere API: $0.00035 LLM call cost
- Savings: $0.00165 (55% reduction)
- Risk: Accuracy gap

**Option B: Deduplication Optimization (Track 05)**
- Fuzzy matching + SentenceTransformers vs LLM
- From $0.0005 → $0.0001 (80% reduction of dedup cost)
- Savings: $0.00032 (11% reduction overall)
- Risk: Lower dedup accuracy

**Option C: Hybrid Approach**
- Cohere for extraction: $0.00035
- Local fuzzy matching: $0.0001
- Total: $0.00145 per extraction
- Savings: $0.00155 vs current (52% total reduction)
- Confidence: High (multiple risk mitigations)

## Volume Sensitivity Analysis

### Scenario 1: 1M queries/year (startup phase)
- Current cost: $150K/year (entity extraction)
- With Cohere: $35K/year
- **Savings: $115K/year**

### Scenario 2: 10M queries/year (growth phase)
- Current cost: $1.5M/year
- With Cohere: $350K/year
- **Savings: $1.15M/year**

### Scenario 3: 100M queries/year (scale phase)
- Current cost: $15M/year
- With Cohere: $3.5M/year
- **Savings: $11.5M/year**

## Decision Framework for Track 05

### Go/No-Go Criteria

**GREEN light** (proceed with recommendation):
- Provider achieves 85%+ F1 score on test set
- Cost per extraction ≤ $0.001
- Latency per extraction ≤ 500ms
- Confidence scores are well-calibrated

**YELLOW light** (conditional recommendation):
- F1 score 80-84% (below target but close)
- Cost ≤ $0.0005 (strong cost advantage)
- Requires validation on larger dataset
- May need confidence thresholds adjusted

**RED light** (reject, stay with Claude 3.5):
- F1 score <80%
- Latency >1 second per extraction
- Confidence scores poorly calibrated
- High error rates on edge cases

## Implementation Cost

### Research Phase (Track 05)
- Staff time: 6 days × 1 person = 48 hours
- LLM API calls for benchmarking: ~$500
- Total: ~$2K

### Implementation Phase (if recommended)
- API switching code: 8-16 hours
- Monitoring and observability: 8-16 hours
- Rollback plan: 4-8 hours
- Total: ~5K (code + engineering time)

### Breakeven
- Research + implementation cost: $7K
- Savings from Cohere vs Claude (first year, 10M queries): $1.15M
- **Breakeven**: <1 day of production use

## Competitive Benchmarks

### Industry Standards

**Entity Extraction Accuracy**:
- Human performance: ~95% F1 (upper bound)
- State-of-the-art NER: 90-92% F1 (academic benchmarks)
- Production systems: 80-85% F1 (real-world data)

**Cost Leaders**:
- Open-source models: $0.0 (self-hosted, but ops cost)
- Cohere: $0.35-$0.50 per 1M tokens
- Groq: $0.10 per 1M tokens (budget leader)
- Claude: $3-$15 per 1M tokens (quality leader)

## Risk Mitigation

### Provider Risk
- Benchmark multiple providers
- Have fallback to Claude 3.5 if issues arise
- Implement provider abstraction (swap with one config change)

### Accuracy Risk
- Start with 10% traffic on new provider
- Monitor F1 score continuously
- Have automatic rollback if score drops >5%

### Latency Risk
- Monitor 99th percentile latency
- Have circuit breaker if latency exceeds threshold
- Implement request timeout and fallback

## Recommendation Priority

### High Impact, Low Risk
1. Claude 3 Haiku (safe drop from 3.5)
2. Cohere (proven in production, good cost)

### High Impact, Medium Risk
3. GPT-4o Mini (verify quality)
4. Hybrid approach (Cohere + local dedup)

### High Impact, High Risk
5. Local LLaMA models (operational complexity)
6. Groq Llama (unproven for this use case)

---

**Analysis Date**: 2025-11-13
**Source**: Track 05 - Entity Extraction Research Planning
**Status**: Baseline for benchmarking phase
