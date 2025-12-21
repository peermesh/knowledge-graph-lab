# Phase 4: Publish Mode - Review Queue & Destinations

## Objective

Build the Publish mode interface for reviewing pending publications and managing publishing destinations.

## What to Build

### 1. Review Queue Components

**PublishQueue.tsx**
Main container for pending publications.

Props:
```typescript
interface PublishQueueProps {
  items: PendingPublication[];
  onApprove: (id: string) => void;
  onSkip: (id: string) => void;
}
```

**PublicationCard.tsx**
A card showing content pending approval.

Props:
```typescript
interface PublicationCardProps {
  item: {
    id: string;
    content: string;
    destination: string; // 'email' | 'twitter' | 'linkedin' | etc
    scheduledTime: Date;
    sourceFinding: {
      title: string;
      domain: string;
    };
  };
  onApprove: () => void;
  onSkip: () => void;
}
```

Visual design:
- Card shows the content that will be published
- Destination indicated with icon and label
- Scheduled time shown
- Source finding reference (what generated this)
- Two clear action buttons: Approve (checkmark) and Skip (X)
- Swipe gestures on mobile: right to approve, left to skip

**EmptyQueueState.tsx**
Shown when no items pending.
- Friendly message: "All caught up!"
- Maybe show recent publishing activity summary

### 2. Destinations Management

**DestinationsList.tsx**
List of configured publishing destinations.

Props:
```typescript
interface DestinationsListProps {
  destinations: Destination[];
  onAdd: () => void;
  onEdit: (id: string) => void;
  onToggle: (id: string, enabled: boolean) => void;
  onDelete: (id: string) => void;
}
```

**DestinationRow.tsx**
A single destination entry.

Content:
- Icon for destination type (email, phone, Twitter, LinkedIn, etc)
- Destination name/identifier (email address, @handle, etc)
- Enabled/disabled toggle
- Edit button
- Status indicator (connected, error, etc)

**AddDestinationFlow.tsx**
Simple flow for adding a destination.

For this prototype, just show a form:
- Destination type selector (dropdown)
- Type-specific fields (email address, phone number, or "Connect" button for social)
- For social platforms, show a mock "Connected" state after clicking connect

### 3. Publishing Settings Per Domain

**DomainPublishSettings.tsx**
Configure how a specific domain publishes.

Content:
- Domain name at top
- List of destinations with toggles (which destinations receive this domain's content)
- Trust level selector per destination: "Auto-publish" or "Review first"

This could be a slide-out panel or modal.

### 4. Mock Data

```typescript
// src/fixtures/publishing.ts
export const mockPendingPublications: PendingPublication[] = [
  {
    id: 'p1',
    content: 'Tesla announces breakthrough in battery cell efficiency, claiming 20% improvement in energy density.',
    destination: 'twitter',
    scheduledTime: new Date('2025-01-20T09:00:00'),
    sourceFinding: {
      title: 'Tesla Battery Breakthrough',
      domain: 'Electric Vehicles'
    }
  },
  {
    id: 'p2',
    content: 'Weekly EV Industry Summary: This week saw major announcements from Tesla, Rivian, and BYD...',
    destination: 'email',
    scheduledTime: new Date('2025-01-20T08:00:00'),
    sourceFinding: {
      title: 'Weekly Summary',
      domain: 'Electric Vehicles'
    }
  },
  // ... more
];

export const mockDestinations: Destination[] = [
  { id: 'dest1', type: 'email', identifier: 'me@example.com', enabled: true, status: 'connected' },
  { id: 'dest2', type: 'phone', identifier: '+1 555-0123', enabled: true, status: 'connected' },
  { id: 'dest3', type: 'twitter', identifier: '@myhandle', enabled: false, status: 'connected' },
  { id: 'dest4', type: 'linkedin', identifier: 'My Profile', enabled: true, status: 'error' },
];
```

### 5. Publish Page Assembly

Update `PublishPage.tsx`:

Layout:
- Desktop: Two columns - queue on left (60%), destinations on right (40%)
- Mobile: Tabs or toggle between "Review" and "Destinations" views

Content:
- Review queue with pending items
- Destinations list with management options
- Badge on nav shows pending count

### 6. Swipe Interaction (Mobile)

Implement swipe gestures on publication cards:
- Swipe right → Approve (green reveal)
- Swipe left → Skip (red/gray reveal)
- Use a library like react-swipeable or implement with touch events

## Acceptance Criteria

- [ ] Pending publications display as cards
- [ ] Approve and Skip buttons work (remove item from queue)
- [ ] Swipe gestures work on mobile
- [ ] Empty state shows when queue is empty
- [ ] Destinations list shows all configured destinations
- [ ] Can toggle destinations enabled/disabled
- [ ] Add destination flow works (mock connection for social)
- [ ] Per-domain publishing settings accessible
- [ ] Trust level toggle (auto vs review) works
- [ ] Pending count shows in navigation badge
- [ ] Desktop and mobile layouts work

## Design Notes

- Approval actions should feel satisfying (subtle animation)
- Make the approve action more prominent than skip
- Destination icons should be recognizable
- Error states should be clear but not alarming
- Keep the review flow fast - minimize friction

## Do NOT Build Yet

- Real OAuth connections to social platforms
- Content editing before publish
- Scheduling modifications
- Publishing history/analytics
- Bulk approve/skip
