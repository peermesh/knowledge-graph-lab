# Decisions Made - AI Module

**Distilled from:** AI-Development-Spec.md, PRD.md, architecture.md, ai-publishing-integration.md

**Date:** 2025-10-10

---

## Decision 1: Tech Stack - Python/FastAPI

**Status:** ✅ Firm Decision

**What Was Decided:**

Use Python 3.11 + FastAPI + spaCy + OpenAI API + Docker as the core technology stack for the AI Module.

**Components:**

- **Python 3.11:** Latest stable Python version
- **FastAPI:** Modern async web framework with automatic OpenAPI docs
- **spaCy:** Local NER library for basic entity extraction
- **OpenAI API:** GPT-4 for complex extraction and synthesis
- **Docker:** Containerization for consistent deployment

**Rationale:**

1. **FastAPI:** Provides excellent async performance, automatic API documentation, and modern Python features
2. **Python:** Best ecosystem for AI/ML libraries (transformers, langchain, etc.)
3. **spaCy:** Free, fast local NER for cost-sensitive operations
4. **OpenAI API:** Highest accuracy for complex extraction tasks
5. **Docker:** Ensures consistent deployment across environments

**Alternatives Considered:**

- Node.js + TypeScript: Rejected due to weaker AI/ML ecosystem
- Django: Rejected due to heavier framework (FastAPI is lighter)
- No containerization: Rejected due to deployment inconsistencies

**Impact:**

- Enables rapid development with Python's AI libraries
- FastAPI provides high performance for API endpoints
- Docker simplifies deployment and scaling

**Source:** `PRD.md` lines 32-39

---

## Decision 2: Mock-First Implementation Strategy

**Status:** ✅ Firm Decision

**What Was Decided:**

Build the AI service with mock responses first (Phase 1), then add real AI integration later (Phase 2).

**Implementation Approach:**

**Phase 1 (Weeks 1-6): Mock Implementation**

- Build API with hardcoded mock responses
- Pattern matching for entity detection
- No AI API costs during infrastructure development
- Enables Backend team to integrate in parallel

**Phase 2 (Weeks 7-10): Real AI Integration**

- Replace mocks with actual LLM calls
- Implement real entity extraction with GPT-4/Claude
- Add prompt engineering and optimization
- Handle API errors and rate limits

**Rationale:**

1. **Cost Savings:** Avoid API costs during development and testing
2. **Parallel Development:** Backend can integrate while AI team builds real extraction
3. **Risk Reduction:** Validate architecture before expensive operations
4. **Faster Iteration:** Mock responses allow rapid testing without API delays
5. **Infrastructure Testing:** Test deployment, scaling, monitoring without AI dependency

**Example Mock Implementation:**
```python
def mock_extract_entities(text):
    entities = []
    if "youtube" in text.lower():
        entities.append({"name": "YouTube", "type": "platform", "confidence": 95})
    if "fund" in text.lower():
        entities.append({"name": "Creator Fund", "type": "grant", "confidence": 87})
    return {"entities": entities}
```

**Alternative Considered:**

- Real AI from Day 1: Rejected due to high costs during development and inability to test infrastructure

**Impact:**

- Saves estimated $5,000+ in API costs during development
- Enables parallel work with Backend team (5-week time savings)
- Reduces risk of cost overruns
- Validates API design before commitment

**Source:** `PRD.md` lines 10-11, 109-150

---

## Decision 3: Microservices Architecture

**Status:** ✅ Firm Decision

**What Was Decided:**

Use a microservices architecture with 5 independent services, including a dedicated AI Processing Service.

**The 5 Services:**

1. **Data Ingestion Service** - Source collection and normalization
2. **AI Processing Service** - Entity extraction and intelligence (our module)
3. **Graph Database Layer** - Knowledge storage and queries
4. **API Gateway** - Request routing, auth, caching
5. **Publishing Service** - Content personalization and distribution

**AI Processing Service Characteristics:**

- Independent deployment
- Own Docker container
- Scales independently
- Communicates via events
- Has dedicated resources

**Rationale:**

1. **Parallel Development:** Teams work independently on services
2. **Service Isolation:** Failures contained, don't cascade to other services
3. **Independent Scaling:** Scale AI processing without scaling ingestion
4. **Technology Flexibility:** Each service can use optimal tech stack
5. **Resilience:** Loose coupling through event-driven architecture

**Alternative Considered:**

- Monolithic architecture: Rejected due to:
  - Difficulty with parallel development
  - All-or-nothing deployment
  - Single point of failure
  - Hard to scale individual components

