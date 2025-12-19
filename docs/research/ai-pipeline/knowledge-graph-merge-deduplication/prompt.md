## Deep Research Assignment: Entity Deduplication Algorithms for Knowledge Graph Merge

**ASSIGNMENT ID:** RES-2025-KG-DEDUP-001
**Research Type:** Deduplication algorithm evaluation + precision/recall benchmarking
**Decision Context:** Entity deduplication with 99%+ precision is critical. False positives (merging different entities) corrupt the graph permanently. This is the highest-stakes quality gate - wrong choice damages graph integrity.

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

**Focus on:** Layer 7 (Knowledge Graph Merge) - deduplication prevents duplicate nodes that break queries.

---

## Researcher Role

You are an entity resolution specialist with 10+ years in database deduplication, similarity algorithms, and large-scale data matching. You combine algorithmic expertise with practical understanding of precision/recall tradeoffs. Your role is to find the algorithm achieving 99%+ precision while maximizing recall.

---

## Deployment Context

**Performance Requirements:**
- Deduplication precision: 99%+ (false positive rate <1%)
- Deduplication recall: 98%+ (false negative rate <2%)
- Latency: Deduplicate 10K entities in <10 seconds
- Scalability: Handle graphs with 100K+ entities
- Cost: Minimize API calls while meeting quality targets

---

## Scope Specification

### Algorithms to Evaluate

**Algorithm 1: Fuzzy String Matching**
- Jaro-Winkler similarity
- Levenshtein distance
- Threshold optimization for precision/recall

**Algorithm 2: Semantic Embeddings**
- SentenceTransformers (all-MiniLM-L6-v2)
- Cosine similarity threshold tuning
- Batch processing for efficiency

**Algorithm 3: LLM-Based Deduplication**
- Prompt Claude/GPT: "Are these entities the same?"
- Confidence thresholding
- Cost vs quality analysis

**Algorithm 4: Hybrid Approach**
- High similarity → fuzzy match (fast)
- Moderate similarity → semantic (accurate)
- Ambiguous → LLM (high precision)

---

## Methodology

### Phase 1: Test Dataset Creation (Day 1)
- Create representative example with 20-30 sample entities
- Include edge cases (name variations, typos, formatting)
- Annotate 2-3 ground truth duplicate pairs showing different merge complexity
- Document types of duplicates (exact, fuzzy, semantic)

### Phase 2: Algorithm Implementation (Day 1.5)
- Implement fuzzy matching baseline
- Implement semantic matching
- Test LLM-based deduplication
- Implement hybrid approach

### Phase 3: Precision/Recall Tuning (Day 2-2.5)
- Test algorithms at different thresholds
- Generate precision-recall curves
- Find optimal threshold for 99%+ precision
- Measure recall at that threshold
- Analyze false positives and negatives

### Phase 4: Scaling and Cost Analysis (Day 3)
- Test with 100K entity dataset
- Measure latency scaling
- Calculate cost per entity
- Final recommendations

---

## MANDATORY DELIVERABLES (Research incomplete without these)

### 1. Test Graph Dataset with Known Duplicates

**File:** `test-graphs-duplicates.json`
**Format:** Sample knowledge graph with ground truth duplicate pairs
**Minimum:** 1-2 sample graphs, 10-20 entities per graph, 2-3 known duplicate examples per graph
**Structure:**
```json
{
  "graph_id": "graph-001",
  "description": "Research paper knowledge graph with 150 entities",
  "entities": [
    {"id": "author-001", "type": "Author", "name": "John Smith", "attributes": {...}},
    {"id": "author-002", "type": "Author", "name": "John Smith PhD", "attributes": {...}}
  ],
  "relationships": [...],
  "ground_truth_duplicates": [
    {"id1": "author-001", "id2": "author-002", "confidence": 1.0, "reason": "Same person, name variations"}
  ]
}
```

**Validation:** `jq '.[] | .ground_truth_duplicates | length' test-graphs-duplicates.json` returns 2-3 per graph

### 2. Deduplication Algorithm Results

**File:** `deduplication-results.csv`
**Format:** CSV with columns: algorithm, test_graph, entities_tested, duplicates_found, true_positives, false_positives, precision, recall
**Required:** Results from YOUR test dataset (not published benchmarks)
**Minimum:** 3-4 algorithms tested on 2-3 graphs = 6-12 result rows

**Example:**
```
algorithm,test_graph,entities_tested,duplicates_found,true_positives,false_positives,precision,recall
fuzzy-matching,graph-001,150,22,19,3,0.86,0.95
semantic-embedding,graph-001,150,21,20,1,0.95,1.0
llm-based,graph-001,150,20,20,0,1.0,1.0
hybrid,graph-001,150,21,20,1,0.95,1.0
```

### 3. Accuracy Measurements

**File:** `accuracy-analysis.md`
**Required Measurements:**
- Precision, recall, F1 score for each algorithm on each test graph
- Confusion matrices (true positives, false positives, true negatives, false negatives)
- Threshold optimization curves (for algorithms with tunable thresholds)
- Distribution of false positives (what types of entities were wrongly merged?)
- Distribution of false negatives (what types of duplicates were missed?)

