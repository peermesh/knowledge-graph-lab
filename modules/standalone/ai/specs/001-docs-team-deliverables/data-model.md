# Data Model: AI Development Module

**Feature**: AI Development Module  
**Date**: 2025-10-20  
**Database**: PostgreSQL 15+ with JSONB support  
**Vector Store**: Qdrant (768-dimensional embeddings)

## Overview

The AI module data model consists of 6 primary tables supporting entity extraction, relationship mapping, knowledge graph construction, and quality monitoring. The design emphasizes data integrity, query performance, and scalability to 1M+ entities and 5M+ relationships.

---

## Table: extracted_entities

**Purpose**: Store extracted entities from documents with metadata and confidence scores

### Schema

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier (auto-generated) |
| text | VARCHAR(500) | NOT NULL | The entity text value |
| entity_type | VARCHAR(50) | NOT NULL | Type: organization, person, funding_amount, date, location |
| confidence | DECIMAL(3,2) | NOT NULL, CHECK (0.00-1.00) | Confidence score 0.00-1.00 |
| source_document_id | UUID | NOT NULL, FK → documents(id) | Reference to source document |
| extraction_method | VARCHAR(50) | NOT NULL | Method: ner_model, rule_based, hybrid |
| positions | JSONB | NOT NULL | Array of [start_char, end_char] positions in source |
| metadata | JSONB | | Additional properties (aliases, description, founded_date) |
| vector_embedding | VECTOR(768) | NOT NULL | 768-dimensional embedding for similarity search |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Entity creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

### Indexes
```sql
CREATE INDEX idx_entities_type ON extracted_entities(entity_type);
CREATE INDEX idx_entities_confidence ON extracted_entities(confidence);
CREATE INDEX idx_entities_source ON extracted_entities(source_document_id);
CREATE INDEX idx_entities_created ON extracted_entities(created_at);
CREATE INDEX idx_entities_text_gin ON extracted_entities USING gin(to_tsvector('english', text));
```

### Validation Rules
- Confidence must be between 0.00 and 1.00
- Entity_type must be in: organization, person, funding_amount, date, location
- Positions must be valid JSON array of [start, end] tuples
- Vector_embedding must be exactly 768 dimensions

### Example Record
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "text": "OpenAI",
  "entity_type": "organization",
  "confidence": 0.95,
  "source_document_id": "660e8400-e29b-41d4-a716-446655440001",
  "extraction_method": "ner_model",
  "positions": [[0, 6], [157, 163]],
  "metadata": {
    "aliases": ["Open AI"],
    "description": "AI research company",
    "founded_date": "2015-12-11"
  },
  "vector_embedding": [0.123, -0.456, ...],  // 768 dimensions
  "created_at": "2025-10-20T14:30:00Z",
  "updated_at": "2025-10-20T14:30:00Z"
}
```

---

## Table: entity_relationships

**Purpose**: Store relationships between extracted entities with evidence and confidence

### Schema

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier (auto-generated) |
| source_entity_id | UUID | NOT NULL, FK → extracted_entities(id) | Entity initiating relationship |
| target_entity_id | UUID | NOT NULL, FK → extracted_entities(id) | Entity receiving relationship |
| relationship_type | VARCHAR(50) | NOT NULL | Type: fund, partner, acquire, compete, collaborate, mention |
| confidence | DECIMAL(3,2) | NOT NULL, CHECK (0.00-1.00) | Confidence score 0.00-1.00 |
| strength | DECIMAL(3,2) | CHECK (0.00-1.00) | Relationship strength 0.00-1.00 (optional) |
| evidence | TEXT | | Supporting text from source document |
| temporal_context | JSONB | | Date ranges, duration information |
| metadata | JSONB | | Additional properties (amount, date, source) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Relationship creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

### Indexes
```sql
CREATE INDEX idx_relationships_source ON entity_relationships(source_entity_id);
CREATE INDEX idx_relationships_target ON entity_relationships(target_entity_id);
CREATE INDEX idx_relationships_type ON entity_relationships(relationship_type);
CREATE INDEX idx_relationships_confidence ON entity_relationships(confidence);
CREATE INDEX idx_relationships_created ON entity_relationships(created_at);
```

### Validation Rules
- Confidence must be between 0.00 and 1.00
- Strength must be between 0.00 and 1.00 (if provided)
- Source_entity_id != target_entity_id (no self-relationships)
- Relationship_type must be in: fund, partner, acquire, compete, collaborate, mention

### Example Record
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "source_entity_id": "880e8400-e29b-41d4-a716-446655440001",  // Microsoft
  "target_entity_id": "550e8400-e29b-41d4-a716-446655440000",  // OpenAI
  "relationship_type": "fund",
  "confidence": 0.87,
  "strength": 0.92,
  "evidence": "Microsoft invested $10 billion in OpenAI",
  "temporal_context": {
    "start_date": "2023-01-23",
    "duration": "multi-year partnership"
  },
  "metadata": {
    "amount": "$10B",
    "date": "2023-01-23",
    "source": "https://news.microsoft.com/..."
  },
  "created_at": "2025-10-20T14:30:00Z",
  "updated_at": "2025-10-20T14:30:00Z"
}
```

