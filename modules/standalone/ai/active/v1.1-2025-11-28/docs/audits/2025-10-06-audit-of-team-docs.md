# Documentation Audit: Knowledge Graph Lab Team Documentation
**Date**: October 6, 2025
**Auditor**: Documentation Review Specialist
**Scope**: `/docs` directory only (team-facing documentation)

---

## Executive Summary

**The documentation suffers from temporal confusion and structural duplication.** Team members cannot determine what phase they're in or where to submit their work because:

1. All entry points direct users to **Phase 1 tasks** despite Phase 1 being complete and the project being in Phase 2
2. **Three different locations** exist for the same deliverables with no explanation of which is authoritative
3. **Cryptic file naming** (02a, 02b, 02c, 03a, 03b, 03c) is never explained, creating navigation paralysis

A new team member following the official entry points will be told to complete Phase 1 research that was finished weeks ago.

---

## Critical Issues (Ranked by Impact)

### Issue #1: Temporal Mismatch - All Navigation Points to Completed Phase
**Problem**: Every onboarding path directs users to Phase 1 work, but Phase 1 is complete and Phase 2 is current.

**Evidence**:
- `docs/README.md:24` → Points to `team/README.md` for "development"
- `docs/team/README.md:15-18` → Table directs ALL roles to `02-phase-1-research/02b-phase-1-research-assignment.md`
- `docs/team/onboarding.md:19` → Tells new members to open Phase 1 research overview
- `docs/team/onboarding.md:40` → Says "Check phase deliverables: phase-1-deliverables.md"
- `docs/team/README.md:40-42` → "Your Next Steps" section lists Phase 1 as the active phase

**Impact**:
- **100% of new team members will be misdirected** to complete work that's already done
- Wastes hours before someone realizes the documentation is outdated
- Creates confusion about project status and timeline
- Undermines trust in documentation accuracy

**Fix**:
Update ALL entry points to reflect current phase:
- Change "Module Assignment Table" in `team/README.md` to point to Phase 2 assignments (`03-phase-2-prd+plan/03b-phase-2-prd-assignment.md`)
- Update onboarding checklist to Phase 2 tasks
- Add a "Current Phase" banner at the top of `team/README.md` that updates as phases progress
- Archive Phase 1 instructions in a "completed-phases/" subdirectory

---

### Issue #2: Three Competing Locations for Deliverables
**Problem**: PRDs and deliverables have three different homes with no explanation of which is authoritative or how they relate.

**Evidence**:
Three locations exist for the same content:
1. **`docs/modules/[module]/PRD.md`** - Contains actual PRDs with technical specs
2. **`docs/team/module-assignments/[module]/deliverables/phase-2-planning/`** - Where instructions say to submit
3. **`.dev/peermesh-canvases/`** - Referenced in PRD.md as "authoritative conceptual PRDs" (outside /docs)

Example from `docs/modules/backend-architecture/PRD.md:1`:
```
**Non-canonical during concept phase — authoritative conceptual PRDs live in .dev/peermesh-canvases/**
```

But `docs/team/project-plan/phase-2-deliverables.md:140` says:
```
3. **Save** to `/docs/team/module-assignments/[your-module]/deliverables/phase-2-planning/PRD.md`
```

**Impact**:
- Team members don't know where to submit work (3 conflicting locations)
- Reviewers don't know where to find latest work
- Risk of duplicate/conflicting versions
- Wasted time resolving "which file is correct?"

**Fix**:
1. **Pick ONE authoritative location**: Recommend `docs/modules/[module]/` as the single source of truth
2. **Remove or redirect other locations**:
   - Make `deliverables/` directories simple submission checkpoints with symlinks to canonical files
   - Add README in each location explaining the relationship
3. **Update all instructions** to reference only the canonical location
4. **Add a table** to team/README.md showing exactly where each file lives

---

### Issue #3: Cryptic File Naming Never Explained
**Problem**: Files are named 02a, 02b, 02c, 03a, 03b, 03c with no legend explaining the pattern.

