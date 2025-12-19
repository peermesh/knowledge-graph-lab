# Team Deliverables Guide

Quick reference for submitting all project deliverables. Bookmark this page.

## Quick Reference Table

| Phase | What You Submit | Where to Put It | File Format | Due When |
|-------|----------------|-----------------|-------------|----------|
| **1** | Research Brief | `docs/team/module-assignments/[your-module]/deliverables/phase-1-research/` | `phase-1-research-brief.md` | After research completion |
| **2** | PRD (Product Requirements Document) | `docs/team/module-assignments/[your-module]/deliverables/phase-2-planning/` | `PRD.md` | After Phase 1 approval |
| **3** | MVP Code + Documentation | `docs/team/module-assignments/[your-module]/deliverables/phase-3-mvp/` | Docker setup + README | After Phase 2 approval |
| **4** | Enhanced Code + Demo | `docs/team/module-assignments/[your-module]/deliverables/phase-4-enhancement/` | Enhanced codebase + presentation | Before Demo Day |
| **5** | Integration Code | `docs/team/module-assignments/[your-module]/deliverables/phase-5-integration/` | Production-ready system | After Demo Day |

## Find Your Module Path

Replace `[your-module]` above with your specific module:

| Your Role | Your Module | Your Base Path |
|-----------|-------------|----------------|
| Backend Engineer | `backend-architecture` | `docs/team/module-assignments/backend-architecture/deliverables/` |
| Frontend Developer | `frontend-design` | `docs/team/module-assignments/frontend-design/deliverables/` |
| AI/ML Engineer | `ai-development` | `docs/team/module-assignments/ai-development/deliverables/` |
| Content Systems | `publishing-tools` | `docs/team/module-assignments/publishing-tools/deliverables/` |

## Submission Process

### For All Phases:
1. **Create your deliverable** in the correct directory (see table above)
2. **Follow the git workflow**: [git-workflow.md](git-workflow.md)
3. **Submit via pull request** using your personal branch (`yourusername/work`)
4. **Post PR link** in Discord when ready for review

### Phase-Specific Notes:

**Phases 1-2**: Documents only (`.md` files in docs directory)
**Phases 3-5**: Code + documentation (may include files outside docs directory)

> **Note**: For Phases 3-5, actual code and Docker configurations may be placed outside the docs/ directory structure. Consult with team lead about final location decisions as development progresses.

## Detailed Phase Guides

Each phase has a comprehensive guide with requirements, success criteria, and examples:

- **Phase 1**: [Research & Discovery](project-plan/phase-1-deliverables.md)
- **Phase 2**: [Planning & PRD](project-plan/phase-2-deliverables.md)
- **Phase 3**: [MVP Development](project-plan/phase-3-deliverables.md)
- **Phase 4**: [Enhancement](project-plan/phase-4-deliverables.md)
- **Phase 5**: [Integration](project-plan/phase-5-deliverables.md)

## Working Ahead Guidelines

Moving faster than your team? Here's how to proceed independently:

### ✅ Can Work Ahead:
- Research and documentation phases (1-2)
- Individual module development (3-4)
- Preparing your module for integration (early Phase 5)

### ⚠️ Coordination Required:
- Integration testing (Phase 5)
- Cross-module API contracts
- Shared infrastructure decisions

### 📋 Best Practices:
- Keep your documentation updated as you progress
- Share findings that might help other modules
- Test your module independently before integration
- Document integration requirements clearly

## File Naming Conventions

### Research Documents (Phase 1):
- `phase-1-research-brief.md` (required)
- Supporting files: descriptive names (`technology-comparison-matrix.md`)

### Planning Documents (Phase 2):
- `PRD.md` (required, must follow SpecKit format)
- Supporting files: descriptive names (`api-specifications.md`)

### Code Deliverables (Phase 3+):
- `README.md` (setup and usage instructions)
- `Dockerfile` or `docker-compose.yml` (containerization)
- Source code: follow your module's conventions

## Getting Help

- **Process Questions**: Check [git-workflow.md](git-workflow.md)
- **Phase Requirements**: See detailed phase guides above
- **Technical Blockers**: Post in your module's Discord channel
- **Integration Questions**: Post in #kgl-integration
- **Urgent Issues**: Contact @grig

## Success Checklist

Before submitting any deliverable:

- [ ] Files are in the correct directory
- [ ] Required files are present (see phase guides)
- [ ] Documentation is complete and clear
- [ ] Git workflow followed correctly
- [ ] PR created and Discord notification posted
- [ ] All acceptance criteria met (see phase-specific guides)

---

**Remember**: This guide covers the submission process. For technical requirements and success criteria, always refer to the detailed phase guides linked above.