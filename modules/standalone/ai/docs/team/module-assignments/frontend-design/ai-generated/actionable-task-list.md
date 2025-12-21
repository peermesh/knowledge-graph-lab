# Frontend Implementation: Complete Actionable Task List
**Status**: Ready to Execute
**Last Updated**: 2025-09-30

---

## How to Use This List

✅ **Mark tasks complete as you finish them**
📌 **Dependencies are clearly marked** - do tasks in order within each phase
🎯 **Each task is small and specific** - no expert knowledge needed
⏱️ **Time estimates included** - plan your work sessions

---

## Phase 0: Setup & Foundation (Week 1, Days 1-2)

### 0.1 Environment Setup
- [ ] **Install Node.js (v18+) and npm** - Download from nodejs.org
  - Time: 15 min
  - Success: Run `node --version` and see v18 or higher

- [ ] **Install VS Code** - Download from code.visualstudio.com
  - Time: 10 min
  - Success: VS Code opens

- [ ] **Install Cursor IDE** - Download from cursor.sh
  - Time: 10 min
  - Success: Cursor opens and you can see AI features

- [ ] **Install Git** - Download from git-scm.com
  - Time: 10 min
  - Success: Run `git --version` in terminal

- [ ] **Clone the repository** - Run `git clone [repo-url]` in terminal
  - Time: 5 min
  - Dependency: Git installed
  - Success: You see the project folder

### 0.2 Project Initialization
- [ ] **Create frontend folder structure**
  ```bash
  mkdir -p frontend/src/{components,pages,hooks,utils,styles,assets}
  mkdir -p frontend/public
  ```
  - Time: 5 min
  - Success: Folders exist in file explorer

- [ ] **Initialize React + Vite project**
  ```bash
  cd frontend
  npm create vite@latest . -- --template react-ts
  npm install
  ```
  - Time: 10 min
  - Dependency: Node.js installed
  - Success: Run `npm run dev` and see Vite welcome page at http://localhost:5173

- [ ] **Install essential dependencies**
  ```bash
  npm install react-router-dom @tanstack/react-query axios zustand
  npm install -D tailwindcss postcss autoprefixer
  npx tailwindcss init -p
  ```
  - Time: 5 min
  - Success: Check package.json and see all packages listed

### 0.3 Workspace Setup
- [ ] **Install VS Code/Cursor extensions**
  - ES7+ React/Redux/React-Native snippets
  - Tailwind CSS IntelliSense
  - ESLint
  - Prettier
  - Time: 10 min
  - Success: Extensions show as installed

- [ ] **Create .gitignore file**
  ```
  node_modules/
  dist/
  .env
  .env.local
  *.log
  ```
  - Time: 2 min
  - Success: File exists in project root

---

## Phase 1: Research & Planning (Week 1, Days 3-5)

### 1.1 Competitive Analysis
- [ ] **Find 10 similar products** - Google: "research discovery tools", "knowledge graph apps", "content feed platforms"
  - Time: 1 hour
  - Tools: Just use Google and click around
  - Success: You have 10 app names written down

- [ ] **Screenshot each app's main interface** - Press Cmd+Shift+4 (Mac) or Windows+Shift+S (Windows)
  - Time: 30 min
  - Dependency: Found 10 products
  - Success: You have 10 screenshot files saved

- [ ] **Screenshot each app's navigation/menu** - Same screenshot method
  - Time: 20 min
  - Success: 10 more screenshots saved

- [ ] **Read negative reviews** - Go to app stores, sort reviews by "lowest rated"
  - Time: 1 hour
  - Success: You have a list of 20+ complaints written down

- [ ] **Create "Anti-Features" list** - Make a doc listing "things NOT to do"
  - Time: 15 min
  - Success: Document exists with 10+ items

### 1.2 Design Research
- [ ] **Google "design trends 2025"** - Visit first 5 results
  - Time: 30 min
  - Success: You have notes on 3-5 trending styles

- [ ] **Visit Webby Awards site** - Go to webbyawards.com and browse winners
  - Time: 30 min
  - Success: Bookmarked 5+ sites you like

