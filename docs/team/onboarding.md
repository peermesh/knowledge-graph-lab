# Team Member Onboarding

Get productive on Day 1. Follow this comprehensive checklist.

## What Are Modules?

The project has four core modules. You'll be assigned to one:

- **Backend Architecture** - APIs, databases, infrastructure
- **Frontend Design** - User interface, React components, visualizations
- **AI Development** - Machine learning, knowledge graphs, RAG systems
- **Publishing Tools** - Multi-channel distribution, personalization

## Day 1 Complete Checklist

### Find Your Module Assignment
- [ ] Read [team/README.md](README.md) to find your module
- [ ] Navigate to your module directory: `team/module-assignments/[your-module]/`
- [ ] Open `01-work-description.md` to understand your module's full scope
- [ ] Ask your team lead which phase you're currently working on

### Set Up Access
- [ ] GitHub - Get repository access (check invite email)
- [ ] Set up Git and GitHub CLI - Follow [git-workflow.md](git-workflow.md)
- [ ] Team communication platform - Get invite link from team lead
- [ ] Find your module channel and post introduction
- [ ] Create free accounts for: OpenAI, Claude, Perplexity
- [ ] AWS Free Tier (if testing deployment)

### Understand the Project
- [ ] Read [Project Overview](../design/system/architecture.md) - What we're building
- [ ] Skim [Project Vision](../design/strategy/vision.md) - Why it matters
- [ ] Review [Project Plan](project-plan/overview.md) - Phase milestones and deliverables

### Learn Repository Structure
- [ ] Read [Module Directory Overview](../../modules/README.md) - How modules are organized
- [ ] Review [Versioning Rules](../../modules/VERSIONING-RULES.md) - How module versions work
- [ ] Understand [Git Workflow](git-workflow.md) - Branching and commit best practices

### Start Your First Assignment
- [ ] Go to your module's current phase folder (ask team lead which phase)
- [ ] Open the `XXb-...-assignment.md` file in that folder (where XX is the phase number)
- [ ] Review the `XXa-...-overview.md` file for context
- [ ] Complete your assigned tasks
- [ ] Submit your work via pull request - See [git-workflow.md](git-workflow.md)

## Module Implementation Phase (Future)

When you move beyond research and planning:

### Module Directory Structure
```
modules/
├── standalone/          # Where you implement your module
│   └── [your-module]/  # Your active module directory
├── experimental/       # For testing new features
└── integrated/         # For cross-module work
```

### Implementation Workflow
- [ ] Work directly in `modules/standalone/[your-module]/`
- [ ] Use Git tags for versioning (see [Versioning Rules](../../modules/VERSIONING-RULES.md))
- [ ] Create feature branches: `yourname/feature-name`
- [ ] For experiments: `modules/experimental/[module]/[yourname]-[feature]/`
- [ ] Follow commit message standards in [Git Workflow](git-workflow.md)

## Getting Help

- **Questions**: Post on Discord

## Success Criteria

- ✅ You know which module you own and what it covers
- ✅ You have access to repository and communication channels
- ✅ You know where to find phase assignments in your module
- ✅ You've completed your first assignment tasks
- ✅ You understand the workflow for submitting work
- ✅ You know how to get help when blocked

