# Reorganization Proposal: Root-Level Files & Publishing Module

**Date**: 2025-01-16  
**Status**: Awaiting Approval  
**Scope**: Root-level files/directories (excluding `/docs` and `/modules`) + Publishing-related directories

---

## Executive Summary

This proposal reorganizes root-level documentation files and publishing-related directories to establish clear organization, reduce clutter, and separate work-in-progress from final deliverables.

---

## Current Problems

### 1. Root-Level File Clutter (15 files to move + 2 keepers = 17 total)
**Problem**: Too many documentation files at root level reduce discoverability.

**Files to relocate**:
- `START-HERE.md` → Getting started docs
- `QUICKSTART.md` → Getting started docs
- `DEMO-QUICKSTART.md` → Getting started docs
- `DOCKER-SETUP.md` → Operations docs
- `DOCKER-DATABASE-SETUP.md` → Operations docs
- `DOCKER-FIRST-POLICY.md` → Operations docs
- `DATABASE-RESET.md` → Operations docs
- `POSTGRES-RUNNING.md` → Operations docs
- `EMAIL-SETUP-INSTRUCTIONS.md` → Operations docs
- `VERIFICATION-GUIDE.md` → Operations docs
- `IMPLEMENTATION-STATUS.md` → Status tracking
- `IMPLEMENTATION-SUMMARY.md` → Status tracking
- `INTEGRATION-READINESS.md` → Status tracking
- `demo-frontend.html` → Operations/demos
- `start-demo.sh` → Operations/demos
- `docker-compose.yml` → **KEEP** (essential config)
- `organize-docs+dirs.md` → **KEEP** (this reorganization document)

### 2. Publishing Module: Deep Nesting (Up to 16 levels)
**Problem**: Excessive nesting makes navigation difficult.

**Example**:
- `docs/team/deliverables/handoffs/publishing-tools/email-integration/working-example/node_modules/@aws-sdk/core/dist-types/ts3.4/submodules/protocols/json/experimental` (16 levels)

### 3. Publishing Module: Node Modules in Repository
**Problem**: `node_modules/` should never be committed to git.

**Location**:
- `docs/team/deliverables/handoffs/publishing-tools/email-integration/working-example/node_modules/`

### 4. Publishing Module: Mixed Deliverables Locations
**Problem**: Publishing deliverables exist in multiple locations:
- `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/` (18 files)
- `docs/team/deliverables/handoffs/publishing-tools/` (email-integration handoff)
- `docs/team/deliverables/phase-1-research/publishing-tools/` (research files)
- `docs/team/module-reviews/publishing/` (module review files) - **NEW from master merge**

**Impact**: Unclear where to find final, approved deliverables.

---

## Proposed Structure

### Mental Model: Creation vs. Consumption

**Creation Zone (Kitchen)**: Where work happens - drafts, raw notes, AI outputs  
**Consumption Zone (Dining Room)**: Where work is presented - deliverables, handoffs, READMEs  
**Configuration Zone**: Essential config files at root  
**Operations Zone**: DevOps and operational documentation

---

## Proposed Directory Tree

```
knowledge-graph-lab/
├── README.md                          # KEEP: Main entry point
├── docker-compose.yml                 # KEEP: Essential config
├── Dockerfile                         # KEEP: Essential config
├── pyproject.toml                     # KEEP: Essential config (if exists)
├── requirements.txt                   # KEEP: Essential config (if exists)
├── pytest.ini                         # KEEP: Essential config (if exists)
├── package.json                       # KEEP: Essential config (if exists)
├── organize-docs+dirs.md             # KEEP: Reorganization guide
│
├── scripts/                           # KEEP: Build/deployment scripts
│   ├── test_api_paths.sh
│   └── verify_routes.py
│
├── src/                               # KEEP: Source code
├── tests/                             # KEEP: Test code
├── .dev/                              # KEEP: Development artifacts
├── .pytest_cache/                     # KEEP: Test cache
│
├── docs/                              # REORGANIZE
│   ├── getting-started/               # NEW: Entry points
│   │   ├── START-HERE.md             # MOVED from root
│   │   ├── QUICKSTART.md             # MOVED from root
│   │   └── DEMO-QUICKSTART.md        # MOVED from root
│   │
│   ├── operations/                    # NEW: Operations docs
│   │   ├── docker/
│   │   │   ├── DOCKER-SETUP.md       # MOVED from root
│   │   │   ├── DOCKER-DATABASE-SETUP.md
│   │   │   └── DOCKER-FIRST-POLICY.md
│   │   ├── database/
│   │   │   ├── DATABASE-RESET.md     # MOVED from root
│   │   │   └── POSTGRES-RUNNING.md   # MOVED from root
│   │   ├── email/
│   │   │   └── EMAIL-SETUP-INSTRUCTIONS.md  # MOVED from root
│   │   ├── verification/
│   │   │   └── VERIFICATION-GUIDE.md # MOVED from root
│   │   └── demos/
│   │       ├── demo-frontend.html    # MOVED from root
│   │       └── start-demo.sh         # MOVED from root
│   │
│   ├── status/                        # NEW: Status tracking
│   │   ├── IMPLEMENTATION-STATUS.md  # MOVED from root
│   │   ├── IMPLEMENTATION-SUMMARY.md # MOVED from root
│   │   └── INTEGRATION-READINESS.md  # MOVED from root
│   │
│   └── team/                          # REORGANIZE PUBLISHING
│       ├── work/                      # NEW: Creation Zone
│       │   └── module-assignments/
│       │       └── publishing-tools/
│       │           ├── raw/
│       │           ├── ai-generated/
│       │           ├── synthesis/
│       │           └── phases/
│       │               ├── phase-1-research/
│       │               ├── phase-2-planning/
│       │               └── phase-3-mvp/
│       │
│       └── deliverables/              # RESTRUCTURED: Consumption Zone
│           ├── phase-1-research/
│           │   └── publishing-tools/
│           ├── phase-3-mvp/           # NEW
│           │   └── publishing-tools/  # MOVED from module-assignments
│           │       └── [18 phase-3-mvp files]
│           └── handoffs/
│               └── publishing-tools/
│                   └── email-integration/  # CLEANED (no node_modules)
│                       └── working-example/
│                           ├── README.md   # Add npm install instructions
│                           ├── package.json
│                           └── send-test-email.js
│                           # NO node_modules/
```

