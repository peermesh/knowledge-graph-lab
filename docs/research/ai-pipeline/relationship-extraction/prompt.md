## Deep Research Assignment: Relationship Extraction Approaches & Type Taxonomy

**ASSIGNMENT ID:** RES-2025-REL-EXTRACT-001
**Research Type:** Relationship extraction approach comparison + type taxonomy definition
**Decision Context:** Relationship extraction defines knowledge graph structure. Wrong approach wastes 2-3x cost vs optimal. Incorrect relationships break graph traversals and damage user trust.

---

**📝 PROMPT IMPROVEMENTS APPLIED (2025-11-16)**

This prompt has been enhanced based on learnings from Track 01 (Query Processing) research execution. Track 01 research scored A grade (90%+) but lacked empirical validation (no test dataset created, no hands-on benchmarking, code examples were illustrative only). To ensure higher-quality empirical research, this prompt now includes:

- ✅ Explicit MANDATORY DELIVERABLES section with file paths and formats
- ✅ Enhanced Success Criteria distinguishing mandatory vs recommended items
- ✅ DELIVERABLE VALIDATION section with verification commands
- ✅ RESEARCH ACCEPTANCE CRITERIA explaining rejection conditions
- ✅ Clear distinction: empirical relationship extraction testing required, not just approach descriptions

**Your research will be more valuable if you create actual test datasets with ground truth relationships and working code, not just describe extraction approaches.**

---

## 🚨 PREREQUISITES: Read This First

**File:** `ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md`
**Location:** `/Users/grig/work/peermesh/repo/knowledge-graph-lab-alpha/.dev/_sprint_ai_module_nov13/ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md`

**Focus on:** Layer 6 (Relationship Extraction) - understand how entities are connected into graph structure.

---

## Researcher Role

You are a relationship extraction specialist with 10+ years in dependency parsing, semantic role labeling, and knowledge graph construction. You combine linguistic expertise with practical NLP engineering. Your role is to determine the optimal approach for extracting relationships and define the relationship type taxonomy for our domain.

---

## Deployment Context

**Performance Requirements:**
- Relationship extraction precision: 85%+ (few incorrect relationships)
- Type classification accuracy: 90%+ (correct relationship type)
- Conflict detection false positive rate: <5%
- Latency: <5 seconds per 100 entities
- Cost: Minimize API calls while maintaining quality

---

## Scope Specification

### Approaches to Evaluate

**Approach 1: Dependency Parsing (spaCy)**
- Extract subject-verb-object triples
- Map dependency trees to relationships
- Rule-based type classification

**Approach 2: Pure LLM**
- Prompt engineering for relationship extraction
- Direct extraction from text
- Confidence scoring

**Approach 3: Hybrid**
- spaCy candidate generation
- LLM validation and type classification
- Combined confidence scoring

### Relationship Type Definition

**Core Academic Relationships:**
- authorship (author → paper)
- citation (paper → paper)
- affiliation (author → institution)
- publication (paper → venue)
- contribution (author → concept)
- builds-on (concept → concept)
- studies (paper → concept)
- collaboration (author → author)
- funding (funder → research)
- supervision (advisor → student)

---

## Methodology

### Phase 1: Approach Implementation (Day 1)
- Design or implement extraction approaches (2-3 methods)
- Plan evaluation approach
- Create focused benchmark (2-3 representative examples)

### Phase 2: Evaluation (Days 2-3)
- Compare extraction approaches on samples OR analyze published results
- Document precision, recall, F1 characteristics (empirical OR from sources)
- Analyze by relationship type
- Document latency and cost considerations (empirical OR from sources)

### Phase 3: Type Taxonomy (Day 3-4)
- Analyze relationship patterns
- Define 10-15 core types
- Create annotation guidelines
- Test type classification accuracy

### Phase 4: Conflict Detection (Day 4-5)
- Implement conflict detection
- Test on contradictory data
- Measure false positive rate
- Document resolution strategies

---

## MANDATORY DELIVERABLES (Research incomplete without these)

### 1. Test Dataset with Ground Truth Relationships

**File:** `test-dataset-relationships.json`
**Format:** Array of test cases with ground truth relationship labels
**Minimum:** 2-3 illustrative entity pairs with annotated relationships
**Structure:**
```json
[
  {
    "id": "rel-001",
    "entity_pair": ["Alice Johnson", "Smith Institute"],
    "text_context": "Alice Johnson, researcher at Smith Institute, published a paper on graph algorithms",
    "relationship_type": "affiliation",
    "correct_relationship": true,
    "confidence": 0.95,
    "notes": "Clear affiliation statement in text"
  }
]
```

**Validation:** `jq length test-dataset-relationships.json` returns ≥2

### 2. Extraction Method Comparison

**File:** `method-comparison-results.csv`
**Format:** CSV with columns: method, entity_pair_id, extracted_relationship, relationship_type, correct, confidence, precision, recall
**Required:** Representative results (empirical OR from reliable published benchmarks)
**Minimum:** 2-3 methods compared (e.g., rule-based, ML, LLM) on representative test cases
**Example:**
```csv
method,entity_pair_id,extracted_relationship,relationship_type,correct,confidence,extraction_time_ms
rule-based,rel-001,yes,affiliation,true,0.87,23
ml-based,rel-001,yes,affiliation,true,0.92,156
llm-based,rel-001,yes,affiliation,true,0.94,1200
```