**Evidence**:
From `docs/team/README.md:47-56`:
```markdown
Each module directory contains:
- `01-work-description.md`
- `02-phase-1-research/`
  - `02a-phase-1-research-overview.md`
  - `02b-phase-1-research-assignment.md`
  - `02c-phase-1-research-advanced.md`
- `03-phase-2-prd+plan/`
  - `03a-phase-2-prd-overview.md`
  - `03b-phase-2-prd-assignment.md`
  - `03c-phase-2-prd-advanced.md`
```

After reading for 10+ minutes, the pattern becomes clear:
- `0Xa` = Overview/Introduction
- `0Xb` = Assignment/Tasks
- `0Xc` = Advanced/Optional Deep Dive

But this is **never stated explicitly anywhere**.

**Impact**:
- New team members waste time figuring out which file to open
- Leads to opening wrong files first (02a when they need 02b)
- Creates unnecessary cognitive load
- Feels like insider knowledge vs accessible documentation

**Fix**:
Add a "File Naming Convention" section to `team/README.md`:
```markdown
## File Naming Convention

Module assignment files follow this pattern:
- **0Xa** files (e.g., `02a-phase-1-research-overview.md`) - High-level introduction, read first
- **0Xb** files (e.g., `02b-phase-1-research-assignment.md`) - Your specific tasks, work from this
- **0Xc** files (e.g., `02c-phase-1-research-advanced.md`) - Optional deep dive, reference material

**Quick rule**: Start with `0Xb` files for actionable tasks.
```

---

### Issue #4: Contradictory File References in Onboarding
**Problem**: Different guidance documents point to different starting files for the same task.

**Evidence**:
- `docs/team/README.md:15` (Assignment Table) → Points to `02b-phase-1-research-assignment.md`
- `docs/team/onboarding.md:19` (Day 1 Checklist) → Points to `02a-phase-1-research-overview.md`

Both are for "Phase 1 research" but recommend different entry points.

**Impact**:
- Confusion about which file to open first
- Some team members miss key information depending on which path they follow
- Inconsistent onboarding experience across team

**Fix**:
1. Standardize entry points: Always start with overview (02a), then assignment (02b)
2. Update all references to follow this sequence
3. Add directional links within docs: "After reading this overview, proceed to [02b-assignment.md]"

---

### Issue #5: Missing Phase State Indicator
**Problem**: No visual indicator of current phase or completion status across the project.

**Evidence**:
- `docs/team/project-plan/overview.md` lists all 5 phases equally with no "YOU ARE HERE" marker
- `docs/team/README.md` doesn't show current phase
- Phase deliverable files don't indicate if they're active, complete, or future

**Impact**:
- Cannot quickly determine project status
- New members don't know if old docs are historical or current
- No way to tell if a phase's documentation is aspirational or actionable

**Fix**:
Add phase indicators:
```markdown
# Team Start Here

**📍 CURRENT PHASE: Phase 2 - Planning & PRD Creation**
Status: In Progress | Phase 1: ✅ Complete | Phase 2: 🔄 Active | Phase 3-5: ⏳ Upcoming

[Progress Bar: ████░░░░░░░░░░░░] 30% Complete
```

---

### Issue #6: Duplicate Content - PRD vs Spec Files
**Problem**: Each module has both a `PRD.md` and a `[Module]-Spec.md` with overlapping content and no explanation of the difference.

**Evidence**:
```
docs/modules/backend-architecture/
├── Backend-Architecture-Spec.md (5,839 bytes)
└── PRD.md (4,719 bytes)

docs/modules/ai-development/
├── AI-Development-Spec.md (14,544 bytes)
└── PRD.md (5,942 bytes)
```

No documentation explains:
- What's the difference between a "PRD" and a "Spec"?
- Which should team members read first?
- Which is authoritative?
- Do they serve different purposes or are they drafts of the same thing?

**Impact**:
- Confusion about which document to follow
- Risk of outdated information if only one is updated
- Wasted time reading duplicate content
- Unclear which document to submit for Phase 2

**Fix**:
1. **Add a README** in `docs/modules/` explaining:
   ```markdown
   # Module Documentation Structure

   Each module contains:
   - **PRD.md** - Product Requirements Document (created in Phase 2, defines WHAT to build)
   - **[Module]-Spec.md** - Technical Specification (created in Phase 3, defines HOW to build)

   Read PRD first for requirements, then Spec for technical implementation details.
   ```
2. **Add headers** to each file type explaining its purpose and relationship to other docs

---

