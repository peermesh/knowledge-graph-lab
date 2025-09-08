---
title: "Project Style Guide (v1.0)"
status: "Draft"
updated: 2025-09-08
owner: "@docs-wg"
applies_to: ["Agents","Interns","PMs","Execs"]
---

<a id="sg-exec-summary"></a>
## Executive Summary
This guide standardizes how we plan, write, and review technical documentation so multiple humans and agents can work in parallel without conflicts. It sets rules for tone, structure, Markdown usage, and versioning; defines deterministic file and anchor naming; and provides copy‑paste templates and checklists. Everyone who writes or reviews documentation—agents, interns, PMs, and executives—should use this guide. It applies to all Markdown in this repository, including specifications, PRDs, RFCs, meeting notes, and how‑to guides. Follow the rules to keep content clear, consistent, accessible, and easy to merge.

<a id="sg-core-principles"></a>
## Core Principles
- **Clarity first**: Prioritize reader understanding over brevity or cleverness.
- **Brevity with substance**: Be concise, but never remove context needed for comprehension.
- **Consistency**: Use uniform structure, tone, and terminology across all documents.
- **Single source of truth**: Facts, definitions, and canonical terms live in one place and are referenced, not duplicated.
- **Evidence and examples**: Support claims with sources and concrete, realistic examples.
- **Accessibility**: Write for a college-level reader; define terms on first use; support screen readers.
- **Determinism**: Use stable filenames, anchors, and front matter to enable safe parallel editing.
- **Traceability**: Every meaningful change is documented and cross-linked.

<a id="sg-authoring-rules"></a>
## Authoring Rules
1) Tone and Voice  
- Why it exists: A consistent, friendly, and direct tone improves comprehension and trust.  
- Good: “This module ingests raw articles and normalizes entities.”  
- Bad: “One might consider that the subsystem could be leveraged to potentially normalize entities.”

2) Active vs. Passive Voice  
- Why it exists: Active voice makes ownership and actions clear.  
- Good: “Module 1 ingests data and writes normalized entities.”  
- Bad: “Data is ingested and normalized by Module 1.”

3) Tense  
- Why it exists: Present tense reduces cognitive load for system behavior; past tense records decisions.  
- Good: “The API returns a 201 status when the entity is created.” / “We chose Postgres after comparing options.”  
- Bad: “The API would return 201.” / “We choose Postgres last week.”

4) Inclusive Language  
- Why it exists: Respectful, neutral language improves inclusivity and professionalism.  
- Good: “They run the migration.” / “Allow list” / “Primary/replica.”  
- Bad: “He runs the migration.” / “Whitelist/blacklist” / “Master/slave.”

5) Acronyms and Terms  
- Why it exists: Unfamiliar acronyms block understanding.  
- Rule: Spell out on first use with acronym in parentheses; add to `docs/glossary.md`.  
- Good: “Knowledge Graph Lab (KGL) builds…”  
- Bad: “KGL builds…” (first mention)

6) Specificity and Examples  
- Why it exists: Concrete examples translate abstract ideas into practice.  
- Good: “We merge ‘NYC’ and ‘New York City’ into one entity based on a 0.92 similarity score.”  
- Bad: “We merge similar cities when they look alike.”

7) Figures and Tables  
- Why it exists: Visuals and tabular data require captions and references to be accessible and scannable.  
- Rule: Provide descriptive alt text, a caption, and reference in text.  
- Good: “Figure 1 shows the ingestion pipeline. See Figure 1.”  
- Bad: “See below.” (no caption/alt text)

8) Citations and Sources  
- Why it exists: Evidence increases credibility and helps reviewers verify claims.  
- Rule: Use footnotes or reference links; prefer primary sources.  
- Good: “We use Levenshtein distance for fuzzy matching.[^lev]”  
- Bad: “We use a common algorithm.”  
[^lev]: Levenshtein, V. “Binary codes capable of correcting deletions, insertions, and reversals.” 1966.

9) Paragraph Discipline  
- Why it exists: Predictable paragraph structure speeds comprehension.  
- Rule: 3–4 sentences; topic sentence first; one idea per paragraph.  
- Good: “Entity resolution links different mentions of the same real-world object. It reduces duplication and improves query accuracy. We apply both rules and ML to decide matches.”  
- Bad: A 7-sentence block mixing multiple unrelated topics.

10) Progressive Disclosure  
- Why it exists: Readers learn faster when complexity builds gradually.  
- Good: Start with “What/Why,” then “How,” then edge cases.  
- Bad: Begin with exceptions or implementation details.

