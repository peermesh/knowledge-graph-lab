# Kit Review Workflow

## Overview

This document defines the standard workflow for reviewing kit outputs to ensure quality and prevent pipeline failures. All kits must pass through these review phases before proceeding to the next development stage.

---

## Review Phases

### Phase 1: Automated Validation

- **Timing**: Immediately after kit execution
- **Tools**: Template detection, constraint validation, decision alignment scripts
- **Duration**: 5-10 minutes (automated)
- **Purpose**: Catch obvious issues before manual review

**Process**:

1. Run automated validation scripts
2. Review automated reports for issues
3. Fix any automated-identified problems
4. Re-run validation to confirm fixes

**Exit Criteria**:

- All automated checks pass
- No high-severity issues found
- Validation reports clean

**Responsible Party**: Kit Author

---

### Phase 2: Template Cleanup Verification

- **Timing**: After automated validation passes
- **Reviewer**: Requirements Author or Technical Writer
- **Duration**: 30-45 minutes per specification
- **Purpose**: Ensure no template contamination remains

**Process**:

1. Apply template cleanup verification checklist
2. Scan for known template patterns
3. Verify all requirements customized for specific system
4. Document any cleanup actions taken
5. Approve or request revisions

**Exit Criteria**:

- No template contamination patterns found
- All constraints customized for specific system
- Clear rationale provided for each requirement

**Responsible Party**: Technical Writer or Requirements Author

**Checklist**: `docs/process/template-cleanup-verification.md`

---

### Phase 3: Technical Feasibility Review

- **Timing**: After template cleanup verification passes
- **Reviewer**: Senior Developer or Technical Architect
- **Duration**: 1-2 hours per specification
- **Purpose**: Validate technical feasibility and implementation practicality

**Process**:

1. Read complete specification
2. Review against technical feasibility checklist
3. Identify any technical issues or concerns
4. Document required changes with rationale
5. Approve or request revisions

**Exit Criteria**:

- Technical feasibility confirmed
- No blocking technical issues
- Implementation approach clear

**Responsible Party**: Senior Developer or Technical Architect

**Checklist**: `docs/process/technical-feasibility-review.md`

---

### Phase 4: Business Necessity Review

- **Timing**: After technical review approval
- **Reviewer**: Product Owner or Business Stakeholder
- **Duration**: 30-60 minutes per specification
- **Purpose**: Validate business necessity and value

**Process**:

1. Review business necessity checklist
2. Assess business value of requirements
3. Identify any business concerns
4. Approve or request business justification

**Exit Criteria**:

- Business value confirmed
- Requirements aligned with strategy
- Success criteria appropriate

**Responsible Party**: Product Owner or Business Analyst

**Checklist**: `docs/process/business-necessity-review.md`

---

### Phase 5: Final Integration Review

- **Timing**: After all individual reviews complete
- **Reviewer**: Module Owner or Team Lead
- **Duration**: 30 minutes per specification
- **Purpose**: Ensure all reviews consistent and complete

**Process**:

1. Review all feedback from previous phases
2. Ensure all issues addressed
3. Confirm cross-kit consistency
4. Final approval for next phase

**Exit Criteria**:

- All previous reviews approved
- All issues resolved
- Cross-kit consistency verified
- Ready for next development phase

**Responsible Party**: Module Owner or Team Lead

---

## Escalation Procedures

### Technical Issues

**Level 1**: Technical reviewer cannot resolve
- **Action**: Escalate to Senior Architect
- **Timeline**: Within 1 business day
- **Decision Authority**: Senior Architect

**Level 2**: Senior Architect cannot resolve
- **Action**: Escalate to CTO or Technical Director
- **Timeline**: Within 2 business days
- **Decision Authority**: CTO

### Business Issues

**Level 1**: Business reviewer cannot resolve
- **Action**: Escalate to Product Director
- **Timeline**: Within 1 business day
- **Decision Authority**: Product Director

**Level 2**: Product Director cannot resolve
- **Action**: Escalate to CEO or Business Owner
- **Timeline**: Within 2 business days
- **Decision Authority**: CEO

