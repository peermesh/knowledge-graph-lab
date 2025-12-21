# RequirementsKit Methodology: How to Create Comprehensive Input

**Purpose**: Detailed guide on creating 500-1000 line comprehensive documents that SpecKit transforms into implementation-ready specifications
**Audience**: Team members gathering requirements and creating specs
**Last Updated**: 2025-10-09

> **Quick Start**: If this is your first time, start with [quickstart.md](quickstart.md) for navigation, then return here for detailed methodology.

---

## Introduction

### What You Need to Know

**The Big Surprise**: SpecKit doesn't create specs from scratch. It *enhances* detailed requirements documents you create first.

**What This Means for You**:

- Spend 2-4 days gathering requirements through conversation with an AI agent
- Create a 500-1000 line comprehensive document
- *Then* use SpecKit to formalize it

**Time Investment**:

- ❌ Wrong approach: 30 minutes with `/specify` → Get weak 126-line spec with gaps
- ✅ Right approach: 2-4 days gathering requirements → Get implementation-ready 576-line spec

**Bottom Line**: The quality of your spec depends on the quality of the requirements document you create *before* using SpecKit.

### Why This Methodology Exists

**RequirementsKit Methodology** guides you through creating comprehensive Product Requirements Documents (PRDs) that SpecKit transforms into implementation-ready specifications.

**The Problem It Solves**: SpecKit needs rich, detailed input (called a **Comprehensive Source**) to produce quality output. Without comprehensive source material, SpecKit produces generic specs with gaps. This methodology ensures you create that comprehensive input.

**The Result**: 500-1000 line Comprehensive Source documents that SpecKit transforms into implementation-ready specifications with all details intact.

---

## Understanding the Process

### What We Learned from the Agents Project

We analyzed how the agents infrastructure project successfully used SpecKit. Here's what actually happened:

#### The Timeline

**Week 1: Requirements Gathering** (No SpecKit yet!)

- **Day 1-2** (4-8 hours): Team member + AI agent had conversations about the problem
  - Discussed pain points, scale, goals
  - Agent asked 50+ clarifying questions
  - Created 10 detailed use cases

- **Day 3-4** (6-10 hours): Technical deep dive
  - Agent proposed complete database schema
  - Wrote example workflows
  - Defined performance targets
  - Broke into implementation phases

- **Day 5** (2-4 hours): Assembled everything
  - Created comprehensive 967-line document
  - Included ALL technical details
  - **This became the input to SpecKit**

**Week 2: SpecKit Enhancement**

- **Day 1**: Fed comprehensive doc to specialist agents (database expert, UI expert, etc.)
- **Day 2**: Merged all specialist versions into final 576-line implementation-ready spec
- **Day 3-4**: Used `/plan` and `/tasks` to create execution plan

#### The Results

**Starting with comprehensive requirements:**

- ✅ 576-line implementation-ready spec
- ✅ 36 specific, testable requirements
- ✅ 20 performance targets with numbers
- ✅ Complete database schema with exact SQL
- ✅ 40+ edge cases documented
- ✅ Zero gaps or clarifications needed
- ✅ Team started implementing immediately

**Starting without comprehensive requirements:**

- ❌ 126-line generic spec
- ❌ 8 vague requirements
- ❌ No performance targets
- ❌ No complete schema
- ❌ 3 edge cases
- ❌ Multiple [NEEDS CLARIFICATION] markers
- ❌ Implementation team had 50+ questions

### The 5-Phase Pipeline

This methodology follows a proven process validated by the Project Tracking SQLite case study, which demonstrated that comprehensive input (967 lines) produces implementation-ready SpecKit output (576 lines).

**High-level overview** (see [workflow.md](workflow.md) for detailed work orders WO-1 through WO-5):

