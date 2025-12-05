# Standalone Module Implementations

Official Standalone Module implementations that comply with the [Standalone Module Requirements](../../docs/modules/shared/standalone-modules/README.md).

## Current Modules

- **backend/** - Backend Infrastructure (FastAPI, PostgreSQL, Redis)
- **frontend/** - Frontend Interface (React)
- **ai/** - AI Intelligence (Entity extraction, knowledge graphs)
- **publishing/** - Publishing System (Content distribution)

## Status

All modules are in active development. Each module should have:
- Dockerfile
- Requirements/dependencies file
- Health endpoint at `/health`
- Compliance with Standalone Module requirements

## Running

From project root:

```bash
docker-compose up
```

## Module Specifications

See [Module Specifications](../../docs/modules/README.md) for detailed requirements.

