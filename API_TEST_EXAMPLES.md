# REST API Test Examples - AI Development Module

Complete test parameters for all API endpoints with ready-to-use JSON payloads.

---

## 🚀 Entity Extraction API

### 1. POST /ai/v1/extract-entities - Basic Extraction

**Description**: Extract entities with default settings (all types)

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "content": "Microsoft invested $10 billion in OpenAI. Sam Altman is the CEO of OpenAI, and the company is based in San Francisco.",
  "document_type": "text",
  "priority": "normal"
}
```

**Expected Result**: Extracts Microsoft, OpenAI, $10 billion, Sam Altman, San Francisco

---

### 2. POST /ai/v1/extract-entities - Custom Entity Types

**Description**: Extract specific custom entity types (showcases flexibility!)

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440001",
  "content": "React is a JavaScript library developed by Meta. It uses Virtual DOM and supports TypeScript. Developers deploy React apps on Vercel and Netlify.",
  "document_type": "text",
  "extraction_config": {
    "entity_types": ["framework", "library", "language", "company", "platform", "technology"],
    "relationship_types": ["developed_by", "uses", "supports", "deploys_on"],
    "confidence_threshold": 0.7,
    "source_type": "official"
  },
  "priority": "high"
}
```

**Expected Result**: React (library), JavaScript (language), Meta (company), Virtual DOM (technology), TypeScript (language), Vercel (platform), Netlify (platform)

---

### 3. POST /ai/v1/extract-entities - Extract ALL Types

**Description**: Let the LLM detect any entity type automatically

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440002",
  "content": "The iPhone 15 was announced at Apple Park in Cupertino on September 12, 2023. Tim Cook presented the new features including USB-C charging and improved camera capabilities.",
  "document_type": "text",
  "extraction_config": {
    "entity_types": null,
    "relationship_types": null,
    "confidence_threshold": 0.65,
    "source_type": "news_major"
  },
  "priority": "normal"
}
```

**Expected Result**: Any types detected - product, location, date, person, feature, etc.

---

### 4. POST /ai/v1/extract-entities - AI/Tech Document

**Description**: Extract from AI industry news with custom types

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440003",
  "content": "Google's DeepMind released Gemini 1.5, a multimodal AI model that can process text, images, and video. The model uses a mixture-of-experts architecture and was trained on Google's TPU v5 infrastructure. It competes with OpenAI's GPT-4 and Anthropic's Claude 3.",
  "document_type": "text",
  "extraction_config": {
    "entity_types": ["company", "product", "model", "architecture", "infrastructure", "capability"],
    "relationship_types": ["released", "competes_with", "trained_on", "uses", "processes"],
    "confidence_threshold": 0.7,
    "source_type": "news_major"
  },
  "priority": "high"
}
```

---

### 5. POST /ai/v1/extract-entities - Financial/Investment News

