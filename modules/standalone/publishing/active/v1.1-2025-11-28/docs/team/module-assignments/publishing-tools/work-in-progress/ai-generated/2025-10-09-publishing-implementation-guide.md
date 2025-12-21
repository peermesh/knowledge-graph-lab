# Publishing Module: Implementation Guide

**Purpose:** Actionable implementation roadmap for Publishing module

**Derived From:** 2025-10-09-publishing-decisions-agreements.md (Document 1)

**Created:** 2025-10-09

**Status:** Draft - Awaiting Blocker Resolution

---

## Quick Start

### What You're Building

Email publishing module that takes AI-generated content and distributes it via customizable templates, with full tracking and legal compliance.

**Core Functionality:**

- Email publishing with AWS SES integration ✓ Extracted (from Doc 1 MVP Features)
- Two-template system (plain text + formatted) ✓ Extracted (from Doc 1 Technical Decision #7)
- Unsubscribe flow with legal compliance ✓ Extracted (from Doc 1 MVP Features)
- Dispatch logging and error tracking ✓ Extracted (from Doc 1 MVP Features)
- Event-triggered publishing (doPublish() method) ✓ Extracted (from Doc 1 MVP Features)

**Out of Scope (this phase):**

- Blog publishing integration ⚠️ Unclear (from Doc 1 - mentioned but not confirmed MVP)
- Push notifications 🟡 Post-MVP (from Doc 1 - explicitly deferred)
- Text message delivery 🟡 Post-MVP (from Doc 1 - explicitly deferred)
- Social sharing/subscribe features ⚠️ Unclear (from Doc 1 - mentioned but not confirmed)
- Admin dashboard ⚠️ Unclear (from Doc 1 - research needed)

### Time Estimate

**Total Estimated Time:** 40-60 hours

**Phase Breakdown:**

- Phase 0 (Foundation & Learning): 6-8 hours
- Phase 1 (Core Pipeline): 12-16 hours
- Phase 2 (Email Publishing): 10-14 hours
- Phase 3 (Template System): 8-10 hours
- Phase 4 (Integration & Testing): 4-6 hours

**Note:** Estimates assume Docker familiarity, blockers resolved before Phase 1 start, AWS account access available.

### Before You Start

### Pre-Implementation Checklist

**Environment Setup:**

- [ ] Docker installed and running (`docker --version`)
- [ ] Node.js installed (v16+ recommended) (`node --version`)
- [ ] Code editor configured (VS Code or preferred IDE)
- [ ] Git configured (`git config --global user.name`)
- [ ] Project repository cloned locally
- [ ] Access to: AWS account, test email accounts, database instance (if available)

**Document Review:**

- [ ] Document 1 (Decisions & Agreements) read completely
- [ ] All Technical Decisions understood (especially Docker, file-based assembly, SES, templates)
- [ ] All Integration Contracts reviewed (Core, AI, Database, Frontend)
- [ ] All Open Questions noted (especially 🔴 Blockers #1, #3, #5, #6)
- [ ] MVP Features scope clear (know what's in/out)
- [ ] Section 8: "Using This Document" reviewed (understand resolution workflow)

**Blocker Resolution Status:**

- [ ] Open Question #1 (AI article schema): [✅ Resolved / ⚠️ In Progress / ❌ Not Started]
- [ ] Open Question #3 (doPublish() trigger): [✅ Resolved / ⚠️ In Progress / ❌ Not Started]
- [ ] Open Question #5 (Auth between modules): [✅ Resolved / ⚠️ In Progress / ❌ Not Started]
- [ ] Open Question #6 (Database query API): [✅ Resolved / ⚠️ In Progress / ❌ Not Started]
- [ ] Frontend request data schema: [✅ Resolved / ⚠️ In Progress / ❌ Not Started]

**If any blocker is ❌ Not Started or ⚠️ In Progress:**

→ **STOP:** Resolve blockers before proceeding to Phase 1

→ **OK to start:** Phase 0 (Foundation & Learning) and Phase 3 (Template System) only

**Team Alignment:**

- [ ] Kickoff meeting held (roles, timeline, communication channels)
- [ ] Technical lead assigned for Publishing module
- [ ] Code review process defined
- [ ] Deployment pipeline access confirmed (or plan in place)
- [ ] Integration points identified: contacts for AI module, Backend, Frontend, Database teams

**Communication Setup:**

- [ ] Slack/Discord channel for Publishing module
- [ ] Access to: AI module team, Backend team, Frontend team, Database team
- [ ] Escalation path defined (who to ask when stuck)
- [ ] Weekly sync meeting scheduled (if applicable)

**AWS SES Prerequisites (for Phase 0):**

- [ ] AWS account credentials available
- [ ] Permission to create SES resources
- [ ] Test email domain/address identified
- [ ] Budget approved for SES usage (if required)

**Ready to Begin:**

- [ ] All above items checked
- [ ] Phase 0 can start immediately (no blockers)
- [ ] Phase 1+ awaiting blocker resolution per Implementation Readiness Matrix

### Critical Path Overview

**Dependency Flow:**

1. **Phase 0: Foundation** → Docker setup, learn email standards, project structure
2. **Phase 1: Core Pipeline** → Request ingestion, file assembly, basic dispatch (depends on Phase 0)
3. **Phase 2: Email Publishing** → SES integration, error handling (depends on Phase 1)
4. **Phase 3: Template System** → Two templates, shortcodes, rendering (depends on Phase 1)
5. **Phase 4: Integration** → Connect to AI/DB modules, end-to-end testing (depends on all previous)

**Blockers to Watch:**

- 🔴 AI article schema - Blocks Phase 1 (file assembly needs schema) - Doc 1 Open Question #1
- 🔴 Database query API - Blocks Phase 1 & 4 (content retrieval, integration) - Doc 1 Open Question #6
- 🔴 doPublish() trigger mechanism - Blocks Phase 1 (pipeline entry point) - Doc 1 Open Question #3
- 🔴 Frontend request data schema - Blocks Phase 1 & 4 (user preferences, integration) - Doc 1 Gap

---

## Implementation Readiness Matrix

**Purpose:** Quick scan of which phases can start vs. blocked

| Phase | Can Start? | Blockers | Dependencies | Confidence |
|-------|------------|----------|--------------|------------|
| **Phase 0: Foundation** | ✅ Yes | None | None | **High** - Mostly standard setup and research |
| **Phase 1: Core Pipeline** | ❌ No | - AI schema (OQ #1)<br>- doPublish() spec (OQ #3)<br>- DB API (OQ #6)<br>- Frontend schema (Gap) | Phase 0 | **Low** - 4 critical blockers unresolved |
| **Phase 2: Email Publishing** | ⚠️ Partial | - SES setup (dependency)<br>- Some error handling details (OQ #11) | Phase 0, Phase 1 | **Medium** - SES can be configured, but depends on Phase 1 |
| **Phase 3: Template System** | ✅ Yes | None | Phase 0 | **High** - Templating approach confirmed, no blockers |
| **Phase 4: Integration** | ❌ No | - All Phase 1 blockers<br>- Auth mechanism (OQ #5) | All prior phases | **Low** - Cannot integrate until contracts defined |

**Key Takeaways:**

- ✅ **Can start immediately:** Phase 0 (Foundation & Learning), Phase 3 (Template System in parallel)
- ⚠️ **Requires planning:** Phase 2 (Email Publishing) can be partially designed but needs Phase 1 complete
- ❌ **Fully blocked:** Phase 1 (Core Pipeline), Phase 4 (Integration) - resolve Document 1 Open Questions first

**Recommended Sequence:**

1. Start Phase 0 immediately (no blockers)
2. Work on Phase 3 templates in parallel (independent of Phase 1)
3. Resolve all 🔴 blockers (Open Questions #1, #3, #5, #6, Frontend schema)
4. Begin Phase 1 (unblocked)
5. Follow with Phase 2, then Phase 4

---

## Phase 0: Foundation & Learning

**Goal:** Set up development environment and understand email publishing standards before implementation

**Time Estimate:** 6-8 hours

**Provenance Summary:**

- ✓ Extracted: 2 tasks (Docker from Tech Decision #1, Research from Critical Quote)
- ⚠️ Inferred: 2 tasks (Project structure, AWS SES setup - standard practice)
- 🔴 Unknown: 0 tasks (no blockers)
- **Total tasks:** 4 (50% extracted, 50% inferred)

**Dependencies:** None

**Blockers:** None - can start immediately

**Confidence:** High - Standard setup and research tasks

---

### P0.1: Docker Environment Setup 🤖 Agent-ready

**What:** Create Docker container structure for publishing module

**Tasks:**

- [ ] Install Docker (if not present) ⚠️ Inferred (standard setup)
- [ ] Create Dockerfile for Node.js environment ✓ Extracted (Docker decision in Doc 1 Tech Decision #1)
- [ ] Set up docker-compose for local development ⚠️ Inferred (standard practice)
- [ ] Create project directory structure ⚠️ Inferred (standard setup)

**Provenance:** Docker containerization from Document 1 Technical Decision #1, setup steps are standard practice

**Could ask agent:** 📋 **Copy-paste ready**

"Create a Dockerfile for a Node.js publishing module that will run as part of a microservices architecture. Include environment variables for AWS SES credentials and database connection. Also create a docker-compose.yml for local development with volume mounts for code."

**Expected output:**

- `Dockerfile` with Node.js base image (node:16-alpine or similar)
- Environment variables: `AWS_SES_ACCESS_KEY`, `AWS_SES_SECRET_KEY`, `DB_CONNECTION_STRING`
- `docker-compose.yml` with service definition, volume mounts for `/src`, environment file reference
- `.env.example` with credential placeholders

**Validation checklist:**

- [ ] Can build Docker image: `docker build -t publishing-module .`
- [ ] Can run locally: `docker-compose up`
- [ ] Environment variables accessible in container (`docker exec <container> env`)
- [ ] Code changes reflect immediately (volume mount working)

**Learning trade-off:** Low (Docker setup is routine, one-time task - agent saves 1-2 hours)

**Time:** 1-2 hours

---

### P0.2: Email Publishing Standards Research 👤 Human-design

**What:** Understand email HTML standards, compliance requirements, and industry best practices

**Learning Objectives:**

- Understand email HTML/CSS limitations (client compatibility)
- Learn legal requirements (CAN-SPAM, GDPR unsubscribe rules)
- Identify minimum vs. enterprise-level features
- Understand AWS SES quotas, limits, bounce handling

**Resources:**

- Email HTML best practices: litmus.com, email on acid
- CAN-SPAM compliance: FTC guidelines
- AWS SES documentation: docs.aws.amazon.com/ses
- Research large-scale email systems: Mailchimp, SendGrid architecture

**Provenance:** ✓ Extracted - Research task explicitly mentioned in Document 1, Critical Quote: "we'll probably need to do some research on what these email publishing tools have in terms of the full suite of things... what's the minimum requirements?"

**Why human:** Requires judgment to synthesize research into project-specific decisions, understand compliance nuances, make architecture trade-offs

**Time:** 3-4 hours

---

### P0.3: Project Structure Creation 🤖 Agent-ready

**What:** Set up code directory structure and initial files

**Tasks:**

- [ ] Create `/src` for application code ⚠️ Inferred
- [ ] Create `/templates` for email templates ✓ Extracted (template system in Doc 1)
- [ ] Create `/temp` for file assembly ✓ Extracted (temp file decision in Doc 1 Tech Decision #3)
- [ ] Create `/logs` for dispatch logging ✓ Extracted (logging in Doc 1)
- [ ] Initialize package.json with dependencies ⚠️ Inferred
- [ ] Create README with setup instructions ⚠️ Inferred

**Provenance:** Directory needs inferred from Document 1 technical decisions (templates, temp files, logs mentioned explicitly)

**Could ask agent:** 📋 **Copy-paste ready**

"Create a Node.js project structure for an email publishing module. Include directories for: email templates, temporary file assembly, dispatch logs. Initialize package.json with dependencies: nodemailer (AWS SES), mustache (templating), and standard utilities. Create a README with setup instructions."

**Expected output:**

- Directory structure: `/src`, `/templates`, `/temp`, `/logs`, `/tests`
- `package.json` with dependencies: `nodemailer`, `@aws-sdk/client-ses`, `mustache`, `dotenv`, dev dependencies: `jest`, `eslint`
- `README.md` with setup instructions (install, configure, run)
- `.gitignore` excluding `node_modules/`, `/temp/*`, `/logs/*`, `.env`

**Validation checklist:**

- [ ] Directory structure created correctly
- [ ] `npm install` runs without errors
- [ ] Dependencies match requirements (check package.json)
- [ ] README instructions are clear and accurate

**Learning trade-off:** Low (boilerplate setup - agent saves 30-45 min)

**Time:** 30-45 min

---

### P0.4: AWS SES Account Setup 👤 Human-design

**What:** Configure AWS Simple Email Service for email dispatch

**Tasks:**

- [ ] Create/access AWS account ⚠️ Inferred
- [ ] Set up SES in appropriate region ⚠️ Inferred
- [ ] Verify sender email domain/address ⚠️ Inferred (SES requirement)
- [ ] Request production access (move out of sandbox) ⚠️ Inferred (SES requirement)
- [ ] Note quotas and limits ⚠️ Inferred
- [ ] Generate SMTP credentials or API keys ⚠️ Inferred

**Provenance:** ✓ Extracted - AWS SES chosen in Document 1 Technical Decision #4, setup steps are standard AWS/SES requirements

**Why human:** Requires AWS account access, security decisions (credential management), understanding quota implications for project scale

**Time:** 1-2 hours

---

## Phase 1: Core Pipeline - Request to Assembly

**Goal:** Build foundational publishing pipeline from trigger to assembled output files

**Time Estimate:** 12-16 hours

**Provenance Summary:**

- ✓ Extracted: 6 tasks (doPublish(), request parsing, content retrieval, file assembly from Doc 1)
- ⚠️ Inferred: 4 tasks (validation, error handling, edge cases - standard practice)
- 🔴 Unknown: 3 tasks (BLOCKED - need OQ #1, #3, #6 resolved)
- **Total tasks:** 13 (46% extracted, 31% inferred, 23% blocked)

**Dependencies:**

- Phase 0 complete (environment ready)
- 🔴 BLOCKER MUST RESOLVE: AI article schema defined (Reference: Document 1 Open Question #1)
- 🔴 BLOCKER MUST RESOLVE: doPublish() trigger mechanism specified (Reference: Document 1 Open Question #3)
- 🔴 BLOCKER MUST RESOLVE: Database API defined (Reference: Document 1 Open Question #6)

**Blockers:** 3 critical - cannot start Phase 1 until all resolved

**Confidence:** Low - Multiple unresolved integration contracts

---

### P1.1: Request Ingestion Handler

**What:** Implement doPublish() method that receives trigger and loads user request data

**Tasks:**

- [ ] Create doPublish() entry point method 🔴 BLOCKED (trigger mechanism undefined - Doc 1 Open Question #3)
- [ ] Parse incoming request data (JSON format) ✓ Extracted (JSON format from Doc 1 Tech Decision #2)
- [ ] Implement request validation ⚠️ Inferred (standard input validation)
- [ ] Set request flag to "in-progress" ✓ Extracted (state tracking from Doc 1 Integration Contracts)

**Provenance:**

- doPublish() trigger: Document 1 Integration Contracts (Core Module row) - mechanism described conceptually but implementation TBD
- JSON format: Document 1 Technical Decision #2
- State flags: Document 1 Integration Contracts notes ("in progress", "published")

**Implementation Notes:**

- Request JSON contains: user preferences, topics, frequency, delivery methods (from Doc 1 Integration Contracts)
- State update must persist to database (API TBD - see Doc 1 Open Question #6)
- Interval logic: "do publish method knows the interval that it's going to be called at" - need to handle timing

**Success Criteria:**

- [ ] Method accepts trigger input (format TBD)
- [ ] Successfully parses JSON request data
- [ ] Updates request status to "in-progress"
- [ ] Logs entry in dispatch log

---

### P1.2: Content Retrieval 🔴 BLOCKED

**What:** Query database for AI-generated content matching user tags, filter out previously sent items

**Tasks:**

- [ ] Make API call to database module 🔴 BLOCKED (Reference: Document 1 Open Question #6)
- [ ] Build query: match user tags, exclude sent items ✓ Extracted (logic from Doc 1)
- [ ] Handle empty results (no new content) ⚠️ Inferred (edge case handling)
- [ ] Parse AI article response 🔴 BLOCKED (Reference: Document 1 Open Question #1)

**Provenance:**

- Query logic: Document 1 Integration Contracts (Database row): "request to the other database for any available stuff that matches those tags that isn't in the list of things we've already sent them"
- AI article format: Document 1 Open Question #1 - "markdown file" mentioned but structure undefined

**Implementation Notes:**

- Tracking "already sent" items: mechanism mentioned but not detailed
- Article format: "probably just be like a markdown file" - assume markdown text, but metadata/images unknown

**Blockers:**

- 🔴 Database query API contract undefined (Reference: Document 1 Open Question #6)
- 🔴 AI article schema undefined (Reference: Document 1 Open Question #1)
- **Impact:** Cannot implement until both blockers resolved
- **Resolution needed before:** Phase 1 start

**Success Criteria:**

- [ ] (BLOCKED) Successfully queries database
- [ ] (BLOCKED) Correctly filters previously sent content
- [ ] (BLOCKED) Parses article data into usable format

---

### P1.3: Temporary File Assembly 🤖 Agent-ready

**What:** Copy retrieved articles to temporary folder for email assembly

**Tasks:**

- [ ] Create temporary folder per publish job ✓ Extracted (temp file approach from Doc 1 Tech Decision #3)
- [ ] Copy article files to temp location ⚠️ Inferred (file operations)
- [ ] Organize files by user/request ID ⚠️ Inferred (tracking/audit trail)
- [ ] Implement cleanup on completion/failure ⚠️ Inferred (temp file management)

**Provenance:**

- Temp file approach: Document 1 Technical Decision #3 - "assemble the template, like copy of the template and then we'll copy these chunks of content in after we've formatted them and we'll have this version of what we're about to send locally in a temporary file"
- Memory constraint: Doc 1 Critical Quote - "don't want to do this all in memory because that means that the server has to have a larger amount of RAM"

**Could ask agent:** 📋 **Copy-paste ready**

"Implement a file assembly system that copies AI article files to a temporary folder structure organized by publish job ID. Include cleanup logic to delete temp files after successful dispatch or on failure. Use Node.js fs module with async/await."

**Expected output:**

- Module: `src/fileAssembly.js` with functions: `createTempFolder(jobId)`, `copyArticles(jobId, articles[])`, `cleanup(jobId, success)`
- Temp folder pattern: `/temp/[jobId]/` with article files inside
- Error handling for file I/O failures
- Cleanup function called from Phase 2 dispatch success/failure

**Validation checklist:**

- [ ] Temp folder created with unique ID: `/temp/job-12345/`
- [ ] Articles copied successfully to temp location
- [ ] Cleanup removes folder after success
- [ ] Cleanup removes folder after error
- [ ] No memory leaks (check with multiple runs)

**Implementation Notes:**

- Temp folder location: consider using `/temp/[job-id]/` pattern
- Cleanup timing: after dispatch complete (Phase 2) or on error
- File size considerations: mentioned storage concerns in Doc 1 Gaps

**Learning trade-off:** Low (file operations are routine - agent saves 1-2 hours)

**Success Criteria:**

- [ ] Creates unique temp folder per job
- [ ] Successfully copies article files
- [ ] Cleanup executes on completion
- [ ] Cleanup executes on failure/error

**Time:** 1-2 hours

---

### P1.4: Content Formatting

**What:** Format markdown articles for email (truncation, HTML conversion prep)

**Tasks:**

- [ ] Determine content length and apply truncation ✓ Extracted (truncation logic from Doc 1)
- [ ] Implement "show more" link insertion ✓ Extracted (truncation UX from Doc 1)
- [ ] Format markdown to email-compatible HTML ⚠️ Inferred (email requires HTML)
- [ ] Handle edge cases (very short articles, no content) ⚠️ Inferred

**Provenance:**

- Truncation: Document 1 Open Question #2: "if you've got an article that's hundreds of pages long, you just want the first paragraph or... 200 words or something"
- Show more link: Doc 1 - "then so if something's larger than 200 words, we'll have a click here for more button"
- HTML conversion: Inferred (emails need HTML, markdown mentioned as source)

**Implementation Notes:**

- Truncation limit: ~200 words suggested but NOT finalized (see Doc 1 Open Question #2)
- "Show more" links to dynamically rendered page (Doc 1 Tech Decision #6)
- Email HTML standards: research from P0.2 should inform approach

**Success Criteria:**

- [ ] Articles truncated at configured limit
- [ ] "Show more" links inserted correctly
- [ ] Markdown converted to email-safe HTML
- [ ] Edge cases handled gracefully

---

## Phase 2: Email Publishing - SES Integration

**Goal:** Implement email dispatch using AWS SES with error handling and logging

**Time Estimate:** 10-14 hours

**Provenance Summary:**

- ✓ Extracted: 5 tasks (Template application, SES dispatch, dispatch logging from Doc 1)
- ⚠️ Inferred: 3 tasks (Error handling, email formatting, edge cases - standard practice)
- 🔴 Unknown: 1 task (Error retry logic details - see OQ #11)
- **Total tasks:** 9 (56% extracted, 33% inferred, 11% unknown)

**Dependencies:**

- Phase 1 complete (assembled content ready)
- Phase 0.4 complete (AWS SES configured)

**Blockers:** 1 minor - error handling details (workaround: use standard retry pattern)

**Confidence:** Medium - Core functionality clear, some error handling TBD

---

### P2.1: Email Assembly with Templates

**What:** Apply template to content using shortcode system

**Tasks:**

- [ ] Load template file ✓ Extracted (template system from Doc 1 Tech Decision #5)
- [ ] Replace shortcodes with user data (name, etc.) ✓ Extracted (shortcode system from Doc 1 Tech Decision #5)
- [ ] Insert article content blocks ⚠️ Inferred (template application)
- [ ] Generate final email HTML ⚠️ Inferred

**Provenance:**

- Template system: Document 1 Technical Decision #5 - "templates use shortcodes... insert the user's first name or insert their last name"
- Shortcodes: Doc 1 - "anything that's like custom code or custom text to not be hard coded, right? That's a basic requirement of a templating system"

**Implementation Notes:**

- Two templates required (plain text + formatted) - from Doc 1 Critical Quote about interchangeability
- Shortcodes needed: user first name, last name, article blocks, unsubscribe link (inferred)
- Template location: `/templates/` directory from P0.3

**Success Criteria:**

- [ ] Template loaded successfully
- [ ] Shortcodes replaced with actual data
- [ ] Content inserted into template
- [ ] Valid HTML email generated

---

### P2.2: AWS SES Dispatch 🤖 Agent-ready

**What:** Send email via AWS SES API and capture response

**Tasks:**

- [ ] Initialize SES client with credentials ⚠️ Inferred (AWS SDK standard)
- [ ] Format email for SES API (to, from, subject, body) ⚠️ Inferred
- [ ] Send email via SES ✓ Extracted (SES decision from Doc 1 Tech Decision #4)
- [ ] Capture send response ⚠️ Inferred
- [ ] Handle SES errors (quota, bounce, invalid email) ⚠️ Inferred

**Provenance:**

- SES usage: Document 1 Technical Decision #4 - "SES by Amazon, the simple email service"
- Error responses: Document 1 Gap - "The email one's also got... the potential be bounced back. So that needs to be added to the log"

**Could ask agent:** 📋 **Copy-paste ready**

"Implement AWS SES email sending in Node.js. Use AWS SDK to send HTML emails with error handling for: quota exceeded, bounced emails, invalid addresses. Return detailed response object with message ID and status. Include retry logic for transient failures."

**Expected output:**

- Module: `src/emailDispatch.js` with function: `sendEmail(to, from, subject, htmlBody, textBody)`
- AWS SDK v3 (@aws-sdk/client-ses) integration
- Error handling for: QuotaExceededException, MessageRejected, InvalidParameterValue
- Retry logic: 3 attempts with exponential backoff for transient errors
- Return object: `{ success: boolean, messageId: string, error?: string }`

**Validation checklist:**

- [ ] Successfully sends test email via SES
- [ ] Returns SES message ID in response
- [ ] Handles quota exceeded gracefully (logs error, doesn't crash)
- [ ] Handles invalid email address gracefully
- [ ] Retry logic executes on transient failures
- [ ] All attempts logged to dispatch log

**Implementation Notes:**

- SES credentials: from P0.4 setup (environment variables: AWS_SES_ACCESS_KEY, AWS_SES_SECRET_KEY)
- From address: must be verified in SES (from P0.4)
- Bounce handling: log for now, full handling TBD (Reference: Document 1 Open Question #11)

**Learning trade-off:** Medium (SES integration is learned skill, but agent handles boilerplate - saves 2-3 hours, moderate learning loss)

**Success Criteria:**

- [ ] Successfully sends email via SES
- [ ] Captures message ID from response
- [ ] Handles common errors gracefully
- [ ] Logs all dispatch attempts

**Time:** 2-3 hours

---

### P2.3: Dispatch Logging

**What:** Record all dispatch events to database with full pipeline context

**Tasks:**

- [ ] Create log entry structure ✓ Extracted (dispatch log from Doc 1)
- [ ] Capture: request ID, timestamp, API response, errors ✓ Extracted (from Doc 1)
- [ ] Store dispatch log to database ⚠️ Inferred (persistence)
- [ ] Link log to original request ✓ Extracted (audit trail from Doc 1)

**Provenance:**

- Logging requirement: Document 1 MVP Features - "Dispatch Logging" confirmed in MVP
- Log contents: Document 1 - "That dispatch log will also have the details of the whole pipeline from the moment it was requested, the moment it entered the system... the moment it was processed, what logic was used for processing, what templates were used... when it was sent"
- Per-request logs: Doc 1 - "each log entry is specific to that one request to that one API"

**Implementation Notes:**

- Log must track: entire pipeline (request → process → template → dispatch)
- Include: templates used, processing logic version, SES response
- Future: handle post-dispatch updates (bounces, unsubscribes) - see Doc 1 Gaps

**Success Criteria:**

- [ ] Log entry created for every dispatch
- [ ] Contains all pipeline details
- [ ] Persisted to database
- [ ] Linked to request record

---

## Phase 3: Template System

**Goal:** Create two email templates (plain text + formatted) with shortcode support

**Time Estimate:** 8-10 hours

**Provenance Summary:**

- ✓ Extracted: 4 tasks (Shortcode system, 2 templates from Doc 1 Tech Decision #5, #7)
- ⚠️ Inferred: 2 tasks (Template engine choice, testing - standard practice)
- 🔴 Unknown: 0 tasks (no blockers)
- **Total tasks:** 6 (67% extracted, 33% inferred)

**Dependencies:**

- Phase 0.2 complete (email standards research)
- Phase 1 complete (know content structure - can also work in parallel)

**Blockers:** None - can start independently of Phase 1

**Confidence:** High - Template approach fully defined in Document 1

---

### P3.1: Template Engine Implementation 🤖 Agent-ready

**What:** Build shortcode replacement system for templates

**Tasks:**

- [ ] Choose/implement templating library (Mustache, Handlebars, etc.) ⚠️ Inferred (standard practice)
- [ ] Define shortcode syntax (e.g., {{first_name}}) ⚠️ Inferred
- [ ] Implement shortcode replacement logic ✓ Extracted (shortcode system from Doc 1 Tech Decision #5)
- [ ] Handle missing data gracefully ⚠️ Inferred

**Provenance:**

- Shortcode system: Document 1 Technical Decision #5 - "using shortcodes, which is a way of saying insert the user's first name... anything that's like custom code or custom text to not be hard coded"

**Could ask agent:** 📋 **Copy-paste ready**

"Create a template engine for email publishing that supports shortcodes like {{first_name}}, {{article_content}}, {{unsubscribe_link}}. Use Mustache.js or similar. Include error handling for missing data (fallback to empty or default). Support nested content blocks for article lists."

**Expected output:**

- Module: `src/templateEngine.js` with function: `renderTemplate(templatePath, data)`
- Library: Mustache.js (or Handlebars.js) integration
- Shortcodes supported: `{{first_name}}`, `{{last_name}}`, `{{article_content}}`, `{{unsubscribe_link}}`, `{{#articles}}...{{/articles}}` (loop)
- Error handling: Missing fields default to empty string with warning log
- Template validation function to check for required shortcodes

**Validation checklist:**

- [ ] Template loads from `/templates/` directory
- [ ] Shortcodes replaced correctly with provided data
- [ ] Missing data doesn't crash (defaults to empty/fallback)
- [ ] Nested article blocks render correctly (loop through array)
- [ ] Errors logged for debugging

**Learning trade-off:** Low (templating is common pattern - agent saves 1-2 hours)

**Success Criteria:**

- [ ] Shortcodes correctly replaced
- [ ] Missing data handled
- [ ] Supports nested blocks (article lists)
- [ ] Template errors logged

**Time:** 1-2 hours

---

### P3.2: Plain Text Template 👤 Human-design

**What:** Create simple plain text email template (Template 1 of 2 required)

**Tasks:**

- [ ] Design text layout structure ✓ Extracted (two templates required from Doc 1 Tech Decision #7)
- [ ] Define shortcodes needed ⚠️ Inferred
- [ ] Add unsubscribe section ✓ Extracted (legal requirement from Doc 1 Critical Quote)
- [ ] Test readability ⚠️ Inferred

**Provenance:**

- Two templates required: Document 1 Critical Quote - "I've found if you do something where you have at least two of something that's supposed to be interchangeable, you can check to make sure it really works for more than the one thing"
- Unsubscribe: Document 1 Critical Quote - "to be compliant with law, we should have the unsubscribe button"

**Why human:** Design decisions (layout, tone, readability) require judgment and UX thinking

**Implementation Notes:**

- Shortcodes needed (minimum): user first_name, article blocks, unsubscribe_link
- Structure: greeting, article list, unsubscribe footer
- Content limit per article: ~200 words (see Doc 1 Open Question #2 for final decision)

**Success Criteria:**

- [ ] Template created and saved to `/templates/plain.txt`
- [ ] All required shortcodes included
- [ ] Unsubscribe section compliant
- [ ] Readable and professional

**Time:** 2-3 hours

---

### P3.3: Formatted HTML Template 👤 Human-design

**What:** Create formatted email template with colors, images, styling (Template 2 of 2)

**Tasks:**

- [ ] Design HTML/CSS layout ✓ Extracted (formatted template required from Doc 1)
- [ ] Ensure cross-client compatibility ⚠️ Inferred (email HTML standards from P0.2)
- [ ] Add visual elements (colors, images per description) ✓ Extracted (from Doc 1)
- [ ] Include responsive design ⚠️ Inferred (best practice)
- [ ] Test in multiple email clients ⚠️ Inferred

**Provenance:**

- Two templates with one formatted: Document 1 suggested "fancy with like a customized color scheme and some images that need to go with it and links to at the bottom to the socials or something"
- Visual quality: Document 1 Critical Quote - "where us as humans will have to look at it and make a lot of tweaks and changes to make it look good and look professional. That's where the rubber hits the road"

**Why human:** Visual design, brand consistency, UX quality require human judgment. This is "where the rubber hits the road" per Doc 1 - iterative refinement critical.

**Implementation Notes:**

- Use email HTML standards from P0.2 research
- Test clients: Gmail, Outlook, Apple Mail minimum
- Images: hosting strategy TBD (inline vs. external links)
- Color scheme: choose professional palette
- Expect iteration: plan time for "tweaks and changes to make it look good"

**Success Criteria:**

- [ ] Template created and saved to `/templates/formatted.html`
- [ ] Works in major email clients
- [ ] Visually professional
- [ ] All shortcodes functional
- [ ] Responsive on mobile

**Time:** 4-5 hours

---

## Phase 4: Integration & Testing

**Goal:** Connect all components, integrate with other modules, end-to-end testing

**Time Estimate:** 4-6 hours

**Provenance Summary:**

- ✓ Extracted: 6 tasks (Module integrations, unsubscribe flow, testing from Doc 1)
- ⚠️ Inferred: 3 tasks (Testing scenarios, Docker validation - standard practice)
- 🔴 Unknown: 4 tasks (All blocked - need OQ #1, #3, #5, #6 resolved)
- **Total tasks:** 13 (46% extracted, 23% inferred, 31% blocked)

**Dependencies:**

- All previous phases complete
- 🔴 ALL BLOCKERS RESOLVED (Reference: Document 1 Open Questions #1, #3, #5, #6, and Frontend schema)

**Blockers:** 4 critical - cannot start Phase 4 until all integration contracts defined

**Confidence:** Low - Fully blocked until Document 1 resolutions complete

---

### P4.1: Module Integration 🔴 BLOCKED

**What:** Connect to Core, AI, Database, Frontend modules

**Tasks:**

- [ ] Implement Core module API calls (doPublish trigger) 🔴 BLOCKED (Reference: Document 1 Open Question #3)
- [ ] Implement AI module content fetching 🔴 BLOCKED (Reference: Document 1 Open Questions #1, #6)
- [ ] Implement Database queries 🔴 BLOCKED (Reference: Document 1 Open Question #6)
- [ ] Implement Frontend unsubscribe callback 🔴 BLOCKED (Reference: Document 1 Open Question #7)
- [ ] Add authentication/authorization 🔴 BLOCKED (Reference: Document 1 Open Question #5)

**Provenance:**

- Integration points: Document 1 Integration Contracts section (all rows except SES)
- Blockers: Document 1 Open Questions #1, #3, #5, #6, #7

**Blockers:**

- 🔴 Core doPublish() trigger undefined (Reference: Document 1 Open Question #3)
- 🔴 AI article schema undefined (Reference: Document 1 Open Question #1)
- 🔴 Database query API undefined (Reference: Document 1 Open Question #6)
- 🔴 Frontend unsubscribe API undefined (Reference: Document 1 Open Question #7)
- 🔴 Auth mechanism undefined (Reference: Document 1 Open Question #5)
- **Impact:** Cannot integrate until all contracts defined
- **Resolution needed before:** Phase 4 start

**Success Criteria:**

- [ ] (BLOCKED) All module APIs connected
- [ ] (BLOCKED) Auth working between modules
- [ ] (BLOCKED) Data flows end-to-end

---

### P4.2: Unsubscribe Flow Implementation

**What:** Implement complete unsubscribe process

**Tasks:**

- [ ] Create unsubscribe confirmation page ✓ Extracted (unsubscribe flow from Doc 1 MVP Features)
- [ ] Display user's subscription details ✓ Extracted (from Doc 1)
- [ ] Handle cancellation confirmation ✓ Extracted (from Doc 1)
- [ ] Update backend state via API ✓ Extracted (from Doc 1)
- [ ] Respect unsubscribe in future publishes ✓ Extracted (from Doc 1)

**Provenance:**

- Unsubscribe flow: Document 1 MVP Features and Critical Quote - full flow described
- Flow steps: Doc 1 - "user has clicked the unsubscribe button. That'll take them to a page that says... this is what you asked for. Remember, are you sure you want this to be canceled? And then if they hit cancel, it'll show something on the screen there saying that it's now not going to send any more messages"

**Implementation Notes:**

- Confirmation page shows: subscription summary, cancel confirmation
- API call to backend: mark subscription as canceled
- Publishing check: skip unsubscribed records in doPublish()

**Success Criteria:**

- [ ] Unsubscribe link works
- [ ] Confirmation page displays correctly
- [ ] State updated in backend
- [ ] Future publishes respect unsubscribe

---

### P4.3: End-to-End Testing

**What:** Test full pipeline from trigger to email delivery

**Tasks:**

- [ ] Create test user request data ⚠️ Inferred
- [ ] Create test AI article content ⚠️ Inferred
- [ ] Execute full pipeline ⚠️ Inferred
- [ ] Verify email delivery ⚠️ Inferred
- [ ] Test unsubscribe flow ✓ Extracted (unsubscribe in Doc 1 MVP)
- [ ] Test error scenarios ⚠️ Inferred
- [ ] Verify dispatch logging ✓ Extracted (logging in Doc 1 MVP)

**Provenance:**

- Unsubscribe testing: Document 1 MVP Features - unsubscribe flow required
- Logging verification: Document 1 MVP Features - dispatch logging required
- General testing: ⚠️ Inferred (standard practice)

**Success Criteria:**

- [ ] Pipeline executes without errors
- [ ] Email delivered to test account
- [ ] Unsubscribe flow works correctly
- [ ] Logs capture all events
- [ ] Error scenarios handled

---

### P4.4: Docker Deployment Validation

**What:** Ensure module runs correctly in Docker container

**Tasks:**

- [ ] Build Docker image ✓ Extracted (Docker containerization from Doc 1 Tech Decision #1)
- [ ] Test container startup ⚠️ Inferred
- [ ] Verify environment variables ⚠️ Inferred
- [ ] Test inter-container communication ✓ Extracted (microservices architecture from Doc 1)
- [ ] Document deployment process ⚠️ Inferred

**Provenance:**

- Docker deployment: Document 1 Technical Decision #1 - "Publishing module will be a standalone Docker container"
- Module connection: Doc 1 - "when we're done, we're going to be connecting that to the other Docker containers"

**Success Criteria:**

- [ ] Container builds successfully
- [ ] Module runs in container
- [ ] Connects to other modules
- [ ] Deployment documented

---

## Automation Opportunities

**How to Use This Section:**

- Tasks marked 🤖 Agent-ready in phases above can be delegated
- Below are high-value automation targets with example prompts
- Consider learning trade-offs before delegating

### High-Value Automations (High Time Savings, Low Learning Loss)

#### P0.1: Docker Environment Setup

**Time Savings:** 1-2 hours

**Learning Trade-off:** Low (routine setup, one-time task)

**Could ask agent:**

"Create a Dockerfile for a Node.js publishing module that will run as part of a microservices architecture. Include environment variables for AWS SES credentials and database connection. Also create a docker-compose.yml for local development with volume mounts for code."

**Why automate:** Boilerplate configuration, standard Docker patterns

**What to review:** Environment variable naming, port mappings, volume paths

---

#### P0.3: Project Structure Creation

**Time Savings:** 30-45 min

**Learning Trade-off:** Low (standard project scaffolding)

**Could ask agent:**

"Create a Node.js project structure for an email publishing module. Include directories for: email templates, temporary file assembly, dispatch logs. Initialize package.json with dependencies: nodemailer (AWS SES), mustache (templating), and standard utilities. Create a README with setup instructions."

**Why automate:** Routine scaffolding, saves manual setup time

**What to review:** Directory names match Phase requirements, dependencies correct

---

#### P1.3: Temporary File Assembly

**Time Savings:** 1-2 hours

**Learning Trade-off:** Low (standard file operations)

**Could ask agent:**

"Implement a file assembly system that copies AI article files to a temporary folder structure organized by publish job ID. Include cleanup logic to delete temp files after successful dispatch or on failure. Use Node.js fs module with async/await."

**Why automate:** Routine file operations, standard patterns

**What to review:** Cleanup logic correctness, error handling

---

#### P2.2: AWS SES Dispatch

**Time Savings:** 2-3 hours

**Learning Trade-off:** Medium (SES integration is learned skill, but boilerplate heavy)

**Could ask agent:**

"Implement AWS SES email sending in Node.js. Use AWS SDK to send HTML emails with error handling for: quota exceeded, bounced emails, invalid addresses. Return detailed response object with message ID and status. Include retry logic for transient failures."

**Why automate:** Well-defined integration, AWS SDK boilerplate

**What to review:** Error handling completeness, retry logic correctness, credential security

---

#### P3.1: Template Engine Implementation

**Time Savings:** 1-2 hours

**Learning Trade-off:** Low (common templating pattern)

**Could ask agent:**

"Create a template engine for email publishing that supports shortcodes like {{first_name}}, {{article_content}}, {{unsubscribe_link}}. Use Mustache.js or similar. Include error handling for missing data (fallback to empty or default). Support nested content blocks for article lists."

**Why automate:** Standard templating implementation, library-based

**What to review:** Shortcode syntax matches requirements, error handling

---

### Do NOT Automate (👤 Human-design tasks)

- **P0.2: Email Publishing Standards Research** - Requires synthesis, judgment, compliance understanding
- **P0.4: AWS SES Account Setup** - Security decisions, account access, cost implications
- **P3.2: Plain Text Template** - Design, tone, readability require human judgment
- **P3.3: Formatted HTML Template** - Visual design, brand consistency, "where the rubber hits the road" per Doc 1
- **P4.2: Unsubscribe Flow Implementation** - Legal compliance, UX flow, critical business logic

---

## Unknowns & Decisions Needed

**From Document 1 Open Questions - Must Resolve Before Implementation:**

### 🔴 Blockers (Cannot Proceed)

| # | Question | Blocks Phase | Impact | Who Can Answer |
|---|----------|--------------|--------|----------------|
| 1 | AI article schema (fields, metadata, images) | Phase 1.2, 1.4 | Cannot parse AI content without schema | AI module owner |
| 3 | doPublish() trigger mechanism and frequency | Phase 1.1 | Cannot implement entry point | Core module/backend |
| 6 | Database query API for unpublished content | Phase 1.2, 4.1 | Cannot retrieve articles | Database module owner |
| - | Frontend request data schema | Phase 1.1, 4.1 | Cannot parse user preferences | Frontend/backend |
| 5 | Authentication/authorization between modules | Phase 4.1 | Cannot integrate securely | Security/backend |

### 🟡 Important (Affects Design)

| # | Question | Affects Phase | Impact | Who Can Answer |
|---|----------|---------------|--------|----------------|
| 2 | Max email content size/truncation limit | Phase 1.4 | Content formatting logic | Product/compliance |
| 4 | Storage limits and garbage collection | Phase 1.3 | Temp file cleanup policy | Infrastructure/cost |
| 7 | Unsubscribe page design and API | Phase 4.2 | Flow implementation details | Frontend/UX + backend |
| 9 | Email HTML markup standard | Phase 2.1, 3.3 | Template rendering approach | Email specialist |
| 10 | Minimum viable dashboard requirements | Future | Out of MVP scope | Product + engineering |
| 11 | Error handling and retry logic | Phase 2.2, 2.3 | Failure recovery strategy | System architect |

### ⚠️ Nice-to-Know (Not Blocking)

| # | Question | Relevance | Impact | Who Can Answer |
|---|----------|-----------|--------|----------------|
| 8 | Multi-user subscriptions support | Future feature | Post-MVP consideration | Product owner |

---

## Learning Objectives

### Phase 0: Foundation
- **Email HTML standards** - Cross-client compatibility, CAN-SPAM compliance
- **AWS SES fundamentals** - Quotas, bounce handling, production setup
- **Docker microservices** - Container patterns, inter-service communication

### Phase 1: Core Pipeline
- **File-based architecture** - Memory vs. disk trade-offs, temp file management
- **JSON data handling** - Schema validation, state management
- **Interval-based processing** - Trigger timing, scheduling logic

### Phase 2: Email Publishing
- **SES integration** - AWS SDK patterns, error handling, bounce management
- **Dispatch logging** - Audit trails, pipeline tracking, debugging support

### Phase 3: Template System
- **Shortcode templating** - Dynamic content insertion, template interchangeability
- **Email HTML design** - Visual quality, cross-client rendering, responsiveness
- **Quality iteration** - "Rubber hits the road" refinement process

### Phase 4: Integration
- **Microservices integration** - API contracts, authentication, error propagation
- **End-to-end testing** - Full pipeline validation, edge case handling
- **Docker deployment** - Container orchestration, production readiness

---

**End of Document**
