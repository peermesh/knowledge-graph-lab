# Product Requirements Document (PRD) Template

**Module Name**: [Your module name]
**Version**: [e.g., 0.1.0]
**Owner(s)**: [Names/teams responsible]

---

**Purpose**: This template defines the structure for a comprehensive Product Requirements Document (PRD). Complete all sections below to create a source document ready for SpecKit processing (target: 600-800 lines for comprehensive modules, 300-500 for simpler modules).

**Why this matters**: SpecKit produces dramatically better results when given rich, detailed input that focuses on WHAT (not HOW). This template balances completeness with brevity—providing enough detail for implementation without over-specifying the solution.

**Who should use this**: Developers and module owners preparing functional and technical requirements for their modules (AI, Backend, Frontend, Publishing).

**⚠️ KEY PRINCIPLE**: Describe observable behavior and requirements, not implementation details. The `/plan` command and implementation team handle the HOW.

---

## Important: Length and Detail Guidance

**Comprehensive Spec (Phase 3 - WO-3):**
- Expected: 800-1,500 lines (detailed, implementation-focused)
- Purpose: Provide rich input for quality refinement
- Don't worry about length - capture all necessary detail

**Final Spec (Phase 4 - WO-4):**
- Target: 500-700 lines (refined, requirements-focused)
- Purpose: Implementation-ready PRD matching case study quality
- Achieved by: Removing implementation details, tightening language, eliminating redundancy

**What This Means:**
- It's NORMAL for this template to produce 1,000+ lines initially
- Quality refinement (WO-4) will reduce it to 500-700 lines
- Focus on completeness here, refinement comes later

---

## Section 1: Problem Statement (50-100 lines)

**Purpose**: Establish context - what problem are you solving and why it matters.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ Current situation described with quantified pain points (e.g., "2 hours/day wasted", "20% failure rate")
- ✅ Who is affected identified (specific user roles, scale expectations)
- ✅ Goals stated with measurable outcomes (e.g., "reduce time by 90%", "increase success to 99.9%")
- ✅ Problem statement is specific (not "improve efficiency" but "reduce manual sync time from 2 hours to 10 minutes")
- ✅ Business value clear (why solving this problem matters)
- ✅ Scale context provided (number of users, records, requests)

**This section is INCOMPLETE if:**
- ❌ Problem is vague or generic ("users want better experience")
- ❌ No quantified metrics (no numbers, percentages, or time estimates)
- ❌ Who is affected is unclear (just "users" without specificity)
- ❌ Goals are aspirational without measurable targets ("make things faster")
- ❌ Current situation not described (no baseline to improve from)
- ❌ Includes market research or competitive analysis (save for separate docs)

### What to include:

