# Publishing Module: Decisions & Agreements

**Source:** docs/team/module-assignments/publishing-tools/work-in-progress/raw/2025-10-01-spark-chat-ben+grig.md
**Distilled:** 2025-10-09
**Status:** Awaiting Human Review
**Module:** publishing-tools

---

## Quick Reference

| Category | Count | Details |
|----------|-------|---------|
| **MVP Features** | 5 confirmed, 4 unclear | Email publishing (✓), templating system (✓), unsubscribe flow (✓), dispatch logging (✓), event-triggered publishing (✓); Blog, notifications, social sharing (⚠️) |
| **Technical Decisions** | 7 made | Docker containerization, JSON data format, file-based assembly, AWS SES, shortcode templates, dynamic page rendering, two-template minimum |
| **Integration Points** | 5 total (2 defined, 3 partial/TBD) | SES (✓), Core module (⚠️), AI module (🔴), Database (⚠️), Frontend (🔴) |
| **Open Questions** | 11 total (4 blockers) | AI schema, database API, trigger mechanism, frontend API (all 🔴) |
| **Gaps Identified** | 12 critical | Error retry, monitoring, storage limits, email standards research, multi-user subscription |
| **Timeline Discussed** | No | No dates or milestones mentioned |

---

## MVP Features

| Feature | Status | Decision Context | Critical Quote |
|---------|--------|------------------|----------------|
| **Email Publishing** | ✓ MVP | Core functionality, extensively discussed as primary use case | "The emails sounds like a good one for sure" |
| **Template System (2 minimum)** | ✓ MVP | Required for formatting, two templates to test interchangeability | "I've found if you do something where you have at least two of something that's supposed to be interchangeable, you can check to make sure it really works" |
| **Unsubscribe Flow** | ✓ MVP | Legal compliance requirement, full flow described | "to be compliant with law, we should have the unsubscribe button" |
| **Dispatch Logging** | ✓ MVP | Track publication events, responses, errors for each request | "That dispatch log will also have the details of the whole pipeline from the moment it was requested" |
| **Event-Triggered Publishing** | ✓ MVP | doPublish() method called by server at intervals | "the server will say something like, publish all current, like do publish will be the call" |
| **Blog Publishing** | ⚠️ Unclear | Mentioned as similar to email, no clear MVP decision | "putting it on a blog would be just... the same thing, but an API call to the blog instead" |
| **Push Notifications** | 🟡 Post-MVP | Explicitly marked as "nice to have" | "The notification thing... That's a nice to have, let's just say for now" |
| **Text Messages** | 🟡 Post-MVP | Future possibility mentioned | "Maybe we can get to push notifications or text messages. I think that'd be super cool" |
| **Shareable Public Pages** | ⚠️ Unclear | Discussed as feature but no timeline | "if you could share that with people and then they could come and see it too" |
| **Social Subscribe Button** | ⚠️ Unclear | Concept discussed, unclear if MVP | "maybe we can just have a subscribe button... that could be like a really good way to add people" |
| **Admin Dashboard** | ⚠️ Unclear | Mentioned for email management, research needed | "we could do a round of research on what that is. Like what's the minimum requirements?" |

---

## Technical Decisions

### Decision: Docker Containerization

**What:** Publishing module will be a standalone Docker container

**Why:** Enable modular development and deployment, allow independent scaling and connection to other PeerMesh components

**Alternatives Considered:** Not discussed

**Critical Quote:**
> "The module itself will be a Docker container with just your part of the work in. And when we're done, we're going to be connecting that to the other Docker containers."

**Status:** ✓ Confirmed

---

### Decision: JSON Format for User Requests

**What:** User preferences and publication requests stored as JSON

**Why:** Structured data format for managing settings, suitable for database storage and API communication

**Alternatives Considered:** Not discussed

**Critical Quote:**
> "the pipeline starts with the sort of sets of instructions in probably JSON file format, where it's, you know, the details about the user and the request"

