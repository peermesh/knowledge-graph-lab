# Knowledge Graph Labs: Detailed Frontend Requirements
## Vision Capture & Product Requirements Document

- **Date**: 2025-09-30
- **Source**: Product Vision Discussion
- **Status**: Research Phase - Requirements Definition

---

## Executive Summary

Knowledge Graph Labs is a research discovery platform that combines AI-powered ontology mapping with personalized content delivery. The frontend must balance exploratory discovery (interactive visualizations, bubble-based onboarding) with practical content consumption (feed-based UI, customizable publishing options).

**Core Value Proposition**: Users define research interests through intuitive interfaces, receive AI-curated deep research results, and control how/when they consume this content across multiple channels (email, notifications, blog publishing).

---

## 1. Core User Features

### 1.1 Authentication & User Management
- **Email signup/login** - Standard authentication flow
- **User preferences storage** - Persistent settings across sessions
- **Custom research profiles** - Multiple topic profiles per user

### 1.2 Publishing & Delivery Settings
Users must be able to configure:

| Output Channel | Controls | Requirements |
|---------------|----------|--------------|
| **Email** | Enable/disable, frequency interval | Standard SMTP integration |
| **Push Notifications** | Enable/disable, frequency interval | Mobile/desktop notifications |
| **Blog Publishing** | Platform selection, auto-publish settings | Integration with Medium, Substack, etc. |
| **Text Messages** | Enable/disable, frequency interval | SMS/messaging gateway |

**UI Requirements**:

- Toggle switches for each channel
- Interval selectors (real-time, hourly, daily, weekly)
- Per-topic channel assignment (different topics → different channels)

### 1.3 Topic Selection & Interest Mapping

#### Bubble Interface (Onboarding)
**Purpose**: Exploratory, visual way to define interests without cognitive overload

**Flow**:

1. Start with empty canvas + single circle with "+" button
2. User clicks "+" → types initial interest (e.g., "creator economy")
3. System sends to backend: `GET /api/related-topics?seed="creator economy"&count=5`
4. Backend returns 5 related concepts
5. Frontend displays as smaller circles orbiting the main circle
6. **Interaction Model**:
   - Single click = add to interests (green border)
   - Double click = explicitly dislike (red border, gets smaller)
   - Click on liked topic = expand that topic with its own related concepts
7. Build interest graph organically through exploration

**UI/UX Considerations**:

- Smooth animations (fade in/out, orbit motion)
- Visual feedback (color changes, size scaling)
- Undo/reset functionality
- "Done" button → saves interest map, transitions to main interface

#### Text-Based Alternative
For "pedantic" users who prefer direct input:

- Search/autocomplete field
- Hierarchical category browser
- Import from list/file
- Same backend API, different presentation

---

## 2. Main Application Layout

### Standard Three-Panel Design

```
┌─────────────────────────────────────────────────────────────┐
│  Header: Logo, User Menu, Notifications                     │
├──────────┬─────────────────────────────┬────────────────────┤
│          │                             │                    │
│  Left    │      Center Panel          │   Right Panel      │
│  Panel   │      (Feed/Lab Views)      │   (Filters)        │
│          │                             │                    │
│  Nav &   │                             │   Fine-tune        │
│  Menu    │                             │   selected item    │
│          │                             │                    │
└──────────┴─────────────────────────────┴────────────────────┘
```

### 2.1 Left Panel (Navigation & Collections)

**Structure** (top to bottom):

1. **Main Navigation**
   - Home
   - Feed
   - Lab Views (collapsible submenu)
   - Settings

2. **Lab Views Submenu**
   - Graph Visualization
   - Hierarchical Directory
   - [Future experimental views]

3. **Your Content Section**
   - Saved Topics
   - Recent Searches
   - Custom Collections
   - Published Items

**Design Pattern**: Similar to YouTube sidebar - clear hierarchy, collapsible sections, icons + text labels

