---
marp: true
theme: peermesh
paginate: true
size: 16:9
---

# AI Module Architecture Review

### **Knowledge Graph Lab - AI Module**

**Date**: November 13, 2025

**Purpose**: Architecture Deep Review & Implementation Planning

---

## Executive Summary

**Phase 1 Complete:** Architecture deep review with gap analysis

**Deliverables:**
- Gap Analysis: 102 concerns evaluated across 10 categories
- Gap Prioritization: Top 30 critical gaps ranked
- Deployment & Infrastructure: Complete Docker + database setup
- Security & Access Control: JWT auth + TLS + RBAC
- Monitoring & Observability: Prometheus + Grafana + logging
- Error Handling & Resilience: Retry + circuit breakers + fallback
- Architectural Decision Records: 7 major decisions documented

**Status:** Ready for implementation

---

## Architecture Coverage - Before & After

### Before Deep Review (27% Coverage)
- ✅ Entity extraction algorithms (well specified)
- ✅ Research orchestration (comprehensive)
- ✅ GraphRAG portability (detailed)
- ❌ Deployment infrastructure (85% missing)
- ❌ Security & access control (92% missing)
- ❌ Monitoring & observability (85% missing)

### After Phase 1 + Phase 2 (75% Coverage)
- ✅ All production blockers resolved (10 CRITICAL gaps)
- ✅ All important operational gaps resolved (11 P1 gaps)
- ✅ Implementation-ready specifications (2,000+ lines)

---

## AI Pipeline Overview

**8-Layer Autonomous System:**

1. **User Query Processing** - FastAPI endpoints
2. **Gap Detection** - Knowledge graph analysis
3. **Research Orchestration** - Multi-agent coordination
4. **Document Ingestion** - Web/PDF/API fetching
5. **Entity Extraction** - LLM-powered NER
6. **Relationship Extraction** - Graph construction
7. **Knowledge Graph Merge** - Conflict resolution
8. **Query Re-execution** - Enriched results

---

## Pipeline Step 1: User Query Processing

**Purpose:** Accept and validate user queries

**Components:**
- FastAPI REST API endpoints
- Request validation (Pydantic models)
- Authentication (JWT tokens)
- Rate limiting (Redis-based)

**Inputs:** User query + context
**Outputs:** Validated request → Gap Detector

**Metrics:**
- Request rate: `http_requests_total`
- Latency (p95): `http_request_duration_seconds`
- Error rate: `http_requests_total{status=~"5.."}`

---

## Pipeline Step 2: Gap Detection

**Purpose:** Identify missing knowledge in graph

**Algorithm:**
1. Parse query into semantic components
2. Query knowledge graph for entities/relationships
3. Calculate confidence scores for matches
4. Flag low-confidence areas as gaps

**Gap Types:**
- Missing entities (person, org, concept not in graph)
- Missing relationships (connection not documented)
- Outdated information (data > 90 days old)

**Outputs:** Gap report → Research Orchestrator

---

## Pipeline Step 3: Research Orchestration

**Purpose:** Plan and coordinate research tasks

**Components:**
- Research Task Generator (LLM-powered)
- Agent Dispatcher (parallel execution)
- Progress Tracker (Redis state)

**Research Strategies:**
- Web search (DuckDuckGo, Bing API)
- Academic papers (arXiv, PubMed)
- Documentation (ReadTheDocs, GitHub)
- API queries (REST, GraphQL)

**Outputs:** Research tasks → Document Ingestion

**Metrics:**
- Tasks created: `research_tasks_total{task_type}`
- Success rate: `research_tasks_total{status="success"}`

---

## Pipeline Step 4: Document Ingestion

**Purpose:** Fetch and process documents from sources

**Supported Formats:**
- Web pages (HTML → Markdown)
- PDFs (PyPDF2, pdfplumber)
- APIs (JSON, XML)
- RSS feeds (feedparser)

**Processing Steps:**
1. Fetch raw content (with retry + timeout)
2. Extract text (format-specific parsers)
3. Clean and normalize (remove boilerplate)
4. Chunk for processing (max 4000 tokens)

