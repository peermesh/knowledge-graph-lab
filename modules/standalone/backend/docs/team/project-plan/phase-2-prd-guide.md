# Phase 2: Product Requirements Document (PRD) Guide

## Quick Overview
Phase 2 is where you transform your research into a clear plan. You'll create a Product Requirements Document (PRD) that specifies exactly what you'll build in Phase 3.

## What is a PRD?
A Product Requirements Document describes:
- **What** you're building (features, functionality)
- **Why** you're building it (problems it solves)
- **How** users will interact with it
- **Technical** approach and architecture

## PRD Structure for SpecKit

Your PRD must have these 4 sections to work with SpecKit:

### 1. SPECIFICATION (/specify)
**What to write:** Clear description of what your module does
**Length:** 1-2 paragraphs
**Focus:** User-facing functionality, not technical details

Example:
```markdown
## Specification
The Publishing Tools module enables users to distribute their knowledge graph insights across multiple channels. Users can select content from their knowledge graph, choose distribution channels (email, API, webhook), customize formatting templates, and schedule automated distributions. The system tracks engagement metrics and provides feedback on content effectiveness.
```

### 2. PLAN (/plan)
**What to write:** Technical architecture and technology choices
**Length:** 1-2 paragraphs
**Focus:** Tech stack, architecture patterns, key libraries

Example:
```markdown
## Plan
Built using Python FastAPI for the backend API with PostgreSQL for persistent storage. Uses Celery with Redis for task scheduling and queue management. Jinja2 templates for email formatting. SendGrid for email delivery, with webhook support via FastAPI endpoints. Frontend uses React with Material-UI components.
```

### 3. TASKS (/tasks)
**What to write:** Numbered list of implementation steps
**Length:** 10-15 tasks
**Focus:** Logical order of development

Example:
```markdown
## Tasks
1. Set up FastAPI project structure
2. Create database models for distribution channels
3. Implement email template system
4. Build SendGrid integration
5. Create webhook delivery system
6. Add content selection API endpoints
7. Implement scheduling system with Celery
8. Build metrics tracking
9. Create React frontend components
10. Add authentication and permissions
```

### 4. ACCEPTANCE CRITERIA
**What to write:** How to verify the module works
**Length:** 5-7 criteria
**Focus:** Testable requirements

Example:
```markdown
## Acceptance Criteria
- User can select content and send via email
- System successfully delivers to webhook endpoints
- Scheduled distributions execute on time
- Metrics dashboard shows delivery statistics
- Templates render correctly with user data
```

## File Naming and Location

Save your PRD here:
```
docs/team/module-assignments/[your-module]/deliverables/phase-2-planning/PRD.md
```

Replace `[your-module]` with:
- `backend`
- `frontend`
- `ai`
- `publishing`

## Tips for Writing Good PRDs

### DO:
- Be specific about features
- Use simple, clear language
- Include all 4 sections
- Think from the user's perspective
- Reference your Phase 1 research

### DON'T:
- Don't include code snippets
- Don't get too technical in the Specification
- Don't make tasks too large (break them down)
- Don't forget acceptance criteria
- Don't exceed 10 pages total

## How This Connects to SpecKit

SpecKit will read your PRD and:
1. Parse the Specification section to understand requirements
2. Use the Plan section to set up the tech stack
3. Follow the Tasks list to generate initial code
4. Validate against Acceptance Criteria

## Checklist Before Submission

- [ ] PRD has all 4 required sections
- [ ] Specification describes user-facing features
- [ ] Plan lists specific technologies
- [ ] Tasks are numbered and logical
- [ ] Acceptance criteria are testable
- [ ] File saved in correct location
- [ ] Total length is under 10 pages

## Example PRD Structure

```markdown
# [Module Name] Product Requirements Document

## Specification
[2-3 paragraphs describing what users can do]

## Plan
[1-2 paragraphs listing tech stack and architecture]

## Tasks
1. [First implementation step]
2. [Second implementation step]
...
15. [Final implementation step]

## Acceptance Criteria
- [Testable requirement 1]
- [Testable requirement 2]
...
- [Testable requirement 7]
```

## Getting Help

If you're stuck:
1. Review your Phase 1 research for ideas
2. Look at the module specification in `docs/modules/[your-module]/`
3. Ask your team lead for clarification
4. Keep it simple - MVPs don't need every feature

## Deadline
Submit your PRD by the Phase 2 deadline. Late submissions delay Phase 3 code generation.