### 2.2 Center Panel (Primary Content Area)

#### Mode 1: Feed View (Default)

**Inspiration**: TikTok/Instagram-style infinite scroll with modern UX patterns

**Core Mechanics**:

- **Infinite scroll** with lazy loading (10 items per batch)
- **Swipe/snap** interaction (optional, desktop uses scroll wheel)
- **Pull-to-refresh** at top
- **Memory management**: Recycle views outside viewport (crucial for performance)

**Content Card Structure**:
```
┌─────────────────────────────────────┐
│  Research Report Title              │
│  ──────────────────────────────     │
│                                     │
│  [Summary content]                  │
│  [Key findings]                     │
│  [Ontology preview snippet]         │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  Related Topics Tags        │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Action buttons: Save, Share,      │
│   Open Full Report, Add to Topics]  │
└─────────────────────────────────────┘
```

**Side Controls** (appear on hover/tap):

- Share
- Save/Bookmark
- Reactions (like/dislike for AI feedback)
- Flag/Report

**API Integration**:
```javascript
// Initial load
GET /api/feed?user_id={id}&offset=0&limit=10

// Pagination
GET /api/feed?user_id={id}&offset=10&limit=10

// Response includes:
{
  items: [...],
  has_more: true,
  next_offset: 20
}
```

#### Mode 2: Lab Views

##### A. Graph Visualization (Ontology Map)

**Purpose**: Visual representation of concept relationships

**Example Data**:

- Nodes: "Bees", "Flowers", "Pollination", "Ecosystems"
- Edges: "Bees --[gets nectar from]--> Flowers"
- Edge labels show relationship type

**UI Requirements**:

- Pan/zoom controls
- Node search/filter
- Click node → highlight connections
- Click edge → show relationship details in right panel
- Cluster detection visualization
- Color coding by topic category

**Technology Considerations** (from existing research doc):

- D3.js vs Cytoscape vs vis.js
- Must handle 10K+ nodes
- Target: 60fps during pan/zoom
- Memory: <500MB for 10K nodes

##### B. Hierarchical Directory (Yahoo-style)

**Purpose**: Traditional text-based navigation for focused research

**Structure**:
```
Creator Economy
├─ [ ] Platforms & Venues
│  ├─ [ ] YouTube & Video
│  ├─ [ ] Podcasting
│  └─ [ ] Music Distribution
├─ [ ] Revenue Models
│  ├─ [ ] Subscriptions
│  ├─ [ ] Sponsorships
│  └─ [ ] Merchandise
└─ [ ] Creator Tools
   ├─ [ ] Editing Software
   └─ [ ] Analytics Platforms
```

**Interaction Model**:

- Checkbox = add to "My Topics"
- Click text = drill down (expand children)
- Breadcrumb navigation
- Infinite nesting supported
- Search/filter across hierarchy

**Design Principles**:
- **Not too dense**: 3-7 items visible per level
- **Not too sparse**: Minimum 2 levels visible
- **Progressive disclosure**: Load children on demand
- **Visual breathing room**: Proper spacing, clear hierarchy

**Data Source**:
```javascript
// Backend returns full hierarchy as JSON
{
  "topic": "Creator Economy",
  "children": [
    {
      "topic": "Platforms & Venues",
      "children": [...]
    }
  ]
}
```

### 2.3 Right Panel (Filters & Fine-Tuning)

**Purpose**: Context-sensitive controls for selected item

**Dynamic Content** based on left panel selection:

| Left Panel Selection | Right Panel Shows |
|---------------------|-------------------|
| Feed item selected | Topic tags, date range, source filters |
| Graph node selected | Node properties, relationship filters, export options |
| Topic in directory | Subtopic filters, recency settings, source credibility sliders |
| Settings page | N/A (right panel hidden or shows help) |

**Design Pattern**: Similar to video editor properties panel - changes based on selection, clearly labeled sections

---

