# Frontend Module: Decisions & Agreements

**Source:** docs/team/module-assignments/frontend-design/work-in-progress/raw/2025-09-30-spark-grig+dante.md
**Distilled:** 2025-10-09
**Status:** Awaiting Human Review
**Module:** frontend-design

---

## Quick Reference

| Category | Count | Details |
|----------|-------|---------|
| **MVP Features** | 6 confirmed, 3 unclear | 3-panel layout (✓), bubble onboarding (✓), feed interface (✓), graph visualization (✓), hierarchy browser (✓), topic selection (✓); Blog publishing UI, text message UI, lookbook management (⚠️) |
| **Technical Decisions** | 5 made | React + Vite, Cytoscape.js for graphs, Dynamic JSON rendering, Component library approach, Infinite scroll feed |
| **Integration Points** | 4 total (0 defined, 4 TBD) | Backend (🔴 API TBD), AI module (🔴 format TBD), Publishing tools (🔴 integration TBD), SpecKit (🔴 workflow TBD) |
| **Open Questions** | 13 total (6 blockers) | Backend API schema, AI data formats, auth mechanism, design system choices, component libraries (all 🔴) |
| **Gaps Identified** | 10 critical | Data schemas, API contracts, auth/security, state management, testing strategy |
| **Timeline Discussed** | No | No specific dates, "zero to one" mentioned as goal |

---

## MVP Features

| Feature | Status | Decision Context | Critical Quote |
|---------|--------|------------------|----------------|
| **3-Panel Layout** | ✓ MVP | Standard IDE-style layout: left menu, center content, right filters | "The idea would be to have like a column on the left... And then on the right-hand side, what we'll do is that'll be our filter" |
| **Bubble Onboarding Interface** | ✓ MVP | Initial user preference gathering via interactive bubbles | "we'll start with a, like a screen with a one circle in the middle and a plus sign" |
| **Feed Interface (Infinite Scroll)** | ✓ MVP | TikTok/Instagram-style content feed in center panel | "we'll find a off the shelf probably a react based component that does that whole feed thing for us" |
| **Graph Visualization** | ✓ MVP | Ontology/relationship mapping using nodes and edges | "we've got that one that you found the nodes and points. That'll be great for the the one of the main things that the AI is good at, which is this uh, uh, ontology mapping" |
| **Hierarchy Browser** | ✓ MVP | Yahoo-style directory drilling interface | "Back in the day, Yahoo was a big deal... directory, which was just text with the secondary level of the idea of the text... you could click on the text or you could click on the subtext" |
| **Topic Selection/Checkboxes** | ✓ MVP | User can select topics of interest from hierarchical view | "And at any level, there's like a little tick box next to the item. And if you click on it, it becomes part of your list of interesting topics" |
| **Email/Publishing Settings** | ⚠️ Unclear | User preferences for delivery channels and intervals | "they need to be able to choose what they're interested in... what kind of output we actually want that in" |
| **Login/Signup** | ⚠️ Unclear | User authentication mentioned but not detailed | "they need to be able to, you know, obviously log in so that they can make custom settings" |
| **Lookbook/Design Collection** | ⚠️ Unclear | Tool for collecting visual design inspiration | "drop things into like a lookbook... you just do screen captures, drop it into that endless canvas" |

---

## Technical Decisions

### Decision: React + Vite Technology Stack

**What:** Use React with Vite for frontend development

**Why:** Modern tooling, fast dev experience (implied from context)

**Alternatives Considered:** Not discussed

**Critical Quote:**
> "We're going to be using React... with Vite"

**Status:** ✓ Confirmed

---

### Decision: Cytoscape.js for Graph Visualization

**What:** Use Cytoscape library for ontology graph rendering

**Why:** Established library for node/edge graphs (implied)

**Alternatives Considered:** Not discussed

**Critical Quote:**
> "we've got that one that you found the nodes and points" [referring to Cytoscape demo]

**Status:** ✓ Confirmed

---

### Decision: Dynamic JSON-Driven UI

**What:** Interface renders dynamically based on JSON data from backend

**Why:** Flexibility to display whatever structure AI provides

**Alternatives Considered:** Not discussed

**Critical Quote:**
> "what we really want is an interface that is dynamic. So whatever the JSON file gives us, we display"