---

## Directory Definitions

### Root Level
**Purpose**: Only essential configuration and entry points  
**Contents**: README, docker-compose.yml, Dockerfile, pyproject.toml, requirements.txt, pytest.ini, package.json

### docs/getting-started/
**Purpose**: Entry points for new users  
**Contents**: START-HERE.md, QUICKSTART.md, DEMO-QUICKSTART.md

### docs/operations/
**Purpose**: DevOps and operational documentation  
**Contents**: Docker setup, database management, email configuration, verification, demos

### docs/status/
**Purpose**: Project status tracking  
**Contents**: Implementation status, summaries, integration readiness

### docs/team/work/module-assignments/publishing-tools/
**Purpose**: Active work in progress (Creation Zone)  
**Contents**: Raw notes, AI-generated drafts, synthesized work

### docs/team/deliverables/
**Purpose**: Final deliverables by phase (Consumption Zone)  
**Contents**: Completed phase work, handoffs

---

## Migration Plan (Step-by-Step)

### Step 1: Create New Directory Structure
```bash
mkdir -p docs/getting-started
mkdir -p docs/operations/{docker,database,email,verification,demos}
mkdir -p docs/status
mkdir -p docs/team/work/module-assignments/publishing-tools/{raw,ai-generated,synthesis,phases/phase-1-research,phases/phase-2-planning,phases/phase-3-mvp}
```

### Step 2: Move Root-Level Documentation Files
1. Getting started files → `docs/getting-started/`
2. Docker docs → `docs/operations/docker/`
3. Database docs → `docs/operations/database/`
4. Email docs → `docs/operations/email/`
5. Verification docs → `docs/operations/verification/`
6. Demo files → `docs/operations/demos/`
7. Status files → `docs/status/`

### Step 3: Reorganize Publishing Deliverables
1. Move `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/*` 
   → `docs/team/deliverables/phase-3-mvp/publishing-tools/`
2. Ensure `docs/team/deliverables/phase-1-research/publishing-tools/` exists (keep as-is)
3. **Keep** `docs/team/module-reviews/publishing/` as-is (not part of this reorganization)

### Step 4: Clean Up Publishing Handoffs
1. **Remove** `docs/team/deliverables/handoffs/publishing-tools/email-integration/working-example/node_modules/`
2. **Add** installation instructions to working-example README.md
3. **Verify** `.gitignore` excludes `node_modules/`

---

## Benefits

1. **Root Cleanup**: 15 files moved → 6-8 essential files remain
2. **Clear Separation**: Work vs. deliverables clearly separated
3. **Reduced Nesting**: 16 levels → 8 levels max
4. **Cleaner Repository**: No node_modules committed
5. **Better Organization**: Logical grouping by purpose
6. **Scalability**: Structure can grow without chaos

---

## Risks & Mitigations

### Risk 1: Broken Links
**Mitigation**: Systematic link checking and updating in Phase 6

### Risk 2: Team Confusion During Transition
**Mitigation**: Clear communication, maintain old structure until new one is stable

### Risk 3: Demo Scripts Broken
**Mitigation**: Update paths in scripts after moves

---

## Approval Required

**Next Step**: Review this proposal and approve before proceeding to Phase 4 (Migration Manifest).

Please review:
- [ ] Root-level file organization makes sense
- [ ] Publishing deliverables moves are appropriate
- [ ] Directory structure is logical
- [ ] No critical concerns

Once approved, we will proceed to create the detailed `MIGRATION-MANIFEST.md`.