- [ ] **Visit Awwwards.com** - Browse "Site of the Day"
  - Time: 30 min
  - Success: Bookmarked 5+ sites you like

- [ ] **Screenshot 20 non-UI inspirations** - Posters, album covers, product packaging
  - Time: 1 hour
  - Tools: Google Images, Pinterest
  - Success: 20 images saved to a "lookbook" folder

- [ ] **Create Figma account** - Go to figma.com and sign up (free)
  - Time: 10 min
  - Success: You can log into Figma

- [ ] **Create Figma lookbook** - Upload all screenshots to one big canvas
  - Time: 30 min
  - Dependency: Figma account, screenshots ready
  - Success: One Figma file with all images

### 1.3 Technology Research
- [ ] **Read React docs intro** - reactjs.org/docs/getting-started
  - Time: 1 hour
  - Success: You understand components, props, state (basic concepts)

- [ ] **Read Cytoscape.js demos** - Go to js.cytoscape.org and click "Demos"
  - Time: 30 min
  - Success: You've seen a graph visualization working

- [ ] **Read TanStack Query basics** - tanstack.com/query/latest/docs
  - Time: 45 min
  - Success: You understand what "data fetching" means

- [ ] **Read Tailwind CSS tutorial** - tailwindcss.com/docs/installation
  - Time: 1 hour
  - Success: You know how to add classes like "bg-blue-500"

---

## Phase 2: Core UI Components (Week 2, Days 1-3)

### 2.1 Basic Layout Structure
- [ ] **Create AppLayout component** - File: `src/components/layout/AppLayout.tsx`
  ```tsx
  // Three-panel layout with header
  // Left panel, center panel, right panel
  ```
  - Time: 30 min
  - Use: Tailwind CSS for layout (flex or grid)
  - Success: You see three empty boxes side by side

- [ ] **Create Header component** - File: `src/components/layout/Header.tsx`
  - Time: 20 min
  - Include: Logo placeholder, user menu placeholder
  - Success: Header appears at top of page

- [ ] **Create LeftPanel component** - File: `src/components/layout/LeftPanel.tsx`
  - Time: 30 min
  - Content: Empty div with background color
  - Success: Colored box appears on left side

- [ ] **Create CenterPanel component** - File: `src/components/layout/CenterPanel.tsx`
  - Time: 30 min
  - Content: Empty div with different background color
  - Success: Colored box appears in center

- [ ] **Create RightPanel component** - File: `src/components/layout/RightPanel.tsx`
  - Time: 30 min
  - Content: Empty div with background color
  - Success: Colored box appears on right side

- [ ] **Connect all layout components** - Import everything into App.tsx
  - Time: 15 min
  - Success: Run `npm run dev` and see complete layout

### 2.2 Navigation Menu (Left Panel)
- [ ] **Create NavItem component** - File: `src/components/navigation/NavItem.tsx`
  - Time: 20 min
  - Props: label (string), icon (optional), onClick (function)
  - Success: Can render a single clickable menu item

- [ ] **Create NavSection component** - File: `src/components/navigation/NavSection.tsx`
  - Time: 30 min
  - Props: title (string), children (NavItems)
  - Success: Can render a titled section with items inside

- [ ] **Create main navigation list** - Add to LeftPanel.tsx
  - Time: 45 min
  - Items: Home, Feed, Lab Views, Settings
  - Success: Four clickable items appear

- [ ] **Add collapsible Lab Views submenu**
  - Time: 30 min
  - Use: useState hook to track open/closed
  - Success: Click "Lab Views" and see submenu appear/disappear

- [ ] **Add "Your Content" section**
  - Time: 30 min
  - Items: Saved Topics, Recent Searches, Custom Collections
  - Success: Second section appears below main nav

### 2.3 Basic Routing
- [ ] **Install React Router** - Already done in setup, now configure it
  - Time: 20 min
  - File: Create `src/router.tsx`
  - Success: File exists with route definitions

- [ ] **Create placeholder pages**
  - Time: 30 min
  - Files: Create empty components in `src/pages/`
    - HomePage.tsx
    - FeedPage.tsx
    - GraphPage.tsx
    - SettingsPage.tsx
  - Success: Four files exist, each just shows its name

