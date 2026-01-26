# WO-COLLECTIONS-004: Inter-Collection Links - Knowledge Network

**Phase:** MVP → v1.0
**Priority:** P1 - Core Feature
**Estimated Effort:** 3-4 days
**Dependencies:** WO-COLLECTIONS-001 (Basic UI)
**Blocks:** Faceted index, link tree navigation

---

## Objective

Enable collections to link to each other, forming a navigable knowledge network. Collections become nodes in a larger graph with typed relationships.

---

## Scope

### In Scope
- Collection connection types (contains, references, extends, etc.)
- Link creation UI
- Link visualization
- Bidirectional navigation
- Link tree rendering

### Out of Scope
- Auto-discovered links (future AI feature)
- Link strength/confidence scoring
- Graph-based querying

---

## Deliverables

### D1: Connection Type Definitions

**File:** `types/collectionLinks.ts`

```typescript
export type CollectionConnectionType =
  | 'contains'      // Parent-child hierarchy
  | 'references'    // Citation/mention
  | 'contradicts'   // Conflicting data
  | 'extends'       // Adds depth/detail
  | 'supersedes'    // Newer version
  | 'relates_to';   // Generic connection

export interface CollectionConnection {
  id: string;
  sourceCollectionId: string;
  targetCollectionId: string;
  connectionType: CollectionConnectionType;
  bidirectional: boolean;
  label?: string;          // Custom label
  strength: number;        // 0-1 relevance
  createdAt: string;
  createdBy: 'USER' | 'AI';
  metadata?: {
    reason?: string;
    sourceItemId?: string;  // If link is from specific item
  };
}

// Inverse relationship display
export const CONNECTION_INVERSE: Record<CollectionConnectionType, string> = {
  contains: 'contained by',
  references: 'referenced by',
  contradicts: 'contradicts',  // Symmetric
  extends: 'extended by',
  supersedes: 'superseded by',
  relates_to: 'related to',    // Symmetric
};
```

### D2: Link Storage Service

**File:** `services/collectionLinkStorage.ts`

```typescript
export const linkStorage = {
  getAll: (): CollectionConnection[] => { ... },

  getByCollection: (collectionId: string): {
    outgoing: CollectionConnection[];
    incoming: CollectionConnection[];
  } => {
    const all = linkStorage.getAll();
    return {
      outgoing: all.filter(l => l.sourceCollectionId === collectionId),
      incoming: all.filter(l => l.targetCollectionId === collectionId),
    };
  },

  create: (link: Omit<CollectionConnection, 'id' | 'createdAt'>) => { ... },
  delete: (linkId: string) => { ... },

  // Get full link tree from a root
  getTree: (rootId: string, depth = 3): CollectionTreeNode => {
    const visited = new Set<string>();
    return buildTree(rootId, depth, visited);
  },
};
```

### D3: Link Creation UI

**File:** `components/collections/LinkCreator.tsx`

```tsx
// Modal for creating collection links
<LinkCreator sourceCollection={collection}>
  <CollectionSearch
    onSelect={setTargetCollection}
    exclude={[collection.id]}
  />
  <ConnectionTypeSelect
    value={connectionType}
    onChange={setConnectionType}
  />
  <Input
    label="Label (optional)"
    value={label}
    onChange={setLabel}
  />
  <Toggle
    label="Bidirectional"
    checked={bidirectional}
    onChange={setBidirectional}
  />
  <Button onClick={createLink}>Create Link</Button>
</LinkCreator>
```

### D4: Links Section in Collection Detail

**File:** `components/collections/CollectionLinks.tsx`

```tsx
// Shows incoming and outgoing links
<CollectionLinks collectionId={id}>
  <Section title="Contains">
    {outgoing.filter(l => l.connectionType === 'contains').map(link => (
      <LinkCard link={link} direction="outgoing" />
    ))}
  </Section>

  <Section title="References">
    {outgoing.filter(l => l.connectionType === 'references').map(link => (
      <LinkCard link={link} direction="outgoing" />
    ))}
  </Section>

  <Section title="Referenced By">
    {incoming.filter(l => l.connectionType === 'references').map(link => (
      <LinkCard link={link} direction="incoming" />
    ))}
  </Section>

  <AddLinkButton onClick={openLinkCreator} />
</CollectionLinks>
```

