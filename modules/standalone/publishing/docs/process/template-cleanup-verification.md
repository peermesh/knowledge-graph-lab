# Template Content Quality Review Checklist

- **Reviewer Role**: Requirements Author or Technical Writer
- **Purpose**: Validate the QUALITY of project-specific content that replaced template placeholders.
- **Review Duration**: 30-45 minutes per specification

---

## ✅ Pre-Review: Automated Validation (MUST PASS FIRST)

**CRITICAL**: Before manual review, ensure automated validation passes:

```bash
# PRIMARY validation - must return exit code 0
python3 scripts/validate_kit_integrity.py <requirements-file>
```

**If validation fails**:

- Exit Code 1: Unfilled placeholders → Author must complete template first
- Exit Code 2: Template contamination → Author must rewrite with project-specific content
- **Do not proceed with manual review until exit code 0**

This automated check eliminates the need for manual contamination detection.

---

## Content Quality Verification (Post-Automation)

**Focus**: Since automation catches unfilled placeholders and contamination, manual review validates content QUALITY and COMPLETENESS.

### 1. Constraint Specificity

- [ ] Each constraint is specific to THIS project (not generic)
- [ ] Technology choices have clear, project-specific rationale
- [ ] Deployment requirements match actual infrastructure plans (named systems/platforms)
- [ ] Performance targets based on THIS system's actual user requirements (with numbers/evidence)

**Example Good Constraint**:
```
Must use PostgreSQL 14+ - Existing 50GB customer dataset already in PostgreSQL,
migration cost $50k+, team has 5 years PostgreSQL expertise
```

**Example Bad (But Not Contamination)**:
```
Must use PostgreSQL - It's a good database and we need a database
```
*Note: Not contamination, but too generic - needs specific PROJECT rationale*

### 2. Rationale Completeness

- [ ] Business justification provided (WHY this serves business needs)
- [ ] Technical justification provided (WHY this is technically necessary)
- [ ] Cost/benefit analysis included where relevant
- [ ] Implementation impact described (WHAT developers must do)

### 3. Context Appropriateness

- [ ] Requirements reflect THIS system's actual usage patterns
- [ ] Constraints appropriate for THIS system's target user base
- [ ] Integration requirements based on THIS system's real dependencies
- [ ] Success criteria measurable and specific to THIS system

### 4. Discovery Alignment

- [ ] Requirements match Discovery Kit technology decisions
- [ ] Rationale consistent with Discovery Kit findings
- [ ] Deviations from Discovery are documented and approved
- [ ] Integration points from Discovery are addressed

### 5. Documentation Quality

- [ ] Alternatives considered and rejection rationale provided
- [ ] Trade-offs explicitly stated
- [ ] Future maintenance implications considered
- [ ] Assumptions clearly documented

---

## Approval Criteria

All criteria must be met for approval:

- [x] ✅ Automated validation passed (exit code 0) - **MANDATORY PREREQUISITE**
- [ ] All constraints are project-specific with clear rationale
- [ ] Requirements are technically feasible (verified via technical review)
- [ ] Requirements are business-justified (verified via business review)
- [ ] Discovery Kit decisions properly reflected

---

## Focus Areas (Common Quality Issues)

Since contamination is caught by automation, focus manual review on these quality issues:

### Weak Rationale (Not Contamination, But Poor Quality)
- **Issue**: "Must use Docker - It's industry standard"
- **Fix**: "Must deploy to company's existing Kubernetes cluster - $500k 3-year investment, security team manages infra, existing monitoring/backup"

### Generic Without Being Contaminated
- **Issue**: "Must support many users"
- **Fix**: "Must support 10,000 concurrent users - Launch target 5,000 users, 2x growth in Q1, load testing validates 10k capacity"

### Missing Project Context
- **Issue**: "Must use REST API"
- **Fix**: "Must use REST API - Integrating with existing customer mobile apps (iOS/Android) that only support REST, 50k active users"

### Incomplete Implementation Guidance
- **Issue**: "System should be fast"
- **Fix**: "Response time <200ms for 95th percentile - User research shows 250ms perceived as slow, competitor benchmarks at 180ms, our target 200ms"

## Historical Note: Contamination Detection (Now Automated)

**Prior to October 2025**, reviewers manually detected template contamination patterns like:

- "Cannot write to local filesystem"
- "Must run on AWS ECS"
- "Must be deployable as a Docker container"

**As of October 2025**, these patterns are automatically detected by `validate_kit_integrity.py` (exit code 2).

Manual reviewers no longer need to check for contamination - focus on content quality instead.

## Documentation Requirements

When completing this review, document:

1. **Review Date**: [Date completed]
2. **Reviewer Name**: [Your name]
3. **Specification Version**: [Version reviewed]
4. **Template Patterns Found**: [List each pattern with location]
5. **Cleanup Actions Taken**: [Describe customization performed]
6. **Approval Status**: [Pass/Fail with rationale]

## Escalation Criteria

Escalate to Module Owner if:

- Major template contamination requires specification rewrite
- Contradictory requirements indicate fundamental misunderstanding
- Customization requires additional stakeholder input
- Discovery Kit decisions need reconsideration

---

- **Document Version**: 1.0
- **Last Updated**: October 2025
- **Related**: technical-feasibility-review.md, business-necessity-review.md, review-workflow.md
