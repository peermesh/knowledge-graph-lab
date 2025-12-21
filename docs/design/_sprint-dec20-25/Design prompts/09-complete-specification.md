# Knowledge Graph Lab - Complete UI Specification

## Overview

Build a React/TypeScript prototype for Knowledge Graph Lab, a personal research automation tool. Users define topics they care about, browse research findings, organize them hierarchically, and control how findings get published to various channels.

**Core promise:** "Tell us what you care about. We'll keep you informed."

**Tech stack:** React, TypeScript, React Router, Tailwind CSS, localStorage for persistence.

**This is a prototype:** All data is mocked. No real backend, authentication, or AI processing.

---

## Application Structure

### Three Modes

The app operates in three modes, switched via navigation:

1. **Discover** - Browse research findings feed
2. **Organize** - Manage hierarchical domain tree
3. **Publish** - Review pending publications and manage destinations

### Navigation

**Desktop (> 768px):** Left rail, 64px wide, always visible. Three mode icons stacked vertically, profile/settings icon at bottom.

**Mobile (< 768px):** Bottom tab bar, fixed position. Same four icons horizontally.

Active mode indicated visually. Smooth transitions between modes (200-300ms fade or slide).

### Routes

```
/onboarding - New user flow (4 steps)
/discover - Discover mode (default after auth)
/organize - Organize mode
/publish - Publish mode
```

---

## Data Types

```typescript
interface Finding {
  id: string;
  title: string;
  summary: string;
  source: string;
  timestamp: Date;
  domain: string;
  imageUrl?: string;
}

interface Suggestion {
  id: string;
  prompt: string;
  options: Array<{
    id: string;
    label: string;
    description: string;
  }>;
}

interface DomainNode {
  id: string;
  name: string;
  findingCount: number;
  children: DomainNode[];
}

interface PendingPublication {
  id: string;
  content: string;
  destination: 'email' | 'phone' | 'twitter' | 'linkedin';
  scheduledTime: Date;
  sourceFinding: {
    title: string;
    domain: string;
  };
}

interface Destination {
  id: string;
  type: 'email' | 'phone' | 'twitter' | 'linkedin';
  identifier: string;
  enabled: boolean;
  status: 'connected' | 'error' | 'pending';
}

interface User {
  name: string;
  email: string;
  preferences: {
    defaultFrequency: 'daily' | 'weekly' | 'realtime';
    timezone: string;
    notifications: { email: boolean; push: boolean; sms: boolean };
    publishingDefaults: {
      trustLevel: 'auto' | 'review';
      destinations: string[];
    };
  };
}
```

---

## Onboarding Flow

Four screens for new users. Progress indicator (dots) at bottom.

### Screen 1: Welcome
- App name/logo
- Headline: "Stay informed about what matters"
- One sentence value prop
- "Get Started" button

### Screen 2: First Topic
- Headline: "What would you like to stay informed about?"
- Large text input
- Placeholder examples cycling: "Tesla's manufacturing strategy", "AI regulation updates"
- "Continue" button (disabled until input provided)

### Screen 3: Frequency
- Headline: "How often do you want updates?"
- Three large tappable cards:
  - Daily - "Brief daily digest"
  - Weekly - "Comprehensive weekly summary"
  - Real-time - "As discoveries happen"
- Selected state clearly indicated

### Screen 4: Delivery
- Headline: "Where should we send your findings?"
- Toggle options:
  - "In this app" (always on, not toggleable)
  - "Email" (reveals email input when enabled)
  - "Phone" (reveals phone input when enabled)
- "Finish Setup" button

### Completion
- Success message: "You're all set!"
- Summary of choices
- "Start Exploring" button → redirects to Discover mode

Persist onboarding state to localStorage. Returning users skip onboarding.

---

## Discover Mode

### Feed Layout
Single scrolling column of cards. Comfortable max-width on desktop (600-700px), centered. Full width on mobile with padding.

### Finding Card
Each finding displays as a card:
- Title (prominent, 16-18px)
- Summary (2-3 lines, truncated)
- Source and timestamp (muted text)
- Domain tag (small pill/badge)
- Optional thumbnail image on right

**Interactions:**
- Tap card → expand to show full content (can be modal or inline expansion)
- Long-press (mobile) / right-click (desktop) → show domain selector overlay
- Domain tag tap → navigate to that domain in Organize mode

### Suggestion Card
Appears every 8-12 findings in the feed. Visually distinct (different background or border).

Content:
- Prompt text: "Based on your interest in [X], you might also want to track:"
- 2-3 tappable option pills with label and brief description
- Dismiss/skip link

**Interactions:**
- Tap option → add to research interests (log to console, show toast)
- Tap dismiss → remove suggestion card from feed

### Domain Selector Overlay
Triggered by long-press/right-click on a finding.
- Shows list of top-level domains
- Search/filter input at top
- Tap domain → assign finding, close overlay, show toast confirmation
- "Create new domain" option at bottom
- Tap outside → dismiss

