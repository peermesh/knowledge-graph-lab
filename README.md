# Knowledge Graph Lab

An AI-powered research platform that transforms information chaos into actionable intelligence.

## What We're Building

A system that discovers opportunities, understands relationships, and delivers personalized insights.

### Core Capabilities
- **Discovers** - Continuously monitors hundreds of sources
- **Understands** - Builds knowledge graphs of relationships  
- **Reasons** - Identifies patterns and opportunities
- **Delivers** - Distributes insights through multiple channels

## Architecture Overview

The platform consists of four integrated modules that must follow shared interoperability standards:

- **Backend Infrastructure** - Docker, databases, APIs, authentication
- **Frontend Interface** - React UI, visualizations, user experience
- **AI Intelligence** - LLMs, knowledge graphs, RAG, entity extraction
- **Publishing System** - Multi-channel distribution, personalization

### ⚡ Shared Module Requirements (Critical)
All modules follow a two-level interoperability system:

**🚀 Standalone Module (MVP - Required):** Basic interoperability for immediate implementation
**[Standalone Module Requirements](docs/modules/shared/standalone-modules/README.md)** - Docker containers, PostgreSQL, basic APIs

**🔬 PeerMesh Module (Advanced - Optional):** Sophisticated features for stretch goals
**[PeerMesh Module Requirements](docs/modules/shared/peermesh-modules/README.md)** - Multi-database, parallel search, event-driven architecture

**Quick Reference:** [SHARED-MODULE-REQUIREMENTS-QUICK-REF.md](docs/modules/SHARED-MODULE-REQUIREMENTS-QUICK-REF.md) - Complete checklist and agent prompts

**Quick validation:** `python3 scripts/validate-standalone-compliance.py docs/modules/backend-architecture/Backend-Architecture-Spec.md`

## Development Kits

This repository includes production-ready development kits for specification and design work.

### RequirementsKit: Requirements Development System

**RequirementsKit** creates comprehensive requirements documentation that feeds into SpecKit's `/specify` command for implementation-ready specifications.

**Quick Start:**

- **Documentation:** [.dev/kits/requirements-kit/README.md](.dev/kits/requirements-kit/README.md)
- **5-Step Guide:** [.dev/kits/requirements-kit/guides/quickstart.md](.dev/kits/requirements-kit/guides/quickstart.md)
- **Extract to Your Project:** [.dev/pre-spec-kit/package-extraction.md](.dev/pre-spec-kit/package-extraction.md)

**Version:** 1.0.0 (2025-10-09)

### Design Kit: UX/UI Design Specifications

**Design Kit** generates comprehensive UX/UI design specifications through a 5-phase workflow:

1. Context Intake - Gather project context and requirements
2. Information Architecture - Design information organization and navigation
3. Interaction Design - Define interaction patterns and user flows
4. Visual Design - Create visual design system and component styling
5. Implementation Guidelines - Generate technical implementation standards

**Quick Start:**

```bash
.dev/kits/design-kit/scripts/bash/create-design-workspace.sh \
  --phase context-intake \
  "Your project description"
```

- **Documentation:** [.dev/kits/design-kit/README.md](.dev/kits/design-kit/README.md)
- **Status:** ✅ Production Ready
- **Size:** ~2,000 lines (simplified from 5,433 lines Python)

### Complete Kit Workflow

The kits work together in sequence:

**Discovery → Requirements → Design → Spec → Validation**

See [.dev/kits/README.md](.dev/kits/README.md) for complete pipeline walkthrough and [.dev/kits/KITS-INDEX.md](.dev/kits/KITS-INDEX.md) for kit descriptions.

## Learn More
- [Project Vision](docs/design/strategy/vision.md) - Why we're building this
- [System Overview](docs/design/system/overview.md) - How it works
- [User Journeys](docs/design/user-journeys/) - 61 use cases across 6 domains
- [Design Documentation](docs/design/index.md) - Complete design and architecture documentation hub

## Repository Structure

```
knowledge-graph-lab/
├── docs/
│   ├── team/           # Team member guides and resources
│   ├── modules/        # Module specifications and assignments
│   │   └── shared/     # ⚡ Shared module requirements (Docker, APIs, auth)
│   ├── design/         # Architecture and requirements
│   ├── research/       # Research methodology and tools
├── scripts/           # ⚡ Validation scripts for shared requirements
├── src/               # Source code (Phase 2+)
└── tests/             # Test suites (Phase 2+)
```

### 🔧 Quick Commands for Module Compliance
```bash
# Validate any module against shared requirements
python3 scripts/validate-standalone-compliance.py docs/modules/backend-architecture/Backend-Architecture-Spec.md

# Use the agent prompt to apply requirements to any module
# Copy the prompt from: docs/modules/shared/standalone-modules/README.md (bottom section)
```

## Development Artifacts

