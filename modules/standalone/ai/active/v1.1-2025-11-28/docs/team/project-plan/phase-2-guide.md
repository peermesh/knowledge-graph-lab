# Phase 2: Planning & Product Requirements Documents (PRDs)

## ✅ Quick Checklist

1. ☐ Read this Phase 2 Guide completely
2. ☐ Read the [SpecKit Guide](../speckit-guide.md) - CRITICAL for PRD format
3. ☐ Review example PRD: `../module-assignments/publishing-tools/deliverables/phase-2-planning/examples/PRD-example.md`
4. ☐ Use PRD structure from SpecKit Guide (not just any template!)
5. ☐ Fill out your PRD (10-15 pages) with all required sections
6. ☐ Validate PRD completeness using Quality Checklist (see below)
7. ☐ Save to: `../module-assignments/[your-module]/deliverables/phase-2-planning/PRD.md`
8. ☐ Submit PR from your `[github-username]/work` branch (see [Git Workflow](../git-workflow.md))

## Quick Start

**Goal**: Transform your Phase 1 research into a clear Product Requirements Document (PRD) that can generate working code.

**Timeline**: 2 weeks

**Deliverable**: A complete PRD in your module's phase-2 folder that SpecKit can use to generate initial code.

---

## What is a PRD?

A Product Requirements Document describes **WHAT** your module needs to do and **WHY**, without explaining **HOW** to build it.

### Good PRD Example
✅ "Users must be able to upload images up to 10MB in JPEG, PNG, or GIF format"

### Bad PRD Example
❌ "Use multer middleware with Express.js to handle multipart/form-data for image uploads"

---

## Your PRD Structure

**IMPORTANT**: Your PRD must follow the SpecKit-compatible format. See the [SpecKit Guide](../speckit-guide.md) for the exact structure required.

Save your PRD to: `docs/team/module-assignments/[your-module]/deliverables/phase-2-planning/PRD.md`

```markdown
# Product Requirements Document: [Your Module Name]

**Module**: [Backend/Frontend/AI/Publishing]
**Author**: [Your Name]
**Date**: [YYYY-MM-DD]
**Status**: Draft

## 1. Module Overview
[2-3 sentences describing what your module does]

## 2. User Stories

### Primary User Story
As a [type of user], I want to [action] so that [benefit].

### Secondary Stories
1. As a [user], I want to [action] so that [benefit]
2. As a [user], I want to [action] so that [benefit]

## 3. Functional Requirements

### Core Features (MUST have)
- FR-001: System MUST [specific capability]
- FR-002: System MUST [specific capability]
- FR-003: Users MUST be able to [action]

### Nice-to-Have Features (SHOULD have)
- FR-101: System SHOULD [optional capability]
- FR-102: System SHOULD [optional capability]

## 4. Data Requirements

### Key Entities
- **[Entity Name]**: [What it represents, key information it contains]
- **[Entity Name]**: [What it represents, relationships]

### Data Constraints
- Data retention: [How long to keep data]
- Data size limits: [Maximum sizes]
- Privacy requirements: [What needs protection]

## 5. Integration Points

### Inputs (What this module receives)
- From [Module]: [Type of data/request]
- From [Module]: [Type of data/request]

### Outputs (What this module provides)
- To [Module]: [Type of data/response]
- To [Module]: [Type of data/response]

## 6. Acceptance Criteria

### Scenario 1: [Name]
**Given** [initial state]
**When** [action occurs]
**Then** [expected outcome]

### Scenario 2: [Name]
**Given** [initial state]
**When** [action occurs]
**Then** [expected outcome]

## 7. Non-Functional Requirements

### Performance
- Response time: [e.g., < 200ms for API calls]
- Throughput: [e.g., handle 100 concurrent users]

### Security
- Authentication: [Required/Not required]
- Data encryption: [Required/Not required]

### Scalability
- Expected load: [e.g., 1000 requests/minute]
- Growth projection: [e.g., 10x in first year]

## 8. Constraints & Assumptions

### Constraints
- Budget: [Any cost limitations]
- Timeline: [Phase 3 MVP deadline]
- Technology: [Any required tech from Phase 1 research]

### Assumptions
- [Assumption about users/system/data]
- [Assumption about users/system/data]

## 9. Success Metrics
- Metric 1: [How you'll measure success]
- Metric 2: [How you'll measure success]

## 10. Open Questions
[Mark anything unclear with: NEEDS CLARIFICATION: specific question]
```

