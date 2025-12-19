# Official RequirementsKit Workflow

**Purpose**: Define the complete end-to-end process from requirements gathering to running system.

**Status**: Official terminology and workflow (2025-10-09)

---

## Visual Dependency Flow: Work Orders WO-1 through WO-5

**Purpose**: High-level view of the 5-phase PRD creation process showing sequential dependencies and time estimates.

**For detailed methodology, see:** [methodology.md](methodology.md)

```
┌─────────────────────────────────────────────────────────────────┐
│ START: Module PRD Creation                                     │
│ Input: User conversations, requirements, existing docs         │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ WO-1: Conversation Distillation                                │
│ Time: 2-3 hours                                                 │
│ Input: Raw conversations, notes, requirements                  │
│ Output: MVP decisions document + distilled requirements        │
│ Deliverable: 00-{module}-decisions.md                         │
│                                                                 │
│ Tasks:                                                          │
│ • T1: Read all conversations (1-1.5 hours)                    │
│ • T2: Create MVP decisions document (1-1.5 hours)             │
│ • T3: Distill requirements list (30-45 minutes)               │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ WO-2: Information Gathering                                    │
│ Time: 4-6 hours                                                 │
│ Input: Distilled requirements from WO-1                        │
│ Output: Research complete, gaps identified, contracts defined  │
│ Deliverables: Source index, gaps document, integration contracts│
│                                                                 │
│ Tasks:                                                          │
│ • T4: Create information sources index (30 min)               │
│ • T5: Identify information needs (45 min)                     │
│ • T6: Research and gap closure (2-3 hours)                    │
│ • T7: Create gaps document (30-45 min)                        │
│ • T8: Create integration contracts (1-2 hours)                │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ WO-3: Comprehensive Spec Creation                              │
│ Time: 8-10 hours                                                │
│ Input: All outputs from WO-2 + template                        │
│ Output: Detailed comprehensive spec (800-1500 lines)           │
│ Deliverable: 05-COMPREHENSIVE-SPEC.md                         │
│                                                                 │
│ Tasks:                                                          │
│ • T9-T18: Fill all 10 sections of PRD template                │
│   (45-60 minutes per section)                                  │
│ • Comprehensive detail (not final abstraction yet)             │
│ • Include SQL DDL, detailed examples, all assumptions          │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ WO-4: Quality Refinement                                       │
│ Time: 3-4 hours                                                 │
│ Input: Comprehensive spec (800-1500 lines) + case study       │
│ Output: Refined PRD (500-700 lines)                            │
│ Deliverable: 10-FINAL-SPEC.md                                 │
│                                                                 │
│ Tasks:                                                          │
│ • T19: Quality comparison vs case study (45-60 min)           │
│ • T20: Refinement pass (2-3 hours)                            │
│   - Remove redundancy                                           │
│   - Elevate abstraction (remove implementation details)        │
│   - Compress to 500-700 lines                                  │
│ • T21: Final polish (30-45 min)                               │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ WO-5: Validation & Learnings                                   │
│ Time: 3-4 hours                                                 │
│ Input: Final spec + validation checklists                      │
│ Output: GO/NO-GO decision with validation evidence             │
│ Deliverable: 11-IMPLEMENTATION-READINESS.md                   │
│                                                                 │
│ Tasks:                                                          │
│ • T18: Completeness validation (30 min)                       │
│ • T19: Quality comparison + technical accuracy (1.5-2.5 hrs)  │
│ • T20: MVP scope verification (15-20 min)                     │
│ • T21: Integration point verification (20-30 min)             │
│ • T22: Final spec confirmation (15 min)                       │
│ • T23: GO/NO-GO decision (15-20 min)                          │
│ • T24: Capture learnings (30-45 min)                          │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ├────────────────┬────────────────┐
                  │                │                │
                  ▼                ▼                ▼
┌─────────────────────┐  ┌──────────────────┐  ┌────────────────┐
│ GO Decision         │  │ NO-GO Decision   │  │ Optional       │
│ Recommendation:     │  │ Recommendation:  │  │ WO-5.5:        │
│ Proceed to /plan    │  │ Address blockers │  │ Deep Technical │
│                     │  │ Fix critical gaps│  │ Review         │
│ Output:             │  │ Re-run validation│  │ (3-4 hours)    │
│ • Spec ready        │  │                  │  │ 8-category     │
│ • /plan can execute │  │ Then retry WO-5  │  │ validation     │
│ • Development start │  │                  │  │                │
└─────────────────────┘  └──────────────────┘  └────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ TOTAL TIME: 20-27 hours (typical module)                       │
│ After system improvements: 15-19 hours (3-6 hour savings)      │
└─────────────────────────────────────────────────────────────────┘
```

