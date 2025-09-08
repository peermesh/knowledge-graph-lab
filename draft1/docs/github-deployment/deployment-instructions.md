# GitHub Deployment Instructions & Validation

**Step-by-step guide for deploying complete GitHub infrastructure for Knowledge Graph Lab**

---

## Pre-Deployment Checklist

### Prerequisites
- [ ] GitHub organization access (`peermesh`)
- [ ] Repository admin permissions
- [ ] Team member GitHub usernames collected
- [ ] Project timeline confirmed (Start: September 9, 2025)

### Files Ready for Deployment
- [ ] 4 research brief issues (`docs/github-deployment/issues/`)
- [ ] Project board configuration (`docs/github-deployment/project-board/`)
- [ ] Repository settings guide (`docs/github-deployment/settings/`)
- [ ] This deployment instruction file

---

## Phase 1: Repository Configuration (15 minutes)

### Step 1: Repository Settings
**Time Estimate**: 5 minutes

1. Navigate to repository Settings → General
2. Update repository description:
   ```
   AI-Powered Creator Economy Research Platform - 10-week intern development program
   ```
3. Add topics: `ai`, `knowledge-graph`, `creator-economy`, `research-platform`, `internship`, `peermesh`
4. Verify features are enabled:
   - ✅ Issues
   - ✅ Projects
   - ✅ Wiki
   - ✅ Discussions
   - ✅ Actions

**Validation**: 
- Repository description updated
- All required features enabled
- Topics visible on repository homepage

### Step 2: Branch Protection Rules
**Time Estimate**: 5 minutes

1. Go to Settings → Branches → Add rule
2. Configure main branch protection:
   - Branch name pattern: `main`
   - Require pull request before merging: ✅
   - Require 1 approval
   - Dismiss stale reviews: ✅
   - Require conversation resolution: ✅

**Validation**:
- Main branch shows "protected" status
- Direct pushes to main are blocked
- PR approval requirement active

### Step 3: Security Settings
**Time Estimate**: 3 minutes

1. Go to Settings → Security & analysis
2. Enable all security features:
   - Dependency graph: ✅
   - Dependabot alerts: ✅
   - Dependabot security updates: ✅
   - Private vulnerability reporting: ✅

**Validation**:
- Security tab shows active monitoring
- Dependabot configuration ready

### Step 4: Collaborator Access
**Time Estimate**: 2 minutes

1. Go to Settings → Collaborators and teams
2. Add team members with appropriate permissions:
   - Interns: Write access
   - Mentors: Maintain access
   - Project lead: Admin access (already configured)

**Validation**:
- All team members have appropriate access levels
- Invitation emails sent if needed

---

## Phase 2: Project Board Setup (10 minutes)

### Step 1: Create New Project
**Time Estimate**: 3 minutes

1. Navigate to repository Projects tab
2. Click "New project"
3. Select "Table" layout
4. Project details:
   - **Name**: `Knowledge Graph Lab - 10-Week Development`
   - **Description**: `AI-Powered Creator Economy Research Platform - 10-week intern development program with 4 specialized modules`

**Validation**:
- Project created and linked to repository
- Table layout active
- Project accessible to team members

### Step 2: Configure Columns
**Time Estimate**: 4 minutes

Create columns in this order:
1. 📋 **Backlog** - All issues that need to be addressed
2. 🔍 **Research** - Week 1 research assignments and ongoing investigation  
3. 📝 **Planning** - Week 2 specification and planning tasks
4. 🚧 **In Progress** - Currently active development work
5. 👀 **Review** - Pull requests and completed work awaiting review
6. ✅ **Done** - Completed and verified work

**Validation**:
- All 6 columns created in correct order
- Column descriptions match specifications
- Columns visible in board view

### Step 3: Create Labels
**Time Estimate**: 2 minutes

Create these labels in repository Settings → Labels:

**Priority Labels**:
- `priority-critical` (color: #d73a4a) 
- `priority-high` (color: #fbca04)
- `priority-medium` (color: #0075ca)
- `priority-low` (color: #ffffff)

**Module Labels**:
- `module-1` (color: #1d76db)
- `module-2` (color: #0e8a16) 
- `module-3` (color: #fbca04)
- `module-4` (color: #f66a0a)

**Type Labels**:
- `research` (color: #7057ff)
- `planning` (color: #1d76db)
- `intern-assignment` (color: #0e8a16)

**Validation**:
- All labels created with correct colors
- Labels available in issue creation

### Step 4: Create Milestones
**Time Estimate**: 1 minute

1. Go to Issues → Milestones → New milestone
2. Create these milestones:

- **Week 1 - Research & Discovery** (Due: September 13, 2025)
- **Week 2 - Specification & Planning** (Due: September 20, 2025)  
- **Week 3-6 - Tier 1 Implementation** (Due: October 18, 2025)
- **Week 7-9 - Tier 2 Enhancement** (Due: November 8, 2025)
- **Week 10 - Integration & Demo** (Due: November 15, 2025)

**Validation**:
- All milestones created with correct due dates
- Milestones available in issue assignment

---

## Phase 3: Issue Creation (5 minutes)

### Step 1: Create Research Brief Issues
**Time Estimate**: 5 minutes

Use the prepared issue content from `docs/github-deployment/issues/` directory.

#### Issue 1: Module 1 Research Brief
1. Click "New issue"
2. Copy title from `issue-01-module-1-research.md`: `[Module 1] Research Brief - Data Ingestion & Source Adapters`
3. Copy full issue body from the file
4. Add labels: `research`, `module-1`, `week-1`, `intern-assignment`
5. Set milestone: `Week 1 - Research & Discovery`
6. Assign to backend intern (if known) or leave unassigned

#### Issue 2: Module 2 Research Brief  
1. Copy title from `issue-02-module-2-research.md`: `[Module 2] Research Brief - AI Knowledge Graph & Autonomous Research`
2. Copy full issue body from the file
3. Add labels: `research`, `module-2`, `week-1`, `intern-assignment`, `ai-ml`
4. Set milestone: `Week 1 - Research & Discovery`
5. Assign to AI/ML intern (if known) or leave unassigned

#### Issue 3: Module 3 Research Brief
1. Copy title from `issue-03-module-3-research.md`: `[Module 3] Research Brief - Reasoning Engine & Content Synthesis`
2. Copy full issue body from the file  
3. Add labels: `research`, `module-3`, `week-1`, `intern-assignment`, `ai-content`
4. Set milestone: `Week 1 - Research & Discovery`
5. Assign to AI/Logic intern (if known) or leave unassigned

#### Issue 4: Module 4 Research Brief
1. Copy title from `issue-04-module-4-research.md`: `[Module 4] Research Brief - Frontend & User Experience`
2. Copy full issue body from the file
3. Add labels: `research`, `module-4`, `week-1`, `intern-assignment`, `frontend`, `ux`
4. Set milestone: `Week 1 - Research & Discovery`
5. Assign to Frontend intern (if known) or leave unassigned

**Validation**:
- All 4 issues created with complete content
- Correct labels and milestones assigned
- Issues appear in project board "Research" column

---

## Phase 4: Automation Setup (Optional - 5 minutes)

### Project Board Automation
**Time Estimate**: 5 minutes

1. In project board, click "Settings" 
2. Configure automated workflows:
   - **New issue**: Move to "Backlog"
   - **Issue with `research` label**: Move to "Research" 
   - **Issue assigned**: Move to "In Progress"
   - **Issue closed**: Move to "Done"
   - **PR created**: Move related issue to "Review"
   - **PR merged**: Move related issue to "Done"

**Validation**:
- Automation rules active
- Test by creating a test issue and verifying movement

---

## Post-Deployment Validation Checklist

### Repository Health Check
- [ ] Repository description and topics updated
- [ ] Branch protection active on main branch
- [ ] Security features enabled and monitoring
- [ ] Team members have appropriate access levels
- [ ] Issue and PR templates working correctly

### Project Board Health Check  
- [ ] Project board created and linked to repository
- [ ] All 6 columns configured with descriptions
- [ ] Labels system complete with correct colors
- [ ] Milestones created with accurate due dates
- [ ] All 4 research issues created and properly categorized

### Issue Validation
- [ ] Issue 1 (Module 1) complete with research focus questions
- [ ] Issue 2 (Module 2) complete with AI/ML specifications
- [ ] Issue 3 (Module 3) complete with content synthesis requirements
- [ ] Issue 4 (Module 4) complete with frontend/UX guidelines
- [ ] All issues show correct labels, milestones, and assignments

### Integration Testing
- [ ] Issues automatically appear in project board
- [ ] Label changes move issues between columns (if automation enabled)
- [ ] Team members can create and edit issues
- [ ] PR creation links properly to issues
- [ ] Milestone progress tracking functional

---

## Team Onboarding Checklist

### For Project Lead
- [ ] Verify all deployment steps completed successfully
- [ ] Send team invitations to repository and project
- [ ] Schedule Week 1 kickoff meeting
- [ ] Prepare team orientation for GitHub workflow
- [ ] Set up communication channels (Slack/Discord integration)

### For Team Members
- [ ] Accept repository collaboration invitation
- [ ] Review project board and issue assignments  
- [ ] Read project documentation in `/docs/` directory
- [ ] Understand GitHub workflow and branch protection rules
- [ ] Ask questions about unclear requirements or expectations

---

## Troubleshooting Common Issues

### Issue: Project board not showing repository issues
**Solution**: Ensure repository is properly linked in project settings

### Issue: Branch protection not working
**Solution**: Verify admin permissions and rule configuration syntax

### Issue: Team members cannot access project board
**Solution**: Check repository collaborator permissions and organization settings

### Issue: Automation not working as expected
**Solution**: Review workflow triggers and test with simple actions

### Issue: Labels or milestones missing from issues
**Solution**: Bulk edit issues or recreate missing configuration elements

---

## Success Metrics

### Immediate Success (Day 1)
- ✅ All 4 research issues created and assigned
- ✅ Project board functional with proper categorization
- ✅ Team members can access and interact with issues
- ✅ Branch protection preventing unauthorized main branch changes

### Week 1 Success
- ✅ All interns actively using GitHub for research collaboration
- ✅ Issue comments and updates tracking progress
- ✅ Project board reflecting real work status
- ✅ No major workflow blockers or access issues

### Ongoing Success Indicators
- Consistent daily activity on issues and project board
- Proper branch workflow with PRs for all changes
- Regular milestone progress updates
- Team collaboration visible in comments and discussions

---

**Ready to Deploy**: Use this step-by-step guide to deploy the complete GitHub infrastructure. Each phase builds on the previous one, so follow the order carefully. The entire deployment should take approximately 30 minutes and result in a fully functional project management system ready for the 10-week intern development program.