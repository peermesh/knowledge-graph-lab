# Where to See Entities, Relationships, and Nodes

## 📍 Quick Answer

After running POST /ai/v1/extract-entities, **scroll down in Swagger UI** to see the response with:
- ✅ **entities** array - All extracted entities
- ✅ **relationships** array - All identified relationships
- ✅ **Graph data** - Available through graph query endpoints

---

## 🎯 Method 1: In the Extraction Response (Immediate)

### Step 1: Run Extraction
In Swagger UI at http://localhost:8000/docs:
1. Find: `POST /ai/v1/extract-entities`
2. Click: "Try it out"
3. Paste test data and click "Execute"

### Step 2: Scroll Down to Response
**Look for the Response section** (below the Execute button)

You'll see JSON like this:

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "entities": [
    {
      "id": "entity-1",
      "text": "Microsoft",
      "type": "company",
      "confidence": 0.95,
      "positions": [[0, 9]],
      "metadata": {}
    },
    {
      "id": "entity-2",
      "text": "OpenAI",
      "type": "company",
      "confidence": 0.92,
      "positions": [[30, 36]],
      "metadata": {}
    },
    {
      "id": "entity-3",
      "text": "$10 billion",
      "type": "funding_amount",
      "confidence": 0.98,
      "positions": [[20, 31]],
      "metadata": {}
    }
  ],
  "relationships": [
    {
      "id": "rel-1",
      "source_entity": "entity-1",
      "target_entity": "entity-2",
      "relationship_type": "invested_in",
      "confidence": 0.96,
      "evidence": "Microsoft invested $10 billion in OpenAI",
      "metadata": {}
    }
  ],
  "processing_time_seconds": 2.45
}
```

### 👀 What You're Looking At:

#### **entities** Array
Each entity shows:
- `text` - The actual text extracted (e.g., "Microsoft")
- `type` - The entity type (e.g., "company", "person", "framework")
- `confidence` - How confident the system is (0.0-1.0)
- `positions` - Where it appears in the document
- `id` - Unique identifier for this entity

#### **relationships** Array
Each relationship shows:
- `source_entity` - ID of the source entity
- `target_entity` - ID of the target entity
- `relationship_type` - Type of relationship (e.g., "invested_in", "uses")
- `confidence` - How confident the system is
- `evidence` - Text that supports this relationship

---

## 🔍 Method 2: Query the Knowledge Graph

After extraction, relationships are stored in the knowledge graph. Query them:

### Endpoint: GET /ai/v1/graph/query

**Find it in Swagger UI:**
1. Scroll down to "knowledge-graph" section
2. Find: `GET /ai/v1/graph/query`
3. Click: "Try it out"

**Enter Query Parameters:**
```
entity_name: Microsoft
relationship_type: invested_in
min_confidence: 0.7
max_depth: 2
limit: 10
```

**Response Shows:**
```json
{
  "entity": "Microsoft",
  "relationships": [
    {
      "target": "OpenAI",
      "type": "invested_in",
      "confidence": 0.96,
      "metadata": {
        "amount": "$10 billion"
      }
    }
  ],
  "depth": 1
}
```

---

## 📊 Method 3: Get Specific Entity Details

### Endpoint: GET /ai/v1/graph/entity/{entity_id}

**To see a node's details:**
1. Copy an entity `id` from the extraction response (e.g., "entity-1")
2. Find: `GET /ai/v1/graph/entity/{entity_id}`
3. Enter the entity_id
4. Click "Execute"

**Response Shows:**
```json
{
  "id": "entity-1",
  "text": "Microsoft",
  "type": "company",
  "confidence": 0.95,
  "relationships": {
    "outgoing": [
      {
        "target": "OpenAI",
        "type": "invested_in",
        "confidence": 0.96
      }
    ],
    "incoming": []
  },
  "metadata": {},
  "created_at": "2025-11-02T08:00:00Z"
}
```

---

## 🗺️ Visual Guide: Where to Look in Swagger UI

```
┌─────────────────────────────────────────────────────────┐
│ Swagger UI: http://localhost:8000/docs                  │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│ POST /ai/v1/extract-entities                            │
│ [Try it out] ← Click this                               │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│ Request body                                             │
│ { "document_id": "...", "content": "..." }              │
│ [Execute] ← Click this                                  │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│ ⭐ SCROLL DOWN HERE ⭐                                   │
│                                                          │
│ Response:                                                │
│ {                                                        │
│   "entities": [ ... ],      ← HERE: All entities        │
│   "relationships": [ ... ],  ← HERE: All relationships  │
│   "processing_time": 2.45                               │
│ }                                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 🎮 Interactive Example

