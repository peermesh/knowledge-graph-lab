# AI Pipeline Research Navigation

## Directory Structure

```
docs/research/ai-pipeline/
├── README.md                                    # Quick overview
├── RESEARCH-INDEX.md                           # Master index of all tracks
├── RESEARCH-TRACKS-INVENTORY.md                # Detailed inventory and readiness
├── NAVIGATION-INDEX.md                         # This file - quick reference guide
│
├── Track 00: Competitive Landscape
│   ├── competitive-landscape-full-systems/     # Commercial platforms & full systems
│   └── competitive-landscape-partial-solutions/ # Open-source tools & academic SOTA
│
├── Track 01: Query Processing & Intent Detection
│   └── query-processing-nlp-evaluation/        # NLP library evaluation
│
├── Track 02: Gap Detection
│   └── gap-detection-algorithms/               # Gap algorithms & Neo4j performance
│
├── Track 03: Research Orchestration (2 prompts)
│   ├── research-orchestration-frameworks/      # Framework evaluation
│   └── research-orchestration-cost-analysis/   # Cost & source integration
│
├── Track 04: Document Ingestion
│   └── document-ingestion-pipeline/            # Parser & chunking strategies
│
├── Track 05: Entity Extraction (2 prompts)
│   ├── entity-extraction-llm-benchmarking/     # LLM provider benchmarking
│   └── entity-extraction-ner-deduplication/    # NER libraries & deduplication
│
├── Track 06: Relationship Extraction
│   └── relationship-extraction/                # Relationship extraction techniques
│
├── Track 07: Knowledge Graph Merge (2 prompts)
│   ├── knowledge-graph-merge-deduplication/    # Deduplication algorithms
│   └── knowledge-graph-merge-neo4j-performance/ # Neo4j performance & transactions
│
└── Track 08: Query Re-execution & Answer Synthesis
    └── query-reexecution-answer-synthesis/     # Answer synthesis strategies
```

## Quick Reference: Where to Find What

| I need to... | Go to... | Key Files |
|---|---|---|
| Understand build vs. buy decision | competitive-landscape-full-systems/ | .meta.md, responses/ |
| Compare open-source tools | competitive-landscape-partial-solutions/ | .meta.md, responses/ |
| Evaluate NLP libraries for query parsing | query-processing-nlp-evaluation/ | prompt.md, responses/ |
| Find gap detection algorithms | gap-detection-algorithms/ | .meta.md, responses/ |
| Compare orchestration frameworks | research-orchestration-frameworks/ | prompt.md, responses/ |
| Get cost analysis | research-orchestration-cost-analysis/ | source-comparison-matrix.md, responses/ |
| Choose document parser | document-ingestion-pipeline/ | .meta.md, responses/ |
| Benchmark LLM providers for entity extraction | entity-extraction-llm-benchmarking/ | responses/ |
| Find NER deduplication techniques | entity-extraction-ner-deduplication/ | .meta.md, responses/ |
| Learn relationship extraction methods | relationship-extraction/ | prompt.md, responses/ |
| Optimize entity deduplication | knowledge-graph-merge-deduplication/ | .meta.md, responses/ |
| Improve Neo4j merge performance | knowledge-graph-merge-neo4j-performance/ | performance-profile.md, cypher-examples.md |
| Understand answer synthesis | query-reexecution-answer-synthesis/ | .meta.md, responses/ |

## Reading Guides

