# Knowledge Graph Lab - Design Document

## What "Done" Looks Like

This document describes the complete MVP. When you're lost or unsure, return here to understand what you're building toward.

---

## Product Summary

Knowledge Graph Lab is a personal research automation tool. Users define topics they care about, the system researches those topics continuously, and delivers findings through channels the user chooses.

**The core promise:** "Tell us what you care about. We'll keep you informed."

---

## The Three Modes

The entire application exists in three modes. Users switch between them via navigation. Each mode has one primary job.

### Discover Mode
**Job:** Browse findings and expand research interests.

The user sees a feed of cards. Each card is a finding from their research streams. They scroll, they tap to read more, they assign findings to domains for organization.

Periodically, suggestion cards appear: "Based on your interest in X, you might also want to track Y." Users tap to add new research interests or ignore to skip.

**When done, Discover mode feels like:** A personalized news feed that actually respects your time. Not overwhelming. Not noisy. Just relevant findings presented cleanly.

### Organize Mode
**Job:** Structure research interests into a manageable hierarchy.

The user sees a tree of domains. Top-level domains like "Electric Vehicles" or "AI Regulation" contain nested sub-domains and ideas. They can create, rename, delete, nest, and promote domains.

Selecting a domain shows its details: how many findings are associated, what sub-domains exist, recent activity.

**When done, Organize mode feels like:** A file browser for your curiosity. Familiar, fast, empowering. You're in control of the structure.

### Publish Mode
**Job:** Control what gets shared and where.

The user sees pending publications waiting for approval. Each card shows content, destination, and timing. Two actions: approve or skip.

A destinations section shows configured outputs: email, phone, social platforms. Users can add, remove, enable, or disable destinations. Per-domain settings control which destinations receive which streams, and whether approval is required.