- [ ] **Connect routes to navigation**
  - Time: 30 min
  - Update: NavItem components to use `<Link>` from react-router
  - Success: Clicking nav items changes the URL

---

## Phase 3: Feed View (Week 2, Days 4-5 & Week 3, Days 1-2)

### 3.1 Feed Card Component
- [ ] **Design FeedCard structure** - Sketch on paper or Figma
  - Time: 20 min
  - Include: Title, summary, tags, action buttons
  - Success: You have a drawing/mockup

- [ ] **Create FeedCard component** - File: `src/components/feed/FeedCard.tsx`
  - Time: 1 hour
  - Props: title, summary, tags, onSave, onShare
  - Use: Tailwind for styling
  - Success: Can render one card with dummy data

- [ ] **Add hover effects to FeedCard**
  - Time: 30 min
  - Effect: Subtle shadow or border on hover
  - Success: Card reacts when you move mouse over it

- [ ] **Create ActionButton component** - File: `src/components/feed/ActionButton.tsx`
  - Time: 20 min
  - Props: icon, label, onClick
  - Success: Reusable button component works

- [ ] **Add action buttons to FeedCard** - Save, Share, Like
  - Time: 30 min
  - Success: Three buttons appear at bottom of card

### 3.2 Infinite Scroll
- [ ] **Install virtualization library**
  ```bash
  npm install @tanstack/react-virtual
  ```
  - Time: 5 min
  - Success: Package in package.json

- [ ] **Read TanStack Virtual docs** - tanstack.com/virtual/latest
  - Time: 30 min
  - Success: You understand "virtual" = only render visible items

- [ ] **Create FeedList component** - File: `src/components/feed/FeedList.tsx`
  - Time: 1.5 hours
  - Use: @tanstack/react-virtual
  - Test: Create array of 1000 dummy items
  - Success: Can scroll through 1000 items smoothly

- [ ] **Test memory usage** - Open Chrome DevTools > Performance
  - Time: 20 min
  - Action: Scroll through feed, check memory doesn't keep growing
  - Success: Memory stays relatively stable

### 3.3 Data Fetching
- [ ] **Set up TanStack Query** - Configure in App.tsx
  ```tsx
  import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
  ```
  - Time: 30 min
  - Success: No errors, app still runs

- [ ] **Create mock API** - File: `src/utils/mockApi.ts`
  - Time: 30 min
  - Function: `fetchFeedItems(offset, limit)` returns fake data
  - Success: Can call function and get array of objects

- [ ] **Create useFeed hook** - File: `src/hooks/useFeed.ts`
  - Time: 45 min
  - Use: useInfiniteQuery from TanStack Query
  - Success: Hook returns data and fetchNextPage function

- [ ] **Connect FeedList to useFeed hook**
  - Time: 30 min
  - Success: Feed shows real data from hook (even if mock)

- [ ] **Add pull-to-refresh** - Install library if needed
  - Time: 45 min
  - Library: Search "react pull to refresh" on npm
  - Success: Pull down at top of feed triggers refresh

---

## Phase 4: Graph Visualization (Week 3, Days 3-5)

### 4.1 Cytoscape Setup
- [ ] **Install Cytoscape.js**
  ```bash
  npm install cytoscape
  npm install @types/cytoscape
  ```
  - Time: 5 min
  - Success: Package installed

- [ ] **Read Cytoscape getting started** - js.cytoscape.org/getting-started
  - Time: 1 hour
  - Success: You understand nodes, edges, layout

- [ ] **Create GraphView component** - File: `src/components/graph/GraphView.tsx`
  - Time: 30 min
  - Content: Empty div with ref for Cytoscape
  - Success: Component renders without errors

- [ ] **Initialize Cytoscape** - Inside GraphView useEffect
  - Time: 45 min
  - Code: Create Cytoscape instance, attach to div
  - Success: Console log shows Cytoscape object

### 4.2 Basic Graph Rendering
- [ ] **Create mock graph data** - File: `src/utils/mockGraphData.ts`
  - Time: 30 min
  - Format: Array of nodes and edges (10 nodes)
  - Success: Can import and see data structure

