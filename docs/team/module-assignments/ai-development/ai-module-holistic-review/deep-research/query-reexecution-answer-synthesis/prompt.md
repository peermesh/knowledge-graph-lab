## Deep Research Assignment: Query Re-execution, Answer Synthesis & Citation Quality

**ASSIGNMENT ID:** RES-2025-ANSWER-SYNTH-001
**Research Type:** Answer synthesis approach comparison + citation strategy testing
**Decision Context:** Query re-execution is the final user-facing layer. Answer quality determines product success. Poor citations damage credibility even if answers are correct. Wrong approach wastes development effort and damages user trust.

---

**📝 PROMPT IMPROVEMENTS APPLIED (2025-11-16)**

This prompt has been enhanced based on learnings from Track 01 (Query Processing) research execution. Track 01 research scored A grade (90%+) but lacked empirical validation (no test dataset created, no hands-on benchmarking, code examples were illustrative only). To ensure higher-quality empirical research, this prompt now includes:

- ✅ Explicit MANDATORY DELIVERABLES section with file paths and formats
- ✅ Enhanced Success Criteria distinguishing mandatory vs recommended items
- ✅ DELIVERABLE VALIDATION section with verification commands
- ✅ RESEARCH ACCEPTANCE CRITERIA explaining rejection conditions
- ✅ Clear distinction: empirical measurements required, not literature extrapolation

**Your research will be more valuable if you create actual test datasets and working code, not just synthesize existing literature.**

---

## 🚨 PREREQUISITES: Read This First

**File:** `ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md`
**Location:** `/Users/grig/work/peermesh/repo/knowledge-graph-lab-alpha/.dev/_sprint_ai_module_nov13/ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md`

**Focus on:** Layer 8 (Query Re-execution) - final step where graph query results become natural language answers with citations.

---

## Researcher Role

You are a question answering systems specialist with 10+ years in natural language generation, information retrieval, and user experience research. You combine technical knowledge of NLG approaches with deep understanding of user preferences for answer quality and citation formats. Your role is to determine the optimal answer synthesis approach and citation strategy.

---

## Deployment Context

**Performance Requirements:**
- Answer relevance: 85%+ user satisfaction (4.25/5 rating)
- Citation accuracy: 98%+ (cited sources actually support claims)
- Confidence calibration: ECE <5% (well-calibrated scores)
- Answer generation latency: <2 seconds per query
- Concurrent users: Support 100+ simultaneous queries
- Graceful degradation: Handle unanswerable queries elegantly

---

## Scope Specification

### Answer Synthesis Approaches

**Approach 1: Template-Based Generation**
- Predefined templates for common query types
- Variable substitution from graph results
- Fast and predictable output
- Consistency and control

**Approach 2: LLM-Based Generation**
- Claude/GPT to write natural answers
- High fluency and naturalness
- Flexible across query types
- Higher cost and latency

**Approach 3: Hybrid**
- Templates for structure
- LLM for natural phrasing
- Balance speed and quality
- Cost optimization

### Citation Strategies

**Strategy 1: Inline Citations**
- Citation numbers in text [1]
- Footnote-style references
- Familiarity from academic writing

**Strategy 2: Source Panels**
- Separate source listing
- Expandable details per source
- Visual separation from answer

**Strategy 3: Hover Citations**
- Inline highlighting with hover
- Minimal visual clutter
- Interactive source display

### Confidence Scoring

**Components:**
- Query success rate
- Answer completeness
- Source quality/confidence
- Graph coverage

**Calibration:**
- Expected Calibration Error (ECE)
- Reliability diagrams
- Threshold optimization

---

## Methodology

### Phase 1: Answer Synthesis Comparison (Day 1)
- Design or implement 2-3 synthesis approaches
- Create focused evaluation set (2-3 representative queries)
- Compare answer generation approaches OR analyze published results
- Document relevance characteristics (empirical OR from sources)
- Document latency and cost considerations (empirical OR from sources)
- Analyze quality by query type

### Phase 2: Citation Strategy Testing (Day 2)
- Evaluate 2-3 citation formats
- Analyze citation accuracy potential (empirical OR from sources)
- Document format preferences and tradeoffs
- Analyze discoverability and trust factors
- Document coverage considerations
- Assess implementation complexity

### Phase 3: Confidence Calibration (Day 3)
- Design confidence scoring approach
- Analyze scoring for representative answers
- Document calibration considerations (empirical OR from sources)
- Consider calibration metrics (ECE, MCE)
- Analyze reliability patterns
- Document threshold considerations

