# Documentation Style Guide

**Purpose**: Enable clear, consistent documentation that helps CS undergraduates build production software  
**Audience**: Interns learning production systems, plus agents and reviewers maintaining docs  
**Read time**: 15 minutes

---

## Core Philosophy

**Write as if the reader is smart but has never built production software before.**

Your reader understands programming, algorithms, and CS theory. They don't understand production systems, real-world tradeoffs, or industry practices. Every document should teach, not just describe.

If an intern needs to ask a question after reading your documentation, you've missed something.

---

## The Five Rules That Matter

### 1. Define Before Using

Every technical term, acronym, or system concept gets explained on first use. No exceptions.

**Bad**: "The service uses CQRS with event sourcing."  
**Good**: "The service separates read and write operations (CQRS pattern) and stores all changes as a sequence of events rather than updating records directly (event sourcing)."

### 2. Show With Examples

Abstract concepts need concrete examples within two paragraphs. Use real data, not foo/bar.

**Bad**: "Entities can have multiple relationships."  
**Good**: "Entities can have multiple relationships. For example, 'New York City' has relationships: `located_in: New York State`, `contains: Manhattan`, and `population: 8.3 million`."

**Where examples are required**:
- **MUST**: APIs, data models, and error paths
- **SHOULD**: new concepts and non-obvious claims  
- **MAY**: omit in executive/vision sections if you link to a canonical example

### 3. Build Complexity Gradually

Start simple. Add complexity. Never jump ahead.

**Right order**:
1. What it is (one sentence)
2. Why we need it (problem it solves)  
3. How it works (basic operation)
4. Example (concrete instance)
5. Edge cases (if relevant)

### 4. Explain Decisions

Don't just state what—explain why. Interns need to understand reasoning to learn.

**Bad**: "We use PostgreSQL for data storage."  
**Good**: "We use PostgreSQL because it supports JSON fields for flexible schemas while maintaining ACID compliance for financial data integrity."

### 5. Forward References (Allowed with Context)

You may reference a later section **if** you add a one-sentence inline explanation and link to a stable anchor.

**Bad**: "The pipeline (details later) handles it."  
**Good**: "The pipeline validates schema, uniqueness, and PII (see [Validation Pipeline](#validation-pipeline)) before storage."

---

## Writing Standards

### Paragraphs
- **Default**: 2-5 sentences, one idea per paragraph
- **May exceed** for formal definitions or multi-step trade-offs (note reason in comment)
- **Must have** one blank line between paragraphs

### Voice and Tense
- **Active voice**: "Module 1 processes data" not "Data is processed by Module 1"
- **Present tense**: for system behavior
- **Past tense**: for decisions already made
- **Future tense**: for planned features

### Terminology
- **Define** on first use in each document
- **Add to glossary** if used 3+ times
- **Use consistently** - no synonyms for the same concept

### Readability
- **Target**: Flesch-Kincaid Grade 12-14
- **If higher**: investigate and either simplify or justify (e.g., "formal spec requires precision")
- **Tool**: Use readability checkers as signals, not gates

---

## Markdown Structure & Visual Design

### Spacing Rules (GitHub-Optimized)

One blank line between ALL block elements:

```markdown
# Document Title

Introduction paragraph with document purpose.

---

## Major Section

Section introduction explaining what's covered.

### Subsection

First content paragraph with complete thought.

Second paragraph building on the first.

```bash
# Commands are copy-paste clean
npm install
```

Explanations go in prose above or below the code block.

---

## Next Major Section

Continue the pattern with consistent spacing.
```

### Document Structure

```markdown
---
title: "Document Title"
version: "v1.0"
updated: 2024-01-15
author: "@username"
status: draft | review | approved | deprecated
doc_id: "unique-permanent-id"
---

# Document Title

Brief introduction stating purpose and scope.

---

## Table of Contents
<!-- Include ONLY if doc has ≥4 H2 sections OR >800 words -->
- [Major Section](#major-section)
- [Another Section](#another-section)
- [References](#references)

---

## Major Section

Introduction to this section.

### Subsection

Content here.
```

### Headings

- **H1**: Once per document (title only)
- **H2**: Major sections (use `---` between them)
- **H3**: Subsections
- **H4**: Allowed sparingly for minor points
- **H5+**: Prohibited - restructure instead

### Diagram Annotations

Use structured annotation blocks for diagrams:

```markdown
<!-- DAB
id: auth-flow
title: User Authentication Flow
type: sequence
actors: User, API, AuthService, Database
must_show: login, validation, token-generation, error-handling
notes: Keep under 20 nodes; show retry logic
-->

```mermaid
%%AUTOGEN:auth-flow%%
sequenceDiagram
    %%placeholder%%