**Outputs:** Processed documents → Entity Extraction

**Metrics:**
- Documents ingested: `documents_ingested_total{source_type, status}`

---

## Pipeline Step 5: Entity Extraction

**Purpose:** Extract named entities from documents

**LLM Providers (with automatic fallback):**
1. Anthropic Claude 3 Sonnet (primary)
2. OpenAI GPT-4 Turbo (fallback 1)
3. Cohere Command (fallback 2)
4. Local Llama 3 (fallback 3 - always available)

**Entity Types:**
- Person, Organization, Location
- Concept, Technology, Method
- Event, Date, Measurement

**Quality Assurance:**
- Confidence scores (0.0-1.0)
- Multi-pass extraction (verify with second LLM)
- Human review queue (low confidence < 0.7)

---

## Pipeline Step 6: Relationship Extraction

**Purpose:** Identify relationships between entities

**Relationship Types:**
- `WORKS_FOR` (Person → Organization)
- `LOCATED_IN` (Organization → Location)
- `INVENTED_BY` (Technology → Person)
- `RELATED_TO` (Concept → Concept)
- Custom types (domain-specific)

**Extraction Methods:**
- Dependency parsing (spaCy)
- LLM-based extraction (prompt engineering)
- Pattern matching (regex + rules)

**Outputs:** Entity-relationship triples → Knowledge Graph

---

## Pipeline Step 7: Knowledge Graph Merge

**Purpose:** Merge new knowledge into existing graph

**Merge Stages:**
1. **Normalization** - Canonical entity names
2. **Entity Resolution** - Deduplicate entities
   - Exact match (name + type)
   - Fuzzy match (Levenshtein distance)
   - Semantic match (embedding similarity)
   - LLM-based disambiguation
3. **Conflict Resolution** - Handle contradictions
   - By recency (prefer newer data)
   - By confidence (prefer higher confidence)
   - By source quality (trusted sources win)
4. **Provenance Tracking** - Record data lineage

**Outputs:** Updated knowledge graph

---

## Pipeline Step 8: Query Re-execution

**Purpose:** Answer original query with enriched knowledge

**Process:**
1. Re-run query against updated knowledge graph
2. Generate comprehensive answer (LLM synthesis)
3. Cite sources (provenance links)
4. Return to user with confidence score

**Response Format:**
```json
{
  "answer": "...",
  "confidence": 0.92,
  "entities": [...],
  "sources": [...],
  "research_conducted": true
}
```

---

## Deployment Architecture

**Docker Compose (Local Development):**
- 6 services: app, postgres, neo4j, qdrant, redis, grafana
- Hot-reload enabled
- Seeded test data
- Health checks on all services

**Kubernetes (Production):**
- Horizontal pod autoscaling (2-10 replicas)
- Rolling updates (zero downtime)
- Secrets via Vault integration
- TLS termination (Nginx ingress)

**Databases:**
- PostgreSQL 16.1 (structured data, JSONB)
- Neo4j 5.14.0 (knowledge graph, Cypher)
- Qdrant 1.7.0 (vector embeddings, HNSW)

---

## Security Architecture

**Authentication:**
- JWT tokens (HS256, 1-hour expiration)
- Refresh tokens (30-day expiration)
- API keys (bcrypt hashed, rate limited)

**Authorization:**
- RBAC with 4 roles: admin, user, readonly, api_consumer
- 12 permissions: entity:read, entity:create, etc.
- Decorator-based enforcement

**Encryption:**
- TLS 1.2+ (Nginx reverse proxy)
- HSTS headers (force HTTPS)
- Encryption at rest (PostgreSQL SSL, Fernet for secrets)

**Compliance:**
- OWASP Top 10 (2021) coverage
- GDPR data protection
- Audit logging (all sensitive operations)

---

## Monitoring & Observability

**Metrics (Prometheus):**
- Infrastructure: CPU, memory, disk, network
- Application: Request rate, latency, errors (RED method)
- LLM: Tokens used, cost, provider success rate
- Business: Entities extracted, queries processed