**Status:** ✓ Confirmed

---

### Decision: Component Library + Off-the-Shelf Approach

**What:** Use existing React components where possible (infinite scroll, etc.)

**Why:** Faster development, proven patterns

**Alternatives Considered:** Building from scratch (rejected for time reasons)

**Critical Quote:**
> "we'll find a off the shelf probably a react based component that does that whole feed thing for us"

**Status:** ✓ Confirmed

---

### Decision: Cursor IDE for Development

**What:** Use Cursor as primary development environment

**Why:** AI-assisted coding, predictive completions, context awareness

**Alternatives Considered:** Traditional IDEs (implied comparison)

**Critical Quote:**
> "We're using cursor... it would give you suggestions... it'll say like hit the tab key to jump to the next instance of this... the AI is the godsend for the developer"

**Status:** ✓ Confirmed

---

## Integration Contracts

| Module | Needs From Them | Provides To Them | Schema Status | Known Structure | Unknown/TBD |
|--------|-----------------|------------------|---------------|-----------------|-------------|
| **Backend/Core** | - User data (preferences, topics)<br>- Feed content (paginated)<br>- Related topics API<br>- Authentication tokens | - User selections (topics, settings)<br>- Unsubscribe requests<br>- Preference updates | 🔴 TBD | **Discussed:**<br>- JSON format confirmed<br>- Pagination: "10 pieces of content at a time"<br>- API calls mentioned<br>- Login/auth required | **TBD:**<br>- Exact JSON schema/field names<br>- Pagination API (cursor vs offset)<br>- Auth mechanism (JWT, OAuth, etc.)<br>- User data structure |
| **AI Module** | - Ontology graph data (nodes, edges)<br>- Related topics for bubble UI<br>- Hierarchical content structure | - User interest signals<br>- Topic selection feedback | 🔴 TBD | **Discussed:**<br>- Single JSON file format<br>- Hierarchical structure<br>- Ontology: nodes (bees, flowers) + relationships ("gets nectar from")<br>- Related topics: "four or five" per request | **TBD:**<br>- JSON schema for graphs<br>- Node/edge format<br>- Hierarchical data structure<br>- Related topics API contract |
| **Publishing Tools** | - Publication status<br>- Email/delivery settings options | - User publishing preferences<br>- Channel selections (email, blog, etc.) | 🔴 TBD | **Discussed:**<br>- User preferences exist<br>- Multiple delivery channels<br>- Settings UI needed | **TBD:**<br>- Preference schema<br>- Settings options available<br>- API endpoints<br>- Status format |
| **SpecKit Workflow** | - Functional spec output<br>- Task lists<br>- Test definitions | - Feature requirements<br>- User stories | 🔴 TBD | **Discussed:**<br>- Slash commands<br>- Pipeline stages<br>- Workflow tool concept | **TBD:**<br>- Integration approach<br>- Data format<br>- Workflow unclear if MVP |

---

## Open Questions

| # | Question | Impact | Priority | Who Can Answer | Context from Conversation |
|---|----------|--------|----------|----------------|---------------------------|
| 1 | What is the exact backend API schema for feed content and user data? | Blocker | 🔴 | Backend developer | "calling our server backend API asking for the content" - API mentioned but undefined |
| 2 | What is the JSON structure for AI ontology graphs and hierarchical data? | Blocker | 🔴 | AI module owner | "it's all going to be coming in in a single JSON file... hierarchical" - format vague |
| 3 | What authentication/authorization mechanism should be used? | Blocker | 🔴 | Security/backend | "obviously log in" - mentioned but no auth strategy discussed |
| 4 | What is the "related topics" API contract for bubble interface? | Blocker | 🔴 | Backend/AI | "send a message to the backend saying, get me some research results or no, better... get me related ideas... I want about four or five of them" - behavior described, API undefined |
| 5 | What component libraries should we use for infinite scroll and feed UI? | High | 🟡 | Frontend/research | "find a off the shelf probably a react based component" - need to identify specific library |
| 6 | What design system/color scheme should we adopt? | High | 🟡 | Design/product | "top design trends of the year... neon green with hot pink... webby Awards" - research mentioned but no decision |
| 7 | What is the pagination API contract? (page size, cursors, offsets) | Blocker | 🔴 | Backend developer | "ask for 10 pieces of content at a time" - concept clear, implementation TBD |
| 8 | What is the exact unsubscribe flow and API? | Medium | 🟡 | Backend/publishing | "turn this off, turn them on" - mentioned but flow not detailed |
| 9 | Should we use V0, Lovable, or Cursor for initial UI generation? | Medium | 🟡 | Team decision | "V0, lovable, even in codecs, or sorry, cursor... You can drop in images" - multiple options mentioned, no choice made |
| 10 | What is the memory management strategy for infinite scroll? | High | 🟡 | Frontend architect | "if you don't recycle views, you just end up with a lot of memory overload problems... that's part of the magic of a good infinite scroll component" - identified as important, strategy TBD |
| 11 | What is the competitive analysis research deliverable format? | Medium | 🟡 | Product/design | "find projects and products... competitive analysis... app store ratings" - research process described, output format unclear |
| 12 | What are the exact requirements for the lookbook/design collection tool? | Low | ⚠️ | Design lead | "drop things into like a lookbook... I'm using Figma more than anything" - concept mentioned, unclear if building or using Figma |
| 13 | What state management library should we use? (Redux, Zustand, Context) | High | 🟡 | Frontend architect | Not discussed - standard React requirement |