**Impact:**

- Enables 4 teams to work in parallel (4x development speed)
- AI module can scale 2-20 replicas based on load
- Failures in other services don't bring down AI module
- Can deploy AI updates without touching other services

**Trade-offs:**

- More operational complexity (5 services vs. 1)
- Requires event bus infrastructure
- More monitoring and observability needed
- Distributed system debugging challenges

**Source:** `architecture.md` lines 5-40

---

## Decision 4: Event-Driven Communication

**Status:** ✅ Firm Decision

**What Was Decided:**

Use an event bus (RabbitMQ) for inter-service communication with asynchronous processing patterns.

**Event Bus Architecture:**

- **Technology:** RabbitMQ (message broker)
- **Pattern:** Publish-subscribe with topics
- **Durability:** Persistent messages with delivery guarantees
- **Error Handling:** Dead letter queues for failed messages

**AI Module Event Types:**

**Events AI Publishes:**

- `entity.extracted` - New entity discovered
- `relationship.discovered` - New relationship mapped
- `report.generated` - News report created
- `processing.failed` - Extraction failed
- `processing.completed` - Document fully processed

**Events AI Subscribes To:**

- `document.normalized` - New document ready for processing
- `extraction.requested` - Explicit extraction request
- `feedback.received` - User correction or feedback

**Rationale:**

1. **Asynchronous Processing:** Non-blocking operations for better performance
2. **Retry Mechanisms:** Automatic handling of transient failures
3. **Audit Trails:** Complete event history for compliance and debugging
4. **Loose Coupling:** Services don't know about each other directly
5. **Scalability:** Easy to add new consumers without changing producers
6. **Resilience:** Dead letter queues capture failed messages for analysis

**Event Schema Example:**
```json
{
  "eventType": "entity.extracted",
  "timestamp": "2025-10-10T14:30:00Z",
  "correlationId": "job-uuid-123",
  "payload": {
    "document_id": "doc-456",
    "entity": {"name": "YouTube", "type": "platform", "confidence": 95}
  }
}
```

**Alternatives Considered:**

- **Synchronous REST Calls:** Rejected due to:
  - Tight coupling between services
  - Cascading failures
  - Poor performance (blocking)
  - No automatic retry
- **gRPC:** Considered but rejected due to:
  - Still synchronous
  - More complex than needed
  - Less tooling support

**Impact:**

- AI module can process documents asynchronously in background
- Other services don't wait for AI processing to complete
- System stays responsive even when AI is under heavy load
- Failed extractions automatically retry with exponential backoff

**Source:** `architecture.md` lines 88-107

---

## Decision 5: Separation of Concerns - AI Generates, Backend Stores, Publishing Distributes

**Status:** ✅ Firm Decision

**What Was Decided:**

Clean separation of responsibilities: AI generates standalone reports with URLs, Backend stores them, Publishing queries and distributes.

**Responsibility Breakdown:**

**AI Module:**

- Generates complete, standalone news reports
- Uses prompts to write in journalistic style
- Has NO knowledge of subscribers or emails
- Each report is self-contained with its own URL
- Tags reports with topics, entities, priority
- Calculates relevance scores by category

**Backend Module:**

- Stores all reports with metadata
- Provides query interface for report retrieval
- Manages report URLs and routing
- Indexes reports for efficient querying

**Publishing Module:**

- Queries reports based on subscriber preferences
- Decides which reports to include in emails
- Formats report excerpts for email presentation
- Handles all subscriber personalization
- Manages delivery timing and channels

**Data Flow:**
```
AI Module → POST /api/reports → Backend Storage → GET /api/reports → Publishing Module → Email/Web
```

**Rationale:**

1. **Loose Coupling:** AI doesn't know about Publishing, Publishing doesn't know about AI internals
2. **Independent Scaling:** Each module scales based on its own load
3. **Clear Boundaries:** No ambiguity about who owns what
4. **Multiple Distribution Channels:** Publishing can add new channels without AI changes
5. **Testability:** Can test AI report generation without Publishing

**Integration Contract:**

**AI → Backend:**
```json
POST /api/reports
{
  "report_id": "uuid",
  "url": "/reports/2025-10-10/openai-funding",
  "headline": "OpenAI Raises $10B...",
  "body": [...],
  "metadata": {
    "entities": ["OpenAI", "Microsoft"],
    "topics": ["AI", "venture_capital"],
    "priority": "breaking",
    "relevance_scores": {"ai_industry": 0.98}
  }
}
```