**Current Situation**:
*   What exists today (or doesn't exist) that necessitates this module.
*   Why the current approach is inadequate.
*   What specific pain points users or the system face.
*   Quantify the problem where possible (e.g., "developers waste 2 hours per day manually syncing data," "20% of requests fail due to...").

**Who is Affected**:
*   Primary users of this module (e.g., "backend developers," "content editors," "end-users on mobile").
*   Their environment and constraints.
*   Scale expectations (e.g., "10,000 daily active users," "1 million records," "20+ concurrent agents").

**Goals**:
*   What success looks like for the module.
*   Measurable outcomes (e.g., "reduce data sync time by 90%," "increase request success rate to 99.9%," "decrease dashboard load time to <500ms").

### What to Include (Requirements Focus):
✅ User pain points with quantified impact
✅ Current workflow and why it's inadequate
✅ Who is affected and their constraints
✅ Measurable goals and success metrics
✅ Scale expectations (users, records, concurrency)
✅ Business value and rationale

### What to Exclude (Implementation Details):
❌ Market research and competitive analysis
❌ Detailed cost-benefit calculations
❌ Historical context beyond immediate problem
❌ Team structure or organizational charts
❌ Project management methodology
❌ Technology selection rationale (save for Section 8)

### Level of Detail (Example):

**Good** (requirements-focused):
```
Current Situation: Developers manually maintain project tracking spreadsheets,
spending 2 hours/day on updates. 20% of status reports contain outdated information
due to sync delays.

Who is Affected: 15 backend developers managing 40+ active projects across 3 teams.

Goals: Centralized project tracking with real-time updates, reducing manual sync
time by 90% and eliminating data staleness.
```

**Too detailed** (implementation-focused):
```
Current Situation: The company uses Google Sheets (spreadsheet ID: 1a2b3c...)
with 47 columns tracking various metrics. Data is entered using Apps Script
triggers that run every 15 minutes. The sync process involves OAuth2 authentication
with refresh tokens stored in ~/.credentials/. Error rate analysis shows 18.7%
of requests fail due to rate limiting (HTTP 429). We compared 7 project management
tools (Jira, Asana, Linear, ...) with feature matrices and cost projections.
```

---

## Section 2: User Stories (5-10 stories)

**Purpose**: Describe how the module will be used in practice from a user's perspective.

**⚠️ CRITICAL**: SpecKit expects a formal user story format. Use the structure below exactly.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ 5-10 user stories covering all major workflows
- ✅ Each story follows "As a... I need... So that..." format
- ✅ User roles are specific with context (not just "user")
- ✅ Acceptance criteria are quantified (specific numbers, times, counts)
- ✅ Stories focus on WHAT capability is needed (not HOW to implement)
- ✅ Stories cover main user journeys end-to-end
- ✅ Edge cases mentioned in acceptance criteria where relevant

**This section is INCOMPLETE if:**
- ❌ Fewer than 5 stories (insufficient coverage of workflows)
- ❌ Stories lack quantified acceptance criteria ("fast" instead of "<2 seconds")
- ❌ Stories describe implementation ("using React form") instead of capability
- ❌ User roles are generic ("as a user") without context
- ❌ Stories missing "So that" benefit statement
- ❌ Acceptance criteria are vague ("works correctly")
- ❌ Major workflows not represented (gap in user journey coverage)

### User Story Format (REQUIRED):

**US-[N]: [Short Descriptive Title]**

As a [specific user type with context],
I need [specific capability or feature],
So that [measurable benefit or value].

**Acceptance**: [Quantified success criteria with specific numbers, times, or counts]

### What to Include (Requirements Focus):
✅ User role with specific context
✅ Capability or feature needed (WHAT, not HOW)
✅ Measurable benefit or value
✅ Quantified acceptance criteria
✅ 5-10 stories covering main workflows
✅ Given/When/Then format for acceptance

### What to Exclude (Implementation Details):
❌ UI mockups or wireframes
❌ Button labels or screen layouts
❌ Database queries or API calls
❌ Technology-specific implementation
❌ Internal system architecture
❌ Code structure or module organization

### Level of Detail (Example):

**Good** (requirements-focused):
```
US-1: Project Status Update

As a backend developer managing multiple projects,
I need to update project status in one centralized location,
So that all stakeholders see current information without manual sync.

Acceptance:
- Update completes in <2 seconds
- Changes visible to all users within 5 seconds
- Supports 20+ concurrent updates
```

**Too detailed** (implementation-focused):
```
US-1: Project Status Update via React Form

As a backend developer using Chrome browser on MacBook Pro,
I need a React form component with Material-UI TextField and Select components,
calling PUT /api/projects/:id with JWT authentication in Authorization header,
So that the PostgreSQL database updates the projects table via Prisma ORM,
triggering WebSocket broadcast through Socket.io to subscribed clients.

Acceptance:
- Form renders in <100ms (React.lazy with Suspense)
- API endpoint uses Express middleware for auth validation
- Database update uses transaction isolation level READ_COMMITTED
- WebSocket broadcast uses Redis pub/sub for horizontal scaling
```

---

## Section 3: Complete Data Model (if applicable)

**Purpose**: Define exactly what data your module stores and how it's structured.

**⚠️ CRITICAL**: SpecKit preserves complete data models perfectly. Do not skimp on details here. Provide full DDL or schemas.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ All tables/collections listed with descriptions
- ✅ All columns/fields with data types specified
- ✅ Primary keys identified for all tables
- ✅ Foreign keys documented with relationships explained
- ✅ Major constraints listed (UNIQUE, NOT NULL, CHECK constraints with reasoning)
- ✅ Indexes mentioned for performance-critical queries
- ✅ Relationships between entities clear (1-to-many, many-to-many)
- ✅ If stateless: Explicitly stated "No persistent data model"

**This section is INCOMPLETE if:**
- ❌ Tables listed without column definitions
- ❌ Data types missing or vague ("string" instead of "VARCHAR(255)")
- ❌ Primary keys not identified
- ❌ Foreign key relationships unclear or missing
- ❌ Constraints not documented (why UNIQUE? why NOT NULL?)
- ❌ Includes complete CREATE TABLE SQL (use high-level description instead)
- ❌ Indexes listed without explaining why they're needed
- ❌ Relationships between tables ambiguous

### What to include:

*   **For SQL Databases**: Provide complete `CREATE TABLE` statements (DDL), including all columns, types, constraints (`NOT NULL`, `UNIQUE`), primary keys, foreign keys, and indexes.
*   **For NoSQL Databases**: Provide complete JSON schemas for each document type.
*   **If Stateless**: Explicitly state "No persistent data model - this module is stateless" and describe any significant in-memory data structures.

### What to Include (Requirements Focus):
✅ Table names and brief descriptions
✅ Column names with data types
✅ Primary keys and foreign keys (which columns)
✅ Major constraints (UNIQUE, NOT NULL, CHECK)
✅ Integration schemas (JSON examples with field types)
✅ Relationships between entities (1-to-many, many-to-many)

### What to Exclude (Implementation Details):
❌ Complete CREATE TABLE statements with all syntax
❌ Index creation statements (mention indexes exist, not full DDL)
❌ Database migration scripts
❌ Query optimization details (EXPLAIN ANALYZE output)
❌ Backup and restore procedures
❌ Performance tuning parameters

### Level of Detail (Example):

**Good** (requirements-focused):
```
Table: users
Purpose: Store user subscription information
Columns:
  - id (UUID, primary key, auto-generated)
  - email (VARCHAR(255), unique, not null, email format)
  - created_at (TIMESTAMP, not null, defaults to now)

Foreign keys: None
Indexes: email (for lookup performance)
Constraints: Email must match valid email pattern
```

**Too detailed** (implementation-focused):
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
ANALYZE users;
```

---

## Section 4: Acceptance Scenarios (3-5 detailed scenarios)

**Purpose**: Show step-by-step execution of key user stories.

**⚠️ CRITICAL**: SpecKit expects `Given/When/Then` format for testability. These scenarios should directly validate the acceptance criteria of your User Stories from Section 2.

**⚠️ CRITICAL**: Keep scenarios brief (15-20 lines max per scenario). Focus on WHAT happens, not HOW it's implemented.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ 3-5 scenarios covering main user stories from Section 2
- ✅ Each scenario follows Given/When/Then format (BDD style)
- ✅ Given conditions include specific example data (not placeholders)
- ✅ When actions are concrete with actual parameters
- ✅ Then outcomes are measurable and observable
- ✅ Measurement criteria specified for success
- ✅ Scenarios are brief (15-20 lines max, not 60+ lines with SQL)
- ✅ Scenarios validate acceptance criteria from user stories

**This section is INCOMPLETE if:**
- ❌ Fewer than 3 scenarios (insufficient coverage)
- ❌ Scenarios don't follow Given/When/Then structure
- ❌ Given conditions use placeholders ("[user]") instead of examples ("user@example.com")
- ❌ Scenarios include SQL queries or implementation code
- ❌ Then outcomes are vague ("works correctly") instead of specific ("returns HTTP 200 with user_id field")
- ❌ Scenarios exceed 20 lines (too detailed, focused on HOW not WHAT)
- ❌ No measurement criteria (how to verify success?)
- ❌ Scenarios don't map to user stories from Section 2

### Scenario Format (REQUIRED):

#### Scenario [N]: [Descriptive Title matching a User Story]

**Given** [specific starting conditions with actual data values]
- [Condition 1, e.g., A user with email "test@example.com" exists]

**When** [a specific action is taken with actual parameters]
- [e.g., The user submits a POST request to /login with email "test@example.com" and password "password123"]

**Then** [specific, measurable, and observable outcomes]
- [Assertion 1, e.g., The system returns an HTTP 200 status code]

**Measurement**: [How to verify - specific metric]

### What to Include (Requirements Focus):
✅ Given/When/Then format (BDD style)
✅ Specific starting conditions with example data
✅ Observable actions and outcomes
✅ Measurable success criteria
✅ 3-5 scenarios covering main workflows
✅ 15-20 lines max per scenario

### What to Exclude (Implementation Details):
❌ Complete test code or test frameworks
❌ SQL queries or database operations
❌ API endpoint implementations
❌ Error handling code
❌ Retry logic or circuit breakers
❌ 60+ line scenarios with SQL setup

### Level of Detail (Example):

See examples below in original template section.

---

### Examples

❌ **TOO MUCH** (60+ lines with SQL statements, detailed implementation):
```
Scenario 1: Weekly Digest Delivery
Given:
- Database has the following records:
  - User table: INSERT INTO users (id, email, digest_interval, tags) VALUES (1, 'user@example.com', 'weekly', '["creator economy", "AI"]');
  - Articles table: INSERT INTO articles (id, title, url, tags, published_date) VALUES ...
  - [30 more lines of SQL setup]
When:
- Scheduler executes at Monday 9:00 AM
- System queries: SELECT * FROM articles WHERE tags @> ANY(SELECT tags FROM users WHERE digest_interval = 'weekly')
- [20 more lines of SQL queries and implementation details]
Then:
- Email queue contains record with specific HTML template structure
- [10 more lines of implementation assertions]
```

✅ **JUST RIGHT** (15-20 lines, focused on observable behavior):
```
Scenario 1: Weekly Digest Delivery
Given:
- User configured weekly digest for tags "creator economy" and "AI"
- 5 matching articles published in the past 7 days
- Scheduled time: Monday 9:00 AM

When:
- Scheduled time arrives
- Digest generation job executes

Then:
- Email delivered within 2 minutes
- Email contains 3-5 matching articles
- Each article includes: title, summary, link
- Email includes unsubscribe link
- User's next_digest_date updated to next Monday 9:00 AM

Measurement: 95% of digests delivered within 15 minutes of scheduled time
```

---

## Section 5: Performance Targets (quantified)

**Purpose**: Define the measurable performance requirements.

**⚠️ CRITICAL**: Every target MUST be quantified with numbers and units.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ Response times quantified with percentiles (p50, p95, p99)
- ✅ Throughput targets with units (requests/second, records/minute)
- ✅ Scalability limits specified (max users, max records, max concurrency)
- ✅ Resource constraints documented (memory, CPU, storage limits)
- ✅ Availability targets stated (uptime %, acceptable downtime)
- ✅ All targets have numbers and units (not "fast" but "<200ms p95")
- ✅ Targets are realistic for expected usage patterns

**This section is INCOMPLETE if:**
- ❌ Targets use qualitative terms ("fast", "responsive", "scalable")
- ❌ No percentiles specified for response times (p50/p95/p99)
- ❌ Throughput without units ("500" instead of "500 requests/second")
- ❌ Scalability limits vague ("lots of users" instead of "10,000 concurrent")
- ❌ Includes benchmark results or load test output (state targets, not test results)
- ❌ Server specifications listed (CPU/RAM) instead of behavior requirements
- ❌ Targets unrealistic (requiring impossible performance)
- ❌ Missing key dimension (response time stated but no throughput target)

### What to include:

**Response Times**:
*   API endpoint latency: e.g., `< 200ms for 95th percentile`

**Throughput**:
*   Requests per second: e.g., `Handles 500 requests/sec`

**Scalability Limits**:
*   Maximum records/documents: e.g., `Scales to 10 million documents`

### What to Include (Requirements Focus):
✅ Quantified response times (with percentiles)
✅ Throughput targets (requests/second, records/minute)
✅ Scalability limits (max users, max records)
✅ Resource constraints (memory, CPU, storage)
✅ Concurrency requirements
✅ Availability targets (uptime %)

### What to Exclude (Implementation Details):
❌ Benchmark results or load test output
❌ Server specifications (CPU cores, RAM GB)
❌ Database tuning parameters
❌ Caching strategies (Redis config, TTL values)
❌ Network configuration details
❌ Infrastructure sizing calculations

### Level of Detail (Example):

**Good** (requirements-focused):
```
Response Times:
- API endpoints: <200ms (p95), <500ms (p99)
- Database queries: <50ms (p95)

Throughput:
- 500 requests/second sustained
- 1000 requests/second peak (5-minute burst)

Scalability:
- 10,000 concurrent users
- 1 million records in database
- 100 concurrent updates
```

**Too detailed** (implementation-focused):
```
Response Times:
- API endpoints: <200ms on AWS t3.medium with 2 vCPU and 4GB RAM
- Achieved via Nginx reverse proxy with gzip compression level 6
- Redis cache (cache-aside pattern) with 15-minute TTL
- Connection pooling: min 10, max 100 connections

Throughput:
- Load test results: ApacheBench -n 10000 -c 100 shows 523 req/sec
- Tested on m5.xlarge EC2 instances in us-east-1
- Database: PostgreSQL 14 with shared_buffers=256MB, work_mem=4MB
- Horizontal scaling via AWS ALB distributing to 3 instances
```

---

## Section 6: Implementation Phases (3-5 high-level milestones)

**Purpose**: Identify major delivery milestones - WHAT to deliver, not HOW to build it.

**⚠️ SIMPLIFIED**: This section defines high-level milestones only. The `/plan` command creates detailed implementation phases with tasks and sequences.

**⚠️ NO TIME ESTIMATES**: Focus on deliverables and dependencies, not duration estimates.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ 3-5 high-level phases (milestones, not day-by-day tasks)
- ✅ Each phase has clear goal (what it achieves)
- ✅ Deliverables are specific and testable per phase
- ✅ Dependencies between phases identified
- ✅ Phases are logically grouped (related deliverables together)
- ✅ MVP-focused sequence (core functionality first)
- ✅ No time estimates or schedules (focus on WHAT not WHEN)

**This section is INCOMPLETE if:**
- ❌ More than 5 phases (too granular, should be high-level milestones)
- ❌ Phases include day-by-day or hour-by-hour schedules
- ❌ Deliverables are vague ("make progress", "work on feature")
- ❌ Dependencies unclear or missing
- ❌ Phases describe HOW to build (technology details, implementation approach)
- ❌ Includes sprint planning or story points
- ❌ Individual developer assignments listed
- ❌ Phases out of logical order (later work blocking earlier work)

### What to include:

For each phase (aim for 3-5 phases):

**Phase [N]: [Phase Name]**

**Goal**: [What this phase achieves - the outcome, not the process]

**Deliverables**:
- [Specific output 1, e.g., "Complete database schema committed"]
- [Specific output 2, e.g., "API endpoints functional"]

**Dependencies**:
- [What must be complete before starting this phase]

### What to Include (Requirements Focus):
✅ 3-5 high-level milestones
✅ What each phase delivers (outcomes)
✅ Dependencies between phases
✅ Logical grouping of deliverables
✅ MVP-focused sequence
✅ Phase goals (not durations)

### What to Exclude (Implementation Details):
❌ Day-by-day or hour-by-hour schedules
❌ Individual developer assignments
❌ Sprint planning or story points
❌ Detailed task breakdowns (save for `/plan`)
❌ Technology evaluation criteria
❌ Team coordination logistics

### Level of Detail (Example):

**Good** (requirements-focused):
```
Phase 1: Core Infrastructure
Goal: Establish foundational data storage and job scheduling
Deliverables:
- Database schema deployed
- Basic CRUD API endpoints
- Job scheduler configured
Dependencies: None

Phase 2: Digest Generation Logic
Goal: Implement content matching and email composition
Deliverables:
- Article matching algorithm
- Email template system
- Content ranking logic
Dependencies: Phase 1 complete
```

**Too detailed** (implementation-focused):
```
Phase 1: Core Infrastructure (Sprint 1-2, Days 1-10)
Goal: Establish foundational data storage using PostgreSQL 14 with Prisma ORM
Deliverables:
- Day 1-2: Developer environment setup with Docker Compose
- Day 3-4: Database schema (migrations written in Prisma DSL)
- Day 5-6: CRUD endpoints (Express router with Joi validation)
- Day 7-8: Celery setup (RabbitMQ message broker, 4 worker processes)
- Day 9-10: Testing and code review
Team: 2 backend developers (Alice on DB, Bob on API)
Technology evaluation: Considered Bull vs Celery (Celery chosen for Python integration)
Dependencies: AWS RDS instance provisioned, VPC configured
```

---

### Example

**Phase 1: Core Infrastructure**
**Goal**: Establish foundational data storage and job scheduling
**Deliverables**:
- Database schema deployed
- Basic CRUD API endpoints
- Job scheduler (Celery) configured
**Dependencies**: None

**Phase 2: Digest Generation Logic**
**Goal**: Implement content matching and email composition
**Deliverables**:
- Article matching algorithm
- Email template system
- Content ranking logic
**Dependencies**: Phase 1 complete

---

## Section 7: Edge Cases (10-15 cases, 2-3 lines each)

**Purpose**: Document failure modes, boundary conditions, and unusual situations.

**⚠️ BRIEF FORMAT**: State the situation and expected behavior. Do NOT include implementation details, error handling code, or retry logic specifics.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ 10-15 edge cases covering main scenarios
- ✅ Each edge case in format "EC-N: [Situation] → [Expected behavior]"
- ✅ Each edge case is 2-3 lines (not 15+ lines with code)
- ✅ Failure scenarios covered (API timeouts, service outages, network errors)
- ✅ Boundary conditions covered (empty data, maximum limits, null values)
- ✅ Concurrency issues covered (simultaneous updates, overlapping jobs)
- ✅ Data quality issues covered (invalid input, malformed data, type mismatches)
- ✅ Edge cases are realistic (not theoretical "what if aliens attack?")

**This section is INCOMPLETE if:**
- ❌ Fewer than 10 edge cases (insufficient coverage)
- ❌ Edge cases include detailed error handling code or retry logic
- ❌ Edge cases exceed 3 lines (too detailed, implementation-focused)
- ❌ Only happy path scenarios (no failure modes documented)
- ❌ Edge cases are too general ("handle errors appropriately")
- ❌ Missing critical scenarios (e.g., external API failure not covered)
- ❌ Edge cases include exception class hierarchies or logging details
- ❌ Vague expected behavior ("do the right thing" instead of specific action)

### Format (REQUIRED):

**EC-[N]**: [Situation] → [Expected behavior]

### What to include:

**Failure Scenarios** - External dependencies fail:
- API timeouts, service outages, network errors

**Boundary Conditions** - Empty or extreme data:
- No matching records, maximum limits reached, null values

**Concurrency Issues** - Race conditions or conflicts:
- Simultaneous updates, overlapping jobs

**Data Quality Issues** - Invalid or malformed data:
- Missing required fields, type mismatches

### What to Include (Requirements Focus):
✅ Situation description (what happens)
✅ Expected behavior (what system does)
✅ 10-15 edge cases covering main scenarios
✅ 2-3 lines per edge case
✅ Failure modes and boundary conditions
✅ Concurrency and data quality issues

### What to Exclude (Implementation Details):
❌ Complete error handling code
❌ Retry logic specifics (exponential backoff algorithms)
❌ Exception class hierarchies
❌ Logging implementation details
❌ Circuit breaker configurations
❌ Detailed recovery procedures

### Level of Detail (Example):

**Good** (requirements-focused):
```
EC-1: SES API timeout → Retry 3x with backoff, mark failed if all attempts fail, alert admin
EC-2: No matching articles for user's tags → Skip user this cycle, log INFO, don't increment schedule
EC-3: User changes interval during processing → Lock row, update takes effect next cycle
EC-4: Article URL returns 404 → Exclude from digest, log WARNING, mark article inactive
EC-5: Email template rendering fails → Use plain text fallback, alert admin
EC-6: Database connection lost → Pause job, retry connection 5x, fail job if persistent
```

**Too detailed** (implementation-focused):
```
EC-1: SES API Timeout Handling
When the AWS SES API times out during email sending:
1. Catch the boto3.exceptions.ReadTimeoutError exception
2. Implement exponential backoff: retry after 1s, 2s, 4s
3. Log each retry attempt with timestamp and error details
4. After 3 failed attempts, mark email as failed in database
5. Update email_queue table: SET status='failed', error_message=...
6. Trigger CloudWatch alarm if failure rate exceeds 5%
7. Send notification to admin via SNS topic
```

---

### Examples

❌ **TOO MUCH** (Implementation details and code):
```
EC-1: SES API Timeout Handling
When the AWS SES API times out during email sending:
1. Catch the boto3.exceptions.ReadTimeoutError exception
2. Implement exponential backoff: retry after 1s, 2s, 4s
3. Log each retry attempt with timestamp and error details
4. After 3 failed attempts, mark email as failed in database
5. Update email_queue table: SET status='failed', error_message=...
6. Trigger CloudWatch alarm if failure rate exceeds 5%
7. Send notification to admin via SNS topic
```

✅ **JUST RIGHT** (Situation → behavior, 2-3 lines):
```
**EC-1**: SES API timeout → Retry 3x with backoff, mark failed if all attempts fail, alert admin
**EC-2**: No matching articles for user's tags → Skip user this cycle, log INFO, don't increment schedule
**EC-3**: User changes interval during processing → Lock row, update takes effect next cycle
**EC-4**: Article URL returns 404 → Exclude from digest, log WARNING, mark article inactive
**EC-5**: Email template rendering fails → Use plain text fallback, alert admin
**EC-6**: Database connection lost → Pause job, retry connection 5x, fail job if persistent
```

---

## Section 8: Technology Constraints

**Purpose**: Document the required technologies and constraints (the **WHAT**, not the *why*).

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ Required language and version specified (e.g., "Python 3.11+")
- ✅ Required database and version specified (e.g., "PostgreSQL 15+")
- ✅ Required external services/APIs listed (e.g., "AWS SES for email")
- ✅ Required libraries with version constraints (e.g., "celery>=5.3.0")
- ✅ Deployment constraints clear (e.g., "Must run as Docker container")
- ✅ Platform constraints stated (e.g., "AWS ECS", "Linux only")
- ✅ Constraints are requirements, not preferences

**This section is INCOMPLETE if:**
- ❌ Technology choices explained (WHY instead of WHAT)
- ❌ Includes comparison matrices or evaluation criteria
- ❌ Alternative options listed (should only state requirements, not alternatives)
- ❌ Missing version constraints ("Python" instead of "Python 3.11+")
- ❌ Includes detailed library configuration (state library, not config)
- ❌ Performance benchmarks comparing technologies
- ❌ Team skill assessments or organizational preferences
- ❌ Vague constraints ("modern database" instead of specific requirement)

### What to include:

**Required Technologies**:
*   Primary technologies that MUST be used (e.g., "Language: Python 3.11+", "Database: PostgreSQL 15+").

**External Dependencies**:
*   Required external services or libraries (e.g., "Requires access to the Stripe API v3," "Must use the `requests` library v2.28+").

**Constraints**:
*   Things the system MUST or MUST NOT do (e.g., "Must be deployable as a Docker container," "Cannot write to the local filesystem").

### What to Include (Requirements Focus):
✅ Required language and version
✅ Required database and version
✅ Required external services/APIs
✅ Required libraries (with version constraints)
✅ Deployment constraints (Docker, serverless, etc.)
✅ Platform constraints (cloud provider, OS)

### What to Exclude (Implementation Details):
❌ Technology comparison matrices
❌ Why technology was chosen (evaluation criteria)
❌ Alternative options considered
❌ Detailed library configuration
❌ Performance benchmarks comparing options
❌ Team skill assessments

### Level of Detail (Example):

**Good** (requirements-focused):
```
Language: Python 3.11+
Database: PostgreSQL 15+
External Services: AWS SES for email delivery
Required Libraries:
- celery>=5.3.0 (job scheduling)
- psycopg2>=2.9.0 (database driver)

Constraints:
- Must be deployable as Docker container
- Cannot write to local filesystem (use S3 for storage)
- Must run on AWS ECS
```

**Too detailed** (implementation-focused):
```
Language: Python 3.11+ (chosen over Node.js and Go)
Evaluation: Python scored 8/10 (Node.js 6/10, Go 7/10)
Criteria: Team expertise (5 Python devs, 2 Node devs), library ecosystem, AI integration

Database: PostgreSQL 15+ (chosen over MySQL and MongoDB)
Comparison matrix:
| Feature | PostgreSQL | MySQL | MongoDB |
|---------|-----------|-------|---------|
| JSON support | Native | Limited | Native |
| ACID | Full | Full | Eventual |
| Performance | 10k qps | 8k qps | 15k qps |
Benchmark: pgbench results show 9,847 TPS on m5.xlarge

External Services: AWS SES (evaluated vs SendGrid, Mailgun)
Cost analysis: SES $0.10/1000 emails, SendGrid $0.85/1000
```

---

## Section 9: Testing Strategy (approach only, not full test suite)

**Purpose**: Describe the testing APPROACH and targets. Do NOT design the complete test suite.

**⚠️ SIMPLIFIED**: State WHAT to test and target metrics. The implementation team designs specific test cases.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ Unit test approach defined (what modules/functions to test)
- ✅ Integration test approach defined (what workflows to test end-to-end)
- ✅ Performance test approach defined (what operations to test under load)
- ✅ Acceptance test approach defined (how to validate scenarios from Section 4)
- ✅ Coverage targets specified (percentage or scope, e.g., ">80% line coverage")
- ✅ What to test stated, not HOW to test (no specific test code)
- ✅ Success criteria for test suite defined

**This section is INCOMPLETE if:**
- ❌ Includes complete test suite with individual test names
- ❌ Includes specific test code or pseudo-code
- ❌ Test framework configuration details (Jest config, pytest fixtures)
- ❌ Mocking strategies or stub implementations
- ❌ CI/CD pipeline configuration
- ❌ Coverage targets missing or vague ("good coverage")
- ❌ No mention of performance or acceptance testing (only unit tests)
- ❌ Test data generation scripts or fixtures

### What to include:

**Unit Tests**:
*   What key modules/functions require unit tests (not specific test cases)
*   Target coverage (e.g., ">80% line coverage for business logic")

**Integration Tests**:
*   What workflows to test end-to-end (e.g., "User signup through first digest delivery")
*   What external integrations to test (e.g., "SES email delivery, database transactions")

**Load/Performance Tests**:
*   What operations to test under load (reference Section 5 targets)
*   Expected scale (e.g., "1000 concurrent digest generations")

**Acceptance Tests**:
*   How to validate Acceptance Scenarios from Section 4
*   Success criteria (e.g., "All scenarios pass in staging environment")

### What to Include (Requirements Focus):
✅ Testing approach for each layer (unit, integration, acceptance)
✅ Coverage targets (percentage or scope)
✅ What to test (modules, workflows, integrations)
✅ Performance test targets (from Section 5)
✅ Success criteria for test suite
✅ Acceptance scenario validation approach

### What to Exclude (Implementation Details):
❌ Complete test suite with individual test names
❌ Specific test code or pseudo-code
❌ Test framework configuration (Jest config, pytest fixtures)
❌ Mocking strategies or stub implementations
❌ CI/CD pipeline configuration
❌ Test data generation scripts

### Level of Detail (Example):

**Good** (requirements-focused):
```
Unit Tests:
- Article matching algorithm
- Email template rendering
- Content ranking logic
- Target: >80% line coverage for business logic

Integration Tests:
- End-to-end: User signup → preference setting → first digest delivery
- External: SES email delivery, PostgreSQL transactions
- Target: All critical workflows covered

Performance Tests:
- 500 requests/sec sustained (per Section 5)
- 1000 concurrent digest generations
- Target: Meet all Section 5 performance targets

Acceptance Tests:
- Validate all scenarios from Section 4
- Success: All scenarios pass in staging environment
```

**Too detailed** (implementation-focused):
```
Unit Tests (Jest framework):
- describe('ArticleMatcher', () => {
    test('should match articles by tag', async () => { ... })
    test('should handle empty tag array', async () => { ... })
    test('should respect date filters', async () => { ... })
  })
- Mock implementation: jest.mock('../services/database')
- Fixtures: __fixtures__/articles.json (127 test records)
- Coverage: nyc --reporter=html --reporter=text
- CI: Run on every PR via GitHub Actions workflow

Integration Tests (Supertest + testcontainers):
- beforeAll(): Start PostgreSQL container, seed database
- Test 1: POST /signup → GET /preferences → Celery job triggers → SES sends email
- Test 2: PUT /preferences → Immediate reschedule → Next digest uses new tags
- Cleanup: afterAll() tears down containers, cleans temp files
```

---

### What NOT to include:
- Detailed test case designs
- Specific test code or pseudo-code
- Complete test suite breakdown with individual test names
- Mocking strategies or test infrastructure details

---

## Section 10: Open Questions and Assumptions

**Purpose**: Document remaining unknowns and assumptions made during PRD creation.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ All open questions listed with resolution path
- ✅ All assumptions documented with rationale
- ✅ Assumptions categorized by type (business logic, integration, technical)
- ✅ Each assumption explains why it was made and impact if wrong
- ✅ Owner identified for resolving each open question
- ✅ Priority assigned to questions (critical/important/nice-to-have)
- ✅ Validation plan for assumptions (how/when to verify)

**This section is INCOMPLETE if:**
- ❌ Open questions without resolution path or owner
- ❌ Assumptions made but not documented (hidden assumptions are dangerous)
- ❌ Assumptions without rationale (why was this assumption necessary?)
- ❌ No priority on open questions (which ones block implementation?)
- ❌ Assumptions without impact analysis (what if assumption is wrong?)
- ❌ No validation plan (how will assumptions be verified?)
- ❌ Questions that should have been answered during research still open
- ❌ Section empty when assumptions were clearly made (dishonest documentation)

---

## Section 11: Success Criteria

**Purpose**: Define measurable completion criteria for the entire module.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ User-facing metrics with target values (completion rates, satisfaction scores)
- ✅ Technical metrics with target values (error rates, response times, uptime)
- ✅ Measurement methods specified for each metric
- ✅ Completion checklist referencing other sections
- ✅ Launch readiness criteria clear (what must be true to ship?)
- ✅ MVP success definition specific and measurable
- ✅ All metrics align with Section 1 goals and Section 5 performance targets

**This section is INCOMPLETE if:**
- ❌ Metrics without target values ("improve completion rate" vs ">90%")
- ❌ Vague measurement methods ("we'll track it somehow")
- ❌ No user-facing success metrics (only technical metrics)
- ❌ No technical success metrics (only business metrics)
- ❌ Completion checklist missing or incomplete
- ❌ Metrics don't align with earlier sections (inconsistent targets)
- ❌ Includes specific monitoring tools/dashboards (state WHAT to measure, not HOW)
- ❌ No definition of what "done" means for this module

### User-Facing Success

**Metrics with Target Values**:
*   [Metric 1]: [Target value with units]
    - Example: "User signup completion rate: >90%"
*   [Metric 2]: [Target value with units]
    - Example: "Digest open rate: >25%"

**Measurement Method**:
*   How will these metrics be tracked? (e.g., "Analytics dashboard, weekly reports")

### Technical Success

**Metrics with Target Values**:
*   [Metric 1]: [Target value with units]
    - Example: "API error rate: <0.1%"
*   [Metric 2]: [Target value with units]
    - Example: "P95 response time: <200ms"
*   [Metric 3]: [Target value with units]
    - Example: "System uptime: >99.9%"

**Measurement Method**:
*   How will these metrics be monitored? (e.g., "CloudWatch dashboards, PagerDuty alerts")

### Completion Criteria

The module is considered DONE when:
*   [ ] All user stories from Section 2 implemented and demonstrated
*   [ ] All acceptance scenarios from Section 4 pass in staging
*   [ ] All performance targets from Section 5 validated under load
*   [ ] All edge cases from Section 7 have defined behavior
*   [ ] Testing strategy from Section 9 executed successfully
*   [ ] Documentation complete (API docs, runbooks, user guides)
*   [ ] Code reviewed and merged to main branch
*   [ ] Deployed to production and monitored for 48 hours

### What to Include (Requirements Focus):
✅ Quantified user-facing metrics (completion rates, satisfaction scores)
✅ Quantified technical metrics (error rates, response times, uptime)
✅ Measurement methods for each metric
✅ Completion checklist (from other sections)
✅ Launch readiness criteria
✅ MVP success definition

### What to Exclude (Implementation Details):
❌ Specific measurement tools (Datadog vs New Relic)
❌ Dashboard JSON configurations
❌ Alert threshold tuning details
❌ Monitoring infrastructure setup
❌ Analytics implementation code
❌ Metric collection pipeline architecture

### Level of Detail (Example):

**Good** (requirements-focused):
```
User-Facing Success:
- User signup completion: >90%
- Digest open rate: >25%
- User retention (30 days): >60%
Measurement: Analytics dashboard, weekly reports

Technical Success:
- API error rate: <0.1%
- P95 response time: <200ms
- System uptime: >99.9%
Measurement: Monitoring dashboard, automated alerts

Completion Criteria:
- All user stories implemented
- All acceptance scenarios pass
- All performance targets met
- 48 hours production monitoring passed
```

**Too detailed** (implementation-focused):
```
User-Facing Success:
- User signup completion: >90% (tracked via Google Analytics 4)
  - Event: signup_complete (custom dimension: source_channel)
  - Dashboard: https://analytics.google.com/dashboard/xyz123
  - BigQuery export: daily at 3 AM UTC
  - Retention analysis: Segment.io cohort builder
- Digest open rate: >25% (AWS SES open tracking + Pixel)
  - Implementation: 1x1 transparent GIF embedded in email
  - Tracking URL: https://tracker.example.com/open?id={user_id}
  - Storage: Redshift table email_events with 90-day TTL

Technical Success:
- API error rate: <0.1% (Datadog APM + custom instrumentation)
  - Metric: aws.apigateway.5xxError / aws.apigateway.count
  - Alert: PagerDuty P2 if error rate >0.5% for 5 minutes
  - Dashboard: Datadog screenboard ID 1234567
```

---

## Validation Checklist

Before submitting this PRD to SpecKit, verify:

### Completeness
- [ ] All 11 sections are complete (Sections 1-9, 11; Section 10 is reserved).
- [ ] Module information (name, version, owners) is filled in.
- [ ] The "Success Criteria" section (Section 11) is filled out.
- [ ] Target length achieved (600-800 lines for comprehensive specs, 300-500 for simpler modules).
- [ ] No [NEEDS CLARIFICATION] markers remain.

### Quality
- [ ] All requirements are specific and testable.
- [ ] All performance targets are quantified with numbers.
- [ ] All technology choices are constraints (WHAT not WHY).
- [ ] Data model is complete with types and relationships.
- [ ] Acceptance scenarios are brief (15-20 lines each) and focus on observable behavior.
- [ ] Edge cases use EC-N format (2-3 lines each, situation → behavior).
- [ ] Implementation phases are high-level milestones without time estimates.
- [ ] Testing strategy describes approach, not detailed test cases.

### Consistency
- [ ] No contradictions between sections.
- [ ] User stories align with acceptance scenarios.
- [ ] Performance targets align with scale requirements.
- [ ] Testing strategy covers all critical scenarios.
- [ ] Success criteria (Section 11) aligns with user stories and acceptance scenarios.

### Readiness
- [ ] Document reviewed by module owner.
- [ ] Technical feasibility validated.
- [ ] Dependencies identified and understood.
- [ ] Document avoids over-specification (no SQL in scenarios, no code in edge cases, no detailed test suites).

### What to Include (Requirements Focus):
✅ All sections complete and substantive
✅ All checklists filled with concrete verification
✅ Cross-section consistency verified
✅ Requirements-focused throughout (WHAT not HOW)
✅ No placeholders or TBD markers
✅ Module owner sign-off

### What to Exclude (Implementation Details):
❌ Premature validation of implementation approach
❌ Technology evaluation details
❌ Team capacity or resource planning
❌ Project management artifacts
❌ Cost estimates or budgets
❌ Stakeholder approval workflows

### Level of Detail (Example):

**Good** (requirements-focused checklist):
```
Completeness:
- All 10 sections filled (Section 10 is placeholder)
- 625 lines total (within 600-800 target)
- No TBD or [NEEDS CLARIFICATION] markers
- Module: Publishing, Owner: Backend team

Quality:
- All 7 user stories have quantified acceptance criteria
- All 5 acceptance scenarios use Given/When/Then
- 12 edge cases in EC-N format (2-3 lines each)
- Performance targets: All have numbers and units

Consistency:
- User stories US-2, US-3, US-5 map to Scenarios 1, 2, 3
- Performance targets reference scale from Problem Statement
- Testing strategy covers all acceptance scenarios
```

**Too detailed** (implementation-focused):
```
Not applicable - validation checklist should be quick yes/no checks,
not detailed implementation validation. Save implementation validation
for Phase 4 (WO-4) quality comparison against case study.
```