- [ ] **Render 10 nodes** - Pass mock data to Cytoscape
  - Time: 30 min
  - Success: You see 10 circles/nodes on screen

- [ ] **Add edge rendering** - Connect nodes with lines
  - Time: 20 min
  - Success: Lines appear connecting nodes

- [ ] **Add edge labels** - Show relationship type on edges
  - Time: 30 min
  - Success: Text appears on lines

- [ ] **Add node labels** - Show node name on nodes
  - Time: 20 min
  - Success: Text appears on circles

### 4.3 Graph Interactions
- [ ] **Add pan/zoom controls** - Built into Cytoscape
  - Time: 15 min
  - Test: Drag to pan, scroll to zoom
  - Success: Graph moves and zooms

- [ ] **Add node click handler**
  - Time: 30 min
  - Action: Console log node data when clicked
  - Success: Click node, see data in console

- [ ] **Highlight connected nodes on click**
  - Time: 45 min
  - Effect: Change color of connected nodes
  - Success: Click node, related nodes change color

- [ ] **Create GraphControls component** - Zoom in/out buttons
  - Time: 30 min
  - Buttons: Zoom +, Zoom -, Reset View
  - Success: Buttons work

### 4.4 Performance Testing
- [ ] **Create 1,000 node dataset** - Expand mock data
  - Time: 20 min
  - Use: Loop to generate nodes programmatically
  - Success: Data array has 1000 items

- [ ] **Test 1K node rendering** - Load 1K nodes
  - Time: 15 min
  - Measure: Check load time (should be <3 seconds)
  - Success: Graph loads and is usable

- [ ] **Test 10K node rendering** - Create 10K dataset
  - Time: 30 min
  - Measure: FPS during pan/zoom (target: 60fps)
  - Success: Graph performs acceptably or you note issues

- [ ] **Document performance results** - Create markdown file
  - Time: 20 min
  - File: `docs/performance-results.md`
  - Success: File has load times, FPS, memory usage

---

## Phase 5: Hierarchical Directory View (Week 4, Days 1-2)

### 5.1 Tree Component
- [ ] **Create TreeNode component** - File: `src/components/tree/TreeNode.tsx`
  - Time: 45 min
  - Props: label, children, onCheck, onExpand
  - Success: Can render one expandable node

- [ ] **Add expand/collapse icon**
  - Time: 20 min
  - Icon: Arrow that rotates (▶ becomes ▼)
  - Success: Icon changes when clicked

- [ ] **Add checkbox**
  - Time: 20 min
  - Success: Checkbox appears, can be checked

- [ ] **Create Tree component** - File: `src/components/tree/Tree.tsx`
  - Time: 30 min
  - Props: data (nested structure)
  - Success: Can render multiple nested nodes

### 5.2 Tree Data & State
- [ ] **Create mock hierarchy data** - File: `src/utils/mockHierarchyData.ts`
  - Time: 30 min
  - Structure: Nested objects (3 levels deep)
  - Example: Creator Economy > Platforms > YouTube
  - Success: Data structure exists

- [ ] **Render mock hierarchy** - Pass to Tree component
  - Time: 20 min
  - Success: Tree appears with nested items

- [ ] **Add expand/collapse state** - Track which nodes are open
  - Time: 45 min
  - Use: useState or Zustand store
  - Success: Clicking expands/collapses children

- [ ] **Add checkbox state** - Track which nodes are checked
  - Time: 45 min
  - Success: Checking boxes works, state is tracked

### 5.3 Tree Features
- [ ] **Add breadcrumb navigation**
  - Time: 45 min
  - Show: Path to current selection
  - Success: Breadcrumbs appear above tree

- [ ] **Add search/filter**
  - Time: 1 hour
  - Input: Text field filters visible nodes
  - Success: Typing filters tree

- [ ] **Style tree for readability** - Proper spacing, indentation
  - Time: 30 min
  - Success: Tree is easy to read

---

## Phase 6: Bubble Interface (Week 4, Days 3-5)

