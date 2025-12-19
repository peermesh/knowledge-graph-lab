## Deep Research Assignment: Document Ingestion Pipeline - Parsing, Chunking & Preprocessing

**ASSIGNMENT ID:** RES-2025-DOC-INGEST-001
**Research Type:** Parser evaluation + chunking strategy testing
**Decision Context:** Document ingestion is the pipeline entry point. Text extraction quality directly impacts entity extraction accuracy. Parser choice determines supported formats, latency, and edge case handling.

---

**📝 PROMPT IMPROVEMENTS APPLIED (2025-11-16)**

This prompt has been enhanced based on learnings from Track 01 (Query Processing) research execution. Track 01 research scored A grade (90%+) but lacked empirical validation (no test document corpus created, no hands-on benchmarking, code examples were illustrative only). To ensure higher-quality empirical research, this prompt now includes:

- ✅ Explicit MANDATORY DELIVERABLES section with file paths and formats
- ✅ Enhanced Success Criteria distinguishing mandatory vs recommended items
- ✅ DELIVERABLE VALIDATION section with verification commands
- ✅ RESEARCH ACCEPTANCE CRITERIA explaining rejection conditions
- ✅ Clear distinction: empirical measurements required, not literature extrapolation

**Your research will be more valuable if you create actual test document corpora and working parsers, not just synthesize existing literature.**

---

## 🚨 PREREQUISITES: Read This First

**File:** `ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md`
**Location:** `/Users/grig/work/peermesh/repo/knowledge-graph-lab-alpha/.dev/_sprint_ai_module_nov13/ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md`

**Focus on:** Layer 4 (Document Ingestion) - understand how raw documents are transformed into clean, chunked text ready for entity extraction.

---

## Researcher Role

You are a document processing specialist with 10+ years in text extraction, OCR systems, and content parsing. You combine deep knowledge of PDF structure, HTML parsing, and text preprocessing with practical experience building production document pipelines. Your role is to identify the optimal parser combination and chunking strategy for our knowledge graph pipeline.

---

## Deployment Context

**Performance Requirements:**
- Text extraction accuracy: 90%+ for text PDFs, 85%+ for HTML
- Parsing latency: <10 seconds per document (target <5 seconds)
- Format support: PDF, HTML, plain text (minimum)
- Edge case handling: Scanned PDFs, tables, multi-column layouts
- Chunk quality: Preserve semantic coherence for entity extraction
- Memory efficiency: <500MB per document process

**Current Challenges:**
- Unknown which parsers handle academic PDFs effectively
- Need chunking strategy that doesn't split entities across chunks
- Must remove boilerplate without losing important content
- Handle documents with mixed content (text, tables, code)
- Balance extraction quality with processing speed

---

## Scope Specification

### PDF Parsing Libraries to Evaluate

**Category 1: Layout-Aware Parsers**
- **pdfplumber**: Layout detection, table extraction, coordinate-based
- **Unstructured**: Multi-format support, chunking built-in
- Evaluation: Table handling, multi-column support, accuracy

**Category 2: Text-Focused Parsers**
- **PyPDF2**: Basic text extraction, metadata handling
- **pdfminer.six**: Low-level PDF parsing, customizable
- Evaluation: Speed, accuracy on simple documents, reliability

**Category 3: OCR Services**
- **Google Vision API**: Scanned PDF handling, cost
- **AWS Textract**: Table extraction, pricing model
- Evaluation: Accuracy on scanned PDFs, latency, cost

**Category 4: Unified Solutions**
- **Apache Tika**: Java-based, multi-format support
- Evaluation: Accuracy, integration complexity, performance

### HTML Parsing Libraries to Evaluate

**Category 1: Boilerplate Removal**
- **Trafilatura**: Content extraction, boilerplate removal
- **Readability**: Python port, article extraction
- Evaluation: Accuracy at isolating main content

**Category 2: General Parsing**
- **BeautifulSoup**: CSS selectors, flexible parsing
- **lxml**: Fast parsing, XPath support
- Evaluation: Speed, flexibility, integration ease

**Category 3: Specialized Extractors**
- **Newspaper3k**: News article extraction, metadata
- Evaluation: Domain-specific accuracy, generalization

### Text Chunking Strategies

