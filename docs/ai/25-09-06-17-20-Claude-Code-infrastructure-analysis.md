# PeerMesh Labs Infrastructure Analysis

**Date**: September 6, 2025 17:20
**Tool**: Claude Code
**Purpose**: Analysis of existing PeerMesh Labs infrastructure and KGL status

## Infrastructure Overview

### What Was Created (September 3, 2025)

#### 1. labs-governance (Private)
- **Purpose**: Central command center for Labs program management
- **Key Components**:
  - `STRATEGIC_PLAN.md` - 5-year vision (exists)
  - `governance/INTERN_HANDBOOK.md` - Complete guide for interns
  - `governance/PROMOTION_CRITERIA.md` - Requirements for Labs → Core
  - `tracking/ACTIVE_PROJECTS.md` - Project pipeline (currently empty)
  - `tracking/INTERN_ROSTER.md` - Intern management
  - Templates for onboarding, reviews, etc.

#### 2. labs-template (Public)
- **Purpose**: Template repository for creating new intern projects
- **Key Files**:
  - `create-labs-project.sh` - Automated project creation script
  - `PRD.md` - Product Requirements Document template
  - `PROMOTION.md` - Promotion to core process guide
  - `.github/` templates for issues and PRs
  - Standard files: README, LICENSE, CONTRIBUTING

#### 3. Main README
- Infrastructure overview at `/peermesh/repo/README.md`
- Quick links and common tasks documentation

### How Projects Should Be Created

The `create-labs-project.sh` script does:
1. Creates repo from template: `labs-[project]-[intern]` naming
2. Sets as public repository
3. Configures team permissions (maintainers: admin, interns: push)
4. Sets up branch protection rules
5. Adds intern as collaborator

Expected project structure from template:
- PRD.md (product requirements)
- PROMOTION.md (path to core)
- Standard GitHub templates
- Clean README

## Knowledge Graph Lab Status

### What KGL Has (Created Today)
✅ Complete documentation structure:
- All `/docs/` subdirectories (Vision, Ontology, Reasoning, etc.)
- Packs system with templates
- Research framework
- RFCs and ADRs
- GitHub templates and CODEOWNERS

✅ GitHub configuration:
- Issues created (6 total)
- Labels (rfc, task)
- Topics added
- Now moved to personal account (grig/knowledge-graph-lab)

### What KGL is Missing (Compared to Labs Template)

#### 1. PRD.md - Product Requirements Document
Should contain:
- Problem & Goals
- Users & Use Cases
- Prior Art & Alternatives
- MVP Scope
- Success Metrics
- Risks & Mitigations
- Architecture & Interfaces
- Delivery Plan
- Deployment Plan
- Repo Plan

#### 2. PROMOTION.md
Should contain promotion criteria and process for moving to core

#### 3. Not Created via Standard Process
- KGL was manually created, not via `create-labs-project.sh`
- Different naming convention (not `labs-[project]-[intern]`)
- Now in personal account, not peermesh org

#### 4. Not Tracked in Governance
- Not listed in `tracking/ACTIVE_PROJECTS.md`
- No intern assignment in roster
- No milestone tracking

## What's Left To Do

### For KGL Specifically
1. **Add PRD.md** - Define concrete product requirements
2. **Add PROMOTION.md** - Define path to core (if applicable)
3. **Update tracking** (if staying connected to Labs program):
   - Add to ACTIVE_PROJECTS.md
   - Define milestones and timeline
   - Assign mentor

### For Intern Handoff (in 2 days)
1. **Decision Required**: 
   - Keep KGL in personal account for experimentation?
   - Create new clean repo in peermesh for interns?
   - Or give interns access to personal repo?

2. **If Creating New Intern Repo**:
   - Use `create-labs-project.sh` to create proper structure
   - Copy clean documentation from KGL
   - Leave out `docs/ai/` directory
   - Add PRD.md with clear scope

3. **Update Governance Tracking**:
   - Add project to ACTIVE_PROJECTS.md
   - Add interns to INTERN_ROSTER.md
   - Create onboarding checklist

### Strategic Questions

1. **Is KGL a Labs project?**
   - If yes: Should follow Labs structure and process
   - If no: Can remain independent in personal account

2. **Intern Access Model**:
   - Option A: Interns work in peermesh/labs-kgl-[intern]
   - Option B: Interns get access to grig/knowledge-graph-lab
   - Option C: Create clean peermesh/knowledge-graph-lab later

3. **Documentation Strategy**:
   - Current KGL has extensive docs but no PRD
   - PRD would help interns understand concrete goals
   - Need to decide: academic demo vs. production path

## Recommendation

Based on the infrastructure analysis:

1. **Keep grig/knowledge-graph-lab** as your personal experimental space
2. **Create peermesh/labs-kgl-demo** using the script for interns:
   ```bash
   ./create-labs-project.sh kgl-demo team
   ```
3. **Copy clean docs** from KGL to new repo
4. **Add PRD.md** with clear, bounded scope for interns
5. **Update governance tracking** to reflect active project

This gives you:
- Personal freedom to experiment messily
- Clean, structured environment for interns
- Proper Labs program integration
- Clear promotion path if successful