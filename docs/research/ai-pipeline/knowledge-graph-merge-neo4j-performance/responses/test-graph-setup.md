# Neo4j Test Graph Setup Documentation

**Purpose:** Create representative test graphs for benchmarking Neo4j merge performance
**Target Scales:** 1K, 10K, and 100K entity graphs
**Schema:** Knowledge graph enrichment pattern (entities, relationships, sources)

---

## Graph Schema

### Node Types

```cypher
// Primary entity node
(:Entity {
  id: String,           // Unique identifier
  type: String,         // Entity type (Person, Organization, Concept, etc.)
  name: String,         // Human-readable name
  source: String,       // Where this entity came from
  confidence: Float,    // Confidence score (0.0-1.0)
  created_at: DateTime, // Creation timestamp
  updated_at: DateTime  // Last update timestamp (optional)
})

// Source document node
(:Source {
  url: String,          // Unique URL identifier
  title: String,        // Document title
  retrieved_at: DateTime // When document was fetched
})
```

### Relationship Types

```cypher
// Entity to entity relationships
(:Entity)-[:RELATED_TO {
  type: String,         // Relationship type
  confidence: Float,    // Relationship confidence
  evidence: String      // Supporting evidence text
}]->(:Entity)

// Entity to source provenance
(:Entity)-[:FROM_SOURCE]->(:Source)
```

---

## Test Graph Configurations

### 1K Node Test Graph (Representative Small-Scale)

**Purpose:** Fast iteration, query optimization testing, index verification
**Graph Composition:**
- 1,000 Entity nodes
- 50 Source nodes
- 1,000 Entity→Source relationships
- 500 Entity→Entity relationships

**Setup Time:** ~2 seconds
**Memory Footprint:** ~5MB data + ~1MB indexes

**Setup Script:**
```cypher
// Step 1: Create constraints and indexes
CREATE CONSTRAINT entity_id_unique IF NOT EXISTS
FOR (e:Entity) REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT source_url_unique IF NOT EXISTS
FOR (s:Source) REQUIRE s.url IS UNIQUE;

CREATE INDEX entity_type_name IF NOT EXISTS
FOR (e:Entity) ON (e.type, e.name);

CREATE INDEX entity_source IF NOT EXISTS
FOR (e:Entity) ON (e.source);

// Step 2: Create source nodes
UNWIND range(1, 50) AS i
CREATE (s:Source {
  url: 'https://example.com/source/' + toString(i),
  title: 'Test Source Document ' + toString(i),
  retrieved_at: datetime()
});

// Step 3: Create entity nodes
UNWIND range(1, 1000) AS i
CREATE (e:Entity {
  id: 'entity_' + toString(i),
  type: CASE i % 5
    WHEN 0 THEN 'Person'
    WHEN 1 THEN 'Organization'
    WHEN 2 THEN 'Concept'
    WHEN 3 THEN 'Technology'
    ELSE 'Event'
  END,
  name: 'Test Entity ' + toString(i),
  source: 'test_generation_1k',
  confidence: 0.5 + (rand() * 0.5),  // Random 0.5-1.0
  created_at: datetime()
});

// Step 4: Create Entity→Source relationships
MATCH (e:Entity)
WHERE e.id STARTS WITH 'entity_'
WITH e, toInteger((e.id - 'entity_') % 50) + 1 AS source_num
MATCH (s:Source {url: 'https://example.com/source/' + toString(source_num)})
CREATE (e)-[:FROM_SOURCE]->(s);

// Step 5: Create Entity→Entity relationships (500 random relationships)
MATCH (e1:Entity)
WHERE toInteger(substring(e1.id, 7)) <= 500
WITH e1, toInteger(substring(e1.id, 7)) + toInteger(rand() * 100) + 1 AS target_num
MATCH (e2:Entity {id: 'entity_' + toString(target_num)})
WHERE e1 <> e2
CREATE (e1)-[:RELATED_TO {
  type: 'associated_with',
  confidence: 0.7 + (rand() * 0.3),
  evidence: 'Test relationship evidence'
}]->(e2);
```

