# Neo4j Performance Profiling Guide

**Purpose:** Interpret PROFILE and EXPLAIN output for Neo4j merge query optimization
**Key Metrics:** DB hits, rows, cache hits, execution time
**Use Case:** Knowledge graph merge performance tuning

---

## PROFILE vs EXPLAIN

### EXPLAIN (Query Plan Only - No Execution)

```cypher
EXPLAIN
MATCH (e:Entity {id: 'entity_500'})
RETURN e;
```

**Output Includes:**
- Execution plan operators
- Estimated rows at each step
- Index usage indicators
- **Does NOT execute the query**

**When to Use:**
- ✅ Production query analysis (safe, no execution)
- ✅ Understanding query planner decisions
- ✅ Verifying index usage
- ✅ Comparing different query formulations

### PROFILE (Actual Execution + Metrics)

```cypher
PROFILE
MATCH (e:Entity {id: 'entity_500'})
RETURN e;
```

**Output Includes:**
- Actual rows processed
- DB hits (database access count)
- Cache hits/misses
- Execution time
- **Executes the query**

**When to Use:**
- ✅ Performance optimization
- ✅ Identifying bottlenecks
- ✅ Validating index performance
- ⚠️ Use cautiously in production (executes query)

---

## Understanding PROFILE Metrics

### 1. DB Hits

> "Abstract units of storage engine work whenever data in the database is touched"

**What it Measures:**
- Number of times Neo4j accesses stored data structures
- Reads from nodes, relationships, properties, indexes
- **NOT** 1:1 equivalent (different operations have different costs)

**Interpretation:**
- **Lower is better** (fewer database accesses)
- **Spikes indicate problems** (full scans, missing indexes, Cartesian products)
- **Use for relative comparison** (not absolute performance prediction)

**Typical DB Hits by Operation:**

| Operation | DB Hits | Performance |
|-----------|---------|-------------|
| NodeUniqueIndexSeek | 1-5 | Excellent ✅ |
| NodeIndexSeek | 5-20 | Good ✅ |
| NodeByLabelScan (small graph <1K) | 100-1000 | Acceptable ⚠️ |
| NodeByLabelScan (large graph >10K) | 10000+ | Poor ❌ |
| Cartesian Product | 100000+ | Very Poor ❌❌ |

### 2. Rows

> "The actual number of rows processed by each operation"

**What it Measures:**
- Data cardinality flowing between query operators
- Number of intermediate results

**Interpretation:**
- **High row counts → high work** in subsequent operations
- **Filter early** to minimize rows in later operations
- **Watch for explosions** (rows increasing unexpectedly)

**Row Flow Patterns:**

```
Good Pattern (rows decrease):
MATCH (e:Entity) WHERE e.type = 'Person'  → 200 rows
  ↓ Filter by confidence
WHERE e.confidence > 0.8                   → 50 rows
  ↓ Return
RETURN e.name                              → 50 rows

Bad Pattern (rows explode):
MATCH (e:Entity)                           → 10000 rows
MATCH (s:Source)                           → 500 rows
  ↓ Cartesian product!
(e)-[:FROM_SOURCE]->(s)                    → 5,000,000 intermediate rows ❌
```

### 3. Cache Hits/Misses

**What it Measures:**
- Page cache performance (graph data in memory)
- Hit: Data found in cache (fast)
- Miss: Data loaded from disk (slow)

**Interpretation:**
- **High cache hits:** Page cache properly sized ✅
- **High cache misses:** Need more memory for page cache ⚠️
- **Cold start effect:** First query after restart has more misses

### 4. Time (Execution Time)

**What it Measures:**
- Actual wall-clock time for each operation

**Interpretation:**
- **Use for end-to-end performance validation**
- **Compare with SLA requirements** (<100ms for deduplication lookups)
- **Account for variability** (network latency, GC pauses, concurrent load)

---

## Sample PROFILE Output Analysis

### Example 1: Optimized Single MERGE (With Unique Constraint)

**Query:**
```cypher
PROFILE
MERGE (e:Entity {id: 'entity_500'})
ON CREATE SET e.name = 'Test Entity', e.created_at = datetime()
ON MATCH SET e.updated_at = datetime()
RETURN e;
```

