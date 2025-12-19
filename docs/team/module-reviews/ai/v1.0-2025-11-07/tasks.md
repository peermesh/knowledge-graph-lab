# Tasks for AI Module v1.0-2025-11-07

## 🎯 HIGHLIGHTS - Top Things to Check Out

### 🔥 Cool Features Worth Exploring
- **Advanced entity extraction with confidence scoring** (src/ai/services/entity_extractor.py:240-350) - Multi-factor confidence calculation using source reliability (30%), context co-occurrence (40%), and model confidence (30%)
- **Hybrid relationship detection** (src/ai/services/relationship_mapper.py:78-99) - Combines rule-based pattern matching with LLM-based detection for 6 relationship types (fund, partner, acquire, compete, collaborate, found)
- **Lazy-loading LLM client with graceful fallback** (src/ai/integrations/llm_client.py:295-319) - Innovative lazy initialization prevents startup crashes when LLM providers unavailable, includes OpenAI→Claude fallback
- **Multi-provider LLM response normalization** (src/ai/integrations/llm_client.py:185-281) - Sophisticated key normalization handles different response formats from OpenAI/Claude/other providers
- **Async chunked document processing** (src/ai/services/entity_extractor.py:171-209) - Smart text chunking with overlap (200 tokens) and parallel processing with semaphore-limited concurrency (max 3 concurrent)

### ⚠️ Potential Issues to Investigate
- **CRITICAL: Missing src/ai/lib/ directory** (src/ai/services/entity_extractor.py:10-22) - All imports from src.ai.lib.* fail (confidence_scoring, text_processing) causing immediate ImportError on module load
- **Vector embedding dimension mismatch** (src/ai/config.py:36 vs src/ai/integrations/vector_db.py:18) - Config specifies 384 dimensions but VectorDBClient hardcodes 768, causing inconsistent embeddings
- **In-memory job storage is not production-ready** (src/ai/api/extraction.py:98) - Jobs stored in dict will lose all state on server restart, no persistence layer
- **Missing pgvector dependency** (src/ai/models/entity.py:9-14) - Code gracefully degrades to ARRAY type but pgvector extension setup not documented
- **No LLM API key validation** (src/ai/integrations/llm_client.py:33-42) - Server starts successfully without API keys but extraction silently returns empty results

---

**Generated:** 2025-11-24
**Module:** AI Intelligence
**Developer:** haejeg  
**Total Tasks:** 20
**Estimated Effort:** 7-9 days

---

## Critical (P0) - Block release

### CRIT-1: Implement missing src/ai/lib/ modules (2 days)
**Files:** entity_extractor.py:10-22, extraction.py:10, main.py:13

Missing imports cause ImportError on startup:
- src/ai/lib/confidence_scoring.py
- src/ai/lib/text_processing.py  
- src/ai/lib/deduplication.py
- src/ai/lib/graph_formatter.py
- src/ai/lib/logging_config.py

**Remediation:** Create lib/ directory and implement all 5 modules per function signatures in entity_extractor.py

---

### CRIT-2: Fix vector embedding dimension mismatch (4 hours)
**Files:** config.py:36, vector_db.py:18, graph_builder.py:129,238

Conflicting dimensions: config=384, vector_db=768, causing Qdrant errors.

**Remediation:** Standardize on one dimension (768 for OpenAI, 384 for sentence-transformers) across all files

---

### CRIT-3: Replace in-memory job storage (1 day)
**Files:** extraction.py:98

Jobs stored in dict lost on restart. Use DocumentProcessingJob model with database persistence.

**Remediation:** Replace jobs_store dict with database queries using existing model

---

### CRIT-4: Add LLM API key validation on startup (4 hours)
**Files:** llm_client.py:33-42, main.py

Server starts without API keys but extraction returns empty results silently.

**Remediation:** Add @app.on_event("startup") validator to fail fast if no LLM provider configured

---

## High Priority (P1) - Complete before next version

### HIGH-1: Document pgvector extension setup (2 hours)
**Files:** README.md, entity.py:9-14

Code uses pgvector but setup not documented. Add installation guide for brew/apt and Docker image.

---

### HIGH-2: Implement deduplication library (1 day)
**Files:** extraction.py:232-240

imported but not implemented. Need fuzzy entity matching with 85% threshold.

**Functions needed:**
- deduplicate_entities(entities, threshold) -> (List, Dict)
- update_relationship_entity_ids(relationships, mapping) -> List

---

### HIGH-3: Implement graph formatter utility (6 hours)
**Files:** Referenced in IMPLEMENTATION_SUMMARY.md:60

Missing visualization formatter for frontend integration.