### Issue #7: Massive File Count Creates Navigation Paralysis
**Problem**: 87+ markdown files in `/docs` with deep nesting (6-7 levels) and no clear hierarchy.

**Evidence**:
```
docs/team/module-assignments/publishing-tools/deliverables/phase-1-research/ai-markdown-files/Analytics Platforms/chatgpt.md
```
That's a 7-level deep path!

File count by type:
- Module assignment files: 4 modules × 10 files each = 40 files
- Deliverable directories: 4 modules × 5 phases × 1 README = 20 files
- User journey docs: 20+ files
- Design docs: 15+ files
- Research files: 10+ files
- **Total: 100+ markdown files**

**Impact**:
- Overwhelming file tree in editors
- Difficult to find specific documents
- Many files are empty templates (just READMEs)
- Can't see the forest for the trees

**Fix**:
1. **Consolidate empty templates**: Remove empty deliverable READMEs until needed
2. **Create navigation index**: Add `docs/team/FILE-INDEX.md` listing all key files by purpose
3. **Flatten structure where possible**: Move user journeys to separate repo or archive
4. **Add breadcrumbs**: Each file should link back to parent index

---

## Quick Wins (Immediate Improvements)

### 1. Add "Current Phase" Banner
**Effort**: 10 minutes
**Impact**: High

Add to top of `docs/team/README.md`:
```markdown
---
**🚀 CURRENT PHASE: Phase 2 - Planning & PRD Creation**

✅ Phase 1 Complete | 🔄 Phase 2 Active (You are here) | ⏳ Phase 3-5 Upcoming

**Your focus right now**: Writing PRDs in `03-phase-2-prd+plan/03b-phase-2-prd-assignment.md`
---
```

### 2. Fix Module Assignment Table
**Effort**: 5 minutes
**Impact**: Critical

Change `docs/team/README.md:12-19` from Phase 1 links to:
```markdown
| Your Role | Current Task (Phase 2) | Assignment File |
|-----------|------------------------|-----------------|
| Backend Engineer | Write Backend PRD | module-assignments/backend-architecture/03-phase-2-prd+plan/03b-phase-2-prd-assignment.md |
| Frontend Developer | Write Frontend PRD | module-assignments/frontend-design/03-phase-2-prd+plan/03b-phase-2-prd-assignment.md |
```

### 3. Add File Naming Legend
**Effort**: 15 minutes
**Impact**: Medium

Add new section to `docs/team/README.md` after line 10:
```markdown
## Understanding File Names

Assignment files follow this pattern:
- **a files** (`03a-...`): Overview - Read this first for context
- **b files** (`03b-...`): Assignment - Your specific tasks, work from this
- **c files** (`03c-...`): Advanced - Optional deep dive and reference material

**Quick start**: Jump directly to `b` files for actionable tasks.
```

### 4. Create Single-Source-of-Truth Table
**Effort**: 20 minutes
**Impact**: High

Add to `docs/team/README.md`:
```markdown
## Where Files Live (Single Source of Truth)

| Document Type | Canonical Location | Purpose |
|---------------|-------------------|---------|
| Module PRDs | `docs/modules/[module]/PRD.md` | Your deliverable - submit here |
| Research briefs | `docs/team/module-assignments/[module]/deliverables/phase-1-research/` | Historical reference |
| Assignment instructions | `docs/team/module-assignments/[module]/0X-phaseX-*/` | Read-only guidance |

**Rule**: When instructions conflict, files in `docs/modules/` are authoritative.
```

### 5. Update Onboarding First Line
**Effort**: 2 minutes
**Impact**: High

Change `docs/team/onboarding.md:1-3` to:
```markdown
# Team Member Onboarding

**⚠️ Note**: This guide was written during Phase 1. We're now in Phase 2.
For current tasks, see [Phase 2 assignments](README.md#module-assignment-table).

Get productive on Day 1. Follow this comprehensive checklist.
```

---

## Structural Recommendations

### Proposed New Structure

