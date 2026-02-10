# Proposal: Knowledge Integration Pipeline for KGL Interface Design

**Proposal ID:** PROP-2025-12-20-001
**Status:** Draft
**Author:** Claude (via conversation with grig)
**Date:** 2025-12-20
**Project:** Knowledge Graph Lab - Frontend Specification V2

---

## Problem Statement

The Knowledge Graph Lab frontend specification requires integration of ideas, requirements, and design decisions scattered across multiple locations:

- Multiple repo directories (`knowledge-graph-lab`, `knowledge-graph-lab-alpha`, `knowledge-graph-lab-prototype`, etc.)
- Obsidian vault documentation
- Markdown inbox folders with research and conversation exports
- RAG/knowledge graph research projects
- Parent PeerMesh project documentation
- Conversation histories across chat systems (not yet exported)

The current specification (00-complete-specification.md) was created from a subset of available documentation. A more complete specification requires systematic integration of scattered knowledge, but the scope is too large for a single session or context window.

---

## Proposed Solution

### Phase 1: Discovery & Inventory (This Proposal)

Create a structured inventory of knowledge sources with metadata about their relevance, recency, and integration priority.

**Deliverable:** `KNOWLEDGE-SOURCES-INVENTORY.md`

### Phase 2: Extraction Pipeline

For each high-priority source, create extraction prompts that pull relevant concepts into a normalized format.

**Deliverable:** `extracted/` directory with normalized concept files

### Phase 3: Synthesis Rounds

Iteratively integrate extracted concepts into the specification through versioned updates.

**Deliverable:** Versioned specifications (`00-complete-specification-v1.1.md`, etc.)

### Phase 4: Validation

Cross-reference synthesized specification against source materials to identify gaps.

**Deliverable:** `SPECIFICATION-GAPS.md`

---

## Known Source Locations

### Tier 1: Primary Project Directories
```
/Users/grig/work/peermesh/repo/knowledge-graph-lab/
/Users/grig/work/peermesh/repo/knowledge-graph-lab-alpha/
```
**Priority:** Highest - authoritative project documentation

### Tier 2: Parent Project Context
```
/Users/grig/work/peermesh/repo/
/Users/grig/work/obsidian-vault/🕸️ PeerMesh.org/
/Users/grig/work/obsidian-vault/🕸️ PeerMesh.org/knowledge-graph-lab/
```
**Priority:** High - provides strategic context and constraints

### Tier 3: Research & Experiments
```
/Users/grig/work/ai/Agentic-RAG-Knowledge-Graph/
/Users/grig/work/ai/repo/private-rag-knowledge-engine/
/Users/grig/Downloads/INBOX-markdown/knowledge-graph-deep-research-archive/
/Users/grig/Downloads/INBOX-markdown/peermesh_kgl_canvas_pack/
```
**Priority:** Medium - technical approaches and research findings

### Tier 4: Inbox & Unsorted
```
/Users/grig/Downloads/INBOX-markdown/
```
**Priority:** Variable - needs triage to identify relevant content

### Tier 5: Conversation Histories (Not Yet Accessible)
- Claude.ai conversations
- ChatGPT conversations
- Other chat systems

**Priority:** Unknown until exported - may contain recent critical decisions

---

## Specification Versioning Strategy

### Archive Policy
Each significant update to the specification creates a new version:
- `00-complete-specification.md` → always the current version
- `_archive/00-complete-specification-v1.0-2025-12-20.md` → timestamped snapshots

### Version Triggers
- Integration of new source material
- Significant structural changes
- Stakeholder review feedback
- Build iteration learnings

### Change Log
Maintain `CHANGELOG.md` documenting what changed between versions and why.

---

## Agent Task Definition

### Task: Knowledge Source Inventory

**Objective:** Create comprehensive inventory of files and directories relevant to KGL frontend specification.

**Inputs:**
- Source location paths (listed above)
- Relevance criteria: frontend, UI, UX, interface, design, user journey, component, visualization, graph