---

## Table: knowledge_graph_nodes

**Purpose**: Store knowledge graph nodes with entity references and embeddings

### Schema

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier (auto-generated) |
| entity_id | UUID | NOT NULL, UNIQUE, FK → extracted_entities(id) | Reference to extracted entity |
| node_type | VARCHAR(50) | NOT NULL | Type: entity, concept, event |
| properties | JSONB | NOT NULL | Node properties (name, aliases, metadata) |
| vector_embedding | VECTOR(768) | NOT NULL | 768-dimensional embedding for similarity |
| degree | INTEGER | NOT NULL, DEFAULT 0 | Number of connections to other nodes |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Node creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

### Indexes
```sql
CREATE UNIQUE INDEX idx_nodes_entity ON knowledge_graph_nodes(entity_id);
CREATE INDEX idx_nodes_type ON knowledge_graph_nodes(node_type);
CREATE INDEX idx_nodes_degree ON knowledge_graph_nodes(degree);
CREATE INDEX idx_nodes_created ON knowledge_graph_nodes(created_at);
```

### Validation Rules
- Unique entity_id per node (one-to-one relationship)
- Node_type must be in: entity, concept, event
- Degree must be non-negative integer

### Example Record
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440000",
  "entity_id": "550e8400-e29b-41d4-a716-446655440000",
  "node_type": "entity",
  "properties": {
    "name": "OpenAI",
    "aliases": ["Open AI"],
    "entity_type": "organization",
    "description": "AI research company"
  },
  "vector_embedding": [0.123, -0.456, ...],  // 768 dimensions
  "degree": 15,
  "created_at": "2025-10-20T14:30:00Z",
  "updated_at": "2025-10-20T14:30:00Z"
}
```

---

## Table: knowledge_graph_edges

**Purpose**: Store knowledge graph edges representing entity relationships

### Schema

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier (auto-generated) |
| source_node_id | UUID | NOT NULL, FK → knowledge_graph_nodes(id) | Source node in relationship |
| target_node_id | UUID | NOT NULL, FK → knowledge_graph_nodes(id) | Target node in relationship |
| relationship_type | VARCHAR(50) | NOT NULL | Type: fund, partner, acquire, compete, collaborate |
| properties | JSONB | | Edge properties (weight, direction, metadata) |
| confidence | DECIMAL(3,2) | NOT NULL, CHECK (0.00-1.00) | Confidence score 0.00-1.00 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Edge creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

### Indexes
```sql
CREATE INDEX idx_edges_source ON knowledge_graph_edges(source_node_id);
CREATE INDEX idx_edges_target ON knowledge_graph_edges(target_node_id);
CREATE INDEX idx_edges_type ON knowledge_graph_edges(relationship_type);
CREATE INDEX idx_edges_confidence ON knowledge_graph_edges(confidence);
CREATE INDEX idx_edges_created ON knowledge_graph_edges(created_at);
```

### Validation Rules
- Confidence must be between 0.00 and 1.00
- Source_node_id != target_node_id (no self-loops)
- Relationship_type must be in: fund, partner, acquire, compete, collaborate

### Example Record
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440000",
  "source_node_id": "bb0e8400-e29b-41d4-a716-446655440001",
  "target_node_id": "990e8400-e29b-41d4-a716-446655440000",
  "relationship_type": "fund",
  "properties": {
    "weight": 0.92,
    "direction": "directed",
    "amount": "$10B",
    "date": "2023-01-23"
  },
  "confidence": 0.87,
  "created_at": "2025-10-20T14:30:00Z",
  "updated_at": "2025-10-20T14:30:00Z"
}
```

---

## Table: document_processing_jobs

**Purpose**: Track document processing lifecycle and results

### Schema

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier (auto-generated) |
| document_id | UUID | NOT NULL, FK → documents(id) | Reference to source document |
| status | VARCHAR(20) | NOT NULL | Status: pending, processing, completed, failed |
| priority | VARCHAR(10) | NOT NULL, DEFAULT 'normal' | Priority: high, normal, low |
| extraction_config | JSONB | | Configuration for entity types and processing rules |
| entities_extracted | INTEGER | DEFAULT 0 | Count of entities extracted |
| relationships_found | INTEGER | DEFAULT 0 | Count of relationships identified |
| processing_time_seconds | DECIMAL(8,2) | | Total processing time |
| error_message | TEXT | | Error details if processing failed |
| retry_count | INTEGER | NOT NULL, DEFAULT 0 | Number of retry attempts |
| started_at | TIMESTAMP | | When processing started |
| completed_at | TIMESTAMP | | When processing completed |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Job creation timestamp |

### Indexes
```sql
CREATE INDEX idx_jobs_status ON document_processing_jobs(status);
CREATE INDEX idx_jobs_priority ON document_processing_jobs(priority);
CREATE INDEX idx_jobs_document ON document_processing_jobs(document_id);
CREATE INDEX idx_jobs_created ON document_processing_jobs(created_at);
```