**Key Principles:**
- **Sequential dependency**: Cannot start WO-N+1 until WO-N completes
- **MVP scope lock**: Define in WO-1, validate in WO-5 (no scope creep between)
- **Comprehensive → Refined**: WO-3 captures all detail, WO-4 compresses to final
- **GO/NO-GO evidence**: Decision based on validation checklist results, not assumptions

---

## Official Terminology

**For complete terminology definitions, see: [../reference/terminology.md](../reference/terminology.md)**

### Quick Reference

**The Three Documents**:
1. **Comprehensive Source** (`05-COMPREHENSIVE-SPEC.md`) - Detailed input we create (800-1500 lines)
2. **SpecKit Specification** (`08-{module}-speckit-output.md`) - What SpecKit produces
3. **Implementation Specification** (`10-FINAL-SPEC.md`) - Final deliverable (500-700 lines)

**Alternate terms**: You may also hear these called PRD, Feature Specification, and Refined Feature Specification. See terminology.md for complete mapping.

### The Complete SpecKit Command Sequence

| Command | Input | Output | Purpose |
|---------|-------|--------|---------|
| `/constitution` | Project principles | constitution.md | Define project values |
| `/specify` | Comprehensive Source | SpecKit Specification | Transform requirements to formal spec |
| `/plan` | SpecKit Specification | Implementation plan | Design implementation approach |
| `/tasks` | Implementation plan | Task list | Break plan into executable tasks |
| `/implement` | Task list | Working code | Execute tasks to build system |

---

## Complete Workflow Visualization