**PROFILE Output:**
```
+----------------------------------------------------------------------+
| Operator                   | Rows | DB Hits | Cache Hits | Time    |
+----------------------------------------------------------------------+
| ProduceResults             |    1 |       0 |          0 | 0.103ms |
| +AntiConditional(CREATE)   |    1 |       0 |          0 | 0.015ms |
| |                          |      |         |            |         |
| +Merge                     |    1 |       2 |          2 | 0.892ms |
| |                          |      |         |            |         |
| +NodeUniqueIndexSeek       |    1 |       2 |          2 | 0.847ms |
+----------------------------------------------------------------------+

Total DB Hits: 2
Execution Time: 1.857ms
```

**Analysis:**

✅ **NodeUniqueIndexSeek:** Using unique constraint index (optimal)
- **Why:** Query filters on `id` property with unique constraint
- **DB hits:** 2 (index lookup + node retrieval)
- **Rows:** 1 (found entity_500)

✅ **AntiConditional:** Efficient ON CREATE/ON MATCH handling
- **DB hits:** 0 (no additional work)
- **Rows:** 1 (flows through)

✅ **Cache Hits:** 2 cache hits, 0 misses
- **Why:** Frequently accessed entity in page cache
- **Performance:** No disk I/O needed

**Performance:** ~850 entities/second (1.857ms per MERGE)

**Bottleneck:** None - this is optimally performing

---

### Example 2: Unoptimized Single MERGE (No Index)

**Query:**
```cypher
PROFILE
MERGE (e:Entity {name: 'Test Entity 500'})
ON CREATE SET e.id = 'entity_new', e.created_at = datetime()
RETURN e;
```

**PROFILE Output:**
```
+----------------------------------------------------------------------+
| Operator                   | Rows | DB Hits | Cache Hits | Time    |
+----------------------------------------------------------------------+
| ProduceResults             |    1 |       0 |          0 | 0.089ms |
| +AntiConditional(CREATE)   |    1 |       0 |          0 | 0.012ms |
| |                          |      |         |            |         |
| +Merge                     |    1 |    1250 |        950 | 18.342ms|
| |                          |      |         |            |         |
| +Filter                    |    1 |       0 |          0 | 0.234ms |
| |                          |      |         |            |         |
| +NodeByLabelScan           | 1000 |    1250 |        950 | 17.891ms|
+----------------------------------------------------------------------+

Total DB Hits: 1250
Execution Time: 36.568ms
```

**Analysis:**

❌ **NodeByLabelScan:** Full scan of all Entity nodes (inefficient)
- **Why:** No index on `name` property
- **DB hits:** 1,250 (scanned all 1,000 entities)
- **Rows:** 1,000 (checked every entity)
- **Cache misses:** 300 (some entities not in cache)

❌ **Filter:** Applied after full scan (wasteful)
- **Rows in:** 1,000 (all entities)
- **Rows out:** 1 (found matching name)
- **Work:** 999 entities scanned unnecessarily

**Performance:** ~27 entities/second (36.568ms per MERGE)

**Performance Degradation:** **19.7x slower** than indexed version

**Fix:**
```cypher
CREATE INDEX entity_name IF NOT EXISTS
FOR (e:Entity) ON (e.name);
```

---

### Example 3: Batch MERGE with UNWIND (100 entities)

**Query:**
```cypher
PROFILE
WITH [
  {id: 'entity_1', name: 'Entity 1'},
  {id: 'entity_2', name: 'Entity 2'},
  // ... 98 more entities
  {id: 'entity_100', name: 'Entity 100'}
] AS batch

UNWIND batch AS entity_data
MERGE (e:Entity {id: entity_data.id})
ON CREATE SET e.name = entity_data.name, e.created_at = datetime()
RETURN count(e) AS merged_count;
```

