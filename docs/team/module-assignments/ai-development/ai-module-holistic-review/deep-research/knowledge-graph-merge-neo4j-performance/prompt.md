## Deep Research Assignment: Neo4j Merge Performance & Transaction Integrity

**ASSIGNMENT ID:** RES-2025-NEO4J-PERF-002
**Research Type:** Neo4j performance benchmarking + transaction integrity testing
**Decision Context:** Merge performance determines knowledge graph freshness. Can we achieve <60 second merges for 100K entities? Poor consistency during concurrent merges corrupts the graph permanently.

---

**📝 PROMPT IMPROVEMENTS APPLIED (2025-11-16)**

This prompt has been enhanced based on learnings from Track 01 (Query Processing) research execution. Track 01 research scored A grade (90%+) but lacked empirical validation (no test dataset created, no hands-on benchmarking, code examples were illustrative only). To ensure higher-quality empirical research, this prompt now includes:

- ✅ Explicit MANDATORY DELIVERABLES section with file paths and formats
- ✅ Enhanced Success Criteria distinguishing mandatory vs recommended items
- ✅ DELIVERABLE VALIDATION section with verification commands
- ✅ RESEARCH ACCEPTANCE CRITERIA explaining rejection conditions
- ✅ Clear distinction: empirical measurements required, not literature extrapolation

**Your research will be more valuable if you create actual test graphs and working code, not just synthesize existing literature.**

---

## 🚨 PREREQUISITES: Read This First

**File:** `ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md`
**Location:** `/Users/grig/work/peermesh/repo/knowledge-graph-lab-alpha/.dev/_sprint_ai_module_nov13/ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md`

**Focus on:** Layer 7 (Knowledge Graph Merge) - Neo4j performance determines update latency and system economics.

---

## Researcher Role

You are a Neo4j performance engineer with 10+ years in graph database optimization, Cypher query tuning, and transaction management. You combine deep knowledge of graph algorithms with practical experience scaling production Neo4j systems. Your role is to optimize merge performance while maintaining data integrity.

---

## Deployment Context

**Performance Requirements:**
- Merge throughput: >100 entities/second (100K in <17 minutes target)
- Deduplication lookup: <100ms per entity
- Concurrent merges: Support 3-5 simultaneous writers
- Consistency: ACID guarantees, no corruption
- Memory: Work within 8GB heap constraint
- Scalability: Handle graphs with 1M+ nodes

---

## Scope Specification

### Performance Dimensions to Benchmark

**Query Patterns:**
- MERGE statement optimization
- Batch size tuning (100 vs 1K vs 10K)
- UNWIND for batch operations
- Index-backed lookups

**Index Strategies:**
- Single-property indexes
- Composite indexes for deduplication
- Full-text search indexes
- Index warmup and caching

**Transaction Management:**
- Transaction size optimization
- Isolation level selection
- Lock contention analysis
- Deadlock prevention

**Concurrent Access:**
- Multiple writers performance
- Write conflict resolution
- Queue-based serialization vs parallel

---

## Methodology

### Phase 1: Baseline Benchmarking
- Set up Neo4j with default configuration
- Create representative test graphs at different scales (e.g., 1K, 10K)
- Implement basic MERGE queries
- Measure throughput and latency with EXPLAIN/PROFILE
- Document query execution plans

### Phase 2: Index Optimization
- Test with and without indexes
- Measure lookup performance improvement
- Document optimal index strategy for deduplication
- Show before/after PROFILE output

### Phase 3: Batch Processing Approach
- Test batch size impact (small vs medium batches)
- Show PROFILE for different UNWIND patterns
- Document throughput at representative scale
- Explain scaling approach for larger graphs

### Phase 4: Concurrent Access
- Test 2-3 concurrent writers on sample graph
- Document transaction behavior
- Validate consistency with simple examples

---

## MANDATORY DELIVERABLES (Research incomplete without these)

### 1. Test Graph Setup Documentation

