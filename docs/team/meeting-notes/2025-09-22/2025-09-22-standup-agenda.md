# Phase 1 Research Review Stand-Up Agenda
- **Date**: September 22, 2025
- **Duration**: 45 minutes

---

## 💡 Quick Reminder: We're Here to Help
**Team note:** If you encounter a blocker, please reach out to @grigb right away. No need to struggle alone - let's solve it together!

### Sharing What You Need
When reaching out about a blocker, it's helpful to include:

1. **What you're trying to find or build** - the specific piece you need
2. **Which module should provide it** - your best guess on the source
3. **How you expect it to work** - the format or structure you're anticipating
4. **Your current approach** - what you've attempted or assumed so far
5. **What would unblock you** - the specific help or decision you need

### Navigating Our Integration Phase
As we connect our modules, remember:

- **Mock data keeps you moving** - create placeholders when needed
- **Document your thinking** - note your assumptions for the team
- **Build adaptable interfaces** - we'll iterate as we learn
- **Communicate often** - share expectations with other modules early

Questions we're all figuring out together:

- How will our APIs communicate?
- What's the best authentication flow?
- Which events should trigger updates?
- Where should different data types live?
- How do we handle cross-module errors gracefully?

---

## 0:00–0:02 — Meeting Setup

**Zoom Display Names**

"Please update your Zoom display name to your full name for clarity.

- Desktop: Participants → hover your name → More → Rename
- Mobile: Participants → tap your name → Rename
Taking 20 seconds for everyone to update."

---

## 0:02–0:03 — Agenda Overview

"Today we'll:

- Review research outputs
- Identify and address blockers
- Assign next 48-hour deliverables
- Review repository changes since last meeting
- Reminder: Log time in timesheet (link in Discord #notices)"

---

## 0:03–0:08 — Repository Changes Review

**Demonstrating how to check changes since last stand-up:**

### A) View Commits
1. Open repo → Code tab → branch (usually main) → History/Commits
2. Find commits since [LAST_MEETING_DATE]
3. Click commits to see Browse files or Files changed

### B) Pull Requests
Search filters:

- Merged: `is:pr is:merged merged:>=YYYY-MM-DD sort:updated-desc`
- Open: `is:pr is:open updated:>=YYYY-MM-DD sort:updated-desc`
- By author: add `author:github-username`

### C) Issues & Decisions
Filter by:

- Decisions: `label:decision updated:>=YYYY-MM-DD`
- Blockers: `label:blocker is:open`
- Phase: `label:"phase:1"`

"Reference issue/PR numbers and file paths during your updates for traceability."

---

## 0:08–0:10 — Report Format

**Each person gets 3 minutes. Please follow this structure:**

1. **Objective** (1 sentence): What you researched/proved with issue #
2. **Top 3 Findings**: One line each with links
3. **Artifacts**: PR numbers, commit IDs, or file paths
4. **Blockers**: Specific requests (who/what needed)
5. **Next 48 Hours**: One deliverable with acceptance criteria

---

## 0:10–0:35 — Individual Reports (3 min each)

- AI Development
- Backend Architecture
- Frontend Design
- Publishing Tools

*Timekeeper will signal at 2:30 and 3:00 marks*

---

## 0:35–0:43 — Module Integration Check (2 min each)

### Backend
- Entity definitions finalized?
- ID strategy decisions?
- Schema blocking other modules?
- Minimal read/write path ready?

### Frontend
- Information architecture defined?
- Key screens identified?
- API contract assumptions to validate?

### AI Development
- Deep research prompts documented?
- Source validation process?
- Prompt/output storage approach?
- Runtime constraints identified?

### Publishing Tools
- Priority channels selected?
- Template structure ready?
- Data feed requirements from Backend?

---

## 0:43–0:45 — Capture Decisions & Actions

"Creating GitHub issues for:

- All decisions (labeled 'decision') with owner and due date
- Blockers requiring follow-up
- Deep-dive topics for separate sessions"

---

## 0:45 — Closing

**Action Items:**

1. Log time in timesheet today (link in #notices)
2. Post in #notices before next stand-up:
   - Your 1-line objective
   - One artifact link (PR/document)
   - Any blocker requests

---

## Meeting Minutes Template

```markdown
# Stand-Up Minutes — Phase 1 Research Review — [DATE]

## Attendees
Facilitator:
Timekeeper:
Scribe:
Team Members:

## Individual Updates
### [Name] — Issue #[number] — [Objective]
- Findings: [link1], [link2], [link3]
- Artifacts: PR #[number] / commits / paths
- Blockers: Issue #[number], #[number]
- Next 48h: [deliverable]

## Module Integration
- Backend: [key decisions/dependencies]
- Frontend: [key decisions/dependencies]
- AI: [key decisions/dependencies]
- Publishing: [key decisions/dependencies]

## Decisions
- D1: [decision] → [owner], due [date]
- D2: [decision] → [owner], due [date]

## Parking Lot
- [topics for separate discussion]

## Next Meeting
Date:
Focus:
```

---

## Facilitator Checklist

- [ ] All participants using real names
- [ ] GitHub changes demonstration completed
- [ ] Each report followed 5-part format
- [ ] Blockers converted to issues with owners
- [ ] Decisions documented and labeled
- [ ] Timesheet reminder acknowledged
- [ ] Next meeting scheduled

---

**Note**: Keep discussions focused. Technical deep-dives should be scheduled as separate sessions to respect everyone's time.
