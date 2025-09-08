---
title: "Project Style Guide (v3.0)"
status: "Draft"
updated: 2025-09-09
owner: "@docs-wg"
applies_to: ["Agents","Interns","PMs","Execs"]
version: "v3.0"
doc_id: "styleguide-v3"
tags: ["documentation","standards","guidelines"]
related: ["./glossary.md","./research-brief-template.md"]
---

<a id="sg-exec-summary"></a>
## Executive Summary

This guide ensures consistent, high-quality documentation across Knowledge Graph Lab by establishing prescriptive rules for planning, writing, and reviewing technical content. It enables multiple humans and AI agents to work in parallel without conflicts through deterministic naming, stable anchors, and clear ownership boundaries. The guide applies to all Markdown files in this repository—specifications, research briefs, PRDs, RFCs, meeting notes, and guides. Every contributor must follow these rules to maintain clarity, accessibility, and merge safety. Version 3.0 adds enhanced parallel-work protocols, AI collaboration guidelines, quality metrics, and expanded templates for research documentation.

<a id="sg-core-principles"></a>
## Core Principles

1. **Clarity over cleverness**: Choose simple, direct language that a college junior can understand
2. **Evidence-based writing**: Support every claim with data, examples, or citations
3. **Single source of truth**: Each fact lives in exactly one canonical location
4. **Deterministic structure**: File names, anchors, and sections follow predictable patterns
5. **Progressive complexity**: Start simple, add detail gradually, never jump to advanced concepts
6. **Accessibility by default**: Screen-reader friendly, mobile-responsive, WCAG 2.1 AA compliant
7. **Parallel-safe authoring**: Multiple contributors can work simultaneously without conflicts
8. **Measurable quality**: Track readability scores, link health, and review velocity

<a id="sg-authoring-rules"></a>
## Authoring Rules

### Rule 1: Voice and Tone
**Why**: Consistent voice reduces cognitive load and builds trust.  
**How**: Use second person ("you") for instructions, third person for descriptions.  
**Good**: "The ingestion module processes 1,000 documents per hour. To increase throughput, you can adjust the batch size."  
**Bad**: "One might observe that we could potentially enhance performance if they modified parameters."

### Rule 2: Active Voice Requirement
**Why**: Active voice clarifies responsibility and reduces word count by 15-20%.  
**How**: Subject performs action on object. Agent before action.  
**Good**: "Module 1 validates input, then sends entities to Module 2."  
**Bad**: "Input is validated and entities are sent by the system."

### Rule 3: Present Tense for Systems
**Why**: Systems exist now (even if incomplete). Past tense is only for decisions already made.  
**How**: Describe current/planned behavior in present tense. Use past for historical context.  
**Good**: "The API returns 429 when rate-limited." / "We chose PostgreSQL after benchmarking three databases."  
**Bad**: "The API would return 429." / "We are choosing PostgreSQL."

### Rule 4: Inclusive Language Mandate
**Why**: Professional documentation respects all readers and avoids alienating terminology.  
**How**: Gender-neutral pronouns, culturally neutral examples, accessible color descriptions.  
**Good**: "The developer configures their environment" / "Primary database" / "Status: green (success)"  
**Bad**: "The developer configures his environment" / "Master database" / "Status: green" (only)

### Rule 5: Acronym Definition Protocol
**Why**: Undefined acronyms block comprehension for 40% of readers (internal survey data).  
**How**: Spell out on first use with acronym in parentheses. Add to glossary.  
**Good**: "Knowledge Graph Lab (KGL) uses Retrieval-Augmented Generation (RAG)..."  
**Bad**: "KGL uses RAG..." (without prior definition)

### Rule 6: Concrete Examples Required
**Why**: Abstract descriptions have 3x higher clarification requests than concrete examples.  
**How**: Every concept gets a real-world example within two paragraphs.  
**Good**: "Entity resolution merges duplicates. For example, 'NYC', 'New York City', and 'New York, NY' resolve to entity `e_nyc_001`."  
**Bad**: "Entity resolution merges similar items when appropriate."

### Rule 7: Visual Content Standards
**Why**: Diagrams improve comprehension by 60% but require accessibility support.  
**How**: All images need alt text, captions, and text references. Diagrams use mermaid when possible.  
**Good**: "Figure 1 shows the three-layer architecture (see Figure 1). Alt: Diagram showing API, Logic, and Data layers."  
**Bad**: "As shown below:" (no caption, no alt text)

### Rule 8: Citation Requirements
**Why**: Unsourced claims reduce document credibility and block verification.  
**How**: Use numbered footnotes for sources. Link to primary sources when available.  
**Good**: "We achieve 95% accuracy using BERT embeddings[^1]." / [^1]: Devlin et al., "BERT: Pre-training of Deep Bidirectional Transformers", 2018.  
**Bad**: "We achieve high accuracy using modern techniques."

