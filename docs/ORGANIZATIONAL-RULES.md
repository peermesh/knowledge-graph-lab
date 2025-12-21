# Organizational Rules: Knowledge Graph Lab

**Last Updated**: 2025-01-16  
**Purpose**: Maintain consistent directory structure and prevent organizational drift

---

## Core Principle: Creation vs. Consumption

Our organization follows a clear mental model:

### 🍳 Creation Zone (Kitchen)
**Where work happens** - Mutable, work-in-progress
- `docs/team/work/` - Active development
- Raw notes, drafts, AI-generated content
- Experimental and exploratory work

### 🍽️ Consumption Zone (Dining Room)
**Where work is presented** - Stable, final deliverables
- `docs/team/deliverables/` - Final, approved work
- Handoffs, completed phases
- Production-ready documentation

---

## Directory Structure Rules

### Root Level (`/`)
**ONLY** essential configuration files:
- `README.md` - Main entry point
- `docker-compose.yml`, `Dockerfile` - Essential config
- `pyproject.toml`, `requirements.txt`, `pytest.ini` - Build config
- `package.json` - Node.js config (if applicable)
- `organize-docs+dirs.md` - Reorganization guide

**DO NOT** place documentation files at root level.

### Documentation Organization

#### `docs/getting-started/`
**Purpose**: Entry points for new users  
**Contents**:
- `START-HERE.md` - Main onboarding guide
- `QUICKSTART.md` - Fast setup instructions
- `DEMO-QUICKSTART.md` - Quick demo setup

**Rule**: Keep these files **concise** and focused on getting started.

#### `docs/operations/`
**Purpose**: DevOps and operational documentation  
**Structure**:
- `operations/docker/` - Docker setup, policies, database setup
- `operations/database/` - Database management, reset procedures
- `operations/email/` - Email configuration
- `operations/verification/` - Verification and testing guides
- `operations/demos/` - Demo scripts and frontend files

**Rule**: Group by operational concern, not by file type.

#### `docs/status/`
**Purpose**: Project status tracking  
**Contents**:
- `IMPLEMENTATION-STATUS.md` - Current implementation status
- `IMPLEMENTATION-SUMMARY.md` - Implementation summaries
- `INTEGRATION-READINESS.md` - Integration readiness assessments

**Rule**: Status files should be **actionable** and regularly updated.

#### `docs/team/work/`
**Purpose**: Active work in progress (Creation Zone)  
**Structure**:
- `work/module-assignments/` - Module-specific work areas
- Raw notes, drafts, AI-generated content go here
- Work in progress that hasn't been finalized

**Rule**: Files can be moved, deleted, or restructured freely here.

#### `docs/team/deliverables/`
**Purpose**: Final deliverables (Consumption Zone)  
**Structure**:
- `deliverables/phase-1-research/` - Completed research
- `deliverables/phase-3-mvp/` - MVP deliverables
- `deliverables/handoffs/` - Handoff documentation

**Rule**: Once files are in `deliverables/`, they should be **stable**. Changes should be minimal and documented.

---

## File Naming Conventions

### Documentation Files
- Use `SCREAMING-SNAKE-CASE.md` for operational/status files
  - Examples: `DOCKER-SETUP.md`, `IMPLEMENTATION-STATUS.md`
- Use `kebab-case.md` for regular documentation
  - Examples: `getting-started.md`, `api-reference.md`

### Scripts
- Use `kebab-case.sh` for shell scripts
  - Example: `start-demo.sh`

### Demos and Examples
- Use `kebab-case.html` for HTML files
  - Example: `demo-frontend.html`

---

## Publishing Module Specific Rules

### Deliverables Organization
**Final deliverables** must be in:
```
docs/team/deliverables/phase-{N}/{module-name}/
```

**NOT** in:
- `docs/team/module-assignments/` (this is the work area)
- `docs/team/work/` (this is for active work)