**Strategy 1: Fixed-Size Chunking**
- Chunk by character count (500, 1000, 2000 chars)
- Overlap strategies (0%, 10%, 20%)
- Evaluation: Speed, consistency, entity splitting rate

**Strategy 2: Semantic Chunking**
- Sentence-based boundaries
- Paragraph-based boundaries
- Section-based (using headers)
- Evaluation: Coherence, entity extraction quality impact

**Strategy 3: Hybrid Approaches**
- Fixed-size with sentence boundaries
- Hierarchical (section → paragraph → sentence)
- Evaluation: Balance of speed and quality

### Evaluation Framework

**Accuracy Testing:**
- Create test set: 20-30 diverse documents
- Academic papers (text PDFs)
- Web articles (HTML with ads/navigation)
- Technical documentation (code samples, tables)
- Scanned documents (if OCR is in scope)
- Measure: % of text correctly extracted vs ground truth
- Document: failure modes, edge cases, error patterns

**Performance Benchmarking:**
- Latency: Parse time per document, per page
- Memory: Peak memory usage during parsing
- Scalability: Performance with 100-page documents
- Reliability: Success rate across document types
- Resource usage: CPU utilization patterns

**Quality Assessment:**
- Table preservation: Are tables extracted or lost?
- Structure preservation: Headers, lists, formatting
- Boilerplate removal: Navigation, ads, footers removed?
- Entity coherence: Do chunks split entities/concepts?
- Downstream impact: Entity extraction quality with each approach

---

## Research Questions

1. **Parser Accuracy?**
   - Which parser achieves 90%+ accuracy on our document types?
   - What accuracy tradeoff for speed optimization?
   - Which edge cases cause failures?

2. **Format Support?**
   - Do we need specialized parsers per format?
   - Can one unified solution handle all formats?
   - What's the cost of format diversity?

3. **Chunking Impact?**
   - Does semantic chunking improve entity extraction?
   - What's the optimal chunk size for our use case?
   - How much overlap is beneficial?

4. **Boilerplate Handling?**
   - Can automated removal achieve 95%+ precision?
   - Are there patterns we can exploit?
   - Risk of removing important content?

5. **Edge Cases?**
   - How do we handle scanned PDFs cost-effectively?
   - What about tables, code blocks, equations?
   - Multi-column layouts and complex formatting?

---

## Methodology

### Phase 1: Parser Library Testing (Days 1-1.5)
- Evaluate 2-3 PDF parsers and 1-2 HTML parsers
- Create focused test set (2-3 representative documents)
- Extract text and demonstrate understanding of differences
- Document accuracy tradeoffs (measured or from reliable sources)
- Document latency considerations (measured or from reliable sources)
- Document edge cases and failure modes
- Create parser comparison matrix

### Phase 2: Chunking Strategy Evaluation (Day 2)
- Implement 3-4 chunking approaches
- Apply to parsed documents
- Measure chunk coherence and entity splitting
- Test impact on entity extraction quality
- Benchmark chunking overhead
- Document optimal chunk sizes
- Create chunking strategy recommendations

### Phase 3: Integration and Optimization (Day 3)
- Design complete pipeline architecture
- Implement error handling and validation
- Test with diverse document formats
- Optimize bottlenecks
- Document failure recovery strategies
- Create deployment guidelines

### Phase 4: Benchmarking and Recommendations (Day 4)
- Run comprehensive performance benchmarks
- Create accuracy and latency comparison tables
- Document cost model (OCR, infrastructure)
- Synthesize findings into recommendations
- Create integration guide and code examples

---

## MANDATORY DELIVERABLES (Research incomplete without these)

### 1. Test Document Corpus

**File:** `test-corpus.zip` or organized directory structure
**Format:** Actual document files (PDF, HTML, arXiv, research papers, etc.)
**Minimum:** 2-3 illustrative examples of various types:
- 1-2 academic PDF papers (text PDFs, not scanned)
- 1 research paper with scanned content/OCR requirements
- 1 HTML web article (with boilerplate: navigation, ads, sidebars)
- 1 technical documentation (with tables, code blocks, formatting)

**Structure:**
```
test-corpus/
  ├── papers/
  │   ├── paper_001.pdf
  │   ├── paper_002.pdf
  │   └── ...
  ├── html/
  │   ├── article_001.html
  │   └── ...
  ├── ground_truth/
  │   ├── paper_001_extracted.txt
  │   └── ...
  └── README.md (describing corpus and sources)
```

