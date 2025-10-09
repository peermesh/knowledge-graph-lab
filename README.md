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

The platform consists of four integrated modules:
- **Backend Infrastructure** - Docker, databases, APIs, authentication
- **Frontend Interface** - React UI, visualizations, user experience
- **AI Intelligence** - LLMs, knowledge graphs, RAG, entity extraction
- **Publishing System** - Multi-channel distribution, personalization

## RequirementsKit: Requirements Development System

This repository includes **RequirementsKit**, a production-ready system for creating comprehensive requirements documentation that feeds into SpecKit's `/specify` command for implementation-ready specifications.

**Quick Start:**
- **Documentation:** [docs/team/methodologies/requirements-kit/README.md](docs/team/methodologies/requirements-kit/README.md)
- **5-Step Guide:** [docs/team/methodologies/requirements-kit/guides/quickstart.md](docs/team/methodologies/requirements-kit/guides/quickstart.md)
- **Extract to Your Project:** [.dev/pre-spec-kit/package-extraction.md](.dev/pre-spec-kit/package-extraction.md)

**What You Get:**
- 2 templates (simple starter + comprehensive format)
- AI expansion rules (transforms simple → comprehensive)
- Quick reference guides (quickstart + cheat sheet)
- Project terminology and conventions

**Proven Results:**
- Publishing Tools module: 625-line PRD, GO recommendation, 100% validation pass
- Clean, minimal interface (7 essential files)
- Development artifacts available in `.dev/pre-spec-kit/` for advanced users

**Version:** 1.0.0 (2025-10-09)

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
│   ├── design/         # Architecture and requirements
│   ├── research/       # Research methodology and tools
├── src/               # Source code (Phase 2+)
└── tests/             # Test suites (Phase 2+)
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

## Project Information

- **Repository**: [github.com/knowledge-graph-lab](https://github.com)
- **Documentation**: See directories below

## For Team Members

→ **[Team Documentation Hub](docs/team/)** - Roles, assignments, and coordination

---

*Building the future of intelligent knowledge systems, one module at a time.*