**Functions needed:**
- format_for_visualization(nodes, edges, layout) -> Dict
- calculate_node_colors(nodes) -> Dict
- apply_layout(nodes, edges, algorithm) -> List

---

### HIGH-4: Add comprehensive LLM error handling (4 hours)
**Files:** llm_client.py:100-125

Missing retry logic for rate limits, token limits, timeouts.

**Remediation:** Add backoff decorator for retry logic and chunk large documents on token errors

---

### HIGH-5: Add relationship type validation (4 hours)  
**Files:** relationship_mapper.py:16-46, 184

Accepts any type from LLM causing inconsistent types. Normalize to 7 canonical types with alias mapping.

---

## Medium Priority (P2) - Schedule for next sprint

### MED-1: Add unit tests for services (2 days)
**Files:** tests/unit/ (empty)

No unit tests exist. Add test coverage for:
- entity_extractor (process_entity, calculate_co_occurrence)
- relationship_mapper (rule_based, llm_based)
- graph_builder (create_node, create_edge)
- confidence_scoring (once implemented)
- text_processing (once implemented)

**Target:** 80% line coverage

---

### MED-2: Implement database connection pooling (4 hours)
**Files:** Create database.py

No visible pool configuration. Add SQLAlchemy pool_size=20, max_overflow=30, pool_pre_ping=True

---

### MED-3: Add request/response logging middleware (4 hours)
**Files:** Create middleware/logging_middleware.py

Add request_id tracking and duration_ms logging for all API calls.

---

### MED-4: Add Prometheus metrics (6 hours)
**Files:** Create api/metrics.py

Add metrics for:
- http_requests_total
- http_request_duration_seconds  
- entities_extracted_total
- extraction_confidence histogram
- jobs_pending/processing gauges

---

### MED-5: Document authentication implementation (4 hours)
**Files:** README.md, dependencies.py

README claims JWT auth but no implementation visible. Either implement or correct documentation.

---

## Low Priority (P3) - Nice to have

### LOW-1: Add OpenAPI schema examples (2 hours)
**Files:** src/ai/api/extraction.py:40-95, src/ai/api/graph_query.py:25-45

Add Config.json_schema_extra examples to all Pydantic models for better API docs.

**Implementation:**
```python
# In src/ai/api/extraction.py:45-50
class ExtractionRequest(BaseModel):
    document_id: str
    text: str
    extraction_type: str = "entities_and_relationships"

    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc-123",
                "text": "Apple Inc. acquired Beats Electronics for $3 billion in 2014.",
                "extraction_type": "entities_and_relationships"
            }
        }
```

---

### LOW-2: Add batch extraction endpoint (4 hours)
**Files:** src/ai/api/extraction.py (add after line 95)

Add POST /ai/v1/extract-entities/batch accepting List[ExtractionRequest] for bulk processing.

**Implementation:**
```python
# In src/ai/api/extraction.py after line 95
@router.post("/extract-entities/batch")
async def batch_extract_entities(
    requests: List[ExtractionRequest],
    db: Session = Depends(get_db)
) -> List[ExtractionResponse]:
    """Process multiple extraction requests in parallel."""
    if len(requests) > 10:
        raise HTTPException(400, "Maximum 10 documents per batch")

    tasks = [process_extraction(req, db) for req in requests]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return [r if not isinstance(r, Exception) else
            ExtractionResponse(error=str(r)) for r in results]
```

---

### LOW-3: Add entity confidence recalculation (4 hours)
**Files:** graph_query.py (new endpoint)

Add POST /ai/v1/entities/recalculate-confidence to recompute scores after algorithm improvements.

---

### LOW-4: Add graph export endpoints (4 hours)
**Files:** graph_query.py (new endpoint)

Add GET /ai/v1/graph/export/{format} supporting JSON, Cypher, GEXF, GraphML formats.

---

### LOW-5: Add entity merge endpoint (6 hours)
**Files:** graph_query.py (new endpoint)

Add POST /ai/v1/entities/merge for manual deduplication when automatic fails.

---

## Summary

| Priority | Tasks | Effort |
|----------|-------|--------|
| P0 (Critical) | 4 | 4 days |
| P1 (High) | 5 | 2.5 days |
| P2 (Medium) | 5 | 4.5 days |
| P3 (Low) | 5 | 3 days |
| **Total** | **20** | **~14 days** |

**Top 3 Priorities:**
1. CRIT-1: Implement missing lib/ modules (blocks ALL functionality)
2. CRIT-2: Fix vector dimension mismatch (blocks vector search)
3. CRIT-3: Replace in-memory job storage (blocks production deployment)