---

## Organize Mode

### Layout
**Desktop:** Domain tree on left (40%), detail panel on right (60%).
**Mobile:** Full-width tree, detail panel in bottom sheet or separate view.

### Domain Tree
Hierarchical list with indentation (16-24px per level).

Each node shows:
- Expand/collapse chevron (if has children)
- Domain name
- Finding count badge (muted)

**Interactions:**
- Tap chevron → expand/collapse
- Tap node → select, show detail panel
- Long-press (mobile) / right-click (desktop) → context menu

### Context Menu Options
- Rename
- Add sub-domain
- Move to... (opens move dialog)
- Promote to top level (if nested)
- Delete (requires confirmation)

### Add Domain
- "+" button at top of tree or within context menu
- Inline text input appears
- Enter to confirm, Escape to cancel

### Move Domain Dialog
Modal showing simplified tree of valid destinations (excludes self and descendants). Tap destination to move, cancel to close.

### Domain Detail Panel
Shows when a domain is selected:
- Domain name (editable inline)
- Finding count
- List of direct sub-domains
- Preview of 3-5 recent findings in this domain
- "View all findings" link (navigates to Discover filtered by domain, or logs to console)

---

## Publish Mode

### Layout
**Desktop:** Two columns - queue (60%) and destinations (40%).
**Mobile:** Tabs or toggle between "Review" and "Destinations" views.

### Pending Publications Queue
List of cards awaiting approval.

Each card shows:
- Content text that will be published
- Destination icon and label
- Scheduled time
- Source finding reference (title and domain)
- Two action buttons: Approve (checkmark) and Skip (X)

**Interactions:**
- Tap Approve → remove card, add to publish queue (log to console)
- Tap Skip → remove card, do not publish
- Swipe right (mobile) → Approve (green reveal animation)
- Swipe left (mobile) → Skip (gray/red reveal animation)

Cards animate out when actioned (slide off screen).

### Empty Queue State
When no pending items:
- Friendly message: "All caught up!"
- Optional: show count of recently published items

### Destinations List
Shows configured publishing destinations.

Each row shows:
- Icon for type (email, phone, twitter, linkedin)
- Identifier (email address, phone number, @handle)
- Enabled/disabled toggle
- Status indicator (connected, error)

**Interactions:**
- Toggle → enable/disable destination
- Tap row → edit destination
- Add button → open add destination flow

### Add Destination Flow
Simple form:
- Destination type dropdown (email, phone, twitter, linkedin)
- Type-specific input (email address, phone number, or "Connect" button for social)
- For social: show mock "Connected" state after clicking connect
- Save/cancel buttons

### Per-Domain Publishing Settings
Accessible from domain detail or as a slide-out panel.

