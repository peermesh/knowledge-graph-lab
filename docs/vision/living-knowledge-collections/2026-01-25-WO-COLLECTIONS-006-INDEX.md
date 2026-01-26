# WO-COLLECTIONS-006: Faceted Index - Master Navigation

**Phase:** v1.0
**Priority:** P2 - Enhancement
**Estimated Effort:** 2-3 days
**Dependencies:** WO-COLLECTIONS-001 (Basic UI), WO-COLLECTIONS-004 (Links)
**Blocks:** None (Final UI polish)

---

## Objective

Build the master navigation interface for browsing all collections with powerful faceted filtering, search, and discovery features.

---

## Scope

### In Scope
- Faceted filter system
- Multi-dimensional search
- Activity feed (recent updates)
- Quick stats dashboard
- Keyboard navigation

### Out of Scope
- AI-powered recommendations
- Collaborative features
- Advanced analytics

---

## Deliverables

### D1: Facet Definitions

**File:** `types/facets.ts`

```typescript
export interface Facet {
  id: string;
  name: string;
  type: 'single' | 'multi' | 'range';
  options: FacetOption[];
  collapsed?: boolean;
}

export interface FacetOption {
  value: string;
  label: string;
  count: number;
  icon?: string;
  color?: string;
}

export interface FacetState {
  domain: string[];
  type: CollectionType[];
  confidence: 'all' | 'verified' | 'partial' | 'low';
  freshness: 'all' | 'today' | 'week' | 'month' | 'stale';
  creator: 'all' | 'user' | 'ai' | 'imported';
}

export const DEFAULT_FACETS: Facet[] = [
  {
    id: 'domain',
    name: 'Domain',
    type: 'multi',
    options: [], // Dynamically populated
  },
  {
    id: 'type',
    name: 'Type',
    type: 'multi',
    options: [
      { value: 'ranking', label: 'Rankings', icon: '📊', count: 0 },
      { value: 'comparison', label: 'Comparisons', icon: '⚖️', count: 0 },
      { value: 'ecosystem', label: 'Ecosystems', icon: '🔗', count: 0 },
      { value: 'timeline', label: 'Timelines', icon: '📅', count: 0 },
      { value: 'network', label: 'Networks', icon: '👥', count: 0 },
      { value: 'taxonomy', label: 'Taxonomies', icon: '🌳', count: 0 },
    ],
  },
  {
    id: 'confidence',
    name: 'Confidence',
    type: 'single',
    options: [
      { value: 'all', label: 'All', count: 0 },
      { value: 'verified', label: 'Verified (80%+)', color: 'green', count: 0 },
      { value: 'partial', label: 'Partial (50-80%)', color: 'yellow', count: 0 },
      { value: 'low', label: 'Low (<50%)', color: 'red', count: 0 },
    ],
  },
  {
    id: 'freshness',
    name: 'Updated',
    type: 'single',
    options: [
      { value: 'all', label: 'All Time', count: 0 },
      { value: 'today', label: 'Today', count: 0 },
      { value: 'week', label: 'This Week', count: 0 },
      { value: 'month', label: 'This Month', count: 0 },
      { value: 'stale', label: 'Stale', color: 'orange', count: 0 },
    ],
  },
];
```

### D2: Faceted Filter Engine

**File:** `services/facetedSearch.ts`

