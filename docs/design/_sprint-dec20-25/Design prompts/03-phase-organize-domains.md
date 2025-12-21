# Phase 3: Organize Mode - Domain Hierarchy

## Objective

Build the Organize mode interface for managing research domains. This is a hierarchical tree structure where users create, nest, and manage their research interests.

## What to Build

### 1. Tree Components

**DomainTree.tsx**
The main tree view container.

Props:
```typescript
interface DomainTreeProps {
  domains: DomainNode[];
  onAddDomain: (parentId: string | null) => void;
  onDeleteDomain: (id: string) => void;
  onRenameDomain: (id: string, newName: string) => void;
  onMoveDomain: (id: string, newParentId: string | null) => void;
  onPromoteDomain: (id: string) => void;
  selectedId: string | null;
  onSelect: (id: string) => void;
}
```

**DomainNode.tsx**
A single node in the tree.

Props:
```typescript
interface DomainNodeProps {
  node: {
    id: string;
    name: string;
    children: DomainNode[];
    findingCount: number;
  };
  depth: number;
  isExpanded: boolean;
  isSelected: boolean;
  onToggleExpand: () => void;
  onSelect: () => void;
  onContextMenu: (e: React.MouseEvent) => void;
}
```

Visual design:
- Indentation shows hierarchy (16-24px per level)
- Expand/collapse chevron for nodes with children
- Node name as primary text
- Finding count as badge (muted)
- Selected state with background highlight
- Hover state on desktop

**DomainContextMenu.tsx**
Context menu for domain actions.

Options:
- Rename
- Add sub-domain
- Move to... (opens move dialog)
- Promote to top level (if nested)
- Delete (with confirmation)

Trigger: right-click on desktop, long-press on mobile

**AddDomainInput.tsx**
Inline input for adding new domains.
- Appears at bottom of tree or under a parent node
- Text input with enter to confirm, escape to cancel
- Auto-focuses when shown

**MoveDomainDialog.tsx**
Modal for moving a domain to a new parent.
- Shows simplified tree of possible destinations
- Excludes the domain being moved and its children
- Confirm/cancel buttons

### 2. State Management

Create a domains context or use local state:

```typescript
interface DomainsState {
  domains: DomainNode[];
  expandedIds: Set<string>;
  selectedId: string | null;
}
```

Operations needed:
- Add domain (at root or under parent)
- Delete domain (and all children)
- Rename domain
- Move domain to new parent
- Promote nested domain to top level
- Toggle expand/collapse
- Select domain

### 3. Mock Data

```typescript
// src/fixtures/domains.ts
export const mockDomains: DomainNode[] = [
  {
    id: 'd1',
    name: 'Electric Vehicles',
    findingCount: 24,
    children: [
      {
        id: 'd1-1',
        name: 'Battery Technology',
        findingCount: 12,
        children: [
          { id: 'd1-1-1', name: 'Solid State', findingCount: 3, children: [] },
          { id: 'd1-1-2', name: 'Recycling', findingCount: 5, children: [] },
        ]
      },
      {
        id: 'd1-2',
        name: 'Manufacturing',
        findingCount: 8,
        children: []
      }
    ]
  },
  {
    id: 'd2',
    name: 'AI Regulation',
    findingCount: 15,
    children: [
      { id: 'd2-1', name: 'EU Policy', findingCount: 7, children: [] },
      { id: 'd2-2', name: 'US Policy', findingCount: 4, children: [] },
    ]
  },
  // ... more
];
```

### 4. Organize Page Assembly

Update `OrganizePage.tsx`:
- Render DomainTree with mock data
- "Add Domain" button at top
- Selected domain shows detail panel on right (desktop) or below (mobile)
- Detail panel shows: domain name, finding count, sub-domains list, recent findings preview

### 5. Domain Detail Panel

**DomainDetail.tsx**
Shows when a domain is selected.

Content:
- Domain name (editable inline)
- Finding count
- List of direct sub-domains
- Preview of 3-5 recent findings in this domain
- "View all findings" link (just logs for now)

## Acceptance Criteria

- [ ] Tree renders with proper indentation
- [ ] Nodes expand/collapse correctly
- [ ] Selecting a node highlights it and shows detail
- [ ] Right-click/long-press shows context menu
- [ ] Can add new domain at root level
- [ ] Can add sub-domain under existing domain
- [ ] Can rename domain via context menu
- [ ] Can delete domain (with confirmation)
- [ ] Can move domain to new parent
- [ ] Can promote nested domain to top level
- [ ] Tree state persists during session
- [ ] Mobile layout works (single column, collapsible detail)

## Design Notes

- Tree should feel like a file browser, familiar and usable
- Keep context menus simple and fast
- Confirmation only needed for destructive actions
- Drag-and-drop is nice-to-have but not required
- Use consistent iconography (folder icons, chevrons)

## Do NOT Build Yet

- Real data persistence
- Drag-and-drop reordering
- Search within tree
- Bulk operations
- Stream configuration per domain