**Status:** ✓ Confirmed

---

### Decision: File-Based Email Assembly (Not In-Memory)

**What:** Assemble emails using temporary files on disk, not in-memory processing

**Why:** Reduce server RAM requirements, enable handling larger content without memory constraints

**Alternatives Considered:** In-memory processing (explicitly rejected)

**Critical Quote:**
> "I think this is the way to do it because you don't want to do this all in memory because that means that the server has to have a larger amount of RAM in it."

**Status:** ✓ Confirmed

---

### Decision: AWS Simple Email Service (SES)

**What:** Use Amazon SES for email dispatch

**Why:** Not explicitly discussed

**Alternatives Considered:** Not discussed

**Critical Quote:**
> "when it was sent to the location to be emailed out, in this case, SES by Amazon, the simple email service"

**Status:** ✓ Confirmed

---

### Decision: Shortcode Template System

**What:** Templates use shortcodes (placeholders) for dynamic content insertion

**Why:** Avoid hard-coding, enable flexible formatting without code changes

**Alternatives Considered:** Hard-coded content (mentioned as anti-pattern)

**Critical Quote:**
> "using shortcodes, which is a way of saying insert the user's first name or insert their last name or something like that. So you can kind of choose the formatting in the template instead of it being hard-coded somewhere."

**Status:** ✓ Confirmed

---

### Decision: Dynamic Page Rendering (On-Demand, Not Static)

**What:** Render "show more" web pages dynamically when user requests, don't pre-save HTML

**Why:** Save storage (avoid duplicating content), allow template changes to apply retroactively, easier customization

**Alternatives Considered:** Static pre-rendered pages (rejected due to storage and maintenance issues)

**Critical Quote:**
> "we may want to do something where that page is actually rendered when they open it... because there's no point in saving these pages fully rendered as well as the, you know, chunks... because it doubles the amount of space required"

**Status:** ✓ Confirmed

---

### Decision: Two-Template Minimum for MVP

**What:** Implement at least two different email templates

**Why:** Test interchangeability, validate templating system architecture

**Alternatives Considered:** Single template (rejected)

**Critical Quote:**
> "I've found if you do something where you have at least two of something that's supposed to be interchangeable, you can check to make sure it really works for more than the one thing."

**Status:** ✓ Confirmed

---

## Integration Contracts

| Module | Needs From Them | Provides To Them | Schema Status | Known Structure | Unknown/TBD |
|--------|-----------------|------------------|---------------|-----------------|-------------|
| **Core/Main Module** | - User request data (JSON)<br>- Trigger: doPublish() method call<br>- Interval timing info | - Publication status updates<br>- Dispatch completion logs | ⚠️ Partial | **Discussed:**<br>- State flags: "in progress", "published"<br>- JSON format confirmed<br>- doPublish() method exists<br>- Interval-based triggering | **TBD:**<br>- Exact JSON schema/field names<br>- Trigger timing mechanism<br>- Error state handling<br>- Request ID format |
| **AI Module** | - Formatted articles (markdown)<br>- Notification when user requests content | - User interest tags/queries<br>- Content received confirmation | 🔴 TBD | **Discussed:**<br>- Format: Markdown files<br>- Content type: Articles<br>- Quote: "It'll probably just be like a markdown file" | **TBD:**<br>- Exact schema/field names<br>- Metadata fields<br>- Image handling<br>- Content length limits<br>- Article ID format |
| **Database** | - User request records<br>- AI-generated content files<br>- Historical send tracking | - Query results: unpublished content by tags<br>- Filter: exclude already-sent items | ⚠️ Partial | **Discussed:**<br>- Query by user tags<br>- Filter already-sent items<br>- Tracking send history<br>- Content storage concept | **TBD:**<br>- API endpoint/method signature<br>- Query response format<br>- Pagination approach<br>- Tracking mechanism details |
| **Frontend** | - User preferences (topics, frequency, delivery methods)<br>- Unsubscribe requests | - Publication confirmations<br>- Unsubscribe completion status | 🔴 TBD | **Discussed:**<br>- User input source<br>- Preference data exists<br>- Unsubscribe flow required | **TBD:**<br>- Preference JSON schema<br>- API endpoints<br>- Unsubscribe page design<br>- Confirmation API |
| **AWS SES** | N/A (external service) | - Formatted email (HTML/text)<br>- Recipient list<br>- Tracking preferences | ✓ Defined | **Defined:**<br>- Standard AWS SES API<br>- HTML/text email format<br>- Bounce/error responses<br>- SendEmail operation | N/A - External service with documented API |