```typescript
export function filterCollections(
  collections: Collection[],
  facets: FacetState,
  searchQuery: string
): Collection[] {
  return collections.filter(c => {
    // Domain filter
    if (facets.domain.length > 0 && !facets.domain.includes(c.metadata.domain || '')) {
      return false;
    }

    // Type filter
    if (facets.type.length > 0 && !facets.type.includes(c.type)) {
      return false;
    }

    // Confidence filter
    if (facets.confidence !== 'all') {
      const conf = c.confidence.overall;
      if (facets.confidence === 'verified' && conf < 0.8) return false;
      if (facets.confidence === 'partial' && (conf < 0.5 || conf >= 0.8)) return false;
      if (facets.confidence === 'low' && conf >= 0.5) return false;
    }

    // Freshness filter
    if (facets.freshness !== 'all') {
      const updated = new Date(c.updatedAt);
      const now = new Date();
      if (facets.freshness === 'today' && !isToday(updated)) return false;
      if (facets.freshness === 'week' && !isThisWeek(updated)) return false;
      if (facets.freshness === 'month' && !isThisMonth(updated)) return false;
      if (facets.freshness === 'stale' && differenceInDays(now, updated) < 30) return false;
    }

    // Search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      const matchesTitle = c.title.toLowerCase().includes(query);
      const matchesTags = c.metadata.tags.some(t => t.toLowerCase().includes(query));
      const matchesItems = c.items.some(i =>
        JSON.stringify(i.data).toLowerCase().includes(query)
      );
      if (!matchesTitle && !matchesTags && !matchesItems) return false;
    }

    return true;
  });
}

export function computeFacetCounts(
  collections: Collection[],
  currentFacets: FacetState
): FacetCounts {
  // Count how many collections match each facet value
  // Used to show (12) next to filter options
  // ...
}
```

### D3: Index Page Component

**File:** `components/collections/CollectionIndex.tsx`

```tsx
export function CollectionIndex() {
  const [facets, setFacets] = useState<FacetState>(DEFAULT_FACET_STATE);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'updated' | 'confidence' | 'items'>('updated');

  const allCollections = useCollections();
  const filteredCollections = useMemo(
    () => filterCollections(allCollections, facets, searchQuery),
    [allCollections, facets, searchQuery]
  );
  const sortedCollections = useMemo(
    () => sortCollections(filteredCollections, sortBy),
    [filteredCollections, sortBy]
  );

  return (
    <div className="collection-index">
      {/* Header */}
      <header className="index-header">
        <h1>Knowledge Index</h1>
        <Button onClick={openCreateModal}>+ New Collection</Button>
      </header>

      {/* Quick Stats */}
      <QuickStats collections={allCollections} />

      {/* Search + Sort */}
      <div className="index-controls">
        <SearchInput
          value={searchQuery}
          onChange={setSearchQuery}
          placeholder="Search collections..."
        />
        <SortSelect value={sortBy} onChange={setSortBy} />
      </div>

      {/* Main Content */}
      <div className="index-layout">
        {/* Facet Sidebar */}
        <aside className="facet-sidebar">
          <FacetPanel
            facets={DEFAULT_FACETS}
            state={facets}
            counts={computeFacetCounts(allCollections, facets)}
            onChange={setFacets}
            onReset={() => setFacets(DEFAULT_FACET_STATE)}
          />
        </aside>

        {/* Collection Grid */}
        <main className="collection-grid">
          {sortedCollections.length === 0 ? (
            <EmptyState
              title="No collections found"
              action={<Button onClick={resetFilters}>Clear Filters</Button>}
            />
          ) : (
            <CollectionGrid collections={sortedCollections} />
          )}
        </main>
      </div>

      {/* Activity Feed */}
      <ActivityFeed collections={allCollections} />
    </div>
  );
}
```

### D4: Quick Stats Dashboard

**File:** `components/collections/QuickStats.tsx`

```tsx
export function QuickStats({ collections }: Props) {
  const stats = useMemo(() => ({
    total: collections.length,
    totalItems: collections.reduce((sum, c) => sum + c.items.length, 0),
    avgConfidence: collections.reduce((sum, c) => sum + c.confidence.overall, 0) / collections.length,
    needsAttention: collections.filter(c => c.confidence.overall < 0.5).length,
    updatedToday: collections.filter(c => isToday(new Date(c.updatedAt))).length,
  }), [collections]);

  return (
    <div className="quick-stats">
      <StatCard value={stats.total} label="Collections" />
      <StatCard value={stats.totalItems} label="Items" />
      <StatCard value={`${(stats.avgConfidence * 100).toFixed(0)}%`} label="Avg Confidence" />
      <StatCard value={stats.needsAttention} label="Needs Attention" color="orange" />
      <StatCard value={stats.updatedToday} label="Updated Today" color="green" />
    </div>
  );
}
```

