# Constraints - AI Module

**Distilled from:** AI-Development-Spec.md, PRD.md, work-description.md

**Date:** 2025-10-10

---

## Performance Constraints

### Accuracy Requirements

**Entity Extraction Targets:**
| Phase | Precision | Recall | Cost/Document |
|-------|-----------|--------|---------------|
| Phase 3 (MVP) | 80% | 75% | $0.10 |
| Phase 4 (Enhanced) | 90% | 85% | $0.07 |
| Phase 5 (Production) | 95% | 85% | $0.05 |

**Relationship Extraction Targets:**
| Phase | Precision | Notes |
|-------|-----------|-------|
| Phase 4 | 80% | Relationship identification begins |
| Phase 5 | 85% | Production-grade relationship accuracy |

**Rationale:** These targets balance accuracy with cost. Phase 3 focuses on proving value, Phase 4 on quality improvements, Phase 5 on production excellence.

**Source:** `AI-Development-Spec.md` lines 13-20, 256-294

---

### Throughput Requirements

**Processing Speed Targets:**
| Phase | Documents/Hour | Improvement Factor |
|-------|----------------|-------------------|
| Phase 3 | 100 | Baseline (1x) |
| Phase 4 | 500 | 5x improvement |
| Phase 5 | 1000 | 10x improvement |

**Constraints:**

- Must process documents within SLA timeframes
- Cannot exceed daily processing quotas
- Must handle traffic spikes (2x baseline)

**Bottlenecks:**

- LLM API rate limits (60 requests/minute typical)
- Network latency to external APIs (100-500ms per call)
- Token processing limits (varies by model)

**Source:** `AI-Development-Spec.md` lines 269-291

---

### Latency Requirements

**Response Time Targets:**

- **Synchronous Extraction:** < 2 seconds per document (goal)
- **Batch Processing:** < 5 minutes per batch (100 documents)
- **Report Generation:** < 10 minutes per report
- **Embedding Generation:** < 1 second per document

**User Experience Impact:**

- Frontend queries need sub-second responses
- Publishing needs reports within digest window (30 minutes)
- Real-time extraction for urgent content

**Source:** `ai-publishing-integration.md` lines 178-181

---

## Cost Constraints

### Budget Limits

**API Cost Targets:**
| Provider | Phase 3 Target | Phase 5 Target | Reduction |
|----------|----------------|----------------|-----------|
| OpenAI GPT-4 | $0.10/doc | $0.05/doc | 50% |
| Overall Average | $0.10/doc | $0.05/doc | 50% |

**Daily Budget Caps:**

- Development: $50/day
- Staging: $200/day
- Production: $1000/day (scales with usage)

**Cost Optimization Strategies:**

- Use cheaper models for simple tasks
- Implement aggressive caching
- Batch API calls where possible
- Use local models (spaCy) for basic NER
- Prompt optimization to reduce tokens

**Source:** `AI-Development-Spec.md` lines 264-291, 307-313

---

### Token Usage Limits

**LLM Provider Limits:**

- **OpenAI GPT-4:** 8k context window (GPT-4 Turbo: 128k)
- **Anthropic Claude:** 100k context window
- **Rate Limits:** 60-200 requests/minute (varies by tier)

**Document Chunking Required:**

- Documents > 2000 tokens must be split
- Maintain context across chunks
- Reassemble results coherently

**Prompt Engineering:**

- Keep prompts concise to save tokens
- Balance detail vs. cost
- A/B test prompt efficiency

**Source:** `AI-Development-Spec.md` lines 44, 226-233

---

## Timeline Constraints

### Development Timeline

**Total Effort:** 100 hours (12 weeks)

**Phase Breakdown:**
| Phase | Duration | Focus | Key Milestones |
|-------|----------|-------|----------------|
| Phase 1 | Weeks 1-6 | Mock Implementation | Docker setup, API with mocks, testing infrastructure |
| Phase 2 | Weeks 7-10 | Real AI Integration | OpenAI API, entity extraction, relationship mapping |
| Phase 3 | Weeks 11-12 | Demo Prep | Integration testing, optimization, demo preparation |

**Phase 1 Details (Weeks 1-6):**

