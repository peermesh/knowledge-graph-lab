# WO-COLLECTIONS-003: Evolution Engine - Self-Improvement System

**Phase:** MVP → v1.0
**Priority:** P1 - Core Feature
**Estimated Effort:** 5-6 days
**Dependencies:** WO-COLLECTIONS-000 (Foundation), WO-COLLECTIONS-001 (Basic UI)
**Blocks:** Auto-hydration, assumption challenging

---

## Objective

Build the Evolution Engine that makes collections self-improving over time through hydration, citation verification, assumption challenging, and staleness detection.

---

## Scope

### In Scope
- Hydration worker (fill missing fields via AI)
- Citation verification (link checking)
- Assumption challenging (find counter-evidence)
- Staleness detection and flagging
- Evolution task queue
- Progress tracking UI

### Out of Scope
- Real-time streaming updates
- Distributed workers
- User notification system

---

## Deliverables

### D1: Evolution Task Queue

**File:** `services/evolutionQueue.ts`

```typescript
interface EvolutionTask {
  id: string;
  type: 'hydrate' | 'verify-citation' | 'challenge-assumption' | 'check-staleness';
  collectionId: string;
  itemId?: string;
  field?: string;
  priority: number;
  status: 'pending' | 'running' | 'completed' | 'failed';
  createdAt: string;
  completedAt?: string;
  result?: any;
  error?: string;
}

export const evolutionQueue = {
  add: (task: Omit<EvolutionTask, 'id' | 'status' | 'createdAt'>) => { ... },
  getNext: (): EvolutionTask | null => { ... },
  complete: (taskId: string, result: any) => { ... },
  fail: (taskId: string, error: string) => { ... },
  getPending: (collectionId?: string): EvolutionTask[] => { ... },
};
```

### D2: Hydration Worker

**File:** `services/workers/hydrationWorker.ts`

```typescript
export async function hydrateField(
  collection: Collection,
  item: CollectionItem,
  field: SchemaField
): Promise<HydrationResult> {
  // Build context from existing data
  const context = {
    collectionTitle: collection.title,
    collectionType: collection.type,
    existingData: item.data,
    targetField: field.name,
    fieldDescription: field.description,
  };

  // Ask AI to research the missing field
  const prompt = buildHydrationPrompt(context);
  const response = await gemini.generateContent({
    model: 'gemini-2.5-flash',
    contents: prompt,
    config: {
      responseMimeType: 'application/json',
      responseSchema: HydrationResultSchema,
    }
  });

  const result = JSON.parse(response.text);

  // If confident, update the item
  if (result.confidence > 0.7) {
    return {
      success: true,
      value: result.value,
      confidence: result.confidence,
      citation: result.source,
    };
  } else {
    // Low confidence → mark as assumption
    return {
      success: true,
      value: result.value,
      confidence: result.confidence,
      assumption: {
        reason: result.reasoning,
        needsVerification: true,
      },
    };
  }
}

const HydrationResultSchema = z.object({
  value: z.any(),
  confidence: z.number(),
  source: z.object({
    url: z.string().optional(),
    title: z.string(),
    excerpt: z.string().optional(),
  }).optional(),
  reasoning: z.string(),
});
```

### D3: Citation Verification Worker

**File:** `services/workers/citationWorker.ts`

```typescript
export async function verifyCitation(citation: Citation): Promise<VerificationResult> {
  // Check if URL is still alive
  const linkCheck = await checkLinkAlive(citation.url);

  if (!linkCheck.alive) {
    return {
      status: 'dead',
      lastWorkingDate: citation.lastChecked,
      archiveUrl: await findArchiveVersion(citation.url),
    };
  }

  // Fetch current content and compare to stored excerpt
  const currentContent = await fetchPageContent(citation.url);
  const excerptStillExists = currentContent.includes(citation.excerpt || '');

  if (!excerptStillExists) {
    return {
      status: 'changed',
      previousExcerpt: citation.excerpt,
      currentRelevantText: await findRelevantExcerpt(currentContent, citation.title),
    };
  }

  return {
    status: 'valid',
    lastChecked: new Date().toISOString(),
  };
}
```

### D4: Assumption Challenger

**File:** `services/workers/challengeWorker.ts`

```typescript
export async function challengeAssumption(
  collection: Collection,
  item: CollectionItem,
  assumption: Assumption
): Promise<ChallengeResult> {
  const prompt = `
You are a fact-checker. Challenge this assumption by finding evidence for or against it.

ASSUMPTION: "${assumption.reason}"
VALUE: ${JSON.stringify(assumption.value)}
CONTEXT: Collection "${collection.title}", Item "${item.data.name || item.id}"

Search for:
1. Contradicting sources
2. Updated information
3. Expert opinions

