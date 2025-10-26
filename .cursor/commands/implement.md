---
description: "Execute implementation tasks systematically"
---

# SpecKit Implement Command

Executes the structured task list to build working software systems.

**Usage:**
1. Have a structured task list with dependencies
2. Run this command to begin systematic implementation
3. Monitor progress and handle errors as they occur

**Input:** Structured task list with dependencies and effort estimates
**Output:** Working software implementation

**Key Features:**
- Executes tasks in dependency order
- Handles parallel task execution where possible
- Provides progress updates and status tracking
- Manages error recovery and task retries
- Follows Test-Driven Development (TDD) approach

**Execution Modes:**
- **Sequential**: Execute one task at a time
- **Parallel**: Execute independent tasks simultaneously
- **Error Recovery**: Retry failed tasks with backoff

**Example:**
```
Implement the AI Development Module according to the structured task list. Start with database setup, then API development, followed by frontend implementation.
```

**Prerequisites:**
- All required tools installed (check with `/speckit.check`)
- Task list validated and dependencies resolved
- Development environment properly configured
- Tests pass before implementation begins

**Error Handling:**
- Failed tasks are marked for manual review
- Dependencies are checked before each execution
- Rollback procedures available for critical failures