**PROFILE Output:**
```
+----------------------------------------------------------------------+
| Operator                   | Rows | DB Hits | Cache Hits | Time    |
+----------------------------------------------------------------------+
| ProduceResults             |    1 |       0 |          0 | 0.102ms |
| +EagerAggregation          |    1 |       0 |          0 | 0.523ms |
| |                          |      |         |            |         |
| +AntiConditional(CREATE)   |  100 |       0 |          0 | 1.245ms |
| |                          |      |         |            |         |
| +Merge                     |  100 |     200 |        198 | 43.129ms|
| |                          |      |         |            |         |
| +NodeUniqueIndexSeek       |  100 |     200 |        198 | 41.874ms|
| |                          |      |         |            |         |
| +Unwind                    |  100 |       0 |          0 | 0.782ms |
+----------------------------------------------------------------------+

Total DB Hits: 200
Execution Time: 87.655ms
```

**Analysis:**

✅ **UNWIND:** Efficient in-memory operation
- **DB hits:** 0 (operates on parameter list in memory)
- **Rows:** 100 (one per batch item)
- **Time:** 0.782ms (negligible)

✅ **NodeUniqueIndexSeek × 100:** Index lookup for each entity
- **DB hits:** 200 total (2 per entity)
- **Rows:** 100 (one entity per lookup)
- **Cache hits:** 198/200 (99% cache hit rate)

✅ **Merge × 100:** Efficient CREATE/MATCH handling
- **Rows in:** 100
- **Rows out:** 100
- **Time:** 43.129ms total = 0.431ms per entity

✅ **EagerAggregation:** COUNT() aggregation
- **DB hits:** 0 (in-memory operation)
- **Rows in:** 100
- **Rows out:** 1 (count result)

**Performance:** ~1,140 entities/second (87.655ms for 100 entities)

**Batching Benefit:** **1.34x faster** than 100 individual optimized MERGEs
- Individual: 100 × 1.857ms = 185.7ms
- Batch: 87.655ms
- Savings: 98ms (transaction overhead reduction)

---

### Example 4: Composite Index Query (Optimally Aligned)

**Query:**
```cypher
PROFILE
MATCH (e:Entity {type: 'Person', name: 'John Doe'})
RETURN e
ORDER BY e.type, e.name;
```

**Assumption:** Composite index exists on `(type, name)` in that order

**PROFILE Output:**
```
+----------------------------------------------------------------------+
| Operator                   | Rows | DB Hits | Cache Hits | Time    |
+----------------------------------------------------------------------+
| ProduceResults             |    1 |       0 |          0 | 0.015ms |
| +Projection                |    1 |       0 |          0 | 0.008ms |
| |                          |      |         |            |         |
| +NodeIndexSeek             |    1 |       2 |          2 | 0.421ms |
+----------------------------------------------------------------------+

Total DB Hits: 2
Execution Time: 0.444ms
```

**Analysis:**

✅ **NodeIndexSeek:** Using composite index (type, name)
- **DB hits:** 2 (index seek + node retrieval)
- **Rows:** 1 (exact match found)
- **Time:** 0.421ms

✅ **No Sort Operation:** Query ordering matches index order
- **Why:** Index stores data pre-sorted by (type, name)
- **Benefit:** Planner skips expensive sort operation
- **Savings:** ~10-50ms for larger result sets

**Performance:** ~2,252 queries/second (0.444ms per query)

**Composite Index Benefit:** **455x faster** than no index (based on Max De Marzi benchmark)

---

### Example 5: Composite Index Query (Wrong Order)

**Query:**
```cypher
PROFILE
MATCH (e:Entity {type: 'Person', name: 'John Doe'})
RETURN e
ORDER BY e.name, e.type;  // ❌ Wrong order!
```

**PROFILE Output:**
```
+----------------------------------------------------------------------+
| Operator                   | Rows | DB Hits | Cache Hits | Time    |
+----------------------------------------------------------------------+
| ProduceResults             |    1 |       0 |          0 | 0.018ms |
| +Projection                |    1 |       0 |          0 | 0.012ms |
| |                          |      |         |            |         |
| +Sort                      |    1 |       0 |          0 | 12.347ms|
| |                          |      |         |            |         |
| +NodeIndexSeek             |    1 |       2 |          2 | 0.458ms |
+----------------------------------------------------------------------+

Total DB Hits: 2
Execution Time: 12.835ms
```

**Analysis:**

⚠️ **Sort Operation Added:** Ordering doesn't match index
- **Why:** ORDER BY (name, type) ≠ index order (type, name)
- **Cost:** 12.347ms sort operation
- **Impact:** 28x slower than aligned query