**Publishing → Backend:**
```
GET /api/reports?date_range=2025-10-10&topics=AI&min_relevance=0.7
```

**Alternative Considered:**

- AI directly sends to Publishing: Rejected due to:
  - Tight coupling (AI needs to know about Publishing)
  - Single distribution channel (hard to add new channels)
  - Can't query historical reports easily
  - Publishing can't control when to fetch reports

**Impact:**

- AI team can work independently of Publishing team
- Can add new distribution channels (Slack, Discord) without AI changes
- Publishing can implement complex personalization without AI changes
- Reports are stored with URLs for web access independent of email

**Source:** `ai-publishing-integration.md` lines 115-163

---

## Decision 6: Multi-Model Strategy

**Status:** ✅ Firm Decision

**What Was Decided:**

Use multiple LLM providers (OpenAI, Anthropic, open models) with task-based selection logic.

**Model Portfolio:**
| Model | Use Case | Cost | Accuracy |
|-------|----------|------|----------|
| GPT-4 | Complex extraction, synthesis | High ($0.03/1k tokens) | Highest |
| GPT-3.5 | Standard extraction | Medium ($0.001/1k tokens) | High |
| Claude | Long documents (100k context) | High | High |
| spaCy | Simple NER, cost-sensitive | Free | Medium |
| Llama (future) | Self-hosted operations | Infrastructure only | Medium-High |

**Selection Logic:**

**Task-Based Selection:**
```python
def select_model(task_type, document_length, budget_remaining):
    if document_length > 10000:
        return "claude"  # Large context window
    elif task_type == "simple_ner" and budget_remaining < threshold:
        return "spacy"  # Cost-sensitive
    elif task_type == "complex_extraction":
        return "gpt-4"  # Highest accuracy
    else:
        return "gpt-3.5"  # Good balance
```

**Fallback Hierarchy:**
```
Primary: GPT-4 → Fallback 1: Claude → Fallback 2: GPT-3.5 → Fallback 3: spaCy
```

**Rationale:**

1. **Avoid Vendor Lock-in:** Not dependent on single provider
2. **Cost Optimization:** Use cheaper models for simple tasks
3. **Resilience:** Fallback options when primary unavailable
4. **A/B Testing:** Compare model performance objectively
5. **Future-Proofing:** Easy to add new models as they emerge

**Model Selection Criteria:**

- **Accuracy Requirements:** High-stakes extraction → GPT-4
- **Cost Constraints:** Budget-limited → spaCy or GPT-3.5
- **Context Length:** Long documents → Claude (100k tokens)
- **Speed Requirements:** Real-time → spaCy (local, fast)
- **Availability:** Primary down → Fallback model

**Alternatives Considered:**

- **Single Provider (OpenAI only):** Rejected due to:
  - Vendor lock-in risk
  - No fallback if service down
  - Miss cost optimization opportunities
  - Can't leverage provider strengths
- **No Local Models:** Rejected due to:
  - 100% dependency on external APIs
  - No offline capability
  - Higher costs for simple tasks

**Impact:**

- Reduced costs by using GPT-3.5 for 60% of tasks (saves ~$6,000/month)
- System stays operational even if OpenAI has outage
- Can leverage Claude's large context for long documents
- A/B testing reveals GPT-4 is 12% more accurate but 30x more expensive

**Model Versioning Strategy:**

- Track model version used for each extraction
- Store model responses for debugging
- Enable rollback to previous model versions
- Document performance by model version

**Source:** `AI-Development-Spec.md` lines 35-40, `work-description.md` lines 176-180

---

## Decision 7: Confidence Scoring System

**Status:** ✅ Firm Decision

**What Was Decided:**

Implement a 0-100 confidence scoring system with weighted formula and validation thresholds.

**Scoring Formula:**
```
confidence_score = (source_score * 0.3) + (context_score * 0.4) + (model_confidence * 0.3)
```

**Components:**

**1. Source Score (30% weight):**

- Official websites: 95-100
- Verified news sources: 85-95
- Social media platforms: 70-85
- Aggregators: 60-75
- Unverified sources: 40-60

**2. Context Score (40% weight - highest):**

- Multiple independent mentions: +20
- Consistent across sources: +15
- Temporal consistency: +10
- Contradictory information: -30

**3. Model Confidence (30% weight):**

- LLM self-reported confidence
- Calibrated against ground truth
- Adjusted for known model biases

**Thresholds:**