**Dashboards (Grafana):**
- System Overview (request rate, latency, errors)
- LLM Operations (provider performance, cost tracking)
- Knowledge Graph Growth (nodes, edges over time)

**Logging (JSON structured):**
- Correlation IDs (trace request flow)
- Contextual data (user_id, request_id)
- Log aggregation (Loki)

---

## Error Handling & Resilience

**Retry Logic:**
- Exponential backoff (1s, 2s, 4s, 8s, 16s)
- Jitter (prevent thundering herd)
- Max attempts: 5 (external APIs), 3 (databases)

**Circuit Breakers:**
- Per-provider breakers (OpenAI, Anthropic, etc.)
- States: CLOSED → OPEN → HALF_OPEN → CLOSED
- Open after 5 failures, test recovery after 60s

**LLM Fallback Chain:**
- Claude → GPT-4 → Cohere → Local LLM
- Automatic failover on provider outage
- Cost optimization (use cheaper models when possible)

---

## Data Backup & Recovery

**Backup Strategy:**
- Daily full backups (PostgreSQL, Neo4j, Qdrant)
- 30-day retention
- Automated via cron jobs
- Off-site storage (S3/GCS)

**Recovery Targets:**
- RTO (Recovery Time Objective): < 15 minutes
- RPO (Recovery Point Objective): < 5 minutes

**Disaster Recovery:**
- Point-in-time recovery (PITR) for PostgreSQL
- Neo4j incremental backups
- Restore procedures documented and tested

---

## Architectural Decisions (ADRs)

**ADR-001:** Multi-Database Strategy
- PostgreSQL + Neo4j + Qdrant
- Each optimized for its workload

**ADR-002:** LLM Provider Strategy
- Multi-provider with automatic fallback
- Circuit breakers prevent cascade failures

**ADR-003:** Event-Driven Research Pipeline
- Redis Streams for async processing
- Decoupled stages, parallel execution

**ADR-004:** JWT Authentication
- Stateless, scalable
- Short-lived access tokens + long-lived refresh tokens

---

## Implementation Roadmap

### Phase 1: MVP Deployment (Weeks 1-4)
- Week 1: Deploy infrastructure (Docker + databases)
- Week 2: Implement entity extraction pipeline
- Week 3: Add monitoring and basic error handling
- Week 4: Integration testing and production deployment

### Phase 2: Production Hardening (Weeks 5-8)
- Week 5: Advanced error handling (circuit breakers, fallback)
- Week 6: Comprehensive monitoring (dashboards, alerts)
- Week 7: Performance optimization
- Week 8: Load testing and tuning

### Phase 3: Feature Expansion (Weeks 9-12)
- Additional entity types and relationship extraction
- Multi-language support
- Advanced search capabilities

---

## Cost Estimates

**LLM API Costs (per 1000 queries):**
- Entity extraction: $15-30 (Claude/GPT-4)
- Relationship extraction: $10-20
- Research generation: $5-10
- **Total: ~$30-60 per 1000 queries**

**Infrastructure Costs (monthly):**
- Compute: $200-500 (3-5 servers)
- Databases: $150-300 (managed services)
- Monitoring: $50-100 (Grafana Cloud optional)
- **Total: ~$400-900/month**

**Cost Optimization:**
- Use cheaper LLM models when quality permits
- Cache frequent queries (Redis)
- Batch processing for non-urgent requests

---

## Success Metrics

**Technical Metrics:**
- System uptime: 99.9% (43 min downtime/month)
- API latency (p95): < 2 seconds
- Error rate: < 0.1%
- LLM provider availability: 99.9%

**Business Metrics:**
- Entities extracted per day: Target 10,000+
- Knowledge graph growth: 1,000+ nodes/week
- User queries processed: 500+ per day
- Research tasks success rate: > 95%

**Quality Metrics:**
- Entity extraction F1 score: > 0.85
- Relationship extraction accuracy: > 0.80
- User satisfaction (query relevance): > 4.0/5.0

---