```
Phase 1: Conversation Distillation (2-3 hours)
  └─ Create MVP decisions document → 00-{module}-decisions.md
      ↓
Phase 2: Information Gathering (4-6 hours)
  ├─ Find all related documentation
  ├─ Index interrelationships
  ├─ Identify gaps in understanding
  └─ Document sources → 01-INFORMATION-SOURCES-INDEX.md
      ↓
Phase 3: Comprehensive Spec Creation (8-10 hours)
  ├─ Fill all 10 template sections
  ├─ Create Comprehensive Source (800-1500 lines)
  ├─ Note gaps and assumptions
  └─ Output → 05-COMPREHENSIVE-SPEC.md
      ↓
Phase 4: Quality Refinement (3-4 hours)
  ├─ Compare to case study benchmark
  ├─ Remove implementation details
  ├─ Tighten to requirements focus
  └─ Output → 10-FINAL-SPEC.md (500-700 lines)
      ↓
Phase 5: Validation (3-4 hours)
  ├─ Completeness validation
  ├─ Integration point verification
  ├─ GO/NO-GO decision
  └─ Output → 11-IMPLEMENTATION-READINESS.md
```

For detailed task breakdowns and dependencies, see the work order flow in [workflow.md](workflow.md).

---

## Deep Dive: The 10 Essential Sections

Now that you understand the overall process and timeline, let's examine each of the 10 sections you need to create in detail. Each section below includes:
- What you need to deliver
- Concrete examples from real projects
- How to gather the information
- Common pitfalls to avoid

---

### 1. Problem Statement (50-100 lines)

**What you need:**

- What's broken today? (Be specific with numbers)
- Who is affected?
- What's the scale? (How many users? How much data?)
- What does success look like?

**Example from agents project:**

```text
Current Issues:
1. Race Conditions: Multiple agents writing simultaneously can clobber files
2. Query Limitations: Can't answer "Time spent per project this week?"
3. No Aggregation: Grep/awk parsing is slow and error-prone

Context: User manages 12+ concurrent projects with 20+ AI agents running simultaneously

Goal: Migrate to SQLite database with real-time dashboard
Success: Dashboard loads in <5 seconds, 20+ agents write without conflicts
```

**How to gather this:**

1. Ask the team: "What hurts right now?"
2. Get numbers: "How many X do we have? How long does Y take?"
3. Define success: "What would make this problem go away?"

---

### 2. Detailed Use Cases (10+ scenarios)

**What you need:**

For each major scenario, write:

- Who is doing what
- What happens today (current behavior)
- What should happen (desired behavior)
- How you'll know it worked (success criteria)
- Include scale numbers

**Example format:**

```text
UC1: Morning Routine
- Who: User waking up after 8 hours offline
- Current: Must read 5+ markdown files manually to understand status
- Desired: Single dashboard shows all project health in <5 seconds
- Success: User sees green/yellow/red indicators, recent activity, what needs attention
- Scale: 12 projects, 200+ activities from yesterday
```

**How to gather this:**

1. Interview team members: "Walk me through your typical workflow"
2. Capture edge cases: "What happens when X goes wrong?"
3. Get scale: "How many times per day? How much data?"

**Tip**: Aim for 10 use cases. If you have fewer than 5, you haven't explored enough.

---

### 3. Complete Data Model (if your feature involves data)

**What you need:**

- Every table with exact columns
- Data types for each column
- Relationships between tables
- Indexes for performance
- Constraints (unique, not null, etc.)

**Example:**

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    display_name TEXT,
    status TEXT DEFAULT 'active',
    health TEXT DEFAULT 'green',
    last_activity_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_health ON projects(health);
```

**How to gather this:**

1. List all the "things" in your system (projects, users, activities, etc.)
2. For each thing, list all its properties
3. Ask: "What do we need to query quickly?" → Those need indexes
4. Ask: "What must be unique?" → Those need constraints

**Tip**: Don't say "we need a database." Show the actual tables with actual columns.

---

### 4. Example Workflows (3-5 detailed scenarios)

**What you need:**

- Step-by-step execution of key scenarios
- Actual commands or queries that would run
- Expected output at each step
- What happens when things go wrong

**Example:**

```text
Workflow: New Agent Joins Mid-Task

Step 1: Agent queries "What am I blocked on?"
Command:
  SELECT task.title, blocking_task.title, blocking_task.status
  FROM tasks task
  JOIN task_dependencies ON dependent_task_id = task.id
  WHERE task.assigned_agent_id = 42

Step 2: System shows results
Output:
  My Task: "Build Python library"
  Blocked By: "Create database schema"
  Blocker Status: "in_progress"