## 3. Data Flow & Backend Integration

### 3.1 JSON-Based Content Delivery

**All research content arrives as structured JSON**:

```json
{
  "research_id": "uuid",
  "title": "Developments in Creator Economy - Oct 2025",
  "created_at": "2025-09-30T10:00:00Z",
  "ontology": {
    "nodes": [
      {"id": "n1", "label": "Creator Economy", "type": "concept"},
      {"id": "n2", "label": "YouTube", "type": "platform"}
    ],
    "edges": [
      {"from": "n1", "to": "n2", "relationship": "includes platform"}
    ]
  },
  "content_hierarchy": {
    "top_level": ["Revenue Models", "Platform Shifts", "Emerging Tools"],
    "sections": [
      {
        "title": "Revenue Models",
        "subsections": [
          {"title": "Subscriptions", "summary": "..."},
          {"title": "Sponsorships", "summary": "..."}
        ]
      }
    ]
  },
  "tags": ["creator-economy", "youtube", "monetization"]
}
```

### 3.2 User Interest Feedback Loop

**Frontend → Backend Communication**:

1. **Topic Selection Events**
   ```javascript
   POST /api/user/interests

   {

     "action": "add",

     "topic": "R&B mixed with country music",

     "source": "bubble_interface",

     "weight": 5 // how deep they drilled

   }
   ```

2. **Engagement Metrics**
   ```javascript
   POST /api/engagement

   {

     "content_id": "uuid",
     "action": "viewed" | "saved" | "shared" | "dismissed",
     "duration_seconds": 45

   }
   ```

3. **Backend Uses This Data To**:
   - Weight research priorities (20 users like music → more music research)
   - Personalize feeds
   - Identify niche interests (harmonicas + slam dancing = rare, minimal research)
   - Balance research resources

---

## 4. Design System & Visual Language

### 4.1 Design Research Requirements

**Pre-Development Phase**:

1. **Competitive Analysis**
   - Identify similar products (research tools, content aggregators)
   - Screenshot interfaces, catalog in Figma
   - Build "lookbook" of visual inspiration

2. **App Store Reconnaissance**
   - Read negative reviews of competitors
   - Identify pain points (e.g., "too cluttered", "slow graph rendering")
   - Build "anti-features" list (what NOT to do)

3. **Design Trends Research**
   - Search "top design trends 2025"
   - Identify 2-3 usable trends (ignore extremes)
   - Reference Webby Awards, Awwwards for inspiration

4. **Visual Inspiration Beyond Web**
   - Collect non-UI visual references (posters, packaging, print design)
   - Use as input to AI design tools for unique outputs
   - Goal: Avoid "default Material Design clone" look

### 4.2 Recommended Visual Direction

**Constraints**:

- Avoid overly skeuomorphic (no 3D buttons, fake textures)
- Avoid ultra-minimal (needs enough visual hierarchy for complex data)
- Must support both "lab" (experimental) and "feed" (familiar) modes

**Suggested Approach**:
- **Flat with depth**: Use shadows/layers for hierarchy, not texture
- **Limited color palette**: 2-3 brand colors + neutrals + accent
- **Generous whitespace**: Let complex graph data breathe
- **Modern typography**: Variable fonts, clear hierarchy
- **Subtle animations**: Transitions for state changes, no gratuitous motion

**Accessibility Requirements**:

- WCAG 2.1 AA compliance (from existing research doc)
- Keyboard navigation for all features
- Screen reader support for graph data (challenging!)
- Color-blind safe palette

---

## 5. Technology Stack Recommendations

### 5.1 Immediate Decisions Required

Based on existing research doc, need to finalize:

1. **UI Framework**: React (likely winner based on ecosystem)
2. **State Management**: Zustand or Context API (Redux may be overkill)
3. **Graph Library**: Cytoscape.js (good balance of performance + features)
4. **Component Library**: Custom components built on Tailwind CSS (avoids generic look)
5. **Build Tool**: Vite (fast, modern)

