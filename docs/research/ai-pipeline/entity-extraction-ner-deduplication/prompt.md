## Deep Research Assignment: NER Libraries & Entity Deduplication Strategies

**ASSIGNMENT ID:** RES-2025-ENTITY-NER-002
**Research Type:** NER library evaluation + deduplication algorithm testing
**Decision Context:** Traditional NER libraries could reduce costs vs LLM APIs, but only if quality is comparable. Entity deduplication with 99%+ precision is critical to prevent false merges that corrupt the knowledge graph.

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

**Focus on:** Layer 5 (Entity Extraction) - understand deduplication requirements and quality gates.

---

## Researcher Role

You are an NLP engineering specialist with expertise in named entity recognition, traditional ML approaches, and entity resolution systems. You combine knowledge of transformer models with practical deduplication experience. Your role is to determine if NER libraries can replace or augment LLM extraction and identify the optimal deduplication strategy.

---

## Deployment Context

**Performance Requirements:**
- Entity extraction F1: Match or exceed LLM baseline (85%+)
- NER speed: >100 entities per second on CPU
- Deduplication precision: 99%+ (false positive rate <1%)
- Deduplication recall: 95%+ (false negative rate <5%)
- Memory: <2GB for NER model deployment
- Cost: Minimize total extraction cost

---

## Scope Specification

### NER Libraries to Evaluate

**Category 1: Production-Ready Libraries**
- **spaCy**: en_core_web_trf, accuracy, speed, customization
- **Flair**: NER models, context embeddings, domain adaptation
- **Hugging Face**: DistilBERT/RoBERTa NER, fine-tuning

**Category 2: Hybrid Approaches**
- spaCy candidate detection + LLM validation
- NER confidence filtering + LLM for low-confidence
- Multi-model voting (combine NER + LLM predictions)

### Deduplication Strategies

**Strategy 1: Fuzzy Matching**
- Levenshtein distance with threshold tuning
- Jaro-Winkler similarity for name matching
- Edit distance with domain-specific weights

**Strategy 2: Semantic Matching**
- SentenceTransformers embeddings
- Cosine similarity threshold optimization
- Batch embedding for performance

**Strategy 3: Hybrid Matching**
- Fuzzy matching for high-similarity pairs
- Semantic matching for moderate similarity
- LLM verification for ambiguous cases

---

## Methodology

### Phase 1: NER Library Benchmarking (Days 1-1.5)
- Evaluate 2-3 NER libraries (spaCy, Flair, or HuggingFace)
- Test on focused sample set OR analyze published benchmarks
- Document F1, speed, memory, model size (empirical OR from sources)
- Consider fine-tuning potential
- Compare to LLM baseline

### Phase 2: Hybrid Approach Testing (Day 2)
- Implement spaCy + LLM hybrid
- Test confidence-based routing
- Measure accuracy improvement and cost
- Analyze error reduction patterns

### Phase 3: Deduplication Evaluation (Days 2.5-3.5)
- Create focused test set with known duplicates (2-3 examples)
- Evaluate fuzzy and semantic matching approaches
- Analyze threshold sensitivity
- Document precision and recall characteristics (empirical OR from sources)
- Error analysis: false positives and negatives

### Phase 4: Integration and Recommendations (Day 4)
- End-to-end cost comparison
- Performance benchmarking
- Integration complexity assessment
- Final recommendations

---

## MANDATORY DELIVERABLES (Research incomplete without these)

### 1. Test Dataset with Duplicates and Variations

**File:** `test-dataset-entities.json`
**Format:** Array of test cases with ground truth labels
**Minimum:** 2-3 illustrative entities with duplicates and variations
**Structure:**
```json
[
  {
    "id": "entity-001",
    "canonical_name": "John Smith",
    "variations": ["John T. Smith", "J. Smith", "John Smith Jr."],
    "entity_type": "PERSON",
    "attributes": {"affiliation": "MIT", "role": "researcher"},
    "expected_duplicates": ["entity-002", "entity-005"],
    "is_duplicate": true,
    "match_confidence": 0.95,
    "notes": "Name variation with same affiliation"
  }
]
```

**Validation:** `jq length test-dataset-entities.json` returns ≥2

### 2. NER Model Comparison Results

**File:** `ner-model-comparison.csv`
**Format:** CSV with columns: model_name, accuracy, precision, recall, f1, speed_entities_per_sec, memory_mb, inference_time_ms
**Required:** Representative results (empirical OR from reliable published benchmarks)
**Minimum:** 2-3 NER models compared
**Evidence:** Include accuracy breakdown by entity type

### 3. Deduplication Algorithm Results

**File:** `deduplication-results.json`
**Format:** JSON with algorithm performance metrics
**Requirements:**
- Tested on YOUR 30+ entity dataset
- Measured accuracy on test data (not published benchmarks)
- Include results for: fuzzy matching, semantic matching, hybrid approach