❌ **Index Still Used for Lookup:** But benefit reduced
- **DB hits:** 2 (same as aligned version)
- **But:** Added sort overhead negates most benefit

**Fix:** Rewrite query to match index order:
```cypher
MATCH (e:Entity {type: 'Person', name: 'John Doe'})
RETURN e
ORDER BY e.type, e.name;  // ✅ Matches index order
```

---

## PROFILE-Driven Optimization Workflow

### Step 1: Baseline with EXPLAIN (Safe)

```cypher
EXPLAIN
MATCH (e:Entity {type: 'Person', name: 'John Doe'})
RETURN e;
```

**Check for:**
- ❌ NodeByLabelScan → Missing index
- ✅ NodeIndexSeek → Index is being used
- ⚠️ Filter after scan → Inefficient ordering

### Step 2: Identify Missing Indexes

```cypher
// If EXPLAIN shows NodeByLabelScan, create index
CREATE INDEX entity_type_name IF NOT EXISTS
FOR (e:Entity) ON (e.type, e.name);
```

### Step 3: Verify with PROFILE (After Index Creation)

```cypher
PROFILE
MATCH (e:Entity {type: 'Person', name: 'John Doe'})
RETURN e;
```

**Confirm:**
- ✅ NodeIndexSeek appears
- ✅ DB hits reduced significantly
- ✅ Execution time meets SLA

### Step 4: Benchmark Throughput

```python
import time

# Measure 1,000 queries
start = time.time()
for i in range(1000):
    session.run("MERGE (e:Entity {id: $id}) RETURN e", id=f"bench_{i}")
end = time.time()

throughput = 1000 / (end - start)
latency_avg = (end - start) / 1000 * 1000  # Convert to ms

print(f"Throughput: {throughput:.0f} queries/sec")
print(f"Avg Latency: {latency_avg:.2f}ms")
```

### Step 5: Iterate on Query Optimization

**Common Optimizations:**

1. **Add LIMIT early:**
```cypher
// Before: Scans all, then limits
MATCH (e:Entity)
WHERE e.confidence > 0.8
RETURN e
LIMIT 10;

// After: Limits scan scope
MATCH (e:Entity)
WHERE e.confidence > 0.8
WITH e LIMIT 10
RETURN e;
```

2. **Use Parameters for Query Plan Caching:**
```cypher
// Before: New plan for each literal value
MERGE (e:Entity {id: 'entity_123'})

// After: Cached plan reused
MERGE (e:Entity {id: $entity_id})
```

3. **Avoid Cartesian Products:**
```cypher
// Before: Cartesian product (BAD)
MATCH (e:Entity), (s:Source)
WHERE e.source_url = s.url
RETURN e, s;

// After: Direct relationship match (GOOD)
MATCH (e:Entity)-[:FROM_SOURCE]->(s:Source)
RETURN e, s;
```

---

## Interpreting Common Operators

### Seek Operators (Fast ✅)

**NodeUniqueIndexSeek:**
- **Use:** Lookup by unique constraint property
- **DB hits:** 1-5
- **Performance:** Excellent (O(log n))

**NodeIndexSeek:**
- **Use:** Lookup by indexed property
- **DB hits:** 5-20
- **Performance:** Good (O(log n))

**NodeByIdSeek:**
- **Use:** Lookup by internal node ID
- **DB hits:** 1
- **Performance:** Excellent (O(1))

### Scan Operators (Slow ⚠️❌)

**NodeByLabelScan:**
- **Use:** Scan all nodes with specific label
- **DB hits:** Proportional to node count
- **Performance:** Poor for large graphs (O(n))
- **When OK:** Small graphs (<1K nodes)

**AllNodesScan:**
- **Use:** Scan all nodes (no label filter)
- **DB hits:** Proportional to total node count
- **Performance:** Very poor (O(n))
- **When OK:** Only for database-wide aggregations

### Expansion Operators

**Expand(All):**
- **Use:** Follow relationships from bound node
- **DB hits:** Proportional to relationship count
- **Performance:** Depends on node degree

**VarLengthExpand:**
- **Use:** Variable-length path traversal
- **DB hits:** Exponential with path length
- **Performance:** Expensive for deep paths

### Filter Operators