```
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 1: PREPARATION (RequirementsKit)                             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ├─ Information Gathering
                              ├─ Interrelationship Mapping
                              ├─ Gap Identification
                              └─ Comprehensive Source Creation
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ DOCUMENT 1: Comprehensive Source (500-1000 lines)                  │
│ File: {module}-comprehensive-source.md                             │
│                                                                     │
│ Contains:                                                           │
│ • Problem Statement                                                 │
│ • 5-10 Use Cases                                                    │
│ • Complete Data Model (SQL DDL)                                     │
│ • Example Workflows                                                 │
│ • Performance Targets (quantified)                                  │
│ • Implementation Phases (3-7)                                       │
│ • Edge Cases (10-20+)                                               │
│ • Technology Constraints                                            │
│ • Testing Strategy                                                  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: SpecKit Transformation                                     │
│ Command: /specify                                                   │
│ Duration: Minutes                                                   │
│ Automated: Yes (SpecKit AI processing)                             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ├─ Extracts requirements → Numbers them (FR-001, NFR-001)
                              ├─ Transforms use cases → Formal user stories
                              ├─ Creates scenarios → Given/When/Then format
                              ├─ Preserves data model → Key Entities section
                              ├─ Consolidates performance → NFR section
                              ├─ Adds SpecKit boilerplate → Execution Flow, Guidelines
                              └─ Removes meta-content → Executive summary, rationale
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ DOCUMENT 2: SpecKit Specification (Transform Output)               │
│ File: {module}-speckit-output.md                                   │
│                                                                     │
│ Contains (SpecKit format):                                          │
│ • Execution Flow (SpecKit-generated)                               │
│ • Quick Guidelines (SpecKit-generated)                             │
│ • User Scenarios & Testing (transformed from use cases)            │
│   - User Stories (US-1, US-2, ...)                                 │
│   - Acceptance Scenarios (Given/When/Then)                         │
│   - Edge Cases                                                      │
│ • Requirements (extracted and numbered)                             │
│   - Functional Requirements (FR-001 to FR-NNN)                     │
│   - Non-Functional Requirements (NFR-001 to NFR-NNN)               │
│ • Key Entities (preserved data model)                              │
│ • Implementation Phases (preserved)                                 │
│ • Success Criteria                                                  │
│ • Review & Acceptance Checklist                                    │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: Manual Refinement                                          │
│ Who: You/Team (manual review)                                      │
│ Duration: 1-3 hours                                                 │
│ Automated: No (human judgment required)                            │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ├─ Validate completeness → No requirements lost?
                              ├─ Check integration points → All interfaces documented?
                              ├─ Verify data model → Schema complete?
                              ├─ Review edge cases → All scenarios covered?
                              ├─ Validate against exclusions → No out-of-scope features added?
                              ├─ Fix any gaps → Add missing details
                              ├─ Organize requirements → Logical grouping if needed
                              └─ Final quality check → Ready for implementation?
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ DOCUMENT 3: Implementation Specification (Final)                   │
│ File: {module}-implementation-spec.md                              │
│                                                                     │
│ Same structure as Document 2, but:                                 │
│ • Gaps filled                                                       │
│ • Integration points emphasized                                     │
│ • Requirements organized optimally                                  │
│ • Edge cases complete                                               │
│ • No [NEEDS CLARIFICATION] markers                                 │
│ • Validated against exclusions                                      │
│ • Ready for /plan command                                          │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 2: SPECKIT COMMAND SEQUENCE (Spec to System)                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ COMMAND 1: /constitution (Optional - once per project)             │
│                                                                     │
│ Purpose: Define project values and principles                      │
│ Input: Project principles, coding standards, architectural rules   │
│ Output: .specify/memory/constitution.md                            │
│ Duration: 10-20 minutes                                             │
│                                                                     │
│ What it creates:                                                    │
│ • Core values (e.g., "Simplicity over complexity")                 │
│ • Coding standards (e.g., "Prefer composition over inheritance")   │
│ • Architectural rules (e.g., "Stateless modules")                  │
│ • Quality bars (e.g., "80% test coverage")                         │
│                                                                     │
│ Note: Constitution is referenced by all subsequent SpecKit commands │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ COMMAND 2: /plan                                                    │
│                                                                     │
│ Purpose: Create technical implementation plan                      │
│ Input: Implementation Specification (Document 3)                   │
│ Output: Technical plan document                                    │
│ Duration: Minutes                                                   │
│                                                                     │
│ What it creates:                                                    │
│ • Architecture decisions                                            │
│ • Component breakdown                                               │
│ • Technology stack specifics                                        │
│ • File structure                                                    │
│ • Module dependencies                                               │
│ • API design                                                        │
│ • Database schema implementation details                            │
│ • Testing approach                                                  │
│                                                                     │
│ Transforms WHAT (spec) → HOW (plan)                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ DOCUMENT 4: Technical Plan                                         │
│ File: {module}-plan.md                                             │
│                                                                     │
│ Contains:                                                           │
│ • Architectural overview                                            │
│ • Component design                                                  │
│ • Technology decisions (HOW to build)                              │
│ • File organization                                                 │
│ • Implementation approach                                           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ COMMAND 3: /tasks                                                   │
│                                                                     │
│ Purpose: Break plan into actionable implementation tasks           │
│ Input: Technical plan (Document 4)                                 │
│ Output: Task list (tasks.md)                                       │
│ Duration: Minutes                                                   │
│                                                                     │
│ What it creates:                                                    │
│ • Ordered list of tasks                                            │
│ • Each task with clear deliverable                                 │
│ • Dependencies between tasks                                        │
│ • Success criteria per task                                        │
│ • Estimated complexity                                              │
│                                                                     │
│ Transforms HOW (plan) → DO (tasks)                                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ DOCUMENT 5: Task List                                              │
│ File: tasks.md                                                      │
│                                                                     │
│ Contains:                                                           │
│ • Task 1: Create database schema                                   │
│   - Deliverable: schema.sql file                                   │
│   - Dependencies: None                                              │
│   - Success: Schema creates without errors                         │
│ • Task 2: Implement data access layer                              │
│   - Deliverable: db.py with CRUD operations                        │
│   - Dependencies: Task 1                                            │
│   - Success: All unit tests pass                                   │
│ • [... more tasks ...]                                             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ COMMAND 4: /implement                                               │
│                                                                     │
│ Purpose: Execute tasks to build the system                         │
│ Input: Task list (Document 5)                                      │
│ Output: Working code                                                │
│ Duration: Hours to days (depends on complexity)                    │
│                                                                     │
│ What it does:                                                       │
│ • Executes tasks in dependency order                               │
│ • Writes code files                                                 │
│ • Creates tests                                                     │
│ • Runs validation                                                   │
│ • Reports progress                                                  │
│                                                                     │
│ Transforms DO (tasks) → DONE (working system)                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ FINAL RESULT: Working System                                       │
│                                                                     │
│ Contains:                                                           │
│ • Source code files                                                 │
│ • Database schema                                                   │
│ • Tests (unit, integration)                                         │
│ • Documentation                                                     │
│ • Configuration files                                               │
│ • Deployment scripts                                                │
│                                                                     │
│ Ready for: Testing, deployment, production use                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Work Order Dependency Flow

**Purpose**: Shows how work orders (WO-1 through WO-5/WO-5.5) flow and block each other in module PRD creation.

**Usage**: When starting a new module (Backend, Frontend, AI, etc.), follow this sequence to create implementation-ready PRDs.

```
┌──────────────────────────────────────────────────────────────────┐
│ WO-1: Conversation Distillation (4-6 hours)                     │
│ • No dependencies - can start immediately                       │
│ • Output: Distilled insights from conversations/notes          │
│ • Deliverable: 00-{module}-decisions.md                        │
│ • Blocks: WO-2 (needs decisions before spec generation)        │
└────────────────┬─────────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ WO-2: Initial Spec Generation (1-2 hours)                       │
│ • Blocked by: WO-1 (needs distilled decisions)                 │
│ • Output: Initial spec structure (generated or manual)         │
│ • Deliverable: 02-{module}-initial-spec.md                     │
│ • Blocks: WO-3 (needs structure before expansion)              │
└────────────────┬─────────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ WO-3: Comprehensive Spec Creation (6-10 hours)                  │
│ • Blocked by: WO-2 (needs initial structure)                   │
│ • Output: Detailed, complete spec (800-1,500 lines)            │
│ • Deliverable: 05-COMPREHENSIVE-SPEC.md                        │
│ • Blocks: WO-4 (needs comprehensive content before refinement) │
└────────────────┬─────────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ WO-4: SpecKit Processing and Refinement (2-4 hours)            │
│ • Blocked by: WO-3 (needs comprehensive spec)                  │
│ • Output: Refined PRD (500-700 lines, requirements-focused)    │
│ • Deliverable: 10-FINAL-SPEC.md                                │
│ • Process:                                                      │
│   1. Compare comprehensive spec to case study benchmark        │
│   2. Remove implementation details (SQL, test suites, etc.)    │
│   3. Tighten language to match abstraction level               │
│   4. Verify against quality-comparison-checklist.md            │
│ • Blocks: WO-5 (needs final spec before validation)            │
└────────────────┬─────────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ WO-5: Validation and Implementation Readiness (2-3 hours)      │
│ • Blocked by: WO-4 (needs final spec)                          │
│ • Output: GO/NO-GO decision with validation results            │
│ • Deliverable: 11-IMPLEMENTATION-READINESS.md                  │
│ • Tasks:                                                        │
│   - T18: Completeness validation                               │
│   - T19: Quality comparison (with technical accuracy optional) │
│   - T20: MVP scope verification                                │
│   - T21: Integration point verification                        │
│   - T22: Final spec confirmation                               │
│ • Optional: WO-5.5 for deep technical review                   │
└────────────────┬─────────────────────────────────────────────────┘
                 │
                 ├─────────────────────────────────────────┐
                 │                                         │
                 ▼                                         ▼
