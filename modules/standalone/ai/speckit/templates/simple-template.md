# Module Specification - Starter Template

<!--
PURPOSE: This is a human-friendly template for creating initial module specifications.
TARGET OUTPUT: 300-500 lines when filled out completely.
NEXT STEP: This starter spec will be expanded by AI to comprehensive format (600-800 lines).
MAPPING: Each section maps 1:1 to comprehensive template sections for AI expansion.
-->

---

## Section 1: Core Problem
**Target when filled: 2-3 paragraphs per question (50-100 lines total)**

### What problem does this module solve?

[Guidance: Describe the current situation and what's broken or missing. Write 2-3 paragraphs explaining what people are doing now, why that's painful, and what will improve when this module exists.]

**Example 1 - Data Validation Module:**
```
Right now, our system accepts data from multiple sources without validation.
Users submit forms, APIs push data, and batch imports run nightly. We discover
data quality issues days or weeks later when reports break or downstream
systems fail. Support teams spend 10-15 hours weekly fixing corrupted records.

This module will validate all incoming data at entry points. It will check
format, completeness, and business rules before accepting data. Invalid data
gets rejected with clear error messages, so users can fix issues immediately.

Success means zero corrupted records reaching the database and support time
for data fixes dropping from 15 hours to under 2 hours weekly.
```

**Example 2 - User Dashboard Module:**
```
Currently, users must navigate through 5-7 different pages to get their daily
work overview. They check emails for notifications, open reports in separate
tools, and manually track their task progress in spreadsheets. This scattered
approach wastes 30-45 minutes daily per user across our 200-person team.

This module creates a single dashboard showing all relevant information:
tasks, notifications, key metrics, and recent activity. Users see everything
they need in one place when they log in each morning.

Success means users spend under 5 minutes getting oriented each day, and
task completion rates improve because nothing falls through the cracks.
```

**Your answer:**
[Write your problem description here - aim for 2-3 solid paragraphs]

### Who will use this module?