### Validation Rules
- Status must be in: pending, processing, completed, failed
- Priority must be in: high, normal, low
- Retry_count >= 0

### Example Record
```json
{
  "id": "cc0e8400-e29b-41d4-a716-446655440000",
  "document_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "completed",
  "priority": "normal",
  "extraction_config": {
    "entity_types": ["organization", "person", "funding_amount"],
    "confidence_threshold": 0.7,
    "language": "en"
  },
  "entities_extracted": 12,
  "relationships_found": 5,
  "processing_time_seconds": 45.23,
  "error_message": null,
  "retry_count": 0,
  "started_at": "2025-10-20T14:30:00Z",
  "completed_at": "2025-10-20T14:30:45Z",
  "created_at": "2025-10-20T14:29:55Z"
}
```

---

## Table: processing_quality_metrics

**Purpose**: Store quality metrics and performance data for monitoring

### Schema

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier (auto-generated) |
| job_id | UUID | NOT NULL, FK → document_processing_jobs(id) | Reference to processing job |
| metric_type | VARCHAR(50) | NOT NULL | Type: accuracy, precision, recall, latency, cost |
| entity_type | VARCHAR(50) | | Entity type for type-specific metrics |
| value | DECIMAL(10,4) | NOT NULL | Metric value (percentage, seconds, dollars) |
| sample_size | INTEGER | | Number of samples used for calculation |
| confidence_interval | DECIMAL(5,4) | | Confidence interval for statistical metrics |
| calculated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | When metric was calculated |
| metadata | JSONB | | Additional metric context |

### Indexes
```sql
CREATE INDEX idx_metrics_job ON processing_quality_metrics(job_id);
CREATE INDEX idx_metrics_type ON processing_quality_metrics(metric_type);
CREATE INDEX idx_metrics_entity_type ON processing_quality_metrics(entity_type);
CREATE INDEX idx_metrics_calculated ON processing_quality_metrics(calculated_at);
```

### Validation Rules
- Metric_type must be in: accuracy, precision, recall, latency, cost
- Value must be appropriate for metric_type (percentages 0-100, latency > 0, cost >= 0)
- Sample_size > 0 (if provided)

### Example Record
```json
{
  "id": "dd0e8400-e29b-41d4-a716-446655440000",
  "job_id": "cc0e8400-e29b-41d4-a716-446655440000",
  "metric_type": "precision",
  "entity_type": "organization",
  "value": 0.8945,
  "sample_size": 12,
  "confidence_interval": 0.0234,
  "calculated_at": "2025-10-20T14:30:45Z",
  "metadata": {
    "true_positives": 11,
    "false_positives": 1,
    "document_type": "news_article"
  }
}
```

---

## Relationships

### Entity Data Flow
```
documents (Backend Module)
  ↓
document_processing_jobs
  ↓
extracted_entities ←→ entity_relationships
  ↓
knowledge_graph_nodes ←→ knowledge_graph_edges
```

### Foreign Key Relationships
- `extracted_entities.source_document_id` → `documents.id` (Backend module)
- `entity_relationships.source_entity_id` → `extracted_entities.id`
- `entity_relationships.target_entity_id` → `extracted_entities.id`
- `knowledge_graph_nodes.entity_id` → `extracted_entities.id` (1:1)
- `knowledge_graph_edges.source_node_id` → `knowledge_graph_nodes.id`
- `knowledge_graph_edges.target_node_id` → `knowledge_graph_nodes.id`
- `document_processing_jobs.document_id` → `documents.id` (Backend module)
- `processing_quality_metrics.job_id` → `document_processing_jobs.id`

---

## State Transitions

### Document Processing Job States
```
pending → processing → completed
                     → failed (with retry) → pending (up to 3 retries)
                                          → failed (final)
```

### Entity Lifecycle
```
[extracted] → [validated] → [deduplicated] → [graph_node_created]
```

---

## Qdrant Vector Collections

### Collection: entity_embeddings

**Purpose**: Store entity vector embeddings for similarity search

**Configuration**:
- Dimensions: 768
- Distance metric: Cosine similarity
- HNSW parameters: M=16, ef_construct=200
- Quantization: Scalar quantization enabled

**Payload Schema**:
```json
{
  "entity_id": "550e8400-e29b-41d4-a716-446655440000",
  "text": "OpenAI",
  "entity_type": "organization",
  "confidence": 0.95,
  "metadata": {
    "aliases": ["Open AI"],
    "description": "AI research company"
  }
}
```

---

## Database Migration Strategy

1. **Initial Schema**: Create all tables with indexes
2. **Seed Data**: Optional seed with sample entities for testing
3. **Data Integrity**: Enable foreign key constraints after initial load
4. **Performance Tuning**: Add indexes based on query patterns
5. **Partitioning**: Consider partitioning by `created_at` at 10M+ entities

---

## Backup and Recovery

- **Backup Frequency**: Daily full backups, hourly incremental
- **Retention**: 30 days for full backups, 7 days for incremental
- **Recovery Point Objective (RPO)**: 1 hour
- **Recovery Time Objective (RTO)**: 4 hours

---

**Data Model Complete**: All schemas defined and validated. Ready for contract generation.