### Cross-Kit Issues

**Level 1**: Module owner cannot resolve
- **Action**: Escalate to Program Manager
- **Timeline**: Within 1 business day
- **Decision Authority**: Program Manager

**Level 2**: Program Manager cannot resolve
- **Action**: Escalate to Project Sponsor
- **Timeline**: Within 2 business days
- **Decision Authority**: Project Sponsor

### Escalation Documentation

When escalating, provide:

1. Clear description of the issue
2. Context and background information
3. Previous attempts to resolve
4. Impact assessment (timeline, scope, cost)
5. Recommended options for resolution

---

## Review Documentation Requirements

### For Each Review

Document the following for every review phase:

- [ ] Review date and duration
- [ ] Reviewer name and role
- [ ] Specific issues found
- [ ] Resolutions implemented
- [ ] Approval status with rationale

### Review Artifacts

Maintain these artifacts for each specification:

- [ ] Completed checklists with responses
- [ ] Issue tracking with resolution details
- [ ] Approval documentation with signatures
- [ ] Change log of modifications made

### Documentation Location

Store review artifacts in:

- `.dev/ai/reviews/[kit-name]/[phase]-review-[date].md`

Example:

- `.dev/ai/reviews/spec-kit/template-cleanup-review-2025-10-15.md`

---

## Quality Gates

### Must Pass Before Next Phase

- [ ] Automated validation passes
- [ ] Template cleanup verified
- [ ] Technical review approved
- [ ] Business review approved
- [ ] Integration review complete

### Optional but Recommended

- [ ] Peer review by another team member
- [ ] Stakeholder consultation if major changes
- [ ] Cross-module impact assessment

---

## Review Workflow Diagram

```
Kit Execution Complete
        |
        v
Phase 1: Automated Validation
        |
        ├─ FAIL → Fix Issues → Re-run
        |
        v PASS
        |
Phase 2: Template Cleanup Verification
        |
        ├─ FAIL → Customize Requirements → Re-verify
        |
        v PASS
        |
Phase 3: Technical Feasibility Review
        |
        ├─ FAIL → Address Technical Issues → Re-review
        ├─ BLOCKED → Escalate to Senior Architect
        |
        v PASS
        |
Phase 4: Business Necessity Review
        |
        ├─ NEEDS REVISION → Justify Business Value → Re-review
        ├─ DEFERRED → Document for Future Phase
        ├─ REJECTED → Stop Process
        |
        v APPROVED
        |
Phase 5: Final Integration Review
        |
        ├─ ISSUES FOUND → Resolve and Re-review
        |
        v APPROVED
        |
Proceed to Next Development Phase
```

---

## Continuous Improvement

### After Each Review Cycle

- [ ] Document lessons learned
- [ ] Update checklists based on issues found
- [ ] Improve automated validation scripts
- [ ] Train team on new patterns discovered

### Quarterly Review

- [ ] Analyze review effectiveness metrics
- [ ] Update processes based on failure patterns
- [ ] Improve reviewer training materials
- [ ] Enhance automated validation capabilities

### Metrics to Track

- Review cycle time per phase
- Number of issues found per phase
- Time to resolution for issues
- Re-review rate (multiple cycles needed)
- Template contamination detection rate

---

## Frequently Asked Questions

### Can reviews run in parallel?

Technical and business reviews can run in parallel after template cleanup verification passes. This reduces overall cycle time.

### What if a reviewer is unavailable?

Each review role should have a designated backup. If both are unavailable, escalate to the next level for assignment.

### How do we handle urgent changes?

Urgent changes still go through all phases but with compressed timelines. Document the urgency rationale and expedite review scheduling.

### What constitutes a blocking issue?

A blocking issue prevents the specification from being implemented as written. Examples: contradictory constraints, unavailable technology, fundamental architectural mismatch.

---

- **Document Version**: 1.0
- **Last Updated**: October 2025
- **Related**: technical-feasibility-review.md, business-necessity-review.md, template-cleanup-verification.md