### Rule 9: Paragraph Structure Formula
**Why**: Consistent structure improves scanning speed by 25%.  
**How**: 3-4 sentences max. Topic sentence, evidence/explanation, connection to context.  
**Good**: "Module 2 stores entities in Neo4j. This graph database enables efficient path queries and relationship traversal. The choice supports our need for flexible schema evolution."  
**Bad**: 7-sentence paragraph mixing three different topics.

### Rule 10: Progressive Disclosure Pattern
**Why**: Readers abandon documents that start with complex details (70% bounce rate).  
**How**: Overview → Core concepts → Implementation → Edge cases → Advanced topics.  
**Good**: "What is X?" → "Why use X?" → "How X works" → "Configuring X" → "Troubleshooting X"  
**Bad**: Starting with configuration parameters before explaining the purpose.

### Rule 11: Numeric Precision Standards
**Why**: Inconsistent number formatting causes misinterpretation of magnitudes.  
**How**: Words for 0-9, numerals for 10+. Always include units and precision. UTC for times.  
**Good**: "Process five files in 12 seconds (±0.5s). Deployment at 14:00 UTC."  
**Bad**: "Process 5 files in about twelve seconds. Deploy this afternoon."

### Rule 12: No Unexplained Magic
**Why**: Vague automation claims hide critical assumptions and failure modes.  
**How**: Specify algorithms, thresholds, retry logic, and fallback behavior.  
**Good**: "Auto-retry failed requests 3 times with exponential backoff (2s, 4s, 8s), then dead-letter queue."  
**Bad**: "The system automatically handles failures."

### Rule 13: Cross-Reference Protocol
**Why**: Broken links waste 5 minutes per reader per incident.  
**How**: Use relative paths and stable anchors. Verify links before commit.  
**Good**: `See [Data Model](./project-design/data-model.md#dm-entities)`  
**Bad**: `See the data model doc` (no link) or `/full/absolute/path`

### Rule 14: Version Documentation Requirements
**Why**: Undocumented changes cause integration failures and confusion.  
**How**: Every breaking change needs migration guide. Deprecation requires 2-version notice.  
**Good**: "v2.0 changes: Field `name` split into `first_name` and `last_name`. Migration: [script](./migrations/v2.md)"  
**Bad**: "Some fields changed in v2.0."

### Rule 15: Error Message Standards
**Why**: Poor error messages account for 30% of support tickets.  
**How**: State what happened, why, and how to fix it. Include error codes.  
**Good**: "Error E1234: Rate limit exceeded (50 requests/minute). Wait 30 seconds or upgrade plan."  
**Bad**: "Request failed."

<a id="sg-tech-markdown"></a>
## Tech Markdown Conventions

### Heading Hierarchy
- **H1 (`#`)**: Exactly one per file—the document title
- **H2 (`##`)**: Major sections with stable anchor IDs
- **H3 (`###`)**: Subsections within major sections  
- **H4 (`####`)**: Rarely used, only for minor subdivisions
- **Never use H5+ (`#####`)**: Restructure content instead

### List Formatting
```markdown
# Ordered (sequential steps)
1. First step with clear action
2. Second step building on first
3. Final verification step

# Unordered (parallel items)
- Independent point one
- Independent point two
  - Nested detail (max 2 levels)
  - Another nested detail
- Independent point three
```

### Code Block Standards
````markdown
```python
# Purpose: Calculate entity similarity score
def calculate_similarity(entity_a: str, entity_b: str) -> float:
    """Calculate Levenshtein distance normalized to 0-1."""
    distance = levenshtein(entity_a, entity_b)
    max_len = max(len(entity_a), len(entity_b))
    return 1.0 - (distance / max_len)
```

```json
// Example: Entity resolution request payload
{
  "entities": [
    {"id": "e_001", "name": "New York City", "type": "location"},
    {"id": "e_002", "name": "NYC", "type": "location"}
  ],
  "threshold": 0.85,
  "algorithm": "levenshtein"
}
```
````

### Table Requirements
```markdown
| Column 1 | Column 2 | Column 3 |
| :------- | :------: | -------: |
| Left-aligned | Centered | Right-aligned |
| Text content | Status | 123 |
| More text | Active | 456 |

Note: Tables must have headers and use proper alignment syntax
```

### Callout Syntax (GitHub Alerts)
```markdown
> [!NOTE]
> Helpful information that users should know.

> [!TIP]
> Optional advice to improve outcomes.

> [!IMPORTANT]
> Essential information for success.

> [!WARNING]
> Critical issue that could cause problems.

> [!CAUTION]
> Dangerous action that could cause data loss or system failure.
```

### Link Standards
```markdown
# Inline links (for single use)
Check the [API documentation](./api-docs.md).

# Reference links (for multiple uses)
Review the [style guide][style] and [glossary][gloss].
The [style guide][style] contains all rules.

[style]: ./STYLEGUIDE-v3.md "Style Guide v3"
[gloss]: ./glossary.md "Project Glossary"

# Anchor links
See [Authoring Rules](#sg-authoring-rules) above.
```