### Try This Right Now:

**1. Open:** http://localhost:8000/docs

**2. Find:** POST /ai/v1/extract-entities

**3. Paste this:**
```json
{
  "document_id": "demo-001",
  "content": "React is a JavaScript framework developed by Meta. It uses TypeScript.",
  "document_type": "text",
  "extraction_config": {
    "entity_types": ["framework", "language", "company"],
    "relationship_types": ["developed_by", "uses"]
  }
}
```

**4. Click Execute**

**5. Scroll down and you'll see:**

**ENTITIES** (in the response):
```json
"entities": [
  { "text": "React", "type": "framework", "confidence": 0.92 },
  { "text": "JavaScript", "type": "language", "confidence": 0.88 },
  { "text": "Meta", "type": "company", "confidence": 0.95 },
  { "text": "TypeScript", "type": "language", "confidence": 0.89 }
]
```

**RELATIONSHIPS** (in the same response):
```json
"relationships": [
  {
    "source_entity": "React",
    "target_entity": "Meta",
    "relationship_type": "developed_by",
    "confidence": 0.93
  },
  {
    "source_entity": "React",
    "target_entity": "TypeScript",
    "relationship_type": "uses",
    "confidence": 0.87
  }
]
```

---

## 📋 Response Structure Cheat Sheet

```
ExtractionResponse
├── job_id              (string)
├── status              (completed/pending/failed)
├── entities            (array) ← LOOK HERE FOR ENTITIES
│   ├── [0]
│   │   ├── id
│   │   ├── text      ← The actual entity text
│   │   ├── type      ← Entity type (flexible!)
│   │   ├── confidence
│   │   ├── positions
│   │   └── metadata
│   └── [1...n]
├── relationships       (array) ← LOOK HERE FOR RELATIONSHIPS
│   ├── [0]
│   │   ├── id
│   │   ├── source_entity    ← From this entity
│   │   ├── target_entity    ← To this entity
│   │   ├── relationship_type ← Type (flexible!)
│   │   ├── confidence
│   │   ├── evidence
│   │   └── metadata
│   └── [1...n]
└── processing_time_seconds
```

---

## 🔄 If You Don't See Results

### Common Issues:

**1. Status is "pending"**
- Document was large, processing async
- Check: GET /ai/v1/jobs/{job_id}
- Wait a few seconds, then check again

**2. Empty arrays**
- Content too short or unclear
- LLM couldn't find entities
- Try more descriptive content

**3. Response code 500**
- Check if Docker services are running: `docker-compose ps`
- Check if LLM API key is set in .env
- Check API logs for errors

---

## 💡 Pro Tips

### 1. Copy entity IDs for Graph Queries
From the extraction response:
```json
"entities": [
  { "id": "abc-123", "text": "Microsoft" }
]
```
Use `abc-123` in: GET /ai/v1/graph/entity/abc-123

### 2. Explore Relationships
Use the relationship data to visualize connections:
```
Microsoft --[invested_in]--> OpenAI
OpenAI --[competes_with]--> Anthropic
```

### 3. Check Confidence Scores
Filter by confidence to get high-quality results:
```json
"extraction_config": {
  "confidence_threshold": 0.8  // Only high-confidence
}
```

### 4. Use Browser DevTools
- Open DevTools (F12)
- Go to Network tab
- See raw JSON responses
- Copy/save for analysis

---

## 🎯 Summary

**To see entities and relationships:**

1. **In Swagger UI Response** ← Easiest!
   - POST /ai/v1/extract-entities
   - Scroll down after Execute
   - See "entities" and "relationships" arrays

2. **Query the Graph**
   - GET /ai/v1/graph/query
   - Search by entity name or relationship type

3. **Get Node Details**
   - GET /ai/v1/graph/entity/{entity_id}
   - Use entity ID from extraction response

**The data is RIGHT THERE in the extraction response!** Just scroll down in Swagger UI after clicking Execute. 📜

---

## 🚀 Quick Test

Run this now to see everything:

```json
{
  "document_id": "test-see-results",
  "content": "Microsoft invested $10B in OpenAI. Sam Altman is CEO.",
  "document_type": "text"
}
```

Then **scroll down** and you'll see:
- ✅ 3-4 entities (Microsoft, OpenAI, $10B, Sam Altman)
- ✅ 2-3 relationships (invested_in, is_ceo_of)
- ✅ All with flexible types!

**Try it now at http://localhost:8000/docs!** 🎉