**File:** `test-graph-setup.md`
**Format:** Documentation with setup instructions and examples
**Required Examples:**
- Setup for 1K node representative graph
- Setup for 10K node graph (optional but helpful)
- Cypher queries for creating test graphs
- Sample merge data and verification queries

**File Structure:**
```
test-graphs/
├── setup-representative.cypher
├── sample-merge-data.json
└── verification-queries.cypher
```

**Content Requirements:**
- Neo4j instance configuration
- Graph structure: node types, relationships, properties
- Cypher script to create test graph
- Explanation of how approach scales to 100K
- Verification queries

**Validation:**
```bash
# Graph must be creatable
neo4j-admin import --nodes test-graphs/setup-representative.cypher
cypher "MATCH (n) RETURN count(n)" returns expected count
```

### 2. Performance Benchmark Results

**File:** `merge-benchmarks.csv`
**Format:** CSV with performance measurements
**Required:** Actual PROFILE measurements from YOUR test graphs
**Minimum:** Representative benchmark results:
- Graph size: 1K and/or 10K nodes
- Merge operations: single and batch approaches
- Throughput and latency measurements
- With and without index comparison

**Example:**
```csv
operation,graph_size,batch_size,throughput_eps,latency_p50_ms,latency_p99_ms
MERGE,1K,1,850,1.2,4.5
MERGE,1K,100,950,10.5,42.1
MERGE,10K,100,750,15.3,68.5
```

### 3. Neo4j Performance Profiling

**File:** `neo4j-performance-profile.md`
**Required Content:**
- Sample PROFILE output for key merge patterns
- Query execution plans (EXPLAIN and PROFILE)
- Index impact measurements (with vs without)
- Latency observations (single merge, batch operations)

**Structure:**
```markdown
## Sample Query: Single MERGE
PROFILE output here...
Latency: 1.2ms (with index), 4.8ms (without)
Index impact: 4x faster

## Sample Query: Batch MERGE with UNWIND
PROFILE output here...
Throughput characteristics
Batch size impact explanation
```

### 4. Index Optimization Results

**File:** `index-optimization-report.md`
**Format:** Documentation with index impact analysis
**Required Content:**
- Query performance without indexes
- Query performance with single-property indexes
- Query performance with composite indexes
- Measured impact on throughput
- Simple memory overhead estimate

### 5. Merge Operation Measurements

**File:** `merge-operation-metrics.json`
**Format:** Sample metrics from representative merge test
**Structure:**
```json
{
  "test_id": "merge-representative",
  "graph_size": 1000,
  "batch_size": 100,
  "total_merges": 1000,
  "total_time_seconds": 8.7,
  "throughput_entities_per_second": 114.9,
  "latency": {
    "p50_ms": 12.3,
    "p99_ms": 65.4
  },
  "consistency_validation": {
    "test_passed": true,
    "notes": "Sample concurrent test explanation"
  }
}
```

### 6. Cypher Query Examples and Explanations

**File:** `cypher-examples.md`
**Requirements:**
- Example MERGE queries (single and batch)
- UNWIND pattern examples for batch operations
- Index creation Cypher
- Query optimization techniques with explanation
- Performance characteristics commentary
- Notes on how approaches scale to larger graphs

**Example Content:**
```markdown
## Single MERGE
MATCH (n {id: 'entity1'}) ...
Performance: [Explain how this performs]

## Batch MERGE with UNWIND
UNWIND $batch as item ...
Performance: [Explain throughput characteristics]

## Index Impact
CREATE INDEX on :Entity(id)
Impact: [Show latency improvement]
```

---

## Deliverable Specifications

### Primary Deliverable: Performance Report (≥3,000 words)

**Required Sections:**
1. Merge Throughput Benchmarks
2. Latency Breakdown
3. Index Recommendations
4. Cypher Query Optimization
5. Concurrent Access Results
6. Transaction Integrity Validation
7. Scaling Projections

---

## Success Criteria

### MANDATORY (Research incomplete until ALL checked)