**Validation:** `find test-corpus -type f | wc -l` returns ≥2

### 2. Ingestion Pipeline Implementation (Working Code)

**File:** `code-repository-link.md` with link to code examples
**Requirements:**
- Code examples demonstrating understanding of parser integration
- Include focused examples showing approach for 2-3 parser candidates
- Include chunking strategy examples
- Show how you would evaluate parsers on test corpus
- Focus on demonstrating understanding, not production-ready system

**Validation:**
```bash
# Code should demonstrate understanding through focused examples
# Not required to be fully executable end-to-end system
```

### 3. Processing Benchmarks (Empirical Measurements)

**File:** `benchmark-results.csv`
**Format:** CSV with columns: parser_name, document_type, doc_count, accuracy_percent, avg_latency_ms, memory_mb, cost_score

**Required Data (YOUR actual measurements OR representative published benchmarks):**
- Extraction accuracy on each document type (measured or cited from reliable sources)
- Parsing latency per document (measured or cited)
- Memory usage per document process (measured or cited)
- Success rate across document types (measured or cited)
- Cost assessment (free/paid, licensing)

**Minimum:** Representative examples from 2-3 parsers tested or benchmarked

**Example rows:**
```
pdfplumber,pdf_text,10,92.5,450,45,5
pdfminer.six,pdf_text,10,88.2,380,32,5
unstructured,pdf_text,10,95.1,2100,180,3
trafilatura,html,5,96.8,120,25,5
```

### 4. Error Handling and Edge Case Testing

**File:** `error-handling-results.md`
**Required:**
- Actual test results for handling edge cases (scanned PDFs, tables, code blocks)
- Error recovery strategies and success rates
- Failure mode documentation
- Latency and quality degradation under error conditions

**Sections:**
- Scanned PDF handling (success rate, OCR fallback testing)
- Table extraction (correct table structure preservation %)
- Multi-column layout handling (accuracy on magazine/newspaper formats)
- Code blocks/equations (preservation of technical content)
- Boilerplate removal precision (% of correct content preserved)

### 5. Code Repository Link

**File:** `code-repository-link.md`
**Format:** Markdown file with:
- URL to repository (GitHub, GitLab, or similar)
- Installation instructions
- Usage examples
- Test dataset information
- Benchmark reproduction instructions

**Validation:** Repository exists, is cloneable, has working tests that pass

---

## Deliverable Specifications

### Primary Deliverable: Technical Report (≥3,000 words)

**Required Sections:**
1. Executive Summary with parser recommendations
2. Parser Accuracy Matrix (per-document results)
3. Performance Benchmarks (latency, memory)
4. Chunking Strategy Analysis with examples
5. Boilerplate Removal Effectiveness
6. Edge Case Handling Documentation
7. Pipeline Architecture Design
8. Integration Guidelines
9. Cost Model and Scaling Analysis
10. Risk Assessment

### Secondary Deliverables

**Working Code Examples:**
- Parser implementations for top candidates
- Chunking algorithm implementations
- Integration test suite
- Performance benchmark scripts

**Test Dataset:**
- Curated set of test documents
- Ground truth annotations
- Edge case examples
- Benchmark results

---

## Success Criteria

### MANDATORY (Research incomplete until ALL checked)

- [ ] **Test corpus created:** `test-corpus/` with 2-3 illustrative documents (PDFs, HTML)
- [ ] **Benchmark results file:** `benchmark-results.csv` with representative measurements (empirical OR cited from reliable sources)
- [ ] **Error handling documentation:** `error-handling-results.md` with edge case analysis
- [ ] **Code repository:** `code-repository-link.md` with code examples demonstrating understanding
- [ ] **Evaluated 2-3 PDF parsers:** With accuracy data (measured OR from reliable sources)
- [ ] **Evaluated 1-2 HTML parsers:** With boilerplate removal analysis
- [ ] **Tested 2-3 chunking strategies:** With impact analysis
- [ ] **Documented 90%+ accuracy potential:** Based on evidence (measured OR from reliable sources)
- [ ] **Latency documented:** Pipeline latency characteristics understood
- [ ] **Key edge cases analyzed:** Scanned PDFs, tables, multi-column, code blocks, boilerplate

