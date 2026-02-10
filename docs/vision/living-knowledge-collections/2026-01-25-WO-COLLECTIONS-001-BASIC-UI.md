# WO-COLLECTIONS-001: Basic UI - Collection List & Detail Views

**Phase:** 0 → MVP
**Priority:** P0 - Critical Path
**Estimated Effort:** 3-4 days
**Dependencies:** WO-COLLECTIONS-000 (Foundation)
**Blocks:** Widget system, Evolution engine UI

---

## Objective

Build the core UI for browsing, creating, and editing collections. Simple CRUD interface without fancy widgets yet.

---

## Scope

### In Scope
- Collection index/list view
- Collection detail view
- Create collection form
- Add/edit item forms
- Basic confidence indicators
- Citation input UI

### Out of Scope
- Fancy widget rendering (WO-002)
- Evolution engine (WO-003)
- Inter-collection links (WO-004)
- Templates/presentations (WO-005)

---

## Deliverables

### D1: Collection Index Page

**File:** `components/collections/CollectionIndex.tsx`

```tsx
// Features:
// - Grid of collection cards
// - Filter by type, domain, confidence
// - Sort by updated, confidence, items
// - Search by title
// - "+ New Collection" button
```

**Card shows:**
- Title
- Type badge
- Item count
- Confidence indicator (color-coded)
- Last updated
- Quick actions (open, edit, delete)

### D2: Collection Detail Page

**File:** `components/collections/CollectionDetail.tsx`

```tsx
// Features:
// - Header with title, description, confidence
// - Items list (table or cards based on type)
// - Add item button
// - Edit collection metadata
// - Bulk actions (verify all, delete selected)
```

### D3: Create/Edit Collection Modal

**File:** `components/collections/CollectionForm.tsx`

```tsx
// Features:
// - Title, description inputs
// - Type selector (dropdown with icons)
// - Schema selector (filtered by type)
// - Domain/tags input
// - Public/private toggle
```

### D4: Item Form

**File:** `components/collections/ItemForm.tsx`

```tsx
// Features:
// - Dynamic fields based on schema
// - Citation input with URL validation
// - Assumption toggle per field
// - Confidence slider
// - Save/cancel buttons
```

### D5: Confidence Indicator Component

**File:** `components/collections/ConfidenceIndicator.tsx`

```tsx
// Visual representations:
// - Overall score (0-100%)
// - Color coding: green (80%+), yellow (50-80%), red (<50%)
// - Breakdown tooltip on hover
// - Animated ring or bar
```

---

## UI Mockup

```
┌─────────────────────────────────────────────────────────┐
│ COLLECTIONS                           [+ New Collection] │
├─────────────────────────────────────────────────────────┤
│ Filter: [All Types ▼] [All Domains ▼]  Search: [____]   │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────┐│
│ │ 📊 Top 10 LLMs  │ │ 🎵 Music Stack  │ │ 📄 AI Papers││
│ │                 │ │                 │ │             ││
│ │ ranking         │ │ ecosystem       │ │ ranking     ││
│ │ 10 items        │ │ 23 items        │ │ 50 items    ││
│ │ ████████░░ 85%  │ │ ██████░░░░ 62%  │ │ ███████░░ 78%│
│ │ Updated 2h ago  │ │ Updated 1d ago  │ │ Updated 5d  ││
│ └─────────────────┘ └─────────────────┘ └─────────────┘│
└─────────────────────────────────────────────────────────┘

Collection Detail:
┌─────────────────────────────────────────────────────────┐
│ ← Back                                                   │
│ Top 10 LLMs 2026                              [Edit]    │
│ The most capable large language models                  │
│ Confidence: ████████░░ 85%  │  10 items  │  Updated 2h │
├─────────────────────────────────────────────────────────┤
│ [+ Add Item]                    Sort: [Rank ▼]          │
├─────────────────────────────────────────────────────────┤
│ #1 │ Claude 4 Opus │ Anthropic │ 94.2 │ 🟢 Verified    │
│ #2 │ GPT-5        │ OpenAI    │ 93.8 │ 🟡 Cited       │
│ #3 │ Gemini Ultra │ Google    │ 92.1 │ 🟢 Verified    │
│ ...                                                      │
└─────────────────────────────────────────────────────────┘
```

---

## Acceptance Criteria

- [ ] Can browse all collections in index view
- [ ] Can filter and search collections
- [ ] Can create new collection with schema
- [ ] Can view collection detail with items
- [ ] Can add/edit/delete items
- [ ] Confidence displays correctly
- [ ] Citations captured and displayed
- [ ] Responsive layout (mobile-friendly)

---

## Next Work Order

→ **WO-COLLECTIONS-002: Widget System - Visual Components**
