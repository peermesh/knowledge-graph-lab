# Knowledge Graph Lab V2 - Build Plan

## Recommendation: Fresh Build

The v1 prototype is fundamentally different from what we need. Updating it would require:
- Adding 2 new modes (Explore, Settings as full mode)
- Completely rewriting all components to be entity-aware
- Adding graph visualization infrastructure
- Restructuring all data types and fixtures

A fresh build with the complete spec will produce a more coherent result.

## Build Strategy

### Option A: Single-Prompt Ambitious Build
Feed the complete specification to an AI agent with good context handling (Claude, GPT-4) and let it build the full application.

**Pros:**
- Coherent architecture from the start
- Agent understands the full vision
- No context loss between phases

**Cons:**
- May produce incomplete implementations
- Hard to course-correct mid-build
- Agent might simplify complex features

### Option B: Phased Build with Context Preservation
Break into 4-5 phases, but always include the full spec as context.

**Recommended Phases:**

**Phase 1: Foundation + Explore Mode**
- App shell with 5-mode navigation
- Knowledge graph visualization (this is the hard part)
- Entity detail panel
- Basic graph interactions

**Phase 2: Discover Mode with Entity Intelligence**
- Feed with entity-rich finding cards
- Relevance scoring display
- Entity badges and navigation
- Suggestion cards

**Phase 3: Organize Mode with Tracking**
- Domain hierarchy
- Entity tracking configuration
- Alert settings

**Phase 4: Publish Mode**
- Approval queue
- Channel configuration
- Content preview

**Phase 5: Polish + Integration**
- Cross-mode navigation
- State management
- Responsive refinement
- Keyboard shortcuts

### Option C: Parallel Builds
Run multiple agents on different modes simultaneously, then integrate.

**Risk:** Integration pain, inconsistent patterns.

## Recommended Approach: Option B

Start with Phase 1 (Foundation + Explore) because:
1. The graph visualization is the technically hardest part
2. It's the most distinctive feature
3. Getting it right early establishes the visual language
4. Other modes can reference entity patterns established here

## Technology Decisions to Lock In

### Graph Visualization
**Recommendation: React Flow**
- Purpose-built for React
- Good performance with 100+ nodes
- Supports custom node shapes
- Active community

Alternatives:
- D3.js (more control, more work)
- Cytoscape.js (powerful but heavy)
- Sigma.js (good for large graphs)

### State Management
**Recommendation: Zustand**
- Simpler than Redux
- Works well with React 18
- Easy persistence

### Styling
**Recommendation: Tailwind CSS**
- Consistent with v1
- Fast iteration
- Good defaults

## Files to Create

1. `00-complete-specification.md` ✅ (done)
2. `01-fixtures/` - Mock data for all entity types
3. `02-phase-foundation-explore.md` - Phase 1 prompt
4. `03-phase-discover.md` - Phase 2 prompt
5. `04-phase-organize.md` - Phase 3 prompt
6. `05-phase-publish.md` - Phase 4 prompt
7. `06-phase-polish.md` - Phase 5 prompt

## Mock Data Requirements

### Entities (~50)
- 15 Organizations (foundations, platforms, companies)
- 10 People (creators, executives)
- 12 Grants (various types, deadlines)
- 8 Platforms (YouTube, Twitch, TikTok, etc.)
- 5 Amounts (funding ranges)

### Relationships (~100)
- funds relationships
- partners_with relationships
- competes_with relationships
- similar_to relationships
- mentions relationships

### Findings (~30)
- Each with 2-5 extracted entities
- Relevance scores and explanations
- Source metadata
- Confidence scores

## Success Metrics

The build is successful when:
1. Knowledge graph visualizes and is interactive
2. Entity types have distinct visual treatment
3. Relationships are visible and labeled
4. Cross-mode navigation works seamlessly
5. Relevance explanations appear on findings
6. The UI feels like an intelligence platform, not a simple app

## Next Steps

1. Create comprehensive mock data fixtures
2. Write Phase 1 prompt (Foundation + Explore)
3. Test build with one agent
4. Iterate on prompt based on results
5. Continue through phases
