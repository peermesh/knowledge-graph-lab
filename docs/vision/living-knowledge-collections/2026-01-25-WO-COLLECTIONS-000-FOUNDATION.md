# WO-COLLECTIONS-000: Foundation - Data Model & Core Types

**Phase:** 0 (Foundation)
**Priority:** P0 - Critical Path
**Estimated Effort:** 2-3 days
**Dependencies:** None
**Blocks:** All subsequent collection work orders

---

## Objective

Establish the foundational data model, TypeScript types, and storage layer for the Collections system. No UI - just the core data infrastructure.

---

## Scope

### In Scope
- Collection, CollectionItem, CollectionSchema TypeScript interfaces
- PredicateType extensions for collection connections
- LocalStorage persistence layer for collections
- Basic CRUD operations (create, read, update, delete)
- Schema validation utilities

### Out of Scope
- UI components (WO-001)
- Evolution engine (WO-003)
- Widget rendering (WO-002)
- Inter-collection connections (WO-004)

---

## Deliverables

### D1: Type Definitions

**File:** `types/collections.ts`

```typescript
// Core collection types
export type CollectionType =
  | 'ranking'
  | 'comparison'
  | 'ecosystem'
  | 'timeline'
  | 'network'
  | 'taxonomy'
  | 'custom';

export interface Collection {
  id: string;
  title: string;
  description?: string;
  type: CollectionType;
  schemaId: string;
  items: CollectionItem[];
  confidence: ConfidenceScore;
  hydrationLevel: number;  // 0-100
  createdAt: string;
  updatedAt: string;
  lastVerified?: string;
  metadata: CollectionMetadata;
}

export interface CollectionItem {
  id: string;
  collectionId: string;
  data: Record<string, any>;
  rank?: number;
  confidence: ConfidenceScore;
  citations: Citation[];
  assumptions: Assumption[];
  hydrationLevel: number;
  createdAt: string;
  updatedAt: string;
  lastVerified?: string;
}

export interface ConfidenceScore {
  overall: number;  // 0-1
  breakdown: {
    cited: number;
    verified: number;
    assumed: number;
    stale: number;
  };
}

export interface Citation {
  id: string;
  url: string;
  title: string;
  author?: string;
  publishedDate?: string;
  accessedDate: string;
  excerpt?: string;
  isAlive: boolean;
  lastChecked: string;
}

export interface Assumption {
  id: string;
  field: string;
  value: any;
  reason: string;
  confidence: number;
  status: 'pending' | 'verified' | 'refuted';
  challengeDate?: string;
}

export interface CollectionMetadata {
  creator: 'USER' | 'AI' | 'IMPORTED';
  domain?: string;
  tags: string[];
  version: number;
  isPublic: boolean;
}
```

### D2: Schema System

**File:** `types/collectionSchemas.ts`

```typescript
export interface CollectionSchema {
  id: string;
  name: string;
  type: CollectionType;
  fields: SchemaField[];
  requiredFields: string[];
  defaultPresentation?: string;
  isSystem: boolean;
}

export interface SchemaField {
  name: string;
  type: FieldType;
  label: string;
  description?: string;
  citationRequired: boolean;
  defaultValue?: any;
  validation?: ValidationRule[];
}

export type FieldType =
  | 'string'
  | 'number'
  | 'boolean'
  | 'date'
  | 'url'
  | 'entity'      // Reference to another item/collection
  | 'citation'
  | 'array'
  | 'object';

export interface ValidationRule {
  type: 'required' | 'min' | 'max' | 'pattern' | 'enum';
  value: any;
  message: string;
}
```

### D3: Built-in Schemas

**File:** `data/defaultSchemas.ts`

```typescript
export const DEFAULT_SCHEMAS: CollectionSchema[] = [
  {
    id: 'schema_ranking',
    name: 'Ranking List',
    type: 'ranking',
    fields: [
      { name: 'rank', type: 'number', label: 'Rank', citationRequired: false },
      { name: 'name', type: 'string', label: 'Name', citationRequired: true },
      { name: 'description', type: 'string', label: 'Description', citationRequired: false },
      { name: 'score', type: 'number', label: 'Score', citationRequired: true },
      { name: 'trend', type: 'string', label: 'Trend', citationRequired: false },
      { name: 'source', type: 'citation', label: 'Source', citationRequired: true },
    ],
    requiredFields: ['rank', 'name'],
    defaultPresentation: 'ranking-card',
    isSystem: true,
  },
  {
    id: 'schema_comparison',
    name: 'Comparison Matrix',
    type: 'comparison',
    fields: [
      { name: 'name', type: 'string', label: 'Item Name', citationRequired: false },
      { name: 'dimensions', type: 'array', label: 'Comparison Dimensions', citationRequired: false },
      { name: 'scores', type: 'object', label: 'Dimension Scores', citationRequired: true },
      { name: 'verdict', type: 'string', label: 'Verdict', citationRequired: false },
    ],
    requiredFields: ['name', 'dimensions'],
    defaultPresentation: 'comparison-matrix',
    isSystem: true,
  },
  {
    id: 'schema_ecosystem',
    name: 'Ecosystem Map',
    type: 'ecosystem',
    fields: [
      { name: 'name', type: 'string', label: 'Tool/Platform Name', citationRequired: false },
      { name: 'category', type: 'string', label: 'Category', citationRequired: false },
      { name: 'description', type: 'string', label: 'Description', citationRequired: false },
      { name: 'url', type: 'url', label: 'Website', citationRequired: false },
      { name: 'integrations', type: 'array', label: 'Integrates With', citationRequired: false },
      { name: 'pricing', type: 'string', label: 'Pricing', citationRequired: true },
    ],
    requiredFields: ['name', 'category'],
    defaultPresentation: 'ecosystem-node',
    isSystem: true,
  },
];
```