OUTPUT:
{
  "verdict": "confirmed" | "refuted" | "uncertain",
  "evidence": [{ "url": "...", "excerpt": "...", "supports": true/false }],
  "confidence": 0.0-1.0,
  "recommendation": "keep" | "update" | "remove"
}
`;

  const response = await gemini.generateContent({
    model: 'gemini-2.5-flash',
    systemInstruction: 'You are a rigorous fact-checker. Be skeptical.',
    contents: prompt,
    tools: [{ googleSearch: {} }],  // Enable grounding
  });

  return JSON.parse(response.text);
}
```

### D5: Staleness Detector

**File:** `services/workers/stalenessWorker.ts`

```typescript
const STALENESS_CONFIG = {
  ranking: { maxAgeDays: 30, refreshPriority: 'high' },
  comparison: { maxAgeDays: 60, refreshPriority: 'medium' },
  ecosystem: { maxAgeDays: 90, refreshPriority: 'medium' },
  timeline: { maxAgeDays: 365, refreshPriority: 'low' },
};

export function detectStaleItems(collection: Collection): StaleItem[] {
  const config = STALENESS_CONFIG[collection.type] || { maxAgeDays: 60 };
  const cutoffDate = subDays(new Date(), config.maxAgeDays);

  return collection.items
    .filter(item => {
      const lastUpdate = new Date(item.updatedAt);
      return lastUpdate < cutoffDate;
    })
    .map(item => ({
      itemId: item.id,
      lastUpdated: item.updatedAt,
      daysSinceUpdate: differenceInDays(new Date(), new Date(item.updatedAt)),
      priority: config.refreshPriority,
    }));
}
```

### D6: Evolution Engine Orchestrator

**File:** `services/evolutionEngine.ts`

```typescript
export class EvolutionEngine {
  private running = false;
  private intervalId: NodeJS.Timeout | null = null;

  start(intervalMs = 60000) {
    if (this.running) return;
    this.running = true;

    this.intervalId = setInterval(() => this.tick(), intervalMs);
    this.tick();  // Run immediately
  }

  stop() {
    this.running = false;
    if (this.intervalId) clearInterval(this.intervalId);
  }

  private async tick() {
    const task = evolutionQueue.getNext();
    if (!task) return;

    try {
      evolutionQueue.updateStatus(task.id, 'running');

      let result;
      switch (task.type) {
        case 'hydrate':
          result = await this.runHydration(task);
          break;
        case 'verify-citation':
          result = await this.runCitationVerify(task);
          break;
        case 'challenge-assumption':
          result = await this.runChallenge(task);
          break;
        case 'check-staleness':
          result = await this.runStalenessCheck(task);
          break;
      }

      evolutionQueue.complete(task.id, result);
      this.updateCollectionConfidence(task.collectionId);

    } catch (error) {
      evolutionQueue.fail(task.id, error.message);
    }
  }

  // Batch operations
  async evolveCollection(collectionId: string) {
    const collection = collectionStorage.getById(collectionId);
    if (!collection) return;

    // Queue hydration for empty fields
    for (const item of collection.items) {
      const schema = getSchema(collection.schemaId);
      for (const field of schema.fields) {
        if (item.data[field.name] === undefined) {
          evolutionQueue.add({
            type: 'hydrate',
            collectionId,
            itemId: item.id,
            field: field.name,
            priority: field.citationRequired ? 1 : 2,
          });
        }
      }
    }

    // Queue citation verification
    for (const item of collection.items) {
      for (const citation of item.citations) {
        evolutionQueue.add({
          type: 'verify-citation',
          collectionId,
          itemId: item.id,
          citationId: citation.id,
          priority: 2,
        });
      }
    }

    // Queue assumption challenges
    for (const item of collection.items) {
      for (const assumption of item.assumptions.filter(a => a.status === 'pending')) {
        evolutionQueue.add({
          type: 'challenge-assumption',
          collectionId,
          itemId: item.id,
          assumptionId: assumption.id,
          priority: 1,
        });
      }
    }
  }
}
```

### D7: Evolution Progress UI

**File:** `components/collections/EvolutionStatus.tsx`

```tsx
// Shows:
// - Current evolution tasks running
// - Queue depth
// - Recent completions
// - Confidence trend over time
// - "Evolve Now" button

<EvolutionStatus collectionId={id}>
  <ProgressRing value={75} label="Evolution Progress" />
  <TaskList tasks={pendingTasks} />
  <Button onClick={evolveNow}>Evolve Collection</Button>
</EvolutionStatus>
```

---

## Acceptance Criteria

- [ ] Hydration fills missing fields with citations
- [ ] Citations are verified (link alive, content unchanged)
- [ ] Assumptions get challenged with counter-evidence search
- [ ] Stale items are flagged based on type-specific thresholds
- [ ] Evolution queue processes tasks in priority order
- [ ] Collection confidence recalculates after evolution
- [ ] UI shows evolution progress and results
- [ ] User can trigger manual evolution

---

## Next Work Order

→ **WO-COLLECTIONS-004: Inter-Collection Links - Knowledge Network**
