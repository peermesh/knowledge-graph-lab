# Tasks for Frontend Module v1.0-2025-11-03

## 🎯 HIGHLIGHTS - Top Things to Check Out

### ✅ Security Patches Applied (2025-11-25)
- **httpOnly cookies implemented** - Removed localStorage token storage, cookies sent automatically with credentials (modules/standalone/frontend/src/services/api.ts:40-100)
- **CSRF protection added** - Extracts CSRF token from cookies and sends with state-changing requests (modules/standalone/frontend/src/services/api.ts:47-52, 94-100)
- **Security headers configured** - Added Content-Security-Policy and enhanced X-Frame-Options in nginx (modules/standalone/frontend/nginx.conf:12-32)

### 🔥 Cool Features Worth Exploring

- **Advanced Performance Monitoring** - Real-time Core Web Vitals tracking with threshold-based alerting (src/services/performance.ts:34-283)
- **Comprehensive Testing Suite** - 85%+ coverage target with Playwright E2E, Vitest unit tests, and axe-core accessibility testing (10 test files across the codebase)
- **Production-Ready Docker Stack** - Multi-stage build with nginx optimization, security headers, and health checks (Dockerfile:1-36, nginx.conf:1-146)
- **WebGL Graph Visualization** - Sigma.js integration supporting 10,000+ nodes at 60fps with dynamic layouts (src/components/Graph/SigmaGraph.tsx:1-224)
- **Robust State Management** - Zustand stores with persistence, devtools integration, and proper TypeScript typing (src/store/useUIStore.ts:1-137)
- **WebSocket Auto-Reconnection** - Exponential backoff strategy with heartbeat monitoring and graceful degradation (src/services/websocket.ts:209-233)

### ⚠️ Remaining Issues to Investigate

- **No Input Sanitization** - User input not sanitized before rendering, potential XSS risk (various components)
- **Incomplete Error Logging** - Production error monitoring commented out, only console.error (src/components/Common/ErrorBoundary.tsx:33-36)
- **Limited Test Coverage** - Only 10 test files for 4,196 lines of component code (~2% file coverage)

---

**Generated:** 2025-11-24
**Module:** Frontend Interface
**Developer:** D-JSimpson
**Total Tasks:** 42
**Estimated Effort:** 8-10 days
**Note:** Includes Phase 3 (Testing Suite) and Phase 4 (Production Prep) enhancements completed November 9, 2025

## Critical (P0) - Block release

### Security

**TASK-FRONTEND-001: Implement CSRF protection for all state-changing requests**
- **Location:** src/services/api.ts:42-56
- **Issue:** No CSRF token validation on POST/PUT/DELETE requests
- **Impact:** Vulnerable to cross-site request forgery attacks
- **STATUS UPDATE (2025-11-25):** ✅ FIXED
  - CSRF token handling implemented with double-submit cookie pattern
  - Token extracted from cookies and sent with all state-changing requests
  - X-CSRF-Token header added to POST/PUT/DELETE/PATCH requests
  - Backend validation ensures token matches cookie value
- **Code Example:**
  ```typescript
  // In setupInterceptors()
  const csrfToken = getCsrfToken(); // Get from secure cookie
  if (config.method !== 'GET' && config.method !== 'HEAD') {
    config.headers['X-CSRF-Token'] = csrfToken;
  }
  ```
- **Estimated Effort:** 4 hours (COMPLETED)
- **Priority:** P0 - Critical security vulnerability

**TASK-FRONTEND-002: Move authentication tokens from localStorage to httpOnly cookies**
- **Location:** src/services/api.ts:45-48, 68-69
- **Issue:** JWT tokens stored in localStorage accessible to any XSS attack
- **Impact:** Token theft vulnerability, session hijacking risk
- **STATUS UPDATE (2025-11-25):** ✅ FIXED
  - Tokens moved from localStorage to httpOnly cookies
  - Cookies marked as Secure (HTTPS only) and SameSite=Strict
  - Frontend automatically sends cookies with all requests (credentials: 'include')
  - All localStorage token operations removed
  - Refresh token flow updated to use cookie-based approach
  - Completes CSRF protection implementation (see TASK-FRONTEND-001)
- **Code to Remove:**
  ```typescript
  // Lines 45-48, 68-69 - all localStorage token operations
  localStorage.getItem('access_token')
  localStorage.removeItem('access_token')
  ```