- **High Confidence:** ≥85 (green flag, 90%+ accurate)
- **Medium Confidence:** 70-84 (yellow flag, 75-85% accurate)
- **Low Confidence:** <70 (red flag, requires review)

**Rationale:**

1. **Transparency:** Users understand certainty of information
2. **Quality Control:** Filter low-confidence extractions
3. **Prioritization:** Focus human review on uncertain extractions
4. **Learning:** Calibrate confidence scores against actual accuracy
5. **User Trust:** Don't present uncertain information as certain

**Validation Strategy:**

- Manual review of 100 random extractions per confidence bucket
- Calculate actual accuracy vs. confidence score
- Recalibrate formula monthly
- Track confidence calibration metrics

**Example Calculation:**
```
Document: "YouTube announces $100M creator fund" (verified press release)

source_score = 95 (official press release)
context_score = 85 (mentioned in 3 independent sources)
model_confidence = 92 (GPT-4 high confidence)

confidence = (95 * 0.3) + (85 * 0.4) + (92 * 0.3)
           = 28.5 + 34 + 27.6
           = 90.1

Result: HIGH CONFIDENCE (≥85)
```

**Alternatives Considered:**

- **Binary (High/Low):** Rejected due to lack of granularity
- **3-Tier (High/Medium/Low):** Considered but less flexible
- **No Confidence Scores:** Rejected due to transparency needs

**Impact:**

- Users can filter results by confidence level
- Low-confidence extractions automatically flagged for review
- Confidence calibration improved accuracy by 8% in testing
- Trust increased as users understand certainty levels

**Source:** `AI-Development-Spec.md` lines 21-28

---

## Decision 8: Phased Rollout Strategy

**Status:** ✅ Firm Decision

**What Was Decided:**

Implement AI module in 3 phases with increasing complexity and accuracy targets.

**Phase Breakdown:**

**Phase 3 (MVP) - Weeks 1-12:**

- **Goal:** Prove value with basic extraction
- **Accuracy:** 80% precision, 75% recall
- **Throughput:** 100 docs/hour
- **Cost:** $0.10/document
- **Features:** 5 entity types, basic confidence scoring, Backend integration

**Phase 4 (Enhanced) - Weeks 13-20:**

- **Goal:** Production-grade quality
- **Accuracy:** 90% entity precision, 80% relationship precision
- **Throughput:** 500 docs/hour (5x improvement)
- **Cost:** $0.07/document (30% reduction)
- **Features:** Relationship extraction, multi-model ensemble, fine-tuning, streaming

**Phase 5 (Production) - Weeks 21+:**

- **Goal:** Best-in-class performance
- **Accuracy:** 95% entity precision, 85% relationship precision
- **Throughput:** 1000 docs/hour (10x improvement)
- **Cost:** $0.05/document (50% reduction)
- **Features:** 10+ entity types, self-improving, granular confidence, feedback loops

**Rationale:**

1. **Incremental Value:** Deliver value quickly, improve over time
2. **Risk Management:** Validate approach before full investment
3. **Learning:** Each phase informs next phase's priorities
4. **Resource Allocation:** Spread costs over time
5. **User Feedback:** Incorporate feedback between phases

**Milestone Gates:**

- Phase 3 → 4: Must achieve 80% accuracy
- Phase 4 → 5: Must achieve 90% accuracy and positive ROI

**Alternative Considered:**

- Big Bang (all features Phase 1): Rejected due to:
  - High risk (no validation before full investment)
  - Longer time to first value
  - Harder to course-correct
  - More expensive upfront

**Impact:**

- Users get value in 12 weeks (not 6+ months)
- Can validate market fit before major investment
- Phased budget easier to approve than big bang
- Each phase's learnings improve next phase

**Source:** `AI-Development-Spec.md` lines 256-294

---

## Decision 9: Data Pipeline Architecture

**Status:** ✅ Firm Decision

**What Was Decided:**

Implement a 8-stage processing pipeline with validation, error handling, and retry logic.

**Pipeline Stages:**

**1. Input Reception:**

- Receive job from queue (RabbitMQ)
- Parse document metadata and content
- Validate format and completeness

**2. Document Chunking:**

- Split into 1000-2000 token segments
- Maintain context across boundaries
- Preserve document structure

**3. Entity Extraction:**

- Select model based on task/budget
- Apply extraction prompt templates
- Parse structured JSON output

**4. Relationship Inference:**

- Analyze entity co-occurrence
- Apply relationship extraction prompts
- Build relationship graph

**5. Confidence Scoring:**

