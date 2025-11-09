# Figma Make Workflow Prompt - Knowledge Graph Lab Interface
**Created:** 2025-10-27  
**Purpose:** Complete prompt for creating Figma prototype using Figma Make workflow  
**Source Documents:** `.dev/ui-example-2025-10-27/` directory

---

## 📋 **INSTRUCTIONS FOR DESIGN AGENT**

**IMPORTANT CLARIFICATION:** This is NOT about using Figma MCP tools to read existing Figma files. "Figma Make" is a separate AI-powered design-to-code service where you paste a comprehensive prompt directly into their web frontend and it generates a complete application/prototype.

**🎯 YOUR PRIMARY TASK:**

You are working with the **Knowledge Graph Lab UI example documents** from `.dev/ui-example-2025-10-27/`. Your job is to:

1. **Review the prompt below** against the source UI example documents to ensure it accurately captures all specifications
2. **Extract and prepare a clean prompt** ready for the user to paste directly into Figma Make's web interface
3. **Create supporting documentation** (README, usage instructions, etc.)

**Source Documents (Reference These):**
- `../01-PRIMARY-SCREENS-SPECIFICATION.md` - Complete screen specifications for all 8 pages
- `../02-WIREFRAME-HANDOVER-INSTRUCTIONS.md` - Design guidance and component specs
- `../03-NAVIGATION-FLOW.md` - User journeys and navigation architecture
- `../04-COMPONENT-INVENTORY.md` - Complete component library specification
- `../README.md` - Overview and design philosophy

**The prompt below was created from these UI example documents.** Verify it captures everything accurately and create a clean, ready-to-paste version.

**What this is NOT:**
- ❌ NOT using Figma MCP tools to read/create Figma files
- ❌ NOT connecting to existing Figma designs
- ❌ NOT about Figma the design tool itself

**What this IS:**
- ✅ A comprehensive prompt ready to paste into Figma Make service
- ✅ Complete specifications for all 8 pages + design system
- ✅ Following the Figma Make workflow pattern (80/5/15 rule: planning done, ready to build)

**🚨 CRITICAL: OUTPUT LOCATION REQUIREMENT**

**All documents and files you create MUST be saved in a subdirectory within this directory:**
- **Location:** `.dev/ui-example-2025-10-27/figma-prototype/`
- **Create subdirectory:** Create a new subdirectory with a timestamp (e.g., `2025-10-27-14-30-00-figma-output/`) or descriptive name (e.g., `agent-output/`)
- **Purpose:** This ensures all work is trackable and organized separately from source specifications

**Example structure:**
```
.dev/ui-example-2025-10-27/
├── figma-prototype/                    ← You are here
│   ├── FIGMA-MAKE-PROMPT.md           ← This prompt
│   └── [your-subdirectory]/           ← Create your work here
│       ├── figma-file-link.md
│       ├── component-library.md
│       ├── design-notes.md
│       └── [any other documents]
├── 01-PRIMARY-SCREENS-SPECIFICATION.md
├── 02-WIREFRAME-HANDOVER-INSTRUCTIONS.md
└── [other source documents]
```

**When creating files:**
1. Create a subdirectory with timestamp or descriptive name
2. Save all outputs (Figma links, notes, documentation, etc.) in that subdirectory
3. Create a README.md in your subdirectory explaining what's included
4. Reference source documents from parent directory (use relative paths like `../01-PRIMARY-SCREENS-SPECIFICATION.md`)

**Workflow Reference:** `.dev/kits/design-kit/workflows/figma-make/WORKFLOW-GUIDE.md`

**Key Source Documents (in parent directory):**
- `../01-PRIMARY-SCREENS-SPECIFICATION.md` - Complete screen specifications
- `../02-WIREFRAME-HANDOVER-INSTRUCTIONS.md` - Design guidance
- `../03-NAVIGATION-FLOW.md` - User journeys
- `../04-COMPONENT-INVENTORY.md` - Component library

---

## 🚀 **THE COMPLETE FIGMA MAKE PROMPT**

**What is Figma Make?**
Figma Make is an AI-powered web service that takes a comprehensive text prompt and generates a complete application/prototype. You access it through their web frontend interface.

**How to Use This Prompt:**
1. **Open Figma Make** in your web browser (their frontend interface)
2. **Copy the entire prompt section below** (between the triple backticks, lines ~84-505)
3. **Paste directly into Figma Make's prompt input field**
4. The service will generate the complete prototype based on the Knowledge Graph Lab UI specifications