### Phase 4: Integration and Optimization (Day 4)
- Build end-to-end system
- Performance benchmarking
- Scalability testing (100+ concurrent)
- Cost projection at scale
- Final recommendations
- Deployment guidelines

---

## MANDATORY DELIVERABLES (Research incomplete without these)

### 1. Test Query Dataset with Incomplete Initial Results

**File:** `test-queries-incomplete-results.json`
**Format:** Array of query objects with initial results and expected improvements
**Minimum:** 2-3 illustrative queries with documented incomplete initial results
**Structure:**
```json
[
  {
    "id": "query-001",
    "question": "What are the key contributions of papers by Alice Smith in graph databases?",
    "initial_query_results": {
      "entity_coverage": 0.65,
      "completeness_score": 0.58,
      "issues": ["Missing 3 papers after 2020", "Incomplete relationship data"]
    },
    "expected_improvement": 0.87,
    "improvement_mechanism": "Re-execution with expanded search scope",
    "notes": "Initial query missed recent publications"
  }
]
```

**Validation:** `jq length test-queries-incomplete-results.json` returns ≥2

### 2. Re-execution Strategy Results

**File:** `reexecution-strategy-results.csv`
**Format:** CSV with columns: query_id, strategy, coverage_before, coverage_after, quality_score_before, quality_score_after, latency_ms, improvement_percent
**Required:** Representative results (empirical OR from analysis/published research)
**Minimum:** 2-3 re-execution strategies analyzed on representative test queries

### 3. Answer Synthesis Evaluation Scores

**File:** `answer-synthesis-evaluation.csv`
**Format:** CSV with columns: query_id, approach, user_relevance_score, citation_accuracy, answer_completeness, confidence_calibration, approach_latency_ms
**Required:** Representative evaluation (empirical OR from analysis/published research)
**Minimum:** 2-3 synthesis approaches (e.g., Template, LLM, Hybrid) analyzed on representative queries

### 4. Working Code for Re-execution and Synthesis

**File:** `code-repository-link.md` with code examples demonstrating understanding
**Requirements:**
- Code examples showing re-execution and synthesis approaches
- Include: README, dependencies, test queries
- Demonstrate understanding through focused examples
- Show approach for 2-3 synthesis methods
- Focus on demonstrating understanding, not production system

**Validation:** Code examples demonstrate understanding of approach

### 5. Code Repository

**Location:** Include link in `code-repository-link.md`
**Must contain:**
- Re-execution logic with decision rules
- Template-based answer generation
- LLM-based answer generation (Claude/GPT integration)
- Hybrid synthesis approach
- Citation tracking and accuracy validation
- Test suite with benchmark queries
- Performance profiling scripts

---

## Deliverable Specifications

### Primary Deliverable: Technical Report (≥3,000 words)

**Required Sections:**
1. Executive Summary with recommendations
2. Answer Synthesis Comparison (user scores, cost, latency)
3. Citation Strategy Analysis (accuracy, user preference)
4. Confidence Calibration Assessment (ECE curves, reliability)
5. Performance Benchmarks (latency, throughput, cost)
6. User Preference Study Results
7. Integration Design
8. Implementation Guidelines
9. Risk Assessment

### Secondary Deliverables

**User Study Results:**
- Relevance ratings per approach
- Citation format preferences
- Confidence communication effectiveness
- Statistical significance tests

**Code Artifacts:**
- Answer generation implementations
- Citation tracking systems
- Confidence scoring algorithms
- Performance benchmark scripts

---

## Success Criteria

### MANDATORY (Research incomplete until ALL checked)

- [ ] **Test dataset created:** `test-queries-incomplete-results.json` with 2-3 illustrative queries
- [ ] **Re-execution strategy results file:** `reexecution-strategy-results.csv` with representative analysis (empirical OR cited)
- [ ] **Answer synthesis evaluation file:** `answer-synthesis-evaluation.csv` with approach comparison
- [ ] **Code repository:** `code-repository-link.md` with code examples demonstrating understanding
- [ ] **2-3 synthesis approaches analyzed:** Representative approaches (e.g., Template, LLM, Hybrid)
- [ ] **2-3 citation strategies analyzed:** Representative formats (e.g., Inline, source panels, hover)
- [ ] **Re-execution improvement documented:** Based on evidence (empirical OR from sources)
- [ ] **User relevance 85%+ potential documented:** Based on evidence (empirical OR from sources)
- [ ] **Citation accuracy 98%+ potential documented:** Based on evidence (empirical OR from sources)
- [ ] **Latency <2 seconds potential documented:** Based on evidence (empirical OR from sources)