**Verification Queries:**
```cypher
// Count nodes
MATCH (e:Entity) RETURN count(e) AS entity_count;
// Expected: 1000

MATCH (s:Source) RETURN count(s) AS source_count;
// Expected: 50

// Count relationships
MATCH (e:Entity)-[:FROM_SOURCE]->(s:Source) RETURN count(*) AS provenance_relationships;
// Expected: 1000

MATCH (e1:Entity)-[:RELATED_TO]->(e2:Entity) RETURN count(*) AS entity_relationships;
// Expected: ~500

// Verify indexes are online
SHOW INDEXES YIELD name, state, type
WHERE state = 'ONLINE'
RETURN name, type;
// Expected: 4 indexes (2 constraints + 2 indexes)

// Test index performance
PROFILE
MATCH (e:Entity {id: 'entity_500'})
RETURN e;
// Should show NodeUniqueIndexSeek, db hits < 10
```

---

### 10K Node Test Graph (Medium-Scale Benchmark)

**Purpose:** Performance benchmarking, concurrent write testing, memory profiling
**Graph Composition:**
- 10,000 Entity nodes
- 500 Source nodes
- 10,000 Entity→Source relationships
- 5,000 Entity→Entity relationships

**Setup Time:** ~20 seconds
**Memory Footprint:** ~50MB data + ~10MB indexes

**Setup Script:**
```cypher
// Step 1: Create constraints and indexes (same as 1K)
CREATE CONSTRAINT entity_id_unique IF NOT EXISTS
FOR (e:Entity) REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT source_url_unique IF NOT EXISTS
FOR (s:Source) REQUIRE s.url IS UNIQUE;

CREATE INDEX entity_type_name IF NOT EXISTS
FOR (e:Entity) ON (e.type, e.name);

CREATE INDEX entity_source IF NOT EXISTS
FOR (e:Entity) ON (e.source);

// Step 2: Create source nodes
UNWIND range(1, 500) AS i
CREATE (s:Source {
  url: 'https://example.com/source/' + toString(i),
  title: 'Test Source Document ' + toString(i),
  retrieved_at: datetime()
});

// Step 3: Create entity nodes (use batching for 10K)
// Batch 1: Entities 1-5000
UNWIND range(1, 5000) AS i
CREATE (e:Entity {
  id: 'entity_' + toString(i),
  type: CASE i % 5
    WHEN 0 THEN 'Person'
    WHEN 1 THEN 'Organization'
    WHEN 2 THEN 'Concept'
    WHEN 3 THEN 'Technology'
    ELSE 'Event'
  END,
  name: 'Test Entity ' + toString(i),
  source: 'test_generation_10k',
  confidence: 0.5 + (rand() * 0.5),
  created_at: datetime()
});

// Batch 2: Entities 5001-10000
UNWIND range(5001, 10000) AS i
CREATE (e:Entity {
  id: 'entity_' + toString(i),
  type: CASE i % 5
    WHEN 0 THEN 'Person'
    WHEN 1 THEN 'Organization'
    WHEN 2 THEN 'Concept'
    WHEN 3 THEN 'Technology'
    ELSE 'Event'
  END,
  name: 'Test Entity ' + toString(i),
  source: 'test_generation_10k',
  confidence: 0.5 + (rand() * 0.5),
  created_at: datetime()
});

// Step 4: Create Entity→Source relationships (batched)
CALL {
  MATCH (e:Entity)
  WHERE e.source = 'test_generation_10k'
  WITH e, toInteger(rand() * 499) + 1 AS source_num
  MATCH (s:Source {url: 'https://example.com/source/' + toString(source_num)})
  CREATE (e)-[:FROM_SOURCE]->(s)
} IN TRANSACTIONS OF 1000 ROWS;

// Step 5: Create Entity→Entity relationships (batched)
CALL {
  MATCH (e1:Entity)
  WHERE toInteger(substring(e1.id, 7)) <= 5000
  WITH e1, toInteger(substring(e1.id, 7)) + toInteger(rand() * 1000) + 1 AS target_num
  MATCH (e2:Entity {id: 'entity_' + toString(target_num)})
  WHERE e1 <> e2
  CREATE (e1)-[:RELATED_TO {
    type: 'associated_with',
    confidence: 0.7 + (rand() * 0.3),
    evidence: 'Test relationship evidence'
  }]->(e2)
} IN TRANSACTIONS OF 1000 ROWS;
```

