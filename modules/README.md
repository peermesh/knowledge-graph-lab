# Module Implementations

This directory contains all module implementations for Knowledge Graph Lab.

**🚨 FOR AI AGENTS:** See [MODULE-ORGANIZATION-RULES.md](./MODULE-ORGANIZATION-RULES.md) for complete rules on organizing, maintaining, and managing this directory.

## Directory Structure

```
modules/
├── standalone/          # Official Standalone Module implementations (MVP)
├── integrated/          # Future PeerMesh/Integrated implementations
└── experimental/        # Developer experiments and work-in-progress
```

## Standalone Modules

Official implementations that comply with [Standalone Module Requirements](../../docs/modules/shared/standalone-modules/README.md).

- **backend/** - Backend Infrastructure module
- **frontend/** - Frontend Interface module
- **ai/** - AI Intelligence module
- **publishing/** - Publishing System module

## Experimental Modules

For new features and experiments. Use naming convention: `[developer-name]-[feature]`

Example: `experimental/backend/john-auth-refactor/`

## Development Workflow

1. **Starting new work**: Create feature branch and work in `experimental/[module]/[your-name]-[feature]/`
2. **Maintaining existing**: Work directly in `standalone/[module]/`
3. **Evolution**: experimental → standalone → integrated

## Running Modules

Use docker-compose from project root:

```bash
docker-compose up
```

This uses modules from `modules/standalone/` by default.