---

## Module-Specific Guidance

### Backend Module
Focus on:
- API endpoints needed (what they do, not how)
- Database entities and relationships
- Authentication/authorization requirements
- Data validation rules

### Frontend Module
Focus on:
- User interface components needed
- User interactions and flows
- Data display requirements
- Responsive design needs

### AI Module
Focus on:
- Input data requirements
- Expected outputs/insights
- Accuracy requirements
- Processing time limits

### Publishing Module
Focus on:
- Distribution channels (email, API, webhooks)
- Content formatting requirements
- Scheduling/timing needs
- Personalization requirements

---

## Converting Research to PRD

### Step 1: Review Your Phase 1 Research
Go through your 10-page research brief and extract:
- Key findings that impact requirements
- Technology recommendations
- Best practices discovered

### Step 2: Translate to Requirements

| Research Finding | PRD Requirement |
|-----------------|----------------|
| "JWT is industry standard for auth" | FR-001: System MUST authenticate users |
| "PostgreSQL handles JSON well" | Data: Support flexible schema for user preferences |
| "Users expect < 3 second load" | Performance: Page load < 3 seconds |

### Step 3: Add User Context
For each requirement, ask:
- Who needs this? (User type)
- What do they need? (Feature)
- Why do they need it? (Benefit)

### Step 4: Make it Testable
Each requirement should be verifiable:
- ❌ Vague: "System should be fast"
- ✅ Testable: "API responses return within 200ms for 95% of requests"

---

## Quality Checklist

Before submitting your PRD:

- [ ] No implementation details (no code, frameworks, libraries)
- [ ] All requirements are testable
- [ ] User stories cover main use cases
- [ ] Integration points with other modules defined
- [ ] Acceptance criteria are clear
- [ ] Open questions are marked with NEEDS CLARIFICATION
- [ ] Document is under 15 pages

---

## What Happens Next?

1. **SpecKit Processing**: Your PRD will be processed by SpecKit to generate initial code
2. **Phase 3 Development**: AI agents will refine the generated code into a working MVP
3. **Your Role**: Review generated code, test functionality, provide feedback

---

## Common Mistakes to Avoid

### ❌ Too Technical
"Implement REST API using Express.js with PostgreSQL database"

### ✅ Just Right
"System must provide API access to user data with standard authentication"

### ❌ Too Vague
"Make it user-friendly"

### ✅ Specific
"Users must complete signup in under 3 steps taking less than 2 minutes"

### ❌ Missing Integration
"My module works independently"

### ✅ Connected
"Receives user data from Backend API, sends formatted content to Publishing module"

---

## Need Help?

- **SpecKit PRD Structure**: [speckit-guide.md](../speckit-guide.md) - MUST READ for PRD format
- **Git Workflow**: [git-workflow.md](../git-workflow.md) - How to submit your work
- **Example PRD**: `docs/team/module-assignments/publishing-tools/deliverables/phase-2-planning/examples/PRD-example.md`
- **SpecKit Tools**: `.dev/tools/speckit-user-guide.md` - For Phase 3 code generation
- Ask in team chat
- Mark uncertainties with NEEDS CLARIFICATION

---

## Submission

1. Save your PRD to: `docs/team/module-assignments/[your-module]/deliverables/phase-2-planning/PRD.md`
2. Create a pull request from your `[github-username]/work` branch
3. Title: "Phase 2 PRD: [Your Module]"
4. Due: [2 weeks from Phase 1 completion]

Remember: Focus on WHAT and WHY, not HOW. SpecKit will handle the HOW.