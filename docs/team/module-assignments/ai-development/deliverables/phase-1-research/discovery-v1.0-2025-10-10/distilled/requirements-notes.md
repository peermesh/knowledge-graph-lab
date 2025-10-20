# Requirements Notes - AI Module

**Distilled from:** AI-Development-Spec.md, PRD.md, work-description.md

**Date:** 2025-10-10

---

## Core Functional Requirements

### 1. Entity Extraction

**Requirement:** Extract structured entities from unstructured text

**Entity Types:**

- **Organizations:** Companies, platforms, foundations
- **People:** Creators, executives, influencers
- **Financial:** Funding amounts, grant values, revenue figures
- **Temporal:** Dates, deadlines, timelines
- **Geographic:** Locations, regions, markets
- **Domain-Specific:** Grants, partnerships, events, programs

**Accuracy Targets:**

- Phase 3 (MVP): 80% precision, 75% recall
- Phase 4 (Enhanced): 90% precision, 85% recall
- Phase 5 (Production): 95% precision, 85% recall

**Named Entity Recognition (NER):**

- Use modern NER models (spaCy, custom-trained)
- Support multiple languages: English, Spanish, French
- Handle multiple formats: HTML, PDF, plain text
- Extract entities with position information (start/end indices)

**Custom Entity Types:**

- Build extractors for domain-specific entities
- Creator economy entities: platforms, creator funds, partnership programs
- Extensible entity type system for future domains

**Source:** `AI-Development-Spec.md` lines 9-14

---

### 2. Relationship Mapping

**Requirement:** Identify and map relationships between entities

**Relationship Types:**

- **Fund:** Who funds whom (organizations → grants)
- **Partner:** Who partners with whom (platforms ↔ brands)
- **Acquire:** Who acquires whom (company acquisitions)
- **Compete:** Who competes with whom (platform rivalry)
- **Collaborate:** Who collaborates with whom (creator collaborations)
- **Mention:** Who mentions whom (social references)

**Relationship Discovery Methods:**

- **Explicit:** Stated directly in text ("Google owns YouTube")
- **Implicit:** Inferred from patterns ("Creators who use X often mention Y")
- **Temporal:** Time-based connections ("Grant X launched after Platform Y's policy change")

**Accuracy Targets:**

- Phase 4: 80% precision for relationship identification
- Phase 5: 85% precision for relationship identification

**Graph Construction:**

- Build knowledge graphs from extracted relationships
- Support temporal relationship tracking (how connections change over time)
- Enable graph traversal and query operations

**Source:** `AI-Development-Spec.md` lines 15-20

---

### 3. Confidence Scoring

**Requirement:** Provide confidence scores for all extractions

**Scoring System:**

- **Scale:** 0-100 (continuous)
- **Thresholds:**
  - High confidence: ≥85
  - Medium confidence: 70-84
  - Low confidence: <70

**Confidence Formula:**
```
score = (source_score * 0.3) + (context_score * 0.4) + (model_confidence * 0.3)
```

**Components:**

- **Source Reliability:** Official sites = high, social media = medium
- **Context Analysis:** Multiple mentions = higher confidence
- **Extraction Certainty:** Model confidence and pattern matching strength

**Implementation:**

- Validate confidence scores against ground truth
- Calibrate thresholds based on accuracy metrics
- Provide confidence explanations (why score is high/medium/low)

**Source:** `AI-Development-Spec.md` lines 21-28

---

### 4. Data Pipeline

**Requirement:** Process documents through complete AI/ML pipeline

**Pipeline Stages:**

1. **Input:** Raw documents from Backend (HTML, PDF, text)
2. **Chunking:** Split into processable segments (1000-2000 tokens)
3. **Extraction:** Pull entities and relationships from chunks
4. **Validation:** Check extracted data for consistency and format compliance
5. **Error Handling:** Retry failed extractions with fallback approaches
6. **Output:** Structured JSON with entities, relationships, confidence scores

**Processing Requirements:**

- **Throughput:**
  - Phase 3: 100 documents/hour
  - Phase 4: 500 documents/hour
  - Phase 5: 1000 documents/hour
- **Latency:** Sub-2 second processing per document (target)
- **Reliability:** Retry mechanisms with exponential backoff