**Verification Queries:**
```cypher
// Count nodes
MATCH (e:Entity) RETURN count(e) AS entity_count;
// Expected: 10000

MATCH (s:Source) RETURN count(s) AS source_count;
// Expected: 500

// Count relationships
MATCH ()-[:FROM_SOURCE]->() RETURN count(*) AS provenance_relationships;
// Expected: 10000

MATCH ()-[:RELATED_TO]->() RETURN count(*) AS entity_relationships;
// Expected: ~5000

// Memory usage check
CALL dbms.queryJmx("org.neo4j:instance=kernel#0,name=Store sizes")
YIELD attributes
RETURN attributes;
```

---

### 100K Node Test Graph (Target-Scale Performance)

**Purpose:** Production-scale testing, scalability validation, throughput benchmarking
**Graph Composition:**
- 100,000 Entity nodes
- 5,000 Source nodes
- 100,000 Entity→Source relationships
- 50,000 Entity→Entity relationships

**Setup Time:** ~3-5 minutes (using APOC batching)
**Memory Footprint:** ~500MB data + ~100MB indexes

**Setup Script (requires APOC):**
```cypher
// Step 1: Create constraints and indexes
CREATE CONSTRAINT entity_id_unique IF NOT EXISTS
FOR (e:Entity) REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT source_url_unique IF NOT EXISTS
FOR (s:Source) REQUIRE s.url IS UNIQUE;

CREATE INDEX entity_type_name IF NOT EXISTS
FOR (e:Entity) ON (e.type, e.name);

CREATE INDEX entity_source IF NOT EXISTS
FOR (e:Entity) ON (e.source);

// Step 2: Create source nodes
CALL apoc.periodic.iterate(
  "UNWIND range(1, 5000) AS i RETURN i",
  "CREATE (s:Source {
    url: 'https://example.com/source/' + toString(i),
    title: 'Test Source Document ' + toString(i),
    retrieved_at: datetime()
  })",
  {batchSize: 1000}
);

// Step 3: Create entity nodes (100K in batches)
CALL apoc.periodic.iterate(
  "UNWIND range(1, 100000) AS i RETURN i",
  "CREATE (e:Entity {
    id: 'entity_' + toString(i),
    type: CASE i % 5
      WHEN 0 THEN 'Person'
      WHEN 1 THEN 'Organization'
      WHEN 2 THEN 'Concept'
      WHEN 3 THEN 'Technology'
      ELSE 'Event'
    END,
    name: 'Test Entity ' + toString(i),
    source: 'test_generation_100k',
    confidence: 0.5 + (rand() * 0.5),
    created_at: datetime()
  })",
  {batchSize: 2000, parallel: false}
);

// Step 4: Create Entity→Source relationships
CALL apoc.periodic.iterate(
  "MATCH (e:Entity) WHERE e.source = 'test_generation_100k' RETURN e",
  "WITH e, toInteger(rand() * 4999) + 1 AS source_num
   MATCH (s:Source {url: 'https://example.com/source/' + toString(source_num)})
   CREATE (e)-[:FROM_SOURCE]->(s)",
  {batchSize: 1000, parallel: false}
);

// Step 5: Create Entity→Entity relationships
CALL apoc.periodic.iterate(
  "MATCH (e1:Entity)
   WHERE toInteger(substring(e1.id, 7)) <= 50000
   RETURN e1",
  "WITH e1, toInteger(substring(e1.id, 7)) + toInteger(rand() * 10000) + 1 AS target_num
   MATCH (e2:Entity {id: 'entity_' + toString(target_num)})
   WHERE e1 <> e2
   CREATE (e1)-[:RELATED_TO {
     type: 'associated_with',
     confidence: 0.7 + (rand() * 0.3),
     evidence: 'Test relationship evidence'
   }]->(e2)",
  {batchSize: 1000, parallel: false}
);
```