### 6.1 Bubble Component
- [ ] **Install Framer Motion**
  ```bash
  npm install framer-motion
  ```
  - Time: 5 min
  - Success: Package installed

- [ ] **Read Framer Motion basics** - framer.com/motion/introduction
  - Time: 45 min
  - Success: You understand animate, transition

- [ ] **Create Bubble component** - File: `src/components/bubble/Bubble.tsx`
  - Time: 45 min
  - Props: label, size, color, onClick, onDoubleClick
  - Success: Can render one animated circle with text

- [ ] **Add animations** - Fade in, scale on hover
  - Time: 30 min
  - Success: Bubble animates smoothly

### 6.2 Bubble Canvas
- [ ] **Create BubbleCanvas component** - File: `src/components/bubble/BubbleCanvas.tsx`
  - Time: 1 hour
  - Layout: Absolute positioning for bubbles
  - Success: Empty canvas renders

- [ ] **Add initial "+" bubble** - Center of canvas
  - Time: 20 min
  - Success: One bubble with + icon appears

- [ ] **Add click handler** - Opens input to add topic
  - Time: 30 min
  - Success: Click shows text input

- [ ] **Add topic submission** - Send topic to backend (mock)
  - Time: 30 min
  - Success: Typing and pressing Enter triggers API call (mock)

### 6.3 Bubble Interactions
- [ ] **Calculate orbit positions** - Math for circle positions
  - Time: 45 min
  - Formula: Use sin/cos to place bubbles in circle around parent
  - Success: Helper function returns x, y coordinates

- [ ] **Render related bubbles** - Show 5 bubbles orbiting main
  - Time: 1 hour
  - Success: After adding topic, 5 smaller bubbles appear

- [ ] **Add single-click = like** - Green border appears
  - Time: 30 min
  - Success: Click changes border color

- [ ] **Add double-click = dislike** - Red border, shrink
  - Time: 30 min
  - Success: Double-click changes border and size

- [ ] **Add expand on click** - Clicked bubble becomes new center
  - Time: 1 hour
  - Success: Click liked bubble, new related bubbles appear

### 6.4 Bubble State Management
- [ ] **Create bubble state store** - File: `src/stores/bubbleStore.ts`
  - Time: 45 min
  - Use: Zustand
  - State: List of bubbles, liked topics, disliked topics
  - Success: Store exports useBubbleStore hook

- [ ] **Connect canvas to store**
  - Time: 30 min
  - Success: Adding/liking bubbles updates store

- [ ] **Add "Done" button** - Saves interests, exits onboarding
  - Time: 30 min
  - Success: Button appears, clicking logs interests to console

---

## Phase 7: Settings & Publishing (Week 5, Days 1-2)

### 7.1 Settings Page Layout
- [ ] **Create SettingsPage component** - File: `src/pages/SettingsPage.tsx`
  - Time: 30 min
  - Layout: Form with sections
  - Success: Page renders in center panel

- [ ] **Add section headers** - Email, Notifications, Blog, etc.
  - Time: 20 min
  - Success: Clear sections visible

### 7.2 Toggle Controls
- [ ] **Create Toggle component** - File: `src/components/settings/Toggle.tsx`
  - Time: 30 min
  - Props: label, checked, onChange
  - Success: Toggle switch works

- [ ] **Add email toggle**
  - Time: 15 min
  - Success: Toggle for email delivery

- [ ] **Add push notification toggle**
  - Time: 15 min
  - Success: Toggle for push notifications

- [ ] **Add blog publishing toggle**
  - Time: 15 min
  - Success: Toggle for blog

- [ ] **Add SMS toggle**
  - Time: 15 min
  - Success: Toggle for text messages

### 7.3 Interval Controls
- [ ] **Create IntervalSelector component** - File: `src/components/settings/IntervalSelector.tsx`
  - Time: 45 min
  - Options: Real-time, Hourly, Daily, Weekly
  - Success: Dropdown or radio buttons work

- [ ] **Add interval for each channel**
  - Time: 30 min
  - Success: Each toggle has interval selector

### 7.4 Settings State
- [ ] **Create settings store** - File: `src/stores/settingsStore.ts`
  - Time: 45 min
  - Use: Zustand
  - State: All toggle states, intervals
  - Success: Store exports useSettingsStore

