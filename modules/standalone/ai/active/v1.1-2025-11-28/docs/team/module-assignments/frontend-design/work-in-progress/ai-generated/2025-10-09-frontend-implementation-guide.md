# Frontend Module: Implementation Guide

**Purpose:** Actionable implementation roadmap for Frontend module
**Derived From:** 2025-10-09-frontend-decisions-agreements.md (Document 1)
**Created:** 2025-10-09
**Status:** Draft - Awaiting Blocker Resolution

---

## Quick Start

### What You're Building

Research discovery platform with dynamic JSON-driven UI, featuring interactive bubble onboarding, hierarchical content browsing, ontology graph visualization, and infinite-scroll feed.

**Core Functionality:**
- 3-panel IDE-style layout (left menu, center content, right filters) ✓ Extracted (from Doc 1 MVP Features)
- Bubble onboarding interface for topic selection ✓ Extracted (from Doc 1 MVP Features)
- Infinite scroll feed with TikTok-style UX ✓ Extracted (from Doc 1 MVP Features)
- Graph visualization for ontology relationships ✓ Extracted (from Doc 1 MVP Features)
- Yahoo-style hierarchical content browser ✓ Extracted (from Doc 1 MVP Features)
- Topic selection with checkboxes ✓ Extracted (from Doc 1 MVP Features)

**Out of Scope (this phase):**
- Lookbook management tool ⚠️ Unclear (from Doc 1 - mentioned, unclear if building)
- Advanced graph interactions (filtering, zooming) ⚠️ Inferred (basic graph only)
- Social/sharing features 🟡 Post-MVP (from Doc 1 - future vision)
- Native mobile app ⚠️ Inferred (responsive web only)

### Time Estimate

**Total Estimated Time:** 60-80 hours

**Phase Breakdown:**
- Phase 0 (Research & Setup): 10-12 hours
- Phase 1 (Core Layout & Navigation): 12-16 hours
- Phase 2 (Bubble Onboarding): 10-14 hours
- Phase 3 (Feed Interface): 12-16 hours
- Phase 4 (Graph & Hierarchy Views): 12-16 hours
- Phase 5 (Integration & Polish): 4-6 hours

**Note:** Estimates assume React familiarity, blockers resolved before implementation, design assets ready.

### Before You Start

### Pre-Implementation Checklist

**Environment Setup:**
- [ ] Node.js installed (v16+ recommended) (`node --version`)
- [ ] Cursor IDE installed and configured
- [ ] React DevTools browser extension installed
- [ ] Git configured (`git config --global user.name`)
- [ ] Project repository cloned locally
- [ ] Access to: Design assets, Figma mockups, backend API documentation (if available)

