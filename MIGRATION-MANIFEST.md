# Migration Manifest: Root-Level Files & Publishing Module

**Date**: 2025-01-16  
**Status**: Ready for Execution  
**Phase**: 4 - Deterministic Manifest

---

## Overview

This manifest provides a comprehensive, deterministic checklist of **every file move** required for the reorganization. Each move is explicitly mapped from source to destination path.

**Total Operations**:
- **15 root-level files** to move
- **18 publishing phase-3-mvp files** to move
- **1 node_modules directory** to remove
- **Multiple directories** to create

---

## Directory Creation (Prerequisites)

Execute these directory creation commands **before** any file moves:

```bash
# Getting Started
mkdir -p docs/getting-started

# Operations
mkdir -p docs/operations/docker
mkdir -p docs/operations/database
mkdir -p docs/operations/email
mkdir -p docs/operations/verification
mkdir -p docs/operations/demos

# Status
mkdir -p docs/status

# Publishing Work Area (Creation Zone)
mkdir -p docs/team/work/module-assignments/publishing-tools/raw
mkdir -p docs/team/work/module-assignments/publishing-tools/ai-generated
mkdir -p docs/team/work/module-assignments/publishing-tools/synthesis
mkdir -p docs/team/work/module-assignments/publishing-tools/phases/phase-1-research
mkdir -p docs/team/work/module-assignments/publishing-tools/phases/phase-2-planning
mkdir -p docs/team/work/module-assignments/publishing-tools/phases/phase-3-mvp

# Publishing Deliverables (Consumption Zone)
mkdir -p docs/team/deliverables/phase-3-mvp/publishing-tools
```

**Verification**: Run `find docs/getting-started docs/operations docs/status docs/team/work docs/team/deliverables/phase-3-mvp -type d 2>/dev/null | wc -l` - should show all directories created.

---

## Category 1: Root-Level Files → Getting Started (3 files)

| # | Source Path | Destination Path | Status |
|---|-------------|------------------|--------|
| 1 | `START-HERE.md` | `docs/getting-started/START-HERE.md` | ⬜ |
| 2 | `QUICKSTART.md` | `docs/getting-started/QUICKSTART.md` | ⬜ |
| 3 | `DEMO-QUICKSTART.md` | `docs/getting-started/DEMO-QUICKSTART.md` | ⬜ |

**Command**:
```bash
git mv START-HERE.md docs/getting-started/START-HERE.md
git mv QUICKSTART.md docs/getting-started/QUICKSTART.md
git mv DEMO-QUICKSTART.md docs/getting-started/DEMO-QUICKSTART.md
```

---

## Category 2: Root-Level Files → Operations/Docker (3 files)

| # | Source Path | Destination Path | Status |
|---|-------------|------------------|--------|
| 4 | `DOCKER-SETUP.md` | `docs/operations/docker/DOCKER-SETUP.md` | ⬜ |
| 5 | `DOCKER-DATABASE-SETUP.md` | `docs/operations/docker/DOCKER-DATABASE-SETUP.md` | ⬜ |
| 6 | `DOCKER-FIRST-POLICY.md` | `docs/operations/docker/DOCKER-FIRST-POLICY.md` | ⬜ |

**Command**:
```bash
git mv DOCKER-SETUP.md docs/operations/docker/DOCKER-SETUP.md
git mv DOCKER-DATABASE-SETUP.md docs/operations/docker/DOCKER-DATABASE-SETUP.md
git mv DOCKER-FIRST-POLICY.md docs/operations/docker/DOCKER-FIRST-POLICY.md
```

---

## Category 3: Root-Level Files → Operations/Database (2 files)

| # | Source Path | Destination Path | Status |
|---|-------------|------------------|--------|
| 7 | `DATABASE-RESET.md` | `docs/operations/database/DATABASE-RESET.md` | ⬜ |
| 8 | `POSTGRES-RUNNING.md` | `docs/operations/database/POSTGRES-RUNNING.md` | ⬜ |

**Command**:
```bash
git mv DATABASE-RESET.md docs/operations/database/DATABASE-RESET.md
git mv POSTGRES-RUNNING.md docs/operations/database/POSTGRES-RUNNING.md
```

---

## Category 4: Root-Level Files → Operations/Email (1 file)

| # | Source Path | Destination Path | Status |
|---|-------------|------------------|--------|
| 9 | `EMAIL-SETUP-INSTRUCTIONS.md` | `docs/operations/email/EMAIL-SETUP-INSTRUCTIONS.md` | ⬜ |

