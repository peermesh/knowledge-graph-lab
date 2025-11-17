# Experimental Modules

Work-in-progress and experimental module implementations.

## Guidelines

- Use naming convention: `[developer-name]-[feature]`
- Example: `experimental/backend/john-auth-refactor/`
- Move to `standalone/` when ready for official use
- Clean up old experiments periodically

## Purpose

This directory is for:
- New feature development
- Refactoring experiments
- Proof-of-concept work
- Learning and exploration

## Moving to Standalone

When your experimental module is ready:
1. Ensure it meets [Standalone Module Requirements](../../docs/modules/shared/standalone-modules/README.md)
2. Create PR to move to `modules/standalone/[module]/`
3. Update docker-compose.yml if needed