```

*Figure 1: Authentication flow with error handling*
```

**Diagram Types**:
- `flowchart` - Process flows, decision trees
- `sequence` - Service interactions over time
- `state` - Entity lifecycle
- `architecture` - System components
- `er` - Database schema
- `class` - Object design
- `gantt` - Timelines
- `pie` - Distributions (max 8 slices)

**Chart Annotation Block (CAB)**:
```markdown
<!-- CAB
id: performance-comparison
title: Response Time by Method
type: bar
data_source: ./data/benchmarks.csv
columns: method, response_time
notes: Label axes clearly; include units
-->

```mermaid
%%AUTOGEN:performance-comparison%%
%%placeholder%%
```

*Figure 2: API response times across methods*
```

**Compatibility Note**: If only `<!-- DIAGRAM: description -->` exists, the diagram agent converts it to DAB format using context.

### Code Blocks

Keep command blocks copy-paste clean:

````markdown
Install the dependencies:

```bash
pip install -r requirements.txt
python -m pytest tests/
```

If tests fail, check Python version (requires 3.8+).
````

For code with logic:

````markdown
Calculate entity similarity:

```python
def calculate_similarity(name1: str, name2: str) -> float:
    """Returns 0.0-1.0 similarity score."""
    distance = levenshtein_distance(name1, name2)
    max_len = max(len(name1), len(name2))
    return 1.0 - (distance / max_len)
```
````

### Tables

Keep tables focused and scannable:

```markdown
Performance comparison across databases:

| Feature | PostgreSQL | MongoDB | DynamoDB |
| :------ | :--------: | :-----: | :------: |
| ACID | ✓ | Partial | ✗ |
| Schema | Flexible | Free | Fixed |
| Scale | Vertical | Both | Horizontal |

*Table 1: Database feature comparison*
```

### Lists

**Ordered** (sequential steps):
```markdown
1. First step with clear action

2. Second step building on first

3. Final verification step
```

**Unordered** (parallel items):
```markdown
- Independent point one
  - Nested detail (max 2 levels)
  
- Independent point two

- Independent point three
```

### Special Blocks

```markdown
> **Note:** Additional context that helps understanding.

> **Warning:** Critical information to prevent errors.

> **Tip:** Optional optimization or best practice.

<details>
<summary>Advanced Configuration (Optional)</summary>

Content for advanced users.

</details>
```

### Accessibility

- **Images**: Include alt text
- **Diagrams**: Add captions after each diagram
- **Links**: Use descriptive text (no "click here")
- **Tables**: Include headers and keep under 5 columns when possible

---

## Document Templates

### Research Brief

```markdown
---
title: "Research: [Topic]"
version: "v1.0"
updated: YYYY-MM-DD
author: "@intern-name"
status: draft
doc_id: "research-[topic]"
---

# Research: [Topic]

One paragraph stating problem, approach, and recommendation.

---

## Executive Summary

Key findings in 3-4 bullets:
- Finding one with metric
- Finding two with impact
- Recommendation with confidence

---

## Problem Statement

### Context
Why this research matters.

### Requirements
- Requirement with metric
- Constraint with deadline

---

## Analysis

### Option 1: [Technology]

Brief description.

**Pros:**
- Advantage with evidence (e.g., "10k req/s")
- Another advantage

**Cons:**
- Limitation with impact
- Workaround if any

**Score:** 4/5 - Justification

### Option 2: [Technology]
[Same structure]

### Comparison

<!-- DAB
id: tech-comparison
title: Technology Score Comparison
type: bar
notes: Show scores by criterion
-->

```mermaid
%%AUTOGEN:tech-comparison%%
%%placeholder%%
```

*Figure 1: Technology comparison scores*

| Criteria | Weight | Option 1 | Option 2 |
| :------- | :----: | :------: | :------: |
| Performance | 30% | 5/5 | 3/5 |
| Learning | 25% | 3/5 | 4/5 |
| **Total** | **100%** | **4.15** | **3.60** |

---

## Recommendation

We recommend **Option 1** because:
1. Highest score (4.15/5.00)
2. Best performance
3. Acceptable learning curve

### Implementation Timeline

<!-- DAB
id: timeline
title: 4-Week Implementation
type: gantt
notes: Show phases and milestones
-->

```mermaid
%%AUTOGEN:timeline%%
%%placeholder%%
```

*Figure 2: Implementation timeline*

---

## References
- [Documentation](link)
- [Benchmarks](link)
```

