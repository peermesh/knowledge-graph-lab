# Versioning Rules

This guide explains the new flattened versioning system for Knowledge Graph Lab modules.

## Overview

**Previous Structure (Deprecated):**
```
modules/
├── publishing/
│   └── active/
│       └── v1.0-2025-11-01/
│           ├── src/
│           ├── tests/
│           └── README.md
```

**New Structure (Current):**
```
modules/
├── standalone/           # Standalone module implementations
│   └── publishing/       # ← Active module in standalone directory
│       ├── src/
│       ├── tests/
│       └── README.md
```

## Git-Based Versioning

We use Git tags for versioning instead of directory structures:

### Tag Format
```
v[major].[minor]-[module]-[YYYY-MM-DD]
```

**Examples:**
- `v1.0-publishing-2025-11-01`
- `v1.1-frontend-2025-12-15`
- `v2.0-ai-2026-01-30`

### Viewing Versions
```bash
# List all module versions
git tag -l | grep v[0-9]

# See what changed between versions
git diff v1.0-publishing-2025-11-01..v1.1-publishing-2025-12-01

# Checkout specific version
git checkout v1.0-ai-2025-11-07
```

## Module Update Process

### For Minor Updates (Bug fixes, small features)
```bash
# 1. Work on the module
cd modules/standalone/publishing
# Make changes...

# 2. Test and commit
git add .
git commit -m "feat: add newsletter personalization"

# 3. Create new tag
git tag v1.1-publishing-2025-12-01

# 4. Push changes and tag
git push origin main --tags
```

### For Major Updates (Breaking changes)
```bash
# 1. Work on the module
cd modules/standalone/ai
# Make breaking changes...

# 2. Update version and commit
echo "2.0.0" > VERSION
git add VERSION
git commit -m "feat!: rewrite knowledge graph processing (breaking)"

# 3. Create major version tag
git tag v2.0-ai-2026-01-30
git push origin main --tags
```

## Automated Versioning (Future)

When we implement automated versioning:

### Semantic Versioning Triggers
- **PATCH** (`1.0.1`): Bug fixes
- **MINOR** (`1.1.0`): New features, backward compatible
- **MAJOR** (`2.0.0`): Breaking changes

### Automated Tagging Script
```bash
# Future implementation
./scripts/tag-module.sh publishing minor "add newsletter templates"
# Creates: v1.1-publishing-2025-12-01
```

## Module States

### Active Modules
- Located in `modules/standalone/[module]/`
- Tagged with version numbers
- Ready for production use

### Experimental Modules
- Located in `modules/experimental/[module]/[feature]/`
- No versioning required
- May graduate to active modules

### Legacy Modules
- Located in `modules/standalone/[module]/` (deprecated)
- Kept for reference only
- Will be removed in future cleanup

## Best Practices

### Commit Messages
```bash
# Good examples
git commit -m "feat: add real-time alert delivery"
git commit -m "fix: resolve memory leak in graph processing"
git commit -m "docs: update API documentation"
git commit -m "refactor: simplify entity extraction logic"

# Bad examples
git commit -m "update stuff"
git commit -m "changes"
```

### Tag Descriptions
```bash
# Add annotated tags with descriptions
git tag -a v1.1-publishing-2025-12-01 -m "Add newsletter personalization and improved analytics"

# Or use lightweight tags for simple releases
git tag v1.0.1-publishing-2025-11-15
```

## Migration from Old System

### What Changed
1. **Removed** `modules/[module]/active/v1.0-YYYY-MM-DD/` hierarchy
2. **Added** Git tags for versioning
3. **Reorganized** modules into `modules/standalone/[module]/` for categorization

### Migration Complete ✅
- ✅ All active modules moved to `modules/standalone/`
- ✅ Git tags created for each version
- ✅ Documentation updated
- ✅ Sync scripts updated to handle new structure

### Legacy Cleanup
The old `standalone/` directory structure remains for reference but is deprecated. Remove after confirming no dependencies.

## Troubleshooting

### Can't Find Module Version
```bash
# Find all tags for a module
git tag -l | grep publishing

# See what changed in a specific version
git show v1.0-publishing-2025-11-01
```

### Module Directory Structure
```bash
# Check current module structure
find modules/standalone/publishing -type f | head -10

# Compare with tagged version
git diff v1.0-publishing-2025-11-01..HEAD -- modules/standalone/publishing/
```

### Rollback to Previous Version
```bash
# Checkout specific version (creates detached HEAD)
git checkout v1.0-ai-2025-11-07

# Or reset to specific version (destructive)
git reset --hard v1.0-ai-2025-11-07
```

## Future Enhancements

### Planned Features
- **Automated tagging** based on commit messages
- **Changelog generation** from git history
- **Version comparison tools**
- **Release notes automation**
- **Dependency version pinning**

### Integration Points
- **CI/CD pipelines** can use tags for deployments
- **Docker images** tagged with module versions
- **Documentation** automatically updated with version info