11) Numbers and Units  
- Why it exists: Consistent numerals reduce ambiguity.  
- Rule: Use words for zero–nine, numerals for 10+; SI units; include time zones.  
- Good: “We processed 12 datasets in 3 hours (UTC).”  
- Bad: “We processed twelve datasets in three hrs.”

12) “No Magic” Claims  
- Why it exists: Vague language hides assumptions.  
- Good: “The service retries three times with exponential backoff (100 ms base).”  
- Bad: “The service automatically retries.”

<a id="sg-tech-markdown"></a>
## Tech Markdown Conventions
- Headings (H1–H4)
  - H1: One per file (document title).  
  - H2: Major sections. Include a stable anchor (see Parallel Authoring).  
  - H3: Subsections.  
  - H4: Rare, for small sub-parts. Avoid H5+.
- Lists
  - Use numbers for ordered steps; dashes for unordered lists.  
  - Nest at most two levels. Keep each bullet to one idea.
- Code Blocks
  - Always provide a language tag and a one-line purpose comment as the first line.
  ```bash
  # Install dependencies
  pip install -r requirements.txt
  ```
  ```json
  // Example entity payload
  {
    "id": "ent_123",
    "name": "New York City",
    "aliases": ["NYC", "New York"]
  }
  ```
- Inline Code
  - Use backticks for file, directory, function, and class names: `docs/glossary.md`, `ingest_entities()`.
- Tables
  - Include a header row; left-align text; avoid complex tables that do not render well on mobile.

  | Term | Definition |
  | :--- | :--------- |
  | Entity | A uniquely identified real-world object in the graph |
  | Relationship | A typed connection between two entities |

- Callouts (GitHub alerts)
  - Use blockquote alerts: NOTE, TIP, IMPORTANT, WARNING.
  > [!NOTE]  
  > Provide API examples with both request and response.
- Definition Lists
  - GitHub Markdown has limited support; standardize on two-column tables (Term/Definition) or bullets with “Term — Definition”.
- Footnotes
  - Use GFM footnotes: `[^id]` and define them in the same file.
- Link References
  - Prefer reference-style links for reuse and clarity:
  ```markdown
  See the [Data Model][data-model] and [Tech Markdown Conventions](#sg-tech-markdown).

  [data-model]: ./project-design/data-model.md "Data Model"
  ```

<a id="sg-parallel-authoring-versioning"></a>
## Parallel-Authoring & Versioning
- File Layout and Naming
  - Lowercase kebab-case; ASCII letters, numbers, and dashes only; no spaces.  
  - Deterministic patterns by doc type:

  | Type | Directory | Filename Pattern |
  | :--- | :-------- | :--------------- |
  | PRD | `docs/project-design/` | `prd-<feature-slug>.md` |
  | RFC | `docs/rfcs/` | `rfc-<####>-<topic-slug>.md` (zero‑padded `####`) |
  | Meeting Notes | `docs/meetings/` | `meet-YYYY-MM-DD-<topic-slug>.md` (UTC) |
  | How-To | `docs/how-to/` | `howto-<task-verb>-<object>.md` |
  | Glossary | `docs/` | `glossary.md` (single source of truth) |
  | Style Guide | `docs/` | `STYLEGUIDE.md` |

- Required Front Matter (all docs)
  ```yaml
  ---
  title: "<Document Title>"
  status: "Draft|Proposed|Approved|Deprecated"
  updated: YYYY-MM-DD
  owner: "@github-handle"
  applies_to: ["Agents","Interns","PMs","Execs"]
  version: "vX.Y"         # increment minor on content changes; major on breaking structure
  doc_id: "<doc-slug-or-id>" # stable identifier; never reused
  tags: ["topic-a","topic-b"]
  related: ["../glossary.md","#sg-terminology-formatting"] # relative paths or anchors
  ---
  ```

- Stable Heading IDs / Anchors
  - Prepend each H2 with an HTML anchor id that is stable even if the heading text changes.
  - Pattern: `<a id="doc-<file-slug>-<section-slug>"></a>` or file-scoped (e.g., this doc uses `sg-...`).
  - Link within or across files using `#<anchor-id>`.

- Glossary Ownership
  - `docs/glossary.md` is the canonical source.  
  - Add new terms via PR; include definition, example, and related terms.

- Change Logs
  - Each substantive doc includes a “Change Log” section at the end.  
  - Summarize what changed and why with dates. Major changes link to PRs.