```
.dev/ai/                # AI-generated documentation (not for end users)
├── audits/            # Quality reviews and audit records
├── proposals/         # Work proposals and planning documents
├── prompts/           # Reusable prompts for AI agents
│   └── speckit-quality-review-prompt.md  # QA review prompt
├── handovers/         # Session handovers between AI agents
├── workorders/        # Task tracking and execution
├── backups/           # Archived copies of important files
├── documentation/     # AI-generated analysis and summaries
└── reports/           # Analysis reports and findings
.dev/PROBLEM-DISCOVERY-PROCESS.md # Standard debugging workflow
```

**What's in .dev/ai/**:
- **audits/**: Quality reviews of documentation (like the multi-model SpecKit reviews)
- **proposals/**: Planning documents for improvements and changes
- **prompts/**: Reusable prompts for AI-assisted quality assurance and analysis
- **handovers/**: Context preservation between AI agent sessions
- **workorders/**: Detailed task breakdowns and implementation instructions

**Note**: These are development artifacts created during project development.

**End users should focus on the `docs/` directory** for production documentation.

**Why .dev/ai/ exists**:

- Preserves development process transparency
- Enables quality assurance through AI reviews
- Maintains session continuity across multiple agents
- Documents decision-making and rationale
- Supports multi-model review strategies

---

## Auto-Sync to Public Repository

This private alpha repo automatically syncs to the public repository ([peermesh/knowledge-graph-lab](https://github.com/peermesh/knowledge-graph-lab)) via GitHub Actions.

### What Gets Synced
- `docs/` → public repo `docs/`
- `modules/` → public repo `modules/`
- `README.md` → public repo `README.md`

### When It Runs
- Automatically on every push to `main` that touches the synced paths
- No manual action required

### How It Works
1. Push changes to `main` branch in this alpha repo
2. GitHub Action detects changes in `docs/`, `modules/`, or `README.md`
3. Action clones public repo, rsyncs changes, commits, and pushes
4. Public repo is updated automatically

### Setup (One-Time)
See [.github/SYNC-SETUP.md](.github/SYNC-SETUP.md) for token configuration.

### Verification
Check the Actions tab in GitHub to see sync status, or verify the public repo directly.

---

## Git Repositories

This project contains **13 independent Git repositories** (including submodules). When making changes, be aware that commits may be needed in multiple repos.

### Repository Map

| # | Repository | Path | Remote | Description |
|---|------------|------|--------|-------------|
| 1 | **knowledge-graph-lab-alpha** | `/` (root) | `alpha` | Main project repository |
| 2 | **kits** | `.dev/kits/` | `origin` | Meta-repository for all development kits |
| 3 | **design-kit** | `.dev/kits/design-kit/` | `origin` | UX/UI design specification generator |
| 4 | **design-catalog** | `.dev/kits/design-kit/design-catalog/` | `origin` | Design component catalog |
| 5 | **discovery-kit** | `.dev/kits/discovery-kit/` | `origin` | Project discovery and analysis |
| 6 | **requirements-kit** | `.dev/kits/requirements-kit/` | `origin` | Requirements generation |
| 7 | **spec-kit** | `.dev/kits/spec-kit/` | `origin` | Feature specification generator |
| 8 | **kickstart-kit** | `.dev/kits/kickstart-kit/` | `origin` | Project initialization |
| 9 | **kit-template** | `.dev/kits/kit-template/` | `origin` | Template for new kits |
| 10 | **walkthrough-kit** | `.dev/kits/walkthrough-kit/` | `origin` | Interactive walkthroughs |
| 11 | **product-wizard** | `.dev/kits/product-wizard/` | `origin` | Product development workflow |
| 12 | **3d-interactive-diagram-lab** | `.dev/projects/3d-interactive-diagram-lab/` | `origin` | 3D visualization experiments |
| 13 | **prompts** | `docs/team/prompts/` | `origin` | Shared prompt library |

### Quick Status Check

```bash
# Check all repos for uncommitted changes
for dir in . .dev/kits .dev/kits/design-kit .dev/kits/design-kit/design-catalog \
  .dev/kits/discovery-kit .dev/kits/requirements-kit .dev/kits/spec-kit \
  .dev/kits/kickstart-kit .dev/kits/kit-template .dev/kits/walkthrough-kit \
  .dev/kits/product-wizard .dev/projects/3d-interactive-diagram-lab docs/team/prompts; do
  echo "=== $dir ===" && cd "$dir" && git status --short && cd - > /dev/null
done
```

---

## Project Information

- **Repository**: [github.com/knowledge-graph-lab](https://github.com)
- **Documentation**: See directories below

## For Team Members

→ **[Team Documentation Hub](docs/team/)** - Roles, assignments, and coordination

---

*Building the future of intelligent knowledge systems, one module at a time.*


 
.
 
 