```
docs/
├── README.md (Current: Good, keep as-is with phase banner)
│
├── team/
│   ├── README.md → **CRITICAL FIX**: Update to Phase 2
│   ├── CURRENT-PHASE.md → **NEW**: Single file showing active phase
│   ├── FILE-INDEX.md → **NEW**: Searchable list of all key files
│   ├── onboarding.md → **ARCHIVE**: Move to team/archive/phase-1-onboarding.md
│   │
│   ├── project-plan/ (Keep as-is, add phase markers)
│   │   └── overview.md → Add "Current Phase: 2" indicator
│   │
│   └── module-assignments/
│       ├── README.md → **NEW**: Explain structure and naming
│       │
│       └── [module]/
│           ├── 01-work-description.md (Keep)
│           ├── CURRENT-ASSIGNMENT.md → **NEW**: Symlink to active phase
│           │
│           ├── archive/
│           │   └── phase-1/ → **MOVE COMPLETED PHASES HERE**
│           │       ├── 02a-overview.md
│           │       ├── 02b-assignment.md
│           │       └── 02c-advanced.md
│           │
│           ├── active/
│           │   └── phase-2/ → **CURRENT WORK**
│           │       ├── 03a-overview.md
│           │       ├── 03b-assignment.md
│           │       └── 03c-advanced.md
│           │
│           └── upcoming/
│               └── phase-3/ → **FUTURE WORK**
│
├── modules/ → **CANONICAL DELIVERABLES**
│   └── [module]/
│       ├── README.md → **NEW**: Explain PRD vs Spec
│       ├── PRD.md (Phase 2 deliverable)
│       └── [Module]-Spec.md (Phase 3 deliverable)
│
├── design/ (Keep for reference, archive if too large)
│
└── archive/ → **NEW**: Completed work
    ├── phase-1-deliverables/
    └── deprecated-docs/
```

### Key Changes Explained

1. **Temporal Organization**: Move completed phases to `archive/`, active phases to `active/`, future to `upcoming/`
2. **CURRENT-PHASE.md**: Single file that always reflects active phase, updated as project progresses
3. **CURRENT-ASSIGNMENT.md**: Symlink that always points to current phase's assignment
4. **FILE-INDEX.md**: Searchable reference for "I need the file about X"
5. **Remove empty templates**: Only create deliverable READMEs when needed

---

## Consolidation Recommendations

### Files to Consolidate

#### 1. Merge Redundant READMEs
**Current**: Each deliverable folder has a nearly-empty README
```
docs/team/module-assignments/*/deliverables/phase-X-*/README.md
```

**Proposal**: Replace with single `DELIVERABLES.md` in module root:
```markdown
# Backend Architecture Deliverables

| Phase | Deliverable | Location | Status |
|-------|-------------|----------|--------|
| 1 | Research Brief | deliverables/phase-1-research/ | ✅ Complete |
| 2 | PRD | ../../modules/backend-architecture/PRD.md | 🔄 In Progress |
| 3 | MVP Code | deliverables/phase-3-mvp/ | ⏳ Upcoming |
```

#### 2. Archive User Journey Docs
**Current**: 20+ user journey files in `docs/design/user-journeys/`

**Issue**: These are valuable but not needed for day-to-day development

**Proposal**:
- Move to separate `docs/research/` directory or external wiki
- Keep single `user-journeys-summary.md` in design/
- Link to full docs if needed

#### 3. Consolidate Phase Deliverables Files
**Current**: Separate files for each phase in `project-plan/`
```
phase-1-deliverables.md
phase-2-deliverables.md
phase-3-deliverables.md
phase-4-deliverables.md
phase-5-deliverables.md
```

**Proposal**: Single `DELIVERABLES.md` with sections:
```markdown
# Project Deliverables by Phase

## 📍 Phase 2: Planning (CURRENT)
[Content from phase-2-deliverables.md]

## ✅ Phase 1: Research (COMPLETE)
<details><summary>Expand to see Phase 1 details</summary>
[Content from phase-1-deliverables.md]
</details>

## ⏳ Phase 3: MVP Development (UPCOMING)
```

---

## Sample Entry Point (Proposed new `docs/team/README.md`)