### Quick Start (15 min)
1. Read this NAVIGATION-INDEX.md (what you're reading now)
2. Scan RESEARCH-INDEX.md sections on infrastructure status
3. Check README.md for directory overview
4. Identify your specific track and open its .meta.md file

**Result:** You understand where information lives and can navigate to what you need

### Technical Deep Dive (2-3 hours)
1. Start with RESEARCH-TRACKS-INVENTORY.md - understand all 9 tracks and dependencies
2. Read the .meta.md file for your track of interest
3. Read the prompt.md to see what questions were researched
4. Review responses/ directory and read 2-3 tool responses (they vary in depth)
5. Synthesize findings from .meta.md findings_summary field

**Result:** You understand research methodology and have actionable findings for your layer

### Complete Review (10+ hours)
1. Read RESEARCH-INDEX.md completely - understand all tracks and their relationships
2. For each track (00-08):
   - Read the .meta.md to understand objectives and findings
   - Read 2-3 responses to see different perspectives
   - Note key decisions and constraints
3. Read RESEARCH-TRACKS-INVENTORY.md to understand dependencies
4. Cross-reference findings between related tracks
5. Document any integration points you discover

**Result:** Full understanding of the entire 8-layer pipeline and all research decisions

## By Pipeline Layer

| Layer | Track # | Research Directory | Key Question |
|-------|---------|-------------------|---------------|
| 0: Competitive Analysis | 00 | competitive-landscape-*/ | Does this system already exist? |
| 1: Query Processing | 01 | query-processing-nlp-evaluation/ | Which NLP library works best? |
| 2: Gap Detection | 02 | gap-detection-algorithms/ | What algorithms detect gaps? |
| 3: Orchestration | 03 | research-orchestration-*/ | Which framework and cost model? |
| 4: Document Ingestion | 04 | document-ingestion-pipeline/ | How to parse and chunk docs? |
| 5: Entity Extraction | 05 | entity-extraction-*/ | Which LLM/NER gives best accuracy at lowest cost? |
| 6: Relationship Extraction | 06 | relationship-extraction/ | How to reliably extract relationships? |
| 7: Knowledge Graph Merge | 07 | knowledge-graph-merge-*/ | How to deduplicate and merge at scale? |
| 8: Query Re-execution | 08 | query-reexecution-answer-synthesis/ | How to synthesize final answers? |

## File Locations

### Master Index Files
- `RESEARCH-INDEX.md` - Complete index with infrastructure status and execution guidance
- `RESEARCH-TRACKS-INVENTORY.md` - Detailed inventory with readiness assessment and dependencies
- `README.md` - High-level overview and directory listing
- `NAVIGATION-INDEX.md` - This file (navigation and quick reference)

### Track 00: Competitive Landscape

**Full Systems (Commercial Platforms)**
- Location: `competitive-landscape-full-systems/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Responses: `responses/claude.md`, `responses/claude-cli.md`, `responses/chatgpt.md`, `responses/gemini.md`, `responses/grok.md`, `responses/deepseek.md`, `responses/perplexity.md`

**Partial Solutions (Open-source & Academic)**
- Location: `competitive-landscape-partial-solutions/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Responses: `responses/claude.md`, `responses/claude-cli.md`, `responses/chatgpt.md`, `responses/gemini.md`, `responses/grok.md`, `responses/deepseek.md`, `responses/perplexity.md`

### Track 01: Query Processing & NLP Evaluation
- Location: `query-processing-nlp-evaluation/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Responses: `responses/`

### Track 02: Gap Detection Algorithms
- Location: `gap-detection-algorithms/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Responses: `responses/`

### Track 03: Research Orchestration

**Part A: Framework Evaluation**
- Location: `research-orchestration-frameworks/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Responses: `responses/`

**Part B: Cost Analysis**
- Location: `research-orchestration-cost-analysis/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Key Files: `source-comparison-matrix.md`
- Responses: `responses/claude.md`, `responses/claude-cli.md`, `responses/chatgpt.md`, `responses/gemini.md`, `responses/grok.md`, `responses/deepseek.md`, `responses/perplexity.md`, `responses/perplexity-cli.md`

### Track 04: Document Ingestion Pipeline
- Location: `document-ingestion-pipeline/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Responses: `responses/`

### Track 05: Entity Extraction

**Part A: LLM Benchmarking**
- Location: `entity-extraction-llm-benchmarking/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Responses: `responses/`

**Part B: NER & Deduplication**
- Location: `entity-extraction-ner-deduplication/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Responses: `responses/`

### Track 06: Relationship Extraction
- Location: `relationship-extraction/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Responses: `responses/`

### Track 07: Knowledge Graph Merge

**Part A: Deduplication Algorithms**
- Location: `knowledge-graph-merge-deduplication/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Responses: `responses/`

**Part B: Neo4j Performance**
- Location: `knowledge-graph-merge-neo4j-performance/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Key Files: `responses/neo4j-performance-profile.md`, `responses/cypher-examples.md`, `responses/index-optimization-report.md`, `responses/test-graph-setup.md`
- Responses: `responses/`

### Track 08: Query Re-execution & Answer Synthesis
- Location: `query-reexecution-answer-synthesis/`
- Metadata: `.meta.md`
- Prompt: `prompt.md`
- Responses: `responses/`

## Research Track Dependencies

### Independent Tracks (start immediately)
- Track 01: Query Processing
- Track 04: Document Ingestion

### Tier 1 (depends on independent tracks)
- Track 02: Gap Detection (benefits from track 01)
- Track 05: Entity Extraction (depends on track 01)

### Tier 2 (depends on Tier 1)
- Track 03: Research Orchestration (depends on tracks 01 & 02)
- Track 06: Relationship Extraction (depends on track 05)

### Tier 3 (depends on Tier 2)
- Track 07: Knowledge Graph Merge (depends on tracks 05 & 06)

### Tier 4 (depends on all previous)
- Track 08: Query Re-execution (depends on tracks 01-07)

**Critical Path:** 01 → 05 → 06 → 07 → 08 (if sequential)

## How to Navigate by Role

### If you're an architect choosing infrastructure
1. Read `competitive-landscape-full-systems/` findings
2. Read `competitive-landscape-partial-solutions/` findings
3. Synthesize findings from tracks 01-08 for build vs. buy decision

### If you're implementing query processing
1. Go to `query-processing-nlp-evaluation/`
2. Read .meta.md findings_summary
3. Compare responses from different LLMs
4. Note tool recommendations and benchmarks

### If you're optimizing entity extraction costs
1. Go to `entity-extraction-llm-benchmarking/`
2. Read cost comparison findings
3. Go to `entity-extraction-ner-deduplication/`
4. Compare accuracy vs. cost tradeoffs

### If you're building the knowledge graph layer
1. Go to `knowledge-graph-merge-deduplication/`
2. Read deduplication algorithm findings
3. Go to `knowledge-graph-merge-neo4j-performance/`
4. Reference cypher-examples.md and performance-profile.md

### If you're doing the final answer synthesis
1. Go to `query-reexecution-answer-synthesis/`
2. Review answer synthesis strategies
3. Check citation accuracy findings
4. Verify latency requirements from track 01 baseline

## Status Overview

**All research complete (2025-11-16)**
- Track 00: Complete (2 topics, 20-28 hours)
- Tracks 01-08: Complete (12 research prompts, 452 hours total)
- Total research output: ~140,000 words
- All .meta.md files include findings summaries

## Tips for Navigation

1. **Start with .meta.md** - Every track has one with objectives, scope, and findings summary
2. **Compare responses** - Different LLMs provide different perspectives and depth
3. **Check findings_summary** - Each .meta.md includes concise findings without reading all responses
4. **Follow dependencies** - If a track depends on another, read in dependency order
5. **Use the quick reference table above** - Maps questions to directories

---

**Last Updated:** 2025-12-04
**Status:** All research complete and indexed
