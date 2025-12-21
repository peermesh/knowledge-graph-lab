# Module Organization Standards

**Version**: 1.0
**Effective Date**: 2025-11-22

To maintain a clean, scalable, and understandable project structure, all modules must adhere to these organizational rules.

---

## 1. Core Philosophy: Creation vs. Consumption

We distinguish between the *Creation* environment and the *Consumption* environment.

*   **Creation (The Kitchen)**: `work-in-progress/`. Messy, iterative, raw ingredients. For the module owner.
*   **Consumption (The Dining Room)**: `deliverables/` & `handoffs/`. Plated, polished, ready. For the team.

**Rule**: Never serve food from the floor. Move it to the table (Deliverables) first.

---

## 2. Standard Module Structure

Every module (`backend-architecture`, `frontend-design`, `ai-development`, `publishing-tools`) MUST have this exact top-level structure:

```
[module-name]/
├── 01-work-description.md          # Scope definition
├── 02-phase-1-research/            # Phase assignments
├── 03-phase-2-prd+plan/            # Phase assignments
│
├── deliverables/                   # FINALIZED work only
│   ├── phase-1-research/
│   ├── phase-2-planning/
│   └── ...
│
├── work-in-progress/               # ACTIVE work
│   ├── raw/                        # Unprocessed notes, transcripts
│   ├── ai-generated/               # AI outputs needing validation
│   └── synthesis/                  # Manual refinements
│
├── handoffs/                       # Integration packages for other devs
│   └── README.md
│
└── README.md                       # Module navigation guide
```

---

## 3. Governance Rules

### Rule 1: No Root Files
No files are allowed at the module root level except:
1.  `README.md`
2.  Standard assignment files (`01-work-description.md`, etc.)

**Why**: Root-level files are the start of entropy. If you create a "quick note," put it in `work-in-progress/raw/`.

### Rule 2: The Archiving Policy
`work-in-progress/` is not a permanent storage unit.
*   **Action**: At the end of each Phase (e.g., "Phase 1 Complete"), move relevant files to `deliverables/` if they are valuable.
*   **Cleanup**: Delete or archive obsolete drafts.

### Rule 3: Handoffs are for Code/Config
*   **Deliverables** = Documents (PRDs, Specs, Research).
*   **Handoffs** = Working Code/Config (e.g., a Docker compose file, a working API client example).
*   *Goal*: A developer should be able to download a `handoffs/` folder and run it immediately.

### Rule 4: Major Artifact Exceptions
Sometimes a massive, self-contained artifact (like `ai-module-holistic-review/`) doesn't fit.
*   **Exception**: Allowed ONLY if it is self-contained, read-only, and represents a major milestone.
*   **Labeling**: Must be clearly marked in the module `README.md` as a "Major Artifact."

---

## 4. Naming Conventions

*   **Directories**: `kebab-case` (e.g., `phase-1-research`, `user-auth`).
*   **Files**: `kebab-case.md` preferred.
*   **Dates**: `YYYY-MM-DD-filename.md` (ISO 8601).

---

## 5. Maintenance Checklist (Weekly)

Module owners should check:
1.  [ ] Are there loose files in the module root? -> Move to `work-in-progress/raw/`.
2.  [ ] Is `work-in-progress/` getting cluttered? -> Archive old runs.
3.  [ ] Are `deliverables/` actually finished? -> If not, move back to WIP.
4.  [ ] Do `handoffs/` have a README? -> If not, add instructions.


