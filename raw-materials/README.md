# Raw Materials & Working Directory

This directory contains informal documentation, working notes, chat logs, and other materials that influence planning but are **not part of the definitive design**. Think of this as the "workshop" area where ideas are developed before becoming formal documentation.

## Directory Structure

### `chats/`
Raw chat logs, conversation exports, and AI assistant interactions that contain valuable insights or decisions. These provide context for how design decisions evolved.

### `notes/`
Informal notes, meeting minutes, quick thoughts, and scratchpad-style documentation. Includes both human and AI-generated working notes.

### `brainstorming/`
Creative exploration, alternative approaches considered, rejected ideas (with rationale), and early conceptual work. Valuable for understanding the design space explored.

### `planning-docs/`
Work-in-progress planning materials, draft requirements, preliminary analysis, and documents that are evolving toward formal specifications.

### `references/`
Links, bookmarks, paper summaries, tool evaluations, and other reference materials that inform the project but don't constitute the design.

## Usage Guidelines

- **Informal First**: Start ideas here before formalizing in `docs/`
- **Context Preservation**: Keep raw materials that explain the "why" behind decisions
- **Timestamp Everything**: Use `YYYY-MM-DD-HHMM-` prefixes for chronological tracking
- **Cross-Reference**: Link to formal documentation when materials get promoted
- **Version Control**: All materials are tracked, nothing is considered "throwaway"

## Relationship to Formal Documentation

```
raw-materials/         → docs/ (formal)
├── chats/            → docs/ai/ (AI-generated final docs)
├── notes/            → docs/Governance/ADR-*.md (decisions)
├── brainstorming/    → docs/Ontology/, docs/Reasoning/ (architecture)
├── planning-docs/    → docs/Product/, docs/Evaluation/ (specifications)
└── references/       → research/ (curated research materials)
```

## File Naming Convention

Use descriptive names with timestamps:
- `2025-09-07-1415-initial-project-review-chat.md`
- `2025-09-07-1430-brainstorm-pack-architecture.md`
- `2025-09-07-1445-notes-competency-questions-ideas.md`

This helps maintain chronological understanding of how concepts developed.