┌────────────────────────────────────┐  ┌────────────────────────────────────┐
│ WO-5.5: Deep Technical Review      │  │ COMPLETE: PRD Ready                │
│ (Optional, 3-4 hours)              │  │ • All validations PASS             │
│ • For complex/high-risk modules    │  │ • 10-FINAL-SPEC.md complete        │
│ • Use technical-accuracy-checklist │  │ • Ready for /plan command          │
│ • 8-section deep validation        │  │ • Development team can start       │
│ • Catches technical gaps           │  └────────────────────────────────────┘
│ • Output: Technical review report  │
└────────────────┬───────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ COMPLETE: PRD Ready (with technical validation)                 │
│ • Final spec + technical review complete                        │
│ • High confidence in implementation readiness                   │
│ • Ready for /plan command                                       │
└──────────────────────────────────────────────────────────────────┘
```

### Work Order Timing Summary

| Work Order | Estimated Time | Critical Path? | Can Parallelize? |
|------------|----------------|----------------|------------------|
| WO-1: Distillation | 4-6 hours | Yes | No (foundational) |
| WO-2: Initial Spec | 1-2 hours | Yes | No (needs WO-1) |
| WO-3: Comprehensive Spec | 6-10 hours | Yes | No (needs WO-2) |
| WO-4: Refinement | 2-4 hours | Yes | No (needs WO-3) |
| WO-5: Validation | 2-3 hours | Yes | Partially (T18-T22 independent) |
| WO-5.5: Technical Review | 3-4 hours (optional) | No | Can run with WO-5 |
| **Total** | **15-25 hours** | - | - |
| **With WO-5.5** | **18-29 hours** | - | - |

### Key Insights

**Why This Sequence?**
- WO-1 establishes decisions → prevents rework in later phases
- WO-2 creates structure → faster comprehensive spec in WO-3
- WO-3 captures all details → enables effective refinement in WO-4
- WO-4 focuses requirements → produces implementation-ready PRD
- WO-5 validates completeness → GO/NO-GO decision with evidence
- WO-5.5 catches technical gaps → prevents costly implementation errors

**Time Savings vs Publishing Module:**
- Publishing baseline: ~25 hours (with rework and confusion)
- With this workflow: ~18-22 hours (15-20% time savings)
- Backend/Frontend/AI modules: Expected 3-6 hours saved each (universal system improvements)

**Blocking Relationships:**
- **Cannot start WO-2** until WO-1 complete (needs decisions)
- **Cannot start WO-3** until WO-2 complete (needs structure)
- **Cannot start WO-4** until WO-3 complete (needs content)
- **Cannot start WO-5** until WO-4 complete (needs final spec)
- **WO-5.5 is optional** and can run in parallel with WO-5

**Parallelization Opportunities:**
- WO-5 tasks (T18-T22) are mostly independent - can work on multiple at once
- WO-5.5 technical review can start as soon as WO-4 completes (doesn't wait for WO-5)
- Session log and assumptions log can be updated throughout (not blocking)

---

## Module Execution Order

**Purpose**: Explains WHY modules should be built in a specific sequence.

**Recommended Sequence**:

**1. AI Module** (Most complex, most dependencies)
- **Reason**: Other modules depend on AI capabilities
- **Learn from**: Complex data model, LLM integration
- **Validate**: Can we specify AI features clearly?

**2. Backend Module** (Foundation for others)
- **Reason**: Frontend and Publishing depend on backend
- **Learn from**: API design, data persistence
- **Validate**: Do integration points with AI work?

**3. Frontend Module** (Depends on AI + Backend)
- **Reason**: Needs both AI and Backend specs complete
- **Learn from**: UI workflows, state management
- **Validate**: Can we connect all the pieces?

**4. Publishing Module** (Depends on all others)
- **Reason**: Uses AI, Backend, and displays via Frontend
- **Learn from**: Multi-module integration
- **Validate**: Does the full system work together?

### Parallel vs Sequential

**Sequential advantages**:
- Learn from each module
- Refine template as we go
- Identify cross-module issues early

**Parallel potential**:
- AI and Backend can start together
- Frontend and Publishing wait for dependencies

---

## Timeline Estimates

### Per Module (Sequential)
- Information Gathering: 4-6 hours
- Spec Creation: 6-10 hours
- SpecKit Processing: 2-4 hours
- Validation: 2-3 hours
- **Total per module**: 14-23 hours

### All 4 Modules (Sequential)
- AI Module: 14-23 hours
- Backend Module: 12-20 hours (learning applied)
- Frontend Module: 12-20 hours
- Publishing Module: 10-18 hours
- **Total**: 48-81 hours (~6-10 working days)

### Parallel Approach
If AI + Backend done in parallel, then Frontend + Publishing:
- **Total**: 26-43 hours (~3-5 working days)

---

## Risk Mitigation

### Risk: Template doesn't match case study learnings
**Mitigation**: Review and refine template before starting modules

### Risk: Documentation gaps too large to proceed
**Mitigation**: Identify gaps early (Phase 2), resolve before spec creation

### Risk: SpecKit output loses critical details
**Mitigation**: Apply case study learnings, manual review and refinement

### Risk: Cross-module integration unclear
**Mitigation**: Integration matrix, validation phase for each module

### Risk: Time estimates too optimistic
**Mitigation**: Start with one module, refine estimates based on actual time

---

## Detailed Workflow Steps

### PHASE 1: RequirementsKit (Preparation)

#### Step 1.1: Information Gathering
**Duration**: 4-6 hours per module
**Deliverables**:
- `00-INFORMATION-GATHERING.md` - Index of all related docs
- `01-INTERRELATIONSHIPS.md` - How pieces connect
- `02-GAPS-IDENTIFIED.md` - What's missing

#### Step 1.2: Comprehensive Source Creation
**Duration**: 8-10 hours per module (WO-3 in the work order flow)
**Deliverable**: `05-COMPREHENSIVE-SPEC.md` (800-1500 lines)

**What to create**: Follow the template, fill all 10 sections:
1. Problem Statement
2. Use Cases & User Stories
3. Complete Data Model
4. Example Workflows
5. Performance Targets
6. Implementation Phases
7. Edge Cases
8. Technology Constraints
9. Testing Strategy
10. (Out of Scope validation - optional)

**Quality gate**: Use template validation checklist

---

### PHASE 2: SpecKit Transformation (Automated)

#### Step 2.1: Run /specify Command
**Command**: `/specify`
**Input**: `05-COMPREHENSIVE-SPEC.md`
**Output**: `08-{module}-speckit-output.md`
**Duration**: Minutes (AI processing)

**What SpecKit does**:
- ✅ Preserves complete data model
- ✅ Transforms use cases → user stories
- ✅ Extracts requirements → numbers them
- ✅ Creates Given/When/Then scenarios
- ✅ Consolidates performance targets
- ✅ Adds Execution Flow & Guidelines
- ❌ Removes executive summary, rationale, process docs

**Manual work**: None (automated)

---

### PHASE 3: Manual Refinement (Human Review)

#### Step 3.1: Validate SpecKit Output
**Duration**: 3-4 hours per module (WO-4: Quality Refinement)
**Input**: `05-COMPREHENSIVE-SPEC.md` (not SpecKit output - we refine the comprehensive version)
**Output**: `10-FINAL-SPEC.md`

**Validation checklist**:
- [ ] All requirements from comprehensive source preserved?
- [ ] Data model complete (all tables, columns, constraints)?
- [ ] Integration points clearly documented?
- [ ] Performance targets all quantified?
- [ ] Edge cases comprehensive?
- [ ] No [NEEDS CLARIFICATION] markers?
- [ ] No out-of-scope features added?

#### Step 3.2: Fill Gaps
**Common gaps to address**:
- Integration interfaces not detailed enough
- Cross-module dependencies unclear
- Assumptions not explicit
- Edge case scenarios incomplete

#### Step 3.3: Final Quality Check
**Deliverable**: `10-FINAL-SPEC.md` (500-700 lines, ready for validation)

**Next**: Proceed to WO-5 validation phase

---

### PHASE 4: SpecKit Command Sequence (Spec → System)

#### Step 4.1: Constitution (Optional - Once Per Project)
**Command**: `/constitution`
**When**: First time using SpecKit on this project
**Input**: Project principles, values, standards
**Output**: `.specify/memory/constitution.md`

**Example constitution content**:
```markdown
# Project Constitution