**Source Material:**
This prompt was created from the UI example documents in `.dev/ui-example-2025-10-27/`:
- Primary Screens Specification (8 screens fully specified)
- Navigation Flow (complete user journeys)
- Component Inventory (full design system)
- Wireframe Handover Instructions (design patterns)

**Ready-to-use prompt for Figma Make:**
Copy the entire section below and paste it directly into Figma Make's web interface:

---

```
Build this following engineering best practices:
- Write all code to WCAG AA accessibility standards
- Create and use reusable components throughout
- Use semantic HTML and proper component architecture
- Avoid absolute positioning; use flexbox/grid layouts
- Build actual code components, not image SVGs
- Keep code clean, maintainable, and well-structured

I need you to build a complete Figma prototype for the Knowledge Graph Lab application. Here's everything:

**PROJECT OVERVIEW:**

**App Type & Purpose:**
Knowledge Graph Lab is a data visualization and discovery platform that helps users explore knowledge graphs, find opportunities (grants, partnerships, events), and receive personalized notifications. The application solves the problem of information overload by providing AI-powered knowledge discovery through visual exploration.

**Core Features:**
1. Bubble Universe Interface - Interactive topic exploration with orbital bubble visualization
2. Multi-View Dashboard - Feed view, Bubble view, and Graph view for different exploration modes
3. Advanced Search & Filtering - Real-time search with autocomplete and comprehensive filtering
4. Entity Relationship Visualization - Network graphs showing connections between entities
5. Personalized Notifications - Multi-channel publishing (Email, Slack, Discord) with intelligent scheduling
6. Saved Collections - Save and organize opportunities, entities, and searches
7. Admin Pipeline Monitoring - Real-time system metrics and pipeline status

**User Flow:**
1. First-time users: Landing → Sign Up → Onboarding (bubble selection) → Dashboard
2. Returning users: Landing → Sign In → Dashboard (default Feed view)
3. Discovery flow: Dashboard → Search → Results → Entity Detail → Related Entities
4. Exploration flow: Dashboard → Switch to Bubble View → Select Topic → Explore Connections
5. Deep dive flow: Dashboard → Graph View → Click Entity → Entity Detail → Follow Relationships
6. Settings flow: Dashboard → Settings → Configure Notifications → Save Preferences

**Page Structure:**
1. **Onboarding** - First-time user bubble selection interface for initial topic setup
2. **Dashboard (Feed View)** - Main content feed showing opportunity cards in infinite scroll format
3. **Dashboard (Bubble View)** - Interactive bubble visualization showing topic relationships
4. **Dashboard (Graph View)** - Network graph visualization of entity relationships
5. **Search Results** - Search interface with autocomplete, filters, and result cards
6. **Entity Detail** - Complete entity information with relationships, activity timeline, and metadata
7. **User Settings** - Notification preferences, display settings, and user configuration
8. **Admin Dashboard** - Pipeline monitoring, metrics, error logs, and system controls

**ALL PAGES & DETAILED SPECIFICATIONS:**

**PAGE 1: ONBOARDING**
**Purpose:** First-time user setup to select initial topics of interest using bubble interface
**Layout Structure:** Full-screen centered layout with floating bubbles
**Key Components:**
- Welcome message text
- Empty space with prompt ("Click to begin")
- Input bubble (appears on click) with text field
- Orbital bubble system (5-7 bubbles around central topic)
- Progress indicator (dots showing steps)
- "Start Exploring" button (appears after selection)
**Interactive Elements:**
- Click empty space → Input bubble appears
- Type topic → Press Enter or click ✓ → Related bubbles orbit
- Click bubbles to select (3-5 required)
- Click "Start Exploring" → Navigate to Dashboard
**Navigation:** Entry point from sign-up. Exit to Dashboard after completion.
**Content:** 
- Welcome text: "Welcome to Knowledge Graph Lab"
- Tagline: "Like exploring a solar system - start with one planet, discover related worlds"
- Prompt: "Click to begin" or "Type your first interest"
**States:** Empty state, input state, bubble generation state, selection state, completion state

**PAGE 2: DASHBOARD - FEED VIEW (Default)**
**Purpose:** Main content discovery interface showing opportunity cards in vertical feed format
**Layout Structure:** Standard 3-panel layout (Navigation sidebar 260px, Content area flexible, Filters panel 320px)
**Key Components:**
- Three-panel layout master template
- Navigation sidebar with Topics, Saved, History, Settings
- Header bar with global search and user menu
- Feed view content area with opportunity cards
- Filter panel with date range, type, source, relevance, confidence filters
- View mode toggle (Feed/Bubble/Graph)
**Interactive Elements:**
- Click opportunity card → Navigate to Entity Detail
- Click Save button → Save to collection (toast confirmation)
- Click Share button → Share modal
- Switch view modes → Transition between Feed/Bubble/Graph
- Apply filters → Results update
- Collapse/expand sidebars
**Navigation:** 
- From: Onboarding, Search Results, Entity Detail, Settings
- To: Search Results, Entity Detail, Settings, Topic views
**Content:**
- 8-10 opportunity cards showing:
  - Title with icon (grant/partnership/event/news)
  - Organization name and location
  - Amount/value (if applicable)
  - Deadline with countdown
  - Relevance score as progress bar (0-100%)
  - Confidence score indicator
  - Description preview (2 lines)
  - Action buttons: Save, Share, Details
**States:** Loading (skeleton cards), Loaded (cards visible), Empty (no results), Error (retry message)

**PAGE 3: DASHBOARD - BUBBLE VIEW**
**Purpose:** Visual topic exploration using interactive bubble interface
**Layout Structure:** Standard 3-panel layout with bubble visualization in content area
**Key Components:**
- Three-panel layout
- Bubble interface component (SVG-based)
- Navigation sidebar
- Filter panel
- View mode toggle
**Interactive Elements:**
- Click bubble → Expand universe (new bubbles appear)
- Hover bubble → Show topic name and details
- Select bubble → Highlight and show connections
- Click outside → Create new bubble for input
**Navigation:** 
- From: Dashboard Feed View, Dashboard Graph View
- To: Dashboard Feed View, Dashboard Graph View, Topic views
**Content:**
- Central topic bubble (user's selected topic)
- 5-7 orbiting related topic bubbles
- Bubble sizes indicate importance (large, medium, small)
- Bubble colors indicate confidence (gradient blue=high to gray=low)
- Labels on bubbles showing topic names
**States:** Default (all bubbles visible), Hover (bubble highlighted), Selected (bubble expanded), Loading (bubbles animating in)

**PAGE 4: DASHBOARD - GRAPH VIEW**
**Purpose:** Network graph visualization of entity relationships
**Layout Structure:** Standard 3-panel layout with graph visualization in content area
**Key Components:**
- Three-panel layout
- Graph visualization component (D3.js or similar placeholder)
- Navigation sidebar
- Filter panel
- Graph controls (Zoom +/-, Center, Filter, Export)
- Legend for node/edge types
**Interactive Elements:**
- Click node → Navigate to Entity Detail
- Hover node → Show tooltip with entity info
- Zoom controls → Zoom in/out
- Pan controls → Move graph view
- Filter nodes → Show/hide by type
**Navigation:**
- From: Dashboard Feed View, Dashboard Bubble View, Entity Detail
- To: Dashboard Feed View, Dashboard Bubble View, Entity Detail
**Content:**
- Nodes representing entities (topics, organizations, people)
- Edges representing relationships (connections, partnerships, funding)
- Node size = Entity importance
- Edge width = Relationship strength
- Color coding by entity/relationship type
**States:** Loading (skeleton graph), Loaded (graph visible), Empty (no data message), Error (retry option)

**PAGE 5: SEARCH RESULTS**
**Purpose:** Search interface with autocomplete, filters, and comprehensive result display
**Layout Structure:** Standard 3-panel layout with search-focused content area
**Key Components:**
- Search bar with autocomplete dropdown
- Filter panel (active and visible)
- Result cards (10-20 visible)
- Sort controls (Relevance, Date, Amount, Deadline)
- View toggle (List/Graph)
- Pagination controls
**Interactive Elements:**
- Type in search → Autocomplete suggestions appear
- Click suggestion → Search executes
- Apply filters → Results update with count
- Click result card → Navigate to Entity Detail
- Sort results → Reorder cards
- Switch view → Toggle between List and Graph
- Pagination → Load more results
**Navigation:**
- From: Dashboard (any view), Header search
- To: Entity Detail, Dashboard, Saved collections
**Content:**
- Search bar: "🔍 Search knowledge graph..."
- Autocomplete suggestions:
  - Recent searches (if any)
  - AI-powered suggestions with relevance scores
  - Popular searches
- Result cards (same format as Feed View):
  - Numbered results (1, 2, 3...)
  - Result count display: "Showing 127 results (0.3s)"
  - Sort dropdown: "Relevance ▼", "Date", "Amount", "Deadline"
- Filter badges showing active filters
**States:** Empty search (no query), Searching (loading indicator), Results (cards visible), No results (empty state with suggestions), Error (retry option)

**PAGE 6: ENTITY DETAIL**
**Purpose:** Complete entity information display with relationships and activity timeline
**Layout Structure:** Standard 3-panel layout with entity-focused content area
**Key Components:**
- Entity detail card (full information)
- Relationship graph visualization (mini network)
- Activity timeline (chronological events)
- Related entities list
- Action buttons (Follow, Export, Share)
- Breadcrumb navigation
**Interactive Elements:**
- Click relationship → Navigate to related entity
- Click related entity → Navigate to that entity's detail
- Click timeline item → Expand details
- Click Follow → Save to followed entities
- Click Export → Export entity data
- Click Share → Share modal
**Navigation:**
- From: Search Results, Dashboard (any view), Graph View, Related entities
- To: Related entities (back and forth), Dashboard, Search Results
**Content:**
- Entity header:
  - Name (e.g., "OpenAI")
  - Type badge (e.g., "Organization • AI/Technology")
  - Metadata (e.g., "Founded: 2015 • San Francisco, CA")
- Confidence score card:
  - Overall confidence: 92%
  - Source score: 9.2/10
  - Context score: 9.2/10
  - Model score: 9.2/10
- Relationships section:
  - "Funded by → Microsoft ($10B)"
  - "Partners → Azure Cloud"
  - "Competes → Anthropic, Google"
  - "Employs → 500+ researchers"
- Recent activity timeline:
  - "Oct 2025: $10B funding round"
  - "Sep 2025: GPT-5 announcement"
  - "Aug 2025: New partnership with..."
- Relationship network visualization:
  - Central entity (OpenAI)
  - Connected entities (Microsoft, Azure, etc.)
  - Relationship labels
**States:** Loading (skeleton), Loaded (full information), Error (retry), Not found (404 message)

**PAGE 7: USER SETTINGS**
**Purpose:** User preference configuration for notifications, display, and account settings
**Layout Structure:** Standard 3-panel layout with settings forms in content area
**Key Components:**
- Settings navigation tabs (Profile, Notifications, Display, API)
- Form sections with grouped fields
- Toggle switches for preferences
- Select dropdowns for options
- Save/Cancel buttons
- Toast notifications for save confirmation
**Interactive Elements:**
- Toggle switches → Change state visually
- Fill form fields → Validation on blur
- Select dropdowns → Choose options
- Click Save → Show success toast
- Click Cancel → Discard changes
**Navigation:**
- From: Dashboard (any view), User menu
- To: Dashboard (after save)
**Content:**
- Notification Preferences section:
  - Delivery channels (Email, Slack, Discord, In-app)
  - Frequency options (Instant, Daily digest, Weekly summary, Custom)
  - Topics to track (with tags: AI ✕, Healthcare ✕, Grants ✕)
  - Relevance threshold slider (min 80%)
- Display Preferences section:
  - Theme (Light, Dark, Auto)
  - Default view (Feed, Bubble, Graph)
  - Results per page (10, 25, 50, 100)
  - Language selector
  - Accessibility options (High contrast, Keyboard hints, Screen reader)
- Profile Settings section:
  - Name, email, avatar
  - Password change
  - Account preferences
**States:** Default (current settings), Editing (form fields active), Saved (success toast), Error (validation errors)

**PAGE 8: ADMIN DASHBOARD**
**Purpose:** System monitoring and pipeline management for administrators
**Layout Structure:** Standard 3-panel layout with metrics and monitoring in content area
**Key Components:**
- Metric cards (4 main metrics: Throughput, Accuracy, Queue Depth, Error Rate)
- Pipeline visualization (progress bars showing stages)
- Recent errors table
- System controls (Configure, Export Logs, Restart)
- Charts (line graphs for metrics over time)
**Interactive Elements:**
- Hover metric card → Show tooltip with details
- Click metric card → Drill down (show detail modal)
- Click error log → Show stack trace
- Click Configure → Settings modal
- Click Restart → Confirmation → Restart pipeline
**Navigation:**
- From: Dashboard (admin only), Admin menu
- To: Pipeline details, User management, System logs
**Content:**
- Metrics overview:
  - "THROUGHPUT: 847 docs/hr ↑ 12.3%"
  - "ACCURACY: 92.3% ↓ 0.7%"
  - "QUEUE DEPTH: 1,247 docs ↓ 234"
  - "ERROR RATE: 0.3%/hr → stable"
- Pipeline visualization:
  - "Input → Chunk → Extract → Validate"
  - Progress bars: "100% 98% 95% 92%"
- Recent errors table:
  - "10:32 | Timeout | Doc #4821"
  - "10:28 | Parse | Doc #4819"
  - "10:15 | API | Rate limit"
- Charts:
  - Throughput over time (line chart)
  - Error rate trend (line chart)
  - Queue depth visualization (area chart)
**States:** Loading (skeleton metrics), Loaded (metrics visible), Error (connection error), Offline (cached data indicator)

**DESIGN SYSTEM:**

**1. Color Palette**
- Primary Color: #0066CC (Blue) - Main brand color for buttons, links, accents
- Secondary Color: #00AA44 (Green) - Success states, positive indicators
- Warning Color: #FF9500 (Orange) - Warnings, pending states
- Error Color: #FF3B30 (Red) - Errors, destructive actions
- Info Color: #0066CC (Blue) - Informational messages
- Background Colors:
  - Light mode: #F5F5F7 (Light gray), White (#FFFFFF)
  - Dark mode: #1C1C1E (Dark gray), #000000 (Black)
- Text Colors:
  - Primary text: #1C1C1E (Dark mode: #F5F5F7)
  - Secondary text: #8E8E93 (Dark mode: #8E8E93)
  - Disabled text: #C7C7CC
- Neutral Palette:
  - Gray scale from #F9FAFB (lightest) to #111827 (darkest)
  - Border colors: #E5E7EB

**2. Typography**
- Font Families:
  - Headings: Inter or SF Pro Display (system font fallback)
  - Body: Inter or SF Pro Text (system font fallback)
  - Monospace: Fira Code or SF Mono (for code/data)
- Font Sizes:
  - H1: 36px (2.25rem) - Page titles
  - H2: 30px (1.875rem) - Section headers
  - H3: 24px (1.5rem) - Subsection headers
  - H4: 20px (1.25rem) - Card titles
  - Body: 16px (1rem) - Default text
  - Small: 14px (0.875rem) - Secondary text
  - Caption: 12px (0.75rem) - Metadata, labels
- Font Weights:
  - Regular: 400 (body text)
  - Medium: 500 (emphasized text)
  - Semibold: 600 (subheadings)
  - Bold: 700 (headings, strong emphasis)
- Line Heights:
  - Tight: 1.25 (headings)
  - Normal: 1.5 (body text)
  - Relaxed: 1.75 (long-form content)

**3. Spacing System**
- Base unit: 8px
- Spacing scale:
  - XS: 4px (0.25rem)
  - SM: 8px (0.5rem)
  - MD: 16px (1rem)
  - LG: 24px (1.5rem)
  - XL: 32px (2rem)
  - 2XL: 48px (3rem)
  - 3XL: 64px (4rem)
- Padding: 8px, 16px, 24px, 32px
- Margins: 8px, 16px, 24px, 32px, 48px, 64px
- Gaps: 8px, 16px, 24px (for flexbox/grid)

**4. Component Styles**
- Button Styles:
  - Primary: Blue background (#0066CC), white text, 8px border radius
  - Secondary: White background, blue border, blue text
  - Ghost: Transparent background, blue text
  - Danger: Red background (#FF3B30), white text
  - Sizes: Small (32px height), Medium (40px), Large (48px)
- Input Field Styles:
  - Border: 1px solid #E5E7EB
  - Border radius: 8px
  - Padding: 12px 16px
  - Focus: Blue border (#0066CC), shadow
  - Error: Red border (#FF3B30)
- Card Styles:
  - Background: White
  - Border radius: 12px
  - Shadow: 0 2px 4px rgba(0, 0, 0, 0.05) (default), 0 8px 16px (hover)
  - Padding: 16px, 24px, or 32px
- Border Radius:
  - Small: 4px (buttons, badges)
  - Medium: 8px (inputs, cards)
  - Large: 12px (large cards)
  - Full: 9999px (pills, avatars)
- Shadow/Elevation:
  - XS: 0 1px 2px rgba(0, 0, 0, 0.05)
  - SM: 0 2px 4px rgba(0, 0, 0, 0.05)
  - MD: 0 4px 8px rgba(0, 0, 0, 0.1)
  - LG: 0 8px 16px rgba(0, 0, 0, 0.1)
  - XL: 0 16px 32px rgba(0, 0, 0, 0.15)

**5. Layout Grid**
- Container max-width: 1440px (desktop)
- Grid columns: 12-column grid system
- Gutter sizes: 24px (desktop), 16px (tablet), 12px (mobile)
- Responsive breakpoints:
  - Mobile: < 768px (single column, stacked)
  - Tablet: 768px - 1439px (2 columns, sidebar collapsed)
  - Desktop: 1440px+ (3 panels visible, full layout)
- Panel widths:
  - Navigation sidebar: 260px (desktop), collapsible
  - Content area: Flexible (fills remaining space)
  - Filter panel: 320px (desktop), overlay on mobile/tablet

**6. Interaction Patterns**
- Hover states: 200ms transition ease-in-out
- Click states: 100ms scale/press animation
- Loading spinners: 1s rotation animation
- Page transitions: 300ms slide animation
- Toast notifications: 3-5 second auto-dismiss
- Modal open/close: 300ms fade + scale animation

**7. Accessibility Requirements**
- WCAG 2.1 AA compliance
- Color contrast ratios: 4.5:1 for text, 3:1 for UI elements
- Keyboard navigation: Tab, Enter, Esc, Arrow keys
- Focus indicators: 2px blue outline on all focusable elements
- ARIA labels: All interactive elements have descriptive labels
- Screen reader support: Semantic HTML, proper heading hierarchy

Build out all 8 pages as separate page components with full functionality, content, and styling according to the design system. Create reusable components for buttons, cards, inputs, and layout elements. Make this a complete, working prototype with all interactions and states defined. Include responsive behavior for mobile, tablet, and desktop breakpoints.

```
---