- **Estimated Effort:** 6 hours (COMPLETED - backend coordination completed)
- **Priority:** P0 - High security risk

**TASK-FRONTEND-003: Add Content Security Policy (CSP) headers**
- **Location:** nginx.conf:12-19
- **Issue:** Missing CSP headers allow inline scripts and unrestricted content sources
- **Impact:** XSS attacks not mitigated by browser security
- **STATUS UPDATE (2025-11-25):** ✅ FIXED
  - Content-Security-Policy header added to nginx configuration
  - Strict CSP enforces: default-src 'self', script-src 'self', style-src 'self', img-src 'self' data: https:
  - Additional headers added: X-Frame-Options (DENY), X-Content-Type-Options (nosniff), X-XSS-Protection
  - All inline scripts removed and moved to external files
  - Tested in production environment
  - Comprehensive security headers configured for defense-in-depth
- **Implementation:**
  ```nginx
  add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' ws: wss:; font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none';" always;
  ```
- **Estimated Effort:** 4 hours (COMPLETED)
- **Priority:** P0 - Required for production security

**TASK-FRONTEND-004: Implement DOMPurify for user-generated content sanitization**
- **Location:** src/components/Feed/ResearchItemCard.tsx, src/components/Graph/NodeDetailsPanel.tsx
- **Issue:** User content rendered without sanitization (potential dangerouslySetInnerHTML usage)
- **Impact:** Stored XSS attacks possible through malicious content
- **Remediation:**
  1. Install DOMPurify: `npm install dompurify @types/dompurify`
  2. Create sanitization utility in src/utils/sanitize.ts
  3. Sanitize all user-generated HTML before rendering
  4. Apply to research item content, entity names, relationship labels
- **Implementation:**
  ```typescript
  import DOMPurify from 'dompurify';
  export const sanitizeHtml = (dirty: string): string => {
    return DOMPurify.sanitize(dirty, {
      ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
      ALLOWED_ATTR: ['href', 'title']
    });
  };
  ```
- **Estimated Effort:** 3 hours
- **Priority:** P0 - XSS prevention

**TASK-FRONTEND-005: Integrate production error monitoring service**
- **Location:** src/components/Common/ErrorBoundary.tsx:33-36
- **Issue:** Error monitoring commented out, only logging to console
- **Impact:** Production errors invisible, no observability
- **Remediation:**
  1. Integrate Sentry or similar service
  2. Add error context (user ID, route, component stack)
  3. Configure source maps for production debugging
  4. Set up error alerting thresholds
- **Implementation:**
  ```typescript
  import * as Sentry from '@sentry/react';

  // In componentDidCatch
  Sentry.captureException(error, {
    contexts: {
      component: { errorInfo },
      user: { id: userId, email: userEmail }
    }
  });
  ```
- **Estimated Effort:** 4 hours
- **Priority:** P0 - Production observability required

## High Priority (P1) - Complete before next version

### Testing

**TASK-FRONTEND-006: Increase test coverage to 80%+ for critical paths**
- **Location:** All component files (4,196 lines with only 10 test files)
- **Issue:** ~2% test file coverage, insufficient for production confidence
- **Impact:** High regression risk, difficult to refactor safely
- **Missing Coverage:**
  - src/pages/Feed/FeedPage.tsx - no tests
  - src/pages/Lab/GraphLabPage.tsx - no tests
  - src/pages/Settings/SettingsPage.tsx - no tests
  - src/components/Layout/ThreePanelLayout.tsx - no tests
  - src/store/useGraphStore.ts - no tests
- **Remediation:**
  1. Add component tests for all pages (Feed, Lab, Settings)
  2. Add store tests for all Zustand stores
  3. Add integration tests for critical user flows
  4. Target 80% line coverage minimum
- **Estimated Effort:** 16 hours
- **Priority:** P1 - Quality gate for production

**TASK-FRONTEND-007: Add E2E tests for complete user journeys**
- **Location:** tests/e2e/ (only 1 file: user-journey.spec.ts)
- **Issue:** Insufficient end-to-end test scenarios
- **Impact:** User-facing bugs not caught before production
- **Missing Scenarios:**
  - Onboarding flow (topic selection → directory browsing → feed)
  - Graph interaction (node selection → details panel → export)
  - Settings management (theme change → notification config → save)
  - WebSocket reconnection handling
  - Offline mode behavior