[Guidance: Identify the primary users and estimate how many people or how often they'll use it. Be specific about user types.]

**Example:**
```
Primary users: Customer support team (12 people) processing 50-80 tickets daily
Secondary users: Product managers (4 people) reviewing support trends weekly
Scale: 400-600 transactions per day, 2000-3000 per week
```

**Your answer:**
[Describe your users and usage scale here]

### What does success look like?

[Guidance: List 3-5 measurable goals with actual numbers. Avoid vague terms like "better" or "improved" - use percentages, time savings, error reductions, etc.]

**Example:**
```
1. Process time drops from 8 minutes to under 2 minutes per transaction
2. Error rate decreases from 12% to under 3%
3. User satisfaction score rises from 3.2/5 to above 4.0/5
4. System handles 2x current volume (1000+ daily transactions) without slowdown
5. New users become productive within 30 minutes (currently takes 4 hours)
```

**Your answer:**
1. [Measurable goal with number]
2. [Measurable goal with number]
3. [Measurable goal with number]
4. [Measurable goal with number]
5. [Measurable goal with number]

---

## Section 2: User Stories
**Target when filled: 3-5 complete stories (40-80 lines total)**

[Guidance: Write one story for each major thing users will do with this module. Each story needs four parts: Who, Needs, Why, and Success. The Success criteria MUST include a measurable number or observable outcome.]

### Story 1: [Give it a short, descriptive title]

- **Who:** [Specific user type - be more specific than "user" or "admin"]
- **Needs:** [What action they need to perform - use active verbs]
- **Why:** [What business benefit or problem resolution this provides]
- **Success:** [How you know it worked - include a measurable outcome!]

**Example - Story 1: Quick Data Validation**
- **Who:** Support agent handling customer data updates
- **Needs:** Submit customer address changes and get immediate validation
- **Why:** Prevents incorrect addresses from entering the system and causing failed deliveries
- **Success:** Agent receives pass/fail response within 2 seconds, with specific error messages for any invalid fields. Zero invalid addresses reach the database.

**Example - Story 2: Batch Import Review**
- **Who:** Data operations manager running nightly imports
- **Needs:** Upload CSV file and see validation results before committing
- **Why:** Catches data quality issues before they corrupt the production database
- **Success:** Manager sees validation report within 30 seconds for files up to 10,000 rows, showing exactly which rows have issues and why. Import proceeds only if error rate is under 1%.

**Your Story 1:**
- **Who:**
- **Needs:**
- **Why:**
- **Success:**

### Story 2: [Title]

**Your Story 2:**
- **Who:**
- **Needs:**
- **Why:**
- **Success:**

### Story 3: [Title]

**Your Story 3:**
- **Who:**
- **Needs:**
- **Why:**
- **Success:**

### Story 4: [Title - OPTIONAL]

**Your Story 4 (if needed):**
- **Who:**
- **Needs:**
- **Why:**
- **Success:**

### Story 5: [Title - OPTIONAL]

**Your Story 5 (if needed):**
- **Who:**
- **Needs:**
- **Why:**
- **Success:**

---

## Section 3: Data Model
**Target when filled: List 4-8 main entities (30-60 lines total)**

[Guidance: List the main "things" your module will store. For each thing, write what information it holds and why you need it. Don't worry about database details like primary keys or indexes - just focus on what data matters and why.]

### What data does this module store?

**Example - Thing 1: Validation Rule**
- **Stores:** Rule name, field name, validation type (format/range/required), expected pattern or value, error message
- **Why:** Defines how to check each data field. System reads these rules to know what's valid and what error message to show users when validation fails.

**Example - Thing 2: Validation Result**
- **Stores:** Timestamp, data source, field name, submitted value, pass/fail status, error message, user who submitted
- **Why:** Creates audit trail of all validation attempts. Used for debugging data issues and generating reports on data quality trends.

**Your Thing 1: [Entity name]**
- **Stores:** [List the key information fields]
- **Why:** [Explain what this data is used for]

**Your Thing 2: [Entity name]**
- **Stores:**
- **Why:**

**Your Thing 3: [Entity name]**
- **Stores:**
- **Why:**

**Your Thing 4: [Entity name - if needed]**
- **Stores:**
- **Why:**

**Your Thing 5: [Entity name - if needed]**
- **Stores:**
- **Why:**

**Your Thing 6: [Entity name - if needed]**
- **Stores:**
- **Why:**

---

## Section 4: How It Works
**Target when filled: 2-3 workflows with 4-8 steps each (50-80 lines total)**

[Guidance: Describe the main workflows - the sequences of steps that happen when someone uses this module. Focus on the happy path (when everything works correctly). Write 4-8 steps per workflow. Include the expected time for each workflow.]

### Workflow 1: [Name the workflow]

**Example - Workflow 1: Single Field Validation**
1. User submits form with email address "user@example"
2. System checks email field against validation rules
3. System finds rule: "email must contain @ and domain"
4. System detects missing domain after @
5. System returns error: "Email must include domain (e.g., user@example.com)"
6. User sees error message next to email field
7. User corrects to "user@example.com" and resubmits
8. System validates successfully and accepts form

**Your Workflow 1:**
1. [First step]
2. [Next step]
3. [Next step]
4. [Next step]
5. [Next step]
6. [Continue as needed...]

### Workflow 2: [Name the workflow]

**Example - Workflow 2: Batch File Validation**
1. Manager uploads CSV file with 5,000 customer records
2. System reads file and creates validation job
3. System validates each row against all applicable rules (runs in background)
4. System generates validation report: 4,850 passed, 150 failed
5. Manager downloads report showing exactly which rows failed and why
6. Manager reviews failures, corrects source data
7. Manager re-uploads corrected file
8. System validates again: 5,000 passed, 0 failed
9. Manager approves import, data enters production database

**Your Workflow 2:**
1. [First step]
2. [Next step]
3. [Next step]
4. [Next step]
5. [Continue as needed...]

### Workflow 3: [Name the workflow - OPTIONAL]

**Your Workflow 3 (if needed):**
1. [First step]
2. [Continue...]

---

## Section 5: Technical Constraints
**Target when filled: 2-4 items per question (30-50 lines total)**

[Guidance: Identify the technical requirements, dependencies, and integrations. What technologies MUST you use? What does this module need from other systems? What do other systems need from this module?]

### What technology MUST you use?

[Guidance: List required programming languages, frameworks, databases, or tools. Include the reason why each is required.]

**Example:**
```
- PostgreSQL database (company standard, already hosts customer data)
- Python 3.9+ (team expertise, existing validation libraries available)
- REST API (must integrate with 3 existing systems that use REST)
- Redis cache (validation rules must load in under 100ms)
```

**Your answer:**
- [Technology 1] - [Why required]
- [Technology 2] - [Why required]
- [Technology 3] - [Why required]

### What does this module depend on?

[Guidance: List other systems, APIs, or services this module needs to work. Include what data or functionality you need from each.]

**Example:**
```
- User Authentication Service: Need current user ID and permissions for audit trail
- Customer Database: Need read access to customer schema to validate field formats
- Notification Service: Need to send alerts when validation rules are updated
```

**Your answer:**
- [Dependency 1]: [What you need from it]
- [Dependency 2]: [What you need from it]
- [Dependency 3]: [What you need from it]

### What do other modules need from this?

[Guidance: List which other systems will call this module and what they'll use it for.]

**Example:**
```
- Customer Portal: Needs real-time validation API for all form submissions
- Batch Import Service: Needs bulk validation endpoint for nightly imports
- Data Quality Dashboard: Needs validation statistics and trend data
```

**Your answer:**
- [Module 1]: [What it needs from you]
- [Module 2]: [What it needs from you]
- [Module 3]: [What it needs from you]

---

## Section 6: Important Edge Cases
**Target when filled: 5-10 edge cases (30-50 lines total)**

[Guidance: List unusual situations and how the system should handle them. Think about: very large inputs, missing data, system failures, concurrent users, invalid inputs, permission issues. Format: "Situation → Expected behavior"]

**Examples:**
```
EC-1: User submits file with 100,000 rows (10x normal size) → System accepts job, processes in background, sends email when complete (not blocking UI)

EC-2: Validation rule gets updated while validation job is running → Job completes using old rules, shows warning that rules changed, offers re-validation

EC-3: Two admins try to update the same validation rule simultaneously → Second save fails with error "Rule modified by [name] at [time], please refresh and try again"

EC-4: External dependency (Customer Database) is down during validation → System returns clear error "Unable to validate - Customer Database unavailable", queues job for retry

EC-5: User submits data with special characters (emoji, unicode) → System validates correctly using UTF-8 encoding, doesn't corrupt data
```

**Your edge cases:**

**EC-1:** [Situation] → [Expected behavior]

**EC-2:** [Situation] → [Expected behavior]

**EC-3:** [Situation] → [Expected behavior]

**EC-4:** [Situation] → [Expected behavior]

**EC-5:** [Situation] → [Expected behavior]

**EC-6:** [Situation] → [Expected behavior]

**EC-7:** [Situation] → [Expected behavior]

**EC-8:** [Situation] → [Expected behavior]

**EC-9:** [Situation] → [Expected behavior]

**EC-10:** [Situation] → [Expected behavior]

---

## Section 7: MVP Scope
**Target when filled: 4-8 must-haves, 2-5 nice-to-haves (30-50 lines total)**

[Guidance: Divide features into two lists: what you MUST build for the first working version (MVP = Minimum Viable Product), and what can wait until later. Be ruthless - the MVP should be buildable in 2-4 weeks. Check your math at the end.]

### For MVP (2-4 weeks), we MUST have:

[Guidance: List only the features you absolutely cannot launch without. These are features that deliver the core value.]

**Example:**
```
- [ ] Validate single field in real-time (email, phone, zip code formats)
- [ ] Return clear error messages when validation fails
- [ ] Admin interface to view existing validation rules
- [ ] API endpoint for form validation (REST)
- [ ] Basic validation rule types: required, format/regex, min/max length
- [ ] Audit log of all validation attempts (for debugging)
```

**Your must-have features:**
- [ ] [Feature 1]
- [ ] [Feature 2]
- [ ] [Feature 3]
- [ ] [Feature 4]
- [ ] [Feature 5]
- [ ] [Feature 6]
- [ ] [Feature 7]
- [ ] [Feature 8]

### Nice to have later (not MVP):

[Guidance: List features that would be great to have but aren't essential for launch. These can be built in version 2.]

**Example:**
```
- [ ] Batch file validation for CSVs
- [ ] Custom validation rule builder (admin creates rules via UI)
- [ ] Validation statistics dashboard
- [ ] Integration with external data quality services
- [ ] Advanced rule types: cross-field validation, conditional rules
```

**Your nice-to-have features:**
- [ ] [Feature 1]
- [ ] [Feature 2]
- [ ] [Feature 3]
- [ ] [Feature 4]
- [ ] [Feature 5]

---

## Section 8: How Will We Test This?
**Target when filled: 2-3 items per category (30-40 lines total)**

[Guidance: Describe your testing approach. What will you test automatically (unit/integration tests)? How will you know the module works correctly in production?]

### Unit tests: What will you test?

[Guidance: List the individual pieces of functionality you'll test in isolation.]

**Example:**
```
- Email format validation (test 10+ valid and invalid formats)
- Required field checking (test empty, null, whitespace-only values)
- Error message generation (verify correct messages for each rule type)
- Validation rule loading from database (test caching, updates)
```

**Your unit tests:**
- [Test category 1]
- [Test category 2]
- [Test category 3]
- [Test category 4]

### Integration tests: What will you test?

[Guidance: List the end-to-end workflows you'll test with real system interactions.]

**Example:**
```
- Complete form submission workflow (submit → validate → return errors → fix → resubmit)
- API endpoint performance (validate response time under 200ms for 95% of requests)
- Database transaction handling (verify audit logs are created correctly)
- Error handling when dependencies are unavailable
```

**Your integration tests:**
- [Test scenario 1]
- [Test scenario 2]
- [Test scenario 3]
- [Test scenario 4]

### Success metrics: How will you measure?

[Guidance: Define the key metrics you'll track in production to know if the module is working well.]

**Example:**
```
- Validation response time (target: 95th percentile under 200ms)
- Error rate (target: under 1% of validations fail due to system errors)
- Data quality improvement (target: invalid records in database drops by 80%)
- User satisfaction (target: support tickets about data errors drop by 60%)
```

**Your success metrics:**
- [Metric 1 with target]
- [Metric 2 with target]
- [Metric 3 with target]
- [Metric 4 with target]

---

## Validation Checklist

[Guidance: Review this checklist before submitting. All items should be checked "Yes".]

- [ ] **Problem statement is clear:** Can someone unfamiliar with this module understand what it does and why it matters?
- [ ] **3-5 user stories with measurable success:** Each story has Who/Needs/Why/Success, and Success includes a number
- [ ] **Data model lists main entities:** Identified 4-8 main things to store with clear purpose for each
- [ ] **2-3 workflows showing happy paths:** Each workflow has 4-8 steps and realistic time expectations
- [ ] **Technology constraints identified:** Listed required tech, dependencies, and what other modules need
- [ ] **5-10 edge cases listed:** Covered unusual situations with clear expected behaviors
- [ ] **MVP scope is realistic:** Must-have list is buildable in 2-4 weeks (6-8 features max)
- [ ] **Testing approach defined:** Have plan for unit tests, integration tests, and production metrics
- [ ] **Document is 300-500 lines total:** Not too short (missing details) or too long (scope creep)

### Final Word Count Check:
- **Current line count:** [Run `wc -l` on this file]
- **Target range:** 300-500 lines
- **Status:** [Within range / Too short / Too long]

---

## Metadata

**Template Version:** 1.0
**Created:** 2025-10-09
**Purpose:** Human-friendly starter template for module specifications
**Next Step:** AI expansion to comprehensive format (600-800 lines)
**Mapping:** Direct 1:1 mapping to comprehensive template sections

**Section Mapping to Comprehensive Template:**
- Section 1 (Core Problem) → Problem Statement + Success Criteria
- Section 2 (User Stories) → User Stories & Scenarios
- Section 3 (Data Model) → Data Model
- Section 4 (How It Works) → Core Workflows
- Section 5 (Technical Constraints) → Technical Requirements + Dependencies
- Section 6 (Important Edge Cases) → Edge Cases & Error Handling
- Section 7 (MVP Scope) → MVP Scope + Feature Prioritization
- Section 8 (How Will We Test This) → Testing Strategy + Success Metrics