- Calculate source, context, model scores
- Apply weighted formula
- Validate calibration

**6. Embedding Generation:**

- Generate document embeddings
- Store in vector database
- Index for similarity search

**7. Validation & Quality Checks:**

- Check entity formats (dates, amounts)
- Validate relationship consistency
- Run schema compliance checks

**8. Output & Reporting:**

- Format output JSON
- Send to Backend via API/event
- Update processing metrics

**Error Handling at Each Stage:**

- Retry with exponential backoff (max 3 attempts)
- Fallback to simpler model if primary fails
- Dead letter queue for non-recoverable errors
- Alert monitoring on error rate > 5%

**Rationale:**

1. **Modularity:** Each stage can be optimized independently
2. **Testability:** Can test each stage in isolation
3. **Observability:** Track metrics at each stage
4. **Resilience:** Errors contained to single stage
5. **Flexibility:** Easy to add new stages or modify existing

**Alternative Considered:**

- Single-stage processing: Rejected due to:
  - Hard to debug which step failed
  - All-or-nothing processing
  - Can't optimize individual steps
  - Poor observability

**Impact:**

- Can identify which stage causes most errors (chunking = 35%)
- Can optimize slow stages independently (extraction = 60% of time)
- Failed documents can be retried from last successful stage
- Clear metrics for each stage enable targeted improvements

**Source:** `AI-Development-Spec.md` lines 41-49

---

## Decision 10: API Design - REST with JSON

**Status:** ✅ Firm Decision

**What Was Decided:**

Use RESTful API design with JSON payloads for all AI module endpoints.

**API Endpoints:**

**1. Extract Entities:**
```
POST /api/extract
Content-Type: application/json

{
  "text": "Document content...",
  "source_id": "doc-123",
  "options": {"confidence_threshold": 70}
}
```

**2. Generate Embeddings:**
```
POST /api/embed
Content-Type: application/json

{
  "text": "Content to embed...",
  "model": "text-embedding-ada-002"
}
```

**3. Summarize Content:**
```
POST /api/summarize
Content-Type: application/json

{
  "text": "Long article...",
  "max_length": 200
}
```

**API Characteristics:**

- RESTful design (POST for actions, GET for queries)
- JSON request/response (application/json)
- OpenAPI documentation (auto-generated by FastAPI)
- Versioning via URL path (/v1/api/extract)
- Standard HTTP status codes
- CORS support for frontend

**Rationale:**

1. **Simplicity:** REST is widely understood
2. **Tooling:** Excellent client libraries for all languages
3. **Documentation:** OpenAPI/Swagger auto-docs
4. **Compatibility:** Works with any HTTP client
5. **Caching:** Standard HTTP caching headers

**Alternatives Considered:**

- **GraphQL:** Rejected due to:
  - Overkill for simple API
  - More complex to implement
  - Less familiar to team
- **gRPC:** Rejected due to:
  - Binary protocol harder to debug
  - Less browser support
  - More setup complexity

**Impact:**

- Frontend can call API with simple fetch()
- Backend can integrate with standard HTTP client
- OpenAPI docs enable easy testing and exploration
- Standard REST patterns reduce learning curve

**Source:** `PRD.md` lines 40-70

---

## Summary of Key Decisions

**Technology Decisions:**

1. ✅ Python/FastAPI tech stack
2. ✅ Multi-model strategy (GPT-4, Claude, spaCy, Llama)
3. ✅ REST API with JSON
4. ✅ RabbitMQ event bus
5. ✅ Docker containerization

**Architecture Decisions:**

6. ✅ Microservices architecture (5 services)
7. ✅ Event-driven communication
8. ✅ 8-stage processing pipeline
9. ✅ Separation of concerns (AI/Backend/Publishing)

**Strategy Decisions:**

10. ✅ Mock-first implementation (Phase 1 mocks, Phase 2 real AI)
11. ✅ Phased rollout (Phase 3 → 4 → 5 with increasing accuracy)
12. ✅ Confidence scoring system (0-100 scale with formula)

**All decisions are firm and supported by clear rationale.**

---

## Sources

- `docs/modules/ai-development/PRD.md` - Tech stack, mock-first strategy, API design
- `docs/modules/ai-development/AI-Development-Spec.md` - Pipeline, confidence scoring, phased rollout
- `docs/design/system/architecture.md` - Microservices, event-driven architecture
- `docs/design/system/ai-publishing-integration.md` - Separation of concerns
- `docs/team/module-assignments/ai-development/01-work-description.md` - Multi-model strategy
