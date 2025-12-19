## Deep Research Assignment: LLM Provider Benchmarking for Entity Extraction

**ASSIGNMENT ID:** RES-2025-ENTITY-LLM-001
**Research Type:** LLM provider benchmarking + cost-benefit analysis
**Decision Context:** Entity extraction costs represent 60% of total pipeline cost. Can we replace Claude 3.5 Sonnet ($0.003/extraction) with cheaper alternative like Cohere ($0.0008/extraction) and save 73% per extraction while maintaining 85%+ F1 score? This is our biggest cost optimization opportunity.

---

**📝 PROMPT IMPROVEMENTS APPLIED (2025-11-16)**

This prompt has been enhanced based on learnings from Track 01 (Query Processing) research execution. Track 01 research scored A grade (90%+) but lacked empirical validation (no test dataset created, no hands-on benchmarking, code examples were illustrative only). To ensure higher-quality empirical research, this prompt now includes:

- ✅ Explicit MANDATORY DELIVERABLES section with file paths and formats
- ✅ Enhanced Success Criteria distinguishing mandatory vs recommended items
- ✅ DELIVERABLE VALIDATION section with verification commands
- ✅ RESEARCH ACCEPTANCE CRITERIA explaining rejection conditions
- ✅ Clear distinction: empirical measurements required, not literature extrapolation

**Your research will be more valuable if you create actual test datasets and benchmark with real LLM API calls, not just synthesize existing literature.**

---

## 🚨 PREREQUISITES: Read This First

**File:** `ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md`
**Location:** `/Users/grig/work/peermesh/repo/knowledge-graph-lab-alpha/.dev/_sprint_ai_module_nov13/ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md`

**Focus on:** Layer 5 (Entity Extraction) - understand how text is transformed into structured entities. Quality threshold of 85%+ F1 is non-negotiable, but cost optimization within that constraint is critical.

---

## Researcher Role

You are an NLP benchmarking specialist with 10+ years in entity extraction systems, model evaluation, and production cost optimization. You combine rigorous statistical methodology with practical understanding of LLM pricing and capabilities. Your role is to find the cheapest LLM that meets our quality requirements.

---

## Deployment Context

**Performance Requirements:**
- Entity extraction F1 score: 85%+ (precision and recall)
- Cost per extraction: Target <$0.0015 (50% of current cost)
- Latency per extraction: <2 seconds for 50 entities
- Confidence calibration: ECE <10%
- Domain coverage: Authors, papers, concepts, venues, institutions
- Batch efficiency: Support processing 100+ entities per request

**Current Baseline:**
- Claude 3.5 Sonnet: $0.003 per 1K tokens (~1 extraction)
- F1 score: Unknown (need to measure)
- If Cohere works at $0.0008, we save $0.0022 per extraction
- At 1M extractions/month: $2,200/month savings

**Cost Optimization Goal:**
- Find model with F1 ≥85% at lowest cost
- Document quality vs cost tradeoff curve
- Identify break-even points for different model choices

---

## Scope Specification

### LLM Providers to Benchmark

**Tier 1: Premium Models**
- **Claude 3.5 Sonnet**: $3/1M input tokens
  - Current baseline, need F1 benchmark
  - Expected: High quality, high cost
- **GPT-4**: $10/1M input tokens
  - Quality comparison to Claude
  - Likely too expensive

**Tier 2: Mid-Range Models**
- **GPT-4 Mini**: $0.15/1M input tokens
  - Significant cost reduction
  - Quality vs Claude comparison critical
- **Cohere Command**: $0.50/1M input tokens
  - Target candidate for cost savings
  - Test F1 score vs Claude

**Tier 3: Budget Models**
- **Claude Haiku**: $0.25/1M input tokens
  - Cheapest Anthropic option
  - Quality threshold test
- **Llama 3 70B (Together AI)**: ~$0.70/1M tokens
  - Open-source alternative
  - Cost-quality tradeoff

### Benchmark Dataset Creation

**Sample Selection:**
- 2-3 representative text samples from academic papers
- Diverse sources: AI, biology, physics, or social science
- Length variation: 100-500 words per sample
- Entity density: 5-15 entities per sample

**Ground Truth Annotation:**
- Annotate entities in samples (or use existing labeled datasets)
- Entity types: author, paper, concept, venue, institution
- Include edge cases: abbreviations, acronyms, multi-word