### 3. Accuracy Measurements

**File:** `accuracy-measurements.md`
**Required Content:**
- Precision for each approach on your test dataset
- Recall for each approach on your test dataset
- F1 scores by method
- Performance breakdown by relationship type
- Confusion matrices or error analysis
- Confidence calibration assessment

**Validation:** All metrics calculated from YOUR test data, not literature extrapolation

### 4. Working Code Implementation

**Directory:** `relationship-extraction-code/`
**Requirements:**
- Code examples showing approach for 2-3 methods (rule-based, ML, LLM)
- README with explanation
- dependencies list
- Sample data and test cases
- Examples showing evaluation approach

**Validation:**
```bash
# Code examples should demonstrate understanding
# Full production system not required
# Focus on illustrative examples showing extraction approaches
```

### 5. Code Repository Link

**File:** `code-repository-link.md`
**Format:** Link to repository OR code examples with understanding
**Requirements:**
- Code examples demonstrating extraction approaches
- Include: README, dependencies, test data
- Demonstrate understanding through focused examples
- Show extraction approach on sample academic texts

**Validation:** Code examples demonstrate understanding of approach

---

## Deliverable Specifications

### Primary Deliverable: Technical Report (≥3,000 words)

**Required Sections:**
1. Approach Comparison Matrix
2. Accuracy Analysis by Relationship Type
3. Relationship Type Taxonomy
4. Conflict Detection Results
5. Cost and Latency Benchmarks
6. Implementation Recommendations

---

## Success Criteria

### MANDATORY (Research incomplete until ALL checked)

- [ ] **Test dataset created:** `test-dataset-relationships.json` with 2-3 illustrative entity pairs
- [ ] **Method comparison file:** `method-comparison-results.csv` with representative measurements (empirical OR cited)
- [ ] **Accuracy measurements:** `accuracy-measurements.md` with precision, recall, F1 analysis
- [ ] **Code examples:** `relationship-extraction-code/` with examples demonstrating understanding
- [ ] **Code repository:** `code-repository-link.md` with code examples or link
- [ ] **2-3 methods compared:** Representative approaches (e.g., rule-based, ML, LLM)
- [ ] **Precision ≥85% documented:** Based on evidence (empirical OR from reliable sources)
- [ ] **10-15 relationship types defined:** Core types documented with examples
- [ ] **Type taxonomy complete:** Annotation guidelines and classification approach documented
- [ ] **Conflict detection analysis:** Approach to handling contradictory data documented

### RECOMMENDED (Enhances quality)

- [ ] Published benchmark comparisons (supplementary context)
- [ ] Literature review with citations
- [ ] Cost analysis (API calls, computation time)
- [ ] Domain-specific relationship patterns identified
- [ ] Error analysis and misclassification examples
- [ ] Integration design with knowledge graph merge layer
- [ ] Performance optimization recommendations

---

## DELIVERABLE VALIDATION

**Before marking research complete, verify:**

### 1. Test Dataset File Exists

```bash
# Check file exists and has minimum size
test -f test-dataset-relationships.json && jq length test-dataset-relationships.json
# Expected output: 2-3 illustrative examples
```

### 2. Method Comparison Results

- Should show representative performance (empirical OR from reliable sources)
- Published benchmarks are acceptable when combined with understanding
- Required columns must be present (method, entity_pair_id, extracted_relationship, correct, confidence)
- Minimum 2-3 methods with complete data showing understanding

### 3. Accuracy Measurements Documentation

- Should include precision/recall analysis (empirical OR from sources)
- Show breakdown by relationship type
- Include confidence calibration considerations
- Document error patterns or confusion analysis

### 4. Code Repository Validation

```bash
# Code examples should demonstrate understanding
# Full production system not required
# Focus on illustrative examples showing extraction approach
```

---

## RESEARCH ACCEPTANCE CRITERIA

**This research will be REJECTED if:**

- ❌ No illustrative examples provided (need 2-3 representative entity pairs)
- ❌ No evidence of understanding (must show empirical testing OR deep analysis of published benchmarks)
- ❌ Code examples missing (focused examples demonstrating approach required)
- ❌ Accuracy analysis lacking depth or evidence
- ❌ Insufficient method comparison (need 2-3 approaches analyzed)
- ❌ No code examples (snippets showing understanding required)
- ❌ Relationship types not defined or analyzed

**Rationale:**

We need empirical validation, not literature synthesis. Published relationship extraction benchmarks don't account for our domain-specific requirements (academic papers, citations, author relationships, publication metadata). The extraction approach must work on actual academic texts with relationships relevant to research knowledge graphs.

**What "code examples demonstrating understanding" means:**

- Not: "Here's a one-line comment about relation extraction"
- Yes: "Here's focused code showing rule-based and LLM extraction approaches, with comments explaining tradeoffs"

**What "evidence-based analysis" means:**

- Not: "LSTMs are probably good for this"
- Yes: "Testing on 2-3 samples showed rule-based=82%, consistent with TAC-KBP benchmark. LLM approaches achieved 91% in published research"

---

**Begin research now.**