- **Estimated Effort:** 12 hours
- **Priority:** P1 - Critical user flows validation

**TASK-FRONTEND-008: Implement visual regression testing**
- **Location:** New - tests/visual/
- **Issue:** No visual regression tests, UI changes undetected
- **Impact:** Visual bugs, accessibility regressions, design inconsistencies
- **Remediation:**
  1. Set up Percy or Chromatic for visual testing
  2. Add snapshots for all major pages
  3. Capture mobile and desktop variants
  4. Test dark/light theme variants
  5. Integrate into CI pipeline
- **Estimated Effort:** 8 hours
- **Priority:** P1 - UI quality assurance

### Performance

**TASK-FRONTEND-009: Optimize bundle size (currently approaching 1MB limit)**
- **Location:** vite.config.ts:90 (chunkSizeWarningLimit: 1000)
- **Issue:** Bundle size near warning threshold, no code splitting for routes
- **Impact:** Slow initial load, poor mobile experience
- **Current Analysis:**
  - graph-vendor chunk includes large Sigma.js library
  - No lazy loading for route components
  - All design iterations bundled in production
- **Remediation:**
  1. Implement React.lazy() for all route components
  2. Exclude design-iterations from production build
  3. Split graph vendor into smaller chunks (sigma + graphology separate)
  4. Analyze bundle with `npm run analyze` before/after
  5. Target <800KB total bundle size
- **Implementation:**
  ```typescript
  const FeedPage = React.lazy(() => import('@/pages/Feed/FeedPage'));
  const GraphLabPage = React.lazy(() => import('@/pages/Lab/GraphLabPage'));
  ```
- **Estimated Effort:** 6 hours
- **Priority:** P1 - Performance target

**TASK-FRONTEND-010: Implement React Query cache optimization**
- **Location:** src/services/api.ts (uses TanStack Query but no custom configuration)
- **Issue:** No cache configuration, potential over-fetching
- **Impact:** Unnecessary API calls, slower user experience
- **Remediation:**
  1. Configure staleTime and cacheTime per query type
  2. Implement optimistic updates for mutations
  3. Add request deduplication
  4. Configure cache persistence for offline support
- **Implementation:**
  ```typescript
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 5 * 60 * 1000, // 5 minutes
        cacheTime: 10 * 60 * 1000, // 10 minutes
        refetchOnWindowFocus: false,
      }
    }
  });
  ```
- **Estimated Effort:** 4 hours
- **Priority:** P1 - Performance improvement

### Accessibility

**TASK-FRONTEND-011: Fix accessibility test failures in skip links**
- **Location:** src/test/accessibility.test.ts:45-53
- **Issue:** Test expects skip link but implementation missing
- **Impact:** Keyboard users cannot skip to main content
- **Remediation:**
  1. Add skip link to ThreePanelLayout component
  2. Ensure it's visually hidden until focused
  3. Target main content landmark with id="main-content"
  4. Test with keyboard navigation
- **Implementation:**
  ```tsx
  <a href="#main-content" className="sr-only focus:not-sr-only">
    Skip to main content
  </a>
  ```
- **Estimated Effort:** 2 hours
- **Priority:** P1 - WCAG 2.1 AA compliance

**TASK-FRONTEND-012: Ensure all interactive elements have accessible names**
- **Location:** src/test/accessibility.test.ts:114-126
- **Issue:** Test checks for button labels but some buttons missing aria-label
- **Impact:** Screen reader users cannot understand button purpose
- **Remediation:**
  1. Audit all icon-only buttons (collapse, settings, close)
  2. Add aria-label to all buttons without visible text
  3. Use aria-labelledby for buttons with associated text
  4. Test with NVDA/JAWS screen readers
- **Estimated Effort:** 3 hours
- **Priority:** P1 - Accessibility requirement

**TASK-FRONTEND-013: Implement keyboard focus management in modal dialogs**
- **Location:** src/test/accessibility.test.ts:55-67
- **Issue:** Modal dialogs don't trap focus properly
- **Impact:** Keyboard users can tab out of modals to background
- **Remediation:**
  1. Use Radix UI Dialog focus trap (already installed)
  2. Ensure first focusable element receives focus on open
  3. Return focus to trigger element on close
  4. Test with Tab and Shift+Tab navigation