**Structure:**
```json
{
  "algorithm": "fuzzy_matching",
  "threshold": 0.85,
  "precision": 0.95,
  "recall": 0.92,
  "f1": 0.935,
  "false_positives": 2,
  "false_negatives": 3,
  "avg_inference_time_ms": 45,
  "test_dataset_size": 30,
  "notes": "Levenshtein distance with domain-specific weights"
}
```

### 4. Working Code Repository

**File:** `code-repository-link.md` with code examples demonstrating understanding
**Requirements:**
- Code examples showing NER + deduplication approach
- Include: README, dependencies, sample test data
- Demonstrate understanding of NER + deduplication pipeline
- Show preprocessing, extraction, and deduplication logic
- Focus on demonstrating understanding, not production system

**Validation:** Code examples demonstrate understanding of approach

---

## Deliverable Specifications

### Primary Deliverable: Technical Report (≥3,000 words)

**Required Sections:**
1. NER Library Comparison Matrix
2. NER vs LLM vs Hybrid Accuracy Analysis
3. Deduplication Precision/Recall Results
4. Cost Analysis: Deployment vs API
5. Speed and Scalability Benchmarks
6. Implementation Recommendations
7. Risk Assessment

---

## Success Criteria

### MANDATORY (Research incomplete until ALL checked)

- [ ] **Test dataset created:** `test-dataset-entities.json` with 2-3 illustrative entities and variations
- [ ] **NER model comparison:** `ner-model-comparison.csv` with representative measurements (empirical OR cited)
- [ ] **Deduplication algorithm results:** `deduplication-results.json` with documented accuracy
- [ ] **Code repository:** `code-repository-link.md` with code examples demonstrating understanding
- [ ] **2-3 NER libraries compared:** F1 scores (empirical OR from reliable sources)
- [ ] **Deduplication precision ≥95% documented:** Based on evidence (empirical OR from sources)
- [ ] **Deduplication recall ≥90% documented:** Based on evidence (empirical OR from sources)
- [ ] **Speed characteristics documented:** >100 entities/second potential demonstrated
- [ ] **Cost analysis:** NER deployment vs LLM with pricing data

### RECOMMENDED (Enhances quality)

- [ ] Hybrid NER + LLM approach tested and compared
- [ ] Published benchmark comparisons (supplementary context)
- [ ] Domain-specific fine-tuning results (e.g., research papers, author names)
- [ ] Integration testing (gap detection → entity extraction → deduplication flow)
- [ ] Confidence scoring strategy for deduplication matches
- [ ] Risk assessment and error analysis

---

## DELIVERABLE VALIDATION

**Before marking research complete, verify:**

### 1. Test Dataset File Exists

```bash
# Check file exists and has minimum count
test -f test-dataset-entities.json && jq length test-dataset-entities.json
# Expected output: 2-3 illustrative examples
```

### 2. NER Model Comparison Results

- Should show representative performance (empirical OR from reliable sources)
- Required columns: model_name, accuracy, precision, recall, f1, speed, memory, inference_time
- Minimum 2-3 NER models with complete data showing understanding
- Include accuracy breakdown per entity type

### 3. Deduplication Algorithm Results

- Should include results for 2-3 algorithms (fuzzy, semantic, hybrid)
- Show precision and recall characteristics (empirical OR from sources)
- Include false positive and false negative analysis
- Document threshold considerations

### 4. Code Repository Validation

```bash
# Code examples should demonstrate understanding
# Full production pipeline not required
# Focus on illustrative examples showing NER + dedup approach
```

---

## RESEARCH ACCEPTANCE CRITERIA

**This research will be REJECTED if:**

- ❌ No illustrative examples provided (need 2-3 representative entities)
- ❌ No evidence of understanding (must show empirical testing OR deep analysis of published benchmarks)
- ❌ Code examples missing (focused examples demonstrating approach required)
- ❌ NER/deduplication performance analysis lacking depth
- ❌ Precision/recall analysis missing or unsupported
- ❌ No integration analysis (must show understanding of NER + dedup pipeline)
- ❌ Cost analysis lacking evidence or depth

**Rationale:**

We need empirical validation, not literature synthesis. Published NER benchmarks (OntoNotes, CONLL) don't account for our domain-specific text (research papers, author names, citations). We must measure actual NER and deduplication performance on real research text and real entity variations. The system must work reliably in our specific context, not just in academic benchmarks.

**What "code examples demonstrating understanding" means:**

- Not: "Here's a one-line comment about spaCy"
- Yes: "Here's focused code showing NER extraction with spaCy and deduplication logic, with comments explaining approach"

**What "evidence-based analysis" means:**

- Not: "spaCy is probably good"
- Yes: "Testing on 2-3 samples showed spaCy F1=78%, consistent with OntoNotes benchmark. Flair achieved 85% in published research"

---

**Begin research now.**