**Chunking Strategy:**

- Maintain context across chunk boundaries
- Handle large documents (multi-page PDFs, long articles)
- Preserve document structure metadata

**Source:** `AI-Development-Spec.md` lines 41-49

---

### 5. Prompt Engineering

**Requirement:** Design and optimize prompts for extraction tasks

**Template Design:**

- Create reusable prompts for different extraction tasks
- Support few-shot learning with example libraries
- Version control for prompt templates

**Output Formatting:**

- Design prompts that return structured JSON/XML consistently
- Handle malformed responses gracefully
- Validate output schema compliance

**Resource Optimization:**

- Balance prompt complexity with computational resources
- Minimize token usage while maintaining accuracy
- A/B test prompt variations for performance

**Source:** `AI-Development-Spec.md` lines 29-34

---

### 6. Model Management

**Requirement:** Select, configure, and monitor AI models

**Model Selection:**

- Support multiple providers: GPT-4, Claude, Llama
- Task-based model selection (cost vs. accuracy tradeoffs)
- Fallback models for resilience

**Fine-tuning:**

- Improve models for domain-specific extraction tasks
- Maintain fine-tuned model versions
- Evaluate fine-tuning effectiveness

**Version Control:**

- Track model versions and configurations
- Enable rollback to previous versions
- Document model performance by version

**Performance Monitoring:**

- Track accuracy per extraction type
- Monitor processing speed and resource usage
- Alert on performance degradation

**Source:** `AI-Development-Spec.md` lines 35-40

---

### 7. News Report Generation & Synthesis

**Requirement:** Transform extracted knowledge into standalone news-style reports

**Report Generation:**

- **Prompt-Driven:** Use configurable prompts for different news styles
- **Content Synthesis:** Aggregate findings from multiple sources
- **Report Types:** Breaking news, analysis, market updates, research summaries

**Report Structure:**

- **Standalone:** Each report is complete, independent article
- **Components:** Unique ID, URL, headline, lead, body, conclusion
- **Style:** Journalistic writing style with proper narrative structure

**Metadata & Tagging:**

- **Topic Tags:** Technology, healthcare, finance, etc.
- **Priority Levels:** Breaking, important, standard
- **Entity Tags:** Companies, people, products mentioned
- **Relevance Scoring:** Scores by category for discovery

**Report Schema:**
```json
{
  "report_id": "uuid",
  "url": "/reports/YYYY-MM-DD/slug",
  "headline": "string",
  "lead": "string",
  "body": [{"type": "paragraph", "content": "..."}],
  "metadata": {
    "report_type": "breaking|analysis|update|summary",
    "entities": ["array"],
    "topics": ["array"],
    "priority": "breaking|important|standard",
    "relevance_scores": {"category": 0.0-1.0}
  }
}
```

**Source:** `AI-Development-Spec.md` lines 50-102

---

### 8. Quality Assurance

**Requirement:** Validate and improve extraction quality

**Validation Rules:**

- Check entity formats (dates, amounts, names)
- Validate relationship consistency
- Enforce schema compliance

**Duplicate Detection:**

- Identify duplicate entities across sources
- Merge duplicate entities intelligently
- Preserve provenance information

**Edge Case Handling:**

- Process incomplete documents gracefully
- Handle malformed inputs
- Support partial extraction results

**Feedback Integration:**

- Learn from user corrections
- Adjust confidence scores based on feedback
- Improve extraction accuracy over time

**Accuracy Tracking:**

- Monitor extraction quality metrics
- Track precision and recall by entity type
- Generate accuracy reports

**Source:** `AI-Development-Spec.md` lines 103-109

---

## Module Boundaries

### What AI Module OWNS

**Core Responsibilities:**

- Entity extraction and relationship mapping
- Confidence score generation
- AI/ML pipeline processing
- News report generation
- Structured data output

**Deliverables:**

- Extracted entities with types and confidence
- Relationships between entities
- Document embeddings (768 or 1536 dimensions)
- Processing status updates
- News reports with metadata

**Source:** `AI-Development-Spec.md` lines 110-117, `work-description.md` lines 11-47

---

### What AI Module DOES NOT OWN