## Risks & Mitigation

**Risk 1:** LLM provider outages
- **Mitigation:** Multi-provider fallback chain

**Risk 2:** High LLM API costs
- **Mitigation:** Budget limits, model downgrade, caching

**Risk 3:** Data synchronization failures (multi-DB)
- **Mitigation:** Background sync jobs, monitoring, alerts

**Risk 4:** Knowledge graph data quality degradation
- **Mitigation:** Confidence scoring, human review queue

**Risk 5:** Scalability bottlenecks
- **Mitigation:** Horizontal scaling, caching, async processing

---

## Team Roles & Responsibilities

**Backend Engineer:**
- Implement FastAPI endpoints
- Database integration (PostgreSQL, Neo4j, Qdrant)
- Event pipeline (Redis Streams)

**AI/ML Engineer:**
- LLM integration and prompt engineering
- Entity/relationship extraction algorithms
- Model fallback and quality monitoring

**DevOps Engineer:**
- Docker + Kubernetes deployment
- Monitoring setup (Prometheus, Grafana)
- Backup/recovery procedures

**Product Manager:**
- Prioritize features
- Define success metrics
- User acceptance testing

---

## Open Questions for Discussion

1. **Deployment Timeline:** Start MVP implementation immediately or complete Phase 3 architecture (ADRs, schemas) first?

2. **LLM Provider Priority:** Which provider should be primary? Claude (quality) vs GPT-4 (speed)?

3. **Data Retention:** How long should we retain raw documents? Entity history?

4. **Human Review:** What confidence threshold requires human review? Who reviews?

5. **Cost Controls:** What's the maximum acceptable LLM cost per query?

---

## Next Steps - Decision Required

**Option A: Complete Remaining Architecture (2-3 weeks)**
- Document all remaining gaps (schemas, prompts, admin tools)
- 100% architecture coverage before implementation
- **Pros:** Comprehensive planning, fewer surprises
- **Cons:** Delays implementation, may over-specify

**Option B: Start Implementation Now (Recommended)**
- Begin with MVP deployment using Phase 1 + Phase 2 docs
- Iterate on architecture based on real-world learnings
- **Pros:** Faster time to value, validate assumptions
- **Cons:** May encounter unforeseen issues

**Option C: Hybrid Approach**
- Start MVP implementation
- Complete remaining architecture in parallel
- Integrate incrementally as architecture completes

---

## Resources & Documentation

**Architecture Documents (7 files, 5,000+ lines):**
- Gap Analysis: `.dev/ai/design/2025-11-13-AI-ARCHITECTURE-GAP-ANALYSIS.md`
- Gap Prioritization: `.dev/ai/design/2025-11-13-GAP-PRIORITIZATION.md`
- Deployment: `.dev/ai/design/2025-11-13-DEPLOYMENT-INFRASTRUCTURE-ARCHITECTURE.md`
- Security: `.dev/ai/design/2025-11-13-SECURITY-ACCESS-CONTROL-ARCHITECTURE.md`
- Monitoring: `.dev/ai/design/2025-11-13-MONITORING-OBSERVABILITY-ARCHITECTURE.md`
- Resilience: `.dev/ai/design/2025-11-13-ERROR-HANDLING-RESILIENCE-ARCHITECTURE.md`
- ADRs: `.dev/ai/design/2025-11-13-ARCHITECTURAL-DECISION-RECORDS.md`

**Sprint Bundle:**
- Location: `.dev/_sprint_ai_module_nov13/`
- Meeting handout: `README.md`

---

## Questions & Discussion

**Meeting Goal:** Make architectural decisions and plan implementation

**Key Decisions Needed:**
1. Which implementation path? (Option A/B/C)
2. LLM provider priorities and budget limits
3. MVP feature scope and timeline
4. Team assignments and responsibilities

<br>

**Ready to discuss architecture and plan next steps.**

---

## Thank You

**AI Module Architecture Review Complete**

Let's build something extraordinary together.

**Contact:** Architecture Team
**Next Meeting:** TBD (Post-decision)