- **Estimated Effort:** 2 hours
- **Priority:** P1 - Critical for keyboard navigation

## Medium Priority (P2) - Schedule for next sprint

### Architecture

**TASK-FRONTEND-014: Extract API client configuration to environment variables**
- **Location:** src/services/api.ts:27-35
- **Issue:** API base URL hardcoded, timeout values not configurable
- **Impact:** Difficult to switch between environments, cannot tune for production
- **Remediation:**
  1. Add VITE_API_TIMEOUT environment variable
  2. Add VITE_API_RETRY_ATTEMPTS environment variable
  3. Update .env.example with new variables
  4. Document in README.md
- **Estimated Effort:** 1 hour
- **Priority:** P2 - Configuration flexibility

**TASK-FRONTEND-015: Implement proper error type hierarchy**
- **Location:** src/services/api.ts:11-21 (only ApiError class)
- **Issue:** Single error type, no distinction between network/validation/auth errors
- **Impact:** Generic error handling, poor user experience
- **Remediation:**
  1. Create NetworkError, ValidationError, AuthError subclasses
  2. Update error interceptor to use appropriate error types
  3. Add retry logic for NetworkError only
  4. Show user-friendly messages per error type
- **Estimated Effort:** 3 hours
- **Priority:** P2 - Better error UX

**TASK-FRONTEND-016: Add TypeScript path alias validation**
- **Location:** tsconfig.json:23-33, vite.config.ts:19-30
- **Issue:** Path aliases defined in both files, no validation they match
- **Impact:** Import resolution failures at build time
- **Remediation:**
  1. Create shared alias configuration file
  2. Import into both tsconfig.json and vite.config.ts
  3. Add build step to validate alias consistency
- **Estimated Effort:** 2 hours
- **Priority:** P2 - Developer experience

### State Management

**TASK-FRONTEND-017: Add Zustand store unit tests**
- **Location:** src/store/useUIStore.ts, useUserStore.ts, useGraphStore.ts (no tests)
- **Issue:** Complex state logic untested
- **Impact:** State mutations may break, difficult to refactor
- **Test Scenarios:**
  - Theme changes update DOM correctly
  - Notifications auto-dismiss after duration
  - Sidebar collapse state persists
  - Right panel visibility toggles
- **Estimated Effort:** 4 hours
- **Priority:** P2 - State reliability

**TASK-FRONTEND-018: Implement state persistence versioning**
- **Location:** src/store/useUIStore.ts:124-131
- **Issue:** No migration strategy for persisted state schema changes
- **Impact:** Breaking changes corrupt user's persisted state
- **Remediation:**
  1. Add version field to persisted state
  2. Implement migration function for version upgrades
  3. Clear invalid state versions
  4. Log migrations for debugging
- **Implementation:**
  ```typescript
  persist(
    (set, get) => ({ ...initialState }),
    {
      name: 'ui-store',
      version: 1,
      migrate: (persistedState, version) => {
        if (version === 0) {
          return { ...defaultState, theme: persistedState.theme };
        }
        return persistedState;
      }
    }
  )
  ```
- **Estimated Effort:** 2 hours
- **Priority:** P2 - Data integrity

### WebSocket

**TASK-FRONTEND-019: Add WebSocket connection retry with jitter**
- **Location:** src/services/websocket.ts:209-233
- **Issue:** Exponential backoff without jitter causes thundering herd
- **Impact:** All disconnected clients reconnect simultaneously
- **Remediation:**
  1. Add random jitter to reconnection delay
  2. Implement connection slot throttling
  3. Add circuit breaker after max failures
- **Implementation:**
  ```typescript
  const jitter = Math.random() * 1000; // 0-1s random
  const delay = Math.min(
    this.config.reconnectInterval * Math.pow(2, attempts) + jitter,
    30000
  );
  ```
- **Estimated Effort:** 2 hours
- **Priority:** P2 - Better scalability

**TASK-FRONTEND-020: Implement WebSocket message queue**
- **Location:** src/services/websocket.ts:170-174
- **Issue:** Messages sent while disconnected are dropped
- **Impact:** Data loss during reconnection periods
- **Remediation:**
  1. Create message queue for offline messages
  2. Replay queue after reconnection
  3. Add queue size limits
  4. Implement message deduplication
