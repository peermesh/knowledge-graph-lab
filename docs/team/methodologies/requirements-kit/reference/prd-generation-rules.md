# PRD Generation Rules

**Purpose**: Complete instruction manual for agents to transform raw content into properly formatted PRDs that SpecKit can process effectively.

**For**: AI agents processing large amounts of source material
**Output**: Well-structured PRD following `comprehensive-template.md`
**Tuning**: Edit this file to refine PRD generation - changes here propagate to all generated PRDs

---

## Core Principle

**Your job**: Transform scattered, incomplete source material into a complete, well-structured PRD that SpecKit can process without gaps or `[NEEDS CLARIFICATION]` markers.

**Success criteria**: The PRD you generate should require minimal human editing before feeding to SpecKit.

---

## Input Processing

### What You'll Receive

You will receive:
- Multiple documentation files (design docs, notes, conversation summaries)
- Possibly contradictory information
- Incomplete details
- Various formats (markdown, prose, bullet points, diagrams)
- Information at different levels of abstraction

### Your First Pass: Understanding

**Before writing anything**:

1. **Read all source material completely**
2. **Identify the core feature/module** being described
3. **Extract key concepts**: What problem is being solved? For whom?
4. **Note gaps**: What's missing or unclear?
5. **Identify conflicts**: Where do sources contradict each other?

**Output internal notes** (not in PRD):
```markdown
## Understanding Phase Notes
- Core feature: [Brief description]
- Primary users: [Who uses this]
- Key problems solved: [List]
- Gaps identified: [What's missing]
- Conflicts found: [Contradictions]
- Assumptions needed: [What I'll need to assume]
```

---

## PRD Structure Rules

### Section 1: Problem Statement (50-100 lines)

**Purpose**: Establish context - what problem we're solving and why it matters.

#### Extraction Rules:

**From source material, extract**:
- Current pain points (look for: "problem", "issue", "challenge", "limitation")
- Who is affected (look for: "user", "team", "developer", "admin")
- Scale expectations (look for: numbers, "concurrent", "volume", "size")
- Goals and outcomes (look for: "goal", "objective", "success", "improve")

#### Generation Rules:

**Current Situation** (15-30 lines):
- Start with: "Currently, [describe existing state]"
- Include specific pain points with examples
- Quantify where possible (time wasted, errors encountered)
- If source lacks quantification, state: "[NEEDS QUANTIFICATION: specific metric needed]"

**Who is Affected** (10-20 lines):
- List primary user types
- Describe their environment and constraints
- Include scale expectations (how many users, requests, data volume)
- If source lacks scale info: "[NEEDS SCALE: user count/request volume needed]"

**Goals** (15-30 lines):
- State what success looks like
- Include measurable outcomes (time saved, capacity increased, errors reduced)
- Link outcomes to user pain points
- Each goal must be measurable or marked "[NEEDS METRIC: how to measure this goal]"

#### Quality Checks:

- [ ] Problem is specific (not generic like "improve user experience")
- [ ] At least 3 concrete pain points identified
- [ ] Scale expectations quantified (N users, X requests/day, Y GB data)
- [ ] Every goal has a measurable outcome

#### Module-Specific Guidance:

**For AI modules**: Focus on knowledge needs, decision support, data extraction challenges
**For Backend modules**: Focus on data persistence, reliability, API requirements
**For Frontend modules**: Focus on user tasks, information access, interaction challenges
**For Publishing modules**: Focus on content distribution, personalization needs

---

### Section 2: User Stories (5-10 stories, 3-5 lines each)

**Purpose**: Show how the module will be used in practice.

#### Extraction Rules:

**From source material, identify**:
- User goals (look for: "user needs to", "must be able to", "wants to")
- Current workflows (look for: "currently", "today", "existing process")
- Desired workflows (look for: "should", "will", "future state")
- Success criteria (look for: "when", "if successful", "validates")

#### Generation Rules:

**Format (STRICT)**:
```markdown
**US-[N]: [Short Title]**

As a [specific user type],
I need [specific capability],
So that [measurable benefit].

**Acceptance**: [Quantified success criteria - must include numbers, times, or counts]
```

**Mandatory elements per story**:
- **User type**: Specific role (not "user" - be specific: "developer managing 10+ projects", "API consumer with rate limits")
- **Capability**: What they need to do (be concrete, not abstract)
- **Benefit**: Why this matters (must tie to pain point from Section 1)
- **Acceptance**: How we verify success (MUST be quantified)

#### Quality Checks:

- [ ] 5-10 distinct user stories (not variations of same story)
- [ ] Each has "As a/I need/So that" format
- [ ] Each has quantified acceptance criteria
- [ ] Each acceptance includes numbers (< 5 seconds, 100% accuracy, 20+ concurrent, etc.)
- [ ] Stories cover different user goals (not repetitive)
- [ ] Stories align with pain points from Section 1

#### Forbidden Patterns:

❌ **Vague acceptance**: "Works correctly"
✅ **Quantified acceptance**: "Returns results in < 1 second for 10,000 records"

❌ **Generic user**: "As a user"
✅ **Specific user**: "As a developer managing 12+ concurrent projects"

❌ **Vague benefit**: "To improve efficiency"
✅ **Specific benefit**: "So I can recover context in < 5 seconds after context switches"

#### If Source Material Lacks Details:

**When user type unclear**: Mark "[NEEDS USER DEFINITION: who is this for?]"
**When benefit vague**: Use best judgment but mark "[VERIFY BENEFIT: is this the real value?]"
**When acceptance unquantifiable**: Mark "[NEEDS ACCEPTANCE METRIC: how do we measure success?]"

---

### Section 3: Complete Data Model (if applicable)

**Purpose**: Define exactly what data the module stores and how it's structured.

#### Extraction Rules:

**From source material, look for**:
- Entity names (nouns that persist: "user", "document", "session")
- Relationships ("has many", "belongs to", "references")
- Fields mentioned ("email", "timestamp", "status")
- Constraints ("unique", "required", "indexed")

#### Generation Rules:

**For each entity, provide**:

```markdown
### Entity: [EntityName]

**Purpose**: [What this entity represents]

**Fields**:
| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| id | UUID | Primary key, not null | Unique identifier |
| [field] | [type] | [constraints] | [purpose] |
| created_at | Timestamp | Not null, default NOW() | Creation time |
| updated_at | Timestamp | Not null, default NOW() | Last update time |

**Relationships**:
- [Relationship type] [OtherEntity]: [Description]

**Indexes**:
- [field] (for [query purpose])
- [field1, field2] (composite for [query purpose])
```

**If SQL database**: Provide complete DDL
**If NoSQL**: Provide JSON schema
**If no persistence**: State "No persistent data model - module is stateless"

#### Quality Checks:

- [ ] All entities have complete field lists
- [ ] All fields have types and constraints
- [ ] All relationships defined
- [ ] Indexes identified for performance
- [ ] DDL/schema provided (not just descriptions)

#### If Source Material Lacks Details:

**Missing field types**: Use sensible defaults but mark "[VERIFY TYPE: confirm data type]"
**Missing constraints**: Mark "[NEEDS CONSTRAINTS: specify required, unique, etc.]"
**Unclear relationships**: Mark "[NEEDS RELATIONSHIP: how does this relate to X?]"

---

### Section 4: Acceptance Scenarios (3-5 detailed scenarios)

**Purpose**: Show step-by-step execution of key operations.

#### Extraction Rules:

**From source material, identify**:
- Operational sequences (look for: "step", "then", "after", "when")
- Starting conditions (look for: "given", "with", "having")
- Expected outcomes (look for: "result", "output", "should")
- Error conditions (look for: "if", "error", "fails", "invalid")

#### Generation Rules:

**Format (STRICT - Given/When/Then)**:

```markdown
#### Scenario [N]: [Descriptive Title]

**Given** [specific starting state with actual values]
- [Condition 1 with data]
- [Condition 2 with data]
- [Condition 3 with data]

**When** [specific action with actual parameters]

**Then** [specific expected outcomes with measurable assertions]
- [Assertion 1 with expected value]
- [Assertion 2 with expected behavior]
- [Assertion 3 with measurable result]
```

**Example (GOOD)**:
```markdown
#### Scenario 1: User Authentication with Valid Credentials

**Given** the following user exists in the database:
- Username: "john@example.com"
- Password hash: (bcrypt of "SecurePass123")
- Account status: "active"
- Last login: 2025-10-01 08:00:00 UTC

**When** user submits login request with:
- Username: "john@example.com"
- Password: "SecurePass123"

**Then** system responds with:
- HTTP 200 status code
- JWT token with 24-hour expiration
- Token contains user_id and role claims
- Last login timestamp updated to current time
- Login event logged with IP address
```