**Command**:
```bash
git mv EMAIL-SETUP-INSTRUCTIONS.md docs/operations/email/EMAIL-SETUP-INSTRUCTIONS.md
```

---

## Category 5: Root-Level Files → Operations/Verification (1 file)

| # | Source Path | Destination Path | Status |
|---|-------------|------------------|--------|
| 10 | `VERIFICATION-GUIDE.md` | `docs/operations/verification/VERIFICATION-GUIDE.md` | ⬜ |

**Command**:
```bash
git mv VERIFICATION-GUIDE.md docs/operations/verification/VERIFICATION-GUIDE.md
```

---

## Category 6: Root-Level Files → Operations/Demos (2 files)

| # | Source Path | Destination Path | Status |
|---|-------------|------------------|--------|
| 11 | `demo-frontend.html` | `docs/operations/demos/demo-frontend.html` | ⬜ |
| 12 | `start-demo.sh` | `docs/operations/demos/start-demo.sh` | ⬜ |

**Command**:
```bash
git mv demo-frontend.html docs/operations/demos/demo-frontend.html
git mv start-demo.sh docs/operations/demos/start-demo.sh
```

---

## Category 7: Root-Level Files → Status (3 files)

| # | Source Path | Destination Path | Status |
|---|-------------|------------------|--------|
| 13 | `IMPLEMENTATION-STATUS.md` | `docs/status/IMPLEMENTATION-STATUS.md` | ⬜ |
| 14 | `IMPLEMENTATION-SUMMARY.md` | `docs/status/IMPLEMENTATION-SUMMARY.md` | ⬜ |
| 15 | `INTEGRATION-READINESS.md` | `docs/status/INTEGRATION-READINESS.md` | ⬜ |

**Command**:
```bash
git mv IMPLEMENTATION-STATUS.md docs/status/IMPLEMENTATION-STATUS.md
git mv IMPLEMENTATION-SUMMARY.md docs/status/IMPLEMENTATION-SUMMARY.md
git mv INTEGRATION-READINESS.md docs/status/INTEGRATION-READINESS.md
```

---

## Category 8: Publishing Phase-3-MVP Deliverables (18 files)

**Source Directory**: `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/`  
**Destination Directory**: `docs/team/deliverables/phase-3-mvp/publishing-tools/`

| # | Source Path | Destination Path | Status |
|---|-------------|------------------|--------|
| 16 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/api-paths-verification-plan.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/api-paths-verification-plan.md` | ⬜ |
| 17 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/api-paths-verification-results.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/api-paths-verification-results.md` | ⬜ |
| 18 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/configuration-fixes-verification.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/configuration-fixes-verification.md` | ⬜ |
| 19 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/container-names-and-ports-plan.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/container-names-and-ports-plan.md` | ⬜ |
| 20 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/container-names-and-ports-results.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/container-names-and-ports-results.md` | ⬜ |
| 21 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/docker-setup-guide.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/docker-setup-guide.md` | ⬜ |
| 22 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/migration-implementation-plan.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/migration-implementation-plan.md` | ⬜ |
| 23 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/migration-implementation-summary.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/migration-implementation-summary.md` | ⬜ |
| 24 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/migration-test-results-final.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/migration-test-results-final.md` | ⬜ |
| 25 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/migration-test-results.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/migration-test-results.md` | ⬜ |
| 26 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/quickstart-update-plan.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/quickstart-update-plan.md` | ⬜ |
| 27 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/quickstart-update-results.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/quickstart-update-results.md` | ⬜ |
| 28 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/response-format-standardization-results.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/response-format-standardization-results.md` | ⬜ |
| 29 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/rfc7807-error-handling-results.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/rfc7807-error-handling-results.md` | ⬜ |
| 30 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/schema-naming-plan.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/schema-naming-plan.md` | ⬜ |
| 31 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/schema-naming-results.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/schema-naming-results.md` | ⬜ |
| 32 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/sqlalchemy-warning-fix-plan.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/sqlalchemy-warning-fix-plan.md` | ⬜ |
| 33 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/sqlalchemy-warning-fix-results.md` | `docs/team/deliverables/phase-3-mvp/publishing-tools/sqlalchemy-warning-fix-results.md` | ⬜ |

**Command** (batch move):
```bash
git mv docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/*.md docs/team/deliverables/phase-3-mvp/publishing-tools/
```