### Phase Deliverables
Each phase should have its own directory:
- `phase-1-research/` - Research phase deliverables
- `phase-2-planning/` - Planning phase deliverables
- `phase-3-mvp/` - MVP phase deliverables

### Handoffs
Handoff documentation goes in:
```
docs/team/deliverables/handoffs/{module-name}/{feature-name}/
```

**Important**: 
- Include installation instructions (especially for npm dependencies)
- **NEVER** commit `node_modules/` directories
- Include `package.json` and `package-lock.json` if dependencies are needed

---

## What NEVER Goes in the Repository

### ❌ node_modules/
**Rule**: `node_modules/` directories must **never** be committed.

**Action**: 
- Add `node_modules/` to `.gitignore`
- If found, remove immediately
- Add installation instructions to README.md instead

### ❌ Large Binary Files
**Rule**: Large binary files should not be in git.

**Exceptions**: 
- Small demo assets (< 1MB) are acceptable
- Essential configuration files

### ❌ Personal Development Files
**Rule**: Personal notes, temporary files, and work-in-progress that isn't shared should not be committed.

**Action**: Keep personal work local or in `docs/team/work/` if it needs to be shared.

---

## File Organization Checklist

Before committing new files, ask:

- [ ] Is this file at the root? Should it be in `docs/`?
- [ ] Is this a deliverable? Should it be in `docs/team/deliverables/`?
- [ ] Is this work in progress? Should it be in `docs/team/work/`?
- [ ] Does this file belong in a subdirectory by concern (e.g., `operations/docker/`)?
- [ ] Is the naming convention correct?
- [ ] Are there any `node_modules/` directories I'm accidentally committing?

---

## Link Maintenance

### When Moving Files
1. **Use `git mv`** - Preserves history and helps with merge resolution
2. **Search for references** - Use `grep` to find files that reference the moved file
3. **Update links** - Update all markdown links to the new path
4. **Update README files** - Ensure README files point to correct locations

### Link Checking
Before major commits:
```bash
# Find broken references to moved files
grep -r "old-path" docs/
```

---

## Depth Limit

**Rule**: Avoid directory nesting deeper than **8 levels**.

**Before**:
```
docs/team/module-assignments/publishing-tools/deliverables/phase-3-mvp/subfolder/file.md
```

**After**:
```
docs/team/deliverables/phase-3-mvp/publishing-tools/file.md
```

**Reason**: Deep nesting makes navigation difficult and paths hard to remember.

---

## Migration Guidelines

### When Reorganizing
1. Follow the 6-phase protocol (`organize-docs+dirs.md`)
2. Create a migration manifest before moving files
3. Use `git mv` to preserve history
4. Update all references after moves
5. Update this document if rules change

### Approval Process
For major reorganizations:
1. Create proposal document
2. Review with team
3. Create migration manifest
4. Execute migration
5. Update documentation

---

## Enforcement

### Pre-Commit Checks
Before committing:
- Review `git status` for unexpected files
- Check for `node_modules/` directories
- Verify file naming conventions
- Confirm files are in correct zones (creation vs. consumption)

### Code Review Checklist
When reviewing PRs:
- [ ] Are new files in appropriate directories?
- [ ] Are root-level files only essential config?
- [ ] Are deliverables in `deliverables/`, not `work/`?
- [ ] No `node_modules/` directories?
- [ ] Links updated if files were moved?

---

## Exceptions

These rules are guidelines, not absolute. Exceptions are allowed when:
- The change improves organization
- The team agrees the exception makes sense
- The exception is documented here

**To request an exception**: Update this document with the exception and rationale.

---

## Questions or Issues?

If you're unsure where a file belongs:
1. Check this document first
2. Consider the Creation vs. Consumption principle
3. Ask: "Is this a final deliverable or work in progress?"
4. When in doubt, use `docs/team/work/` for WIP

---

**Remember**: Good organization is an ongoing effort. Regular cleanup prevents drift.