**Document Review:**
- [ ] Document 1 (Decisions & Agreements) read completely
- [ ] All Technical Decisions understood (React+Vite, Cytoscape, dynamic JSON, component library approach)
- [ ] All Integration Contracts reviewed (Backend, AI, Publishing, SpecKit)
- [ ] All Open Questions noted (especially 🔴 Blockers #1, #2, #3, #4, #7)
- [ ] MVP Features scope clear (know what's in/out)
- [ ] Section 8: "Using This Document" reviewed (understand resolution workflow)

**Blocker Resolution Status:**
- [ ] Open Question #1 (Backend API schema): [✅ Resolved / ⚠️ In Progress / ❌ Not Started]
- [ ] Open Question #2 (AI JSON format): [✅ Resolved / ⚠️ In Progress / ❌ Not Started]
- [ ] Open Question #3 (Authentication mechanism): [✅ Resolved / ⚠️ In Progress / ❌ Not Started]
- [ ] Open Question #4 (Related topics API): [✅ Resolved / ⚠️ In Progress / ❌ Not Started]
- [ ] Open Question #7 (Pagination API): [✅ Resolved / ⚠️ In Progress / ❌ Not Started]

**If any blocker is ❌ Not Started or ⚠️ In Progress:**
→ **STOP:** Resolve blockers before proceeding to Phases 2-5
→ **OK to start:** Phase 0 (Research & Setup) and Phase 1 (Core Layout) partially

**Team Alignment:**
- [ ] Kickoff meeting held (roles, timeline, communication channels)
- [ ] Technical lead assigned for Frontend module
- [ ] Code review process defined
- [ ] Deployment pipeline access confirmed (or plan in place)
- [ ] Integration points identified: contacts for Backend, AI, Publishing, Database teams

**Communication Setup:**
- [ ] Slack/Discord channel for Frontend module
- [ ] Access to: Backend team, AI module team, Design team
- [ ] Escalation path defined (who to ask when stuck)
- [ ] Weekly design review meeting scheduled (if applicable)

**Design Prerequisites (for Phase 0):**
- [ ] Design tools access: Figma, lookbook tool (or equivalent)
- [ ] Webby Awards research list prepared
- [ ] Competitive analysis target list (10+ products)

**Ready to Begin:**
- [ ] All above items checked
- [ ] Phase 0 can start immediately (no blockers)
- [ ] Phases 2-5 awaiting blocker resolution per Implementation Readiness Matrix

### Critical Path Overview

**Dependency Flow:**
1. **Phase 0: Research & Setup** → Competitive analysis, design trends, environment setup
2. **Phase 1: Core Layout** → 3-panel structure, routing, navigation (depends on Phase 0)
3. **Phase 2: Bubble Onboarding** → Interactive topic selection UI (depends on Phase 1)
4. **Phase 3: Feed Interface** → Infinite scroll content display (depends on Phase 1)
5. **Phase 4: Graph & Hierarchy** → Visualization components (depends on Phase 1)
6. **Phase 5: Integration** → Connect all views, polish UX (depends on all previous)

**Blockers to Watch:**
- 🔴 Backend API schema - Blocks Phase 3 (feed data), Phase 2 (related topics) - Doc 1 Open Questions #1, #4
- 🔴 AI data format - Blocks Phase 4 (graph, hierarchy rendering) - Doc 1 Open Question #2
- 🔴 Authentication - Blocks Phase 1 (login/signup), Phase 5 (user data) - Doc 1 Open Question #3
- 🔴 Pagination API - Blocks Phase 3 (infinite scroll implementation) - Doc 1 Open Question #7

---

## Implementation Readiness Matrix

**Purpose:** Quick scan of which phases can start vs. blocked

| Phase | Can Start? | Blockers | Dependencies | Confidence |
|-------|------------|----------|--------------|------------|
| **Phase 0: Research & Setup** | ✅ Yes | None | None | **High** - Competitive analysis, design research, standard setup |
| **Phase 1: Core Layout** | ⚠️ Partial | - Auth mechanism (OQ #3) | Phase 0 | **Medium** - Layout can be built, login blocked until auth defined |
| **Phase 2: Bubble Onboarding** | ❌ No | - Related topics API (OQ #4) | Phase 0, Phase 1 | **Low** - Core functionality blocked until API defined |
| **Phase 3: Feed Interface** | ❌ No | - Backend feed API (OQ #1)<br>- Pagination API (OQ #7) | Phase 0, Phase 1 | **Low** - Cannot fetch/display content without API |
| **Phase 4: Graph & Hierarchy** | ❌ No | - AI JSON format (OQ #2) | Phase 0, Phase 1 | **Low** - Cannot render dynamic data without schema |
| **Phase 5: Integration & Polish** | ❌ No | - All Phase 1-4 blockers | All prior phases | **Low** - Fully blocked until integrations defined |

**Key Takeaways:**
- ✅ **Can start immediately:** Phase 0 (Research & Setup) - no blockers
- ⚠️ **Requires planning:** Phase 1 (Core Layout) - can build layout, but login blocked
- ❌ **Fully blocked:** Phases 2, 3, 4, 5 - resolve Document 1 Open Questions first

**Recommended Sequence:**
1. Start Phase 0 immediately (competitive analysis, design research, project setup)
2. Build Phase 1 layout structure (skip login/signup until auth resolved)
3. Resolve all 🔴 blockers (Open Questions #1, #2, #3, #4, #7)
4. Begin Phases 2, 3, 4 (can work in parallel once unblocked)
5. Complete with Phase 5 integration

---

## Phase 0: Research & Setup

**Goal:** Complete competitive analysis, design research, and environment setup before coding

**Time Estimate:** 10-12 hours

**Provenance Summary:**
- ✓ Extracted: 2 tasks (Competitive analysis, Design trends research from Doc 1 Critical Quotes)
- ⚠️ Inferred: 3 tasks (React setup, component library research, Cursor IDE - standard practice)
- 🔴 Unknown: 0 tasks (no blockers)
- **Total tasks:** 5 (40% extracted, 60% inferred)

**Dependencies:** None
**Blockers:** None - can start immediately
**Confidence:** High - Research and standard setup tasks

---

### P0.1: Competitive Analysis 👤 Human-design

**What:** Research 10+ similar products, analyze UI/UX patterns, pain points

**Learning Objectives:**
- Identify common UI patterns in research/discovery tools
- Understand user pain points from app store reviews
- Discover unique differentiators for our product
- Map competitive feature sets

**Tasks:**
- [ ] Identify 10+ competitor products ✓ Extracted (from Doc 1 Critical Quote on competitive analysis)
- [ ] Screenshot main interfaces ⚠️ Inferred (standard research practice)
- [ ] Review app store ratings for pain points ✓ Extracted (from Doc 1 - "go to the ratings... where everyone's bitching... that's the gold")
- [ ] Document UI patterns that work ⚠️ Inferred
- [ ] Create comparison matrix ⚠️ Inferred

**Provenance:** ✓ Extracted - Competitive analysis explicitly required in Doc 1: "try to find projects and products and platforms that are on the market that do exactly this... competitive analysis"

**Why human:** Requires synthesis, judgment about user needs, strategic thinking about differentiation

**Time:** 3-4 hours

---

### P0.2: Design Trends Research 👤 Human-design

**What:** Research current design trends, build lookbook of visual inspiration

**Learning Objectives:**
- Understand 2025 design trends
- Identify color schemes and visual styles
- Collect reference materials for AI-assisted design

**Tasks:**
- [ ] Research "top design trends 2025" ✓ Extracted (from Doc 1: "do a search for top design trends of the year that you're in")
- [ ] Review Webby Awards for inspiration ✓ Extracted (from Doc 1)
- [ ] Collect visual references (billboards, cereal boxes, non-web) ✓ Extracted (from Doc 1 - "get like billboard ads... backs of cereal boxes")
- [ ] Create lookbook in Figma ✓ Extracted (from Doc 1 - "drop things into like a lookbook... I'm using Figma")
- [ ] Identify color schemes (note: "neon green with hot pink" current trend) ✓ Extracted (from Doc 1)

**Provenance:** ✓ Extracted - Design research process from Doc 1 Critical Quote: "top design trends of the year... Webby Awards... drop things into like a lookbook"

**Why human:** Visual curation, aesthetic judgment, understanding design principles

**Time:** 3-4 hours

---

### P0.3: React + Vite Project Setup 🤖 Agent-ready

**What:** Initialize React project with Vite, configure tooling

**Tasks:**
- [ ] Create Vite React project ✓ Extracted (from Doc 1 Tech Decision #1)
- [ ] Configure TypeScript (if using) ⚠️ Inferred (best practice)
- [ ] Set up ESLint and Prettier ⚠️ Inferred (code quality)
- [ ] Configure routing (React Router) ⚠️ Inferred (multi-view app)
- [ ] Set up environment variables ⚠️ Inferred (API endpoints)

**Provenance:** ✓ Extracted - React + Vite from Doc 1 Technical Decision #1: "We're going to be using React... with Vite"

**Could ask agent:**
"Create a new Vite React project with TypeScript. Configure React Router for multi-view navigation, ESLint for code quality, and environment variable support for API endpoints. Create basic project structure with /components, /pages, /utils, /services directories."

**Learning trade-off:** Low (standard project scaffolding - agent saves 1 hour)

**Time:** 1 hour

---

### P0.4: Component Library Research 👤 Human-design

**What:** Identify and select React component libraries for infinite scroll, graphs

**Tasks:**
- [ ] Research infinite scroll React libraries ✓ Extracted (from Doc 1 - "find a off the shelf probably a react based component")
- [ ] Research Cytoscape.js integration ✓ Extracted (from Doc 1 Tech Decision #2)
- [ ] Evaluate memory management features ✓ Extracted (from Doc 1 - "if you don't recycle views... memory overload")
- [ ] Select state management library (Redux/Zustand/Context) ⚠️ Inferred (Doc 1 Open Question #13)
- [ ] Document selected libraries and rationale ⚠️ Inferred

**Provenance:** ✓ Extracted from Doc 1 Open Question #5 and Technical Decision #4 (component library approach)

**Why human:** Requires evaluation of library quality, community support, project fit

**Time:** 2-3 hours

---

### P0.5: Cursor IDE Setup and Configuration 👤 Human-design

**What:** Configure Cursor IDE for AI-assisted development

**Tasks:**
- [ ] Install Cursor IDE ✓ Extracted (from Doc 1 Tech Decision #5)
- [ ] Configure AI settings ⚠️ Inferred
- [ ] Set up project context ⚠️ Inferred
- [ ] Learn predictive completion features ✓ Extracted (from Doc 1 - "it would give you suggestions... hit the tab key")

**Provenance:** ✓ Extracted - Cursor usage from Doc 1 Technical Decision #5

**Why human:** Requires learning tool features, understanding AI-assisted workflows

**Time:** 1 hour

---

## Phase 1: Core Layout & Navigation

**Goal:** Build 3-panel IDE-style layout with routing and navigation

**Dependencies:**
- Phase 0 complete (research, setup done)
- 🔴 Auth mechanism defined (for login/signup) - Doc 1 Open Question #3

**Time Estimate:** 12-16 hours

### P1.1: 3-Panel Layout Structure 🤖 Agent-ready

**What:** Implement left menu, center content, right filter panels

**Tasks:**
- [ ] Create layout component with CSS Grid/Flexbox ✓ Extracted (from Doc 1 MVP Feature)
- [ ] Left panel: navigation and menu ✓ Extracted (from Doc 1 - "column on the left... major subsections")
- [ ] Center panel: main content area ✓ Extracted (from Doc 1)
- [ ] Right panel: filter controls ✓ Extracted (from Doc 1 - "right-hand side... dial in the values")
- [ ] Implement responsive breakpoints ⚠️ Inferred

**Provenance:** ✓ Extracted from Doc 1 MVP Features and Critical Quote: "column on the left... And then on the right-hand side, what we'll do is that'll be our filter"

**Could ask agent:**
"Create a 3-panel IDE-style layout component in React. Left panel (250px fixed width) for navigation, center panel (flex-grow) for main content, right panel (300px fixed width) for filters. Use CSS Grid for layout. Make responsive: collapse side panels on mobile. Use semantic HTML."

**Learning trade-off:** Low (standard layout pattern - agent saves 2 hours)

**Time:** 2 hours

---

### P1.2: Navigation Menu (Left Panel) 👤 Human-design

**What:** Build left navigation with Lab views section and user preferences

**Tasks:**
- [ ] Create menu structure ✓ Extracted (from Doc 1 - "broken into subsections... Your section")
- [ ] Add Lab views section ✓ Extracted (from Doc 1 - "we'll have a section that's lab")
- [ ] Add user preferences section ⚠️ Inferred
- [ ] Implement menu item click handling ⚠️ Inferred
- [ ] Active state styling ⚠️ Inferred

**Provenance:** ✓ Extracted from Doc 1 Critical Quote: "left-hand column is like broken into subsections... And so like the top level hierarchy... we'll have a section that's lab"

**Why human:** UX decisions about menu organization, visual design, interaction patterns

**Time:** 3-4 hours

---

### P1.3: Routing Setup

**What:** Configure React Router for multi-view navigation

**Tasks:**
- [ ] Define routes for each view ⚠️ Inferred
- [ ] Bubble onboarding route ✓ Extracted (from Doc 1 MVP)
- [ ] Feed view route ✓ Extracted (from Doc 1 MVP)
- [ ] Graph view route ✓ Extracted (from Doc 1 MVP)
- [ ] Hierarchy browser route ✓ Extracted (from Doc 1 MVP)
- [ ] Implement route transitions ⚠️ Inferred

**Provenance:** ✓ Extracted - Multiple views from Doc 1 MVP Features, routing inferred as standard requirement

**Success Criteria:**
- [ ] All views accessible via routes
- [ ] Navigation updates route correctly
- [ ] Browser back/forward works

---

### P1.4: Login/Signup Flow 🔴 BLOCKED

**What:** Implement authentication UI and flow

**Tasks:**
- [ ] Create login form 🔴 BLOCKED (auth mechanism undefined - Doc 1 Open Question #3)
- [ ] Create signup form 🔴 BLOCKED
- [ ] Implement auth state management 🔴 BLOCKED
- [ ] Handle authentication tokens 🔴 BLOCKED
- [ ] Protected route logic 🔴 BLOCKED

**Provenance:** ✓ Extracted from Doc 1 MVP Features: "they need to be able to, you know, obviously log in so that they can make custom settings"

**Blockers:**
- Cannot implement without auth strategy (JWT, OAuth, session-based?)
- Need backend API contract for login/signup endpoints

**Success Criteria:**
- [ ] (BLOCKED) User can sign up
- [ ] (BLOCKED) User can log in
- [ ] (BLOCKED) Auth state persists

---

## Phase 2: Bubble Onboarding Interface

**Goal:** Build interactive bubble UI for initial topic selection

**Dependencies:**
- Phase 1 complete (layout, routing ready)
- 🔴 Related topics API defined - Doc 1 Open Question #4

**Time Estimate:** 10-14 hours

### P2.1: Initial Bubble UI 👤 Human-design

**What:** Create starting screen with single circle and plus sign

**Tasks:**
- [ ] Design bubble component (circle with text/icon) ✓ Extracted (from Doc 1 Critical Quote)
- [ ] Create canvas for bubble layout ⚠️ Inferred
- [ ] Implement central "+" button ✓ Extracted (from Doc 1 - "one circle in the middle and a plus sign")
- [ ] Add input modal for topic entry ✓ Extracted (from Doc 1 - "you get asked, you know, what do you want in this plus sign")
- [ ] Bubble animation (orbit pattern) ✓ Extracted (from Doc 1 - "slightly smaller circles, like orbiting the big circle")

**Provenance:** ✓ Extracted from Doc 1 Critical Quote: "we'll start with a, like a screen with a one circle in the middle and a plus sign... you get asked, you know, what do you want in this plus sign"

**Why human:** Visual design, animation timing, UX feel require human judgment and iteration

**Time:** 4-5 hours

---

### P2.2: Related Topics API Integration 🔴 BLOCKED

**What:** Request and display related topics from backend/AI

**Tasks:**
- [ ] Create API service for related topics 🔴 BLOCKED (API undefined - Doc 1 Open Question #4)
- [ ] Request "4-5 related ideas" per user input 🔴 BLOCKED
- [ ] Display as orbiting bubbles 🔴 BLOCKED
- [ ] Handle API errors/loading ⚠️ Inferred

**Provenance:** ✓ Extracted from Doc 1 Critical Quote: "send a message to the backend saying, get me some research results or no, better... get me related ideas... I want about four or five of them"

**Blockers:**
- API endpoint undefined
- Request/response schema unknown
- AI processing time/async handling unclear

**Success Criteria:**
- [ ] (BLOCKED) User types topic
- [ ] (BLOCKED) Related topics fetched
- [ ] (BLOCKED) Bubbles display results

---

### P2.3: Bubble Interaction Logic

**What:** Implement click (like) and double-click (expand) interactions

**Tasks:**
- [ ] Single click: add green circle (like) ✓ Extracted (from Doc 1 - "click once and it's like a green circle around the bubble")
- [ ] Double click: add red circle or expand ✓ Extracted (from Doc 1 - "click on one twice and it gets a little smaller and a red circle... means you definitely don't want any of that")
- [ ] Track user selections (state) ⚠️ Inferred
- [ ] Send feedback to backend ⚠️ Inferred

**Provenance:** ✓ Extracted from Doc 1 Critical Quote about Apple Music/Spotify-style onboarding

**Success Criteria:**
- [ ] Visual feedback on click
- [ ] User preferences tracked
- [ ] Can proceed to main app

---

## Phase 3: Feed Interface

**Goal:** Implement infinite scroll feed with TikTok-style UX

**Dependencies:**
- Phase 1 complete (center panel ready)
- 🔴 Backend feed API defined - Doc 1 Open Questions #1, #7

**Time Estimate:** 12-16 hours

### P3.1: Infinite Scroll Component 🤖 Agent-ready

**What:** Integrate off-the-shelf React infinite scroll library

**Tasks:**
- [ ] Install selected library (from P0.4 research) ✓ Extracted (from Doc 1 Tech Decision #4)
- [ ] Configure pagination (10 items per request) ✓ Extracted (from Doc 1 - "ask for 10 pieces of content at a time")
- [ ] Implement view recycling ✓ Extracted (from Doc 1 - "if you don't recycle views, you just end up with a lot of memory overload")
- [ ] Add pull-to-refresh ✓ Extracted (from Doc 1 - "pull down to reload")
- [ ] Loading states ⚠️ Inferred

**Provenance:** ✓ Extracted from Doc 1 Technical Decision #4 and Critical Quote about feed UX

**Could ask agent:**
"Integrate React infinite scroll library (react-infinite-scroll-component or similar). Configure to fetch 10 items per page, implement view recycling for memory efficiency, add pull-to-refresh. Handle loading states and end-of-content. Connect to API service (placeholder for now)."

**Learning trade-off:** Low (library integration - agent saves 2-3 hours)

**Time:** 2-3 hours

---

### P3.2: Feed Item Component 👤 Human-design

**What:** Design and build feed card/item component

**Tasks:**
- [ ] Design feed item layout ⚠️ Inferred (from lookbook research)
- [ ] Content rendering (dynamic JSON) ✓ Extracted (from Doc 1 - "whatever the JSON file gives us, we display")
- [ ] Side action buttons (share, save, etc.) ✓ Extracted (from Doc 1 - "interface elements for the content go on the sides")
- [ ] Swipe/snap interaction ✓ Extracted (from Doc 1 - "swipe and then snap and hold")
- [ ] Visual polish ⚠️ Inferred

**Provenance:** ✓ Extracted from Doc 1 Critical Quote about feed UX patterns

**Why human:** Visual design, interaction feel, content presentation require human judgment

**Time:** 4-5 hours

---

### P3.3: Feed Data Service 🔴 BLOCKED

**What:** Create service to fetch feed content from backend

**Tasks:**
- [ ] Create API service module 🔴 BLOCKED (API schema undefined - Doc 1 Open Question #1)
- [ ] Implement pagination logic 🔴 BLOCKED (pagination API TBD - Doc 1 Open Question #7)
- [ ] Handle API errors ⚠️ Inferred
- [ ] Caching strategy ⚠️ Inferred

**Provenance:** ✓ Extracted from Doc 1: "It'll just be calling our server backend API asking for the content"

**Blockers:**
- Backend API schema unknown
- Pagination contract (cursor vs. offset, page size) undefined

**Success Criteria:**
- [ ] (BLOCKED) Fetches content successfully
- [ ] (BLOCKED) Handles pagination
- [ ] (BLOCKED) Error states managed

---

## Phase 4: Graph & Hierarchy Views

**Goal:** Implement ontology graph visualization and hierarchy browser

**Dependencies:**
- Phase 1 complete (layout ready)
- 🔴 AI data format defined - Doc 1 Open Question #2

**Time Estimate:** 12-16 hours

### P4.1: Cytoscape Graph Visualization 🤖 Agent-ready

**What:** Integrate Cytoscape.js for ontology graph rendering

**Tasks:**
- [ ] Install Cytoscape.js ✓ Extracted (from Doc 1 Tech Decision #2)
- [ ] Create graph component wrapper ⚠️ Inferred
- [ ] Configure node/edge rendering ✓ Extracted (from Doc 1 - "ontology mapping... two objects together and the line between them, there's a little label")
- [ ] Implement basic interactions (pan, zoom) ⚠️ Inferred
- [ ] Style nodes and edges ⚠️ Inferred (from lookbook)

**Provenance:** ✓ Extracted from Doc 1 Technical Decision #2 and Critical Quote on ontology graphs

**Could ask agent:**
"Integrate Cytoscape.js into React. Create a graph visualization component that renders nodes (entities) and edges (relationships with labels). Example: 'bees' node connected to 'flowers' node with edge labeled 'gets nectar from'. Enable pan/zoom interactions. Style nodes as circles with text labels, edges as arrows with relationship text."

**Learning trade-off:** Low (library integration, clear requirements - agent saves 2 hours)

**Time:** 2-3 hours

---

### P4.2: Hierarchy Browser 👤 Human-design

**What:** Build Yahoo-style directory drilling interface

**Tasks:**
- [ ] Create expandable tree/list component ✓ Extracted (from Doc 1 MVP Feature)
- [ ] Multi-level text hierarchy ✓ Extracted (from Doc 1 - "text with the secondary level... smaller text underneath it")
- [ ] Click to expand/drill down ✓ Extracted (from Doc 1)
- [ ] Topic checkboxes ✓ Extracted (from Doc 1 - "little tick box next to the item")
- [ ] Track selected topics ⚠️ Inferred

**Provenance:** ✓ Extracted from Doc 1 Critical Quote: "Back in the day, Yahoo was a big deal... directory, which was just text with the secondary level... you could click on the text or you could click on the subtext"

**Why human:** UX for information density, visual hierarchy, interaction patterns require human judgment per Doc 1 principle: "brains like to group things... chunk things"

**Time:** 4-5 hours

---

### P4.3: Dynamic JSON Rendering 🔴 BLOCKED

**What:** Parse and render whatever JSON structure AI provides

**Tasks:**
- [ ] Create dynamic renderer component 🔴 BLOCKED (JSON schema undefined - Doc 1 Open Question #2)
- [ ] Handle variable data structures 🔴 BLOCKED
- [ ] Recursive rendering for nested data 🔴 BLOCKED
- [ ] Error handling for malformed JSON ⚠️ Inferred

**Provenance:** ✓ Extracted from Doc 1 Technical Decision #3: "what we really want is an interface that is dynamic. So whatever the JSON file gives us, we display"

**Blockers:**
- JSON schema from AI module undefined
- Hierarchical structure format unknown
- Ontology graph format unknown

**Success Criteria:**
- [ ] (BLOCKED) Renders variable JSON
- [ ] (BLOCKED) Handles nested structures
- [ ] (BLOCKED) Graceful error handling

---

## Phase 5: Integration & Polish

**Goal:** Connect all components, implement state management, polish UX

**Dependencies:**
- All previous phases complete
- 🔴 ALL BLOCKERS RESOLVED

**Time Estimate:** 4-6 hours

### P5.1: State Management Implementation

**What:** Implement global state (Redux/Zustand/Context)

**Tasks:**
- [ ] Set up state management library (from P0.4 selection) ⚠️ Inferred (Doc 1 Open Question #13)
- [ ] User state (auth, preferences) ⚠️ Inferred
- [ ] Selected topics state ✓ Extracted (from Doc 1)
- [ ] Feed state (pagination, cache) ⚠️ Inferred
- [ ] UI state (active view, filters) ⚠️ Inferred

**Provenance:** ✓ Extracted (topic selection) + ⚠️ Inferred (state management best practice)

**Success Criteria:**
- [ ] State persists across views
- [ ] Selected topics accessible globally
- [ ] User preferences maintained

---

### P5.2: Filter Panel (Right Side)

**What:** Implement filter controls for selected view

**Tasks:**
- [ ] Create filter UI components ✓ Extracted (from Doc 1 - "dial in the values for it")
- [ ] Context-aware filters (change per view) ✓ Extracted (from Doc 1)
- [ ] Apply filters to feed/graph/hierarchy ⚠️ Inferred
- [ ] Filter state management ⚠️ Inferred

**Provenance:** ✓ Extracted from Doc 1 Critical Quote: "right-hand side, what we'll do is that'll be our filter for like whatever you've selected, you can fine-tune the results"

**Success Criteria:**
- [ ] Filters update based on active view
- [ ] Filters apply to displayed content
- [ ] Filter state persists

---

### P5.3: UX Polish & Accessibility

**What:** Final UX improvements, accessibility, responsiveness

**Tasks:**
- [ ] Add loading states and skeletons ⚠️ Inferred
- [ ] Error boundary implementation ⚠️ Inferred
- [ ] Keyboard navigation ⚠️ Inferred (accessibility standard)
- [ ] Screen reader support ⚠️ Inferred (accessibility standard)
- [ ] Responsive design testing ⚠️ Inferred
- [ ] Performance optimization ⚠️ Inferred

**Provenance:** ⚠️ Inferred (standard UX/accessibility practices, not discussed in Doc 1)

**Success Criteria:**
- [ ] WCAG 2.1 AA compliance
- [ ] Works on mobile/tablet/desktop
- [ ] Smooth animations, no jank

---

## Automation Opportunities

**How to Use This Section:**
- Tasks marked 🤖 Agent-ready can be delegated
- Consider learning trade-offs before delegating
- Review agent output carefully

### High-Value Automations

#### P0.3: React + Vite Project Setup

**Time Savings:** 1 hour
**Learning Trade-off:** Low (boilerplate)

**Could ask agent:**
"Create a new Vite React project with TypeScript. Configure React Router for multi-view navigation, ESLint for code quality, and environment variable support for API endpoints. Create basic project structure with /components, /pages, /utils, /services directories."

---

#### P1.1: 3-Panel Layout Structure

**Time Savings:** 2 hours
**Learning Trade-off:** Low (standard pattern)

**Could ask agent:**
"Create a 3-panel IDE-style layout component in React. Left panel (250px fixed width) for navigation, center panel (flex-grow) for main content, right panel (300px fixed width) for filters. Use CSS Grid for layout. Make responsive: collapse side panels on mobile."

---

#### P3.1: Infinite Scroll Component

**Time Savings:** 2-3 hours
**Learning Trade-off:** Low (library integration)

**Could ask agent:**
"Integrate React infinite scroll library (react-infinite-scroll-component). Configure to fetch 10 items per page, implement view recycling for memory efficiency, add pull-to-refresh. Handle loading states and end-of-content."

---

#### P4.1: Cytoscape Graph Visualization

**Time Savings:** 2 hours
**Learning Trade-off:** Low (library integration)

**Could ask agent:**
"Integrate Cytoscape.js into React. Create graph visualization component that renders nodes (entities) and edges (relationships with labels). Enable pan/zoom. Style nodes as circles with text labels, edges as arrows with relationship text."

---

### Do NOT Automate (👤 Human-design tasks)

- **P0.1: Competitive Analysis** - Requires strategic thinking, user empathy
- **P0.2: Design Trends Research** - Visual curation, aesthetic judgment
- **P0.4: Component Library Research** - Quality evaluation, project fit assessment
- **P1.2: Navigation Menu** - UX decisions, visual design
- **P2.1: Initial Bubble UI** - Visual design, animation feel, user delight
- **P3.2: Feed Item Component** - Content presentation, visual hierarchy
- **P4.2: Hierarchy Browser** - Information architecture, cognitive load management

---

## Unknowns & Decisions Needed

**From Document 1 Open Questions - Must Resolve Before Implementation:**

### 🔴 Blockers (Cannot Proceed)

| # | Question | Blocks Phase | Impact | Who Can Answer |
|---|----------|--------------|--------|----------------|
| 1 | Backend API schema (feed, user data) | P3.3, P5.1 | Cannot fetch/display content | Backend developer |
| 2 | AI JSON format (ontology, hierarchy) | P4.3 | Cannot render dynamic data | AI module owner |
| 3 | Authentication mechanism (JWT, OAuth, etc.) | P1.4 | Cannot implement login | Security/backend |
| 4 | Related topics API contract | P2.2 | Cannot build bubble onboarding | Backend/AI |
| 7 | Pagination API (cursor, offset, page size) | P3.1, P3.3 | Cannot implement infinite scroll | Backend developer |

### 🟡 Important (Affects Design)

| # | Question | Affects Phase | Impact | Who Can Answer |
|---|----------|---------------|--------|----------------|
| 5 | Component library selection | P3.1, P4.1 | Implementation approach | Frontend/research (P0.4) |
| 6 | Design system (colors, typography) | All phases | Visual consistency | Design/product (P0.2) |
| 10 | Memory management strategy | P3.1 | Performance, UX | Frontend architect |
| 13 | State management library | P5.1 | Architecture pattern | Frontend architect (P0.4) |

---

## Learning Objectives

### Phase 0: Research & Setup
- **Competitive analysis** - Understand market, user needs, UI patterns
- **Design trends** - Current visual language, lookbook curation
- **Cursor IDE** - AI-assisted development workflow
- **Component ecosystem** - React library landscape

### Phase 1: Core Layout
- **3-panel layouts** - IDE-style interfaces, CSS Grid mastery
- **React Router** - Multi-view navigation, route management
- **Authentication UI** - Login flows, protected routes

### Phase 2: Bubble Onboarding
- **Interactive animations** - Bubble physics, orbital motion
- **Progressive disclosure** - Gamified UX, user engagement
- **API integration** - Async data fetching, state updates

### Phase 3: Feed Interface
- **Infinite scroll** - Memory management, view recycling
- **TikTok-style UX** - Swipe interactions, snap behavior
- **Dynamic rendering** - JSON-driven UI, flexible layouts

### Phase 4: Graph & Hierarchy
- **Graph visualization** - Cytoscape.js, node/edge rendering
- **Information architecture** - Hierarchical data, drill-down UX
- **Dynamic JSON** - Variable structure handling

### Phase 5: Integration & Polish
- **State management** - Global state, cross-component communication
- **Accessibility** - WCAG compliance, keyboard navigation
- **Performance** - Optimization, smooth animations

---

**End of Document**
