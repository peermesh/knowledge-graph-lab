# Junior Developer SpecKit Guide

**Purpose**: Step-by-step instructions for junior developers to clean up their workspace, update SpecKit, run it with proper validation, and commit their work.

**Last Updated**: October 27, 2025

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Understanding SpecKit File Structure](#understanding-speckit-file-structure)
3. [Step 1: Update to Latest SpecKit Version](#step-1-update-to-latest-speckit-version)
4. [Step 2: Clean Your Branch](#step-2-clean-your-branch)
5. [Step 3: Run SpecKit Commands](#step-3-run-speckit-commands)
6. [Step 4: Sanity Checks & Validation](#step-4-sanity-checks--validation)
7. [Step 5: Docker Validation](#step-5-docker-validation)
8. [Step 6: Document Issues](#step-6-document-issues)
9. [Step 7: Commit and Push](#step-7-commit-and-push)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, make sure you have:

- ✅ Git repository cloned
- ✅ Your module branch checked out (e.g., `001-ai-module`, `002-backend-module`, etc.)
- ✅ Docker installed and running
- ✅ Access to Cursor IDE with SpecKit extension
- ✅ Read access to `memory/constitution.md`
- ✅ Read access to `docs/team/deliverables/requirements-kit-v2/`

---

## Understanding SpecKit File Structure

**Before you start, understand where SpecKit creates its output:**

### Standard SpecKit Output Location

```
specs/[branch-name]/
├── spec.md              # Generated specification (main output)
├── plan.md              # Implementation plan (after /plan command)
├── tasks.md             # Task breakdown (after /tasks command)
├── contracts/           # API specifications
└── data-model.md        # Data structures
```

**Example**: If you're on branch `001-ai-module`, SpecKit creates:
```
specs/001-ai-module/
├── spec.md
├── plan.md
└── tasks.md
```

**Key Points:**
- ✅ **Output location**: `specs/[your-branch-name]/`
- ✅ **Automatic**: SpecKit creates the branch name directory automatically
- ✅ **Clean**: Each branch gets its own clean output directory
- ❌ **Don't manually specify output paths** unless you have advanced needs

---

## Step 1: Update to Latest SpecKit Version

**Why**: Ensures you have bug fixes and latest features

### 1.1: Check Current Version

```bash
cd specs/github-spec-kit
git remote -v
```

**Expected output**:
```
origin  https://github.com/peermesh/spec-kit.git (fetch)
origin  https://github.com/peermesh/spec-kit.git (push)
```

### 1.2: Fetch Latest Changes

```bash
git fetch origin
```

### 1.3: Check if Updates Available

```bash
git status
```

**If you see "Your branch is behind 'origin/main'"**, proceed to update:

```bash
git pull origin main
```

### 1.4: Verify Update

```bash
git log --oneline -5
```

**Expected**: Should show recent commits from the SpecKit repository

### 1.5: Return to Project Root

```bash
cd ../..
pwd  # Should show: /Users/.../knowledge-graph-lab-alpha
```

---

## Step 2: Clean Your Branch

**Purpose**: Remove any old SpecKit test runs so you start fresh

### 2.1: Commit Current State

**First, save any work in progress:**

```bash
# Check what files have changed
git status

# Add and commit current work
git add -A
git commit -m "chore: checkpoint before SpecKit cleanup"
```

### 2.2: Check for Old SpecKit Output

**Look for the output directory for your branch:**

```bash
# Replace [your-branch-name] with your actual branch (e.g., 001-ai-module)
ls -la specs/[your-branch-name]/
```

**If the directory exists and has old content**, you need to clean it:

```bash
# Option 1: Remove the entire directory (recommended for fresh start)
rm -rf specs/[your-branch-name]/

# Option 2: Keep the directory but remove old files
rm -f specs/[your-branch-name]/*.md
rm -rf specs/[your-branch-name]/contracts/
```

### 2.3: (Optional) Clean Old Spec Directories

**If you have directories for old branches you're no longer using:**

```bash
# List all spec directories
ls -la specs/

# Remove old branch directories you don't need
# Example: If 000-test-branch is old and not needed
rm -rf specs/000-test-branch/
```

**⚠️ Warning**: Only delete directories for branches you're NOT currently working on!

### 2.4: Commit Cleanup

```bash
git add -A
git commit -m "chore: clean old SpecKit output for fresh run"
```

---

## Step 3: Run SpecKit Commands

**Now run SpecKit with your module's input specification**

### 3.1: Identify Your Module

| Module | Input Specification Path |
|--------|--------------------------|
| **AI Module** | `docs/team/deliverables/requirements-kit-v2/ai-module-spec.md` |
| **Backend Module** | `docs/team/deliverables/requirements-kit-v2/backend-module-spec.md` |
| **Frontend Module** | `docs/team/deliverables/requirements-kit-v2/frontend-module-spec.md` |
| **Publishing Module** | `docs/team/deliverables/requirements-kit-v2/publishing-module-spec.md` |

### 3.2: Run /specify Command

**Open Cursor IDE and run the appropriate command for your module:**

**AI Module:**
```
/specify "docs/team/deliverables/requirements-kit-v2/ai-module-spec.md"
```

**Backend Module:**
```
/specify "docs/team/deliverables/requirements-kit-v2/backend-module-spec.md"
```

**Frontend Module:**
```
/specify "docs/team/deliverables/requirements-kit-v2/frontend-module-spec.md"
```

**Publishing Module:**
```
/specify "docs/team/deliverables/requirements-kit-v2/publishing-module-spec.md"
```

**⚠️ Note**: The commands above use the **standard** SpecKit behavior. Output will automatically go to `specs/[your-branch-name]/spec.md`.

**Expected Result:**
- ✅ Creates `specs/[your-branch-name]/spec.md`
- ✅ No errors in Cursor output
- ✅ File is readable and well-formatted

### 3.3: Verify Output Created

```bash
# Check that spec.md was created
ls -la specs/[your-branch-name]/

# Should see:
# spec.md (and possibly other files)
```

### 3.4: (Optional) Run /plan Command

**If your module is ready for implementation planning:**

```
/plan
```

**Expected Result:**
- ✅ Creates `specs/[your-branch-name]/plan.md`
- ✅ Contains architecture decisions and component breakdown

### 3.5: (Optional) Run /tasks Command

**If you have a plan and want task breakdown:**

```
/tasks
```

**Expected Result:**
- ✅ Creates `specs/[your-branch-name]/tasks.md`
- ✅ Contains ordered task list for implementation

---

## Step 4: Sanity Checks & Validation

**Critical step: Verify SpecKit output matches requirements and follows constitution**

### 4.1: Read the Constitution (REQUIRED)

📖 **MUST READ FIRST**: `memory/constitution.md`

**Key things to look for:**
- ✅ Modular independence (each module is standalone)
- ✅ Docker containerization requirements
- ✅ Quality gates and validation process
- ✅ Performance standards (startup < 30s, API < 500ms, 99% uptime)
- ✅ Testing requirements (80%+ coverage)

### 4.2: Read Shared Module Requirements (REQUIRED)

📖 **MUST READ**: `docs/modules/SHARED-MODULE-REQUIREMENTS-QUICK-REF.md`

**Key things to look for:**
- ✅ API contract standards
- ✅ Error handling patterns
- ✅ Security requirements
- ✅ Logging and monitoring requirements
- ✅ Inter-module communication protocols

### 4.3: Read Your Input Specification

📖 **Read**: `docs/team/deliverables/requirements-kit-v2/[your-module]-spec.md`

**Make a mental note of:**
- Key features and requirements
- API endpoints and contracts
- Data models and schemas
- Integration points with other modules
- Performance and scalability requirements

### 4.4: Read SpecKit Output

📖 **Read**: `specs/[your-branch-name]/spec.md`

**Now compare with what you just read above.**

### 4.5: Create Missing Items Checklist

**Create a file to track issues:**

```bash
nano specs/[your-branch-name]/VALIDATION-ISSUES.md
```

**Template for your checklist:**

```markdown
# Validation Issues for [Your Module]

## Date: [Today's date]
## Reviewer: [Your name]

---

## Missing Requirements from Input Spec

❌ **[Requirement Name]**
- **Expected**: [What should be in spec.md]
- **Found**: [What's actually there, or "Missing"]
- **Action**: [What needs to be fixed]

---

## Constitution Compliance Issues

### Modular Independence
- [ ] Module can run standalone
- [ ] Docker container specified
- [ ] No premature inter-module dependencies

### Quality Gates
- [ ] 5-phase review process mentioned
- [ ] Automated validation specified
- [ ] Technical feasibility review included

### Performance Standards
- [ ] Container startup < 30 seconds specified
- [ ] API response < 500ms specified
- [ ] 99% uptime requirement mentioned

### Development Standards
- [ ] Docker containerization from Phase 3 specified
- [ ] 80%+ test coverage requirement specified
- [ ] Complete documentation specified

---

## Shared Module Requirements Compliance

- [ ] API contract standards followed
- [ ] Error handling patterns specified
- [ ] Security requirements included
- [ ] Logging/monitoring specified
- [ ] Inter-module protocols defined

---

## Technical Issues

❌ **[Issue Name]**
- **Problem**: [Describe the technical issue]
- **Impact**: [Why this matters]
- **Fix**: [How to resolve it]

---

## Documentation Gaps

- [ ] Setup instructions complete
- [ ] API documentation complete
- [ ] Troubleshooting guide included
- [ ] Configuration reference provided

---

## Overall Assessment

**Ready for Implementation?** ❓ (YES/NO with explanation)

**Critical Blockers**: [List any blockers]

**Nice-to-Have Improvements**: [List enhancements for later]
```

### 4.6: Update spec.md with Missing Items

**If you found issues, fix them now:**

```bash
# Edit the generated spec
nano specs/[your-branch-name]/spec.md
```

**Add missing sections:**
- Constitution requirements that were overlooked
- Input spec requirements that weren't included
- Technical details that need clarification
- Documentation sections that are incomplete

**Add an "Issues and Gaps" section at the end:**

```markdown
---

## Issues and Gaps Identified

**Validation Date**: [Today's date]
**Validated By**: [Your name]

### Missing from SpecKit Output
- [X] [Requirement name] - Added to [Section X]
- [X] [Another requirement] - Added to [Section Y]

### Constitution Compliance
- [X] Docker containerization requirements - Added to Deployment section
- [X] Performance standards - Added to Non-Functional Requirements
- [X] Testing requirements - Added to Quality Assurance section

### Technical Issues Resolved
- [X] [Issue name] - Fixed by [what you did]

### Documentation Gaps Filled
- [X] Setup instructions - Added new section
- [X] API documentation - Enhanced API Reference section
```

---

## Step 5: Docker Validation

**If your module has a Dockerfile, test it:**

### 5.1: Check for Dockerfile

```bash
# Look for Dockerfile in your module directory
ls -la [module-directory]/Dockerfile
```

**Module directories:**
- AI Module: `ai/Dockerfile`
- Backend Module: `backend/Dockerfile`
- Frontend Module: `frontend/Dockerfile`
- Publishing Module: `publishing/Dockerfile`

### 5.2: Build Docker Image

```bash
cd [module-directory]
docker build -t [module-name]:test .
```

**Expected result**: Build completes without errors

### 5.3: Run Container

```bash
docker run -p [port]:[port] [module-name]:test
```

**Expected result**: Container starts in under 30 seconds

### 5.4: Test Health Check

```bash
# In another terminal
curl http://localhost:[port]/health
```

**Expected result**: HTTP 200 response with health status

### 5.5: Document Results

**Add to your VALIDATION-ISSUES.md:**

```markdown
---

## Docker Validation Results

**Build Status**: ✅ SUCCESS / ❌ FAILED
**Build Time**: [X seconds]

**Container Start Status**: ✅ SUCCESS / ❌ FAILED
**Startup Time**: [X seconds] (Constitution requirement: < 30s)

**Health Check Status**: ✅ SUCCESS / ❌ FAILED
**Response**: [paste curl output]

**Issues Found**:
- [List any issues]

**Action Items**:
- [List what needs to be fixed]
```

---

## Step 6: Document Issues

**Consolidate all findings into a clear summary**

### 6.1: Create Issue Summary

```bash
nano specs/[your-branch-name]/ISSUE-SUMMARY.md
```

**Template:**

```markdown
# SpecKit Run Issue Summary

**Module**: [Your module name]
**Branch**: [Your branch name]
**Date**: [Today's date]
**Developer**: [Your name]

---

## Executive Summary

**SpecKit Run Status**: ✅ SUCCESS / ⚠️ SUCCESS WITH ISSUES / ❌ FAILED

**Critical Issues Found**: [number]
**Enhancement Opportunities**: [number]

**Ready for Implementation?**: YES / NO / WITH FIXES

---

## Critical Issues (BLOCKERS)

1. **[Issue Name]**
   - **Severity**: CRITICAL
   - **Description**: [What's wrong]
   - **Impact**: [Why this blocks implementation]
   - **Fix Required**: [What needs to be done]
   - **Owner**: [Who should fix this]

---

## Important Issues (HIGH PRIORITY)

1. **[Issue Name]**
   - **Severity**: HIGH
   - **Description**: [What's wrong]
   - **Impact**: [Why this matters]
   - **Fix Required**: [What needs to be done]

---

## Enhancement Opportunities (NICE TO HAVE)

1. **[Enhancement Name]**
   - **Severity**: LOW
   - **Description**: [What could be improved]
   - **Benefit**: [Why this would help]
   - **When**: [Can be done later or before implementation?]

---

## Recommendations

**Next Steps**:
1. [First thing to do]
2. [Second thing to do]
3. [Third thing to do]

**Timeline**: [How long will fixes take?]

**Help Needed**: [Do you need assistance? From whom?]
```

---

## Step 7: Commit and Push

**Save your work to the repository**

### 7.1: Check Git Status

```bash
git status
```

**You should see changes to:**
- `specs/[your-branch-name]/spec.md`
- `specs/[your-branch-name]/VALIDATION-ISSUES.md`
- `specs/[your-branch-name]/ISSUE-SUMMARY.md`
- Possibly `specs/[your-branch-name]/plan.md` and `tasks.md`

### 7.2: Review Changes

```bash
# Review what changed in spec.md
git diff specs/[your-branch-name]/spec.md
```

### 7.3: Stage All Changes

```bash
git add -A
```

### 7.4: Commit with Descriptive Message

```bash
git commit -m "feat: complete SpecKit run for [module-name] with validation

- Ran /specify command on [module]-spec.md
- Generated spec.md with validation
- Added constitution compliance checks
- Validated shared module requirements
- Tested Docker integration (if applicable)
- Documented [X] issues found
- Updated spec.md with missing requirements

Issues found: [number]
Critical blockers: [number]
Ready for implementation: [YES/NO]"
```

### 7.5: Push to Remote

```bash
git push origin [your-branch-name]
```

**Expected result**: Changes pushed successfully to GitHub

---

## Troubleshooting

### Issue: "SpecKit command not found"

**Solution:**
1. Verify SpecKit is installed: `ls specs/github-spec-kit/`
2. Check Cursor settings: `.cursor/commands.json` should exist
3. Restart Cursor IDE
4. Try running from Cursor's command palette (Cmd+Shift+P / Ctrl+Shift+P)

---

### Issue: "Permission denied" when running scripts

**Solution:**
```bash
chmod +x specs/github-spec-kit/scripts/bash/*.sh
```

---

### Issue: "Output directory already exists"

**Solution:**
```bash
# Remove old output and start fresh
rm -rf specs/[your-branch-name]/
# Then re-run /specify command
```

---

### Issue: "Constitution file not found"

**Solution:**
```bash
# Verify constitution exists
ls -la memory/constitution.md

# If missing, check with team lead
```

---

### Issue: "Docker build fails"

**Solution:**
1. Check Docker is running: `docker ps`
2. Check Dockerfile syntax
3. Review error messages carefully
4. Check for missing dependencies in `requirements.txt` or `package.json`
5. Ask for help if stuck

---

### Issue: "Too many issues found, overwhelmed"

**Solution:**
1. **Prioritize**: Focus on CRITICAL and HIGH severity first
2. **Ask for help**: Bring issue summary to team meeting
3. **Break it down**: Fix one category at a time (Docker → Constitution → Shared Requirements)
4. **Document well**: Even if you can't fix everything, good documentation helps the next person

---

## Getting Help

**If you're stuck:**

1. **Check existing documentation**:
   - `specs/github-spec-kit/README.md`
   - `docs/team/methodologies/requirements-kit/guides/workflow.md`
   - `memory/constitution.md`

2. **Ask in team channel**:
   - Post your `ISSUE-SUMMARY.md`
   - Explain what you tried
   - Share error messages

3. **Schedule pair programming**:
   - Sometimes you just need another pair of eyes
   - Don't struggle alone for hours

---

## Success Criteria

**You've successfully completed this guide when:**

✅ **Updated SpecKit** to latest version
✅ **Cleaned workspace** of old test runs
✅ **Ran /specify** command successfully
✅ **Generated spec.md** in correct location
✅ **Read constitution** and understand requirements
✅ **Read shared requirements** and understand standards
✅ **Compared** input spec vs output spec
✅ **Documented** all missing items and issues
✅ **Updated spec.md** with fixes
✅ **Tested Docker** (if applicable)
✅ **Created issue summary** with clear next steps
✅ **Committed and pushed** all changes to your branch

**Great job! You're ready for the next team meeting. 🎉**

---

## Appendix: Module-Specific Notes

### AI Module Notes

**Special considerations:**
- LLM integration complexity
- Embeddings and vector search
- API key management
- Rate limiting and costs

**Common issues:**
- Missing OpenAI API configuration
- Vector database setup unclear
- Embedding model not specified

---

### Backend Module Notes

**Special considerations:**
- API design and REST principles
- Database schema and migrations
- Authentication and authorization
- Session management

**Common issues:**
- API endpoints not RESTful
- Database migrations not specified
- Auth strategy unclear

---

### Frontend Module Notes

**Special considerations:**
- Component architecture (React/Vue/etc.)
- State management (Redux/Vuex/etc.)
- UI/UX design system
- Responsive design requirements

**Common issues:**
- Component hierarchy unclear
- State management not specified
- Design system not referenced

---

### Publishing Module Notes

**Special considerations:**
- Multi-module integration
- Content rendering pipeline
- Export formats (PDF, HTML, etc.)
- Template management

**Common issues:**
- Integration points with AI/Backend not clear
- Export format details missing
- Template system not specified

---

**End of Guide**