**Not AI's Responsibility:**

- **Data Fetching:** Backend fetches from sources
- **Database Storage:** Backend stores extracted data
- **User Interface:** Frontend displays results
- **Content Distribution:** Publishing sends insights to users
- **Infrastructure:** Backend handles servers and deployment
- **Vector Database Deployment:** Backend responsibility
- **Graph Visualization:** Frontend responsibility
- **Email Generation:** Publishing responsibility

**Rationale:** Clear boundaries enable parallel development, prevent scope creep, maintain loose coupling

**Source:** `AI-Development-Spec.md` lines 118-124, `work-description.md` lines 49-63

---

## Integration Requirements

### From Backend Architecture

**What AI Receives:**

- Raw documents in queue (HTML, PDF, plain text)
- Processing job requests with document IDs
- Vector database connection details
- Storage API endpoints

**Job Queue Message Format:**

- Document ID, source URL, content type
- Priority level, retry count
- Processing timeout, metadata

**Source:** `AI-Development-Spec.md` lines 126-140

---

### To Backend Architecture

**What AI Sends:**

- Extracted entities with types and confidence
- Relationships between entities
- Document embeddings (768-dimensional vectors)
- Processing status updates
- Error notifications

**Response Format:**
```json
{
  "entities": [
    {"name": "string", "type": "org|person|amount|date", "confidence": 0-100}
  ],
  "relationships": [
    {"from": "entity_id", "to": "entity_id", "type": "fund|partner|compete", "confidence": 0-100}
  ],
  "embeddings": [float array],
  "status": "success|partial|failed",
  "processing_time": "milliseconds"
}
```

**Source:** `AI-Development-Spec.md` lines 146-160

---

### To Backend for Storage

**What AI Sends:**

- Generated news reports with unique IDs and URLs
- Report metadata for indexing
- Entity and topic tags
- Relevance scores by category

**Storage API:**
```
POST /api/reports
{
  "report": {report_object},
  "metadata": {metadata_object}
}
```

**Source:** `AI-Development-Spec.md` lines 168-191

---

### To Publishing Module

**What Publishing Can Query:**

- All stored reports by date range
- Reports filtered by tags/topics/entities
- Reports sorted by relevance scores
- Report metadata for email assembly

**Query Interface:**
```
GET /api/reports?date_range=X&topics=Y&min_relevance=Z
```

**Note:** Publishing module independently queries reports—AI has no knowledge of subscribers or distribution

**Source:** `AI-Development-Spec.md` lines 193-217

---

### To Frontend Module

**What AI Provides:**

- Extracted entities for graph visualization
- Relationship data for network displays
- Confidence scores for visual encoding
- Timeline data for temporal views
- Search embeddings for similarity queries

**Source:** `AI-Development-Spec.md` lines 218-225

---

## Configuration Requirements

**API Configuration:**

- LLM API keys (OpenAI, Anthropic)
- Rate limit settings per provider
- Timeout configurations

**Model Settings:**

- Model selection preferences (GPT-4 vs. Claude vs. Llama)
- Fallback model hierarchy
- Cost vs. accuracy preferences

**Extraction Rules:**

- Pattern libraries for entity recognition
- Custom entity type definitions
- Relationship type vocabulary

**Quality Thresholds:**

- Confidence levels: 70 (medium), 85 (high)
- Minimum accuracy requirements
- Precision vs. recall tradeoffs

**Resource Limits:**

- Daily budget caps per API
- Processing quotas
- Rate limiting rules

**Environment Variables:**

- Separate configs for dev/staging/production
- API keys and secrets management
- Feature flags for experiments

**Source:** `AI-Development-Spec.md` lines 226-233

---

## Monitoring & Observability

**Metrics to Track:**

- Extraction accuracy (precision/recall per entity type)
- Processing speed (documents/hour)
- API usage per document
- Confidence score distributions
- Error rates by document type
- Cost per extraction

**Performance Monitoring:**

- Track processing time trends
- Detect accuracy degradation
- Monitor API usage spikes
- Alert on anomalies

**Error Alerting:**

- Error rates above 5% baseline
- API failures and timeouts
- Timeout clusters exceeding 10% of requests
- Model performance drops