### 5.2 Additional Stack Considerations

**Feed Component**:

- Use off-the-shelf React infinite scroll library
- Candidates: `react-virtualized`, `react-window`, `@tanstack/react-virtual`
- Must support view recycling (memory management)

**Animations**:

- Framer Motion for bubble interface animations
- CSS transitions for simple interactions

**Data Fetching**:

- React Query (TanStack Query) for caching + state
- Handles pagination, refetching, optimistic updates

**Routing**:

- React Router v6 (standard choice)

**Testing**:

- Jest (unit tests)
- Playwright (e2e tests per existing doc)

---

## 6. Development Approach: Zero to One Strategy

### 6.1 The SpecKit Workflow

**Philosophy**: Use AI to accelerate initial prototype, then refine

**Process**:

1. **Constitution Phase** (Project-wide rules)
   - Define coding standards
   - Database choices
   - No fake data
   - TypeScript strict mode
   - Accessibility requirements

2. **Specification Phase** (Per-module specs)
   - Input: This requirements doc (condensed)
   - Output: Functional specification
   - Review: Human edits for accuracy
   - Goal: Clear, unambiguous implementation guide

3. **Test-Driven Development** (AI-generated)
   - AI writes tests first (crucial for AI dev)
   - Tests define expected behavior
   - Prevents AI from "hallucinating" success
   - Separate AI writes tests vs. implementation (no cheating)

4. **Task Generation** (Granular steps)
   - AI breaks spec into hundreds of tasks
   - Sequential execution
   - Human reviews output periodically
   - Can pause, audit, restart

5. **Audit & Refactor Phase**
   - AI audits own code for "smelly code"
   - Check for: unnecessary nesting, unclear variable names, tight coupling
   - Performance profiling
   - Human makes final decisions

### 6.2 Parallel AI Design Exploration

**Use V0, Lovable, Cursor for rapid UI prototyping**:

1. **Input Preparation**:
   - Lookbook images (moodboard)
   - Condensed requirements (key features only)
   - Specific constraints (3-panel layout, etc.)

2. **Batch Generation**:
   - Generate 10+ variations per platform
   - Different visual inputs per batch
   - Screenshot all results

3. **Component Extraction**:
   - Identify best individual elements (buttons, cards, animations)
   - Extract code
   - Build custom component library

4. **Iteration**:
   - Mix/match best pieces
   - Refine with specific prompts ("make this button glow on hover")
   - Build cohesive design system

### 6.3 Cursor + Predictive Coding

**For implementation refinement**:

- Cursor understands full file context
- Predicts next code based on patterns
- Speeds up: renaming, refactoring, repetitive structure creation
- Human guides, AI accelerates

---

## 7. Success Metrics

### 7.1 User Experience Metrics

- **Onboarding completion rate**: >70% complete bubble interface
- **Daily active users**: Track feed engagement
- **Topic diversity**: Average topics per user (target: 5-10)
- **Publishing setup**: % users who configure ≥1 output channel

### 7.2 Technical Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Graph load (1K nodes) | <3s | Lighthouse |
| Graph fps (pan/zoom) | 60fps | Chrome DevTools |
| Feed scroll jank | 0 dropped frames | Performance API |
| Initial bundle size | <1MB gzipped | Webpack analyzer |
| Time to interactive | <2s | Lighthouse |

### 7.3 Development Velocity Metrics

- **PRD → Prototype time**: <5 days (measure AI acceleration)
- **Component reusability**: >60% components used 3+ times
- **Test coverage**: >80% for core features
- **Accessibility score**: 100% WCAG 2.1 AA

---

## 8. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Graph performance with 10K+ nodes** | High | Early POC, fallback to progressive loading |
| **AI-generated code quality** | Medium | Rigorous TDD, human audit phases |
| **Scope creep (too many features)** | High | MVP feature freeze, phase 2 backlog |
| **Generic UI design** | Low | Extensive lookbook, unique visual inputs |
| **Accessibility for complex graphs** | Medium | Early screen reader testing, alternative views |

