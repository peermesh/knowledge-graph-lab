# UNIFIED PROCESS GUIDE: The Knowledge Graph Lab Standard
## Version 1.0 (2025-11-25)

**Status**: 🟢 AUTHORITATIVE
**Purpose**: Defines the single valid workflow for all development, architecture, and integration tasks. This document replaces all fragmented "sprint dashes" and "inbox notes".

---

## 1. CORE PHILOSOPHY: "The Granular Gate"

We do not "just build". We **Specify -> Validate -> Build**.

*   **Architect's Role**: Define the "What" and "How" (Tech Strategy, Contracts, Design).
*   **Developer's Role**: Execute the "Build" (Standalone Stability, Compliance).
*   **The Gate**: No code is written until the **Granular Design** is approved.

---

## 2. THE LIFECYCLE (The Unified Path)

Every feature, module, or kit must pass through these 4 Phases.

### Phase 1: Technology Strategy (The "Nov 13" Standard)
*Source: `_sprint_ai_module_nov13/PIPELINE-TECH-STRATEGY-HANDOVER.md`*
*   **Focus**: Evaluation, not Implementation.
*   **Deliverable**: A "Tech Evaluation Matrix" (Vendor/Tool options with trade-offs).
*   **Rule**: Don't write code until you know *why* you chose that stack.

### Phase 2: Granular Design (The "Inbox" Standard)
*Source: User's Inbox Directive (`grig-walk-through...`)*
*   **Focus**: Detailed specification down to the attribute level.
*   **Deliverables (Required before coding)**:
    1.  **Functional Spec**: Every API endpoint defined (inputs/outputs/security).
    2.  **Component Map**: Hierarchical tree of UI/CLI components.
    3.  **Static JSON Index**: A mapped directory of JSON files representing all API responses. **Hardcoded mocks in code are BANNED.**
    4.  **Health Check Design**: The first feature spec is always the System Health/Status page.

### Phase 3: Standalone Build (The "Nov 9" Standard)
*Source: `_sprint_nov9/ACTION-PLAN.md` & `review-process.md`*
*   **Focus**: Technical Compliance & Stability.
*   **Deliverables**:
    1.  **Dockerfile**: Must build and run in isolation.
    2.  **Tests**: Unit/Integration tests passing.
    3.  **UKIS Compliance**: Adherence to Universal Kit Interface Standards.
*   **Rule**: Fix Docker builds *first* before adding features.

### Phase 4: Integration (The "Convergence" Standard)
*   **Focus**: Moving from Standalone to Integrated.
*   **Action**: Replace "Static JSON" with real "Service-to-Service" calls based on the validated Contracts from Phase 2.

---

## 3. CRITICAL "DASH" ARTIFACTS (Integrated)

This guide formally integrates the "lost" wisdom from previous sprints:

| Source | Insight Integrated | Action |
| :--- | :--- | :--- |
| **Nov 13 Sprint** | Tech Strategy > Implementation | **Rewrite Pipeline Docs** to focus on vendor evaluation. |
| **Nov 9 Sprint** | Docker Criticality | **Docker Build** is the P0 check for every module. |
| **Module Review** | Snapshot Audits | Use `review-process.md` logic for all future audits. |
| **Design Workflow** | `Research -> Spec -> Publish` | Separate `.dev/design` (WIP) from `docs/design` (Final). |

---

## 4. EXECUTION INSTRUCTIONS (For Agents)

**When starting a task:**
1.  Check **Where am I?** (Phase 1, 2, 3, or 4?).
2.  If Phase 2 (Design) is incomplete, **STOP**. Do not write code. Generate the *Component Map* and *Static JSON* first.
3.  If Phase 3 (Build) is broken (Docker fails), **STOP**. Fix the build before adding features.

**When navigating directories:**
*   `docs/` = Authoritative / Published.
*   `.dev/` = WIP / Kitchen.
*   `modules/standalone/` = Active Codebase.
*   `archive/` = Dead ends (e.g., `peermesh-scaffolding`).

---

## 5. CURRENT STATE & NEXT STEPS
*Refer to `docs/MASTER-WORK-TRACKER.md` for the live status of all streams.*

**Immediate Application of this Process:**
*   **Website Extraction System**: Currently stalled at Phase 2. **Action**: Create Component Map & Static JSON.
*   **AI Module**: Stalled at Phase 1. **Action**: Select "Option A" (Tech Strategy) to proceed.
