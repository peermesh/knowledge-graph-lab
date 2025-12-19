# MASTER WORK TRACKER: The Complete Parallel State
## Date: 2025-11-25
**Status**: 🔵 TRACKING (Audit Phase)
**Purpose**: A single source of truth identifying every active, stalled, and parallel work stream in the system. This document does not force convergence; it maps the reality of the complex ecosystem.

---

## 1. THE DEVELOPER STREAMS (Technical Execution)
*The team is building independent modules, focusing on compliance and functionality.*

| Module | Owner | Current Focus | Status | Location |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend** | D-JSimpson | **Reference Implementation** | 🟢 Excellent | `modules/standalone/frontend/` |
| **Backend** | gorodinskiia | **Standardization** (API Paths, Migrations) | 🟡 Needs Work | `modules/standalone/backend/` |
| **AI Module** | haejeg | **Tech Strategy** (vs Implementation) | 🟡 Pending Decision | `modules/standalone/ai/` |
| **Publishing** | bschreiber8 | **Documentation & Migrations** | ✅ Good | `modules/standalone/publishing/` |

**Critical Note**: The Backend module currently has a **Security Vulnerability** (Auth Bypass) and a **Structural Issue** (Nested Directories).

---

## 2. THE ARCHITECT STREAMS (Tooling & Kits)
*You are building the "meta-layer" to automate and standardize the work.*

| Kit | Current State | Blocker | Next Step |
| :--- | :--- | :--- | :--- |
| **Discovery Kit** | Functional but Monolithic | "Wave 5" Refactor abandoned | Connect Jinja2 templates or accept monolith |
| **Requirements Kit** | Installed v1.0 | Missing Dependencies | Install `pip install -e .` |
| **Integration Suite** | Designed | Path Errors | Fix `scripts/` vs `.dev/scripts/` |
| **Website Extraction** | **Specified** (Ready to Build) | Missing "Granular" Artifacts | Create Component Map & Health Check |

---

## 3. THE SPRINT ARTIFACTS (Rapid Iteration Results)
*Valuable intelligence trapped in temporary directories. Needs to be integrated, not deleted.*

| Source | Key Insight | Action Required |
| :--- | :--- | :--- |
| **Nov 13 Sprint** | **Tech Strategy Over Implementation**: Shift pipeline docs from "how to code" to "vendor evaluation". | Rewrite Pipeline Docs |
| **Nov 9 Sprint** | **Docker Criticality**: Identified missing Dockerfiles as key blocker. | Verify Docker builds |
| **Start Here** | **Design Workflow**: Validated the `Research -> Spec -> Publish` lifecycle. | Enforce in Design Kit |
| **Module Review** | **Gap Analysis**: Detailed per-module feedback lists. | Ensure developers see their specific lists |

---

## 4. THE INBOX STREAMS (User Directives)
*Specific methodologies defined by the User that usually get ignored by "fast" agents.*

*   **The "Granular Layer" Process**: A strict requirement for detailed specs, component maps, and static JSON mocks *before* coding.
*   **The "Health Check" First**: Building monitoring before features.
*   **The "Roadmap" Logic**: A dynamic pathing system for user navigation (found in `roadmap.md`).

---

## 5. THE INFRASTRUCTURE & MAINTENANCE
*   **Security**: Critical Backend Auth Patch (Ready to apply).
*   **Sprawl**: `peermesh-scaffolding` (Shadow Architecture) needs archiving.
*   **Testing**: `integration-testing-copy-one` (Duplicate) needs deletion.

---

## 6. NEXT STEPS (Tracking Mode)
This document serves as the index. We are not forcing these into one line yet. We are ensuring:
1.  **Developers** get their specific Gap Analysis (from Nov 17).
2.  **Kits** get unblocked (Paths/Dependencies).
3.  **Security** gets patched.
4.  **Sprint Insights** don't get lost (they need to move to `docs/design` or `docs/strategy`).