- Week 1-2: Setup (Docker, FastAPI, mock system)
- Week 3-4: Mock logic (entity detector, mock database)
- Week 5-6: Enhanced mocks (relationships, summarization)

**Phase 2 Details (Weeks 7-10):**

- Week 7-8: Real AI integration (OpenAI API, testing)
- Week 9-10: Optimization (prompt improvement, caching, cost reduction)

**Constraint Impact:**

- Limited time for experimentation
- Must prioritize MVP features
- Mock-first enables parallel Backend work

**Source:** `PRD.md` lines 8, 19-31, 72-107

---

### Delivery Milestones

**Phase 3 Deliverables (MVP):**

- 15-page technical comparison report
- Working prototype on 50 test documents
- Performance analysis with accuracy curves
- Architecture recommendation

**Phase 4 Deliverables (Enhanced):**

- Advanced entity extraction operational
- Relationship extraction with confidence
- Multi-model ensemble working
- Automated quality dashboard

**Phase 5 Deliverables (Production):**

- 95% accuracy achieved
- 1000 docs/hour throughput
- Self-improving system active
- Complete monitoring suite

**Source:** `AI-Development-Spec.md` lines 256-294

---

## Scope Constraints

### Module Boundaries - What AI OWNS

**In Scope:**

- Entity extraction and relationship mapping
- Confidence score generation
- AI/ML pipeline processing
- News report generation
- Structured data output
- Prompt engineering and optimization
- Model selection and management

**Deliverables:**

- Extracted entities with types and confidence
- Relationships between entities
- Document embeddings (768-1536 dimensions)
- Processing status updates
- News reports with metadata
- Quality metrics and monitoring data

**Source:** `AI-Development-Spec.md` lines 110-117

---

### Module Boundaries - What AI DOES NOT OWN

**Out of Scope:**

- **Data Fetching:** Backend fetches from sources (not AI)
- **Database Storage:** Backend stores extracted data (not AI)
- **User Interface:** Frontend displays results (not AI)
- **Content Distribution:** Publishing sends insights (not AI)
- **Infrastructure Deployment:** Backend handles servers (not AI)
- **Vector Database Management:** Backend owns vector DB (not AI)
- **Graph Visualization:** Frontend creates visual displays (not AI)
- **Email Generation:** Publishing handles email composition (not AI)

**Rationale for Boundaries:**

- Clear separation enables parallel development
- Prevents scope creep and overlap
- Maintains loose coupling between services
- Each module can scale independently

**Integration Points:**

- AI receives documents from Backend
- AI sends results to Backend
- Frontend queries Backend (not AI directly)
- Publishing queries Backend (not AI directly)

**Source:** `AI-Development-Spec.md` lines 118-124, `work-description.md` lines 49-63

---

## Resource Constraints

### Infrastructure Limits

**Development Environment:**

- Local Docker containers
- Limited CPU/memory on developer machines
- No GPU access (use cloud APIs)

**Staging Environment:**

- Kubernetes cluster (shared)
- 4 CPU cores, 16GB RAM per pod
- Limited to 3 replicas

**Production Environment:**

- Kubernetes cluster (dedicated)
- Auto-scaling 2-20 replicas
- 8 CPU cores, 32GB RAM per pod
- GPU access for embeddings (optional)

**Source:** Implied by containerization approach

---

### API Rate Limits

**External API Constraints:**
| Provider | Free Tier | Paid Tier | Rate Limit |
|----------|-----------|-----------|------------|
| OpenAI | No free tier | Pay-as-you-go | 60-200 req/min |
| Anthropic | Limited free | Pay-as-you-go | 50-100 req/min |
| Pinecone | 1 index free | $70+/month | 100-1000 req/sec |

**Mitigation Strategies:**

- Implement request queuing
- Use exponential backoff on rate limit errors
- Distribute load across multiple API keys
- Cache aggressively to reduce API calls
- Use local models for simple tasks

**Source:** `AI-Development-Spec.md` lines 226-233, 307-313

---

### Processing Quotas

**Daily Limits:**

- **API Calls:** Based on budget cap ($1000/day = ~10,000 docs at $0.10/doc)
- **Token Usage:** Track and alert at 80% of daily quota
- **Storage:** No hard limits but monitor growth