---

## Open Questions

| # | Question | Impact | Priority | Who Can Answer | Context from Conversation |
|---|----------|--------|----------|----------------|---------------------------|
| 1 | What is the exact schema for AI-generated articles? (fields, metadata, images) | Blocker | 🔴 | AI module owner | "It'll probably just be like a markdown file" - format mentioned but structure undefined |
| 2 | What is the max email content size before truncation? (200 words? other limit?) | High | 🟡 | Product/compliance | "if you've got an article that's hundreds of pages long, you just want the first paragraph or... 200 words or something" - approximate, not firm |
| 3 | What is the exact doPublish() trigger mechanism and call frequency? | Blocker | 🔴 | Core module/backend | "server will say something like, publish all current, like do publish will be the call" - behavior described, implementation undefined |
| 4 | What are storage limits and garbage collection thresholds? | High | 🟡 | Infrastructure/cost | "we'll have to do some math on how many markdown files... we can store on a system before it's not economically viable" - identified need, no specifics |
| 5 | What authentication/authorization is required between modules? | Blocker | 🔴 | Security/backend | Not discussed - inferred as standard microservices requirement |
| 6 | What is the database query API for fetching unpublished content by user tags? | Blocker | 🔴 | Database module owner | "we're going to make a request to the other database for any available stuff that matches those tags" - concept clear, API undefined |
| 7 | What is the unsubscribe page design and confirmation API contract? | Medium | 🟡 | Frontend/UX + backend | "take them to a page that says... this is what you asked for. Remember, are you sure" - flow described, implementation not detailed |
| 8 | Do we support multi-user subscriptions (friends sharing feed)? | Low | ⚠️ | Product owner | "it might be cool if you could like create your own list of people that receive it with you. I don't know like how that would work" - uncertain if in scope |
| 9 | What email HTML markup language/standard should we use? | Medium | 🟡 | Email specialist | "I think there's a markup language for emails. Did you... run into that or not" - identified as consideration, not resolved |
| 10 | What is minimum viable dashboard for email management? | Medium | 🟡 | Product + engineering | "we could do a round of research on what that is. Like what's the minimum requirements?" - research task identified |
| 11 | What error handling and retry logic for failed email dispatch? | High | 🟡 | System architect | Not discussed - inferred as critical for production reliability |

---

## Critical Quotes

### Legal: Unsubscribe Requirement

**Context:** Explicit legal compliance mandate for email system

> "to be compliant with law, we should have the unsubscribe button, the link there, which means anyone who's had enough can click a button to unsubscribe"

**Implications:** Unsubscribe flow is MVP requirement, not optional. Must implement: button in email → confirmation page → backend state update → respect preference in future sends.

---

### Vision: Quality Standards - "Rubber Hits the Road"

**Context:** Sets quality bar for template rendering and visual output

> "That's where us as humans will have to look at it and make a lot of tweaks and changes to make it look good and look professional. That's where the rubber hits the road, as they say."

**Implications:** Template rendering quality is critical success factor, not just functional checkbox. Expect iterative refinement phase. Visual output quality = system value perception.

---

### Technical: Template Interchangeability Test

**Context:** Rationale for two-template minimum in MVP

> "I've found if you do something where you have at least two of something that's supposed to be interchangeable, you can check to make sure it really works for more than the one thing."