- **Estimated Effort:** 4 hours
- **Priority:** P2 - Reliability improvement

**TASK-FRONTEND-021: Add WebSocket subscription persistence**
- **Location:** src/services/websocket.ts:126-143
- **Issue:** Subscriptions lost on reconnection
- **Impact:** Real-time updates stop after reconnect
- **Remediation:**
  1. Store active subscriptions in memory
  2. Re-subscribe automatically after reconnect
  3. Add subscription state to UI store
  4. Show subscription status to user
- **Estimated Effort:** 3 hours
- **Priority:** P2 - UX improvement

### Performance Monitoring

**TASK-FRONTEND-022: Add custom performance marks for key user actions**
- **Location:** src/services/performance.ts:64-78
- **Issue:** Only measuring browser metrics, no application-specific timing
- **Impact:** Cannot correlate performance issues with user actions
- **Remediation:**
  1. Add performance.mark() for graph rendering
  2. Track feed scroll performance
  3. Measure WebSocket message processing time
  4. Create dashboard of custom metrics
- **Implementation:**
  ```typescript
  performance.mark('graph-render-start');
  // ... render graph
  performance.mark('graph-render-end');
  performance.measure('graph-render', 'graph-render-start', 'graph-render-end');
  ```
- **Estimated Effort:** 3 hours
- **Priority:** P2 - Better observability

**TASK-FRONTEND-023: Implement performance budget enforcement**
- **Location:** vite.config.ts (no budget configuration)
- **Issue:** No automated checks for bundle size increases
- **Impact:** Performance regressions go unnoticed
- **Remediation:**
  1. Add bundlesize package to devDependencies
  2. Configure bundle size limits per chunk
  3. Add budget check to CI pipeline
  4. Fail builds that exceed budget
- **Implementation:**
  ```json
  "bundlesize": [
    { "path": "dist/assets/js/index-*.js", "maxSize": "300 KB" },
    { "path": "dist/assets/js/graph-vendor-*.js", "maxSize": "400 KB" }
  ]
  ```
- **Estimated Effort:** 2 hours
- **Priority:** P2 - Performance protection

### Graph Visualization

**TASK-FRONTEND-024: Add graph layout persistence**
- **Location:** src/components/Graph/SigmaGraph.tsx:23-88
- **Issue:** Graph layout randomized on every render
- **Impact:** Disorienting user experience, loss of spatial memory
- **Remediation:**
  1. Save node positions to localStorage after user adjustments
  2. Restore positions on next render
  3. Add "Reset Layout" button
  4. Implement smart layout updates (preserve positions of existing nodes)
- **Estimated Effort:** 4 hours
- **Priority:** P2 - UX improvement

**TASK-FRONTEND-025: Implement graph interaction analytics**
- **Location:** src/components/Graph/SigmaGraph.tsx (no analytics)
- **Issue:** No tracking of graph interactions
- **Impact:** Cannot understand how users explore graphs
- **Remediation:**
  1. Track node clicks, hover time, zoom levels
  2. Record most-viewed entity types
  3. Measure graph rendering performance per size
  4. Send to analytics service
- **Estimated Effort:** 3 hours
- **Priority:** P2 - Product insights

**TASK-FRONTEND-026: Add graph export functionality**
- **Location:** Missing implementation (mentioned in README)
- **Issue:** Export feature incomplete
- **Impact:** Users cannot save or share graph visualizations
- **Remediation:**
  1. Implement PNG export of current graph view
  2. Add SVG export for scalable graphics
  3. Export JSON data for graph state
  4. Add "Share Graph" link generation
- **Estimated Effort:** 6 hours
- **Priority:** P2 - Feature completion

### Component Improvements

**TASK-FRONTEND-027: Add Button component loading state**
- **Location:** src/components/Common/Button.tsx:7-50
- **Issue:** No built-in loading/spinner state
- **Impact:** Developers implement loading inconsistently
- **Remediation:**
  1. Add `isLoading` prop to ButtonProps
  2. Show spinner icon when loading
  3. Disable button during loading
  4. Add loading variant to Storybook
- **Implementation:**
  ```tsx
  interface ButtonProps {
    isLoading?: boolean;
    // ...existing props
  }
  // In render:
  {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  ```
- **Estimated Effort:** 1 hour
- **Priority:** P2 - Component consistency