## 📝 **WHAT YOU SHOULD DO AS THE AGENT**

**Your Primary Tasks:**

1. **OUTPUT LOCATION** - Create a subdirectory: `.dev/ui-example-2025-10-27/figma-prototype/[timestamp]-output/`

2. **Create Documentation Files:**
   - **README.md** - Explain what this prompt is, how to paste it into Figma Make's web interface, and what it generates
   - **PROMPT-READY-TO-USE.md** - Clean copy of just the prompt section (between triple backticks, ~lines 84-505) ready to paste into Figma Make's frontend
   - **ALTERNATIVE-OPTIONS.md** - If user doesn't have Figma Make access, suggest alternatives (v0, Claude, Bolt.new)

3. **Review the Prompt Against Source Documents:**
   - Read `../01-PRIMARY-SCREENS-SPECIFICATION.md` and verify all 8 pages are fully captured
   - Read `../03-NAVIGATION-FLOW.md` and verify navigation flows are complete
   - Read `../04-COMPONENT-INVENTORY.md` and verify design system matches
   - Read `../02-WIREFRAME-HANDOVER-INSTRUCTIONS.md` for design patterns
   - Ensure the prompt accurately reflects the Knowledge Graph Lab UI example specifications
   - Note any gaps or improvements needed

4. **Create Supporting Materials (Optional but Helpful):**
   - Mock data examples for the prototype
   - Component checklist
   - Design system reference summary

**Important Notes:**
- **This is NOT about Figma MCP** - Do not try to use Figma MCP tools
- **Figma Make is a web service** - The user will paste the prompt directly into Figma Make's web frontend interface
- **Source is UI example documents** - This prompt was built from `.dev/ui-example-2025-10-27/` specifications
- **Your role** - Review the prompt against source docs, extract clean version, document usage instructions
- **The prompt should be complete** - It follows the Figma Make workflow and should include everything from the UI example documents (project overview, all 8 pages, complete design system)

## ✅ **SUCCESS CRITERIA**

The Figma prototype will be considered complete when:
- [ ] All 8 pages are fully designed with realistic content
- [ ] Component library is created and documented
- [ ] Navigation flow works between all pages
- [ ] Responsive variations exist for key screens
- [ ] All component states are shown (default, hover, active, disabled, loading, error)
- [ ] Design system tokens are consistently applied
- [ ] Interactive prototype demonstrates main user flows
- [ ] Accessibility requirements are met

---

**Ready to use?** Copy the entire prompt section (between the triple backticks) and paste it into Figma Make. The workflow guide recommends this should generate the complete prototype in one pass.

