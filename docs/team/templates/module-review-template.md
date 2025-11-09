# Module Review & Gap Analysis Template

**Module**: [Your Module Name - AI, Backend, Frontend, or Publishing]  
**Date**: [Review Date]  
**Reviewer**: [Your Name]  
**Branch**: [Your branch name]

---

## What You've Done

### Completed Work Summary

**Features Implemented:**
- [ ] Feature 1: [Brief description]
- [ ] Feature 2: [Brief description]
- [ ] Feature 3: [Brief description]

**Components Built:**
- [ ] Component 1: [Description]
- [ ] Component 2: [Description]
- [ ] Component 3: [Description]

**Integration Points Completed:**
- [ ] Integration point 1: [Description]
- [ ] Integration point 2: [Description]

**Progress Since Last Review:**
- [What has been accomplished since the last meeting/demo]

---

## Concerns & Issues

### Things That Look Like They Weren't Done Correctly

**❌ [Issue Name]**
- **What's wrong**: [Clear description of the problem]
- **Where it occurs**: [Specific file/component/feature]
- **Impact**: [Why this matters - what it prevents or breaks]
- **Why it happened**: [Root cause if known]
- **Fix needed**: [What needs to be done to resolve it]

**❌ [Issue Name]**
- **What's wrong**: [Clear description]
- **Where it occurs**: [Specific location]
- **Impact**: [Why this matters]
- **Why it happened**: [Root cause]
- **Fix needed**: [Resolution steps]

### Known Bugs or Problems

**🐛 [Bug Name]**
- **Description**: [What the bug does]
- **Steps to reproduce**: [How to see the bug]
- **Severity**: High / Medium / Low
- **Workaround**: [If any exists]

### Unclear Requirements

**❓ [Requirement/Feature Name]**
- **What's unclear**: [Specific question or ambiguity]
- **Where it came from**: [Spec document, conversation, etc.]
- **Blocking**: [What this prevents you from doing]
- **What you need**: [Clarification needed]

### Technical Debt

**⚠️ [Technical Debt Item]**
- **What was done**: [Shortcut or temporary solution taken]
- **Why**: [Reason for the shortcut]
- **Impact**: [What this means for future work]
- **When to fix**: [Suggested timeline]

---

## Remaining Work

### What's Left to Do

**Specific Tasks to Complete Standalone Module:**

1. **[Task Name]**
   - **Description**: [What needs to be done]
   - **Priority**: High / Medium / Low
   - **Estimated time**: [Hours or days]
   - **Dependencies**: [What this depends on]

2. **[Task Name]**
   - **Description**: [What needs to be done]
   - **Priority**: High / Medium / Low
   - **Estimated time**: [Hours or days]
   - **Dependencies**: [What this depends on]

3. **[Task Name]**
   - **Description**: [What needs to be done]
   - **Priority**: High / Medium / Low
   - **Estimated time**: [Hours or days]
   - **Dependencies**: [What this depends on]

### Blockers Identified

**🚫 [Blocker Name]**
- **What's blocking**: [Clear description]
- **Why it's blocking**: [What work is prevented]
- **Who can help**: [Person/team that can resolve]
- **Alternative approach**: [If any exists]

### Timeline Estimate

**To Complete Standalone Module:**
- **Optimistic estimate**: [Best case scenario]
- **Realistic estimate**: [Most likely scenario]
- **Pessimistic estimate**: [Worst case scenario]
- **Confidence level**: High / Medium / Low

**Reasoning**: [Explain your estimates]

### Dependencies

**What You Need from Others:**
- [ ] [Dependency 1]: [What you need and from whom]
- [ ] [Dependency 2]: [What you need and from whom]

**What You Need from the System:**
- [ ] [System requirement 1]: [What's needed]
- [ ] [System requirement 2]: [What's needed]

---

## Standalone Module Assessment

### Current State

**How Close to Standalone Module Status?**

**✅ Completed Requirements:**
- [ ] Module runs in Docker successfully
- [ ] Docker container starts in < 30 seconds
- [ ] Core functionality implemented
- [ ] API endpoints functional (if applicable)
- [ ] Health check endpoint working
- [ ] Documentation complete
- [ ] Basic tests passing

**❌ Missing Requirements:**
- [ ] [Requirement that's missing]
- [ ] [Another missing requirement]

**Current Completion Percentage**: [Estimate: X%]

### Gap Analysis

**What's Missing to Be Truly Standalone:**

1. **[Gap Category]**
   - **What's missing**: [Specific gap]
   - **Impact**: High / Medium / Low
   - **Effort to fix**: [Estimated effort]
   - **Priority**: [When this should be addressed]

2. **[Gap Category]**
   - **What's missing**: [Specific gap]
   - **Impact**: High / Medium / Low
   - **Effort to fix**: [Estimated effort]
   - **Priority**: [When this should be addressed]

**Gap Categories to Consider:**
- Missing core features
- Integration points not ready
- Performance requirements not met
- Documentation gaps
- Testing gaps
- Docker/containerization issues
- Configuration/deployment issues

### Success Criteria

**What "Done" Means for Your Module:**

**MVP/Standalone Module Definition:**
- [ ] [Criterion 1]: [Specific, measurable goal]
- [ ] [Criterion 2]: [Specific, measurable goal]
- [ ] [Criterion 3]: [Specific, measurable goal]

**Example criteria:**
- Module runs in Docker without crashing
- All critical use cases work end-to-end
- API returns responses in < 500ms
- Documentation allows another developer to run it
- Health checks pass consistently

---

## Docker Demo Status

### Current Demo Capabilities

**What Works in Docker:**
- [ ] [Feature 1]: [What you can demonstrate]
- [ ] [Feature 2]: [What you can demonstrate]
- [ ] [Feature 3]: [What you can demonstrate]

**What Doesn't Work Yet:**
- [ ] [Feature 1]: [What's broken or incomplete]
- [ ] [Feature 2]: [What's broken or incomplete]

**Demo Script:**
```bash
# Commands to run your demo
docker build -t [module-name] .
docker run -p [port]:[port] [module-name]
# Then demonstrate:
# [Step 1]
# [Step 2]
# [Step 3]
```

**Known Issues During Demo:**
- [Any things that might break or look wrong during the demo]

---

## Overall Assessment

### Ready for Next Phase?

**Standalone Module Status**: ❌ Not Ready / ⚠️ Partially Ready / ✅ Ready

**Explanation**: [Why this status]

### Critical Blockers

**List any blockers that prevent progress:**
1. [Blocker 1]
2. [Blocker 2]

### Nice-to-Have Improvements

**Things that can wait until after standalone module is complete:**
- [Improvement 1]
- [Improvement 2]

---

## Notes & Additional Context

**Anything else relevant for the review:**
- [Additional notes, context, or information]

---

## How to Use This Template

1. **Read the detailed guide**: See [Module Review & Gap Analysis Template Guide](module-review-template-guide.md) for detailed explanations of each section, examples, and tips
2. **Copy this template** to your module's deliverables folder or work-in-progress folder
3. **Fill in all sections** - be honest and thorough (use the guide for help)
4. **Name it**: `[date]-[module-name]-review.md` (e.g., `2025-11-10-ai-module-review.md`)
5. **Commit it** to your branch before the meeting
6. **Reference it** during your demo and discussion

**Remember**: This is an iterative process. The goal is to show progress, identify issues, and plan next steps - not to have everything perfect.

**Need Help?** See the [detailed guide](module-review-template-guide.md) for explanations, examples, and tips for each section.