### D5: Activity Feed

**File:** `components/collections/ActivityFeed.tsx`

```tsx
export function ActivityFeed({ collections, limit = 10 }: Props) {
  const activities = useMemo(() => {
    const events: ActivityEvent[] = [];

    collections.forEach(c => {
      // Collection updates
      events.push({
        type: 'collection_updated',
        collectionId: c.id,
        collectionTitle: c.title,
        timestamp: c.updatedAt,
      });

      // Recent item additions
      c.items
        .filter(i => isThisWeek(new Date(i.createdAt)))
        .forEach(item => {
          events.push({
            type: 'item_added',
            collectionId: c.id,
            collectionTitle: c.title,
            itemTitle: item.data.name || item.data.title,
            timestamp: item.createdAt,
          });
        });

      // Assumptions verified
      c.items.forEach(item => {
        item.assumptions
          .filter(a => a.status === 'verified' && isThisWeek(new Date(a.challengeDate!)))
          .forEach(assumption => {
            events.push({
              type: 'assumption_verified',
              collectionId: c.id,
              collectionTitle: c.title,
              assumption: assumption.field,
              timestamp: assumption.challengeDate!,
            });
          });
      });
    });

    return events
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      .slice(0, limit);
  }, [collections, limit]);

  return (
    <div className="activity-feed">
      <h3>Recent Activity</h3>
      <ul>
        {activities.map(activity => (
          <ActivityItem key={activity.timestamp} activity={activity} />
        ))}
      </ul>
    </div>
  );
}
```

---

## UI Mockup

```
┌─────────────────────────────────────────────────────────┐
│ KNOWLEDGE INDEX                        [+ New Collection]│
├─────────────────────────────────────────────────────────┤
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │
│ │   12   │ │  156   │ │  78%   │ │   3    │ │   5    │ │
│ │Collect.│ │ Items  │ │Confid. │ │Needs ⚠️│ │Today ✓ │ │
│ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ │
├─────────────────────────────────────────────────────────┤
│ Search: [________________________] Sort: [Updated ▼]    │
├───────────────┬─────────────────────────────────────────┤
│ FILTERS       │                                         │
│               │ ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│ Domain        │ │Top LLMs │ │Music    │ │AI Papers│    │
│ ☑ AI (5)     │ │📊 Rank  │ │🔗 Eco   │ │📊 Rank  │    │
│ ☐ Music (3)  │ │85% ████ │ │62% ███  │ │78% ████ │    │
│ ☐ Finance (2)│ └─────────┘ └─────────┘ └─────────┘    │
│               │                                         │
│ Type          │ ┌─────────┐ ┌─────────┐               │
│ ☑ Rankings   │ │Networks │ │Timelines│               │
│ ☑ Ecosystems │ │👥 Net   │ │📅 Time  │               │
│ ☐ Timelines  │ │91% ████ │ │45% ██   │               │
│               │ └─────────┘ └─────────┘               │
│ Confidence    │                                         │
│ ○ All         │                                         │
│ ● Verified    │ RECENT ACTIVITY                        │
│ ○ Partial     │ • "Claude 4" added to Top LLMs (2h)    │
│ ○ Low         │ • Music Stack confidence → 62% (1d)    │
│               │ • Assumption verified: "DAW price" (2d)│
│ [Clear All]   │                                         │
└───────────────┴─────────────────────────────────────────┘
```

---

## Acceptance Criteria

- [ ] Facet filters work correctly (single and multi-select)
- [ ] Counts update as filters change
- [ ] Search works across title, tags, and items
- [ ] Sort by updated/confidence/items works
- [ ] Quick stats show accurate numbers
- [ ] Activity feed shows recent events
- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] URL reflects filter state (shareable)
- [ ] Mobile-responsive layout

---

## Milestone: MVP Complete

This work order completes the MVP. The Collections feature now includes:
- ✅ Data model & storage
- ✅ Basic CRUD UI
- ✅ Widget system
- ✅ Evolution engine
- ✅ Inter-collection links
- ✅ Presentation templates
- ✅ Faceted index

**Ready for v1.0 polish and user testing.**