**Alternative Setup (without APOC):**
```cypher
// Use CALL IN TRANSACTIONS (Neo4j 5.x+)
CALL {
  UNWIND range(1, 100000) AS i
  CREATE (e:Entity {
    id: 'entity_' + toString(i),
    type: CASE i % 5
      WHEN 0 THEN 'Person'
      WHEN 1 THEN 'Organization'
      WHEN 2 THEN 'Concept'
      WHEN 3 THEN 'Technology'
      ELSE 'Event'
    END,
    name: 'Test Entity ' + toString(i),
    source: 'test_generation_100k',
    confidence: 0.5 + (rand() * 0.5),
    created_at: datetime()
  })
} IN TRANSACTIONS OF 2000 ROWS;
```

---

## Sample Merge Data

### Entity Merge Test Data (JSON format)

**File:** `sample-merge-data.json`

```json
[
  {
    "id": "entity_new_1",
    "type": "Person",
    "name": "Alice Johnson",
    "source": "web_research_batch_1",
    "confidence": 0.92
  },
  {
    "id": "entity_500",
    "type": "Organization",
    "name": "Updated Organization Name",
    "source": "web_research_batch_1",
    "confidence": 0.88
  },
  {
    "id": "entity_new_2",
    "type": "Technology",
    "name": "GraphRAG",
    "source": "academic_paper_extraction",
    "confidence": 0.95
  }
]
```

### Merge Query for Test Data

```cypher
// Load merge data and execute MERGE
WITH [
  {id: "entity_new_1", type: "Person", name: "Alice Johnson", source: "web_research_batch_1", confidence: 0.92},
  {id: "entity_500", type: "Organization", name: "Updated Organization Name", source: "web_research_batch_1", confidence: 0.88},
  {id: "entity_new_2", type: "Technology", name: "GraphRAG", source: "academic_paper_extraction", confidence: 0.95}
] AS merge_batch

UNWIND merge_batch AS entity_data
MERGE (e:Entity {id: entity_data.id})
ON CREATE SET
  e.type = entity_data.type,
  e.name = entity_data.name,
  e.source = entity_data.source,
  e.confidence = entity_data.confidence,
  e.created_at = datetime()
ON MATCH SET
  e.confidence = CASE
    WHEN entity_data.confidence > e.confidence
    THEN entity_data.confidence
    ELSE e.confidence
  END,
  e.updated_at = datetime()
RETURN count(e) AS entities_merged;
```

**Expected Result:**
- 2 entities created (entity_new_1, entity_new_2)
- 1 entity updated (entity_500)
- Total merged: 3

---

## Verification Queries

### Performance Verification

```cypher
// 1. Verify index usage on single lookup
PROFILE
MATCH (e:Entity {id: 'entity_500'})
RETURN e;
// Expected: NodeUniqueIndexSeek, db hits < 10, time < 5ms

// 2. Verify composite index usage
PROFILE
MATCH (e:Entity {type: 'Person', name: 'Test Entity 100'})
RETURN e;
// Expected: NodeIndexSeek, db hits < 50

// 3. Verify deduplication performance (no duplicates created)
MATCH (e:Entity)
WITH e.id AS entity_id, count(e) AS occurrences
WHERE occurrences > 1
RETURN entity_id, occurrences;
// Expected: 0 rows (no duplicates)

// 4. Verify relationship integrity
MATCH ()-[r:FROM_SOURCE]->()
WHERE NOT EXISTS((startNode(r))) OR NOT EXISTS((endNode(r)))
RETURN count(r) AS orphaned_relationships;
// Expected: 0

// 5. Test merge throughput (single entity)
// Run 100 times and measure average time
PROFILE
MERGE (e:Entity {id: 'bench_entity_' + toString(toInteger(rand() * 10000))})
ON CREATE SET e.name = 'Benchmark Entity'
RETURN e;
```

### Data Quality Verification