### Technical Specification

```markdown
---
title: "Specification: [Component]"
version: "v1.0"
updated: YYYY-MM-DD
author: "@engineer"
status: draft
doc_id: "spec-[component]"
---

# Specification: [Component]

What this component does and why it exists.

---

## Overview

### Purpose
Problem this solves.

### Scope
**In Scope:**
- Feature 1
- Feature 2

**Out of Scope:**
- Future consideration

<!-- DAB
id: system-context
title: Component in System
type: architecture
notes: Show interfaces and data flow
-->

```mermaid
%%AUTOGEN:system-context%%
%%placeholder%%
```

*Figure 1: Component architecture*

---

## API Design

### Create Entity

Create new entity in the knowledge graph.

**Request:**
```http
POST /api/v1/entities
Content-Type: application/json

{
  "name": "New York City",
  "type": "location"
}
```

**Success Response (201):**
```json
{
  "id": "entity_nyc_001",
  "name": "New York City",
  "type": "location",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Response (400):**
```json
{
  "error": "INVALID_TYPE",
  "message": "Type must be: person|location|organization"
}
```

---

## Implementation

### Database Schema

```sql
CREATE TABLE entities (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_entities_type ON entities(type);
```

### Key Algorithm

```python
def generate_entity_id(name: str, type: str) -> str:
    """Generate deterministic entity ID."""
    normalized = f"{type}:{name.lower().strip()}"
    hash_value = hashlib.sha256(normalized.encode()).hexdigest()[:8]
    return f"entity_{hash_value}"
```

---

## Testing

### Coverage Requirements
- Unit tests: 90% coverage
- Integration tests: All endpoints
- Performance: 1000 req/s sustained

### Example Test

```python
def test_entity_creation():
    """Verify entity creation."""
    entity = create_entity("NYC", "location")
    assert entity.id.startswith("entity_")
    assert entity.type == "location"
```

---

## References
- [API Guidelines](./api-guidelines.md)
- [Security Standards](./security.md)
```

---

## Quality Checklist

### Content
- [ ] Terms defined on first use
- [ ] Complex concepts have examples
- [ ] Decisions explained with reasoning
- [ ] Forward references include inline explanation
- [ ] Examples follow MUST/SHOULD/MAY rules

### Structure
- [ ] One H1 for title
- [ ] Proper spacing throughout
- [ ] Code blocks have language tags
- [ ] Command blocks are copy-paste clean
- [ ] Tables have headers and captions

### Diagrams
- [ ] DAB/CAB annotations where helpful
- [ ] Placeholders marked with %%AUTOGEN%%
- [ ] Captions under each diagram
- [ ] Figures numbered and referenced

### Accessibility
- [ ] Alt text for images
- [ ] Descriptive link text
- [ ] Table headers present
- [ ] Diagrams have captions

### Readability
- [ ] FK Grade 12-14 (or justified if higher)
- [ ] Paragraphs 2-5 sentences (or noted exception)
- [ ] No unexplained jargon
- [ ] Active voice throughout

---

## Common Mistakes to Avoid

### Dense Paragraphs
**Wrong**: One 12-sentence wall explaining three ideas.  
**Right**: Three short paragraphs, each with one clear point.

### Command Blocks with Comments
**Wrong**:
```bash
npm install  # Install dependencies
```

**Right**:
```bash
npm install
```
Install project dependencies.

### Missing Diagram Context
**Wrong**: Random diagram with no explanation.  
**Right**: Introduction, annotated diagram placeholder, caption.

### Unexplained Decisions
**Wrong**: "We use Kubernetes."  
**Right**: "We use Kubernetes for automatic scaling (handles our variable traffic), self-healing (restarts failed pods), and zero-downtime deployments."

---

## File Naming

Simple and predictable:
- Research: `YYYY-MM-research-[topic].md`
- Specs: `YYYY-MM-spec-[component].md`
- Guides: `guide-[task].md`
- Meeting notes: `YYYY-MM-DD-meeting-[topic].md`

---

## For Documentation Ops

The following belong in a separate "Documentation Operations Guide":
- CI/CD integration and link checking
- Branch and merge strategies
- Deprecation and anchor preservation
- Review assignment and approval workflows
- Repository structure and governance

This keeps the style guide focused on writing while ops details remain available for maintainers.

---

## Remember

Good documentation teaches. It respects the reader's intelligence while acknowledging their inexperience with production systems. 

Write the documentation you wish you'd had when you were learning.

---