- [ ] **Connect settings page to store**
  - Time: 30 min
  - Success: Changing toggles updates store

- [ ] **Add save button** - Sends settings to backend (mock)
  - Time: 30 min
  - Success: Button triggers API call, shows confirmation

---

## Phase 8: Backend Integration (Week 5, Days 3-5)

### 8.1 API Client Setup
- [ ] **Create axios instance** - File: `src/utils/api.ts`
  - Time: 30 min
  - Config: Base URL, default headers
  - Success: File exports configured axios

- [ ] **Create API endpoints file** - File: `src/utils/endpoints.ts`
  - Time: 20 min
  - Content: Object with all API URLs
  - Success: Centralized endpoint definitions

### 8.2 API Hooks
- [ ] **Create useFetchFeed hook** - Replace mock data
  - Time: 45 min
  - Use: TanStack Query
  - Endpoint: /api/feed
  - Success: Hook fetches real data from backend

- [ ] **Create useRelatedTopics hook** - For bubble interface
  - Time: 45 min
  - Endpoint: /api/related-topics
  - Success: Hook fetches related topics

- [ ] **Create useUserInterests hook** - Get/set user interests
  - Time: 45 min
  - Endpoints: GET/POST /api/user/interests
  - Success: Hook can read and write interests

- [ ] **Create useSettings hook** - Get/set settings
  - Time: 45 min
  - Endpoints: GET/POST /api/user/settings
  - Success: Hook can read and write settings

### 8.3 Authentication
- [ ] **Install auth library** - Choose: Auth0, Clerk, or custom
  - Time: 1 hour (research + install)
  - Success: Library installed, configured

- [ ] **Create login page** - File: `src/pages/LoginPage.tsx`
  - Time: 1 hour
  - Form: Email, password
  - Success: Form renders

- [ ] **Create signup page** - File: `src/pages/SignupPage.tsx`
  - Time: 1 hour
  - Form: Email, password, confirm password
  - Success: Form renders

- [ ] **Add auth hooks** - useAuth, useUser
  - Time: 1 hour
  - Success: Hooks return user data, login/logout functions

- [ ] **Protect routes** - Redirect to login if not authenticated
  - Time: 45 min
  - Success: Visiting protected pages redirects to login

### 8.4 Error Handling
- [ ] **Create ErrorBoundary component**
  - Time: 30 min
  - Catches: React errors, shows fallback UI
  - Success: Breaking app shows error page instead of blank

- [ ] **Add toast notifications** - Install library (react-hot-toast)
  ```bash
  npm install react-hot-toast
  ```
  - Time: 30 min
  - Success: Can show success/error messages

- [ ] **Add error handling to all API calls**
  - Time: 1 hour
  - Action: Catch errors, show toast
  - Success: Failed API calls show error message

---

## Phase 9: Polish & Refinement (Week 6)

### 9.1 Responsive Design
- [ ] **Test on mobile viewport** - Chrome DevTools device mode
  - Time: 30 min
  - Success: Identify layout issues

- [ ] **Add mobile breakpoints** - Tailwind responsive classes
  - Time: 2 hours
  - Action: Adjust layout for sm/md screens
  - Success: Layout works on mobile

- [ ] **Test on tablet viewport**
  - Time: 30 min
  - Success: Layout works on tablet

### 9.2 Accessibility
- [ ] **Add ARIA labels** - To buttons, inputs, interactive elements
  - Time: 1 hour
  - Success: Screen reader can announce elements

- [ ] **Test keyboard navigation** - Tab through entire app
  - Time: 30 min
  - Success: Can navigate without mouse

- [ ] **Check color contrast** - Use WebAIM contrast checker
  - Time: 30 min
  - Tool: webaim.org/resources/contrastchecker
  - Success: All text meets WCAG AA

- [ ] **Add focus indicators** - Visible outline on focused elements
  - Time: 30 min
  - Success: Tab shows clear focus

### 9.3 Loading States
- [ ] **Add loading spinner component**
  - Time: 30 min
  - Success: Spinner component exists