---

## Critical Quotes

### Vision: Dynamic JSON-Driven Interface

**Context:** Core architectural principle for flexibility

> "what we really want is an interface that is dynamic. So whatever the JSON file gives us, we display"

**Implications:** Frontend must handle variable data structures. Cannot hardcode for specific content types. Need robust JSON parsing and dynamic rendering system.

---

### Vision: "Zero to One" Goal

**Context:** Project objective - rapid prototyping

> "how to go from zero to one. That's a lovely catchphrase in Silicon Valley. It means you didn't have anything. Now you've got something to demo"

**Implications:** Focus on getting working prototype quickly. Perfect code less important than demonstrable functionality. Speed is priority.

---

### Technical: Brain-Friendly UI Principles

**Context:** UX design philosophy

> "the brain doesn't like parsing that stuff. It's like, it just, it sees it as a big blob. It doesn't see it as 20 interesting things... brains like to group things... they like to chunk things and they like to summarize"

**Implications:** Information density must be carefully managed. Hierarchy and grouping critical. Don't overwhelm with too much info at once.

---

### Vision: Bubble Onboarding Flow

**Context:** User preference collection strategy

> "we'll start with a, like a screen with a one circle in the middle and a plus sign... you get asked, you know, what do you want in this plus sign?... the AI will then churn a little bit and return with, you know, five different things that are related... display those as like slightly smaller circles, like orbiting the big circle"

**Implications:** Interactive, progressive disclosure approach. Start simple (one topic), expand based on user interaction. Gamified UX to make preference setting engaging.

---

### Technical: Off-the-Shelf Components

**Context:** Development speed strategy

> "we'll find a off the shelf probably a react based component that does that whole feed thing for us... the magic of a good infinite scroll component is it handles the memory right"

**Implications:** Don't build core UI patterns from scratch. Research and use proven libraries for infinite scroll, memory management. Focus custom development on unique features.

---

### Vision: Competitive Analysis Process

**Context:** Research methodology before design

> "try to find projects and products and platforms that are on the market that do exactly this... competitive analysis... go to the ratings of the, on the app store where everyone's bitching about the app... that's the gold right there"

**Implications:** Competitive research is MVP prerequisite. Study competitors' UI/UX. Mine app store reviews for pain points. Adopt best practices, avoid known pitfalls.

---

### Vision: AI-Assisted Development Philosophy

**Context:** Development approach and team skill building

> "we can use English language to the weird language someone wrote 30 years ago to get to the assembly language... we're going to try to leverage AI and become an AI development team"

**Implications:** Embrace AI coding tools (Cursor, V0, etc.). Bridge gap between natural language requirements and code. Team learning objective: master AI-assisted development workflow.

---

### Technical: Design Trends Research

**Context:** Visual design decision making

> "do a search for top design trends of the year that you're in... neon green with hot pink... Webby Awards... drop things into like a lookbook"

**Implications:** Research current design trends. Build visual reference library (lookbook). Use inspiration images with AI generation tools to create unique, contemporary UIs.