**Implications:** MVP MUST include two templates (suggested: plain text + formatted with images/colors) to validate templating system architecture. Single template = untested design.

---

### Scope: Notifications Explicitly Deferred

**Context:** Clear priority: email first, mobile later

> "The notification thing might be like a little, is an API call to something that like actually has access to the mobile device. That's a nice to have, let's just say for now."

**Implications:** Push notifications OUT of MVP. Email publishing is the core focus. Mobile can be added later with same rendering logic (different dispatch target).

---

### Technical: Memory vs. File Architecture

**Context:** Core architectural decision for server efficiency

> "I think this is the way to do it because you don't want to do this all in memory because that means that the server has to have a larger amount of RAM in it."

**Implications:** Architecture pattern: use temporary files, not in-memory buffers. Trade-off: lower RAM requirements for higher I/O operations. Design for disk-based assembly.

---

### Vision: Email Publishing Systems Are Valuable and Complex

**Context:** Real-world validation of problem domain significance

> "I had a buddy who in 2026, I think, was hired into this secret team... building the email publishing system for Nest... And now he's a self-made millionaire living in New Zealand"

**Implications:** Email publishing at scale is complex, deep problem space. Don't underestimate scope. Nest invested heavily in this - expect hidden complexity. Value proposition is proven.

---

### Scope: Research Email Standards - Explicit Task

**Context:** Identified research prerequisite before detailed implementation

> "we'll probably need to do some research on what these email publishing tools have in terms of the full suite of things... what's the minimum requirements? And what are these like large systems doing for sending like millions of emails?"

**Implications:** Research task is part of MVP work. Need to understand: minimum compliance requirements, scale considerations, industry standards. Don't reinvent wheel - learn from established systems.

---

### Vision: Feedback Loop and Content Relevance

**Context:** Long-term value of user interaction data for AI improvement

> "the more we get from the user about their interests the curating of the work, we're understanding the user. We're also understanding the space in general, right?"

**Implications:** System isn't just one-way publishing - it's a feedback loop. User interactions (clicks, saves, preferences) inform AI content generation. Long-term: improve relevance, build knowledge graph of user-topic-content relationships.

---

## Gaps Identified

### 🔴 Blockers (Implementation Cannot Proceed)