**Alternative** (if batch fails, move individually):
```bash
for file in docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/*.md; do
  git mv "$file" docs/team/deliverables/phase-3-mvp/publishing-tools/
done
```

---

## Category 9: Cleanup Operations

### 9.1 Remove node_modules Directory

| # | Action | Path | Status |
|---|--------|------|--------|
| 34 | **Remove** | `docs/team/deliverables/handoffs/publishing-tools/email-integration/working-example/node_modules/` | ⬜ |

**Command**:
```bash
git rm -r docs/team/deliverables/handoffs/publishing-tools/email-integration/working-example/node_modules
```

**Note**: If `node_modules/` is not tracked by git, use:
```bash
rm -rf docs/team/deliverables/handoffs/publishing-tools/email-integration/working-example/node_modules
```

### 9.2 Update .gitignore (if needed)

| # | Action | Path | Status |
|---|--------|------|--------|
| 35 | **Verify/Add** | `.gitignore` contains `node_modules/` | ⬜ |

**Command**:
```bash
grep -q "node_modules" .gitignore || echo "node_modules/" >> .gitignore
```

### 9.3 Add README to working-example (if missing)

| # | Action | Path | Status |
|---|--------|------|--------|
| 36 | **Create/Update** | `docs/team/deliverables/handoffs/publishing-tools/email-integration/working-example/README.md` | ⬜ |

**Content to add**:
```markdown
## Installation

This example requires Node.js dependencies. Install them with:

\`\`\`bash
npm install
\`\`\`

## Usage

See \`send-test-email.js\` for the working example.
```

---

## Category 10: Remove Empty Directories (Post-Move Cleanup)

After all moves are complete, remove empty parent directories:

| # | Directory to Remove | Condition | Status |
|---|---------------------|-----------|--------|
| 37 | `docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/` | If empty after moves | ⬜ |
| 38 | `docs/team/module-assignments/publishing-tools/deliverables/` | If empty | ⬜ |

**Command** (only if directories are empty):
```bash
# Check if empty first
find docs/team/module-assignments/publishing-tools/deliverables -type d -empty -delete
```

**Note**: Do not remove `docs/team/module-assignments/publishing-tools/` - it may contain other work files.

---

## Execution Checklist

### Pre-Execution
- [ ] Review this manifest for accuracy
- [ ] Ensure working directory is clean (`git status`)
- [ ] Create backup branch: `git branch backup-pre-reorganization`
- [ ] Verify all source files exist

### Execution Steps
- [ ] **Step 1**: Create all directories (see "Directory Creation" section)
- [ ] **Step 2**: Move root-level files (Categories 1-7, 15 files)
- [ ] **Step 3**: Move publishing phase-3-mvp files (Category 8, 18 files)
- [ ] **Step 4**: Cleanup operations (Category 9)
- [ ] **Step 5**: Remove empty directories (Category 10)

### Post-Execution Verification
- [ ] Verify all files moved: `git status` shows moves, not deletions
- [ ] Verify no broken moves: `git status` shows no untracked duplicates
- [ ] Verify node_modules removed: `ls docs/team/deliverables/handoffs/publishing-tools/email-integration/working-example/` shows no `node_modules/`
- [ ] Verify root is clean: `ls -1 *.md *.html *.sh 2>/dev/null` only shows kept files
- [ ] Test a moved file: `cat docs/getting-started/START-HERE.md` works
- [ ] Commit changes: `git commit -m "reorganize: move root docs and publishing deliverables per MIGRATION-MANIFEST.md"`

---

## Rollback Plan

If something goes wrong:

1. **Abort current changes**:
   ```bash
   git reset --hard HEAD
   git clean -fd
   ```

2. **Restore from backup branch**:
   ```bash
   git checkout backup-pre-reorganization
   git branch -D 001-publishing-module  # if needed
   git checkout -b 001-publishing-module
   ```

3. **Manual rollback** (if needed):
   - Check `git log` for commit hash before reorganization
   - `git checkout <commit-hash> -- <file-path>` for each moved file

---

## Summary

- **Total File Moves**: 33 files (15 root + 18 publishing)
- **Total Cleanup Actions**: 3 (node_modules removal, .gitignore check, README update)
- **Total Empty Dir Removals**: 2 (conditional)
- **Total Operations**: 38

**Estimated Time**: 5-10 minutes  
**Risk Level**: Low (all moves are tracked by git)

---

**Ready for execution!** ✅