**Quality Assurance:**
- Document annotation approach
- Note any disagreements or challenges
- Document guidelines used

### Benchmark Methodology

**Extraction Protocol:**
- Same prompt template for all providers
- Extract entities with confidence scores
- Batch processing where supported
- Record all outputs for analysis

**Metrics Collection:**
- **Accuracy**: Precision, recall, F1 per entity type
- **Cost**: Total tokens, cost per extraction
- **Latency**: API call time, total processing time
- **Confidence**: Score distributions, calibration (ECE)
- **Consistency**: Same input → same output reliability
- **Batch efficiency**: Cost reduction with batching

---

## Research Questions

1. **Cost Savings?**
   - Can we achieve 85%+ F1 with model <$0.0015 per extraction?
   - What's the cheapest model that meets quality threshold?
   - How much do we save at different query volumes?

2. **Quality Tradeoffs?**
   - What F1 score do we get at each price point?
   - Which entity types are hardest for cheaper models?
   - Is there a quality cliff below certain price point?

3. **Latency Impact?**
   - Do cheaper models process faster or slower?
   - Does batching reduce latency per extraction?
   - What's the user experience impact?

4. **Confidence Reliability?**
   - Do cheaper models have well-calibrated confidence?
   - Can we trust confidence scores for quality gates?
   - Does confidence help identify extraction errors?

5. **Batch Optimization?**
   - Can we batch 10-100 entities per request?
   - What cost reduction does batching provide?
   - Does batching impact latency or accuracy?

---

## Methodology

### Phase 1: Benchmark Preparation (Day 1)
- Design evaluation approach
- Build focused 2-3 sample benchmark dataset (or use existing)
- Annotate ground truth entities
- Plan provider comparison approach
- Document baseline prompt template

### Phase 2: Provider Benchmarking (Days 2-3)
- Compare representative providers on focused samples OR analyze published benchmarks
- Collect F1 scores per provider and entity type (empirical OR from reliable sources)
- Document latency and cost characteristics (empirical OR from pricing/benchmarks)
- Analyze confidence score patterns
- Evaluate batch processing considerations
- Create cost vs accuracy comparison

### Phase 3: Deep Analysis (Day 4)
- Statistical significance testing
- Confidence calibration analysis (ECE)
- Edge case error analysis
- Cost projection at different volumes
- Sensitivity analysis: impact of pricing changes
- Risk assessment for model switching

### Phase 4: Recommendation (Days 5-6)
- Synthesize findings into recommendation
- Create Pareto frontier plot (cost vs quality)
- Document implementation guidance
- Build cost calculator tool
- Final report and decision documentation

---

## MANDATORY DELIVERABLES (Research incomplete without these)

### 1. Test Dataset with Ground Truth Labels

**File:** `test-dataset-entities.json`
**Format:** Array of test cases with ground truth entity labels
**Minimum:** 2-3 illustrative research paper text samples with entity annotations
**Structure:**
```json
[
  {
    "id": "entity-001",
    "text": "John Smith published 'Deep Learning Fundamentals' at ACM 2023",
    "ground_truth_entities": [
      {"text": "John Smith", "type": "author", "start": 0, "end": 10},
      {"text": "Deep Learning Fundamentals", "type": "paper", "start": 24, "end": 49},
      {"text": "ACM", "type": "venue", "start": 54, "end": 57},
      {"text": "2023", "type": "year", "start": 58, "end": 62}
    ],
    "entity_count": 4,
    "notes": "Clear multi-entity example with distinct types"
  }
]
```

**Validation:** `jq length test-dataset-entities.json` returns ≥2

### 2. Benchmark Results with Real API Calls

**File:** `benchmark-results-providers.csv`
**Format:** CSV with columns: provider, model, test_cases_count, precision, recall, f1, cost_per_extraction, latency_ms, tokens_used
**Required:** Representative results (from actual testing OR reliable published benchmarks)
**Minimum:** 2-3 providers compared (e.g., Claude, GPT-4, Cohere) on representative test cases