- [ ] **Test graphs created:** Representative setup with 1K-10K nodes documented
- [ ] **Benchmark results:** `merge-benchmarks.csv` with performance measurements
- [ ] **Performance profiling:** `neo4j-performance-profile.md` with sample PROFILE output
- [ ] **Index optimization:** `index-optimization-report.md` with with/without index comparison
- [ ] **Merge metrics:** `merge-operation-metrics.json` with representative measurements
- [ ] **Cypher examples:** `cypher-examples.md` with documented queries and performance notes
- [ ] **Throughput documented:** Sample measurements showing merge rates
- [ ] **Index impact measured:** Quantified performance improvement with indexes
- [ ] **Batch processing explained:** Documentation of batch size and UNWIND approach
- [ ] **Scaling approach:** Explanation of how approach extends to larger graphs
- [ ] **Transaction behavior:** Documentation of concurrent access approach

### RECOMMENDED (Enhances quality)

- [ ] Published benchmarks comparison (supplementary context)
- [ ] Query plan optimization recommendations
- [ ] Memory optimization tuning guide
- [ ] Failure recovery testing and documentation
- [ ] Performance projections for 1M+ node graphs
- [ ] Production deployment checklist

---

## DELIVERABLE VALIDATION

**Before marking research complete, verify:**

### 1. Test Graph Setup File

```bash
# Check file exists
test -f test-graph-setup.md

# Must contain Cypher setup script
grep -c "CYPHER\|CREATE" test-graph-setup.md
# Should contain graph creation commands
```

### 2. Benchmark Results File

```bash
# Check file exists and has data
test -f merge-benchmarks.csv && wc -l merge-benchmarks.csv
# Expected: 5+ lines (header + representative measurements)

# Verify columns are present
head -1 merge-benchmarks.csv | grep -E "throughput_eps|latency"
# Must contain actual measurements
```

### 3. Performance Profile Documentation

```bash
# Check file exists
test -f neo4j-performance-profile.md

# Must contain PROFILE output
grep -c "PROFILE\|latency" neo4j-performance-profile.md
# Should find sample PROFILE outputs
```

### 4. Index Optimization Results

```bash
# Check file exists
test -f index-optimization-report.md

# Must contain index comparison
grep -E "without|with" index-optimization-report.md
# Should compare performance with/without indexes
```

### 5. Merge Metrics JSON

```bash
# Check file exists and has valid JSON
test -f merge-operation-metrics.json && jq . merge-operation-metrics.json
# Expected: valid JSON with representative data
```

### 6. Cypher Examples Documentation

```bash
# Check file exists
test -f cypher-examples.md

# Must contain query examples
grep -c "MERGE\|UNWIND" cypher-examples.md
# Should show multiple Cypher patterns
```

---

## RESEARCH ACCEPTANCE CRITERIA

**This research will be REJECTED if:**

- ❌ Test graphs not documented (no Cypher setup provided)
- ❌ No sample PROFILE output (only literature references)
- ❌ No Cypher examples showing merge strategies
- ❌ No benchmark results on actual Neo4j instance
- ❌ Index impact not measured (no before/after comparison)
- ❌ No explanation of scaling approach for larger graphs
- ❌ Concurrent access not addressed (even at conceptual level)

**Rationale:**

This research should demonstrate understanding of Neo4j merge performance through concrete examples and sample measurements. Show that you understand merge strategies, how indexes affect performance, what batch sizes make sense, and how approaches scale. Use representative graphs to validate thinking, not to build production infrastructure.

**What "benchmarked" means:**

- Not: "According to Neo4j documentation, MERGE with batches is fast"
- Yes: "On my 1K node test graph, single MERGE = 1.2ms, batch-100 MERGE = 850 EPS. With index: 1.2ms, without index: 4.8ms = 4x improvement"

**What "performance explained" means:**

- Not: "Neo4j PROFILE output shows db hits and rows"
- Yes: "Here's the PROFILE output, here's what it shows: index lookup time dominates, batch processing reduces per-entity overhead, larger batches hit memory limits around X size"

---

**Begin research now.**