### Footnote Format
```markdown
We achieved 95% accuracy using transformer models[^1].
The baseline approach yielded only 72% accuracy[^2].

[^1]: Vaswani et al., "Attention Is All You Need", NeurIPS 2017
[^2]: Internal benchmarks, January 2025, n=10,000 samples
```

<a id="sg-parallel-authoring-versioning"></a>
## Parallel-Authoring & Versioning

### File Naming Determinism
All files use predictable, conflict-free naming:

| Document Type | Directory | Naming Pattern | Example |
| :------------ | :-------- | :------------- | :------ |
| Research Brief | `docs/research/` | `YYYY-MM-module-N-research.md` | `2025-01-module-1-research.md` |
| PRD | `docs/project-design/` | `prd-NNNN-<feature>.md` | `prd-0001-ingestion.md` |
| RFC | `docs/rfcs/` | `rfc-NNNN-<topic>.md` | `rfc-0042-auth-system.md` |
| Meeting Notes | `docs/meetings/` | `YYYY-MM-DD-HH-<topic>.md` | `2025-01-15-14-standup.md` |
| Module Docs | `docs/modules/module-N-<name>/` | `README.md` + others | `module-1-ingestion/README.md` |
| How-To Guide | `docs/how-to/` | `<verb>-<object>.md` | `configure-database.md` |
| Technical Spec | `docs/specs/` | `spec-NNNN-<component>.md` | `spec-0003-api-gateway.md` |

### Required YAML Front Matter
```yaml
---
title: "Descriptive Title"
status: "Draft|Review|Approved|Deprecated|Archived"
updated: YYYY-MM-DD
owner: "@github-username"
reviewers: ["@user1", "@user2"]  # New in v3
version: "vMAJOR.MINOR.PATCH"
doc_id: "unique-permanent-id"
parent_doc: "parent-doc-id"  # New in v3 for hierarchy
depends_on: ["doc-id-1", "doc-id-2"]  # New in v3
tags: ["module-1", "research", "tier-1"]
related: ["./glossary.md", "#anchor-id"]
estimated_reading_time: "X minutes"  # New in v3
target_audience: ["interns", "developers", "executives"]  # New in v3
---
```

### Stable Anchor Protocol
Every H2 section must have a permanent anchor ID that never changes:

```markdown
<a id="doc-<doctype>-<section>"></a>
## Section Title Can Change But Anchor Stays

Examples:
<a id="doc-prd-requirements"></a>
## Functional Requirements

<a id="doc-rfc-alternatives"></a>
## Alternatives Considered
```

### Branch and PR Strategy for Docs
1. **Branch Naming**: `docs/<doc-id>-<description>`
2. **One Document Per PR**: Each PR modifies exactly one primary document
3. **Dependent Changes**: List dependencies in PR description
4. **Review Assignment**: Auto-assign based on `reviewers` front matter
5. **Merge Order**: Respect `depends_on` ordering

### Glossary Management Protocol
- **Single Owner**: `@docs-wg` owns `docs/glossary.md`
- **Addition Process**: PR with single term addition, definition, example
- **Modification Process**: Include justification and impact analysis
- **Deprecation**: Mark obsolete terms but never delete (for history)

### Change Tracking Requirements
Every document includes a Change Log section:

```markdown
## Change Log

### v3.0.0 - 2025-01-15
- **Breaking**: Renamed `user_name` to `username` throughout
- **Added**: WebSocket support for real-time updates
- **Fixed**: Rate limiting calculation error
- **Deprecated**: REST endpoint `/old/api` (remove in v4.0)

### v2.1.0 - 2025-01-10
- **Added**: Batch processing endpoints
- **Improved**: Error messages with specific codes
```

<a id="sg-templates"></a>
## Templates (Copy-Paste Ready)

### Research Brief Template
```markdown
---
title: "Research Brief: Module N - <Topic>"
status: "Draft"
updated: YYYY-MM-DD
owner: "@intern-username"
reviewers: ["@mentor", "@tech-lead"]
version: "v1.0"
doc_id: "research-module-N-<topic>"
parent_doc: "module-N-readme"
tags: ["research", "module-N", "week-1"]
estimated_reading_time: "10 minutes"
target_audience: ["developers", "tech-lead"]
---

<a id="doc-research-summary"></a>
## Executive Summary
[One paragraph: problem, approach, key findings, recommendation]

<a id="doc-research-problem"></a>
## Problem Statement
### Context
[Background and why this research matters]

### Research Questions
1. Primary: [Main question to answer]
2. Secondary: [Supporting questions]

### Success Criteria
- [ ] Technology recommendation with rationale
- [ ] Implementation timeline with milestones
- [ ] Risk assessment and mitigation plan

<a id="doc-research-analysis"></a>
## Technology Analysis

### Option 1: [Technology Name]
**Pros:**
- [Specific advantage with evidence]

**Cons:**
- [Specific limitation with evidence]

**Evaluation Score:** X/5
**Rationale:** [Why this score]

### Option 2: [Technology Name]
[Same structure]

### Comparison Matrix
| Criterion | Option 1 | Option 2 | Weight |
| :-------- | :------: | :------: | :----: |
| Learning Curve | 3/5 | 4/5 | 30% |
| Performance | 5/5 | 3/5 | 25% |
| Community Support | 4/5 | 5/5 | 20% |
| Cost | 5/5 | 2/5 | 15% |
| Integration Ease | 3/5 | 4/5 | 10% |
| **Weighted Total** | **3.85** | **3.65** | **100%** |

<a id="doc-research-recommendation"></a>
## Recommendation
### Primary Choice
[Technology name with 2-3 sentence justification]

### Implementation Approach
```mermaid
gantt
    title Implementation Timeline
    dateFormat  YYYY-MM-DD
    section Research
    Technology Selection :done, 2025-01-15, 3d
    section Development  
    Core Implementation :active, 2025-01-18, 5d
    Testing : 2025-01-23, 2d