**Filter:**
- **Use:** Apply WHERE clause predicates
- **DB hits:** 0 (in-memory operation)
- **Performance:** Fast, but wasteful if applied after full scan

---

## Performance Targets by Use Case

### Deduplication Lookup (<100ms SLA)

**Target:** <100ms per entity lookup

**Achieved with:**
- ✅ Unique constraint on lookup property
- ✅ NodeUniqueIndexSeek operator
- ✅ <10 DB hits per lookup
- ✅ High cache hit rate

**PROFILE Validation:**
```cypher
PROFILE
MATCH (e:Entity {id: 'entity_500'})
RETURN e;
// Expected: Time < 5ms, DB hits < 10
```

### Batch Merge (>100 entities/second)

**Target:** >100 entities/second

**Achieved with:**
- ✅ Batch size 100-1,000
- ✅ UNWIND pattern
- ✅ Indexed lookups
- ✅ Transaction batching

**PROFILE Validation:**
```cypher
PROFILE
UNWIND $batch AS entity  // $batch = 100 entities
MERGE (e:Entity {id: entity.id})
ON CREATE SET e.name = entity.name
RETURN count(e);
// Expected: Time < 100ms for 100 entities (1,000 eps)
```

### Concurrent Writes (3-5 writers)

**Target:** 3-5 concurrent writers without excessive deadlocks

**Achieved with:**
- ✅ Consistent lock ordering
- ✅ Retry on deadlock
- ✅ Read-committed isolation
- ✅ Batch size 500-1,000

**Monitoring:**
```cypher
// Check for blocked transactions
CALL dbms.listTransactions()
YIELD transactionId, currentQuery, status, elapsedTimeMillis
WHERE status = 'Blocked'
RETURN transactionId, currentQuery, elapsedTimeMillis;
// Expected: 0 or very few blocked transactions
```

---

## Common Performance Anti-Patterns

### 1. Full Scan + Filter (Instead of Index)

❌ **Bad:**
```cypher
PROFILE
MATCH (e:Entity)
WHERE e.type = 'Person' AND e.name = 'John Doe'
RETURN e;
// Shows: NodeByLabelScan + Filter (1000 DB hits)
```

✅ **Good:**
```cypher
CREATE INDEX entity_type_name FOR (e:Entity) ON (e.type, e.name);

PROFILE
MATCH (e:Entity {type: 'Person', name: 'John Doe'})
RETURN e;
// Shows: NodeIndexSeek (2 DB hits)
```

### 2. Cartesian Product

❌ **Bad:**
```cypher
PROFILE
MATCH (e:Entity)
MATCH (s:Source)
WHERE e.source_url = s.url
RETURN e, s;
// Shows: Cartesian product (1000 × 500 = 500,000 rows!)
```

✅ **Good:**
```cypher
PROFILE
MATCH (e:Entity)-[:FROM_SOURCE]->(s:Source)
RETURN e, s;
// Shows: Expand from Entity (1000 rows)
```

### 3. Late Filtering

❌ **Bad:**
```cypher
PROFILE
MATCH (e:Entity)-[:RELATED_TO]->(other:Entity)
WHERE e.confidence > 0.8
RETURN e, other;
// Shows: Expand all relationships first, then filter
```

✅ **Good:**
```cypher
PROFILE
MATCH (e:Entity)
WHERE e.confidence > 0.8
WITH e
MATCH (e)-[:RELATED_TO]->(other:Entity)
RETURN e, other;
// Shows: Filter before expansion
```

---

## Summary

**Key Metrics:**
- **DB Hits:** Lower is better, watch for spikes
- **Rows:** Minimize row cardinality, filter early
- **Cache Hits:** High hit rate indicates proper memory sizing
- **Time:** Validate against SLA requirements

**Optimization Workflow:**
1. EXPLAIN to identify query plan
2. Create indexes for scanned properties
3. PROFILE to validate improvement
4. Benchmark throughput
5. Monitor in production

**Performance Targets:**
- Deduplication: <100ms (NodeUniqueIndexSeek, <10 DB hits)
- Batch merge: >100 eps (UNWIND + indexes, 1000 batch size)
- Concurrent writes: 3-5 writers (<1% deadlock rate)
