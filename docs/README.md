# Knowledge Graph Lab

Knowledge Graph Lab is an AI-powered research platform that transforms scattered information into actionable insights for the creator economy.

## Core Capabilities

Knowledge Graph Lab delivers four main capabilities to help users navigate the creator economy:

- **Discovers**: Monitors hundreds of sources (RSS, APIs, websites) to find opportunities:
  - Grants: Platform creator programs, community accelerators
  - Partnerships: Collaboration opportunities, community partnerships
  - Platform updates: Creator program features, platform tools and resources

- **Understands**: Builds knowledge graphs mapping entities (YouTube, MrBeast, Google) and relationships (Google owns YouTube, grants require platform accounts) from unstructured text.

- **Reasons**: Identifies patterns like seasonal grant cycles, platform migration trends, and collaboration opportunities across different creator communities.

- **Delivers**: Distributes insights through web interface, email digests, API endpoints, and webhooks - each personalized to user interests and preferences.

## Quick Start

- **For new team members**: Start with [team onboarding](team/onboarding.md)
- **For system overview**: Read the [vision](design/strategy/vision.md) and [architecture](design/system/architecture.md)
- **For development**: Check your [module assignment](team/README.md)

## Documentation Structure

Find documentation in three main sections:

### System Design & Strategy (design/)
**Start here to understand the system:**

- [Vision](design/strategy/vision.md) - Why we're building this and the problem we're solving
- [Architecture](design/system/architecture.md) - Technical components and data flow
- [Success Metrics](design/strategy/success-metrics.md) - Measurable targets and KPIs

**Implementation details:**

- [Deployment](design/system/deployment.md) - Production deployment instructions
- [Research Methodology](design/research/methodology.md) - Depth-First Distillation approach
- [User Journeys](design/user-journeys/) - 61 use cases across 6 domains

### ⚡ Shared Module Requirements (modules/shared/)
**Two-level interoperability system that all modules must follow:**

#### 🚀 **Standalone Module** (MVP - Required)
- **[Standalone Module Requirements](modules/shared/standalone-modules/README.md)** - Basic interoperability for immediate team handover
- ✅ **Docker containers** with standard setup
- ✅ **Single PostgreSQL** database with module schemas
- ✅ **Basic REST APIs** with OpenAPI documentation
- ✅ **JWT authentication** managed by Backend module
- ✅ **Development environment** with mocks and offline capability

#### 🔬 **PeerMesh Module** (Advanced - Optional)
- **[PeerMesh Module Requirements](modules/shared/peermesh-modules/README.md)** - Sophisticated features for stretch goals
- ✅ **Multi-database architecture** (PostgreSQL + Qdrant + OpenSearch + TimescaleDB)
- ✅ **Parallel search** across specialized backends
- ✅ **Event-driven architecture** with NATS JetStream
- ✅ **Dual-layer authorization** (SpiceDB + OPA)
- ✅ **Advanced observability** (OpenTelemetry, Prometheus, Grafana)

- **[Implementation Guide](modules/shared/README.md)** - Complete guide on how to use both levels of the shared module system

**Quick validation:** `python3 scripts/validate-standalone-compliance.py docs/modules/backend-architecture/Backend-Architecture-Spec.md`

**Quick Reference:** [SHARED-MODULE-REQUIREMENTS-QUICK-REF.md](modules/SHARED-MODULE-REQUIREMENTS-QUICK-REF.md) - Complete checklist and agent prompt

### Team Resources (team/)
**Everything for productivity:**

- [Start Here](team/README.md) - Module assignments and navigation
- [Project Plan](team/project-plan/overview.md) - 5 project phases with deliverables
- [Onboarding](team/onboarding.md) - Day 1 setup checklist
- [Module Ownership](team/module-ownership.md) - Who owns what
- Module assignments in team/module-assignments/

### SpecKit - PRD Creation System (speckit/)
**Create implementation-ready specifications:**

- [SpecKit Overview](speckit/README.md) - Simple templates for comprehensive PRDs
- [Quick Start](speckit/guides/quickstart.md) - 5-minute introduction
- [Simple Template](speckit/templates/simple-template.md) - Start creating your PRD here

### Research Tools
- Deep research prompt generator (team/prompts/deep-research-prompt-generator.md)
- All team prompts are now centralized in team/prompts/