### D5: Link Tree Navigation

**File:** `components/collections/LinkTree.tsx`

```tsx
interface LinkTreeProps {
  rootCollectionId: string;
  maxDepth?: number;
  expandedPaths?: string[];
}

export function LinkTree({ rootCollectionId, maxDepth = 3 }: LinkTreeProps) {
  const tree = useMemo(
    () => linkStorage.getTree(rootCollectionId, maxDepth),
    [rootCollectionId, maxDepth]
  );

  return (
    <TreeView>
      <TreeNode node={tree} depth={0}>
        {({ node, isExpanded, toggle }) => (
          <div className="tree-node">
            <ExpandButton onClick={toggle} expanded={isExpanded} />
            <CollectionMiniCard collection={node.collection} />
            <ConnectionBadge type={node.connectionType} />

            {isExpanded && node.children.map(child => (
              <TreeNode key={child.collection.id} node={child} depth={depth + 1} />
            ))}
          </div>
        )}
      </TreeNode>
    </TreeView>
  );
}
```

### D6: Connection Badges & Indicators

**File:** `components/collections/ConnectionBadge.tsx`

```tsx
const CONNECTION_STYLES: Record<CollectionConnectionType, BadgeStyle> = {
  contains: { color: 'blue', icon: '📦' },
  references: { color: 'green', icon: '🔗' },
  contradicts: { color: 'red', icon: '⚡' },
  extends: { color: 'purple', icon: '➕' },
  supersedes: { color: 'orange', icon: '🔄' },
  relates_to: { color: 'gray', icon: '↔️' },
};

export function ConnectionBadge({ type, direction }: Props) {
  const style = CONNECTION_STYLES[type];
  const label = direction === 'incoming'
    ? CONNECTION_INVERSE[type]
    : type.replace('_', ' ');

  return (
    <Badge color={style.color}>
      {style.icon} {label}
    </Badge>
  );
}
```

---

## UI Mockup

```
Collection Detail - Links Section:
┌─────────────────────────────────────────────────────────┐
│ CONNECTIONS                              [+ Add Link]    │
├─────────────────────────────────────────────────────────┤
│ 📦 Contains (3)                                          │
│ ├── Top LLMs → "Claude Models" collection               │
│ ├── Top LLMs → "OpenAI Models" collection               │
│ └── Top LLMs → "Open Source LLMs" collection            │
│                                                          │
│ 🔗 References (2)                                        │
│ ├── Top LLMs → "Transformer Architecture" collection    │
│ └── Top LLMs → "AI Safety Research" collection          │
│                                                          │
│ 🔗 Referenced By (1)                                     │
│ └── "AI Research Landscape" → Top LLMs                  │
└─────────────────────────────────────────────────────────┘

Link Tree View:
┌─────────────────────────────────────────────────────────┐
│ AI Research Landscape                                    │
│ ├─📦─ LLMs (contains)                                   │
│ │     ├─📦─ Top LLMs (contains)                         │
│ │     │     ├─🔗─ Transformer Architecture (references) │
│ │     │     └─🔗─ AI Safety Research (references)       │
│ │     ├─📦─ LLM Benchmarks (contains)                   │
│ │     └─📦─ LLM Safety (contains)                       │
│ ├─📦─ Computer Vision (contains)                        │
│ └─📦─ Robotics (contains)                               │
└─────────────────────────────────────────────────────────┘
```

---

## Acceptance Criteria

- [ ] Can create links between collections
- [ ] All connection types work correctly
- [ ] Bidirectional links show on both ends
- [ ] Link tree renders with expandable nodes
- [ ] Navigation works (click to open linked collection)
- [ ] Connection badges show correct type and direction
- [ ] No circular reference issues in tree rendering

---

## Next Work Order

→ **WO-COLLECTIONS-005: Presentation Templates - Visual Presets**
