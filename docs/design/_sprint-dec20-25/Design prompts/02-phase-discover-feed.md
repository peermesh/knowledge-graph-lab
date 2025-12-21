# Phase 2: Discover Mode - Feed Interface

## Objective

Build the Discover mode feed experience. This is where users browse findings from their research streams and encounter suggestions for expanding their interests.

## What to Build

### 1. Feed Components

**FindingCard.tsx**
A card displaying a single research finding.

Props:
```typescript
interface FindingCardProps {
  id: string;
  title: string;
  summary: string;
  source: string;
  timestamp: Date;
  domain: string;
  imageUrl?: string;
}
```

Visual design:
- Clean card with subtle border or shadow
- Title prominent (16-18px)
- Summary text truncated to 2-3 lines
- Source and timestamp in muted text
- Domain shown as small tag/pill
- Optional thumbnail image on right side
- Tap/click opens expanded view (Phase 2b)

**SuggestionCard.tsx**
Periodically appears in feed to suggest new research topics.

Props:
```typescript
interface SuggestionCardProps {
  prompt: string; // "Based on your EV interest..."
  suggestions: Array<{
    id: string;
    label: string;
    description: string;
  }>;
  onAdd: (id: string) => void;
  onDismiss: () => void;
}
```

Visual design:
- Visually distinct from finding cards (different background or border)
- Prompt text at top
- 2-3 tappable suggestion pills/buttons
- Dismiss/skip option
- Friendly, non-pushy tone

**FeedList.tsx**
Container that renders the feed.
- Virtualized scrolling for performance (use react-window or similar)
- Intersperse SuggestionCards every 8-12 findings
- Pull-to-refresh gesture on mobile
- Loading states and empty states

### 2. Quick Domain Assignment

When user wants to save/tag a finding:

**DomainSelector.tsx**
Overlay that appears on long-press (mobile) or right-click (desktop).

- Shows flat list of top-level domains
- Search/filter input at top
- "Add to [domain]" action
- "Create new domain" option at bottom
- Dismisses after selection

For now, just log the action to console. Real assignment comes later.

### 3. Mock Data

Create fixture file with 20-30 mock findings:
```typescript
// src/fixtures/findings.ts
export const mockFindings: Finding[] = [
  {
    id: '1',
    title: 'Tesla Opens New Gigafactory in Mexico',
    summary: 'The facility will focus on producing next-generation battery cells...',
    source: 'Reuters',
    timestamp: new Date('2025-01-15'),
    domain: 'Electric Vehicles',
  },
  // ... more
];
```

Create 2-3 mock suggestions:
```typescript
export const mockSuggestions: Suggestion[] = [
  {
    prompt: 'Based on your EV manufacturing interest',
    suggestions: [
      { id: 's1', label: 'Battery recycling', description: 'End-of-life battery processing' },
      { id: 's2', label: 'Supply chain', description: 'Raw material sourcing' },
    ]
  }
];
```

### 4. Discover Page Assembly

Update `DiscoverPage.tsx`:
- Render FeedList with mock data
- Handle domain assignment interactions (console.log for now)
- Handle suggestion add/dismiss (console.log for now)
- Responsive layout (single column on mobile, comfortable width on desktop)

## Acceptance Criteria

- [ ] Feed displays mock findings as cards
- [ ] Cards show title, summary, source, timestamp, domain tag
- [ ] Suggestion cards appear periodically in feed
- [ ] Long-press/right-click on finding shows domain selector
- [ ] Domain selector has search filter
- [ ] Suggestion pills are tappable (logs to console)
- [ ] Feed scrolls smoothly with many items
- [ ] Empty state shows when no findings
- [ ] Mobile and desktop layouts work

## Design Notes

- Cards should breathe (adequate padding and spacing)
- Avoid visual clutter
- Suggestion cards should feel helpful not intrusive
- Domain selector should appear quickly and be easy to dismiss
- Consider subtle hover states on desktop

## Do NOT Build Yet

- Expanded finding detail view
- Real domain assignment logic
- Filtering or search within feed
- Infinite scroll/pagination
- Real-time updates