**TASK-FRONTEND-028: Implement ErrorBoundary per route**
- **Location:** src/App.tsx:24-65 (only top-level ErrorBoundary)
- **Issue:** All errors bubble to top, losing route context
- **Impact:** Error recovery difficult, entire app crashes
- **Remediation:**
  1. Wrap each route with dedicated ErrorBoundary
  2. Provide route-specific fallback UI
  3. Allow navigation to other routes after error
  4. Include route path in error reports
- **Estimated Effort:** 2 hours
- **Priority:** P2 - Better error isolation

**TASK-FRONTEND-029: Add ResearchItemCard actions menu**
- **Location:** src/components/Feed/ResearchItemCard.tsx
- **Issue:** Limited interaction options (save only)
- **Impact:** Missing features: share, report, hide, archive
- **Remediation:**
  1. Add dropdown menu with actions
  2. Implement "Share" (copy link, email, social)
  3. Implement "Report" (inappropriate content)
  4. Implement "Hide" (remove from feed)
  5. Add keyboard shortcuts for actions
- **Estimated Effort:** 4 hours
- **Priority:** P2 - Feature enhancement

### Documentation

**TASK-FRONTEND-030: Create Storybook for component library**
- **Location:** New - .storybook/
- **Issue:** No visual component documentation
- **Impact:** Inconsistent component usage, difficult onboarding
- **Remediation:**
  1. Install Storybook 7.x
  2. Create stories for all Common components
  3. Document all props and variants
  4. Add interactive controls
  5. Deploy to GitHub Pages
- **Estimated Effort:** 8 hours
- **Priority:** P2 - Developer documentation

**TASK-FRONTEND-031: Add JSDoc comments to all public APIs**
- **Location:** All service files (api.ts, websocket.ts, performance.ts)
- **Issue:** No inline documentation for functions
- **Impact:** Unclear usage, frequent code diving
- **Remediation:**
  1. Add JSDoc to all exported functions
  2. Document parameters with types and examples
  3. Add @throws and @returns annotations
  4. Generate API documentation with TypeDoc
- **Estimated Effort:** 4 hours
- **Priority:** P2 - API documentation

## Low Priority (P3) - Nice to have

### Developer Experience

**TASK-FRONTEND-032: Add pre-commit hooks for code quality**
- **Location:** New - .husky/, package.json
- **Issue:** No automated code quality checks before commit
- **Impact:** Low-quality code committed to repository
- **Remediation:**
  1. Install husky and lint-staged: `npm install -D husky lint-staged`
  2. Run ESLint on staged files
  3. Run Prettier formatting
  4. Run type checking
  5. Prevent commits with errors
- **Implementation:**
  ```json
  // In package.json
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "bash -c 'tsc --noEmit'"
    ]
  },
  "scripts": {
    "prepare": "husky install"
  }
  ```
  ```bash
  # .husky/pre-commit
  #!/usr/bin/env sh
  . "$(dirname -- "$0")/_/husky.sh"
  npx lint-staged
  ```
- **Estimated Effort:** 1 hour
- **Priority:** P3 - Team consistency

**TASK-FRONTEND-033: Add GitHub Actions for CI/CD**
- **Location:** New - .github/workflows/
- **Issue:** No continuous integration pipeline
- **Impact:** Manual testing, delayed feedback
- **Remediation:**
  1. Create test.yml workflow (run on PRs)
  2. Create build.yml workflow (validate builds)
  3. Create deploy.yml workflow (deploy to staging)
  4. Add status badges to README
- **Estimated Effort:** 4 hours
- **Priority:** P3 - Automation

**TASK-FRONTEND-034: Configure Renovate for dependency updates**
- **Location:** New - renovate.json
- **Issue:** Manual dependency updates, security vulnerabilities
- **Impact:** Outdated dependencies, security risks
- **Remediation:**
  1. Add renovate.json configuration
  2. Enable automated PRs for updates
  3. Group related updates
  4. Schedule updates weekly
- **Estimated Effort:** 1 hour
- **Priority:** P3 - Maintenance automation

### Internationalization

**TASK-FRONTEND-035: Add i18n infrastructure**
- **Location:** New - src/i18n/
- **Issue:** All text hardcoded in English
- **Impact:** Cannot support international users
- **Remediation:**
  1. Install react-i18next
  2. Extract all strings to translation files
  3. Create en-US.json baseline
  4. Add language switcher to settings
  5. Support RTL layouts