- **AI Article Schema Definition** - Need exact data structure: fields, metadata, image handling to parse and template articles - **Source: ✓ From conversation** ("It'll probably just be like a markdown file" - vague) - **(See Open Question #1)**

- **Database Query API Contract** - Specific API for querying unpublished content by user tags, filtering already-sent items - **Source: ✓ From conversation** (concept described, implementation undefined) - **(See Open Question #6)**

- **doPublish() Trigger Implementation** - Exact mechanism for how/when publishing pipeline is invoked by server - **Source: ✓ From conversation** (behavior described, technical details missing) - **(See Open Question #3)**

- **Frontend Request Data Schema** - JSON structure for user preferences from frontend - **Source: ⚠️ Inferred** (integration mentioned, schema not detailed beyond "JSON file format") - **(Related to Integration Contracts)**

### 🟡 Likely Needed (High Probability Required)

- **Error Handling and Retry Logic** - What happens when email dispatch fails: retry attempts, alerting, fallback behavior - **Source: ⚠️ Inferred** (dispatch mentioned, failure scenarios not covered) - **(See Open Question #11)**

- **Storage Limits and Cleanup Policy** - Specific thresholds for archiving/deleting old content - **Source: ✓ From conversation** ("we'll have to do some math on how many markdown files... economically viable to keep" - identified, not resolved) - **(See Open Question #4)**

- **Email Content Size/Truncation Limits** - Firm decision on max email length before "show more" truncation - **Source: ✓ From conversation** ("200 words or something" - approximate, not definitive) - **(See Open Question #2)**

- **Rate Limiting and Throttling** - Prevent abuse, manage AWS SES quotas, handle high-volume publishing - **Source: ⚠️ Inferred** (standard for email systems, not discussed)

- **Email HTML Markup Standard** - Which email HTML/CSS framework to use for cross-client compatibility - **Source: ✓ From conversation** ("there's a markup language for emails. Did you... run into that" - mentioned, not resolved) - **(See Open Question #9)**

- **Bounce and Error Response Handling** - How to process email bounces, spam reports, delivery failures from SES - **Source: ✓ From conversation** ("The email one's also got... the potential be bounced back. So that needs to be added to the log" - identified, not detailed) - **(Related to error handling - See Open Question #11)**

### ⚠️ Standard Practices (Not Discussed, Typical for Systems)

- **Logging and Monitoring** - Application logs, error tracking, performance metrics beyond dispatch logs - **Source: ⚠️ Inferred** (dispatch log mentioned, broader observability not covered)

- **Backup and Disaster Recovery** - Database backups, content recovery, system restore procedures - **Source: ⚠️ Inferred** (standard practice)

- **Configuration Management** - Environment variables, secrets (AWS credentials), feature flags - **Source: ⚠️ Inferred** (standard practice)

- **Health Checks and Readiness Probes** - Docker container health monitoring, orchestration integration - **Source: ⚠️ Inferred** (Docker mentioned, health checks not discussed)

- **Testing Strategy** - Unit tests, integration tests, email rendering preview/testing environment - **Source: ⚠️ Inferred** (quality emphasized, testing approach undefined)

- **Deployment Pipeline** - CI/CD, versioning, rollback strategy, blue-green deployment - **Source: ⚠️ Inferred** (standard practice)

- **API Versioning** - How to handle breaking changes in module contracts - **Source: ⚠️ Inferred** (integrations discussed, versioning not covered)

- **Authentication/Authorization Between Modules** - How modules verify identity and permissions for API calls - **Source: ⚠️ Inferred** (standard microservices requirement, not discussed)

### Post-MVP Considerations (Future Scope)

- **Blog Publishing Integration** - API calls to Substack, Patreon, other platforms - **Source: ✓ From conversation** ("putting it on a blog would be... an API call to the blog instead" - similar to email, unclear if MVP)

- **Multi-User Subscriptions (Sharing with Friends)** - Allow users to invite others to their custom feed - **Source: ✓ From conversation** ("it might be cool if you could like create your own list of people that receive it with you" - uncertain)

- **Social Features (Subscribe Button, Follower Count)** - Turn published pages into social hubs - **Source: ✓ From conversation** ("maybe we can just have a subscribe button... that could be like a really good way to add people")

- **Push Notifications** - Mobile notification delivery channel - **Source: ✓ From conversation** ("The notification thing... That's a nice to have, let's just say for now" - explicitly post-MVP)

- **Text Message Publishing** - SMS delivery channel - **Source: ✓ From conversation** ("Maybe we can get to push notifications or text messages" - future possibility)

- **Interactive Web Pages (Save Snippets, Deep Dive Topics)** - Rich user interaction beyond static viewing - **Source: ✓ From conversation** ("save this snippet for me for later or like let's dive into these topics further")

- **Admin Dashboard for Email Management** - UI for viewing sent emails, user analytics, system tuning - **Source: ✓ From conversation** ("we could do a round of research on what that is... what's the minimum requirements?" - research identified, scope unclear)

- **Feedback Loop and AI Content Weighting** - User signals (clicks, saves) improve AI relevance - **Source: ✓ From conversation** ("the more we get from the user about their interests... weighting system where we can apply weights")

- **SEO and Search Engine Visibility** - Public pages as content hubs for search traffic - **Source: ✓ From conversation** ("the whole internet and all of the search engines will be hitting it too")

---

## Using This Document: Resolving TBDs and Gaps

### Quick Start: Are We Ready to Implement?

**Check these indicators:**

✅ **Ready for Implementation:**
- All 🔴 Blocker Open Questions resolved (see Open Questions section)
- All Integration Contracts either ✓ Defined OR have documented workaround plan
- All MVP Features confirmed (no ⚠️ Unclear items remaining)
- Team consensus documented (synthesis stage complete)

⚠️ **Partially Ready (can start some work):**
- Some 🔴 Blockers resolved, others documented with mitigation
- Foundation work can proceed (Phase 0 in Implementation Guide)
- Integration-dependent work blocked until contracts defined

❌ **Not Ready:**
- Multiple 🔴 Blockers unresolved
- Integration Contracts mostly 🔴 TBD
- MVP scope still has ⚠️ Unclear items

---

### How to Resolve Integration Contract TBDs

**When you see 🔴 TBD (No Schema Defined):**

**What it means:** Integration mentioned in conversation but no schema/contract discussed

**Resolution process:**
1. **Review conversation context** (see "Known Structure" column and related Open Questions)
2. **Identify decision maker** (see "Who Can Answer" in Open Questions)
3. **Gather requirements:**
   - What data flows in? (see "Needs From Them" column)
   - What data flows out? (see "Provides To Them" column)
   - What's the interaction pattern? (API call, event trigger, polling?)
4. **Define minimal schema** covering discussed use cases
5. **Document in integration contract design doc**
6. **Update this document:** Change 🔴 TBD → ✓ Defined, add schema reference

**Example: AI Module Integration Resolution**

**Before (🔴 TBD):**
```
| **AI Module** | Formatted articles | User queries | 🔴 TBD | "markdown file" mentioned, no schema |
```

**After resolution (✓ Defined):**
```
| **AI Module** | Formatted articles | User queries | ✓ Defined | Schema: docs/integrations/ai-article-schema.json - Fields: article_id, title, content_markdown, summary, url, tags[], image_url (optional) |
```

**Resolution artifacts created:**
- `docs/integrations/ai-article-schema.json` - Full JSON schema
- `docs/integrations/ai-module-contract.md` - Integration contract doc
- Updated Integration Contracts table in this document

---

**When you see ⚠️ Partial (Some Structure Known):**

**What it means:** Conversation discussed some structure but details incomplete

**IMPORTANT:** Check the "Known Structure" column - don't ignore this!

**Resolution process:**
1. **Start with known structure** (extract from Known Structure column)
2. **Identify gaps** (see "Unknown/TBD" column or Open Questions)
3. **Fill gaps through:**
   - Follow-up conversation with module owner
   - Review existing similar integrations
   - Technical research (industry standards, library documentation)
4. **Document complete schema**
5. **Update status:** ⚠️ Partial → ✓ Defined

**Example: Core Module Integration Resolution**

**What we know (from conversation):**
- State flags: "in progress", "published"
- JSON format for user requests
- doPublish() trigger method exists

**What's unknown:**
- Exact JSON schema fields
- Trigger timing/frequency
- Error state handling

**Resolution action:**
1. Use known state flags as starting point
2. Design JSON schema around "user request" concept mentioned
3. Prototype doPublish() signature based on described behavior
4. Validate with backend team
5. Document complete contract

---

### How to Prioritize and Resolve Open Questions

**Resolution Order (by Priority):**

**1️⃣ All 🔴 Blockers First** (Implementation cannot proceed)
- These block multiple phases of development
- Usually integration schemas, auth mechanisms, core architectural decisions
- **Action:** Schedule resolution meetings ASAP, assign DRIs (Directly Responsible Individuals)

**2️⃣ 🟡 Important Next** (Affects design but has workarounds)
- Can stub these initially but need real answers before production
- Examples: Storage limits, email size thresholds, error retry logic
- **Action:** Document workaround approach, add to technical debt log

**3️⃣ ⚠️ Nice-to-Know Last** (Optimization or edge cases)
- Doesn't block MVP implementation
- Can be addressed in post-MVP iterations
- **Action:** Add to backlog, prioritize after MVP launch

**Resolution Workflow:**

For each Open Question:
1. **Check "Who Can Answer"** column → Contact that person/team
2. **Review "Context from Conversation"** → Understand what triggered the question
3. **Determine resolution type:**
   - **Technical decision:** Architecture/design session
   - **Product decision:** Stakeholder alignment meeting
   - **Research needed:** Spike/investigation task
4. **Document decision** in appropriate section:
   - Technical Decisions (if architectural choice)
   - MVP Features (if scope clarification)
   - Integration Contracts (if schema definition)
5. **Update Open Questions:** Mark as ✅ Resolved with reference to where documented

---

### How to Address Identified Gaps

**Gaps are categorized by urgency. Treat each category differently:**

**🔴 Blockers (Cannot Implement Without):**

**What they are:** Missing architectural decisions, undefined contracts, fundamental unknowns

**Resolution approach:**
- **Technical design session** with engineering team
- **Stakeholder alignment** for product decisions
- **Document in:** Integration contracts, technical design docs, architectural decision records (ADRs)

**Example gaps from this document:**
- AI article schema definition → Integration contract needed (Open Question #1)
- Authentication between modules → Security design doc needed (Open Question #5)
- Database query API contract → Backend API spec needed (Open Question #6)

**Timeline:** Resolve before Phase 1 implementation starts

---

**🟡 Likely Needed (High Probability Required):**

**What they are:** Production requirements not discussed but standard for this system type

**Resolution approach:**
- **Engineering team discussion** on approach
- **Industry best practices research** (how do similar systems handle this?)
- **Document in:** Non-functional requirements, system design, deployment guide

**Example gaps from this document:**
- Error handling and retry logic → Standard microservices pattern (Open Question #11)
- Storage limits and cleanup policy → Capacity planning doc (Open Question #4)
- Rate limiting and throttling → API gateway configuration

**Timeline:** Resolve during implementation phases (can stub initially)

---

**⚠️ Standard Practices (Industry-Standard Requirements):**

**What they are:** Assumed requirements for production systems (logging, monitoring, backups, etc.)

**Resolution approach:**
- **Reference architecture patterns** from similar projects
- **Existing implementation review** (what do we already do for other modules?)
- **Document in:** Operational runbook, deployment guide, monitoring setup

**Example gaps from this document:**
- Logging and monitoring → Adopt project-wide observability standards
- Backup and disaster recovery → Use existing backup infrastructure
- Configuration management → Standard environment variable approach
- Health checks → Docker orchestration standard

**Timeline:** Address during DevOps/deployment setup (not blocking development)

---

### Workflow: From TBDs to Implementation-Ready

**Step 1: Audit Current State**
- [ ] Count 🔴 Blockers in Open Questions (Currently: 4 blockers - #1, #3, #5, #6)
- [ ] Count 🔴 TBD in Integration Contracts (Currently: 2 TBD - AI Module, Frontend)
- [ ] Count 🔴 Blockers in Gaps Identified (Currently: 4 blockers)
- [ ] Total blockers = sum of above

**Step 2: Prioritize Blocker Resolution**
- [ ] Create resolution task for each 🔴 Blocker
- [ ] Assign DRI (Directly Responsible Individuals)
- [ ] Set deadlines (Phase 0 completion target)
- [ ] Track in project management tool

**Step 3: Execute Resolution**
- [ ] Hold design sessions, stakeholder meetings, research spikes
- [ ] Document all decisions with rationale
- [ ] Create integration contracts, schemas, design docs
- [ ] Update this document as items resolve

**Step 4: Validate Readiness**
- [ ] All MVP-critical 🔴 Blockers → ✅ Resolved
- [ ] All Integration Contracts → ✓ Defined (or documented workaround)
- [ ] All ⚠️ Unclear MVP Features → ✓ Confirmed or 🟡 Post-MVP
- [ ] Team consensus: "We can start implementation"

**Step 5: Handoff to Implementation**
- [ ] Mark document status: "Ready for Implementation"
- [ ] Reference in Implementation Guide (Document 2)
- [ ] Begin Phase 0: Foundation & Learning

---

### Example: Complete Resolution Flow

**Starting State (from this document):**

**Open Question #1:** What is exact schema for AI-generated articles?
- **Status:** 🔴 Blocker
- **Who:** AI module owner
- **Context:** "markdown file" mentioned, structure undefined

**Integration Contract - AI Module:**
- **Status:** 🔴 TBD
- **Notes:** Format vague, schema undefined

**Gap - AI Article Schema:**
- **Category:** 🔴 Blocker
- **Description:** Cannot parse/template articles without schema

---

**Resolution Process:**

1️⃣ **Identify DRI:** AI module owner (Alice)
2️⃣ **Schedule meeting:** Grig + Alice design session
3️⃣ **Design session output:**
   - AI provides markdown files with frontmatter metadata
   - Schema defined: `{ article_id, title, content_markdown, summary, url, tags[], created_at, image_url? }`
   - Contract documented: `docs/integrations/ai-article-schema.json`
4️⃣ **Update this document:**
   - Open Question #1: ✅ Resolved (reference: ai-article-schema.json)
   - Integration Contract - AI Module: ✓ Defined (schema documented)
   - Gap removed from Blockers section
5️⃣ **Implementation Guide updated:**
   - Phase 1 blocker removed
   - Task P1.2 updated with schema reference

---

**Result State:**

**Open Questions:** 10 total (3 blockers) ← was 11 total (4 blockers)

**Integration Contracts:**
```
| **AI Module** | Formatted articles | User queries | ✓ Defined | Schema: docs/integrations/ai-article-schema.json - Markdown with frontmatter. Fields: article_id, title, content_markdown, summary (200 words), url, tags[], image_url (optional), created_at |
```

**Gaps Identified - Blockers:** 3 remaining ← was 4

**Implementation Guide - Phase 1:**
- ✅ Can proceed (blocker resolved)
- Task P1.2 now references ai-article-schema.json

---

### Quick Reference: Resolution Checklist

**For each 🔴 TBD Integration Contract:**
- [ ] Review conversation context (Known Structure column, Open Questions)
- [ ] Identify who can define schema (module owner)
- [ ] Extract any discussed structure (don't ignore partial info!)
- [ ] Schedule design session to define complete schema
- [ ] Document in integration contract doc
- [ ] Update Integration Contracts table: 🔴 → ✓

**For each 🔴 Blocker Open Question:**
- [ ] Check "Who Can Answer"
- [ ] Understand "Context from Conversation"
- [ ] Determine resolution type (meeting, research, design)
- [ ] Execute resolution
- [ ] Document decision in appropriate section
- [ ] Mark question as ✅ Resolved

**For each ⚠️ Unclear MVP Feature:**
- [ ] Schedule product/stakeholder clarification
- [ ] Get explicit in/out decision
- [ ] Update MVP Features table: ⚠️ → ✓ MVP or 🟡 Post-MVP
- [ ] Update Implementation Guide phases if needed

---

### When This Document is "Complete"

**Definition of Complete:**

1. **All Integration Contracts:** ✓ Defined (no 🔴 TBD for MVP-critical integrations)
2. **All Open Questions:** 🔴 Blockers resolved, 🟡 Important have workaround or acceptance
3. **All MVP Features:** Clear ✓ MVP or 🟡 Post-MVP (no ⚠️ Unclear)
4. **All Gaps - Blockers:** Resolved or documented technical debt with mitigation
5. **Synthesis Stage:** Human validation complete, team consensus documented

**Deliverables when complete:**
- This document (updated with resolutions)
- Integration contract docs (one per integration)
- Technical design docs (for architectural decisions)
- Updated Implementation Guide (Phase 0 unblocked)

**Next step:** Begin Implementation Phase 0 (Foundation & Learning)

---

**End of Document**