---

## 9. Phase 1 Research Deliverables (Updated)

### Existing Research Tasks (Keep)
- Technology stack comparison (React/Vue/Angular)
- Graph library benchmarking (D3/Cytoscape/vis.js)
- State management evaluation
- Component library assessment

### Additional Research Tasks (Add)

1. **Infinite Scroll Component Research**
   - Compare: react-virtualized vs react-window vs tanstack/react-virtual
   - Benchmark: memory usage with 1000+ feed items
   - Test: integration with React Query for pagination

2. **Bubble Interface Animation Research**
   - Framer Motion vs React Spring vs CSS animations
   - Performance: 50+ animated bubbles simultaneously
   - Touch interaction libraries for mobile

3. **Hierarchical Data UI Patterns**
   - Best practices for expandable trees
   - Progressive disclosure techniques
   - Search/filter integration

4. **Design Tool Workflow**
   - V0.dev vs Lovable.ai vs Cursor AI design mode
   - Prompt patterns that yield usable code
   - Component extraction workflows

5. **Publishing Integration Options**
   - Medium API capabilities
   - Substack embedding options
   - Ghost CMS integration
   - Email service providers (SendGrid, Mailgun)

---

## 10. Next Steps

### Immediate Actions (This Week)

1. **Finalize Technology Stack** (from research)
   - Confirm React as framework
   - Choose state management approach
   - Select graph library

2. **Build Competitive Lookbook**
   - Screenshot 10+ similar products
   - Identify 5 key UI patterns to adopt/avoid
   - Create Figma board

3. **Create Condensed Spec for SpecKit**
   - Distill this doc into 2-3 pages
   - Focus on functional requirements
   - Define clear success criteria per feature

### Week 2-3: Prototyping

1. **SpecKit POC**
   - Run bubble interface through SpecKit
   - Generate tests + implementation
   - Audit output quality

2. **Parallel AI Design Generation**
   - V0/Lovable runs with lookbook input
   - Generate 30+ UI variations
   - Screenshot + catalog best elements

3. **Graph Visualization POC**
   - Implement 1K node demo
   - Benchmark performance
   - Validate meets 60fps target

### Week 4: Integration & Review

1. **Assemble Prototype**
   - Combine best UI components
   - Integrate working graph viz
   - Connect to mock API

2. **Demo & Feedback**
   - Show to team
   - Collect qualitative feedback
   - Measure against success metrics

3. **Roadmap Refinement**
   - Identify gaps
   - Prioritize features for MVP
   - Create Phase 2 backlog

---

## Appendix A: Key Terminology

- **Ontology**: Formal representation of knowledge (concepts + relationships)
- **Ontology Mapping**: Connecting related concepts with labeled relationships
- **Zero to One**: Going from no prototype to first working demo
- **Smelly Code**: Code that works but has structural problems (maintainability issues)
- **TDD (Test-Driven Development)**: Write tests before implementation
- **Progressive Disclosure**: Show information gradually as needed, not all at once
- **View Recycling**: Reuse UI components for performance (infinite scroll optimization)
- **Lookbook**: Collection of visual references for design inspiration

## Appendix B: Reference Links

- **SpecKit**: https://github.com/github/speckit
- **OpenAI Pulse**: Chat GPT's feed-based research delivery (competitive reference)
- **React Virtualization**: https://github.com/bvaughn/react-virtualized
- **Cytoscape.js**: https://js.cytoscape.org/
- **Framer Motion**: https://www.framer.com/motion/
- **TanStack Query**: https://tanstack.com/query/latest
- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/

---

- **Document Status**: Draft for review
- **Next Review**: After initial research phase completion
- **Owner**: Frontend Design Team
- **Last Updated**: 2025-09-30
