# Migration Manifest

**Date:** 2025-11-22
**Purpose:** Deterministic map of all file movements for the module reorganization.

## 1. Backend Architecture Module

**Status:** Standardize Structure Only (Add missing dirs)

- [x] `docs/team/module-assignments/backend-architecture/work-in-progress/raw/` (Created)
- [x] `docs/team/module-assignments/backend-architecture/work-in-progress/ai-generated/` (Created)
- [x] `docs/team/module-assignments/backend-architecture/work-in-progress/synthesis/` (Created)
- [x] `docs/team/module-assignments/backend-architecture/handoffs/` (Created)
- [x] `docs/team/module-assignments/backend-architecture/README.md` (Created)

## 2. AI Development Module

**Status:** Standardize Structure Only (Add missing dirs)

- [x] `docs/team/module-assignments/ai-development/work-in-progress/raw/` (Created)
- [x] `docs/team/module-assignments/ai-development/work-in-progress/ai-generated/` (Created)
- [x] `docs/team/module-assignments/ai-development/work-in-progress/synthesis/` (Created)
- [x] `docs/team/module-assignments/ai-development/handoffs/` (Created)
- [x] `docs/team/module-assignments/ai-development/README.md` (Created)

## 3. Frontend Design Module (The Cleanup)

### 3.1 Root Cleanup (Already Partially Executed)

*   `docs/team/module-assignments/frontend-design/raw/` -> Moved to `work-in-progress/raw/` (Done)
*   `docs/team/module-assignments/frontend-design/ai-generated/` -> Moved to `work-in-progress/ai-generated/` (Done)
*   `docs/team/module-assignments/frontend-design/synthesis/` -> Deleted (Empty) (Done)

### 3.2 Research Flattening Strategy

**Source Directory:** `docs/team/module-assignments/frontend-design/deliverables/phase-1-research/original-research/`
**Target Directories:**
1.  `docs/team/module-assignments/frontend-design/deliverables/phase-1-research/research-briefs/` (For synthesized/final docs)
2.  `docs/team/module-assignments/frontend-design/deliverables/phase-1-research/research-raw/` (For messy AI outputs)

#### File Mapping Table

| Original Path (relative to original-research/) | New Path (relative to phase-1-research/) | Notes |
| :--- | :--- | :--- |
| **ComponentLibrary-DesignSystem/** | | |
| `ComponentLibrary-DesignSystem/brief.md` | `research-raw/ComponentLibrary-DesignSystem/brief.md` | Context |
| `ComponentLibrary-DesignSystem/prompt.md` | `research-raw/ComponentLibrary-DesignSystem/prompt.md` | Context |
| `ComponentLibrary-DesignSystem/*-FINAL.md` | `research-briefs/ComponentLibrary-DesignSystem-Part*.md` | **Key Move** |
| `ComponentLibrary-DesignSystem/response-*/` | `research-raw/ComponentLibrary-DesignSystem/response-*/` | Keep structure deep inside raw |
| **DataArchitecture-ContentManagement/** | | |
| `DataArchitecture-ContentManagement/FINAL.md` | `research-briefs/DataArchitecture-ContentManagement.md` | **Key Move** |
| `DataArchitecture-ContentManagement/responses/` | `research-raw/DataArchitecture-ContentManagement/responses/` | |
| **InteractiveGraphVisualization/** | | |
| `InteractiveGraphVisualization/FINAL.md` | `research-briefs/InteractiveGraphVisualization.md` | **Key Move** |
| `InteractiveGraphVisualization/responses/` | `research-raw/InteractiveGraphVisualization/responses/` | |
| **Performance-Monitoring-Optimization/** | | |
| `Performance-Monitoring-Optimization/FINAL.md` | `research-briefs/Performance-Monitoring-Optimization.md` | **Key Move** |
| `Performance-Monitoring-Optimization/responses/` | `research-raw/Performance-Monitoring-Optimization/responses/` | |
| **RealtimeCollaboration-Updates/** | | |
| `RealtimeCollaboration-Updates/FINAL.md` | `research-briefs/RealtimeCollaboration-Updates.md` | **Key Move** |
| `RealtimeCollaboration-Updates/responses/` | `research-raw/RealtimeCollaboration-Updates/responses/` | |
| **Search-Filter-InformationArchitecture/** | | |
| `Search-Filter-InformationArchitecture/FINAL.md` | `research-briefs/Search-Filter-InformationArchitecture.md` | **Key Move** |
| `Search-Filter-InformationArchitecture/responses/` | `research-raw/Search-Filter-InformationArchitecture/responses/` | |
| **StateManagement-ReactPatterns/** | | |
| `StateManagement-ReactPatterns/FINAL.md` | `research-briefs/StateManagement-ReactPatterns.md` | **Key Move** |
| `StateManagement-ReactPatterns/responses/` | `research-raw/StateManagement-ReactPatterns/responses/` | |

## 4. Documentation Updates Required

After file moves, update these files to point to new locations:

1.  `docs/team/README.md`
2.  `docs/team/onboarding.md`
3.  `docs/team/module-assignments/frontend-design/README.md`
4.  `docs/team/module-assignments/frontend-design/02-phase-1-research/02b-phase-1-research-assignment.md`

---

**Approval:** Ready to execute?