```

### Risk Mitigation
| Risk | Probability | Impact | Mitigation |
| :--- | :---------: | :----: | :--------- |
| [Risk description] | High/Med/Low | High/Med/Low | [Specific action] |

<a id="doc-research-validation"></a>
## Validation Plan
1. [Proof of concept test]
2. [Performance benchmark]
3. [Integration test]

## References
[^1]: [Author, "Title", Publication, Year]

## Change Log
- YYYY-MM-DD: Initial research completed
```

### Technical Specification Template
```markdown
---
title: "Technical Specification: <Component>"
status: "Draft"
updated: YYYY-MM-DD
owner: "@engineer"
reviewers: ["@architect", "@tech-lead"]
version: "v1.0.0"
doc_id: "spec-NNNN-<component>"
depends_on: ["prd-NNNN"]
tags: ["spec", "technical", "module-N"]
estimated_reading_time: "15 minutes"
target_audience: ["developers", "qa"]
---

<a id="doc-spec-overview"></a>
## Overview
### Purpose
[What this component does and why it exists]

### Scope
**In Scope:**
- [Included functionality]

**Out of Scope:**
- [Explicitly excluded]

### Success Metrics
- [Measurable outcome with target value]

<a id="doc-spec-architecture"></a>
## Architecture
### Component Diagram
```mermaid
graph TD
    A[Client] -->|HTTPS| B[API Gateway]
    B --> C[Service Layer]
    C --> D[Data Layer]