Step 3: Agent understands
Result: "I'm waiting for schema creation to complete"
```

**How to gather this:**

1. Pick your most important scenarios
2. Write them like a recipe: First do X, then Y happens, then do Z
3. Use real commands, real queries, real UI interactions
4. Show what the user sees at each step

---

### 5. Performance Targets (with numbers!)

**What you need:**

- Response time targets (use milliseconds or seconds)
- Throughput targets (how many concurrent users/operations)
- Scale limits (how much data before it breaks)
- Resource limits (memory, disk, CPU)

**Example:**

```text
Performance Targets:
- Single query: <10ms
- Complex join query: <100ms
- Dashboard page load: <500ms
- Full-text search: <1 second (even with 50,000 records)
- Concurrent writes: Support 20 agents without lock errors
- Database size: <10MB for 10,000 activities
```

**How to gather this:**

1. Ask: "How fast is fast enough?"
2. Ask: "How many users at once?"
3. Ask: "How much data will we have?"
4. Test with realistic numbers, not "should be fast"

**Tip**: Vague = useless. "Fast" is not a target. "<100ms" is a target.

---

### 6. Implementation Phases (3-7 phases)

**What you need:**

- Break the work into phases (MVP first, then enhancements)
- For each phase: goal, deliverables, time estimate, success criteria
- Show dependencies (what must happen before each phase)

**Example:**

```text
Phase 1: Core Database (2-3 hours)
Goal: Get basic data writing to SQLite
Deliverables:
  - Database schema script
  - Python library for CRUD operations
  - Updated tracking scripts to write to both markdown and SQLite
Success: 100% of writes go to both systems, counts match
Dependencies: None (first phase)

Phase 2: Web Dashboard (2-3 hours)
Goal: View data in browser
Deliverables:
  - Flask app with overview page
  - Project detail pages
  - Auto-refresh every 10 seconds
Success: Dashboard loads in <500ms, shows real-time data
Dependencies: Phase 1 complete (need database first)
```

**How to gather this:**

1. Ask: "What's the minimum viable version?"
2. Ask: "What comes next after MVP?"
3. Estimate hours realistically (add buffer)
4. Define "done" for each phase

---

### 7. Edge Cases (20+ scenarios)

**What you need:**

- What happens when things fail?
- What happens at boundaries (empty data, huge data, malformed data)?
- What happens with concurrent access?
- What happens during migration or upgrades?

**Example:**

```text
Edge Cases:
1. Migration interrupted mid-process
   → Transaction rollback, no partial data, can retry

2. 50 agents writing simultaneously
   → Connection pooling, lock timeout handling, retry logic

3. Dashboard with 50,000 activities
   → Pagination (100 per page), infinite scroll

4. Invalid markdown format
   → Skip invalid entries, log errors, continue processing

5. User deletes project with active agents
   → Block deletion, show error: "3 agents still working on this"
```

**How to gather this:**

1. Ask: "What could go wrong?"
2. Ask: "What happens at the extremes?"
3. Ask: "What about concurrent users?"
4. Think about Murphy's Law

**Tip**: If you have fewer than 20 edge cases, you're not thinking hard enough.

---

### 8. Technology Constraints

**What you need:**

- What technologies must you use (or can't use)?
- Why did you choose X over Y?
- What are the dependencies on external tools?

**Example:**

```text
Technology Constraints:

SQLite (not PostgreSQL):
✅ No server needed
✅ Single file, easy backup
✅ Built into Python
✅ Perfect for local use
❌ Not for multi-server (but we don't need that)

Python for library (not Bash):
✅ Better SQLite support
✅ Easier error handling
✅ Flask integration later
```

**How to gather this:**

1. List technology choices you've made
2. Explain why (don't just say "because we know it")
3. Acknowledge tradeoffs

---

### 9. Out of Scope (explicit list)

**What you need:**

- What are you NOT building?
- Why are you deferring those features?
- When might you build them?

**Example:**

```text
Out of Scope (Not in V1):
1. Multi-user concurrent access from different machines
   Why: This is a single-user local tool
   Future: Maybe in V2 if we need team collaboration

2. Cloud synchronization
   Why: Local-first approach, no cloud dependency
   Future: Could add if users request it

3. Mobile app
   Why: Desktop-first, responsive web is enough
   Future: Not planned
```

**How to gather this:**

1. List features someone might expect but you're not building
2. Explain why (scope, time, priorities)
3. Be clear about what's deferred vs what's permanently excluded

**Tip**: Being explicit about what you're NOT building prevents scope creep.

---

### 10. Testing Strategy

**What you need:**

- What kinds of tests (unit, integration, load, etc.)?
- What specific things need testing?
- What are the acceptance criteria?

**Example:**

```text
Testing Strategy:

Unit Tests:
- Database CRUD operations (all tables)
- Concurrent write handling
- Data validation and constraints

Integration Tests:
- Tracking script writes to both markdown and SQLite
- Dashboard shows correct data from database
- Dependency resolution triggers work end-to-end

Load Tests:
- 100 concurrent tracking script calls
- Dashboard with 10,000 activities (performance)
- 50 browsers refreshing simultaneously

Acceptance:
- All tests pass
- No data loss in 1000 concurrent operations
- Queries complete in <100ms
```

**How to gather this:**

1. Ask: "What could break?"
2. Ask: "How will we know it works at scale?"
3. Define pass/fail criteria

---

## Putting It Into Practice: Day-by-Day Execution

You now know WHAT to create in each of the 10 sections. This section shows you WHEN and HOW to execute, breaking down the work into manageable daily chunks.

**Total Time Investment**: 2-4 days for comprehensive requirements, 1-2 days for SpecKit processing

---

### Week 1: The Requirements Conversation

Set aside 2-4 days for this. Don't rush it.

#### Day 1-2: Problem Exploration (4-8 hours total)

1. **Start a conversation with an AI agent** (Claude, ChatGPT, etc.)
   - Share this guide with the agent
   - Say: "I need to create a comprehensive requirements document following the 10-section template"

2. **Describe the problem**
   - What's broken today
   - Who it affects
   - Current workarounds
   - Scale (users, data, frequency)

3. **Let the agent ask clarifying questions**
   - The agent will ask 50+ questions
   - Answer with specifics and numbers
   - Examples: "How many concurrent users?" → "20 agents running simultaneously"

4. **Capture use cases together**
   - Walk through typical workflows
   - Describe edge cases
   - Define success criteria
   - Get 10+ scenarios documented

**Output**: Draft use cases and problem understanding

#### Day 3-4: Technical Specification (6-10 hours total)

1. **Agent proposes technical solutions**
   - Complete data model (if applicable)
   - Example queries/workflows
   - Technology choices

2. **You validate and adjust**
   - "Yes, that's right" or "No, we need X instead"
   - Add missing pieces
   - Challenge assumptions

3. **Define performance targets**
   - Agent: "How fast does this need to be?"
   - You: "Search results in under 1 second"
   - Get numbers for everything

4. **Break into phases**
   - Agent proposes MVP first, enhancements later
   - You adjust priorities
   - Define deliverables for each phase

**Output**: Complete technical specification with all 10 sections

#### Day 5: Assembly and Validation (2-4 hours)

1. **Agent assembles everything into one document**
   - All 10 sections
   - Consistent formatting
   - No contradictions

2. **You review using the checklist** (see Quality Assurance section)
   - Check completeness
   - Verify numbers are specific
   - Ensure nothing is vague

3. **Save the document**
   - Save as `work/{module-name}/05-COMPREHENSIVE-SPEC.md`
   - This is your Comprehensive Source (input to SpecKit)

**Output**: 800-1500 line Comprehensive Source document

---

### Week 2: Refinement and Validation

**Now** you refine and validate your Comprehensive Source. This phase follows the official workflow (see [workflow.md](workflow.md) for complete details).

#### Phase 4: Quality Refinement (WO-4, 3-4 hours)

1. **Compare to case study benchmark**
   - Review Project Tracking SQLite example
   - Check abstraction level
   - Identify what to remove

2. **Refine the comprehensive spec**
   - Remove implementation details (SQL DDL, test code)
   - Focus on requirements and acceptance criteria
   - Compress from 800-1500 lines to 500-700 lines
   - Maintain all critical requirements

3. **Save refined spec**
   - `work/{module-name}/10-FINAL-SPEC.md`
   - This is your final PRD

**Output**: 10-FINAL-SPEC.md (500-700 lines, requirements-focused)

#### Phase 5: Validation (WO-5, 3-4 hours)

1. **Run validation checklist**
   - Completeness validation (all requirements present?)
   - Quality comparison (matches case study level?)
   - MVP scope verification (no scope creep?)
   - Integration point verification (all interfaces defined?)

2. **Make GO/NO-GO decision**
   - GO: All validations pass, ready for /plan
   - NO-GO: Address gaps, fix blockers, re-validate

3. **Save readiness report**
   - `work/{module-name}/11-IMPLEMENTATION-READINESS.md`
   - Documents GO/NO-GO with evidence

**Output**: GO/NO-GO decision with validation evidence

#### Using SpecKit Commands (After GO decision)

1. Run `/plan` on 10-FINAL-SPEC.md
   - Creates technical implementation plan
   - Defines architecture and components

2. Run `/tasks` on the plan
   - Creates actionable task list with dependencies

3. Run `/implement` on tasks
   - Executes tasks to build working system

**Output**: Ready to implement or already implementing

---

## Quality Assurance: Validation and Gates

Before moving to SpecKit processing, validate your comprehensive document against these criteria.

---

### Quick Validation Checklist

Before considering your requirements document "ready for SpecKit", check these boxes:

#### Content Completeness

- [ ] Problem statement with numbers (not just "it's slow")
- [ ] 10+ use cases with scale and success criteria
- [ ] Complete data model with exact schema (if applicable)
- [ ] 3-5 example workflows with actual commands
- [ ] Performance targets with numbers (<Xms, Y concurrent users)
- [ ] 3-7 implementation phases with deliverables
- [ ] 20+ edge cases
- [ ] Technology choices with rationale
- [ ] Out of scope list
- [ ] Testing strategy

#### Quality Checks

- [ ] No vague words ("fast", "scalable", "robust") without numbers
- [ ] Every requirement is testable (you can prove it works)
- [ ] No contradictions between sections
- [ ] No [NEEDS CLARIFICATION] markers
- [ ] Specific, not generic ("Save to SQLite" not just "Save data")

#### Length Check

- [ ] Simple feature: 200-300 lines minimum
- [ ] Medium feature: 400-600 lines minimum
- [ ] Complex feature: 800-1000+ lines minimum

**If your document is under 200 lines, you haven't gathered enough requirements.**

### Quality Gates from the 5-Phase Pipeline

#### Gate 1: Information Gathering Complete
**Before proceeding to Spec Creation**:
- [ ] All documentation indexed
- [ ] Interrelationships mapped
- [ ] Gaps identified and assessed
- [ ] High-impact gaps have resolution plan

#### Gate 2: Comprehensive Spec Complete
**Before proceeding to SpecKit Processing**:
- [ ] 500-1000 lines achieved
- [ ] All 10 template sections complete
- [ ] Validation checklist 100%
- [ ] Module owner reviewed

#### Gate 3: SpecKit Processing Complete
**Before proceeding to Validation**:
- [ ] SpecKit output reviewed
- [ ] All details preserved
- [ ] Integration points clear
- [ ] No [NEEDS CLARIFICATION] markers

#### Gate 4: Validation Complete
**Before proceeding to Implementation**:
- [ ] Integration points validated
- [ ] Gaps resolved
- [ ] Implementation readiness confirmed
- [ ] Module owner sign-off

---

## Common Pitfalls and How to Avoid Them

Learn from these 5 common mistakes to save time and create better specifications.

---

### ❌ Mistake 1: Starting with `/specify` Too Early

**Don't do this:**

```text
Day 1: Run /specify with "project tracking migration"
Result: Weak 126-line spec with gaps
```

**Do this instead:**

```text
Day 1-4: Gather comprehensive requirements (500-1000 lines)
Day 5: NOW run /specify with that comprehensive doc as input
Result: Strong 576-line implementation-ready spec
```

---

### ❌ Mistake 2: Vague Performance Targets

**Don't write:**

- "System should be fast"
- "Should handle many users"
- "Should scale well"

**Write instead:**

- "Queries complete in <100ms"
- "Support 20 concurrent agents"
- "Handle 50,000 records without degradation"

---

### ❌ Mistake 3: Skipping Use Cases

**Don't write:**

- "System needs to track projects"

**Write instead:**

```text
UC1: Morning Routine
User wakes up, opens dashboard, sees:
- 12 projects with health indicators (green/yellow/red)
- Recent activity stream (last 20 activities)
- What needs attention today
Success: Loads in <5 seconds, accurate status
```

---

### ❌ Mistake 4: Incomplete Data Model

**Don't write:**

- "We need a database to store projects"

**Write instead:**

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    display_name TEXT,
    vision TEXT,
    current_focus TEXT,
    status TEXT DEFAULT 'active',
    health TEXT DEFAULT 'green',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_status ON projects(status);
```

---

### ❌ Mistake 5: No Edge Cases

**Don't just document happy path:**

- "User creates project successfully"

**Also document:**

- "What happens when 50 users create projects simultaneously?"
- "What happens when project name has emoji?"
- "What happens when database is locked?"
- "What happens during migration?"

---

## Advanced Techniques

Once you're comfortable with the basic process, these advanced techniques help with complex modules.

---

### Gap Identification Template

When you encounter missing information during requirements gathering, document it systematically:

```markdown
### Gap: [Brief Description]
**Type**: Missing requirement / Unclear integration / Assumption
**Impact**: High / Medium / Low
**Details**: What we don't know
**Blocking**: What this prevents us from specifying
**Resolution needed**: What we need to clarify
```

**Critical**: This structured format helps track and resolve gaps before they block implementation.

### Module Execution Order Rationale

When working on multiple modules, follow this recommended sequence:

**1. AI Module** (Most complex, most dependencies)
- **Reason**: Other modules depend on AI capabilities
- **Learn from**: Complex data model, LLM integration
- **Validate**: Can we specify AI features clearly?

**2. Backend Module** (Foundation for others)
- **Reason**: Frontend and Publishing depend on backend
- **Learn from**: API design, data persistence
- **Validate**: Do integration points with AI work?

**3. Frontend Module** (Depends on AI + Backend)
- **Reason**: Needs both AI and Backend specs complete
- **Learn from**: UI workflows, state management
- **Validate**: Can we connect all the pieces?

**4. Publishing Module** (Depends on all others)
- **Reason**: Uses AI, Backend, and displays via Frontend
- **Learn from**: Multi-module integration
- **Validate**: Does the full system work together?

**Why This Sequence?**
- **Sequential advantages**: Learn from each module, refine template as we go, identify cross-module issues early
- **Parallel potential**: AI and Backend can start together, Frontend and Publishing wait for dependencies

For complete workflow details, see [workflow.md](workflow.md).

### Real Example: Reference Implementation

Want to see a real example? Look at the agents project SQLite migration:

**What it includes:**

- 967 lines total
- 10 detailed use cases
- Complete SQLite schema (10 tables, exact DDL)
- 4 example SQL workflows
- 7 implementation phases
- Performance targets: "<10ms queries", "20+ concurrent agents"
- 40+ edge cases
- Testing strategy with unit/integration/load tests

This became the input to SpecKit and produced a 576-line implementation-ready spec that the team executed successfully.

---

## FAQ

**Q: Can't I just run `/specify` and let it create everything?**

A: No. SpecKit needs comprehensive input. Without it, you get generic 126-line specs with gaps.

**Q: 2-4 days seems like a lot. Can we go faster?**

A: You can, but you'll pay for it later with multiple clarification rounds and implementation delays. The agents project proved that investing upfront saves time overall.

**Q: What if we don't have all 10 sections?**

A: Different features need different levels of detail. But if you're missing sections, ask why. Out of scope? Fine, document it. No data model? Maybe you need one. No edge cases? You're not thinking hard enough.

**Q: How do we know when we're done gathering requirements?**

A: Use the checklist. If all boxes are checked and your document is 500+ lines, you're ready.

**Q: What if requirements change during implementation?**

A: Update the comprehensive document first, then update the spec. The comprehensive doc is your source of truth.

---

## Next Steps

**Ready to start?**
1. Review [quickstart.md](quickstart.md) for overview and navigation
2. Follow [workflow.md](workflow.md) for official work order sequence (WO-1 through WO-5)
3. Use [comprehensive-template.md](../templates/comprehensive-template.md) as your structure

**Need supporting materials?**
- [prd-generation-rules.md](../reference/prd-generation-rules.md) - Rules for creating quality PRDs
- [terminology.md](../reference/terminology.md) - Official terms and definitions

---

**Document Status**: Consolidated from spec-kit-guide.md and STRATEGY.md on 2025-10-09