**Description**: Extract investment and funding information

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440004",
  "content": "Sequoia Capital led a $150 million Series B round for AI startup Anthropic. The funding values the company at $5 billion. Previous investors include Google, Spark Capital, and Salesforce Ventures. The capital will be used to expand their research team and develop Claude AI.",
  "document_type": "text",
  "extraction_config": {
    "entity_types": ["investor", "company", "funding_amount", "valuation", "funding_round", "product"],
    "relationship_types": ["led_round", "invested_in", "valued_at", "used_for", "developing"],
    "confidence_threshold": 0.75,
    "source_type": "news_major"
  },
  "priority": "high"
}
```

---

### 6. POST /ai/v1/extract-entities - Large Document (Async)

**Description**: Process large document that triggers async processing

```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440005",
  "content": "INSERT_LONG_ARTICLE_HERE (>10KB will trigger async processing automatically)",
  "document_type": "text",
  "extraction_config": {
    "entity_types": null,
    "confidence_threshold": 0.7,
    "source_type": "unknown"
  },
  "priority": "low"
}
```

**Note**: Content >10KB automatically triggers async processing. Returns job_id for status checking.

---

### 7. GET /ai/v1/jobs/{job_id} - Check Job Status

**Description**: Check the status of an async extraction job

**URL**: `GET /ai/v1/jobs/550e8400-e29b-41d4-a716-446655440005`

**No body required** - Just use the job_id from the POST response

**Response States**:
- `pending` - Job queued
- `processing` - Currently extracting
- `completed` - Done, results available
- `failed` - Error occurred

---

## 🔍 Knowledge Graph Query API

### 8. GET /ai/v1/graph/query - Query Relationships

**Description**: Query the knowledge graph for entity relationships

**Query Parameters**:
```
?entity_name=Microsoft
&relationship_type=invested_in
&min_confidence=0.7
&max_depth=2
&limit=10
```

**Full URL Example**:
```
GET /ai/v1/graph/query?entity_name=Microsoft&relationship_type=invested_in&min_confidence=0.7&max_depth=2&limit=10
```

---

### 9. GET /ai/v1/graph/query - Find All Relationships

**Description**: Get all relationships for an entity (any type)

**Query Parameters**:
```
?entity_name=OpenAI
&max_depth=3
&limit=50
```

**Expected Result**: All relationships involving OpenAI (invested_in, founded_by, competes_with, etc.)

---

### 10. GET /ai/v1/graph/query - Specific Relationship Types

**Description**: Query for specific relationship types (showcases flexibility!)

**Query Parameters**:
```
?entity_name=React
&relationship_type=uses,supports,built_with
&min_confidence=0.6
&max_depth=1
&limit=20
```

**Expected Result**: Only "uses", "supports", and "built_with" relationships for React

---

### 11. GET /ai/v1/graph/entity/{entity_id} - Get Entity Details

**Description**: Get detailed information about a specific entity

**URL**: `GET /ai/v1/graph/entity/550e8400-e29b-41d4-a716-446655440000`

**No body required** - Use entity ID from extraction results

**Expected Result**: Entity properties, relationships, confidence scores, metadata

---

### 12. GET /ai/v1/graph/similarity - Find Similar Entities

**Description**: Find entities similar to a given entity using vector search

**Query Parameters**:
```
?entity_text=React
&top_k=10
&min_similarity=0.8
```

**Expected Result**: Vue, Angular, Svelte, Next.js, etc. (similar frameworks)

---

### 13. GET /ai/v1/graph/similarity - Find Similar with Type Filter

**Description**: Find similar entities of specific types

**Query Parameters**:
```
?entity_text=OpenAI
&entity_types=company,organization
&top_k=5
&min_similarity=0.75
```

**Expected Result**: Anthropic, Google DeepMind, Mistral AI, etc.

---

## 📊 Quality Monitoring API

### 14. GET /ai/v1/quality/metrics - Get Overall Quality

**Description**: Get quality metrics for all processing

**Query Parameters**:
```
?start_date=2025-11-01
&end_date=2025-11-02
```

**Expected Result**: Accuracy, precision, recall, latency metrics

---

### 15. GET /ai/v1/quality/metrics - Entity-Specific Metrics

**Description**: Get quality metrics for specific entity types

**Query Parameters**:
```
?entity_type=company
&start_date=2025-11-01
&end_date=2025-11-02
```

**Expected Result**: Quality metrics specifically for "company" entities

---

### 16. GET /ai/v1/quality/metrics - Recent Metrics

**Description**: Get latest quality metrics (last 24 hours)

**Query Parameters**:
```
?hours=24
```

**Expected Result**: Recent processing quality data

---

## 🏥 Health Check API

### 17. GET /health - Basic Health Check

**Description**: Simple health check endpoint

**No parameters required**

**Expected Result**:
```json
{
  "status": "healthy",
  "service": "ai-module",
  "version": "1.0.0"
}
```

---

### 18. GET /ai/v1/health - Detailed Health Check

**Description**: Detailed health status with service checks

**No parameters required**

**Expected Result**:
```json
{
  "service": "AI Development Module",
  "version": "1.0.0",
  "status": "operational",
  "checks": {
    "database": "healthy",
    "vector_db": "healthy",
    "message_queue": "healthy",
    "llm_client": "ready"
  }
}
```

---

## 🎯 Test Scenarios

### Scenario 1: Tech Company Analysis

**Step 1**: Extract entities
```json
POST /ai/v1/extract-entities
{
  "document_id": "test-scenario-001",
  "content": "Meta (formerly Facebook) acquired Instagram for $1 billion in 2012. Mark Zuckerberg is the CEO. The company competes with TikTok and Snapchat.",
  "document_type": "text",
  "extraction_config": {
    "entity_types": ["company", "person", "product", "acquisition_amount"],
    "relationship_types": ["acquired", "ceo_of", "competes_with", "formerly_known_as"],
    "confidence_threshold": 0.7
  }
}
```

**Step 2**: Query relationships
```
GET /ai/v1/graph/query?entity_name=Meta&max_depth=2&limit=20
```

**Step 3**: Find similar companies
```
GET /ai/v1/graph/similarity?entity_text=Meta&entity_types=company&top_k=5
```

---

### Scenario 2: AI Model Comparison

**Step 1**: Extract AI models and capabilities
```json
POST /ai/v1/extract-entities
{
  "document_id": "test-scenario-002",
  "content": "GPT-4 by OpenAI supports multimodal inputs. Claude 3 Opus by Anthropic excels at long-context tasks. Gemini 1.5 by Google can process 1 million tokens. All three models use transformer architecture.",
  "document_type": "text",
  "extraction_config": {
    "entity_types": ["model", "company", "capability", "architecture", "metric"],
    "relationship_types": ["developed_by", "supports", "excels_at", "uses", "processes"],
    "confidence_threshold": 0.7
  }
}
```

**Step 2**: Query model capabilities
```
GET /ai/v1/graph/query?entity_name=GPT-4&relationship_type=supports,uses&max_depth=1
```

---

### Scenario 3: Investment Tracking

**Step 1**: Extract funding information
```json
POST /ai/v1/extract-entities
{
  "document_id": "test-scenario-003",
  "content": "Andreessen Horowitz invested $100M in xAI. Sequoia Capital led Anthropic's $450M Series C. Google invested $2.7B in Anthropic over 5 years.",
  "document_type": "text",
  "extraction_config": {
    "entity_types": ["investor", "company", "funding_amount", "funding_round", "timeframe"],
    "relationship_types": ["invested_in", "led_round", "raised", "over_period"],
    "confidence_threshold": 0.75
  }
}
```

**Step 2**: Query investment relationships
```
GET /ai/v1/graph/query?entity_name=Anthropic&relationship_type=invested_in,led_round&min_confidence=0.75
```

---

## 💡 Tips for Testing

### 1. Start Simple
Begin with basic extraction (no config) to see what types the LLM detects:
```json
{
  "document_id": "test-001",
  "content": "Your text here",
  "document_type": "text"
}
```

### 2. Use Custom Types
Test the flexible type system with domain-specific types:
- Software: `framework`, `library`, `language`, `tool`
- Business: `investor`, `valuation`, `market`, `industry`
- Science: `molecule`, `technique`, `measurement`, `organism`

### 3. Test Relationship Flexibility
Try custom relationship types:
- Tech: `uses`, `depends_on`, `integrates_with`, `built_with`
- Business: `invested_in`, `acquired_by`, `competes_with`, `partners_with`
- People: `founded_by`, `ceo_of`, `works_at`, `collaborated_with`

### 4. Adjust Confidence Thresholds
- `0.5-0.6`: Exploratory (more results, lower quality)
- `0.7`: Balanced (recommended default)
- `0.8-0.9`: High precision (fewer results, higher quality)

### 5. Use Source Types
Set appropriate source reliability:
- `official`: 0.95 reliability
- `news_major`: 0.85 reliability
- `social`: 0.50 reliability
- `unknown`: 0.70 reliability

---

## 🚀 Quick Copy-Paste Tests

### Test 1: Basic (Copy & Paste in Swagger UI)
```json
{
  "document_id": "quick-test-001",
  "content": "Apple announced iPhone 15 in September 2023",
  "document_type": "text"
}
```

### Test 2: Tech Stack (Shows Flexibility)
```json
{
  "document_id": "quick-test-002",
  "content": "Our app uses React, TypeScript, and PostgreSQL. It's deployed on AWS with Docker containers.",
  "document_type": "text",
  "extraction_config": {
    "entity_types": ["framework", "language", "database", "platform", "technology"],
    "relationship_types": ["uses", "deployed_on", "containerized_with"]
  }
}
```

### Test 3: Business News
```json
{
  "document_id": "quick-test-003",
  "content": "Microsoft invested $10B in OpenAI. Sam Altman is CEO.",
  "document_type": "text",
  "extraction_config": {
    "entity_types": null,
    "confidence_threshold": 0.7
  }
}
```

---

## 📖 Ready to Test!

1. **Open**: http://localhost:8000/docs
2. **Find**: POST /ai/v1/extract-entities
3. **Click**: "Try it out"
4. **Paste**: Any JSON from above
5. **Click**: "Execute"
6. **See**: Extracted entities with flexible types! 🎉

All examples showcase the **flexible entity and relationship types** we just implemented!