- PR / Merge Etiquette
  - One conceptual change per PR; small, reviewable diffs.  
  - Use the Writer and Reviewer Checklists (see Review & QA).  
  - Do not rename anchors casually; if required, preserve the old anchor with an empty placeholder to avoid breaking links.

<a id="sg-templates"></a>
## Templates (Copy-Paste Ready)

### PRD.md
```markdown
---
title: "PRD: <Feature Name>"
status: "Draft"
updated: YYYY-MM-DD
owner: "@owner"
applies_to: ["Agents","Interns","PMs","Execs"]
version: "v0.1"
doc_id: "prd-<feature-slug>"
tags: ["prd","product"]
related: ["../glossary.md"]
---

<a id="doc-prd-overview"></a>
## Overview
- Problem statement (what/why).  
- Success metrics and KPIs.  
- Audience and scope.

## Goals and Non-Goals
- Goals:
- Non-Goals:

## Users and Scenarios
- Primary users and jobs-to-be-done.
- Example flows.

## Requirements
- Functional requirements (numbered).
- Non-functional requirements (latency, availability, privacy).

## Scope and Assumptions
- In scope:
- Out of scope:
- Assumptions:

## Data Model and APIs
- Link to `../project-design/data-model.md`.
- Example API request/response (with language tags).

## Risks and Mitigations
- Risk → Mitigation.

## Milestones and Acceptance Criteria
- Milestone 1 → criteria.
- Milestone 2 → criteria.

## Appendix
- Glossary entries (link to `../glossary.md`).
- References.

## Change Log
- YYYY-MM-DD: Initial draft.
```

### RFC.md
```markdown
---
title: "RFC-####: <Topic>"
status: "Proposed"
updated: YYYY-MM-DD
owner: "@owner"
applies_to: ["Agents","Interns","PMs","Execs"]
version: "v0.1"
doc_id: "rfc-<####>-<topic-slug>"
tags: ["rfc","design"]
related: ["../glossary.md","../project-design/api-specification.md"]
---

## Summary
One-paragraph problem and proposed direction.

## Motivation
Why this matters; tradeoffs; affected stakeholders.

## Design
Architecture, data flows, algorithms. Include diagrams and examples.

## Alternatives Considered
Option A, B, C with pros/cons.

## Migration / Backwards Compatibility
Steps and safeguards.

## Security / Privacy
Threats and mitigations.

## Drawbacks
Costs, risks, maintenance burden.

## Unresolved Questions
Open items and decision deadlines.

## Decision (filled when approved)
Approved approach and rationale.

## Change Log
- YYYY-MM-DD: Proposal created as RFC-####.
```

### MeetingNotes.md
```markdown
---
title: "Meeting: <Topic>"
status: "Draft"
updated: YYYY-MM-DD
owner: "@facilitator"
applies_to: ["Agents","Interns","PMs","Execs"]
version: "v1.0"
doc_id: "meet-YYYY-MM-DD-<topic-slug>"
tags: ["meeting"]
related: []
---

## When and Where
- Date: YYYY-MM-DD (UTC)
- Time: HH:MM–HH:MM (UTC)
- Location: <Video link or room>

## Participants
- @name (role)

## Agenda
1. Item 1
2. Item 2

## Notes
- Key discussion points (objective and concise).

## Decisions
- Decision → Owner → Rationale.

## Action Items
| Owner | Action | Due | Status |
| :---- | :----- | :-- | :----- |
| @name | Do X | YYYY-MM-DD | Open |

## References
- Links to docs, issues, and RFCs.

## Change Log
- YYYY-MM-DD: Notes captured.
```

### HowTo.md
````markdown
---
title: "How-To: <Task>"
status: "Draft"
updated: YYYY-MM-DD
owner: "@owner"
applies_to: ["Agents","Interns","PMs","Execs"]
version: "v1.0"
doc_id: "howto-<task-verb>-<object>"
tags: ["how-to"]
related: []
---

## Summary
What this achieves and when to use it.

## Prerequisites
- Tools, permissions, environments.

## Steps
1. Do X.
2. Do Y.
```bash
# Example command for Step 2
your_command --flag value
```

## Verification
- How to confirm success.

## Troubleshooting
- Symptom → Cause → Fix.

## References
- Links to APIs, specs, or external sources.

## Change Log
- YYYY-MM-DD: Initial version.
````

<a id="sg-review-qa-checklists"></a>
## Review & QA Checklists