**Example Analysis:**
```markdown
## Fuzzy Matching Algorithm

### Overall Performance
- Precision: 86% (19/22 detected duplicates were correct)
- Recall: 95% (19/20 ground truth duplicates found)
- F1: 0.90

### False Positive Analysis (3 incorrect merges)
- 2 cases: Similar names but different organizations
- 1 case: Same last name, different first names

### False Negative Analysis (1 missed duplicate)
- 1 case: Completely different name spellings (nickname variant)
```

### 4. Code Examples Showing Merge Approach

**File:** `deduplication-code-examples.md`
**Requirements:**
- Show implementation examples for 3-4 algorithm approaches (fuzzy, semantic, LLM, hybrid)
- Pseudocode or language-specific snippets demonstrating core logic
- Include example input/output showing how each algorithm would process one duplicate pair
- Explain threshold tuning approach with 1-2 concrete examples
- Demonstrate understanding of algorithm strengths/weaknesses on sample data

**Example Format:**
```markdown
## Fuzzy Matching Example
Input: {"id": "author-001", "name": "John Smith"} vs {"id": "author-002", "name": "Jon Smith"}
Algorithm: Jaro-Winkler similarity
Code: [implementation]
Output: Similarity score 0.92, above threshold 0.85 → merge
```

---

## Deliverable Specifications

### Primary Deliverable: Technical Report (≥3,000 words)

**Required Sections:**
1. Algorithm Comparison Matrix
2. Precision-Recall Curves
3. Threshold Recommendations
4. Cost Analysis
5. Scalability Results
6. Edge Case Analysis
7. Implementation Guidance

---

## Success Criteria

### MANDATORY (Research incomplete until ALL checked)

- [ ] **Test dataset created:** `test-graphs-duplicates.json` with 1-2 graphs, 10-20 entities, 2-3 ground truth duplicates each
- [ ] **Deduplication results file:** `deduplication-results.csv` with results from YOUR test data
- [ ] **Accuracy analysis:** `accuracy-analysis.md` with precision/recall/F1 for each algorithm on sample data
- [ ] **Code examples:** `deduplication-code-examples.md` showing implementation approach for 3-4 algorithms
- [ ] **All 4 algorithms evaluated:** Fuzzy matching, semantic embeddings, LLM-based, hybrid with examples
- [ ] **Threshold tuning explained:** Documentation showing how to optimize thresholds with concrete examples
- [ ] **Algorithm comparison:** Clear analysis of when each algorithm performs well/poorly
- [ ] **Edge cases identified:** Documentation of which duplicate types are challenging for each approach

### RECOMMENDED (Enhances quality)

- [ ] Published benchmark comparisons (supplementary reference)
- [ ] Cost analysis per entity deduplicated
- [ ] Risk assessment and edge cases
- [ ] Integration guidance for Knowledge Graph Merge layer
- [ ] Monitoring strategy for deduplication in production

---

## DELIVERABLE VALIDATION

**Before marking research complete, verify:**

### 1. Test Dataset File Exists

```bash
# Check file exists and has valid JSON structure
test -f test-graphs-duplicates.json && jq . test-graphs-duplicates.json > /dev/null
# Check minimum number of duplicate pairs per graph
jq '.[] | .ground_truth_duplicates | length' test-graphs-duplicates.json
# Expected output: 2-3 for each graph
```

### 2. Deduplication Results File

- Must show results on YOUR sample test dataset
- Required columns: algorithm, test_graph, entities_tested, duplicates_found, true_positives, false_positives, precision, recall
- Minimum 3-4 algorithms tested on sample data
- Results should be actual measurements on your test data

### 3. Accuracy Analysis Document

- Must include precision/recall/F1 calculations for each algorithm on your test data
- Analysis of which duplicate types each algorithm handles well
- Documentation of false positives and negatives with examples
- Clear comparison of algorithm strengths/weaknesses

### 4. Code Examples Validation

```bash
# Check file exists
test -f deduplication-code-examples.md
# Must contain clear implementation examples
grep -c "Algorithm" deduplication-code-examples.md
# Should find examples for 3-4 different approaches
```

---

## RESEARCH ACCEPTANCE CRITERIA

**This research will be REJECTED if:**

- ❌ Test dataset not created (literature review without sample data)
- ❌ No results on YOUR test data (only published benchmarks from other domains)
- ❌ No code examples showing implementation approach
- ❌ No clear algorithm comparison (which is best for which types of duplicates?)
- ❌ No threshold tuning explanation (how do you balance precision vs recall?)
- ❌ No analysis of algorithm strengths/weaknesses on concrete examples

**Rationale:**

This research should demonstrate understanding of deduplication approaches through concrete examples on representative data. Show that you understand when each algorithm works well, how thresholds affect results, and what tradeoffs exist. Use your sample graphs to validate approach, not to build a production system.

**What "code examples" means:**

- Not: "I read papers on fuzzy matching and semantic embeddings"
- Yes: "Here's how each algorithm handles these 2-3 duplicate pairs, with example output showing similarity scores and merge decisions"

**What "algorithm evaluation" means:**

- Not: "Paper X says fuzzy matching achieves 90% precision on general data"
- Yes: "On my 10-20 entity sample, fuzzy matching caught 2/3 duplicates (recall 67%), semantic matching caught all 3 (recall 100%), but semantic has more false positives"

---

**Begin research now.**
