# Repository Migration Plan: knowledge-graph-lab → PeerMesh Organization

**Date**: September 8, 2025 13:21  
**Tool**: Claude Code  
**Status**: DRAFT - Awaiting Review

## Executive Summary
Plan for migrating the private `knowledge-graph-lab` repository from personal account to the PeerMesh GitHub organization as a new public/shared repository.

## Current State
- **Repository Location**: `/Users/grig/work/peermesh/repo/knowledge-graph-lab`
- **Repository Type**: Private, personal account
- **Current Remote**: Personal GitHub account
- **Repository Content**: Knowledge graph laboratory/experimental code

## Target State
- **New Organization**: https://github.com/peermesh
- **Repository Name**: TBD (likely `knowledge-graph-lab` or similar)
- **Visibility**: TBD (Public or Private)
- **Access Control**: Organization-managed

## Pre-Migration Checklist

### 1. Repository Audit
- [ ] Review all files for sensitive information
- [ ] Check for hardcoded credentials, API keys, tokens
- [ ] Review `.env` files and secrets
- [ ] Audit commit history for sensitive data
- [ ] Check for personal information in commits
- [ ] Review branch protection rules
- [ ] Document current repository settings

### 2. Cleanup Tasks
- [ ] Remove or relocate sensitive configuration files
- [ ] Clean up experimental/temporary files
- [ ] Update documentation to reflect new location
- [ ] Review and update README.md
- [ ] Ensure all dependencies are documented
- [ ] Update any absolute paths or URLs

### 3. Organization Preparation
- [ ] Confirm access to PeerMesh organization
- [ ] Verify repository creation permissions
- [ ] Decide on repository naming convention
- [ ] Determine visibility (public/private)
- [ ] Plan team access and permissions
- [ ] Set up branch protection rules

## Migration Strategy Options

### Option 1: Fork and Transfer (Recommended)
**Pros:**
- Preserves complete history
- Maintains all branches
- GitHub handles redirects
- Clean migration path

**Cons:**
- Requires organization permissions
- May need to handle forks/stars manually

**Steps:**
1. Push all local changes to current repository
2. Transfer repository ownership via GitHub settings
3. Update local remotes
4. Verify all branches and tags transferred
5. Update CI/CD configurations

### Option 2: Fresh Repository with History
**Pros:**
- Clean start with curated history
- Opportunity to clean up commit history
- Can selectively migrate branches

**Cons:**
- More complex process
- Potential to lose metadata (issues, PRs)

**Steps:**
1. Create new repository in PeerMesh organization
2. Add new remote to local repository
3. Push all branches to new remote
4. Migrate issues/wiki if needed
5. Archive or delete old repository

### Option 3: Fresh Repository (Clean Start)
**Pros:**
- Completely clean history
- No risk of exposing old sensitive data
- Simplified structure

**Cons:**
- Loses all history
- Loses commit attribution
- Most destructive option

**Steps:**
1. Create new repository in PeerMesh organization
2. Copy current working tree (without .git)
3. Initialize as new repository
4. Create initial commit
5. Push to new repository

## Items Requiring Decisions

### Must Decide Before Migration:
1. **Repository Name**: Keep `knowledge-graph-lab` or rename?
2. **Visibility**: Public or Private repository?
3. **Migration Strategy**: Which option (1, 2, or 3)?
4. **Team Access**: Who needs what level of access?
5. **Branch Strategy**: Keep all branches or curate?
6. **Issue/PR Migration**: Migrate existing issues/PRs?
7. **Wiki/Documentation**: Migrate or recreate?
8. **CI/CD**: Any automation to set up?

### Repository Settings to Configure:
- [ ] Default branch (main/master)
- [ ] Branch protection rules
- [ ] Merge strategies
- [ ] Issue templates
- [ ] PR templates
- [ ] Security policies
- [ ] Dependency scanning
- [ ] Code scanning

## Risk Assessment

### High Risk Items:
- **Sensitive Data Exposure**: Credentials, keys, or personal data in history
- **Access Control**: Improper permissions in new organization
- **Breaking Dependencies**: Other projects depending on current location

### Medium Risk Items:
- **Lost Metadata**: Issues, PRs, discussions not migrated
- **Broken Links**: Documentation or external references
- **CI/CD Disruption**: Build pipelines need reconfiguration

### Low Risk Items:
- **Contributor Attribution**: May need to re-map contributors
- **Fork Relationships**: Existing forks won't auto-update

## Post-Migration Tasks

### Immediate Actions:
1. [ ] Verify repository accessibility
2. [ ] Test clone/pull/push operations
3. [ ] Verify all branches transferred
4. [ ] Check file integrity
5. [ ] Update local git remotes
6. [ ] Test any CI/CD pipelines

### Follow-up Actions:
1. [ ] Update documentation with new URLs
2. [ ] Notify team members of new location
3. [ ] Update any external references
4. [ ] Monitor for broken dependencies
5. [ ] Set up organization-specific integrations
6. [ ] Archive or delete old repository

## Do NOT Do List

### Never Without Explicit Approval:
- ❌ Delete the original repository
- ❌ Force push over existing history
- ❌ Make repository public without security audit
- ❌ Transfer without backing up locally first
- ❌ Commit sensitive files to new repository
- ❌ Change critical settings without discussion

### Avoid Common Mistakes:
- ❌ Forgetting to update git submodules
- ❌ Not checking for hardcoded repository URLs
- ❌ Ignoring CI/CD configuration updates
- ❌ Skipping local backup before migration
- ❌ Not testing access before announcing

## Migration Commands Reference

### Backup Current Repository
```bash
# Create complete backup
git clone --mirror /Users/grig/work/peermesh/repo/knowledge-graph-lab knowledge-graph-lab-backup

# Create working backup
cp -r /Users/grig/work/peermesh/repo/knowledge-graph-lab knowledge-graph-lab-backup-working
```

### Update Remotes
```bash
# View current remotes
git remote -v

# Add new organization remote
git remote add peermesh https://github.com/peermesh/knowledge-graph-lab.git

# Change origin to new location
git remote set-url origin https://github.com/peermesh/knowledge-graph-lab.git

# Remove old remote
git remote remove origin
```

### Push to New Repository
```bash
# Push all branches
git push peermesh --all

# Push all tags
git push peermesh --tags

# Push specific branch
git push peermesh main
```

## Questions for Discussion

1. **Timing**: When should the migration happen?
2. **Downtime**: Is any downtime acceptable?
3. **Team Coordination**: Who needs to be notified?
4. **Backup Strategy**: Where to store backups?
5. **Rollback Plan**: How to revert if issues arise?
6. **Documentation**: What needs updating?
7. **Dependencies**: What might break?
8. **Security**: Any additional security reviews needed?

## Next Steps

1. **Review this plan thoroughly**
2. **Make decisions on all TBD items**
3. **Perform security audit if going public**
4. **Create backup of current repository**
5. **Execute chosen migration strategy**
6. **Verify successful migration**
7. **Complete post-migration tasks**

## Notes

- Current repository appears to be a knowledge graph experimental/lab project
- Migration provides opportunity to clean up and reorganize
- Consider if any experimental code should be excluded
- Good time to establish coding standards for shared repository

---

**Status**: Awaiting your review and decisions on the above items before proceeding with any migration actions.