### Writer Checklist (pre-PR)
- [ ] Front matter includes required keys and valid values.
- [ ] File name follows the pattern for its type.
- [ ] Each H2 has a stable anchor id.
- [ ] Terms are defined on first use and added to `docs/glossary.md`.
- [ ] Examples are realistic; API samples include request and response.
- [ ] Code fences include language tags and a purpose comment.
- [ ] No “TODO/TBD/XXX” or placeholder text remains.
- [ ] Links use reference style or stable anchors; no dead links.
- [ ] Images have alt text; figures include captions and are referenced in text.
- [ ] Ran a spell check/read-through for clarity and tone.

### Reviewer Checklist (pre-merge)
- [ ] Content is accurate, complete, and consistent with the glossary.
- [ ] Rules in this style guide are followed (tone, tense, inclusivity).
- [ ] Structure matches the appropriate template.
- [ ] Anchors are stable; cross-links resolve.
- [ ] Risky or ambiguous claims have citations or are reworded.
- [ ] Change Log summarizes meaningful changes.
- [ ] Scope is appropriate for a single PR; diffs are reviewable.

### Accessibility Checklist
- [ ] Logical heading order (no skipped levels).
- [ ] Link text is descriptive (avoid “here”).
- [ ] Alt text describes the purpose of images.
- [ ] Lists and tables use proper Markdown syntax.
- [ ] Sufficient color contrast in images (if applicable).

<a id="sg-terminology-formatting"></a>
## Terminology & Formatting Guide

- Canonical Terms (add to `docs/glossary.md`)
  - Knowledge Graph Lab (KGL) — The project and codebase for our knowledge graph platform.
  - Entity — A uniquely identified real-world object represented in the graph.
  - Relationship — A typed connection between two entities.
  - Ontology — The formal vocabulary (types, properties, relationships) of the graph.
  - Entity Resolution — The process of merging multiple mentions into one entity.
  - Module — A cohesive set of code and docs serving one capability (e.g., ingestion).
  - Agent — An automated system actor (e.g., AI assistant) that reads/writes docs.
  - PR (Pull Request) — A proposed change set submitted for review.
  - RFC (Request for Comments) — A structured proposal for a technical decision.

- Banned Terms (with replacements)
  - “Whitelist/blacklist” → “Allow list/deny list”
  - “Master/slave” → “Primary/replica”
  - “Simply/just/obviously/clearly” → remove or replace with specifics
  - “Foo/bar/baz” → realistic domain examples (e.g., “New York City”)

- Capitalization and Headings
  - Titles (H1): Title Case.  
  - Headings (H2–H4): Sentence case.  
  - Proper nouns and acronyms are capitalized.

- Dates, Times, Numbers
  - Date: `YYYY-MM-DD` (ISO 8601).  
  - Time: 24-hour, include time zone (UTC preferred).  
  - Numbers: words for zero–nine; numerals for 10+; include units.

- File and Code References
  - Use backticks: `docs/project-design/api-specification.md`, `resolve_entities()`.

- Code Blocks
  - Include language tag and a purpose comment on the first line. Prefer complete, runnable snippets when feasible.

<a id="sg-examples-library"></a>
## Examples Library

- PRD (bad → good)
  - Bad: “The system will maybe improve search.”  
  - Good: “This feature reduces median query latency by 25% and increases successful entity matches by 10% on the news dataset.”

- RFC (bad → good)
  - Bad: “We’ll use a graph DB because it’s cool.”  
  - Good: “We adopt a labeled property graph to support flexible schema evolution and path queries; benchmarks show 1.8× faster traversals on our workload.”

- How-To (bad → good)
  - Bad: “Run the script and it should work.”  
  - Good: “Run `seed_data.py` with `--env staging`. Verify `200 OK` from `/healthz`. If it fails, see Troubleshooting: ‘Missing credentials’.”

<a id="sg-change-log"></a>
## Change Log
- 2025-09-08: Converted guidelines into prescriptive rules with rationale and examples.
- 2025-09-08: Added deterministic file/anchor schemes and required front matter.
- 2025-09-08: Standardized Tech Markdown (headings, lists, code fences, tables, callouts, footnotes, link refs).
- 2025-09-08: Included copy-paste templates for PRD, RFC, Meeting Notes, and How-To.
- 2025-09-08: Added Writer/Reviewer/Accessibility checklists to support parallel review.
- 2025-09-08: Defined terminology, banned terms, capitalization, and date/time rules.
- 2025-09-08: Introduced stable anchor policy and PR/merge etiquette for parallel authorship.