**Monthly Limits:**

- **API Budget:** $30,000/month for production
- **Storage:** 1TB for vectors, 100GB for reports

**Monitoring Required:**

- Real-time usage tracking
- Alert at 70%, 85%, 95% of quota
- Auto-throttle at 98% to prevent overrun

**Source:** `AI-Development-Spec.md` lines 231

---

## Data Constraints

### Input Format Requirements

**Supported Formats:**

- HTML (primary)
- PDF (secondary)
- Plain text (tertiary)
- JSON (structured data)

**Language Support:**

- English (primary, 95% accuracy target)
- Spanish (secondary, 85% accuracy target)
- French (tertiary, 85% accuracy target)

**Document Size Limits:**

- Maximum: 100,000 tokens (chunking required above 2000)
- Minimum: 100 tokens (below this, quality degrades)
- Optimal: 1000-5000 tokens

**Unsupported Formats:**

- Images (no OCR in Phase 3-4)
- Audio/Video transcripts (Phase 5+)
- Scanned PDFs (no OCR in Phase 3-4)

**Source:** `AI-Development-Spec.md` lines 307-313

---

### Data Quality Requirements

**Input Quality:**

- Must be UTF-8 encoded
- HTML must be valid (or parseable)
- PDFs must have extractable text
- No corrupted or malformed content

**Output Quality:**

- All entities must have confidence scores
- All relationships must reference valid entities
- JSON output must be schema-compliant
- Reports must pass grammar/style checks

**Validation Rules:**

- Dates must be valid ISO-8601
- Amounts must be positive numbers
- Names must not be empty
- URLs must be properly formatted

**Source:** `AI-Development-Spec.md` lines 103-109

---

## Technical Constraints

### Model Selection Constraints

**Available Models:**
| Model | Pros | Cons | Use Case |
|-------|------|------|----------|
| GPT-4 | Highest accuracy | Most expensive ($0.03/1k tokens) | Complex extraction |
| GPT-3.5 | Good balance | Medium cost ($0.001/1k tokens) | Standard extraction |
| Claude | Large context (100k) | Rate limits | Long documents |
| spaCy | Free, fast | Lower accuracy | Simple NER |
| Llama | Self-hosted | Setup complexity | Cost-sensitive ops |

**Selection Criteria:**

- Cost vs. accuracy tradeoffs
- Context window requirements
- Rate limit availability
- Response time needs

**Source:** `AI-Development-Spec.md` lines 35-40, `work-description.md` lines 176-180

---

### Integration Constraints

**Backend Dependencies:**

- Requires job queue (RabbitMQ) operational
- Needs vector database (Pinecone/Qdrant) deployed
- Depends on graph database (Neo4j) running
- Requires Redis for caching

**API Contract Constraints:**

- Must adhere to agreed JSON schemas
- Cannot change response format without versioning
- Must maintain backward compatibility
- Health check endpoints required

**Event Schema Constraints:**

- Events must follow CloudEvents spec
- Correlation IDs required for tracing
- Timestamps must be ISO-8601 UTC

**Source:** `AI-Development-Spec.md` lines 126-167

---

## Coordination Constraints

### Team Dependencies

**With Backend Architecture Team:**

- **Timing:** Early coordination required
- **Dependencies:**
  - Vector database connection details
  - Job queue infrastructure
  - Storage API endpoints
- **Blockers:** AI cannot start until queue operational

**With Frontend Design Team:**

- **Timing:** Mid-project coordination
- **Dependencies:**
  - Result data structure requirements
  - Streaming protocol needs
  - Display format specifications
- **Blockers:** Minor (can mock frontend needs)

**With Publishing Tools Team:**

- **Timing:** Phase 3-4 priority
- **Dependencies:**
  - Report format specifications
  - Personalization requirements
  - Distribution timing needs
- **Blockers:** Reports can be generated without Publishing

**Source:** `work-description.md` lines 65-123

---

### Communication Constraints

**Meeting Requirements:**

- Daily standups: 10 AM via Discord
- Weekly sync with Backend team
- Bi-weekly demos to stakeholders
- Code reviews within 24 hours

**Documentation Requirements:**

- API changes must be documented before implementation
- Prompt templates must be versioned
- Model selection logic must be explained
- Confidence calculations must be documented