---

## Gaps Identified

### 🔴 Blockers (Implementation Cannot Proceed)

- **Backend API Schema** - Need complete API documentation for feed, user data, preferences - **Source: ✓ From conversation** ("calling our server backend API" - mentioned but undefined) - **(See Open Question #1)**

- **AI Data Format** - Need JSON structure for ontology graphs, hierarchical content, related topics - **Source: ✓ From conversation** ("single JSON file... hierarchical" - vague) - **(See Open Question #2)**

- **Authentication Mechanism** - Need login/signup implementation, token management, session handling - **Source: ⚠️ Inferred** ("obviously log in" - mentioned, strategy undefined) - **(See Open Question #3)**

- **Related Topics API** - Specific API for bubble interface to request related concepts - **Source: ✓ From conversation** (behavior described: "get me related ideas... four or five of them" - contract undefined) - **(See Open Question #4)**

- **Pagination API** - Page size, cursor/offset strategy, loading states - **Source: ✓ From conversation** ("ask for 10 pieces of content at a time" - concept clear, details TBD) - **(See Open Question #7)**

### 🟡 Likely Needed (High Probability Required)

- **Component Library Selection** - Which React libraries for infinite scroll, graphs, etc. - **Source: ✓ From conversation** ("find a off the shelf" - identified need, no selection) - **(See Open Question #5)**

- **Design System Choice** - Color palette, typography, spacing system - **Source: ✓ From conversation** (research process described, no decisions made) - **(See Open Question #6)**

- **State Management** - Redux, Zustand, Context API choice - **Source: ⚠️ Inferred** (standard React requirement, not discussed) - **(See Open Question #13)**

- **Routing Strategy** - React Router vs. alternative, route structure - **Source: ⚠️ Inferred** (multi-page app implied, routing not discussed)

- **Memory Management for Infinite Scroll** - View recycling, cleanup strategy - **Source: ✓ From conversation** ("if you don't recycle views, you just end up with a lot of memory overload" - identified, solution TBD) - **(See Open Question #10)**

### ⚠️ Standard Practices (Not Discussed, Typical for Systems)

- **Error Handling and Loading States** - UI feedback for API failures, loading indicators - **Source: ⚠️ Inferred** (standard practice)

- **Responsive Design Strategy** - Mobile vs. desktop layouts, breakpoints - **Source: ⚠️ Inferred** (not discussed but expected)

- **Accessibility Standards** - WCAG compliance, keyboard navigation, screen readers - **Source: ⚠️ Inferred** (standard practice)

- **Testing Strategy** - Unit, integration, e2e testing approach - **Source: ⚠️ Inferred** (quality mentioned in context of SpecKit/TDD, frontend testing not detailed)

- **Build and Deployment** - CI/CD pipeline, environment configs, Docker integration - **Source: ⚠️ Inferred** (Docker mentioned for backend, frontend deployment not discussed)

### Post-MVP Considerations (Future Scope)

- **Lookbook Management Tool** - Design inspiration collection and organization - **Source: ✓ From conversation** ("drop things into like a lookbook... I'm using Figma" - mentioned, unclear if building feature)

- **Advanced Graph Interactions** - Beyond basic visualization (filtering, zooming, etc.) - **Source: ⚠️ Inferred** (basic graph visualization confirmed, advanced features not discussed)

- **Social Features** - Sharing, collaboration implied in broader vision - **Source: ✓ From conversation** (broader vision mentioned: "distributed networks and chat in the future")

- **Mobile App** - Native mobile version beyond responsive web - **Source: ⚠️ Inferred** (not discussed, possible future)

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
- Foundation work can proceed (Phase 0: Research & Setup in Implementation Guide)
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
   - What's the interaction pattern? (API call, WebSocket, polling?)
4. **Define minimal schema** covering discussed use cases
5. **Document in integration contract design doc**
6. **Update this document:** Change 🔴 TBD → ✓ Defined, add schema reference

**Example: Backend API Integration Resolution**

**Before (🔴 TBD):**
```
| **Backend/Core** | Feed content | User selections | 🔴 TBD | JSON mentioned, pagination "10 at a time", no schema |
```

**After resolution (✓ Defined):**
```
| **Backend/Core** | Feed content | User selections | ✓ Defined | API: docs/integrations/backend-api-spec.json - GET /feed?page=1&limit=10. Fields: items[], nextCursor, hasMore. Response: {items: [{id, title, content, tags[]}], pagination: {nextCursor, hasMore}} |
```

**Resolution artifacts created:**
- `docs/integrations/backend-api-spec.json` - Full API specification (OpenAPI/Swagger)
- `docs/integrations/backend-integration-guide.md` - Integration documentation
- Updated Integration Contracts table in this document

---

**When you see ⚠️ Partial (Some Structure Known):**

**What it means:** Conversation discussed some structure but details incomplete

**IMPORTANT:** Check the "Known Structure" column - don't ignore this!

**Resolution process:**
1. **Start with known structure** (extract from Known Structure column)
2. **Identify gaps** (see "Unknown/TBD" column or Open Questions)
3. **Fill gaps through:**
   - Follow-up conversation with backend/AI module owner
   - Review existing similar APIs
   - Technical research (REST best practices, GraphQL standards)
4. **Document complete schema**
5. **Update status:** ⚠️ Partial → ✓ Defined

**Example: AI Module Integration Resolution**

**What we know (from conversation):**
- Single JSON file format
- Ontology structure: nodes + relationships
- Example: bees → "gets nectar from" → flowers
- Related topics: "four or five" per request

**What's unknown:**
- Exact JSON schema for graph data
- Node/edge field names
- Related topics API endpoint

**Resolution action:**
1. Use ontology example as starting point
2. Design JSON schema: `{ nodes: [{id, label, type}], edges: [{source, target, relationship}] }`
3. Prototype related topics API endpoint: `POST /api/related-topics { topic: string, count: number }`
4. Validate with AI module team
5. Document complete contract

---

### How to Prioritize and Resolve Open Questions

**Resolution Order (by Priority):**

**1️⃣ All 🔴 Blockers First** (Implementation cannot proceed)
- These block multiple phases of development
- Usually API schemas, auth mechanisms, core architectural decisions
- **Action:** Schedule resolution meetings ASAP, assign DRIs (Directly Responsible Individuals)

**2️⃣ 🟡 Important Next** (Affects design but has workarounds)
- Can stub these initially but need real answers before production
- Examples: Component library selection, design system, state management
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
   - Integration Contracts (if API/schema definition)
5. **Update Open Questions:** Mark as ✅ Resolved with reference to where documented

---

### How to Address Identified Gaps

**Gaps are categorized by urgency. Treat each category differently:**

**🔴 Blockers (Cannot Implement Without):**

**What they are:** Missing API contracts, undefined schemas, fundamental unknowns

**Resolution approach:**
- **Technical design session** with backend/AI teams
- **API contract definition** workshops
- **Document in:** Integration contracts, API specs, OpenAPI/Swagger docs

**Example gaps from this document:**
- Backend API schema → API specification needed (Open Question #1)
- AI data format → JSON schema definition needed (Open Question #2)
- Authentication mechanism → Auth design doc needed (Open Question #3)

**Timeline:** Resolve before Phase 1 implementation starts

---

**🟡 Likely Needed (High Probability Required):**

**What they are:** Production requirements not discussed but standard for this system type

**Resolution approach:**
- **Engineering team discussion** on approach
- **Industry best practices research** (how do similar systems handle this?)
- **Document in:** Component library decisions, design system docs, architecture decisions

**Example gaps from this document:**
- Component library selection → Research and evaluate options (Open Question #5)
- Design system choice → Design research and trend analysis (Open Question #6)
- State management → Architecture pattern decision (Open Question #13)

**Timeline:** Resolve during Phase 0 research and implementation phases

---

**⚠️ Standard Practices (Industry-Standard Requirements):**

**What they are:** Assumed requirements for production systems (testing, accessibility, performance, etc.)

**Resolution approach:**
- **Reference architecture patterns** from similar projects
- **Existing implementation review** (what do we already do for other modules?)
- **Document in:** Testing strategy, accessibility guidelines, performance benchmarks

**Example gaps from this document:**
- Error handling and loading states → Standard React patterns
- Responsive design strategy → Mobile-first approach
- Accessibility standards → WCAG 2.1 AA compliance
- Testing strategy → Jest + React Testing Library

**Timeline:** Address during implementation (not blocking initial development)

---

### Workflow: From TBDs to Implementation-Ready

**Step 1: Audit Current State**
- [ ] Count 🔴 Blockers in Open Questions (Currently: 5 blockers - #1, #2, #3, #4, #7)
- [ ] Count 🔴 TBD in Integration Contracts (Currently: 4 TBD - all integrations)
- [ ] Count 🔴 Blockers in Gaps Identified (Currently: 5 blockers)
- [ ] Total blockers = sum of above

**Step 2: Prioritize Blocker Resolution**
- [ ] Create resolution task for each 🔴 Blocker
- [ ] Assign DRI (Directly Responsible Individuals)
- [ ] Set deadlines (Phase 0 completion target)
- [ ] Track in project management tool

**Step 3: Execute Resolution**
- [ ] Hold design sessions, stakeholder meetings, research spikes
- [ ] Document all decisions with rationale
- [ ] Create integration contracts, API specs, design docs
- [ ] Update this document as items resolve

**Step 4: Validate Readiness**
- [ ] All MVP-critical 🔴 Blockers → ✅ Resolved
- [ ] All Integration Contracts → ✓ Defined (or documented workaround)
- [ ] All ⚠️ Unclear MVP Features → ✓ Confirmed or 🟡 Post-MVP
- [ ] Team consensus: "We can start implementation"

**Step 5: Handoff to Implementation**
- [ ] Mark document status: "Ready for Implementation"
- [ ] Reference in Implementation Guide (Document 2)
- [ ] Begin Phase 0: Research & Setup

---

### Example: Complete Resolution Flow

**Starting State (from this document):**

**Open Question #1:** What is the exact backend API schema for feed content and user data?
- **Status:** 🔴 Blocker
- **Who:** Backend developer
- **Context:** "calling our server backend API" - mentioned but undefined

**Integration Contract - Backend/Core:**
- **Status:** 🔴 TBD
- **Known:** JSON format, pagination "10 at a time"
- **Unknown:** Schema, endpoints, auth

**Gap - Backend API Schema:**
- **Category:** 🔴 Blocker
- **Description:** Cannot fetch/display content without API contract

---

**Resolution Process:**

1️⃣ **Identify DRI:** Backend developer (Alex)
2️⃣ **Schedule meeting:** Frontend lead + Alex API design session
3️⃣ **Design session output:**
   - REST API: `/api/feed`, `/api/user/preferences`, `/api/topics/related`
   - Pagination: cursor-based with `nextCursor` field
   - Schema defined: OpenAPI 3.0 spec created
   - Auth: JWT tokens in Authorization header
4️⃣ **Update this document:**
   - Open Question #1: ✅ Resolved (reference: docs/integrations/backend-api-spec.yaml)
   - Integration Contract - Backend/Core: ✓ Defined (API spec documented)
   - Gap removed from Blockers section
5️⃣ **Implementation Guide updated:**
   - Phase 1 blocker removed
   - Task P1.4 updated with API reference

---

**Result State:**

**Open Questions:** 12 total (4 blockers) ← was 13 total (5 blockers)

**Integration Contracts:**
```
| **Backend/Core** | Feed content, User data, Related topics | User selections, preferences | ✓ Defined | API spec: docs/integrations/backend-api-spec.yaml - REST endpoints defined, JWT auth, cursor pagination |
```

**Gaps Identified - Blockers:** 4 remaining ← was 5

**Implementation Guide - Phase 1:**
- ✅ Can proceed (blocker resolved)
- All API integration tasks reference backend-api-spec.yaml

---

### Quick Reference: Resolution Checklist

**For each 🔴 TBD Integration Contract:**
- [ ] Review conversation context (Known Structure column, Open Questions)
- [ ] Identify who can define schema (backend/AI module owner)
- [ ] Extract any discussed structure (don't ignore partial info!)
- [ ] Schedule design session to define complete API contract
- [ ] Document in OpenAPI/Swagger spec or integration doc
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
- Integration contract docs (API specs for Backend, AI, Publishing modules)
- Technical design docs (for architectural decisions: component libraries, state management, auth)
- Updated Implementation Guide (Phase 0 unblocked)

**Next step:** Begin Implementation Phase 0 (Research & Setup)

---

**End of Document**
