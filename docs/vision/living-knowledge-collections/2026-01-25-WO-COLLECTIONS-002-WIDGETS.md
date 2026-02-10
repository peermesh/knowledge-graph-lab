# WO-COLLECTIONS-002: Widget System - Visual Components

**Phase:** MVP
**Priority:** P1 - Core Feature
**Estimated Effort:** 4-5 days
**Dependencies:** WO-COLLECTIONS-001 (Basic UI)
**Blocks:** Presentation templates

---

## Objective

Build the modular widget library that renders collection data as visual infographics. Each widget is reusable, composable, and data-bound.

---

## Scope

### In Scope
- Widget base architecture
- 6 core widget types
- Data binding system
- Widget composition
- Basic interactivity (hover, click)

### Out of Scope
- Drag-and-drop customization
- Widget marketplace
- Advanced animations

---

## Deliverables

### D1: Widget Architecture

**File:** `components/widgets/WidgetBase.tsx`

```typescript
interface WidgetProps<T = any> {
  data: T;
  binding: DataBinding;
  style?: WidgetStyle;
  onInteract?: (action: InteractionAction) => void;
  children?: React.ReactNode;
}

interface DataBinding {
  source: 'collection' | 'item' | 'computed';
  fields: Record<string, string>;  // widgetProp → dataField
  transforms?: Record<string, (value: any) => any>;
}

// Base widget with common functionality
export function WidgetBase<T>({ data, binding, style, children }: WidgetProps<T>) {
  const boundData = useMemo(() => bindData(data, binding), [data, binding]);
  return (
    <div className={cn('widget', style?.className)} style={style?.inline}>
      {children}
    </div>
  );
}
```

### D2: Core Widgets

#### Widget: RankingCard
```tsx
// For: ranking collections
// Shows: rank badge, title, score bar, trend arrow, citations
<RankingCard
  rank={1}
  title="Claude 4 Opus"
  subtitle="Anthropic"
  score={94.2}
  maxScore={100}
  trend="up"
  citations={2}
  confidence={0.92}
/>
```

#### Widget: StatBlock
```tsx
// For: key metrics highlight
// Shows: large number, label, trend, sparkline
<StatBlock
  value={94.2}
  label="Benchmark Score"
  trend={+2.1}
  sparkline={[88, 90, 92, 94]}
/>
```

#### Widget: ComparisonRow
```tsx
// For: comparison collections
// Shows: item name, dimension bars, verdict badge
<ComparisonRow
  name="Claude 4"
  dimensions={['Speed', 'Quality', 'Cost']}
  scores={[85, 94, 70]}
  verdict="Best for Quality"
/>
```

#### Widget: EcosystemNode
```tsx
// For: ecosystem collections
// Shows: icon, name, category, integration count
<EcosystemNode
  icon="🎹"
  name="Ableton Live"
  category="DAW"
  integrations={12}
  onClick={() => drillDown('ableton')}
/>
```

#### Widget: TimelineEvent
```tsx
// For: timeline collections
// Shows: date, title, description, impact badge
<TimelineEvent
  date="2023-03-14"
  title="GPT-4 Released"
  description="OpenAI launches multimodal LLM"
  impact="high"
/>
```

#### Widget: CitationStack
```tsx
// For: showing sources on any item
// Shows: stacked source cards with status
<CitationStack
  citations={[
    { url: '...', title: 'Anthropic Blog', alive: true },
    { url: '...', title: 'ArXiv Paper', alive: true },
  ]}
  onVerify={(id) => checkCitation(id)}
/>
```

### D3: Widget Composition

```tsx
// Combine widgets into collection views
<CollectionView collection={collection}>
  <WidgetRow>
    <StatBlock value={collection.items.length} label="Items" />
    <StatBlock value={collection.confidence.overall * 100} label="Confidence" />
    <StatBlock value={collection.hydrationLevel} label="Hydration" />
  </WidgetRow>

  <WidgetGrid columns={2}>
    {collection.items.map(item => (
      <RankingCard key={item.id} {...bindToRanking(item)} />
    ))}
  </WidgetGrid>
</CollectionView>
```

### D4: Widget Registry

**File:** `services/widgetRegistry.ts`

```typescript
const WIDGET_REGISTRY: Record<string, WidgetDefinition> = {
  'ranking-card': {
    component: RankingCard,
    applicableTypes: ['ranking'],
    requiredFields: ['rank', 'name'],
    optionalFields: ['score', 'trend', 'citations'],
  },
  'stat-block': {
    component: StatBlock,
    applicableTypes: ['*'],  // Universal
    requiredFields: ['value', 'label'],
  },
  // ... more widgets
};

export function getWidgetForType(type: CollectionType): WidgetDefinition[] {
  return Object.values(WIDGET_REGISTRY).filter(
    w => w.applicableTypes.includes(type) || w.applicableTypes.includes('*')
  );
}
```

---

## Visual Reference

```
┌─────────────────────────────────────────────────────────┐
│ RANKING CARD                                             │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ ┌───┐                                               │ │
│ │ │ 1 │  Claude 4 Opus                    ↑ +2.1     │ │
│ │ └───┘  Anthropic                                    │ │
│ │        ████████████████████░░░░ 94.2/100           │ │
│ │        🔗 2 citations  │  ✓ Verified               │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ STAT BLOCK                                               │
│ ┌─────────────────┐ ┌─────────────────┐                 │
│ │      94.2       │ │       10        │                 │
│ │  Benchmark ↑2.1 │ │   Items  +3     │                 │
│ │  ▁▂▃▅▆▇        │ │  ▂▃▃▄▅▆▇       │                 │
│ └─────────────────┘ └─────────────────┘                 │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ECOSYSTEM NODE                                           │
│        ┌─────┐                                          │
│        │ 🎹  │                                          │
│        └─────┘                                          │
│      Ableton Live                                       │
│         DAW                                             │
│    ──○──○──○──                                         │
│    12 integrations                                      │
└─────────────────────────────────────────────────────────┘
```

---

## Acceptance Criteria

- [ ] All 6 core widgets render correctly
- [ ] Data binding works with collection data
- [ ] Widgets are responsive
- [ ] Hover states provide additional info
- [ ] Click actions trigger callbacks
- [ ] Widgets compose in grids/rows
- [ ] Widget registry returns correct widgets for type

---

## Next Work Order

→ **WO-COLLECTIONS-003: Evolution Engine - Self-Improvement System**