```

### Data Flow
[Sequence of operations with example]

<a id="doc-spec-api"></a>
## API Specification

### Endpoint: Create Entity
**Method:** `POST /api/v1/entities`

**Request:**
```json
{
  "name": "string, required, max 255 chars",
  "type": "enum: person|organization|location",
  "metadata": {
    "source": "string, optional",
    "confidence": "number, 0.0-1.0"
  }
}
```

**Response (201 Created):**
```json
{
  "id": "e_abc123",
  "name": "Example Corp",
  "type": "organization",
  "created_at": "2025-01-15T14:30:00Z",
  "metadata": {
    "source": "manual_entry",
    "confidence": 0.95
  }
}
```

**Error Responses:**
| Code | Reason | Response Body |
| :--- | :----- | :------------ |
| 400 | Invalid input | `{"error": "E1001", "message": "Name required"}` |
| 409 | Duplicate | `{"error": "E1002", "message": "Entity exists", "existing_id": "e_xyz"}` |

<a id="doc-spec-implementation"></a>
## Implementation Details
### Database Schema
```sql
-- Entity table
CREATE TABLE entities (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_entities_type ON entities(type);
CREATE INDEX idx_entities_name ON entities(name);
```

### Key Algorithms
```python
def generate_entity_id(name: str, type: str) -> str:
    """Generate deterministic entity ID."""
    hash_input = f"{type}:{name.lower().strip()}"
    hash_value = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
    return f"e_{hash_value}"
```

<a id="doc-spec-testing"></a>
## Testing Strategy
### Unit Tests
- [ ] ID generation determinism
- [ ] Input validation rules
- [ ] Error handling paths

### Integration Tests
- [ ] Database transactions
- [ ] API contract compliance
- [ ] Rate limiting behavior

### Performance Targets
- Response time: p95 < 200ms
- Throughput: 1000 requests/second
- Database connections: max 50

<a id="doc-spec-security"></a>
## Security Considerations
- Input sanitization against SQL injection
- Rate limiting: 100 requests/minute per IP
- Authentication: Bearer tokens with 1-hour expiry
- Audit logging: All mutations logged with user ID

<a id="doc-spec-deployment"></a>
## Deployment
### Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://localhost:6379
API_KEY=<secret>
LOG_LEVEL=INFO
```

### Health Checks
```http
GET /health
```
Returns: `{"status": "healthy", "version": "1.0.0", "uptime": 3600}`

## Change Log
- YYYY-MM-DD: Initial specification
```

### Enhanced PRD Template
```markdown
---
title: "PRD: <Feature Name>"
status: "Draft"
updated: YYYY-MM-DD
owner: "@product-manager"
reviewers: ["@tech-lead", "@design-lead", "@qa-lead"]
version: "v1.0"
doc_id: "prd-NNNN-<feature>"
depends_on: ["strategy-doc-id"]
tags: ["prd", "product", "tier-1"]
estimated_reading_time: "12 minutes"
target_audience: ["developers", "designers", "executives"]
---

<a id="doc-prd-problem"></a>
## Problem Statement
### User Problem
[Specific problem users face, with evidence]

### Business Impact
- Current cost: [Quantified impact]
- Opportunity size: [Market or efficiency gain]

### Evidence
- User interviews: [Key finding with sample size]
- Analytics: [Specific metric showing problem]
- Support tickets: [Pattern from ticket analysis]

<a id="doc-prd-solution"></a>
## Proposed Solution
### High-Level Approach
[One paragraph describing the solution]

### Key Features
1. **Feature Name**: [What it does and why]
2. **Feature Name**: [What it does and why]

### User Flow
```mermaid
graph LR
    A[User Need] --> B{Decision Point}
    B -->|Path 1| C[Action]
    B -->|Path 2| D[Alternative]
    C --> E[Outcome]
    D --> E
```

<a id="doc-prd-success"></a>
## Success Metrics
### Primary KPIs
| Metric | Current | Target | Measurement |
| :----- | :-----: | :----: | :---------- |
| [Metric name] | X | Y | [How measured] |

### Secondary Metrics
- [Metric with target]

### Guardrail Metrics
- [Metric that shouldn't degrade]

<a id="doc-prd-requirements"></a>
## Requirements
### Functional Requirements
| ID | Requirement | Priority | Acceptance Criteria |
| :- | :---------- | :------: | :------------------ |
| F1 | [What system must do] | P0 | [How to verify] |
| F2 | [What system should do] | P1 | [How to verify] |

### Non-Functional Requirements
| Category | Requirement | Target |
| :------- | :---------- | :----- |
| Performance | Page load time | < 2 seconds |
| Reliability | Uptime | 99.9% |
| Security | Authentication | OAuth 2.0 |
| Accessibility | WCAG compliance | Level AA |

<a id="doc-prd-scope"></a>
## Scope Definition
### In Scope - MVP
- [Specific feature/capability]

### In Scope - Future
- [Feature for v2]

### Out of Scope
- [What we explicitly won't do]

### Dependencies
- [External system or team]

<a id="doc-prd-design"></a>
## Design Specifications
### Visual Design
- [Link to Figma/mockups]
- Key interaction patterns

### Content Requirements
- [Copy needs and tone]

### Responsive Behavior
- Desktop: [Behavior]
- Mobile: [Adaptations]

<a id="doc-prd-risks"></a>
## Risk Assessment
| Risk | Probability | Impact | Mitigation | Owner |
| :--- | :---------: | :----: | :--------- | :---- |
| [Risk description] | H/M/L | H/M/L | [Action] | @owner |

<a id="doc-prd-timeline"></a>
## Timeline
### Milestones
| Milestone | Date | Deliverable | Success Criteria |
| :-------- | :--- | :---------- | :--------------- |
| Design Complete | YYYY-MM-DD | Mockups approved | Stakeholder sign-off |
| Dev Complete | YYYY-MM-DD | Feature code complete | Passes QA |
| Launch | YYYY-MM-DD | Feature live | Metrics baseline |

### Launch Plan
1. **Soft Launch**: [Approach]
2. **Monitoring**: [What to watch]
3. **Rollback**: [Criteria and process]

## References
- [User Research Report](./research/user-study-N.md)
- [Technical Specification](./specs/spec-NNNN.md)
- [Design System](./design/system.md)

## Change Log
- YYYY-MM-DD: Initial PRD
- YYYY-MM-DD: Updated success metrics after review
```

<a id="sg-review-qa-checklists"></a>
## Review & QA Checklists

### Writer Checklist (Pre-Commit)
#### Content Quality
- [ ] Document purpose stated in first paragraph
- [ ] All technical terms defined on first use
- [ ] Every concept has concrete example
- [ ] Claims supported by evidence/citations
- [ ] No TODO, TBD, or FIXME markers remain

#### Structure & Format
- [ ] YAML front matter complete and valid
- [ ] File name follows naming convention
- [ ] H2 sections have stable anchor IDs
- [ ] Code blocks have language tags and purpose comments
- [ ] Tables have headers and alignment
- [ ] Images have alt text and captions

#### Cross-References
- [ ] Internal links use relative paths
- [ ] Anchor links resolve correctly
- [ ] External links use HTTPS
- [ ] Glossary terms linked on first use
- [ ] No broken links (verified with tool)

#### Standards Compliance
- [ ] Active voice used throughout
- [ ] Present tense for system behavior
- [ ] Inclusive language check passed
- [ ] Numbers/units follow standards
- [ ] Paragraph length ≤ 4 sentences

### Reviewer Checklist (Pre-Merge)
#### Technical Accuracy
- [ ] Information factually correct
- [ ] Code examples compile/run
- [ ] API examples match implementation
- [ ] Performance claims verified
- [ ] Security considerations addressed

#### Completeness
- [ ] Addresses stated goals
- [ ] Covers typical use cases
- [ ] Includes error scenarios
- [ ] Migration path documented (if breaking)
- [ ] Testing approach defined

#### Consistency
- [ ] Terminology matches glossary
- [ ] Tone consistent with style guide
- [ ] References align with other docs
- [ ] Versioning follows semver
- [ ] Change log updated

#### Quality
- [ ] Readable at college level
- [ ] Examples clear and realistic
- [ ] Progressive disclosure followed
- [ ] No unexplained magic
- [ ] Actionable next steps

### Accessibility Checklist
#### Structure
- [ ] Heading hierarchy logical (no skipped levels)
- [ ] Lists use proper markdown syntax
- [ ] Tables not used for layout
- [ ] Document sections clearly separated

#### Navigation
- [ ] Link text descriptive (no "click here")
- [ ] Heading text unique and descriptive
- [ ] Table of contents for docs > 5 sections
- [ ] Skip links for long documents

#### Media
- [ ] Images have descriptive alt text
- [ ] Diagrams explained in text
- [ ] Color not sole information carrier
- [ ] Contrast ratio ≥ 4.5:1 in images

#### Language
- [ ] Sentences < 25 words average
- [ ] Technical jargon minimized
- [ ] Abbreviations expanded
- [ ] Instructions clear and sequential

### AI-Human Collaboration Checklist
#### AI Agent Tasks
- [ ] Clear task boundaries defined
- [ ] Input/output formats specified
- [ ] Success criteria measurable
- [ ] Error handling documented
- [ ] Human review points identified

#### Human Review Requirements
- [ ] Technical accuracy verified
- [ ] Business logic validated
- [ ] User experience considered
- [ ] Edge cases covered
- [ ] Documentation readable

#### Handoff Protocol
- [ ] Work state documented
- [ ] Next actions listed
- [ ] Blockers identified
- [ ] Dependencies noted
- [ ] Time estimate provided

<a id="sg-terminology-formatting"></a>
## Terminology & Formatting Guide

### Core Project Terms
These terms have specific meanings in Knowledge Graph Lab context:

| Term | Definition | Usage Example |
| :--- | :--------- | :------------ |
| Knowledge Graph Lab (KGL) | The complete AI research platform project | "KGL processes 10,000 documents daily" |
| Module | Self-contained service component with specific responsibility | "Module 1 handles data ingestion" |
| Entity | Uniquely identified real-world object in the graph | "Entity `e_nyc_001` represents New York City" |
| Relationship | Typed connection between entities | "The `located_in` relationship connects cities to countries" |
| Claim | Structured statement with confidence score | "Claim: 'Population: 8.3M' with 0.95 confidence" |
| Evidence | Source metadata for claim verification | "Evidence includes URL, timestamp, and excerpt hash" |
| Ontology | Domain schema defining types and constraints | "Our ontology defines 15 entity types" |
| Living Ontology | Versioned schema allowing controlled evolution | "The living ontology added 3 new predicates in v2" |
| Frontier Queue | Prioritized list of items to research | "The frontier queue contains 500 pending topics" |

### Technical Terms
| Term | Definition | When to Use |
| :--- | :--------- | :---------- |
| API | Application Programming Interface | First mention in any document |
| REST | Representational State Transfer | When describing API architecture |
| GraphQL | Query language for APIs | When discussing alternative to REST |
| WebSocket | Protocol for real-time communication | For live updates discussion |
| Docker | Container platform | Infrastructure/deployment contexts |
| Kubernetes (K8s) | Container orchestration | Scaling/production contexts |
| CI/CD | Continuous Integration/Deployment | Development workflow contexts |
| OAuth | Open Authorization standard | Authentication contexts |
| JWT | JSON Web Token | Session/auth token contexts |

### Banned Terms → Replacements
| Don't Use | Use Instead | Reason |
| :-------- | :---------- | :----- |
| Whitelist/Blacklist | Allow list/Deny list | Inclusive language |
| Master/Slave | Primary/Replica | Inclusive language |
| Dummy data | Sample data | Respectful language |
| Sanity check | Validation check | Ableist language |
| Obviously/Simply | Remove or be specific | Condescending |
| Kill | Terminate/Stop | Violent metaphor |
| Foo/Bar/Baz | Real examples | Meaningless |
| RTFM | See documentation | Hostile |
| Grandfather in | Maintain legacy support | Ageist |

### Capitalization Rules
- **Document titles (H1)**: Title Case
- **Section headings (H2-H4)**: Sentence case
- **Product names**: As trademarked (GitHub, PostgreSQL, not Github, Postgres)
- **Acronyms**: All caps (API, REST, SQL)
- **File names**: lowercase-kebab-case.md
- **Variables/code**: Follow language conventions

### Date and Time Standards
```markdown
Dates: YYYY-MM-DD (2025-01-15)
Times: HH:MM timezone (14:30 UTC)
Durations: Spell out units (5 minutes, not 5m)
Ranges: YYYY-MM-DD to YYYY-MM-DD
Relative: Avoid (use absolute dates)
```

### Number Formatting
```markdown
0-9: Spell out (five servers)
10+: Use numerals (15 servers)
Thousands: Comma separator (1,000)
Decimals: Consistent precision (0.95 or 0.950)
Percentages: 95% (not 95 percent)
Ranges: 10-15 (en dash, no spaces)
Multiplication: 3x faster (not 3X)
```

### Code Reference Standards
```markdown
Files: `path/to/file.py`
Functions: `calculate_similarity()`
Classes: `EntityResolver`
Variables: `user_id`
Commands: `pip install -r requirements.txt`
Environment vars: `DATABASE_URL`
Inline code: Use backticks for any code element
```

### Unit Standards
| Measurement | Format | Example |
| :---------- | :----- | :------ |
| Time | Number + full unit | 5 seconds, 2 minutes |
| Data size | Binary (GiB) or Decimal (GB) | 10 GiB RAM, 500 GB disk |
| Frequency | Per time unit | 1,000 requests/second |
| Money | ISO currency code | USD 99.99, EUR 75.00 |
| Temperature | Celsius with C | 20°C |
| Percentage | Number + % | 99.9% uptime |

<a id="sg-examples-library"></a>
## Examples Library

### Research Brief (Bad → Good)
**Bad**: "I looked at some tools and FastAPI seems good because it's fast."

**Good**: "After evaluating four Python frameworks against five criteria (performance, learning curve, community support, async capabilities, and production readiness), FastAPI scores highest at 4.2/5. Performance benchmarks show 30,000 requests/second (vs Flask's 8,000), the active community provides 24-hour issue response times, and native async support aligns with our concurrent processing requirements. The 2-week ramp-up time fits our timeline."

### Technical Specification (Bad → Good)
**Bad**: "The API returns data about entities in JSON."

**Good**: 
```markdown
### Get Entity Endpoint
**Method**: `GET /api/v1/entities/{entity_id}`
**Response (200 OK)**:
```json
{
  "id": "e_nyc_001",
  "name": "New York City",
  "type": "location",
  "population": 8336817,
  "confidence": 0.98,
  "last_updated": "2025-01-15T10:30:00Z"
}
```
**Error (404)**: `{"error": "E2001", "message": "Entity e_xyz_999 not found"}`
```

### PRD Problem Statement (Bad → Good)
**Bad**: "Users complain about search being bad."

**Good**: "Current entity search has 65% precision (35% false positives) causing users to spend 12 minutes average finding correct entities (user study n=50, December 2024). Support tickets about 'wrong search results' increased 3x in Q4 (from 20 to 60/week). Customer interviews reveal frustration with irrelevant results appearing above exact matches. This impacts 10,000 daily active users and correlates with 15% session abandonment rate."

### Error Message (Bad → Good)
**Bad**: "Error: Failed"

**Good**: "Error E3456: Database connection timeout after 30 seconds. Possible causes: (1) Database server down - check status at monitoring.internal/db, (2) Network issues - verify VPN connection, (3) Connection pool exhausted - current: 50/50. Action: Retry in 5 seconds or contact @database-team."

### Commit Message (Bad → Good)
**Bad**: "fixed stuff"

**Good**: "Fix entity deduplication ignoring case sensitivity

Problem: Entity matcher compared 'NYC' and 'nyc' as different entities
Solution: Normalize to lowercase before comparison
Impact: Reduces duplicate entities by ~15% in test dataset
Test: Added unit tests for case-insensitive matching"

### How-To Introduction (Bad → Good)
**Bad**: "This guide shows database setup."

**Good**: "This guide walks you through PostgreSQL setup for local development, including installation, schema creation, and sample data loading. You'll need Docker installed and 2GB free disk space. Expected completion time: 15 minutes. By the end, you'll have a working database with test data ready for Module 2 integration."

<a id="sg-quality-metrics"></a>
## Quality Metrics

### Readability Metrics
- **Target**: Flesch-Kincaid Grade Level 12-14 (college)
- **Tool**: `readability-checker` or built-in linters
- **Action**: Rewrite if score > 14

### Documentation Coverage
- **Target**: 100% of public APIs documented
- **Measurement**: Automated doc coverage tools
- **Review**: Quarterly documentation audits

### Link Health
- **Target**: Zero broken links
- **Tool**: `markdown-link-check` in CI/CD
- **Frequency**: On every commit

### Review Velocity
- **Target**: Documentation reviewed within 24 hours
- **Measurement**: PR review time tracking
- **Escalation**: Auto-assign if > 24 hours

### Update Frequency
- **Target**: Documentation updated within 1 sprint of code changes
- **Measurement**: Doc-code drift analysis
- **Alert**: Flag outdated docs > 30 days

### User Satisfaction
- **Target**: 80% helpful rating
- **Method**: Embedded feedback widget
- **Review**: Monthly analysis of feedback

<a id="sg-ai-human-collaboration"></a>
## AI-Human Collaboration Guidelines

### Task Division
**AI Agents Excel At:**
- Initial draft creation from templates
- Consistency checking across documents
- Link validation and reference updates
- Format standardization
- Example code generation
- Change log maintenance

**Humans Must Handle:**
- Technical accuracy verification
- Business logic validation
- User experience decisions
- Complex problem solving
- Creative examples
- Strategic decisions

### AI Agent Instructions
When assigning documentation tasks to AI agents, provide:

```markdown
TASK: Create technical specification for [component]
CONTEXT: 
- Related PRD: [link]
- Architecture decision: [link]
- Similar existing spec: [link]
CONSTRAINTS:
- Follow STYLEGUIDE-v3.md exactly
- Use spec template from section X
- Include Python code examples
- Target audience: senior developers
OUTPUT: 
- File: docs/specs/spec-0004-[component].md
- Length: 8-10 sections
- Include: API examples, error codes, performance targets
REVIEW: @human-reviewer by YYYY-MM-DD
```

### Human Review Focus Areas
1. **Technical Correctness**: Verify algorithms, performance claims, security implications
2. **Business Alignment**: Ensure matches product requirements and user needs
3. **Completeness**: Check for missing edge cases, error scenarios, dependencies
4. **Clarity**: Confirm examples make sense, progression is logical
5. **Integration**: Validate consistency with other system components

### Handoff Documentation
When transferring work between AI and human (or vice versa):

```markdown
## Handoff Record
**From**: @ai-agent-1 
**To**: @human-reviewer
**Date**: 2025-01-15 14:30 UTC
**Document**: spec-0004-auth.md

### Completed
- [ ] Initial specification structure
- [ ] API endpoint definitions
- [ ] Example requests/responses
- [ ] Database schema

### Needs Review
- [ ] Performance targets (need benchmarks)
- [ ] Security section (needs security team input)
- [ ] Error codes (verify with existing system)

### Blockers
- Missing: OAuth provider configuration details
- Unclear: Session timeout requirements

### Next Actions
1. Verify performance targets with load tests
2. Security team review by 2025-01-17
3. Add migration guide for existing auth system
```

<a id="sg-versioning-strategy"></a>
## Document Versioning Strategy

### Version Number Format
Documents use semantic versioning: `vMAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (restructure, scope change)
- **MINOR**: New sections, significant content additions
- **PATCH**: Typos, clarifications, small fixes

### Version Triggers
| Change Type | Version Bump | Example |
| :---------- | :----------- | :------ |
| Typo fix | PATCH (1.0.0 → 1.0.1) | Spelling correction |
| New example | PATCH (1.0.1 → 1.0.2) | Add code sample |
| New section | MINOR (1.0.2 → 1.1.0) | Add troubleshooting |
| Restructure | MAJOR (1.1.0 → 2.0.0) | Reorder all sections |
| Scope change | MAJOR (2.0.0 → 3.0.0) | Expand from API to full system |

### Deprecation Process
```markdown
## Section Title [DEPRECATED]
> [!WARNING]
> This section is deprecated as of v2.0.0 and will be removed in v3.0.0.
> New location: [Link to new section]
> Migration guide: [Link to migration doc]

[Original content remains for reference]
```

<a id="sg-change-log"></a>
## Change Log

### v3.0.0 - 2025-09-09
- **Breaking**: Restructured templates with required fields for research briefs and technical specs
- **Breaking**: Added mandatory `reviewers`, `parent_doc`, and `depends_on` front matter fields
- **Added**: AI-Human collaboration guidelines and handoff protocols
- **Added**: Quality metrics with specific targets and measurement methods
- **Added**: Expanded templates for Research Brief and Technical Specification
- **Added**: Document versioning strategy with semantic versioning
- **Added**: Enhanced accessibility checklist with WCAG 2.1 AA compliance
- **Added**: Comprehensive terminology guide based on project glossary
- **Added**: Error message standards with codes and resolution steps
- **Added**: Cross-reference protocol for internal and external links
- **Added**: Deprecation process for phasing out content
- **Improved**: Parallel authoring rules with branch strategy and merge protocols
- **Improved**: Expanded examples library with more bad → good transformations
- **Improved**: More prescriptive rules with measurable success criteria
- **Fixed**: Clarified file naming patterns to prevent conflicts
- **Fixed**: Added reading time estimates to improve planning

### v2.0.0 - 2025-09-08
- Converted from philosophy-based to rule-based approach
- Added deterministic file naming and anchor schemes
- Introduced required YAML front matter
- Created copy-paste ready templates
- Added writer/reviewer/accessibility checklists

### v1.0.0 - 2025-09-08  
- Initial style guide with writing philosophy
- Basic formatting guidelines
- General quality recommendations