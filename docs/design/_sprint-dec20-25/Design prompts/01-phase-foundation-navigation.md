# Phase 1: Foundation & Navigation Shell

## Objective

Set up the React application shell with routing, authentication wrapper, and the three-mode navigation structure. No real functionality yet, just the skeleton.

## What to Build

### 1. Project Setup
- Create React app with TypeScript
- Install React Router for navigation
- Install Tailwind CSS for styling
- Set up basic folder structure:
  ```
  src/
    components/
      layout/
      shared/
    pages/
      Discover/
      Organize/
      Publish/
      Onboarding/
    hooks/
    utils/
    types/
  ```

### 2. Layout Components

**AppShell.tsx**
- Wrapper component for authenticated state
- Contains navigation and main content area
- Handles responsive behavior (desktop vs mobile)

**DesktopNav.tsx**
- Left rail navigation
- Three icon buttons: Discover, Organize, Publish
- Small profile/settings icon at bottom
- Active state indicator for current mode
- Width: 64px collapsed

**MobileNav.tsx**
- Bottom tab bar
- Same three icons plus profile
- Active state indicator
- Fixed to bottom of viewport

### 3. Page Shells

Create placeholder pages for each mode:
- `DiscoverPage.tsx` - Shows "Discover Mode" text for now
- `OrganizePage.tsx` - Shows "Organize Mode" text for now  
- `PublishPage.tsx` - Shows "Publish Mode" text for now
- `OnboardingPage.tsx` - Shows "Welcome" text for now
- `SettingsPanel.tsx` - Slide-out panel shell (empty for now)

### 4. Routing Setup

```
/onboarding - First-time user flow
/discover - Discover mode (default after auth)
/organize - Organize mode
/publish - Publish mode
```

### 5. Mock Authentication

Simple context that tracks:
- `isAuthenticated: boolean`
- `isNewUser: boolean` (for onboarding redirect)
- `user: { name, email }` (mock data)

Route protection: unauthenticated users see login placeholder, new users redirect to onboarding.

## Acceptance Criteria

- [ ] App loads without errors
- [ ] Three-mode navigation works on desktop (left rail)
- [ ] Three-mode navigation works on mobile (bottom tabs)
- [ ] Clicking nav icons switches between mode pages
- [ ] Active mode is visually indicated in nav
- [ ] Settings panel slides in/out (empty is fine)
- [ ] Routes are defined and working
- [ ] Mock auth context is available throughout app

## Design Notes

- Use a calm, minimal aesthetic
- Dark mode preferred but not required
- Icons should be simple line icons (use Lucide or similar)
- Smooth transitions between modes (fade or slide)
- Nav should feel unobtrusive, not heavy

## Do NOT Build Yet

- Actual page content for any mode
- Real authentication
- Any data fetching
- Complex animations
- Settings content