### RECOMMENDED (Enhances quality)

- [ ] Published parser comparison benchmarks (supplementary context only)
- [ ] Literature review on document parsing best practices
- [ ] Cost optimization analysis (OCR service costs, infrastructure)
- [ ] Failure mode analysis and recovery recommendations
- [ ] Integration design with Layer 1 (Entity Extraction)

---

## Evaluation Rubric

### Extraction Accuracy (40 points)
- 95%+ accuracy on text PDFs: 15 points
- 85-94%: 10 points
- <85%: 5 points
- HTML parsing 95%+ accuracy: 10 points
- Boilerplate removal 95%+ precision: 10 points
- Edge case handling: 5 points

### Performance (20 points)
- <5 seconds per document: 20 points
- 5-10 seconds: 15 points
- >10 seconds: 10 points

### Reliability (20 points)
- Handles diverse formats gracefully: 10 points
- Good error handling: 5 points
- Clear failure modes documented: 5 points

### Integration (15 points)
- Easy Python integration: 5 points
- Low dependency complexity: 5 points
- Good documentation: 5 points

### Cost Efficiency (5 points)
- Free/low-cost solution: 5 points
- Moderate cost: 3 points
- High cost: 0 points

**Decision Threshold:**
- Score 80+: Strong recommendation for production
- Score 65-79: Viable with documented limitations
- Score <65: Needs improvement or alternative approach

---

## DELIVERABLE VALIDATION

**Before marking research complete, verify:**

### 1. Test Corpus Exists

```bash
# Check corpus directory and file count
find test-corpus -type f | wc -l
# Expected output: 2-3 illustrative examples
```

### 2. Benchmark Results Table

- Should show representative measurements (empirical OR from reliable sources)
- Published benchmarks are acceptable when combined with understanding
- Required columns: parser_name, document_type, doc_count, accuracy_percent, avg_latency_ms, memory_mb
- Minimum 2-3 parsers with data showing understanding
- Accuracy values from empirical testing OR cited reliable sources

### 3. Error Handling Documentation

- Must include ACTUAL test results for edge cases
- Must show success/failure rates for specific scenarios (scanned PDFs, tables, etc.)
- Must document latency degradation under error conditions
- Must describe recovery strategies tested

### 4. Code Repository Validation

```bash
# Code examples should demonstrate understanding
# Full production pipeline not required
# Focus on illustrative examples showing parser integration approach
```

### 5. Pipeline Performance Proof

- Must include actual latency measurements on YOUR test corpus
- Proof: execution logs, timing output, or profiling results
- Show results for multiple document types and sizes
- Document both cold and warm execution times

---

## RESEARCH ACCEPTANCE CRITERIA

**This research will be REJECTED if:**

- ❌ No illustrative examples provided (need 2-3 representative documents)
- ❌ No evidence of understanding (must show empirical testing OR deep analysis of published benchmarks)
- ❌ Code examples missing (focused examples demonstrating approach required)
- ❌ No accuracy analysis (empirical OR from reliable published sources)
- ❌ No latency analysis (empirical OR from reliable published sources)
- ❌ No edge case analysis (must analyze scanned PDFs, tables, boilerplate handling)
- ❌ Parser comparison lacking depth (must show understanding through evidence)

**Rationale:**

We need empirical validation tailored to our domain. Published parser benchmarks don't account for our specific document types (academic papers, research articles, technical documentation, web sources). The parser must work on actual research documents against our specific quality standards.

Accuracy must be measured by comparing YOUR parser output against ground truth extracted from YOUR test documents - not by citing benchmark papers that tested different document types and quality standards.

**What "code examples demonstrating understanding" means:**

- Not: "Here's a one-line comment about pdfplumber"
- Yes: "Here's focused code showing how I would integrate pdfplumber, with comments explaining tradeoffs"

**What "evidence-based analysis" means:**

- Not: "I think pdfplumber is probably good"
- Yes: "Testing on 2 sample PDFs showed 92% accuracy, consistent with published benchmark X showing 95% on dataset Y"

**What "edge case analysis" means:**

- Not: "Scanned PDFs need OCR"
- Yes: "Scanned PDF handling tested on 1-2 samples OR analyzed from published research showing 60% success rate with quality issues"

---

**Begin research now.**
