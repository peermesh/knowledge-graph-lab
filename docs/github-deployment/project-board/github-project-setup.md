# GitHub Project Board Setup Instructions

## Project Configuration

**Project Title**: Knowledge Graph Lab Intern Program  
**Description**: 10-week internship project with 4 CS interns building modular AI research platform  
**Visibility**: Private (until ready for interns)

## Workflow Columns (Standard Development Flow)

### 1. Backlog
- **Purpose**: All open ideas/issues not yet prioritized
- **Auto-add**: New issues automatically added here
- **Label Filter**: None (catches all new issues)

### 2. To Do / Ready  
- **Purpose**: Selected backlog items planned for current sprint
- **Trigger**: Manual move from Backlog when prioritized
- **Label Filter**: `ready-for-work`, `sprint-planned`

### 3. In Progress
- **Purpose**: Issues currently being worked on
- **Auto-add**: When issue is assigned to team member
- **Trigger**: Manual move from To Do when work begins
- **Label Filter**: `in-progress`

### 4. In Review
- **Purpose**: Code is up in a pull request or under peer review
- **Auto-add**: When pull request is opened that references issue
- **Trigger**: Automatic when PR linked to issue
- **Label Filter**: `in-review`

### 5. Testing / QA
- **Purpose**: Items implemented but undergoing verification
- **Trigger**: Manual move from In Review when code review complete
- **Label Filter**: `testing`, `qa`

### 6. Blocked
- **Purpose**: Items waiting on dependency, external approval, or another team
- **Trigger**: Manual move from any column when blocked
- **Label Filter**: `blocked`, `waiting-for`

### 7. Done
- **Purpose**: Completed, merged, and tested items
- **Auto-add**: When issue is closed and PR is merged
- **Trigger**: Automatic when issue is closed
- **Label Filter**: None (final destination)

## Initial Setup Items

Add these 4 issues to project immediately:

1. **Issue #7**: [Module 1] Research Brief - Data Ingestion & Source Adapters
2. **Issue #8**: [Module 2] Research Brief - AI Knowledge Graph & Autonomous Research  
3. **Issue #9**: [Module 3] Research Brief - Reasoning Engine & Content Synthesis
4. **Issue #10**: [Module 4] Research Brief - Frontend & User Experience

**Initial Column**: All research briefs start in "To Do / Ready" (they're planned for Week 1)  
**Due Date**: Friday 5:00 PM (End of Week 1)  
**Labels**: `week-1-research`, `research-brief`, `module-[1-4]`

## Automation Rules

1. **New Issues → Backlog**: Automatically add new issues to Backlog
2. **Assigned → In Progress**: Move to In Progress when assigned
3. **PR Opened → In Review**: Move to In Review when PR references issue
4. **Issue Closed → Done**: Move to Done when issue is closed
5. **Label "blocked" → Blocked**: Move to Blocked column when blocked label applied

## Project Settings

- **Visibility**: Private initially, public after intern onboarding
- **Issue Templates**: Use existing 4 templates in `.github/ISSUE_TEMPLATE/`
- **Permissions**: Admin access for project lead, write access for interns
- **Milestones**: Week 1 Research, Week 2 Planning, Demo Day (Week 10)

---

**Setup Time**: 15-20 minutes via GitHub web interface  
**Manual Steps Required**: Project creation, column setup, automation rules  
**Ready for**: Immediate intern workflow support Monday morning