### D4: Storage Service

**File:** `services/collectionStorage.ts`

```typescript
const STORAGE_KEYS = {
  COLLECTIONS: 'kgl_collections',
  SCHEMAS: 'kgl_collection_schemas',
};

export const collectionStorage = {
  // Collections
  getAll: (): Collection[] => {
    const data = localStorage.getItem(STORAGE_KEYS.COLLECTIONS);
    return data ? JSON.parse(data) : [];
  },

  getById: (id: string): Collection | undefined => {
    return collectionStorage.getAll().find(c => c.id === id);
  },

  save: (collection: Collection): void => {
    const collections = collectionStorage.getAll();
    const index = collections.findIndex(c => c.id === collection.id);
    if (index >= 0) {
      collections[index] = { ...collection, updatedAt: new Date().toISOString() };
    } else {
      collections.push(collection);
    }
    localStorage.setItem(STORAGE_KEYS.COLLECTIONS, JSON.stringify(collections));
  },

  delete: (id: string): void => {
    const collections = collectionStorage.getAll().filter(c => c.id !== id);
    localStorage.setItem(STORAGE_KEYS.COLLECTIONS, JSON.stringify(collections));
  },

  // Items within collection
  addItem: (collectionId: string, item: CollectionItem): void => {
    const collection = collectionStorage.getById(collectionId);
    if (collection) {
      collection.items.push(item);
      recalculateConfidence(collection);
      collectionStorage.save(collection);
    }
  },

  updateItem: (collectionId: string, itemId: string, updates: Partial<CollectionItem>): void => {
    const collection = collectionStorage.getById(collectionId);
    if (collection) {
      const itemIndex = collection.items.findIndex(i => i.id === itemId);
      if (itemIndex >= 0) {
        collection.items[itemIndex] = { ...collection.items[itemIndex], ...updates };
        recalculateConfidence(collection);
        collectionStorage.save(collection);
      }
    }
  },
};

function recalculateConfidence(collection: Collection): void {
  const items = collection.items;
  if (items.length === 0) {
    collection.confidence = { overall: 0, breakdown: { cited: 0, verified: 0, assumed: 0, stale: 0 } };
    return;
  }

  const cited = items.filter(i => i.citations.length > 0).length / items.length;
  const verified = items.filter(i => i.lastVerified).length / items.length;
  const assumed = items.filter(i => i.assumptions.length > 0).length / items.length;
  const stale = items.filter(i => isStale(i.lastVerified)).length / items.length;

  collection.confidence = {
    overall: (cited * 0.4 + verified * 0.4 + (1 - assumed) * 0.1 + (1 - stale) * 0.1),
    breakdown: { cited, verified, assumed, stale }
  };
}
```

### D5: Validation Utilities

**File:** `utils/collectionValidation.ts`

```typescript
export function validateItem(item: CollectionItem, schema: CollectionSchema): ValidationResult {
  const errors: ValidationError[] = [];

  // Check required fields
  for (const fieldName of schema.requiredFields) {
    if (!item.data[fieldName]) {
      errors.push({ field: fieldName, message: `${fieldName} is required` });
    }
  }

  // Check field types and validations
  for (const field of schema.fields) {
    const value = item.data[field.name];
    if (value !== undefined) {
      const typeError = validateFieldType(value, field.type);
      if (typeError) errors.push({ field: field.name, message: typeError });

      for (const rule of field.validation || []) {
        const ruleError = validateRule(value, rule);
        if (ruleError) errors.push({ field: field.name, message: ruleError });
      }
    }
  }

  return { valid: errors.length === 0, errors };
}

export function calculateHydrationLevel(item: CollectionItem, schema: CollectionSchema): number {
  const totalFields = schema.fields.length;
  const filledFields = schema.fields.filter(f => item.data[f.name] !== undefined).length;
  return Math.round((filledFields / totalFields) * 100);
}
```

---

## Acceptance Criteria

- [ ] All TypeScript types compile without errors
- [ ] Default schemas load correctly
- [ ] CRUD operations work via collectionStorage
- [ ] Confidence score recalculates on item changes
- [ ] Hydration level calculates correctly
- [ ] Validation catches missing required fields
- [ ] No UI dependencies - pure data layer

---

## Testing

```typescript
// Manual test script
const testCollection: Collection = {
  id: 'test_1',
  title: 'Top 5 LLMs',
  type: 'ranking',
  schemaId: 'schema_ranking',
  items: [],
  confidence: { overall: 0, breakdown: { cited: 0, verified: 0, assumed: 0, stale: 0 } },
  hydrationLevel: 0,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  metadata: { creator: 'USER', tags: ['AI', 'LLM'], version: 1, isPublic: false }
};

collectionStorage.save(testCollection);
console.log(collectionStorage.getById('test_1'));  // Should return collection
```

---

## Next Work Order

→ **WO-COLLECTIONS-001: Basic UI - Collection List & Detail Views**