### RECOMMENDED (Enhances quality)

- [ ] Published benchmark comparisons (supplementary context)
- [ ] Confidence calibration analysis (ECE <5%)
- [ ] 100+ concurrent query scalability testing
- [ ] Cost model and projections
- [ ] User preference study for citation formats
- [ ] Integration design with Layer 8 system
- [ ] Risk assessment and tradeoffs
- [ ] Monitoring and alerting strategy

---

## DELIVERABLE VALIDATION

**Before marking research complete, verify:**

### 1. Test Query Dataset File Exists

```bash
# Check file exists and has minimum size
test -f test-queries-incomplete-results.json && jq length test-queries-incomplete-results.json
# Expected output: 2-3 illustrative examples
```

### 2. Re-execution Strategy Results Table

- Should show representative performance (empirical OR from sources)
- Required columns must be present (query_id, strategy, coverage_before, coverage_after, quality_score_before, quality_score_after, latency_ms, improvement_percent)
- Minimum 2-3 re-execution strategies analyzed on representative queries
- Shows improvement characteristics (empirical OR from sources)

### 3. Answer Synthesis Evaluation Results

- Should include evaluation of 2-3 synthesis approaches (e.g., Template, LLM, Hybrid)
- Required columns: query_id, approach, user_relevance_score, citation_accuracy, answer_completeness, confidence_calibration, approach_latency_ms
- Representative queries analyzed (empirical OR from sources)
- Evaluation approach documented

### 4. Citation Strategy Testing

- Should include analysis of 2-3 citation strategies (e.g., inline, source panels, hover)
- Show citation accuracy characteristics (empirical OR from sources)
- Document user preference or effectiveness considerations
- Include implementation notes for each strategy

### 5. Code Repository Validation

```bash
# Code examples should demonstrate understanding
# Full production system not required
# Focus on illustrative examples showing re-execution and synthesis approach
```

---

## RESEARCH ACCEPTANCE CRITERIA

**This research will be REJECTED if:**

- ❌ No illustrative examples provided (need 2-3 representative queries)
- ❌ No evidence of understanding (must show empirical testing OR deep analysis of published research)
- ❌ Code examples missing (focused examples demonstrating approach required)
- ❌ Answer synthesis evaluation lacking depth or evidence
- ❌ Citation accuracy analysis missing or unsupported
- ❌ Latency/performance analysis lacking depth or evidence
- ❌ No integration analysis (must show understanding of query re-execution → synthesis → citation)

**Rationale:**

We need empirical validation, not literature synthesis. Published benchmarks don't account for our specific knowledge graph (research papers, authors, citations) and query types. Answer synthesis must work on real queries with real knowledge graph data. Citation accuracy must be validated on actual answers your system generates.

**What "code examples demonstrating understanding" means:**

- Not: "Here's a one-line comment about templates"
- Yes: "Here's focused code showing template-based and LLM synthesis approaches, with citation logic and comments explaining tradeoffs"

**What "evidence-based analysis" means:**

- Not: "LLM synthesis is probably better"
- Yes: "Testing on 2-3 queries showed Template=3.8/5, LLM=4.2/5 in user ratings, consistent with published QA research showing similar patterns"

**What "citation accuracy analysis" means:**

- Not: "Citations should be accurate"
- Yes: "Analysis of 2-3 examples showed inline citations achieving 98% accuracy in published research, with clear tradeoffs vs source panels"

---

## Evaluation Rubric

### Answer Quality (40 points)
- User relevance 4.5+/5: 40 points
- 4.0-4.4/5: 30 points
- 3.5-3.9/5: 20 points
- <3.5/5: 10 points

### Citation Quality (20 points)
- Citation accuracy 99%+: 20 points
- 95-98%: 15 points
- 90-94%: 10 points
- <90%: 5 points

### Confidence Calibration (20 points)
- ECE <3%: 20 points
- ECE 3-5%: 15 points
- ECE 5-10%: 10 points
- ECE >10%: 5 points

### Performance (15 points)
- <1 sec, 100+ concurrent: 15 points
- 1-2 sec, 50+ concurrent: 12 points
- 2-5 sec or limited concurrency: 8 points
- >5 sec or poor concurrency: 3 points

### Implementation Quality (5 points)
- Clear, complete recommendations: 5 points
- Good recommendations: 3 points
- Limited guidance: 1 point

**Decision Threshold:**
- Score 85+: Ready for production
- Score 75-84: Good, needs optimization
- Score <75: Needs significant improvement

---

**Begin research now.**