## Core Values
- Simplicity over complexity
- Explicit over implicit
- Testability over cleverness

## Architectural Rules
- Modules are standalone (no tight coupling)
- Data models are complete before implementation
- All performance targets must be measurable

## Quality Standards
- 80% test coverage minimum
- All public APIs documented
- No [NEEDS CLARIFICATION] in specs
```

#### Step 4.2: Planning
**Command**: `/plan`
**Input**: `10-FINAL-SPEC.md`
**Output**: `{module}-plan.md`
**Duration**: Minutes

**What /plan creates**:
- Architecture decisions (HOW to build)
- Component breakdown
- File structure
- API design specifics
- Database implementation details

#### Step 4.3: Task Generation
**Command**: `/tasks`
**Input**: `{module}-plan.md`
**Output**: `tasks.md`
**Duration**: Minutes

**What /tasks creates**:
- Ordered task list

#### Step 4.4: Sanity Check & Validation
**Purpose**: Verify SpecKit output matches requirements and follows constitution

**Duration**: 2-3 hours

**Step 4.4.1: File Structure Verification**
```
specs/[branch-name]/
├── spec.md              # Generated specification
├── plan.md              # Implementation plan
├── tasks.md             # Task breakdown
├── contracts/           # API specifications
└── data-model.md        # Data structures
```

**Step 4.4.2: Constitution Compliance Check**
📖 **MUST READ FIRST**: `memory/constitution.md`

**Key Requirements for ALL Modules:**

✅ **Modular Independence** (Constitution Principle II)
- Each module must function as a complete, standalone system
- Must run independently in Docker containers
- No inter-module dependencies until Phase 5 integration

✅ **Quality Gates** (Constitution Principle III)
- Must pass 5-phase review process
- Automated validation required
- Technical feasibility review required

✅ **Performance Standards** (Constitution Principle IV)
- Container startup under 30 seconds
- API response times under 500ms
- 99% uptime success rate

✅ **Development Standards**
- Docker containerization starting Phase 3
- Comprehensive automated testing (80%+ coverage)
- Complete documentation

**Step 4.4.3: Input vs Output Comparison**

**Step 1: Read Your Module Input**
📖 **Read**: `docs/team/deliverables/requirements-kit-v2/[your-module]-spec.md`

**Step 2: Read SpecKit Output**
📖 **Read**: `specs/[branch-name]/spec.md`

**Step 3: Create Missing Items List**

Compare the input spec with the output spec and document:

❌ **Missing Requirements**: Things from input that aren't in the output spec
❌ **Incorrect Implementation**: Requirements that are implemented wrong
❌ **Missing Universal Compliance**: Things that don't follow the constitution
❌ **Technical Issues**: Implementation details that don't make sense

**Common Issues to Look For:**

1. **Missing Docker Requirements**
   - Does the spec mention Docker containerization?
   - Does it specify container startup time < 30 seconds?
   - Does it include health checks?

2. **Missing Testing Requirements**
   - Are there unit tests specified?
   - Are there integration tests?
   - Is there 80%+ test coverage requirement?

3. **Missing Performance Requirements**
   - API response time < 500ms?
   - 99% uptime requirement?
   - Resource usage limits?

4. **Missing Documentation Requirements**
   - API documentation?
   - Setup instructions?
   - Troubleshooting guides?

5. **Constitution Violations**
   - Does it assume inter-module dependencies too early?
   - Does it skip required quality gates?
   - Does it ignore evidence-based decision requirements?

**Step 4.4.4: Update the Spec.md File**

**If you find missing items, update the spec.md file:**

```bash
# Edit the generated spec file
nano specs/[branch-name]/spec.md