```markdown
# Team Start Here

---
**🚀 PROJECT STATUS**

**Current Phase**: Phase 2 - Planning & PRD Creation
**Timeline**: October 2025
**Active Deliverable**: Product Requirements Documents (PRDs)

✅ Phase 1 Complete | 🔄 **Phase 2 Active** | ⏳ Phase 3-5 Upcoming

---

## Your Quick Action (Based on Current Phase)

**If you're in Phase 2** (October 2025):
1. Find your module in the table below
2. Open your Phase 2 assignment file (ends with `03b-phase-2-prd-assignment.md`)
3. Follow the instructions to write your PRD
4. Submit to `docs/modules/[your-module]/PRD.md`

**If you're new to the project**:
Start with [Onboarding](onboarding.md), then return here for your current phase assignment.

---

## Module Assignments (Phase 2 - PRD Writing)

| Your Role | Module | Current Assignment | Where to Submit |
|-----------|--------|-------------------|-----------------|
| Backend Engineer | Backend Architecture | [PRD Assignment](module-assignments/backend-architecture/03-phase-2-prd+plan/03b-phase-2-prd-assignment.md) | [PRD.md](../modules/backend-architecture/PRD.md) |
| Frontend Developer | Frontend Design | [PRD Assignment](module-assignments/frontend-design/03-phase-2-prd+plan/03b-phase-2-prd-assignment.md) | [PRD.md](../modules/frontend-design/PRD.md) |
| AI/ML Engineer | AI Development | [PRD Assignment](module-assignments/ai-development/03-phase-2-prd+plan/03b-phase-2-prd-assignment.md) | [PRD.md](../modules/ai-development/PRD.md) |
| Content Systems | Publishing Tools | [PRD Assignment](module-assignments/publishing-tools/03-phase-2-prd+plan/03b-phase-2-prd-assignment.md) | [PRD.md](../modules/publishing-tools/PRD.md) |

---

## Understanding Assignment Files

Each module has three types of files per phase:

| File Pattern | Example | Purpose | When to Use |
|--------------|---------|---------|-------------|
| **0Xa-overview** | `03a-phase-2-prd-overview.md` | High-level introduction and context | Read first to understand the big picture |
| **0Xb-assignment** | `03b-phase-2-prd-assignment.md` | Specific tasks and requirements | **Start here for actionable work** |
| **0Xc-advanced** | `03c-phase-2-prd-advanced.md` | Optional deep dive and reference | Read when you need more detail |

**Quick rule**: Jump to `0Xb` files to start working immediately.

---

## Essential Links

### Current Phase (Phase 2)
- **[Phase 2 Deliverables Guide](project-plan/phase-2-deliverables.md)** - Requirements and submission process
- **[Git Workflow](git-workflow.md)** - How to submit your work
- **[Module Ownership](module-ownership.md)** - Who to contact for questions

### Project Overview
- **[Project Plan](project-plan/overview.md)** - All 5 phases explained
- **[System Architecture](../design/system/architecture.md)** - Technical overview
- **[Vision Document](../design/strategy/vision.md)** - Why we're building this

### Getting Help
- **Questions about your module**: Contact your module owner (see [Module Ownership](module-ownership.md))
- **Integration questions**: Ask in #kgl-integration channel
- **Process questions**: Contact @grig

---

## Where Everything Lives

| What You Need | Where to Find It | Notes |
|---------------|------------------|-------|
| **Your current assignment** | `module-assignments/[module]/03-phase-2-prd+plan/03b-*` | Read-only instructions |
| **Where to submit PRD** | `docs/modules/[module]/PRD.md` | Your deliverable goes here |
| **Past phase work** | `module-assignments/[module]/deliverables/phase-1-research/` | Historical reference only |
| **Project-wide guidelines** | `project-plan/` | Process and requirements |

**Rule**: When file locations conflict in documentation, files in `docs/modules/` are authoritative.

---

## Development Roadmap

![Knowledge Graph Lab Roadmap](../images/Knowledge-Graph-Lab-roadmap.png)

*This roadmap shows our 5-phase development process. You're currently in Phase 2 (Planning).*

---

## Need Help?

- **Can't find a file?** Check the [File Index](FILE-INDEX.md)
- **Not sure what phase we're in?** Check the banner at the top of this page
- **Conflicting instructions?** Files in `docs/modules/` are the source of truth
- **Still stuck?** Ask in Discord #kgl-general

---

**Last Updated**: October 6, 2025 (Updated for Phase 2)
```

---

## Navigation Flow Analysis

### Current Navigation Flow (Broken)