**Source:** `work-description.md` lines 217-222

---

## Quality Constraints

### Accuracy Thresholds

**Minimum Viable Accuracy:**

- Entity extraction: 80% precision (Phase 3)
- Relationship extraction: 75% precision (Phase 4)
- Below these thresholds: System not ready for users

**Confidence Calibration:**

- High confidence (≥85): Should be 90%+ accurate
- Medium confidence (70-84): Should be 75-85% accurate
- Low confidence (<70): Should be flagged for review

**Validation Method:**

- Manual review of random sample (100 documents)
- Precision/recall calculation
- Confusion matrix analysis
- Regular recalibration (monthly)

**Source:** `AI-Development-Spec.md` lines 21-28, 256-262

---

### Hallucination Prevention

**Constraints:**

- Hallucination rate must be < 5% (Phase 5)
- High-confidence extractions must cite source positions
- Synthetic entities must be flagged
- Contradictory information must be reconciled

**Detection Methods:**

- Cross-reference with source text
- Entity grounding in original document
- Relationship validation against known facts
- User feedback loop for corrections

**Source:** Implied by quality requirements

---

## Operational Constraints

### Deployment Constraints

**Rollback Requirements:**

- Must maintain 3 previous model versions
- One-click rollback capability < 2 minutes
- Gradual traffic shifting (10% → 50% → 100%)
- Automated health checks during deployment

**Testing Requirements:**

- Integration tests must pass before deployment
- A/B testing on 10% traffic for new models
- Performance benchmarks must not regress
- Cost per document must not exceed targets

**Source:** `AI-Development-Spec.md` lines 295-302

---

### Monitoring Constraints

**Required Metrics:**

- Extraction accuracy (by entity type)
- Processing speed (docs/hour)
- API cost per document
- Error rate by type
- Confidence score distribution

**Alert Thresholds:**

- Error rate > 5%: Page on-call engineer
- Accuracy drop > 5%: Email team lead
- Cost per doc > target: Alert finance
- Queue depth > 1000: Auto-scale

**Retention:**

- Metrics: 90 days (Prometheus)
- Logs: 30 days (Elasticsearch)
- Traces: 7 days (Jaeger)

**Source:** `AI-Development-Spec.md` lines 241-254

---

## Compliance Constraints

### Data Privacy

**Requirements:**

- Must not log PII in plain text
- API keys must be encrypted at rest
- Sensitive entities must be redacted in logs
- GDPR compliance for EU users (future)

**Handling:**

- Detect and redact: emails, phone numbers, addresses
- Hash user IDs in logs
- Encrypt data in transit (TLS 1.3)
- No persistent storage of raw documents

**Source:** Implied by general security best practices

---

### Model Bias

**Constraints:**

- Must test for demographic bias in entity extraction
- Avoid over-representation of certain entity types
- Balance training data across domains
- Regular bias audits (quarterly)

**Mitigation:**

- Diverse training data
- Fairness metrics tracking
- User feedback for bias reporting
- Model fine-tuning to reduce bias

**Source:** Implied by AI ethics requirements

---

## Summary of Critical Constraints

**Must-Have (Phase 3):**

- ✅ 80% entity extraction accuracy
- ✅ 100 docs/hour throughput
- ✅ $0.10 cost per document
- ✅ Clear module boundaries maintained
- ✅ 100-hour development timeline met

**Must-Have (Phase 5):**

- ✅ 95% entity extraction accuracy
- ✅ 85% relationship extraction accuracy
- ✅ 1000 docs/hour throughput
- ✅ $0.05 cost per document
- ✅ < 5% hallucination rate

**Cannot Compromise:**

- Module boundaries (no scope creep)
- Data privacy (no PII leaks)
- API contract compatibility (no breaking changes)
- Budget limits (no overruns)

---

## Sources

- `docs/modules/ai-development/AI-Development-Spec.md` - Performance targets, module boundaries, quality requirements
- `docs/modules/ai-development/PRD.md` - Timeline, tech stack, implementation approach
- `docs/team/module-assignments/ai-development/01-work-description.md` - Scope boundaries, team coordination
- `docs/design/system/ai-publishing-integration.md` - Integration constraints
