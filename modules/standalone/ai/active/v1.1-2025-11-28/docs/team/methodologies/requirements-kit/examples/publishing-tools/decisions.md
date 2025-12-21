---
module: publishing-tools
created: 2025-10-08
status: mvp-planning
scope: module-specific-decisions
---

# Publishing Module - Module-Specific Decisions

**Purpose**: Track all decisions specific to the Publishing Tools module that may not apply universally to other modules.

**Note**: Universal decisions that apply across all modules should be documented in `/meta-instructions/` instead.

---

## MVP Scope Decisions

### Core Value Proposition
**Decision**: Publishing module allows content creators to receive automated email digests of relevant content based on their interests.

**Single sentence**: "This module allows a content creator to receive a weekly email digest of 3-5 articles matching their interests so that they save 30 minutes of manual research per week."

### MVP Features (≤10 Total)

**Included in MVP**:
1. Schedule weekly digest (hardcoded to weekly for MVP)
2. Receive email digest
3. Email contains 3-5 articles
4. Click article link to read full content
5. Unsubscribe via email link

**Count**: 5 features ✓ (Well within 10-feature limit)

**Explicitly Excluded from MVP** (Post-MVP features):
- ❌ Multiple schedule intervals (daily/monthly) - weekly proves scheduling works
- ❌ SMS notifications - email proves notification channel works
- ❌ Push notifications - email proves notification channel works
- ❌ Multiple email templates - one template proves rendering works
- ❌ Public feed sharing - not core to email delivery
- ❌ Analytics dashboard - can query database manually for MVP
- ❌ Custom send times - can hardcode 9:00 AM for MVP
- ❌ A/B testing - need users first
- ❌ Email preview feature - not essential for MVP
- ❌ Template customization UI - one template is sufficient

**Rationale**: Following "One of Each" rule from MVP specification creation guide - one channel (email), one interval (weekly), one template.

### Personalization Approach

**Decision**: Use mock JSON data for MVP instead of full personalization engine.

**Mock Data Specification**:
- Location: TBD (will be documented in mock-data-strategy.md)
- Format: JSON file with user preferences and article mappings
- Structure: To be defined in coordination with AI module integration contract

**What Mock Represents**:
- User interest tags (e.g., ["creator economy", "open source"])
- Article selection logic (to be replaced by real AI module)
- Deduplication rules (which articles already sent)

**Post-MVP**: Replace mock JSON with actual AI module API integration.

### Analytics Approach

**Decision**: Analytics is nice-to-have, NOT required for MVP.

**MVP Alternative**: Manual database queries to verify:
- How many emails sent
- Which users received digests
- Delivery success/failure rates

**Post-MVP**: Add analytics dashboard if user feedback indicates need.

### Technology Constraints

**Email Service Provider**: Amazon SES
- Rationale: Per phase-1-research-brief.md recommendation
- MVP Note: Will operate in SES Sandbox mode (verified email addresses only)
- Configuration: Needs to be specified in integration contracts

**Template System**: TBD based on research brief
- Candidates: Jinja2, MJML, or simple HTML
- Decision pending: Review of research brief recommendations

**Scheduling**: TBD based on research brief
- Candidates: Celery Beat, cron, custom scheduler
- Decision pending: Review of research brief recommendations

**Database**: Shared PostgreSQL (per universal module requirements)
- Tables needed: TBD in data model phase
- Integration: Needs to align with Backend module schema

### Integration Dependencies

**Depends On**:
1. **AI Module**: Article search/recommendation
2. **Backend Module**: User data and authentication
3. **Email Service (SES)**: Email delivery

**Decision**: All dependencies will have stub implementations for standalone MVP operation (per MVP specification creation guide).

**Stub Requirements**:
- AI Module Stub: Returns hardcoded articles from seed data
- Backend Module Stub: Returns hardcoded user data
- SES Stub: Logs email to stdout instead of actually sending

**Environment Variable Control**:
```bash
USE_MOCK_AI_MODULE=true
USE_MOCK_BACKEND_MODULE=true
USE_MOCK_SES=true
```

### Data Persistence

**What Needs to Persist** (preliminary - subject to change):
1. User publication preferences (tags, interval, timezone)
2. Scheduling state (next_scheduled_send)
3. Dispatch log (when emails were sent)
4. Sent article history (for deduplication)

**What Does NOT Need to Persist in MVP**:
- Email content (can be regenerated)
- Click tracking data (post-MVP analytics)
- Email templates (can be file-based)

### Testing Strategy

**MVP Testing Requirements** (per MVP specification creation guide):
1. **Manual smoke test** (required): 5-step checklist verifying end-to-end flow
2. **Automated happy path test** (required): Single integration test
3. **Unit tests** (optional): 3-5 tests for critical logic (deduplication, scheduling)

**MVP Does NOT Require**:
- Load testing (works for 5-10 test users is sufficient)
- Comprehensive edge case coverage
- Performance optimization tests

### Timeline Constraint

**Decision**: Publishing module MVP must complete in 2-4 weeks maximum.

**Rationale**: Per MVP specification creation guide and lessons from overbuilt PRD example (which attempted 9-week, 10-phase project).

**Estimation Approach**:
- Use 2.5x multiplier on ideal estimates
- Only count "must have" tasks in MVP timeline
- Defer "should have" and "could have" to post-MVP

---

## Open Questions (To Be Resolved)

### Integration Contracts
1. What exact JSON schema does AI module use for article search?
2. What exact JSON schema does Backend module use for user data?
3. How is authentication handled between modules?

**Resolution Path**: Review Ben conversation (distilled) for answers.

### Technical Implementation
1. Which template system was chosen in research brief?
2. Which scheduling approach was recommended?
3. Are there existing database schemas to align with?

**Resolution Path**: Review existing documentation in `docs/modules/publishing-tools/`.

### User Workflows
1. How do users configure their publication preferences?
2. Where is the preference configuration UI?
3. Is preference configuration in scope for Publishing module or Frontend module?

**Resolution Path**: Review Dante conversation (distilled) for Frontend integration details.

---

## Decision History

### 2025-10-08: Initial Scope Definition
- **Decided**: MVP is email-only with 5 core features
- **Decided**: Mock data approach for personalization
- **Decided**: Analytics is post-MVP
- **Decided**: All dependencies will have stubs
- **Context**: Planning session with user to define approach before information gathering

---

## Notes

- This document should be updated as new module-specific decisions are made
- Universal decisions should go to `/meta-instructions/` instead
- Reference STRATEGY.md for overall project execution plan
- Reference mvp-specification-creation-guide.md for scope control principles