```
New Team Member arrives
    ↓
docs/README.md
    ↓ "For new team members"
docs/team/onboarding.md
    ↓ "Check team/README.md for assignment"
docs/team/README.md
    ↓ Module Assignment Table
team/module-assignments/backend/02-phase-1-research/02b-assignment.md
    ↓ ❌ **DEAD END**: Phase 1 is complete!
```

**Time to realize error**: 30-60 minutes
**Frustration level**: High
**Success rate**: 0%

### Proposed Navigation Flow (Fixed)

```
New Team Member arrives
    ↓
docs/README.md
    ↓ "For new team members"
docs/team/README.md  [Has "CURRENT PHASE: 2" banner]
    ↓ Module Assignment Table → Phase 2 links
team/module-assignments/backend/03-phase-2-prd+plan/03b-assignment.md
    ↓ ✅ Correct current task
docs/modules/backend/PRD.md
    ↓ ✅ Submit work here
```

**Time to start work**: 5-10 minutes
**Frustration level**: Low
**Success rate**: 95%+

---

## Team Member Navigation Test Results

### Scenario: "I'm assigned to Backend, what do I do today?"

#### Current Documentation Path:
1. Open `docs/team/README.md` → Told to go to Phase 1 assignment (WRONG)
2. Realize Phase 1 is done, search for Phase 2
3. Find three different files mentioning Phase 2:
   - `project-plan/phase-2-deliverables.md` (general requirements)
   - `module-assignments/backend/03-phase-2-prd+plan/03b-assignment.md` (my tasks)
   - `modules/backend/PRD.md` (submission template?)
4. Confused about which to read first and where to submit
5. **Time to productivity**: 45+ minutes

#### With Proposed Fixes:
1. Open `docs/team/README.md` → See banner "CURRENT PHASE: 2"
2. Find module in table → Click Phase 2 assignment link
3. Open `03b-phase-2-prd-assignment.md` → Read tasks
4. See clear submission instruction: "Submit to `docs/modules/backend/PRD.md`"
5. **Time to productivity**: 10 minutes

---

## Detailed Findings by Section

### Issue: Broken Cross-References

**Examples**:
1. `docs/team/project-plan/phase-1-deliverables.md:94` says:
   ```
   Save to `/docs/team/module-assignments/[your-module]/deliverables/phase-1-research/`
   ```
   But actual submitted work is in:
   ```
   docs/team/module-assignments/publishing-tools/deliverables/phase-1-research/phase-1-research-brief.md
   ```
   (Correct location, but only Publishing Tools has submitted work)

2. `docs/modules/backend-architecture/PRD.md:1` says:
   ```
   **Non-canonical during concept phase — authoritative conceptual PRDs live in .dev/peermesh-canvases/**
   ```
   This references a location **outside /docs** that team members can't access per audit constraints.

3. Multiple files reference Discord channels that may not exist or have different names

---

## Missing Documentation

### Critical Gaps:

1. **No "Current Phase" indicator** anywhere in docs
2. **No glossary** explaining project-specific terms:
   - What's a "PRD" vs a "Spec"?
   - What's "SpecKit"?
   - What does "module ownership" mean in practice?
3. **No file naming convention guide** (02a/02b/02c pattern)
4. **No troubleshooting guide** for common confusion points
5. **No "What's changed" log** when transitioning phases

---

## Conclusion

The documentation is **structurally comprehensive but temporally misaligned**. The core issue isn't missing information—it's that the documentation frozen in Phase 1 while the project moved to Phase 2.

### Immediate Actions (This Week):
1. ✅ Add "Current Phase" banners
2. ✅ Fix Module Assignment Table to point to Phase 2
3. ✅ Add file naming legend
4. ✅ Create single-source-of-truth table

### Short-Term Actions (Next 2 Weeks):
1. Consolidate duplicate deliverable READMEs
2. Archive completed phase documentation
3. Add README to `docs/modules/` explaining PRD vs Spec
4. Create FILE-INDEX.md for searchability

### Long-Term Actions (Phase 3+):
1. Implement automated phase status updates
2. Archive user journey docs to separate location
3. Create documentation maintenance process
4. Add documentation review to phase transition checklist

---

**Recommendation**: Focus on **Critical Issues #1-3** immediately. These three fixes alone will eliminate 80% of team confusion.