- [ ] **Add loading states to all data fetches**
  - Time: 1 hour
  - Success: Loading spinners appear during fetches

- [ ] **Add skeleton screens** - For feed cards
  - Time: 1 hour
  - Success: Placeholder cards show while loading

### 9.4 Final Touches
- [ ] **Add favicon** - Place in /public folder
  - Time: 15 min
  - Success: Icon appears in browser tab

- [ ] **Update page titles** - Use react-helmet or similar
  - Time: 30 min
  - Success: Each page has descriptive title

- [ ] **Add 404 page** - For unknown routes
  - Time: 30 min
  - Success: Visiting bad URL shows 404 page

- [ ] **Add empty states** - When no data exists
  - Time: 45 min
  - Success: Empty feed shows helpful message

---

## Phase 10: Testing & Deployment (Week 7)

### 10.1 Unit Tests
- [ ] **Install testing libraries**
  ```bash
  npm install -D vitest @testing-library/react @testing-library/jest-dom
  ```
  - Time: 10 min
  - Success: Packages installed

- [ ] **Write tests for components** - Start with 5 key components
  - Time: 3 hours (30 min each)
  - Components: FeedCard, TreeNode, Bubble, Toggle, NavItem
  - Success: Run `npm test` and see passing tests

- [ ] **Write tests for hooks** - useFeed, useBubbleStore
  - Time: 2 hours
  - Success: Hooks tested, tests pass

- [ ] **Achieve 60% test coverage** - Run coverage report
  - Time: 2 hours (write more tests)
  - Command: `npm run test:coverage`
  - Success: Coverage report shows >60%

### 10.2 E2E Tests
- [ ] **Install Playwright**
  ```bash
  npm install -D @playwright/test
  npx playwright install
  ```
  - Time: 10 min
  - Success: Playwright installed

- [ ] **Write E2E test: User flow** - Login → view feed → save item
  - Time: 1.5 hours
  - Success: Test passes

- [ ] **Write E2E test: Onboarding** - Bubble interface flow
  - Time: 1.5 hours
  - Success: Test passes

- [ ] **Write E2E test: Settings** - Change settings, save
  - Time: 1 hour
  - Success: Test passes

### 10.3 Performance Optimization
- [ ] **Run Lighthouse audit** - Chrome DevTools
  - Time: 20 min
  - Success: Generate report with scores

- [ ] **Optimize bundle size** - Check with webpack-bundle-analyzer
  - Time: 1 hour
  - Action: Code split large libraries
  - Success: Bundle <1MB gzipped

- [ ] **Add lazy loading** - For routes and heavy components
  - Time: 1 hour
  - Use: React.lazy, Suspense
  - Success: Initial load faster

- [ ] **Optimize images** - Compress, use WebP
  - Time: 30 min
  - Tool: Use TinyPNG or similar
  - Success: Images smaller

### 10.4 Deployment
- [ ] **Create production build**
  ```bash
  npm run build
  ```
  - Time: 5 min
  - Success: /dist folder created

- [ ] **Choose hosting** - Vercel, Netlify, or Cloudflare Pages
  - Time: 30 min (research)
  - Success: Account created

- [ ] **Deploy to hosting** - Follow provider docs
  - Time: 45 min
  - Success: App accessible at public URL

- [ ] **Set up CI/CD** - GitHub Actions to auto-deploy
  - Time: 1 hour
  - Success: Push to main triggers deployment

- [ ] **Test production deployment** - Check all features work
  - Time: 30 min
  - Success: Everything works on live site

---

## Phase 11: Documentation (Week 7-8)

### 11.1 Code Documentation
- [ ] **Add JSDoc comments** - To all components and hooks
  - Time: 2 hours
  - Success: Every function has description

- [ ] **Create component README** - Document props, usage
  - Time: 1 hour
  - File: `src/components/README.md`
  - Success: README exists with examples

### 11.2 User Documentation
- [ ] **Write user guide** - How to use the app
  - Time: 2 hours
  - File: `docs/user-guide.md`
  - Success: Step-by-step guide exists