**Process:**
1. Recursively scan each Tier 1-4 location
2. Identify files matching relevance criteria (by filename and content sampling)
3. Categorize by type: specification, research, conversation export, code, design asset
4. Assess recency (file modification date)
5. Estimate integration priority

**Output:** `KNOWLEDGE-SOURCES-INVENTORY.md` with structured entries:
```markdown
## [Source Name]
- **Path:** /full/path/to/file.md
- **Type:** specification | research | conversation | code | design
- **Recency:** YYYY-MM-DD
- **Relevance:** high | medium | low
- **Key Topics:** [list]
- **Integration Notes:** [brief description of what this contains]
```

### Task: Concept Extraction (Per Source)

**Objective:** Extract relevant concepts from a single source file into normalized format.

**Inputs:**
- Source file path
- Current specification (for context)
- Extraction template

**Process:**
1. Read source file
2. Identify concepts relevant to frontend specification
3. Categorize: entity types, interaction patterns, visual design, user flows, components, data structures
4. Note conflicts or extensions to current specification
5. Output in normalized format

**Output:** `extracted/[source-name]-concepts.md`

### Task: Synthesis Round

**Objective:** Integrate extracted concepts into specification.

**Inputs:**
- Current specification version
- Set of extracted concept files
- Integration priorities

**Process:**
1. Review extracted concepts
2. Identify additions, modifications, conflicts
3. Propose specification updates
4. Create new version with changes
5. Archive previous version
6. Update changelog

**Output:** 
- New specification version
- Changelog entry
- Archived previous version

---

## File Structure

```
/docs/design/_sprint-dec20-25/v2-spec/
├── 00-complete-specification.md          # Current version
├── BUILD-PLAN.md
├── CHANGELOG.md                          # Version history
├── KNOWLEDGE-SOURCES-INVENTORY.md        # Discovery results
├── SPECIFICATION-GAPS.md                 # Validation findings
├── _archive/                             # Previous versions
│   └── 00-complete-specification-v1.0-2025-12-20.md
├── extracted/                            # Normalized concepts from sources
│   ├── vision-md-concepts.md
│   ├── user-journeys-concepts.md
│   └── ...
└── proposals/
    └── PROP-2025-12-20-001-knowledge-integration.md  # This file
```

---

## Scope Boundaries

### In Scope
- Frontend/interface-related documentation
- User experience and journey documentation
- Visual design decisions
- Component specifications
- Interaction patterns
- Data structures visible to users

### Out of Scope (for this effort)
- Backend implementation details
- Infrastructure/deployment
- AI/ML pipeline internals
- Business strategy (unless it affects UX)

---

## Success Criteria

1. **Inventory Complete:** All Tier 1-3 sources catalogued with relevance assessment
2. **High-Priority Extracted:** Top 10 sources have concept extraction complete
3. **Specification Updated:** At least one synthesis round producing v1.1
4. **Gaps Identified:** Known missing areas documented for future work
5. **Process Documented:** Future agents can continue the work

---

## Estimated Effort

| Phase | Sessions | Notes |
|-------|----------|-------|
| Discovery & Inventory | 1-2 | Scanning and cataloguing |
| Extraction (per source) | 0.5 each | ~10 high-priority sources = 5 sessions |
| Synthesis Round | 1-2 | Per integration cycle |
| Validation | 1 | Cross-reference check |

**Total:** 8-12 agent sessions over multiple conversations

---

## Next Actions

1. [ ] Archive current specification as v1.0
2. [ ] Create CHANGELOG.md
3. [ ] Create extracted/ directory
4. [ ] Begin Phase 1: Run inventory task on Tier 1 sources
5. [ ] Triage Tier 4 (INBOX) for KGL-relevant content

---

## Notes for Future Agents

- The user has limited time to manually organize; automation and agent-driven work is preferred
- Always save work to the project directory, never leave it only in conversation
- The specification will evolve; treat it as living document
- When in doubt about scope, focus on what affects the user interface
- There may be a device-crawling script somewhere; search for "crawl" or "index" or "scan" in the user's work directories if needed