**Quality Monitoring:**

- Confidence score drops
- Accuracy below thresholds
- Hallucination detection
- Entity resolution failures

**Resource Monitoring:**

- API quota usage
- Resource consumption trends
- Cost tracking per provider

**Integration Health:**

- Backend API connectivity
- Database write failures
- Event bus latency

**Source:** `AI-Development-Spec.md` lines 241-247

---

## Logging & Debugging

**Structured Logging:**

- JSON format with job_id, timestamp, stage, duration
- Log levels: DEBUG, INFO, WARN, ERROR
- Correlation IDs across services

**Debug Information:**

- Model responses (sampled or full)
- Confidence calculations
- Retry attempts and outcomes
- Processing decision trees

**Audit Trail:**

- All entity extraction decisions
- Relationship inference logic
- Confidence score changes
- Model version used per extraction

**Performance Logs:**

- API call timing
- Token usage per request
- Processing bottlenecks
- Cache hit rates

**Error Context:**

- Full error details with stack traces
- Input data samples (sanitized)
- System state at error time
- Suggested remediation steps

**Source:** `AI-Development-Spec.md` lines 248-254

---

## Success Criteria by Phase

### Phase 3 Success - MVP

**Functional:**

- Extract 5 core entity types with 80% accuracy
- Process 100 documents per hour
- Basic confidence scoring (high/medium/low)
- Integration with Backend pipeline

**Cost:**

- $0.10 average cost per document

**Deliverables:**

- 15-page technical comparison report
- Working prototype on 50 test documents
- Performance analysis with accuracy/efficiency curves
- Architecture recommendation with library choices

**Source:** `AI-Development-Spec.md` lines 256-262

---

### Phase 4 Success - Enhancement

**Functional:**

- Advanced entity extraction with 90% accuracy
- Relationship extraction with 80% accuracy
- Multi-model ensemble approach
- Fine-tuning pipeline operational
- Streaming processing for real-time extraction
- Automated quality monitoring dashboard

**Cost:**

- $0.07 per document (30% reduction from Phase 3)

**Source:** `AI-Development-Spec.md` lines 277-285

---

### Phase 5 Success - Production

**Functional:**

- 95% extraction accuracy on core entities
- 85% accuracy on relationships
- Process 1000 documents per hour (10x Phase 3)
- Granular confidence scores (0-100 scale)
- Handle 10+ entity types
- Self-improving through feedback loops

**Cost:**

- $0.05 average cost per document (50% reduction from Phase 3)

**Source:** `AI-Development-Spec.md` lines 286-294

---

## API Endpoints (MVP)

### 1. Extract Entities
```
POST /api/extract
{
  "text": "YouTube announced a new $100M creator fund...",
  "source_id": 123
}

Response:
{
  "entities": [
    {"name": "YouTube", "type": "platform", "confidence": 0.95},
    {"name": "creator fund", "type": "grant", "confidence": 0.87}
  ],
  "relationships": [
    {"from": "YouTube", "to": "creator fund", "type": "offers"}
  ]
}
```

### 2. Generate Embeddings
```
POST /api/embed
{"text": "content to embed"}

Response:
{"embedding": [0.1, 0.2, ...]}  # 384 or 768 dimensions
```

### 3. Summarize Content
```
POST /api/summarize
{"text": "long article text..."}

Response:
{"summary": "YouTube launches $100M creator fund..."}
```

**Source:** `PRD.md` lines 40-70

---

## Tech Stack (Decided)

**Core:**

- Python 3.11
- FastAPI (async API framework)
- Docker (containerization)

**AI/ML:**

- spaCy (local NER)
- OpenAI API (GPT-4 for complex extraction)
- Anthropic API (Claude for alternatives)
- LangChain/LlamaIndex (RAG framework - TBD)

**Supporting:**

- Pydantic (data validation)
- pytest (testing)
- structlog (structured logging)

**Source:** `PRD.md` lines 32-39

---

## Sources

- `docs/modules/ai-development/AI-Development-Spec.md` - Primary specification
- `docs/modules/ai-development/PRD.md` - MVP implementation plan
- `docs/team/module-assignments/ai-development/01-work-description.md` - Module boundaries and coordination