- [ ] **Create video walkthrough** - Record screen showing features
  - Time: 1 hour
  - Tool: Loom or QuickTime
  - Success: Video uploaded

### 11.3 Developer Documentation
- [ ] **Write setup instructions** - How to run locally
  - Time: 1 hour
  - File: Update `README.md`
  - Success: Another dev can follow and run app

- [ ] **Document architecture** - High-level system design
  - Time: 1.5 hours
  - File: `docs/architecture.md`
  - Success: Diagram + explanation exists

- [ ] **Document API integration** - Endpoint specs, auth flow
  - Time: 1 hour
  - File: `docs/api-integration.md`
  - Success: Clear API docs

---

## Completion Checklist

### Functional Requirements
- [ ] Users can sign up and log in
- [ ] Users can configure email/notification/blog settings
- [ ] Users can select topics via bubble interface
- [ ] Users can select topics via text/hierarchy
- [ ] Users can view research feed
- [ ] Users can view graph visualization
- [ ] Users can view hierarchical directory
- [ ] Users can save and share content

### Technical Requirements
- [ ] Graph renders 1K nodes in <3 seconds
- [ ] Graph maintains 60fps during pan/zoom
- [ ] Initial bundle <1MB gzipped
- [ ] Time to interactive <2 seconds
- [ ] WCAG 2.1 AA compliant
- [ ] Works on mobile/tablet/desktop
- [ ] Test coverage >60%

### Polish Requirements
- [ ] Loading states everywhere
- [ ] Error handling everywhere
- [ ] Empty states for no data
- [ ] Responsive design
- [ ] Accessible (keyboard nav, screen reader)
- [ ] Deployed to production
- [ ] Documentation complete

---

## Troubleshooting Guide

### Stuck on a task?
1. **Break it smaller** - Can this task be split into 2-3 smaller tasks?
2. **Google it** - Search "[technology] [what you're trying to do]"
3. **Ask AI** - Paste the task into Claude/ChatGPT with "How do I do this?"
4. **Skip for now** - Mark it, move to next task, come back later

### Common issues:
- **npm install fails** → Delete node_modules and package-lock.json, try again
- **Import errors** → Check file path is correct (relative path)
- **TypeScript errors** → Start with .tsx files, ignore types initially if stuck
- **Styling not working** → Check Tailwind config, make sure CSS is imported
- **API calls fail** → Check network tab in DevTools, verify endpoint URL

---

## Progress Tracking

**Total Tasks**: 200+
**Estimated Time**: 7-8 weeks (full-time)

### Weekly Goals
- **Week 1**: Setup + Research complete
- **Week 2**: Basic layout + Feed working
- **Week 3**: Graph visualization working
- **Week 4**: Bubble interface + Tree view working
- **Week 5**: Settings + Backend integration
- **Week 6**: Polish + Accessibility
- **Week 7**: Testing + Deployment
- **Week 8**: Documentation + Buffer

### Mark Your Progress
Copy this to a separate document and check off as you go:

```
Phase 0: [ ] Not started [ ] In progress [ ] Complete
Phase 1: [ ] Not started [ ] In progress [ ] Complete
Phase 2: [ ] Not started [ ] In progress [ ] Complete
Phase 3: [ ] Not started [ ] In progress [ ] Complete
Phase 4: [ ] Not started [ ] In progress [ ] Complete
Phase 5: [ ] Not started [ ] In progress [ ] Complete
Phase 6: [ ] Not started [ ] In progress [ ] Complete
Phase 7: [ ] Not started [ ] In progress [ ] Complete
Phase 8: [ ] Not started [ ] In progress [ ] Complete
Phase 9: [ ] Not started [ ] In progress [ ] Complete
Phase 10: [ ] Not started [ ] In progress [ ] Complete
Phase 11: [ ] Not started [ ] In progress [ ] Complete
```

---

## Next Steps

**START HERE**:
1. Do Phase 0, Task 0.1 - Install Node.js
2. Check the box when done
3. Move to next task
4. Repeat until you're walking through the gardens and out the other side with the roses 🌹

**Questions?** Review the detailed requirements doc, Google the technology, or ask for help on specific tasks.

Good luck! You've got this. 🚀
