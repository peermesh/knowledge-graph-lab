# Module Implementations

This directory contains all module implementations for Knowledge Graph Lab.

**🚨 FOR AI AGENTS:** See [VERSIONING-RULES.md](./VERSIONING-RULES.md) for complete versioning and maintenance rules.

## Directory Structure

```
modules/
├── standalone/          # Standalone module implementations
│   ├── publishing/      # Publishing System module (v1.0 - Nov 1, 2025)
│   ├── frontend/        # Frontend Interface module (v1.0 - Nov 3, 2025)
│   ├── backend/         # Backend Infrastructure module (v1.0 - Nov 5, 2025)
│   └── ai/              # AI Intelligence module (v1.0 - Nov 7, 2025)
├── integrated/          # Future PeerMesh-integrated implementations
└── experimental/        # Developer experiments and work-in-progress
```

## Directory Purposes

### Standalone Modules (`modules/standalone/`)

These are complete, self-contained module implementations that can run independently:

- **publishing/** - Publishing System module with multi-channel distribution
- **frontend/** - React/TypeScript frontend with knowledge graph visualization
- **backend/** - FastAPI backend with database and entity management
- **ai/** - AI services for knowledge graph processing and entity extraction

### Development Workflow Directories

- **experimental/** - For new features and developer experiments before integration
  - Use naming: `experimental/[module]/[developer]-[feature]/`
  - Example: `experimental/backend/john-auth-refactor/`
  - No versioning required, can be deleted if experiments fail
  - Promoted to `standalone/` when ready

- **integrated/** - For future PeerMesh-integrated implementations
  - Reserved for modules that span multiple systems
  - Will contain cross-module orchestration logic
  - Currently empty, planned for future development

**Note:** Empty directories contain `.gitkeep` files to ensure they're tracked in git and visible in the repository structure.

## Current Standalone Modules

All active modules are located in `modules/standalone/` and can run independently:

- **publishing/** - Publishing System module
  - Status: ✅ Active (v1.0-publishing-2025-11-01)
  - Description: Multi-channel publishing with personalization, analytics, and real-time alerts
  - Quick Start: `cd modules/standalone/publishing && ./start-demo.sh`

- **frontend/** - Frontend Interface module
  - Status: ✅ Active (v1.0-frontend-2025-11-03)
  - Description: React/TypeScript frontend with knowledge graph visualization
  - Quick Start: `cd modules/standalone/frontend && npm start`

- **backend/** - Backend Infrastructure module
  - Status: ✅ Active (v1.0-backend-2025-11-05)
  - Description: FastAPI backend with database, authentication, and entity management
  - Quick Start: `cd modules/standalone/backend && python -m uvicorn src.main:app`

- **ai/** - AI Intelligence module
  - Status: ✅ Active (v1.0-ai-2025-11-07)
  - Description: Knowledge graph processing, entity extraction, and relationship mapping
  - Quick Start: `cd modules/standalone/ai && python -m uvicorn src.api.main:app`

## Versioning System

**Git Tags**: Each module version is tagged as `v1.0-[module]-[date]`
- Example: `v1.0-publishing-2025-11-01`
- View tags: `git tag -l | grep v1.0`

**Future Updates**: See [VERSIONING-RULES.md](./VERSIONING-RULES.md)

## Experimental Modules

For new features and experiments. Use naming convention: `[developer-name]-[feature]`

Example: `experimental/backend/john-auth-refactor/`

## Development Workflow

1. **Starting new work**: Create feature branch and work in `experimental/[module]/[your-name]-[feature]/`
2. **Maintaining existing**: Work directly in module directories (publishing/, frontend/, etc.)
3. **Versioning**: Use Git tags for releases, no directory versioning
4. **Evolution**: experimental → module root → integrated

## Running Modules

Use docker-compose from project root:

```bash
docker-compose up
```

Or run individual standalone modules:

```bash
# Publishing System
cd modules/standalone/publishing && ./start-demo.sh

# Frontend (development)
cd modules/standalone/frontend && npm start

# Backend API
cd modules/standalone/backend && python -m uvicorn src.main:app

# AI Service
cd modules/standalone/ai && python -m uvicorn src.api.main:app
```