#### Quality Checks:

- [ ] 3-5 critical scenarios documented
- [ ] Each uses Given/When/Then format
- [ ] Given conditions are specific with actual data
- [ ] When actions include actual parameters
- [ ] Then assertions are measurable and specific
- [ ] Scenarios cover happy path AND error conditions

#### Forbidden Patterns:

❌ **Vague Given**: "Given user exists"
✅ **Specific Given**: "Given user with email 'john@example.com' and active status exists"

❌ **Vague Then**: "Then system succeeds"
✅ **Specific Then**: "Then system returns HTTP 200 with JWT token valid for 24 hours"

---

### Section 5: Performance Targets (quantified)

**Purpose**: Define measurable performance requirements.

#### Extraction Rules:

**From source material, look for**:
- Response times (look for: "fast", "quick", "milliseconds", "seconds")
- Throughput (look for: "requests", "concurrent", "per second", "volume")
- Scalability (look for: "users", "records", "size", "scale")
- Resource constraints (look for: "memory", "disk", "CPU")

#### Generation Rules:

**All targets MUST be quantified with numbers and units**

**Categories**:

1. **Response Times**:
   - API endpoint latency: < [N]ms for [percentile]
   - Query execution: < [N]ms for [data volume]
   - Page load: < [N]ms for [typical use]

2. **Throughput**:
   - Requests per second: [N] requests/sec
   - Concurrent operations: [N]+ concurrent users/agents
   - Data processing rate: [N] records/second

3. **Scalability**:
   - Maximum records: Up to [N] records
   - Maximum users: Up to [N] concurrent users
   - Data volume: Up to [N] GB

4. **Resource Constraints**:
   - Memory usage: < [N] MB/GB
   - Disk space: < [N] MB/GB
   - CPU usage: < [N]% under load

#### Quality Checks:

- [ ] Every target has a number
- [ ] Every number has a unit (ms, requests/sec, GB, etc.)
- [ ] Targets cover response times, throughput, scalability
- [ ] Targets are realistic for the use case
- [ ] No vague terms ("fast", "scalable") without numbers

#### If Source Material Lacks Numbers:

**Make educated guesses based on**:
- Similar systems
- Reasonable user expectations
- Industry standards

**Mark assumptions**: "[ASSUMPTION: based on typical [similar system] performance, verify with stakeholders]"

**Examples of defaults**:
- Web API: < 200ms for 95th percentile
- Search: < 1s for 10,000 records
- Dashboard load: < 500ms
- Concurrent users: 10+ for small systems, 100+ for medium, 1000+ for large

---

### Section 6: Implementation Phases (3-7 phases)

**Purpose**: Break implementation into manageable, sequential phases.

#### Extraction Rules:

**From source material, identify**:
- Natural breakpoints (look for: "first", "then", "after", "phase")
- Dependencies (look for: "depends on", "requires", "before")
- MVP mentions (look for: "minimum", "essential", "must have")
- Optional features (look for: "nice to have", "future", "later")

#### Generation Rules:

**For each phase**:

```markdown
**Phase [N]: [Phase Name]**

**Goal**: [What this phase achieves]

**Deliverables**:
- [Specific output 1]
- [Specific output 2]
- [Specific output 3]

**Success Criteria**:
- [How to verify phase completion]
- [What tests must pass]

**Dependencies**:
- [What must be complete before starting]
- [External dependencies]
```

**DO NOT include time estimates** (removed per user decision)

#### Quality Checks:

- [ ] 3-7 phases (not too granular, not too coarse)
- [ ] Each phase has clear deliverables
- [ ] Each phase has success criteria
- [ ] Dependencies between phases identified
- [ ] MVP clearly identified (which phases are essential)
- [ ] Phases are sequential and logical

#### If Source Material Lacks Phase Info:

**Default breakdown**:
1. Phase 1: Core data model and basic CRUD
2. Phase 2: Primary workflows and business logic
3. Phase 3: Integration points and APIs
4. Phase 4: Testing and error handling
5. Phase 5: Performance optimization
6. Phase 6: Documentation and deployment

Mark: "[VERIFY PHASES: confirm this breakdown matches project needs]"

---

### Section 7: Edge Cases (10-20+ scenarios)

**Purpose**: Document failure modes, boundary conditions, and unusual situations.

#### Extraction Rules:

**From source material, look for**:
- Error mentions (look for: "error", "fails", "invalid", "exception")
- Limits (look for: "maximum", "minimum", "too many", "empty")
- Concurrency (look for: "concurrent", "simultaneous", "parallel")
- Integration issues (look for: "service", "API", "external", "third-party")

#### Generation Rules:

**Categories to cover**:

1. **Failure Scenarios**: External services fail, network errors, data corruption
2. **Boundary Conditions**: Empty data, maximum volumes, malformed inputs
3. **Concurrent Access**: Multiple users/agents, race conditions, locks
4. **Integration Issues**: Upstream unavailable, rate limits, auth failures

**Format per edge case**:
```markdown
- **[Brief description]**: [Expected system behavior - specific, not just "handle error"]
```

**Example (GOOD)**:
```markdown
- **Database connection lost mid-transaction**: Transaction rolls back automatically, user sees "Connection lost, please retry", operation can be safely retried without duplicates
- **Concurrent write to same record**: Last write wins, version number incremented, audit log records both attempts with timestamps
```

#### Quality Checks:

- [ ] 10-20+ edge cases documented
- [ ] Covers failures, boundaries, concurrency, integration
- [ ] Each specifies expected behavior (not just "handle error")
- [ ] Critical edge cases have mitigation strategies

#### If Source Material Lacks Edge Cases:

**Generate standard edge cases for the module type**:

**All modules**:
- Empty/missing input data
- Malformed input data
- Maximum data volume exceeded
- Concurrent access conflicts

**API modules**:
- Rate limits exceeded
- Authentication token expired
- Upstream service unavailable
- Invalid request parameters

**Data modules**:
- Database connection lost
- Transaction deadlock
- Duplicate key violation
- Schema migration failure

Mark: "[STANDARD EDGE CASES: verify these apply to this module]"

---

### Section 8: Technology Constraints

**Purpose**: Document technology choices and requirements (WHAT not WHY).

#### Extraction Rules:

**From source material, identify**:
- Technologies mentioned (look for: specific tools, frameworks, languages)
- Requirements (look for: "must use", "requires", "depends on")
- Constraints (look for: "cannot", "must not", "limited to")
- Versions (look for: version numbers, "latest", "minimum")

#### Generation Rules:

**Focus on WHAT is required, not WHY**:

```markdown
**Required Technologies**:
- [Technology 1]: [Version requirement]
- [Technology 2]: [Version requirement]

**External Dependencies**:
- [Service/Library 1]: [Version/availability requirement]
- [Service/Library 2]: [Version/availability requirement]

**Constraints**:
- [Constraint 1: what's required or forbidden]
- [Constraint 2: what's required or forbidden]

**Configuration**:
- [Environment variables needed]
- [Required secrets/credentials]
- [Runtime modes]
```

**Do NOT include**:
- ❌ Rationale ("because it's fast")
- ❌ Alternatives considered ("chose X over Y")
- ❌ Architectural decisions ("we decided to use microservices")

**DO include**:
- ✅ What technology is required
- ✅ Version constraints
- ✅ Configuration requirements
- ✅ Hard dependencies

#### Quality Checks:

- [ ] All required technologies listed
- [ ] Version constraints specified
- [ ] External dependencies identified
- [ ] Configuration needs documented
- [ ] No "WHY" rationale (that's for ADRs, not PRDs)

---

### Section 9: Testing Strategy

**Purpose**: Define how the module will be validated.

#### Extraction Rules:

**From source material, identify**:
- Test types mentioned (look for: "unit", "integration", "load", "e2e")
- Coverage expectations (look for: "coverage", "percent", "must test")
- Critical paths (look for: "critical", "must test", "key scenarios")

#### Generation Rules:

**For each test type**:

```markdown
**[Test Type]**:
- What to test: [Specific components/functions]
- Coverage target: [Percentage or criteria]
- Key scenarios: [Critical paths to verify]
```

**Typical structure**:

1. **Unit Tests**: Individual functions/components
2. **Integration Tests**: System interactions
3. **Load/Performance Tests**: Validate performance targets from Section 5
4. **Acceptance Tests**: Validate user stories from Section 2

#### Quality Checks:

- [ ] All test types defined (unit, integration, load minimum)
- [ ] Testing validates performance targets
- [ ] Testing validates user story acceptance criteria
- [ ] Critical paths identified

---

### Section 10: Integration Points

**Purpose**: Document how this module connects to other modules.

#### Extraction Rules:

**From source material, identify**:
- Module dependencies (look for: "needs", "depends on", "uses")
- Provided interfaces (look for: "provides", "exposes", "offers")
- Data flows (look for: "sends", "receives", "publishes", "consumes")

#### Generation Rules:

```markdown
## Dependencies (What we need from other modules)

**From [Module Name]**:
- [Interface/API]: [What we use it for]
- [Data format]: [What data we consume]
- [Events/hooks]: [What we listen for]

## Provides (What we offer to other modules)

**To [Module Name]**:
- [Interface/API]: [What we expose]
- [Data format]: [What data we produce]
- [Events/hooks]: [What we publish]

## Data Contracts

**Input data format**:
```json
{example}
```

**Output data format**:
```json
{example}
```
```

#### Quality Checks:

- [ ] All dependencies on other modules documented
- [ ] All interfaces this module provides documented
- [ ] Data formats specified (JSON schemas, API contracts)
- [ ] Integration points clearly defined

#### If Source Material Lacks Integration Info:

Mark each unclear integration: "[NEEDS INTEGRATION SPEC: define interface with [Module Name]]"

---

### Section 11: Success Criteria (NEW)

**Purpose**: Define overall project success metrics.

#### Extraction Rules:

**From source material, identify**:
- Success metrics (look for: "success", "complete when", "done when")
- Business value (look for: "value", "benefit", "saves", "improves")
- Completion criteria (look for: "ready", "production-ready", "shippable")

#### Generation Rules:

```markdown
## Overall Success Metrics

**User-facing success**:
- [Metric 1 with target]: [How measured]
- [Metric 2 with target]: [How measured]

**Technical success**:
- [Metric 1 with target]: [How measured]
- [Metric 2 with target]: [How measured]

**Business success**:
- [Metric 1 with target]: [How measured]
- [Metric 2 with target]: [How measured]

## Completion Criteria

The module is complete when:
- [ ] All user stories validated
- [ ] All acceptance scenarios pass
- [ ] Performance targets met
- [ ] Integration points validated
- [ ] [Module-specific criterion]
```

#### Quality Checks:

- [ ] Success metrics are measurable
- [ ] Success metrics tie back to problem statement (Section 1)
- [ ] Completion criteria are clear
- [ ] Both technical and user-facing success defined

---

## Cross-Section Rules

### Consistency Validation

**After generating all sections, verify**:

1. **User stories (Section 2) align with problem statement (Section 1)**
   - Each user story addresses a pain point from Section 1

2. **Acceptance scenarios (Section 4) validate user stories (Section 2)**
   - At least one scenario per critical user story

3. **Performance targets (Section 5) appear in acceptance scenarios (Section 4)**
   - Each performance target tested in at least one scenario

4. **Edge cases (Section 7) cover scenarios from Section 4**
   - Error paths from scenarios become edge cases

5. **Testing strategy (Section 9) covers all acceptance criteria**
   - Tests validate user stories and scenarios

6. **Integration points (Section 10) reference data model (Section 3)**
   - Entities in data model flow through integration points

7. **Success criteria (Section 11) tie to problem statement (Section 1)**
   - Success metrics measure goal achievement from Section 1

### Gap Identification

**If any section cannot be completed due to missing source information**:

**Mark with**:
```markdown
[NEEDS CLARIFICATION: Specific question about what's needed]
```

**Common gaps**:
- User types not defined → "[NEEDS USER DEFINITION: who are the primary users?]"
- Scale unknown → "[NEEDS SCALE: how many users/requests/records?]"
- Performance unknown → "[NEEDS PERFORMANCE TARGET: what's acceptable response time?]"
- Integration undefined → "[NEEDS INTEGRATION SPEC: how does this connect to [Module]?]"

### Conflict Resolution

**When source materials contradict each other**:

1. **Prioritize** most recent information
2. **Note the conflict**: "[CONFLICT DETECTED: Source A says X, Source B says Y - using Y (more recent)]"
3. **If unable to resolve**: "[NEEDS RESOLUTION: Source A says X, Source B says Y - which is correct?]"

---

## Quality Assurance Checklist

Before considering PRD complete, verify:

### Completeness

- [ ] All 11 sections completed
- [ ] No section is empty or just "[TODO]"
- [ ] Target length achieved (500-1000 lines for complex modules)
- [ ] All [NEEDS CLARIFICATION] markers have specific questions

### Quantification

- [ ] All user story acceptance criteria have numbers
- [ ] All performance targets have numbers and units
- [ ] All scale expectations quantified
- [ ] No vague terms without numbers

### Format

- [ ] User stories follow "As a/I need/So that" format
- [ ] Acceptance scenarios follow "Given/When/Then" format
- [ ] Data model has complete tables/entities with types
- [ ] Edge cases specify expected behaviors
- [ ] Integration points clearly defined

### Consistency

- [ ] User stories address problems from Section 1
- [ ] Scenarios validate user stories
- [ ] Performance targets tested in scenarios
- [ ] Testing covers acceptance criteria
- [ ] Success criteria measure problem resolution

### SpecKit-Readiness

- [ ] No implementation details (HOW) - only requirements (WHAT)
- [ ] All requirements testable
- [ ] All acceptance criteria measurable
- [ ] Data model implementation-ready
- [ ] No ambiguous language

---

## Output Format

**Your final output should be**:

```markdown
# [Module Name] - Product Requirements Document (PRD)

**Module**: [Name]
**Version**: 1.0
**Created**: [Date]
**Owner**: [Team/Person]

---

[Section 1: Problem Statement]
[Section 2: User Stories]
[Section 3: Complete Data Model]
[Section 4: Acceptance Scenarios]
[Section 5: Performance Targets]
[Section 6: Implementation Phases]
[Section 7: Edge Cases]
[Section 8: Technology Constraints]
[Section 9: Testing Strategy]
[Section 10: Integration Points]
[Section 11: Success Criteria]

---

## Validation Checklist

[Include the quality assurance checklist with items checked]

---

## Open Questions

[List any [NEEDS CLARIFICATION] items here for easy reference]
```

---

## CLARIFICATION: When to Use `/specify` Command

**CRITICAL DISTINCTION**: The `/specify` command and "SpecKit processing" are different concepts.

### Use `/specify` When:
- ✅ Starting from scratch with a feature description
- ✅ No existing comprehensive spec (before WO-3)
- ✅ Want SpecKit to generate initial structure
- ✅ Alternative to manually filling 10-section template

### DO NOT Use `/specify` When:
- ❌ Comprehensive spec already exists (like `05-COMPREHENSIVE-SPEC.md`)
- ❌ Spec just needs quality refinement (WO-4)
- ❌ Next step is implementation planning (use `/plan` command instead)

### For WO-4 "SpecKit Processing and Refinement":
**This refers to**: Manual quality refinement by comparing comprehensive spec to case study benchmark
**This does NOT mean**: Running `/specify` command again

**Correct WO-4 Process**:
1. Read comprehensive spec (from WO-3)
2. Compare section-by-section using quality guidelines
3. Identify over-specifications (implementation details, redundancy)
4. Refine manually to achieve production quality
5. Create final spec (500-700 lines)

**Next Step After Final Spec**: Use `/plan` command for implementation planning

**Full decision guide**: See [when-to-use-specify-guide.md](../../checklists/when-to-use-specify-guide.md) for complete decision tree and examples

---

## Critical: Avoiding Over-Specification

**Problem**: Following template section ranges literally produces 1843-line documents instead of 600-800 target.

**Your job**: Provide the RIGHT level of detail - enough for SpecKit, not implementation plans.

### Length Discipline

**Target lengths by section**:
- Section 1 (Problem Statement): 50-100 lines ✓
- Section 2 (User Stories): 5-7 stories × 7 lines = 35-50 lines
- Section 3 (Data Model): Complete DDL but concise (100-200 lines)
- Section 4 (Acceptance Scenarios): 3-5 scenarios × 15-20 lines = 45-100 lines
- Section 5 (Performance Targets): 20-30 targets, 1-2 lines each = 20-60 lines
- Section 6 (Implementation Phases): 3-5 phases × 10-15 lines = 30-75 lines
- Section 7 (Edge Cases): 10-15 cases × 2-3 lines = 30-45 lines
- Section 8 (Technology Constraints): 30-50 lines
- Section 9 (Testing Strategy): 30-50 lines
- Section 10 (Integration Points): 40-60 lines
- Section 11 (Success Criteria): 30-50 lines

**Total target: 600-800 lines**

**If approaching 1000+ lines**: You're over-specifying. Stop and cut.

### Acceptance Scenarios: 15-20 Lines MAX

**The Problem**: Agents produce 60-line scenarios with complete SQL setup and API implementation details.

**The Solution**: Focus on WHAT happens, not HOW it's implemented.

❌ **TOO MUCH** (60 lines - implementation details):
```markdown
#### Scenario 1: User Subscribes to Weekly Digest

**Given**:
- A user with user_id `550e8400-e29b-41d4-a716-446655440000` exists in the database
- User table contains: email `creator@example.com`, first_name `Jane`, last_name `Smith`, created_at `2025-10-01`
- publication_request table has no existing record for this user
- Database connection pool has 3 available connections
- SES API credentials are configured in environment: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
- interest_tags array: `['creator economy', 'open source', 'web3']`
- send_interval enum value: `'weekly'`
- preferred_send_time: `'monday_09:00'`
- timezone: `'America/Los_Angeles'`

**When** user submits POST request to `/api/publication-requests`:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "interest_tags": ["creator economy", "open source", "web3"],
  "send_interval": "weekly",
  "preferred_send_time": "monday_09:00",
  "timezone": "America/Los_Angeles"
}
```

**Then** system performs the following operations:
1. Validates user_id exists in users table via SELECT query
2. Executes INSERT statement:
```sql
INSERT INTO publication_requests (
  request_id, user_id, interest_tags, send_interval,
  preferred_send_time, timezone, status, created_at
) VALUES (
  gen_random_uuid(),
  '550e8400-e29b-41d4-a716-446655440000',
  ARRAY['creator economy', 'open source', 'web3'],
  'weekly',
  'monday_09:00',
  'America/Los_Angeles',
  'active',
  NOW()
)
```
3. Commits transaction to database
4. Sends confirmation email via SES API call to send_via_ses()
5. Returns HTTP 201 response with Location header
6. Response body includes complete publication_request object
7. Logs event to application log with INFO level
8. Updates metrics counter for new_subscriptions

**Measurement**:
- API response time: < 150ms at 95th percentile
- Database insert time: < 50ms
- Email delivery time: < 30 seconds
- Zero duplicate subscription entries
```

✅ **JUST RIGHT** (15 lines - requirements only):
```markdown
#### Scenario 1: User Subscribes to Weekly Digest

**Given** user with email `creator@example.com` authenticated and has no active subscriptions

**When** user submits subscription request:
- Interest tags: `['creator economy', 'open source']`
- Send interval: `weekly`
- Preferred time: `Monday 9 AM Pacific`

**Then** system responds with:
- HTTP 201 Created
- Subscription confirmation email sent within 30 seconds
- Subscription record created with status `active`
- User receives first digest on next scheduled Monday

**Measurement**: 95% of requests complete in < 200ms, zero duplicate subscriptions
```

**Key differences**:
- ✅ WHAT happens: User subscribes, gets confirmation, first digest scheduled
- ❌ HOW it happens: SQL statements, API implementation, logging details
- ✅ Measurable outcomes: Response time, delivery time, duplicate prevention
- ❌ Implementation details: Database connection pools, transaction commits

**Rule**: If you're writing SQL, API calls, or implementation steps in acceptance scenarios, STOP. Those belong in `/plan` output, not PRDs.

### Edge Cases: Statements Not Solutions

**The Problem**: Agents write 15-line implementation plans for each edge case.

**The Solution**: State the situation and expected behavior in 2-3 lines. Don't solve the problem.

❌ **TOO MUCH** (15 lines per case - implementation solution):
```markdown
**EC-1: SES API Returns Transient Error**

**Situation**: When send_via_ses() calls the Amazon SES API, the API returns HTTP 503 Service Unavailable due to temporary AWS service degradation.

**Behavior**:
1. Catch boto3.exceptions.ClientError exception in try/except block
2. Log ERROR level message with full stack trace and request_id
3. Extract error code from exception metadata
4. If error code is '503' or 'ServiceUnavailable':
   - Set retry flag in Celery task queue
   - Use exponential backoff: wait 2^attempt_number seconds
   - Maximum 3 retry attempts
5. After 3 failed retries:
   - Log CRITICAL level message
   - Send PagerDuty alert to on-call engineer
   - Mark email as 'failed' in publication_logs table
   - Queue admin notification email
6. Update prometheus metric: email_send_failures_total
7. Return error response to calling function
```

✅ **JUST RIGHT** (2-3 lines - requirement statement):
```markdown
**EC-1**: SES API timeout → Retry 3x with exponential backoff, alert admin if all attempts fail
**EC-2**: Invalid email in database → Mark as invalid, pause subscription, flag for manual review
**EC-3**: Mailbox full (soft bounce) → Retry after 7 days, treat as hard bounce if second failure
**EC-4**: Rate limit exceeded → Queue for next send window, log warning, don't retry immediately
**EC-5**: User unsubscribed mid-send → Cancel send, update status, don't log as failure
```

**Key differences**:
- ✅ WHAT to do: Retry logic, admin alerts, subscription pausing
- ❌ HOW to do it: Exception handling, database queries, metric updates
- ✅ Expected behavior: System response to edge case
- ❌ Implementation: Code structure, function calls, data flows

**Rule**: State "situation → behavior" in 1-2 lines. Leave implementation to engineers and `/plan`.

### Implementation Phases: Milestones Not Plans

**The Problem**: Agents create detailed 6-day task breakdowns with hour estimates.

**The Solution**: High-level milestones with deliverables, not implementation schedules.

❌ **TOO MUCH** (detailed implementation plan with time estimates):
```markdown
**Phase 5: Email Delivery Integration** (6 days, 48 hours total)

**Day 1-2** (16 hours): AWS SES Configuration
- Hour 1-2: Create AWS IAM user with SES permissions
- Hour 3-4: Generate access keys and store in .env file
- Hour 5-6: Configure SES sending domain in AWS console
- Hour 7-8: Verify domain ownership via DNS TXT records
- Hour 9-12: Set up DKIM signing and SPF records
- Hour 13-14: Request production access (move out of sandbox)
- Hour 15-16: Configure boto3 client with credentials

**Day 3** (8 hours): Send Function Implementation
- Hour 1-3: Implement send_via_ses() function with error handling
- Hour 4-5: Add retry logic using tenacity library
- Hour 6-7: Implement email templating with Jinja2
- Hour 8: Write unit tests for send function

**Day 4** (8 hours): Webhook Endpoint
- Hour 1-3: Create Flask endpoint for /webhooks/ses-notifications
- Hour 4-5: Parse SNS notification JSON payload
- Hour 6-7: Update publication_logs table based on bounce/complaint events
- Hour 8: Add endpoint authentication with SNS signature verification

**Day 5** (8 hours): Retry and Queue Management
- Hour 1-3: Implement Celery task for async email sending
- Hour 4-5: Configure retry logic with exponential backoff
- Hour 6-7: Add dead letter queue for failed sends
- Hour 8: Implement admin alert for repeated failures

**Day 6** (8 hours): Integration Testing
- Hour 1-2: Set up test SES account in sandbox mode
- Hour 3-4: Test happy path with real email delivery
- Hour 5-6: Test bounce and complaint handling
- Hour 7-8: Load test with 100 concurrent sends

**Deliverables**:
- send_via_ses() function with error handling
- Webhook endpoint for bounce notifications
- Celery async task queue
- Integration tests passing
- Documentation in docs/email-delivery.md

**Success Criteria**:
- Can send 100 emails within 5 minutes
- Bounces processed within 30 seconds
- Failed sends retry automatically
- Admin alerts trigger on persistent failures
```

✅ **JUST RIGHT** (high-level milestone):
```markdown
**Phase 5: Email Delivery**

**Goal**: Integrate Amazon SES for reliable email delivery with bounce handling

**Deliverables**:
- SES integration with sending function
- Webhook endpoint for delivery status notifications
- Retry logic for failed sends with exponential backoff
- Admin alerts for persistent delivery failures

**Success Criteria**:
- 100+ emails sent within 5 minutes
- Bounce notifications processed within 30 seconds
- Failed sends retry automatically up to 3 times
- Delivery rate > 95% for valid email addresses

**Dependencies**:
- Phase 4 (content generation) must be complete
- AWS SES account with production access
- Domain verification and DKIM configuration
```

**Key differences**:
- ✅ WHAT to deliver: SES integration, webhook, retry logic
- ❌ HOW to build it: Hour-by-hour task breakdown
- ✅ Success criteria: Measurable outcomes
- ❌ Time estimates: Day/hour breakdowns (user decision: "terrible idea")
- ✅ Dependencies: What's needed before starting
- ❌ Implementation steps: Specific technical tasks

**Rule**: Describe the milestone goal, deliverables, and success criteria. Don't plan the implementation. Engineers know how to build; they need to know WHAT to build.

### Testing: Approach Not Test Suite

**The Problem**: Agents write complete test suites with 50+ individual test cases.

**The Solution**: Describe testing approach, coverage targets, and key scenarios. Don't design the tests.

❌ **TOO MUCH** (complete test suite):
```markdown
## Section 9: Testing Strategy

### 9.1 Unit Testing (Coverage target: 90%)

**Test Suite 1: Content Assignment**

**Test 1.1**: test_assign_content_success()
- Setup: Mock article database with 10 articles across 5 tags
- Execute: Call assign_content(user_id="test-user", tags=["tech", "AI"])
- Assert: Returns 3-5 articles, all have matching tags, sorted by relevance
- Expected: AssertionError if < 3 or > 5 articles returned

**Test 1.2**: test_assign_content_no_matches()
- Setup: Mock article database with articles for different tags
- Execute: Call assign_content(user_id="test-user", tags=["nonexistent"])
- Assert: Returns empty list, logs warning message
- Expected: No exception raised, empty response

**Test 1.3**: test_assign_content_invalid_user()
- Setup: Mock user database without test user
- Execute: Call assign_content(user_id="nonexistent", tags=["tech"])
- Assert: Raises UserNotFoundError with appropriate message
- Expected: Exception raised, no database mutation

[... 50 more test cases across 8 test suites ...]

### 9.2 Integration Testing

**Integration Test 1**: test_full_digest_pipeline()
- Setup: Create test user, test subscription, 20 test articles
- Execute: Trigger scheduled task for digest generation
- Assert: Email sent via SES, contains 3-5 articles, unsubscribe link present
- Cleanup: Delete test data, remove sent email from queue

[... 20 more integration test scenarios ...]

### 9.3 Load Testing

**Load Test 1**: test_concurrent_user_processing()
- Setup: Create 1,000 test users with active subscriptions
- Execute: Trigger digest generation for all users simultaneously
- Monitor: Response times, database connection pool, memory usage
- Assert: All users processed within 15 minutes, zero failures

[... complete load testing specifications ...]
```

✅ **JUST RIGHT** (testing approach):
```markdown
## Section 9: Testing Strategy

### Unit Testing
**What to test**: Content assignment logic, email template rendering, scheduling calculations, webhook parsing
**Coverage target**: 85% code coverage minimum
**Key scenarios**:
- Content matches user tags correctly
- Handles missing/invalid data gracefully
- Scheduling respects timezones and user preferences

### Integration Testing
**What to test**: Full digest pipeline (schedule → fetch content → render → send), webhook processing for bounces/complaints
**Coverage target**: All critical user workflows from Section 2
**Key scenarios**:
- End-to-end digest delivery completes successfully
- Bounce notifications update subscription status
- Failed sends trigger retry and alert mechanisms

### Load/Performance Testing
**What to test**: System handles target load from Section 5
**Performance targets to validate**:
- 1,000 users processed within 15 minutes
- 95% of emails delivered within SLA
- Concurrent webhook handling without queue backup
- Database query performance under load

### Acceptance Testing
**What to test**: All acceptance scenarios from Section 4 pass
**Success metrics**:
- All user stories from Section 2 validated
- All edge cases from Section 7 handled correctly
- Performance targets from Section 5 met consistently

### Validation Gates
- [ ] Unit tests: 85%+ coverage, all passing
- [ ] Integration tests: All critical workflows passing
- [ ] Load tests: Performance targets met under sustained load
- [ ] Acceptance tests: All scenarios from Section 4 verified
- [ ] Edge case tests: All cases from Section 7 handled correctly
```

**Key differences**:
- ✅ WHAT to test: Testing categories and coverage areas
- ❌ HOW to test: Individual test implementations
- ✅ Coverage targets: Percentages and validation criteria
- ❌ Test code: Specific test functions and assertions
- ✅ Success metrics: How to validate quality
- ❌ Test suite design: Complete test case specifications

**Rule**: Describe the testing approach, what needs validation, and success criteria. Engineers will design the actual test suite during implementation.

### Summary: The Right Level of Detail

**PRD purpose**: Define WHAT to build, not HOW to build it

**Include**:
- ✅ What problems we're solving
- ✅ What users need to accomplish
- ✅ What data we need to store
- ✅ What behaviors are expected
- ✅ What performance is required
- ✅ What success looks like

**Exclude**:
- ❌ SQL implementation details
- ❌ API implementation code
- ❌ Hour-by-hour task schedules
- ❌ Complete test suites
- ❌ Exception handling code
- ❌ Algorithm implementations

**Remember**: The `/plan` command will take this PRD and create detailed implementation plans. Your job is to provide complete requirements, not implementation solutions.

**Length check**: If your PRD exceeds 800 lines, you're writing implementation details. Stop and remove HOW, keep only WHAT.

---

## Expanding from Starter Template

**Purpose**: Transform a filled starter template (300-500 lines) into a comprehensive PRD (600-800 lines) suitable for SpecKit processing.

**Input**: `templates/simple-template.md` (filled by user)
**Output**: Comprehensive PRD following all rules in this document

### Understanding the Two Templates

**Starter Template** (300-500 lines):
- Quick capture of core feature concept
- Minimal structure (8 sections vs 11)
- User-friendly, less intimidating
- Allows incomplete information
- Good for initial brainstorming

**Comprehensive PRD** (600-800 lines):
- Complete requirements for SpecKit
- Full structure (11 sections)
- All quantification required
- Ready for specification generation
- Good for formal processing

**Your job**: Take starter content and expand it to comprehensive format without over-specifying.

### Section-by-Section Expansion Mapping

#### Starter Section 1: Core Problem → Comprehensive Section 1: Problem Statement

**What to keep**:
- User's problem description exactly as written
- Who is affected (user types)
- Goals and desired outcomes

**What to add**:
- Quantification if missing (mark "[NEEDS QUANTIFICATION: metric]" if can't infer)
- Specific pain points broken out with examples
- Scale expectations (number of users, request volume, data size)
- Structure into subsections: Current Situation / Who is Affected / Goals

**Length**: 50-100 lines (same as starter, just more structured)

**Example**:
```markdown
# Starter input (30 lines, unstructured):
Users want personalized content digests but our system sends everyone the same newsletter.
Marketing team spends 10+ hours weekly manually curating different lists. We need
automation that respects user preferences...

# Comprehensive output (60 lines, structured):
## 1. Problem Statement

### Current Situation
Currently, the content distribution system sends identical newsletters to all 15,000
subscribers, regardless of their interests or preferences. This creates several problems:
- 68% of users report receiving irrelevant content (Q3 2025 survey)
- Open rates declining 3% monthly (now at 22% vs industry average 28%)
- Marketing team spends 10-12 hours weekly manually segmenting lists with poor results
- No data on individual user preferences or content consumption patterns

### Who is Affected
[... continues with quantified impact ...]
```

#### Starter Section 2: User Stories → Comprehensive Section 2: User Stories

**What to keep**:
- User's 3-5 core user stories
- The essential user needs they identified

**What to add**:
- 2-3 additional user stories for edge cases (admin users, error scenarios)
- Strict formatting: "As a/I need/So that" structure
- Quantified acceptance criteria for each story
- Specific user types (not generic "user")

**Length**: 35-50 lines (5-7 stories × 7 lines each)

**Example transformation**:
```markdown
# Starter input (informal):
- Users should be able to set their content preferences
- System should send digests based on those preferences
- Marketing should see engagement metrics

# Comprehensive output (formatted with acceptance):
**US-1: Content Preference Configuration**

As a subscriber with limited reading time,
I need to specify my content interests and preferred delivery schedule,
So that I receive only relevant articles at convenient times.

**Acceptance**: User can select 3-10 interest tags from predefined list,
choose send frequency (daily/weekly/monthly), set preferred delivery time,
and changes take effect within 24 hours.

**US-2: Personalized Digest Delivery**

As a subscriber who selected "AI" and "open source" interests with weekly delivery,
I need to receive curated digests matching my preferences every Monday morning,
So that I stay informed without email overload.

**Acceptance**: 95% of digests delivered within 30 minutes of scheduled time,
contain 3-7 articles matching user's tags, include unsubscribe and preference
update links, delivery rate > 98% for valid emails.

[... 3-5 more stories ...]
```

**What NOT to do**:
- ❌ Don't discard user's original stories - preserve their intent
- ❌ Don't add stories the user didn't imply - expand, don't invent
- ❌ Don't leave acceptance criteria vague - quantify or mark for clarification

#### Starter Section 3: Data → Comprehensive Section 3: Complete Data Model

**What to keep**:
- Entity names user specified
- Basic fields they mentioned
- Relationships they described

**What to add**:
- Complete DDL with all field types
- Constraints (NOT NULL, UNIQUE, etc.)
- Foreign keys and relationships
- Indexes for performance
- Standard fields (id, created_at, updated_at)

**Length**: 100-200 lines (biggest expansion: 3-4x from starter)

**How to infer missing details**:
- **Data types**: From usage context (emails = VARCHAR, counts = INTEGER, etc.)
- **Constraints**: From user stories (unique emails, required fields, etc.)
- **Relationships**: From workflows (user has many subscriptions, etc.)
- **Indexes**: From expected queries (search by user_id, filter by status, etc.)

**Example transformation**:
```markdown
# Starter input (basic entities):
We need to store:
- Users (email, name, timezone)
- Subscriptions (user preferences, tags, frequency)
- Articles (title, content, tags, publish date)

# Comprehensive output (complete DDL):
## 3. Complete Data Model

### Entity: users

**Purpose**: Store subscriber accounts and authentication

**Fields**:
| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| user_id | UUID | Primary key, NOT NULL | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| first_name | VARCHAR(100) | NULL | User first name |
| last_name | VARCHAR(100) | NULL | User last name |
| timezone | VARCHAR(50) | NOT NULL, DEFAULT 'UTC' | User timezone |
| status | ENUM('active','inactive','suspended') | NOT NULL, DEFAULT 'active' | Account status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last modification |

**Relationships**:
- Has many: publication_requests (one user can have multiple subscriptions)

**Indexes**:
- email (for login and lookup queries)
- status (for active user queries)

### Entity: publication_requests

[... complete DDL for each entity ...]

**SQL DDL**:
```sql
CREATE TABLE users (
  user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);

[... DDL for all entities ...]
```
```

**What NOT to do**:
- ❌ Don't guess entities user didn't mention - infer only from their workflows
- ❌ Don't add complex optimization fields unless performance requires it
- ❌ Don't create database implementation (connection pools, migrations) - just schema

**If details are truly unknown**:
- Mark: "[VERIFY TYPE: confirm VARCHAR(255) is sufficient for this field]"
- Mark: "[NEEDS RELATIONSHIP: clarify how articles relate to subscriptions]"

#### Starter Section 4: Workflows → Comprehensive Section 4: Acceptance Scenarios

**What to keep**:
- User's workflow steps exactly as described
- The sequence of operations they outlined

**What to transform**:
- Convert prose workflows to Given/When/Then format
- Add specific data values (not placeholders)
- Add measurement criteria
- Keep to 15-20 lines per scenario maximum

**Length**: 45-100 lines (3-5 scenarios × 15-20 lines)

**Example transformation**:
```markdown
# Starter input (prose workflow):
When a user subscribes, they fill out a form with their interests and preferred
schedule. The system should save this, send a confirmation email, and queue them
for the next digest at their preferred time.

# Comprehensive output (Given/When/Then):
#### Scenario 1: New User Subscription

**Given** unauthenticated visitor on subscription page

**When** visitor submits subscription form:
- Email: `alice@example.com`
- Interests: `['AI', 'open source', 'creator economy']`
- Frequency: `weekly`
- Preferred time: `Monday 9:00 AM Pacific`

**Then** system responds with:
- HTTP 201 Created
- Confirmation email sent to alice@example.com within 30 seconds
- Subscription record created with status `pending_confirmation`
- Email contains confirmation link valid for 48 hours
- First digest scheduled for next Monday 9:00 AM Pacific

**Measurement**:
- API response < 200ms at 95th percentile
- Confirmation email delivery rate > 99%
- Zero duplicate subscriptions for same email
```

**What NOT to do**:
- ❌ Don't add SQL implementation (see "Avoiding Over-Specification" above)
- ❌ Don't expand to 60 lines with complete API details
- ❌ Don't invent workflows user didn't describe - clarify instead

#### Starter Section 5: Tech Constraints → Comprehensive Section 8: Technology Constraints

**What to keep**:
- User's technology choices and requirements
- Version constraints they specified
- Any "must use" or "cannot use" directives

**What to add**:
- Complete list of dependencies
- Configuration requirements (env vars, secrets)
- External service dependencies
- Runtime requirements

**Length**: 30-50 lines (roughly 2x expansion)

**Example transformation**:
```markdown
# Starter input (basic tech list):
Must use:
- Python 3.11+
- PostgreSQL for data
- Amazon SES for email
- FastAPI for API

# Comprehensive output (complete constraints):
## 8. Technology Constraints

### Required Technologies

**Language & Runtime**:
- Python 3.11 or higher
- Virtual environment with pip/poetry for dependency management

**Database**:
- PostgreSQL 14+ for persistent storage
- SQLAlchemy 2.0+ ORM for database interactions
- Alembic for schema migrations

**Email Service**:
- Amazon SES (Simple Email Service) for email delivery
- boto3 SDK for AWS integration
- SES production access (out of sandbox mode)

**API Framework**:
- FastAPI 0.100+ for REST API
- Pydantic for request/response validation
- Uvicorn as ASGI server

### External Dependencies

**AWS Services**:
- SES: Email delivery with bounce/complaint notifications
- SNS: Webhook notifications for email events (bounces, complaints)
- IAM: Credentials with SES send permissions

**Third-party Services**:
- None required for MVP

### Configuration Requirements

**Environment Variables**:
- DATABASE_URL: PostgreSQL connection string
- AWS_ACCESS_KEY_ID: SES access credentials
- AWS_SECRET_ACCESS_KEY: SES secret credentials
- AWS_REGION: SES region (e.g., us-east-1)
- API_SECRET_KEY: JWT token signing key

**Secrets Management**:
- Store AWS credentials in environment variables or secrets manager
- Never commit credentials to version control

### Constraints

- Must support deployment to standard Python hosting (Docker, Heroku, AWS ECS)
- Database must support JSONB for tags storage
- Email templates must render correctly in major email clients
```

**What NOT to do**:
- ❌ Don't explain WHY technologies were chosen (that's for ADRs)
- ❌ Don't compare alternatives or discuss tradeoffs
- ❌ Don't add deployment architecture (that's for infrastructure docs)

#### Starter Section 6: Edge Cases → Comprehensive Section 7: Edge Cases

**What to keep**:
- All edge cases user specified
- Their descriptions of expected behavior

**What to add**:
- 3-5 additional standard edge cases based on module type
- Consistent "situation → behavior" format
- Specific behaviors (not just "handle error")

**Length**: 30-45 lines (10-15 cases × 2-3 lines)

**Example transformation**:
```markdown
# Starter input (informal edge cases):
- What if email is invalid?
- What if SES is down?
- What if user unsubscribes during send?
- What about concurrent edits?

# Comprehensive output (formatted edge cases):
## 7. Edge Cases

### Email Delivery Failures
- **EC-1**: Invalid email format in database → Mark subscription as `invalid_email`, pause sends, flag for manual review
- **EC-2**: SES API timeout or 503 error → Retry 3x with exponential backoff (2s, 4s, 8s), alert admin if all fail
- **EC-3**: Hard bounce (permanent delivery failure) → Mark subscription as `bounced`, update status to `inactive`, log reason
- **EC-4**: Soft bounce (mailbox full) → Retry after 7 days, treat as hard bounce if second soft bounce
- **EC-5**: Rate limit exceeded → Queue emails for next send window (1 hour), log warning, don't retry immediately

### User Subscription Management
- **EC-6**: User unsubscribes mid-digest generation → Cancel pending send, update status to `unsubscribed`, don't log as failure
- **EC-7**: User updates preferences during digest preparation → Use new preferences for next digest, complete current with old preferences
- **EC-8**: Duplicate subscription request (same email) → Return existing subscription, send "already subscribed" email, don't create duplicate

### Content and Data Issues
- **EC-9**: No articles match user's tags → Send "no content this period" email, don't skip digest entirely, suggest tag expansion
- **EC-10**: Article content missing or malformed → Exclude from digest, log warning, continue with remaining articles

### Concurrent Access
- **EC-11**: Two processes update same subscription simultaneously → Last write wins with version increment, audit log both attempts
- **EC-12**: User deletes account during active digest send → Cancel send immediately, mark as `user_deleted`, cleanup subscription data

### Database and Infrastructure
- **EC-13**: Database connection lost mid-transaction → Rollback automatically, user sees "temporary error" message, operation retryable
- **EC-14**: Scheduled task fails to start → Log critical error, alert ops team, retry on next schedule cycle
```

**What NOT to do**:
- ❌ Don't write implementation solutions (see "Avoiding Over-Specification")
- ❌ Don't expand each case to 15 lines with error handling code
- ❌ Don't invent edge cases unrelated to user's feature

**If user provided minimal edge cases**:
Add standard ones based on module type (see Section 7 generation rules above), but mark: "[STANDARD EDGE CASES: verify these apply to this feature]"

#### Starter Section 7: MVP Scope → Comprehensive Section 6: Implementation Phases

**What to keep**:
- User's must-have vs nice-to-have distinction
- Their sequencing hints ("first we need X, then Y")

**What to transform**:
- Convert feature list into 3-5 logical phases
- Add deliverables and success criteria per phase
- Identify dependencies between phases
- DO NOT add time estimates (per user decision)

**Length**: 30-75 lines (3-5 phases × 10-15 lines)

**Example transformation**:
```markdown
# Starter input (feature priority list):
MVP must-haves:
- User registration and preference setting
- Content tagging system
- Basic digest generation and email sending
- Unsubscribe functionality

Nice-to-have later:
- Advanced analytics dashboard
- A/B testing for content
- Social sharing features

# Comprehensive output (phased milestones):
## 6. Implementation Phases

**Phase 1: Core User Management**

**Goal**: Enable users to create accounts and configure content preferences

**Deliverables**:
- User registration with email confirmation
- Preference configuration UI (tags, frequency, send time)
- Account management (update preferences, deactivate account)
- Unsubscribe mechanism with one-click option

**Success Criteria**:
- Users can register and confirm email within 5 minutes
- Preference updates take effect within 24 hours
- Unsubscribe works from digest emails and web UI
- All user stories US-1, US-3 validated

**Dependencies**: None (foundational phase)

---

**Phase 2: Content Management**

**Goal**: Establish content repository with tagging for personalization

**Deliverables**:
- Article ingestion pipeline with tag assignment
- Content database with search and filtering
- Tag management system (create, edit, map to articles)
- Content-to-user matching algorithm

**Success Criteria**:
- 100+ articles ingested and tagged correctly
- Matching algorithm returns 3-7 relevant articles per user tag set
- Content queries complete in < 100ms for 10,000 articles
- All acceptance scenarios for content assignment pass

**Dependencies**:
- Phase 1 complete (need user preference data)

---

**Phase 3: Digest Generation and Delivery**

**Goal**: Generate personalized digests and deliver via email

**Deliverables**:
- Digest template rendering engine
- Scheduling system for user-preferred send times
- Amazon SES integration for email delivery
- Bounce and complaint handling webhook

**Success Criteria**:
- Digests render correctly in major email clients (Gmail, Outlook, Apple Mail)
- 1,000+ users processed within 15 minutes
- Email delivery rate > 95% for valid addresses
- Bounce notifications processed within 30 seconds
- All user stories US-2, US-4 validated

**Dependencies**:
- Phase 1 complete (need user schedules)
- Phase 2 complete (need content matching)
- AWS SES production access approved

---

**Phase 4: Monitoring and Optimization** (Post-MVP)

**Goal**: Add observability and performance optimization

**Deliverables**:
- Analytics dashboard for engagement metrics
- Performance monitoring and alerting
- A/B testing framework for content and timing
- Database query optimization

**Success Criteria**:
- Engagement metrics visible in real-time dashboard
- Performance targets from Section 5 met consistently
- A/B tests can run with statistical significance
- User story US-5 (admin metrics) validated

**Dependencies**:
- Phase 3 complete and stable in production
- Minimum 2 weeks of production data for baseline metrics

---

**MVP Definition**: Phases 1-3 constitute the minimum viable product. Phase 4 is post-MVP enhancement.
```

**What NOT to do**:
- ❌ Don't create hour-by-hour task breakdowns
- ❌ Don't add time estimates (days, weeks) - user explicitly rejected this
- ❌ Don't include implementation details (which functions to write)
- ❌ Don't plan engineering tasks - describe deliverables only

#### Starter Section 8: Testing → Comprehensive Section 9: Testing Strategy

**What to keep**:
- User's testing approach and priorities
- Coverage expectations they mentioned

**What to add**:
- Structured test types (unit, integration, load, acceptance)
- Specific coverage targets with percentages
- Connection to performance targets (Section 5)
- Validation gates (what must pass before shipping)

**Length**: 30-50 lines

**Example transformation**:
```markdown
# Starter input (basic testing notes):
Need good test coverage, especially for email delivery and user preference handling.
Should test under load - we expect 5,000+ users eventually.

# Comprehensive output (structured strategy):
## 9. Testing Strategy

### Unit Testing
**What to test**:
- Content matching algorithm (tags to articles)
- Email template rendering (HTML generation)
- Preference validation (input sanitization)
- Scheduling calculations (timezone conversions)

**Coverage target**: 85% code coverage minimum for core business logic

**Key scenarios**:
- Content matching returns correct number of articles (3-7)
- Template renders correctly with various article counts
- Timezone conversions handle DST correctly
- Invalid preferences rejected with clear error messages

---

### Integration Testing
**What to test**:
- Full digest pipeline: schedule → content fetch → render → send
- Webhook processing: bounce/complaint → database update
- User workflow: registration → confirmation → first digest
- Admin workflow: user management → metrics viewing

**Coverage target**: All critical user workflows from Section 2

**Key scenarios**:
- End-to-end digest delivery completes for various user configurations
- Bounce notifications correctly update subscription status
- Failed sends trigger retry mechanism and eventual admin alert
- User preference updates reflected in next digest

---

### Load/Performance Testing
**What to test**: System performance under expected load

**Performance targets to validate** (from Section 5):
- 1,000 concurrent users processed within 15 minutes
- API response times < 200ms at 95th percentile
- Email delivery: 95% sent within 30 minutes of schedule
- Database queries: < 100ms for content matching
- Webhook processing: < 1 second per notification

**Load scenarios**:
- Simulate 5,000 active subscriptions with varied schedules
- Concurrent API requests during peak preference update times
- Sustained digest generation for 1 hour
- Burst webhook delivery (100 notifications in 1 minute)

---

### Acceptance Testing
**What to test**: All acceptance scenarios from Section 4 pass in production-like environment

**Success criteria**:
- Scenario 1 (subscription) passes with all assertions
- Scenario 2 (digest delivery) passes with timing requirements
- Scenario 3 (preference update) passes with propagation time < 24h
- Scenario 4 (unsubscribe) passes with immediate effect
- All edge cases from Section 7 handled correctly

---

### Validation Gates

**Before Phase 1 completion**:
- [ ] Unit tests: 85%+ coverage, all passing
- [ ] Integration tests: User registration and preference workflows passing
- [ ] No critical security vulnerabilities

**Before Phase 3 completion (MVP)**:
- [ ] All unit and integration tests passing
- [ ] Load tests: 1,000 users processed successfully
- [ ] Acceptance tests: All scenarios from Section 4 validated
- [ ] Performance targets from Section 5 met
- [ ] Edge cases from Section 7 handled correctly

**Before production launch**:
- [ ] All tests passing in staging environment
- [ ] Load testing validated at 2x expected initial load
- [ ] Security audit completed
- [ ] Disaster recovery tested
- [ ] Monitoring and alerting operational
```

**What NOT to do**:
- ❌ Don't write individual test cases (see "Avoiding Over-Specification")
- ❌ Don't design test suite structure
- ❌ Don't specify testing frameworks/tools (that's Section 8)

### Generate New Sections

**Section 5: Performance Targets** and **Section 10: Integration Points** often don't exist in starter templates. You must infer them.

#### Generating Section 5: Performance Targets

**Infer from**:
1. **User stories**: Acceptance criteria often hint at performance ("within seconds", "quickly", etc.)
2. **Scale expectations**: Problem statement mentions number of users/volume
3. **Workflows**: Time-sensitive operations (email delivery, API responses)
4. **Industry standards**: Default reasonable targets for similar systems

**Example inference**:
```markdown
# From starter user story:
As a subscriber, I need digests delivered at my preferred time,
so I'm not disrupted by poorly timed emails.
Acceptance: Emails arrive within my chosen time window

# Infer performance targets:
### Response Times
- API endpoints: < 200ms at 95th percentile
- Content matching query: < 100ms for 10,000 articles
- Email template rendering: < 500ms per digest

### Throughput
- Digest generation: 1,000 users processed in 15 minutes
- Concurrent API requests: 50+ simultaneous preference updates
- Webhook processing: 100 notifications/minute

### Scalability
- Support 10,000 active subscriptions (initial target)
- Handle 50,000 articles in content database
- Process 100,000 digest sends/day

### Delivery SLA
- 95% of scheduled digests sent within 30 minutes of target time
- 99% delivery rate for valid email addresses
- Bounce notifications processed within 60 seconds
```

**If truly unable to infer**: Mark "[NEEDS PERFORMANCE TARGET: what's acceptable for X?]" but provide reasonable defaults based on similar systems.

#### Generating Section 10: Integration Points

**Infer from**:
1. **Technology constraints**: External services mentioned (SES, databases)
2. **Data model**: What data flows in/out
3. **Workflows**: Where external systems are referenced
4. **Architecture context**: Multi-module systems have integration needs

**Example inference**:
```markdown
# From starter mentions of "SES for email" and "PostgreSQL database"

## 10. Integration Points

### Dependencies (What we need)

**Database: PostgreSQL**
- Interface: SQLAlchemy ORM + raw SQL for complex queries
- Data consumed: All user, subscription, article data
- Connection requirements: Connection pool (10-20 connections), SSL enabled

**Email Service: Amazon SES**
- Interface: boto3 SDK, SES API v2
- Data format: Email messages (JSON), delivery status webhooks (SNS notifications)
- Authentication: AWS IAM credentials with SES send permissions
- Rate limits: Respect SES sending limits (14 emails/second by default)

---

### Provides (What we offer)

**REST API**
- Interface: FastAPI RESTful endpoints
- Exposed to: Frontend web application, mobile apps (future)
- Authentication: JWT tokens with 24-hour expiration

**Webhook Endpoints**
- Interface: HTTP POST receivers
- Exposed to: Amazon SNS for bounce/complaint notifications
- Authentication: SNS signature verification

---

### Data Contracts

**API Request Example** (POST /api/subscriptions):
```json
{
  "email": "user@example.com",
  "interest_tags": ["AI", "open source"],
  "send_interval": "weekly",
  "preferred_send_time": "monday_09:00",
  "timezone": "America/Los_Angeles"
}
```

**API Response Example**:
```json
{
  "subscription_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending_confirmation",
  "confirmation_sent": true,
  "next_digest_scheduled": "2025-10-14T09:00:00-07:00"
}
```

**Webhook Payload Example** (SNS bounce notification):
```json
{
  "notificationType": "Bounce",
  "bounce": {
    "bounceType": "Permanent",
    "bouncedRecipients": [
      {"emailAddress": "bounced@example.com"}
    ]
  },
  "mail": {
    "messageId": "0000014a8a7e-aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee-000000"
  }
}
```
```

**If integration points unclear**: Mark "[NEEDS INTEGRATION SPEC: clarify how this connects to X]"

### Expansion Quality Checklist

**Before finalizing comprehensive PRD, verify**:

#### Faithfulness to Starter
- [ ] All user's original content preserved (no loss of intent)
- [ ] Expansions stay true to user's vision
- [ ] No invented features user didn't request
- [ ] User's priorities maintained (MVP vs nice-to-have)

#### Completeness
- [ ] All 11 comprehensive sections present
- [ ] All starter sections successfully mapped
- [ ] Generated sections (5, 10) based on solid inferences
- [ ] No section is just "[TODO]" without explanation

#### Length Discipline
- [ ] Total length: 600-800 lines (not 1843)
- [ ] Each section within target range (see "Avoiding Over-Specification")
- [ ] No implementation details (SQL, API code, test cases)
- [ ] Focus on WHAT, not HOW

#### Quantification
- [ ] All user stories have quantified acceptance criteria
- [ ] All performance targets have numbers and units
- [ ] All scale expectations specified
- [ ] Vague terms ("fast", "scalable") replaced with measurements

#### Formatting
- [ ] User stories: "As a/I need/So that" + Acceptance
- [ ] Acceptance scenarios: Given/When/Then format
- [ ] Edge cases: "EC-N: situation → behavior" format
- [ ] Data model: Complete DDL or schema provided
- [ ] Phases: Goal/Deliverables/Success/Dependencies structure

#### Consistency
- [ ] User stories (Sect 2) address problems (Sect 1)
- [ ] Scenarios (Sect 4) validate user stories (Sect 2)
- [ ] Performance targets (Sect 5) tested in scenarios (Sect 4)
- [ ] Testing (Sect 9) covers acceptance criteria
- [ ] Success criteria (Sect 11) measure problem resolution (Sect 1)

#### Clarity Markers
- [ ] Unknown details marked: "[NEEDS CLARIFICATION: specific question]"
- [ ] Assumptions marked: "[ASSUMPTION: based on X, verify]"
- [ ] Inferences marked: "[INFERRED FROM: workflow Y]"
- [ ] Conflicts marked: "[CONFLICT: Source A vs Source B]"

### Expansion Example (End-to-End)

**Starter template excerpt** (50 lines):
```markdown
## 1. Core Problem
Users want personalized content but we send everyone the same newsletter.
Marketing spends 10+ hours weekly doing manual curation with poor results.

## 2. User Stories
- Users set their content interests
- System sends digests matching those interests
- Users can unsubscribe easily

## 3. Data
Users (email, name, preferences)
Subscriptions (user_id, tags, frequency)
Articles (title, content, tags)

## 4. Workflows
User subscribes → fills form → confirmation email → queued for digest
...
```

**Comprehensive expansion** (400 lines, excerpts):
```markdown
## 1. Problem Statement

### Current Situation
Currently, the content distribution system sends identical newsletters to all
15,000 subscribers regardless of interests...
[expands to 60 lines with quantification]

## 2. User Stories

**US-1: Content Preference Configuration**

As a subscriber with limited reading time,
I need to specify my content interests and delivery schedule,
So that I receive only relevant articles at convenient times.

**Acceptance**: User can select 3-10 tags, choose frequency, set time;
changes effective within 24 hours.

[6 more stories, formatted, quantified]

## 3. Complete Data Model

### Entity: users

**Fields**:
| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| user_id | UUID | PK, NOT NULL | Unique identifier |
[complete DDL with 3 entities, relationships, indexes]

## 4. Acceptance Scenarios

#### Scenario 1: User Subscribes to Weekly Digest

**Given** visitor on subscription page

**When** submits form with email, tags, frequency

**Then** HTTP 201, confirmation email within 30s, record created

**Measurement**: 95% complete < 200ms

[4 more scenarios, 15 lines each]

## 5. Performance Targets

### Response Times
- API endpoints: < 200ms at 95th percentile
- Content matching: < 100ms for 10,000 articles
[complete performance requirements with numbers]

## 6. Implementation Phases

**Phase 1: Core User Management**
Goal: Enable registration and preference configuration
Deliverables: Registration, preference UI, account management
Success: US-1, US-3 validated
Dependencies: None

[4 more phases with structure]

## 7. Edge Cases

- **EC-1**: Invalid email → Mark invalid, pause, flag review
- **EC-2**: SES timeout → Retry 3x exponential, alert if fail
[13 more edge cases, concise]

## 8. Technology Constraints

### Required Technologies
- Python 3.11+
- PostgreSQL 14+ with JSONB support
- Amazon SES with production access
[complete tech stack with versions]

## 9. Testing Strategy

### Unit Testing
What: Content matching, template rendering, scheduling
Coverage: 85% minimum
Key scenarios: Correct article counts, timezone handling
[structured testing approach]

## 10. Integration Points

### Dependencies
PostgreSQL: SQLAlchemy ORM, connection pool
Amazon SES: boto3 SDK, SNS webhooks
[complete integration specifications]

## 11. Success Criteria

### User-facing Success
- 95% delivery rate for scheduled digests
- < 5% unsubscribe rate in first month
[measurable success metrics]
```

**Transformation summary**:
- Started: 300 lines (starter template)
- Ended: 650 lines (comprehensive PRD)
- Expansion: ~2x growth (not 6x to 1843)
- Focus: Added structure, quantification, completeness
- Avoided: Implementation details, hour-by-hour plans, test suites

---

## Tuning This Document

**To improve PRD generation**:

1. **Add examples** to sections where agents struggle
2. **Strengthen rules** where output quality is poor
3. **Add default values** for common gaps
4. **Refine quality checks** based on review feedback

**This is a living document** - refine it as you learn what works.

---

**Remember**: Your PRD should be so complete that SpecKit can process it with minimal additions or clarifications. Quality here saves time in all downstream steps.