```cypher
// 1. Entity count by type
MATCH (e:Entity)
RETURN e.type AS entity_type, count(e) AS count
ORDER BY count DESC;

// 2. Confidence distribution
MATCH (e:Entity)
RETURN
  'High (0.8-1.0)' AS confidence_range,
  count(e) AS count
WHERE e.confidence >= 0.8
UNION
MATCH (e:Entity)
RETURN
  'Medium (0.6-0.8)' AS confidence_range,
  count(e) AS count
WHERE e.confidence >= 0.6 AND e.confidence < 0.8
UNION
MATCH (e:Entity)
RETURN
  'Low (0.0-0.6)' AS confidence_range,
  count(e) AS count
WHERE e.confidence < 0.6
ORDER BY confidence_range;

// 3. Source coverage (entities per source)
MATCH (e:Entity)-[:FROM_SOURCE]->(s:Source)
RETURN s.url AS source, count(e) AS entity_count
ORDER BY entity_count DESC
LIMIT 10;

// 4. Relationship density
MATCH (e:Entity)
OPTIONAL MATCH (e)-[:RELATED_TO]->(other)
RETURN
  e.id,
  count(other) AS relationship_count
ORDER BY relationship_count DESC
LIMIT 10;
```

---

## Scaling to Larger Graphs

### Linear Scaling Pattern

The test graph setup follows a **linear scaling pattern**:

| Graph Size | Entities | Sources | Relationships | Setup Time | Memory |
|------------|----------|---------|---------------|------------|--------|
| 1K | 1,000 | 50 | 1,500 | ~2 sec | ~5 MB |
| 10K | 10,000 | 500 | 15,000 | ~20 sec | ~50 MB |
| 100K | 100,000 | 5,000 | 150,000 | ~3 min | ~500 MB |
| 1M | 1,000,000 | 50,000 | 1,500,000 | ~30 min | ~5 GB |

### Batch Size Recommendations by Graph Size

- **1K graph:** Single transaction OK (fast)
- **10K graph:** Batch size 1,000-2,000
- **100K graph:** Batch size 2,000-5,000
- **1M+ graph:** Batch size 5,000-10,000 + parallel processing

### Memory Requirements by Graph Size

- **1K graph:** 512 MB heap + 256 MB page cache
- **10K graph:** 2 GB heap + 1 GB page cache
- **100K graph:** 4 GB heap + 3 GB page cache
- **1M graph:** 8-16 GB heap + 8-16 GB page cache

---

## Cleanup Queries

### Remove Test Graphs

```cypher
// Delete 1K test graph
MATCH (e:Entity)
WHERE e.source = 'test_generation_1k'
DETACH DELETE e;

MATCH (s:Source)
WHERE s.url STARTS WITH 'https://example.com/source/'
  AND toInteger(split(s.url, '/')[4]) <= 50
DELETE s;

// Delete 10K test graph
MATCH (e:Entity)
WHERE e.source = 'test_generation_10k'
DETACH DELETE e;

MATCH (s:Source)
WHERE s.url STARTS WITH 'https://example.com/source/'
  AND toInteger(split(s.url, '/')[4]) <= 500
DELETE s;

// Delete 100K test graph
CALL apoc.periodic.iterate(
  "MATCH (e:Entity) WHERE e.source = 'test_generation_100k' RETURN e",
  "DETACH DELETE e",
  {batchSize: 1000}
);

// Verify cleanup
MATCH (e:Entity) RETURN count(e) AS remaining_entities;
MATCH (s:Source) RETURN count(s) AS remaining_sources;
```

---

## Test Graph Characteristics

### Entity Type Distribution (All Test Graphs)

- **Person:** 20% of entities
- **Organization:** 20% of entities
- **Concept:** 20% of entities
- **Technology:** 20% of entities
- **Event:** 20% of entities

### Relationship Patterns

- **Entity→Source:** 1:1 (every entity has 1 source)
- **Entity→Entity:** ~50% of entities have outgoing relationships
- **Relationship Confidence:** Random 0.7-1.0 (high confidence)

### Confidence Score Distribution

- **Range:** 0.5-1.0
- **Mean:** ~0.75
- **Distribution:** Uniform random

---

## Summary

This test graph setup provides **representative graphs at 3 scales** (1K, 10K, 100K) that mirror the knowledge graph enrichment use case. The setup scripts are **reproducible, scalable, and include verification queries** to ensure data quality and performance validation.

**Key Features:**
- ✅ Unique constraints on entity IDs and source URLs
- ✅ Composite indexes for efficient deduplication
- ✅ Provenance tracking (entity→source relationships)
- ✅ Linear scaling pattern from 1K to 1M+ nodes
- ✅ Verification queries for correctness and performance
- ✅ Cleanup scripts for test graph removal