Content:
- Domain name at top
- List of destinations with checkboxes (which receive this domain's content)
- Trust level per destination: "Auto-publish" or "Review first" toggle

---

## Settings Panel

Slide-out panel from right (desktop) or full-screen (mobile). Triggered by profile/settings icon in nav.

### Sections

**Account**
- Profile photo placeholder (display only)
- Name (editable text input)
- Email (display only)
- "Sign Out" button

**Preferences**
- Default update frequency (dropdown: daily/weekly/realtime)
- Time zone (dropdown)
- Notification toggles (email, push, sms)

**Publishing Defaults**
- Default trust level for new streams (dropdown: auto/review)
- Default destinations (checkboxes)

**Data**
- "Export my data" button (mock - just log to console)
- "Delete account" button (mock - show confirmation, log to console)

**About**
- App version: "1.0.0-prototype"
- Links: Help, Privacy Policy, Terms (can be # hrefs)

### Close Behavior
- X button in panel header
- Click outside panel (desktop only)
- Escape key

---

## Visual Design

### Aesthetic
Calm, minimal, capable. Not a busy dashboard. Think: reading app meets research assistant.

### Colors
- Neutral base (light or dark theme)
- One accent color for interactive elements and active states
- Muted colors for secondary text and metadata
- Avoid bright attention-grabbing colors except for primary actions

### Typography
- Single typeface family (something clean, not Inter/Roboto/Arial)
- Clear hierarchy: headings, body text, captions
- Generous line-height (1.5+)
- No text smaller than 14px

### Spacing
- Generous padding inside cards (16-24px)
- Consistent gaps between elements (16px standard)
- Breathing room throughout

### Cards
- Subtle border or shadow, not heavy
- Rounded corners (6-8px)
- Hover state on desktop (slight lift or background change)
- Clear tap targets

### Icons
- Simple line icons (Lucide recommended)
- Consistent stroke weight
- 20-24px size for nav, 16-20px inline

---

## States

### Loading
- Skeleton cards with pulse animation
- Show briefly even with mock data to demonstrate pattern

### Empty
- Friendly message explaining what will appear here
- Simple icon or illustration optional
- Call-to-action where appropriate

### Error
- Clear, non-technical message
- Retry option when applicable
- Use toast for transient errors

### Success
- Brief toast confirmation for actions
- Auto-dismiss after 3 seconds
- No blocking modals for routine actions

---

## Responsive Breakpoints

- **Mobile:** < 768px - single column, bottom nav, touch gestures, full-screen panels
- **Desktop:** ≥ 768px - multi-column where appropriate, left rail nav, hover states, side panels

All features must work on both mobile and desktop.

---

## Mock Data

Create fixture files with:

**Findings (20-30 items):**
```typescript
{ id: '1', title: 'Tesla Opens New Gigafactory in Mexico', summary: 'The facility will focus on next-generation battery production...', source: 'Reuters', timestamp: new Date('2025-01-15'), domain: 'Electric Vehicles' }
```

**Domains (nested structure):**
```typescript
{ id: 'd1', name: 'Electric Vehicles', findingCount: 24, children: [
  { id: 'd1-1', name: 'Battery Technology', findingCount: 12, children: [
    { id: 'd1-1-1', name: 'Solid State', findingCount: 3, children: [] }
  ]}
]}
```

**Pending Publications (5-10 items):**
```typescript
{ id: 'p1', content: 'Tesla announces 20% improvement in battery efficiency...', destination: 'twitter', scheduledTime: new Date('2025-01-20T09:00:00'), sourceFinding: { title: 'Tesla Battery Breakthrough', domain: 'Electric Vehicles' }}
```

**Destinations (4-5 items):**
```typescript
{ id: 'dest1', type: 'email', identifier: 'user@example.com', enabled: true, status: 'connected' }
```

**Suggestions (2-3 items):**
```typescript
{ id: 's1', prompt: 'Based on your EV manufacturing interest', options: [
  { id: 'opt1', label: 'Battery recycling', description: 'End-of-life processing' }
]}
```

---

## File Structure

```
src/
├── components/
│   ├── layout/
│   │   ├── AppShell.tsx
│   │   ├── DesktopNav.tsx
│   │   ├── MobileNav.tsx
│   │   └── SettingsPanel.tsx
│   ├── discover/
│   │   ├── FeedList.tsx
│   │   ├── FindingCard.tsx
│   │   ├── SuggestionCard.tsx
│   │   └── DomainSelector.tsx
│   ├── organize/
│   │   ├── DomainTree.tsx
│   │   ├── DomainNode.tsx
│   │   ├── DomainContextMenu.tsx
│   │   └── DomainDetail.tsx
│   ├── publish/
│   │   ├── PublishQueue.tsx
│   │   ├── PublicationCard.tsx
│   │   ├── DestinationsList.tsx
│   │   └── DestinationRow.tsx
│   ├── onboarding/
│   │   ├── OnboardingWelcome.tsx
│   │   ├── OnboardingTopic.tsx
│   │   ├── OnboardingFrequency.tsx
│   │   └── OnboardingDelivery.tsx
│   └── shared/
│       ├── Toast.tsx
│       ├── Modal.tsx
│       └── EmptyState.tsx
├── pages/
│   ├── DiscoverPage.tsx
│   ├── OrganizePage.tsx
│   ├── PublishPage.tsx
│   └── OnboardingPage.tsx
├── context/
│   └── AppContext.tsx
├── fixtures/
│   ├── findings.ts
│   ├── domains.ts
│   ├── publications.ts
│   └── destinations.ts
├── types/
│   └── index.ts
└── App.tsx
```

---

## Definition of Done

The prototype is complete when:

- [ ] New user can complete 4-step onboarding
- [ ] Discover mode shows feed with finding cards
- [ ] Suggestion cards appear in feed and are interactive
- [ ] Findings can be assigned to domains via long-press/right-click
- [ ] Organize mode shows collapsible domain tree
- [ ] Domains can be created, renamed, deleted, moved, and promoted
- [ ] Selecting domain shows detail panel
- [ ] Publish mode shows pending publications queue
- [ ] Publications can be approved or skipped (including swipe on mobile)
- [ ] Destinations can be viewed, toggled, added
- [ ] Settings panel opens and preferences are editable
- [ ] Navigation works between all three modes
- [ ] Badge shows pending publication count
- [ ] State persists to localStorage
- [ ] Loading, empty, and error states exist
- [ ] Mobile layout works (< 768px)
- [ ] Desktop layout works (≥ 768px)
- [ ] Transitions are smooth
- [ ] Visual design is consistent throughout

---

## What NOT to Build

- Real backend or API integration
- Real authentication
- Real AI/LLM features
- Real OAuth for social platforms
- Search or filtering
- Drag-and-drop in tree
- Keyboard shortcuts
- Analytics
- Multiple accounts
- Sharing/collaboration
- Data import/export
- Undo functionality
- Bulk operations

Focus on the core interaction patterns with mocked data.