# Add missing sections from your analysis
# Ensure all requirements from input are covered
# Ensure constitution compliance is explicit

# Add this section to document issues found:
## Issues and Gaps Identified

### Missing from SpecKit Output
- [ ] Requirement from input spec not addressed
- [ ] Constitution compliance not enforced
- [ ] Performance requirements missing

### Technical Issues
- [ ] Docker configuration incomplete
- [ ] API contracts missing
- [ ] Testing strategy unclear

### Documentation Gaps
- [ ] Missing setup instructions
- [ ] API documentation incomplete
- [ ] Troubleshooting guides missing
```

**Step 4.4.5: Docker Integration Validation**

**Verify the spec includes:**
- ✅ Dockerfile exists and is valid
- ✅ Starts in under 30 seconds
- ✅ All dependencies properly declared
- ✅ Ports properly exposed
- ✅ Health checks implemented

**Test the Docker setup:**
```bash
# If there's a Dockerfile in your module directory
cd [your-module-directory]
docker build -t [module-name] .
docker run -p [port]:[port] [module-name]

# Test endpoints
curl http://localhost:[port]/health
```

**Step 4.4.6: Document Issues and Gaps**

**For each gap identified, determine:**

1. **Is this critical?** (Blocks development)
2. **Is this enhancement?** (Can be added later)
3. **Who needs to fix it?** (You, team lead, or other developer)
4. **What's the fix?** (Specific changes needed)

**Step 4.4.7: Final Validation**

**Before proceeding to implementation:**
- [ ] All requirements from input preserved in output
- [ ] Constitution compliance verified
- [ ] Docker integration tested and working
- [ ] Issues documented with resolution plan
- [ ] Ready for `/implement` command

#### Step 4.5: Implementation
**Command**: `/implement`
**Input**: `tasks.md`
**Output**: Working code
**Duration**: Hours to days

**What /implement does**:
- Executes tasks in order
- Writes code files
- Creates tests
- Validates against spec

---

## Summary: The Three Documents & Two Steps

### Document 1: Comprehensive Source (05-COMPREHENSIVE-SPEC.md)
- **You create this** (8-10 hours using template, WO-3)
- **800-1500 lines** of detailed requirements
- **Contains** all 10 template sections with examples, SQL, workflows

### ⬇️ **STEP 1: Quality Refinement** (3-4 hours, WO-4)

### Document 2: Implementation Specification (10-FINAL-SPEC.md)
- **You refine this** (compress comprehensive spec)
- **500-700 lines** requirements-focused
- **Remove** implementation details, keep requirements and acceptance criteria

### ⬇️ **STEP 2: Validation** (3-4 hours, WO-5)

### Document 3: Validated & Ready (11-IMPLEMENTATION-READINESS.md)
- **GO/NO-GO decision** with evidence
- **Ready for /plan** command if GO
- **Final deliverable** to development team

### ⬇️ **SpecKit Commands** (/plan → /tasks → /implement)

### Final Result: Working System

---

## File Naming Conventions

> **Working directory:** This system assumes you create a `work/` directory
> in your project for active module development. Production templates are in
> `docs/team/methodologies/requirements-kit/`.

```
work/{module-name}/
├── 00-{module}-decisions.md                 # WO-1: MVP decisions and scope
├── 01-INFORMATION-SOURCES-INDEX.md          # WO-2: Source documents index
├── 02-GAPS-IDENTIFIED.md                    # WO-2: Missing information
├── 03-INTEGRATION-CONTRACTS.md              # WO-2: Interface definitions
├── 04-ASSUMPTIONS-LOG.md                    # Ongoing: Assumptions made
├── 05-COMPREHENSIVE-SPEC.md                 # WO-3: Comprehensive Source (800-1500 lines)
├── 06-SESSION-LOG.md                        # Ongoing: Work session tracking
├── 07-REFINEMENT-NOTES.md                   # WO-4: Refinement decisions
├── 08-{module}-speckit-output.md            # Optional: SpecKit /specify output
├── 09-VALIDATION-REPORT.md                  # WO-5: Validation checklist results
├── 10-FINAL-SPEC.md                         # WO-4: Final PRD (500-700 lines)
└── 11-IMPLEMENTATION-READINESS.md           # WO-5: GO/NO-GO decision
```

---

## Quick Reference

### Official Terms

| What We Say | Official Term |
|-------------|---------------|
| "The input doc" | Comprehensive Source |
| "What SpecKit spits out" | SpecKit Specification |
| "The final spec" | Implementation Specification |
| "SpecKit processing" | Transform Step |
| "Our edits after" | Refinement Step |

### Command Sequence

```
Comprehensive Source
    ↓ /specify
SpecKit Specification
    ↓ manual refinement
Implementation Specification
    ↓ /plan
Technical Plan
    ↓ /tasks
Task List
    ↓ /implement
Working System
```

---

**This is the official workflow. Use this terminology consistently throughout all documentation.**