- **Estimated Effort:** 12 hours
- **Priority:** P3 - Internationalization

**TASK-FRONTEND-036: Add date/time localization**
- **Location:** date-fns usage throughout components
- **Issue:** Dates shown in US format only
- **Impact:** Confusing for international users
- **Remediation:**
  1. Use date-fns locale support
  2. Detect user's browser locale
  3. Format dates according to locale
  4. Add format preference to settings
- **Estimated Effort:** 3 hours
- **Priority:** P3 - Better UX

### Progressive Web App

**TASK-FRONTEND-037: Add service worker for offline support**
- **Location:** New - src/sw.js
- **Issue:** App requires network connection
- **Impact:** Cannot use during network outages
- **Remediation:**
  1. Add Workbox for service worker generation
  2. Cache static assets
  3. Implement offline fallback page
  4. Add "Install App" prompt
  5. Support background sync
- **Estimated Effort:** 8 hours
- **Priority:** P3 - PWA features

**TASK-FRONTEND-038: Add web app manifest**
- **Location:** New - public/manifest.json
- **Issue:** Cannot install as progressive web app
- **Impact:** Missing mobile app experience
- **Remediation:**
  1. Create manifest.json with app metadata
  2. Add app icons (192x192, 512x512)
  3. Configure theme colors
  4. Add splash screen
- **Estimated Effort:** 2 hours
- **Priority:** P3 - Installation

### Analytics & Monitoring

**TASK-FRONTEND-039: Implement Google Analytics or Mixpanel**
- **Location:** New - src/services/analytics.ts
- **Issue:** No usage analytics
- **Impact:** Cannot measure feature adoption or user behavior
- **Remediation:**
  1. Choose analytics provider (GA4 or Mixpanel)
  2. Add tracking script
  3. Track page views and navigation
  4. Track custom events (feature usage)
  5. Set up conversion funnels
- **Estimated Effort:** 4 hours
- **Priority:** P3 - Product insights

**TASK-FRONTEND-040: Add Real User Monitoring (RUM)**
- **Location:** Integration with performance monitoring
- **Issue:** Only tracking synthetic performance, not real users
- **Impact:** Don't know actual user experience
- **Remediation:**
  1. Integrate DataDog RUM or similar
  2. Track real user Core Web Vitals
  3. Monitor error rates by browser/device
  4. Set up performance alerts
- **Estimated Effort:** 3 hours
- **Priority:** P3 - Observability

### Accessibility Enhancements

**TASK-FRONTEND-041: Add keyboard shortcuts documentation**
- **Location:** New - src/pages/Help/KeyboardShortcuts.tsx
- **Issue:** Keyboard shortcuts exist but undocumented
- **Impact:** Power users cannot discover shortcuts
- **Remediation:**
  1. Create keyboard shortcuts help page
  2. Add "Press ? for help" hint
  3. Document all shortcuts (navigation, actions, graph)
  4. Make printable cheat sheet
- **Estimated Effort:** 3 hours
- **Priority:** P3 - Discoverability

**TASK-FRONTEND-042: Implement dark mode auto-scheduling**
- **Location:** src/store/useUIStore.ts:38-51
- **Issue:** Auto theme only uses system preference
- **Impact:** Cannot schedule dark mode for specific times
- **Remediation:**
  1. Add "Auto (Scheduled)" theme option
  2. Let users set dark mode start/end times
  3. Automatically switch at scheduled times
  4. Respect system override
- **Estimated Effort:** 2 hours
- **Priority:** P3 - User preference

---

## Summary by Priority

- **P0 (Critical):** 5 tasks, ~21 hours - Security and error monitoring
- **P1 (High):** 8 tasks, ~59 hours - Testing, performance, accessibility
- **P2 (Medium):** 19 tasks, ~63 hours - Architecture, features, monitoring
- **P3 (Low):** 10 tasks, ~48 hours - Nice-to-have features and polish

**Total:** 42 tasks, ~191 hours (~24 working days)

**Recommended Sprint Plan:**
1. **Sprint 1 (Week 1):** Complete all P0 tasks + start P1 testing
2. **Sprint 2 (Week 2):** Complete P1 tasks
3. **Sprint 3-4 (Weeks 3-4):** Select P2 tasks based on roadmap priorities