**Example:**
```csv
provider,model,test_cases,precision,recall,f1,cost_per_extraction,latency_ms,tokens_used
Anthropic,Claude 3.5 Sonnet,3,0.92,0.89,0.905,0.003,450,287
OpenAI,GPT-4 Mini,3,0.85,0.82,0.835,0.0015,380,198
Cohere,Command,3,0.78,0.75,0.765,0.0008,320,156
```

### 3. Performance Comparison Matrix

**File:** `entity-extraction-comparison-matrix.md`
**Required Content:**
- Accuracy metrics: Precision, Recall, F1 per provider and per entity type
- Cost analysis: Cost per extraction, total cost for 30 test cases, cost per 1M extractions
- Latency analysis: API response time, token-per-extraction ratios
- Cost-Quality tradeoff visualization (could be ASCII chart or description)
- Break-even analysis: At what volume does cheaper model ROI justify switching

**Validation Commands:**
```bash
# Verify matrix has all 5+ providers
grep -c "provider" entity-extraction-comparison-matrix.md  # >= 5
# Verify all metrics present
grep -E "(Precision|Recall|F1|Cost|Latency)" entity-extraction-comparison-matrix.md | wc -l  # >= 15
```

### 4. Working Code Repository

**File:** `code-repository-link.md` with code examples demonstrating understanding
**Requirements:**
- Code examples showing approach to benchmarking
- Include: README, dependencies list, sample dataset, API integration examples
- Demonstrate understanding of entity extraction evaluation
- Show how to calculate precision/recall
- Focus on demonstrating understanding, not production system

**Repository Structure:**
```
entity-extraction-benchmark/
├── README.md
├── requirements.txt
├── config.yaml (API keys template)
├── test-dataset-entities.json
├── benchmark_providers.py
├── entity_extractor.py
├── evaluation_metrics.py
├── results/
│   ├── benchmark-results-providers.csv
│   ├── entity-extraction-comparison-matrix.md
│   └── detailed-results/
└── tests/
    └── test_extraction.py
```

**Validation:** Code examples demonstrate understanding of benchmarking approach

### 5. Cost Projection and ROI Analysis

**File:** `cost-roi-analysis.md`
**Required:**
- Current cost at different volumes (100K, 1M, 10M extractions/month)
- Cost with recommended provider
- Monthly savings (if switching)
- Break-even timeline for migration effort
- Risk assessment of switching from Claude to alternative

---

## Deliverable Specifications

### Primary Deliverable: Benchmark Report (≥3,500 words)

**Required Sections:**
1. Executive Summary with cost savings recommendation
2. Provider Comparison Matrix (F1, cost, latency)
3. Statistical Analysis (significance tests, confidence intervals)
4. Pareto Frontier: Best accuracy at each cost level
5. Confidence Calibration Assessment
6. Edge Case Analysis
7. Batch Processing Cost Reduction
8. Cost Projections at Scale (100K/1M/10M extractions)
9. Risk Assessment and Sensitivity Analysis
10. Implementation Guidance

### Secondary Deliverables

**Cost Calculator:**
- Spreadsheet: configurable volume, provider choice
- Break-even analysis between providers
- ROI calculator for model switching

**Code Artifacts:**
- Benchmark evaluation scripts
- Provider API integration examples
- Statistical analysis notebooks
- Batch processing implementations

---

## Success Criteria

### MANDATORY (Research incomplete until ALL checked)

- [ ] **Test dataset created:** `test-dataset-entities.json` with 2-3 illustrative examples
- [ ] **Benchmark results file:** `benchmark-results-providers.csv` with representative measurements (empirical OR cited)
- [ ] **Performance matrix created:** `entity-extraction-comparison-matrix.md` with accuracy, cost, latency metrics
- [ ] **Code repository:** `code-repository-link.md` with code examples demonstrating understanding
- [ ] **2-3 providers compared:** Representative providers (e.g., Claude, GPT-4, Cohere)
- [ ] **Precision ≥85% documented:** Based on evidence (empirical OR from reliable sources)
- [ ] **Recall ≥85% documented:** Based on evidence (empirical OR from reliable sources)
- [ ] **Cost projections:** Calculated for representative volumes
- [ ] **ROI analysis:** Clear recommendation based on evidence

### RECOMMENDED (Enhances quality)

