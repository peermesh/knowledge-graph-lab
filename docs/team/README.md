# Team Start Here

Welcome! You're here to build a module. Let's get you to the right place.

## System Architecture

![Knowledge Graph Lab Architecture](../images/Knowledge-Graph-Lab.png)

*The Knowledge Graph Lab consists of interconnected modules that work together through a central Core Module. Each team member will be building one of these specialized modules.*

## Module Assignments

| Your Role | Your Module Directory | What You'll Find |
|-----------|----------------------|------------------|
| Backend Engineer | [module-assignments/backend-architecture/](module-assignments/backend-architecture/) | Database design, API architecture, Docker setup |
| Frontend Developer | [module-assignments/frontend-design/](module-assignments/frontend-design/) | React components, UI/UX design, state management |
| AI/ML Engineer | [module-assignments/ai-development/](module-assignments/ai-development/) | LLM integration, knowledge graph, entity extraction |
| Content Systems | [module-assignments/publishing-tools/](module-assignments/publishing-tools/) | Multi-channel distribution, email systems, analytics |

**Next Step**: Navigate to your module directory above. Inside you'll find assignments organized by phase.

## Module Implementation Directory

Once your research and planning phases are complete, you'll work in the main `modules/` directory:

```
modules/
├── standalone/          # Active, production-ready modules
│   ├── publishing/     # Publishing System module
│   ├── frontend/       # Frontend Interface module
│   ├── backend/        # Backend Infrastructure module
│   └── ai/             # AI Intelligence module
├── experimental/       # Development sandbox for new features
└── integrated/         # Future cross-module integrations
```

### Working in the Modules Directory

**For Active Development:**
- Work directly in `modules/standalone/[your-module]/`
- Use Git tags for versioning (see [modules/VERSIONING-RULES.md](../../modules/VERSIONING-RULES.md))
- Example: `modules/standalone/backend/` for backend development

**For Experimental Features:**
- Create branches for experimental work
- Use naming: `yourname/experimental-[feature]`
- Work in `modules/experimental/[module]/[yourname]-[feature]/`
- Promoted to `standalone/` when stable

**Git Workflow for Module Development:**
```bash
# Create feature branch
git checkout -b yourname/experimental-backend-auth

# Work in experimental directory
cd modules/experimental/backend/yourname-experimental-auth/

# When ready to promote
git mv modules/experimental/backend/yourname-experimental-auth/* modules/standalone/backend/
git commit -m "feat: add authentication system to backend module"

# Create version tag
git tag v1.1-backend-2025-11-25
```

## Quick Links

- **System Overview**: [../design/product/system-overview.md](../design/product/system-overview.md) - What we're building and how modules connect (READ FIRST)
- **Git Workflow**: [git-workflow.md](git-workflow.md) - How to submit your work
- **Deliverables by Phase**: [project-plan/](project-plan/) - Requirements for each phase
- **Project Plan**: [project-plan/overview.md](project-plan/overview.md) - All phases and deliverables
- **Module Ownership**: [module-ownership.md](module-ownership.md) - Who owns what and communication channels
- **Research Methodology**: [../design/research/methodology.md](../design/research/methodology.md) - How to conduct research
- **New team member?**: [onboarding.md](onboarding.md) - Complete setup guide
- **Project vision**: [../design/strategy/vision.md](../design/strategy/vision.md) - Core mission and objectives

## Development Methodologies

**[RequirementsKit](methodologies/requirements-kit/)** - Requirements development system for Phase 2

Use this systematic approach to create comprehensive requirements documentation:

- **[Quick Start Guide](methodologies/requirements-kit/guides/quickstart.md)** - 5-minute overview
- **[Templates](methodologies/requirements-kit/templates/)** - Simple starter + comprehensive format
- **[Workflow](methodologies/requirements-kit/guides/workflow.md)** - Official 5-phase process

**When to use**: During Phase 2 (Planning) to create your module's PRD

## Development Roadmap

![Knowledge Graph Lab Roadmap](../images/Knowledge-Graph-Lab-roadmap.png)

*This roadmap shows the 5-phase development process you'll follow: from initial research through to final integration. Each phase builds upon the previous one, culminating in a connected, publicly available system.*

## Getting Started

1. **Understand the project**: Read [project-plan/overview.md](project-plan/overview.md) for all phases
2. **Find your module**: Use the Module Assignments table above
3. **Explore your module directory**: Inside you'll find:
   - `01-work-description.md` - Your module's full scope
   - `02-phase-1-research/` - Research phase assignments
   - `03-phase-2-prd+plan/` - Planning phase assignments
   - `deliverables/` - Where your completed work goes
   - `work-in-progress/` - Where your active work happens
4. **Ask your team lead**: Which phase you should be working on right now
5. **Start your assignment**: Open the `b` file in your current phase folder (e.g., `02b-...-assignment.md`)

## Module Directory Structure

Each module is organized like this:

```
module-assignments/[your-module]/
├── 01-work-description.md          ← Your module's complete scope
├── 02-phase-1-research/            ← Research phase (technology selection)
│   ├── 02a-...-overview.md         ← Overview/context
│   ├── 02b-...-assignment.md       ← Specific tasks
│   └── 02c-...-advanced.md         ← Deep dive/references
├── 03-phase-2-prd+plan/            ← Planning phase (PRD writing)
│   ├── 03a-...-overview.md
│   ├── 03b-...-assignment.md
│   └── 03c-...-advanced.md
├── deliverables/                   ← Your completed, finalized work
│   ├── phase-1-research/
│   ├── phase-2-planning/
│   └── [future phases...]
├── work-in-progress/               ← Active construction zone
│   ├── raw/                        ← Notes, transcripts
│   ├── ai-generated/               ← AI outputs
│   └── synthesis/                  ← Drafts
└── handoffs/                       ← Code/integrations ready for others
```

**File naming pattern**:

- **`a` files** (e.g., `02a-*`): Overview and context
- **`b` files** (e.g., `02b-*`): Your assignment (start here)
- **`c` files** (e.g., `02c-*`): Advanced topics and references

**Your workflow**:

1. Your team lead tells you which phase to work on (e.g., "Phase 2")
2. Open that phase's folder in your module (e.g., `03-phase-2-prd+plan/`)
3. Start with the `b` file (e.g., `03b-phase-2-prd-assignment.md`)
4. Refer to `a` (overview) and `c` (advanced) files as needed
5. Do your work in `work-in-progress/`
6. Move completed, reviewed work to `deliverables/`