**When done, Publish mode feels like:** A calm review queue. Nothing goes out without your say-so (unless you've chosen to trust auto-publish). You're never surprised by what's shared in your name.

---

## User Journey: New User

1. **Welcome** - App explains its purpose in one sentence
2. **First topic** - User types what they want to research
3. **Frequency** - User picks daily, weekly, or real-time
4. **Delivery** - User enables email, phone, or just in-app
5. **Done** - User lands in Discover mode with their first stream active

Total time: under 2 minutes. No account creation friction in this prototype (mocked).

---

## User Journey: Returning User

1. **Open app** - Lands in Discover mode (or last-used mode)
2. **Browse feed** - Scan findings, assign to domains if desired
3. **Check publications** - Badge shows pending count, review if needed
4. **Organize occasionally** - Restructure domains as interests evolve
5. **Adjust settings rarely** - Change preferences when needed

The app should feel like checking in on a trusted assistant, not managing a complex system.

---

## Visual Design Principles

### Aesthetic Direction
Calm, capable, minimal. Not a dashboard full of charts. Not a busy productivity app. Think: a well-designed reading app meets a personal research assistant.

### Color
- Neutral base (light or dark theme, developer's choice)
- One accent color for interactive elements
- Muted colors for secondary information
- Avoid bright, attention-grabbing colors except for actions

### Typography
- One typeface family is fine
- Clear hierarchy: headings, body, captions
- Generous line height for readability
- No tiny text

### Spacing
- Generous padding inside cards
- Consistent spacing between elements
- Breathing room matters more than density
- White space is a feature, not waste

### Cards
- Subtle borders or shadows, not heavy
- Rounded corners (4-8px)
- Clear tap/click targets
- Hover states on desktop

### Icons
- Simple line icons (Lucide, Feather, or similar)
- Consistent stroke weight
- Meaningful, not decorative

---

## Interaction Patterns

### Navigation
- Desktop: Left rail, always visible, 64px wide
- Mobile: Bottom tab bar, fixed position
- Three primary icons: Discover, Organize, Publish
- Settings accessed via profile icon

### Mode Switching
- Tap nav icon to switch
- Smooth transition (fade or slide, 200-300ms)
- State preserved when switching away and back

### Cards in Feed
- Tap to expand/view detail
- Long-press (mobile) or right-click (desktop) for quick actions
- Swipe gestures on mobile where appropriate

### Tree in Organize
- Tap chevron to expand/collapse
- Tap node to select
- Long-press or right-click for context menu
- Indentation shows hierarchy

### Queue in Publish
- Two clear action buttons per card
- Swipe right to approve, left to skip (mobile)
- Cards animate out when actioned

### Settings
- Slide-out panel from right (desktop)
- Full screen on mobile
- Close via X button or tap outside (desktop)

---

## Component Behavior Reference

### Finding Card (Discover)
| Element | Behavior |
|---------|----------|
| Card tap | Opens finding detail |
| Domain tag tap | Opens that domain in Organize |
| Long-press | Shows domain assignment menu |
| Image | Optional, displays if available |

### Domain Node (Organize)
| Element | Behavior |
|---------|----------|
| Chevron tap | Expand/collapse children |
| Node tap | Select, show detail panel |
| Long-press/right-click | Context menu |
| Finding count badge | Display only |

### Publication Card (Publish)
| Element | Behavior |
|---------|----------|
| Approve button | Removes card, queues for publish |
| Skip button | Removes card, does not publish |
| Swipe right | Same as approve |
| Swipe left | Same as skip |
| Destination icon | Display only |

### Destination Row (Publish)
| Element | Behavior |
|---------|----------|
| Toggle | Enable/disable destination |
| Row tap | Open edit flow |
| Status indicator | Shows connected/error state |

---

## States to Handle

### Loading
- Skeleton cards while content loads
- Subtle pulse animation
- Brief duration even with mock data (demonstrates pattern)

### Empty
- Friendly message explaining what will appear
- Optional illustration or icon
- Call-to-action where appropriate

### Error
- Clear message, not technical jargon
- Retry option when applicable
- Toast for transient errors

### Success
- Brief confirmation (toast or inline)
- No blocking modals for routine actions
- Celebrate sparingly (onboarding complete is okay)

---

## Responsive Behavior

### Mobile (< 768px)
- Single column layouts
- Bottom tab navigation
- Full-screen modals and panels
- Touch-optimized targets (44px minimum)
- Swipe gestures enabled

### Tablet (768px - 1024px)
- Can use either mobile or desktop patterns
- Developer's discretion based on what works

### Desktop (> 1024px)
- Multi-column layouts where appropriate
- Left rail navigation
- Side panels instead of full-screen
- Hover states enabled
- Right-click context menus

---

## Data Model Summary

### Domain
A research topic or interest area. Can contain sub-domains infinitely nested. Has a name and associated finding count.

### Finding
A piece of research output. Has title, summary, source, timestamp, and belongs to a domain. May have an image.

### Pending Publication
Content ready to be published. Has the content text, destination, scheduled time, and reference to source finding.

### Destination
A configured output channel. Has type (email, phone, twitter, etc.), identifier, enabled state, and connection status.

### User
Profile information plus preferences (frequency, timezone, notification settings, publishing defaults).

---

## What's NOT in MVP

These features are intentionally excluded from the first version:

- Real backend integration (everything is mocked)
- Actual authentication (mocked)
- Real AI/LLM processing
- OAuth connections to social platforms
- Content editing before publish
- Search within the app
- Filtering or sorting options
- Drag-and-drop in domain tree
- Keyboard shortcuts
- Analytics or usage tracking
- Multiple user accounts
- Sharing or collaboration
- Import/export of data
- Undo for destructive actions
- Bulk operations

These may come later. For now, focus on the core interaction patterns.

---

## Definition of Done

The prototype is complete when:

1. **Onboarding works** - New user can complete the 4-step flow
2. **Discover works** - Feed displays, suggestions appear, domain assignment functions
3. **Organize works** - Tree displays, all CRUD operations work, detail panel shows
4. **Publish works** - Queue displays, approve/skip work, destinations manageable
5. **Settings work** - Panel opens, preferences editable, persists to localStorage
6. **Navigation works** - All three modes accessible, transitions smooth
7. **Mobile works** - All features functional on small screens
8. **Desktop works** - All features functional with mouse/keyboard
9. **States handled** - Loading, empty, and error states exist
10. **Feels cohesive** - Consistent visual language throughout

---

## Quick Reference: Screen Inventory

| Screen | Mode | Purpose |
|--------|------|---------|
| Onboarding Welcome | - | Introduce app |
| Onboarding Topic | - | Get first research interest |
| Onboarding Frequency | - | Set update cadence |
| Onboarding Delivery | - | Configure destinations |
| Onboarding Complete | - | Confirm and transition |
| Discover Feed | Discover | Browse findings |
| Finding Detail | Discover | Expanded finding view |
| Domain Selector | Discover | Assign finding to domain |
| Domain Tree | Organize | View/manage hierarchy |
| Domain Detail | Organize | Selected domain info |
| Domain Context Menu | Organize | Actions for a domain |
| Move Domain Dialog | Organize | Relocate a domain |
| Publish Queue | Publish | Pending publications |
| Destinations List | Publish | Manage outputs |
| Add Destination | Publish | Configure new output |
| Domain Publish Settings | Publish | Per-domain publish rules |
| Settings Panel | - | Preferences and account |

---

## When You're Stuck

1. Re-read this document
2. Check the phase document for your current phase
3. Look at the component inventory for structure
4. Make a reasonable decision and document it
5. Keep moving - a working prototype beats a perfect plan

The goal is demonstrating the interaction patterns, not building production software. Favor done over perfect.