- [ ] Confidence calibration analyzed (ECE metric)
- [ ] Statistical significance tests on F1 differences
- [ ] Per-entity-type breakdown (authors, papers, concepts, venues)
- [ ] Error analysis: which entities are hardest to extract
- [ ] Batch processing efficiency tests
- [ ] Risk assessment for model switching

---

## Evaluation Rubric

### Cost Efficiency (35 points)
- Found model with F1≥85% at <$0.0008: 35 points
- F1≥85% at $0.0008-$0.0015: 28 points
- F1≥85% at $0.0015-$0.003: 20 points
- No model <$0.003 meets F1 threshold: 10 points

### Quality (30 points)
- Best model F1≥90%: 30 points
- Best model F1 85-89%: 23 points
- Best model F1 80-84%: 15 points
- Best model F1 <80%: 5 points

### Analysis Rigor (20 points)
- Statistical significance tests: 8 points
- Confidence calibration analysis: 6 points
- Edge case analysis: 6 points

### Implementation Guidance (10 points)
- Clear provider recommendation: 5 points
- Migration guidance: 3 points
- Risk mitigation: 2 points

### Cost Modeling (5 points)
- Accurate cost projections: 3 points
- Sensitivity analysis: 2 points

**Decision Threshold:**
- Score 85+: Strong recommendation, implement immediately
- Score 70-84: Viable, document tradeoffs carefully
- Score <70: Insufficient evidence, continue research

---

## DELIVERABLE VALIDATION

**Before marking research complete, verify:**

### 1. Test Dataset File Exists

```bash
# Check file exists and has minimum size
test -f test-dataset-entities.json && jq length test-dataset-entities.json
# Expected output: 2-3 illustrative examples
```

### 2. Benchmark Results CSV

- Should show representative measurements (empirical OR from reliable sources)
- Published benchmarks are acceptable when combined with understanding
- Required columns: provider, model, test_cases, precision, recall, f1, cost_per_extraction, latency_ms, tokens_used
- Minimum 2-3 providers with complete data showing understanding

```bash
# Verify CSV has required columns
head -1 benchmark-results-providers.csv | grep -c ","  # >= 8 columns
# Count data rows (should be 5+)
tail -n +2 benchmark-results-providers.csv | wc -l  # >= 5
```

### 3. Comparison Matrix Documentation

- Must show performance on YOUR test dataset
- Must have accuracy breakdown (precision, recall, F1 per provider)
- Must show cost analysis (cost per extraction, projections)
- Must show latency measurements
- Must include cost-quality tradeoff analysis

### 4. Code Repository Validation

```bash
# Code examples should demonstrate understanding
# Full production benchmarking system not required
# Focus on illustrative examples showing evaluation approach
```

### 5. ROI Analysis Document

- Must include cost calculations at 100K, 1M, and 10M extraction volumes
- Must show annual savings with recommended provider
- Must discuss migration risks and benefits
- Must be based on YOUR benchmark results (not generic estimates)

---

## RESEARCH ACCEPTANCE CRITERIA

**This research will be REJECTED if:**

- ❌ No illustrative examples provided (need 2-3 representative samples)
- ❌ No evidence of understanding (must show empirical testing OR deep analysis of published benchmarks)
- ❌ Code examples missing (focused examples demonstrating approach required)
- ❌ No precision/recall analysis (empirical OR from reliable published sources)
- ❌ Cost analysis lacking depth or evidence
- ❌ Missing comparison matrix with key metrics

**Rationale:**

We need empirical validation, not literature synthesis. Published benchmarks don't account for our domain-specific entity types (academic authors, paper titles, venues, institutions, concepts). The extraction system must be benchmarked on actual research paper text with ground truth labels for our specific use case.

**What "code examples demonstrating understanding" means:**

- Not: "Here's a one-line comment about API calls"
- Yes: "Here's focused code showing how I would benchmark providers, with evaluation logic and cost calculation"

**What "evidence-based analysis" means:**

- Not: "I think Claude is probably best"
- Yes: "Testing on 2-3 samples showed Claude F1=92%, consistent with benchmark X. Cost analysis based on pricing: Claude=$0.003/extraction"

**What "cost analysis" means:**

- Not: "Claude costs something per token"
- Yes: "Based on pricing pages and token estimates, Claude=$0.003 per extraction, Cohere=$0.0008, projected savings=73%"

---

**Begin research now.**
