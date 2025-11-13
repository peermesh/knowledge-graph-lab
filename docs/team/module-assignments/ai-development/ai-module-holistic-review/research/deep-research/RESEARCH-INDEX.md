# Deep Research Index

**Last updated:** 2025-11-13
**Project:** Knowledge Graph Lab Alpha - AI Module
**Location:** `docs/team/module-assignments/ai-development/ai-module-holistic-review/research/deep-research/`

---

## Active Research Topics

| Priority | Status | Topic | Gap | Directory | Est. Effort |
|----------|--------|-------|-----|-----------|-------------|
| 1 | pending | Commercial Platforms & Full System Evaluation | Does a single commercial platform solve our 8-layer pipeline? | `./competitive-landscape-full-systems/` | 8-12 hours |
| 1 | pending | Partial Solutions, Layer-by-Layer Analysis & Academic SOTA | If no single platform, which open-source tools work best for each layer? | `./competitive-landscape-partial-solutions/` | 12-16 hours |

---

## Research Topic 1: Commercial Platforms & Full System Evaluation

**Directory:** `competitive-landscape-full-systems/`

**Gap:** Does Perplexity AI, Microsoft GraphRAG, LangChain, LlamaIndex, Neo4j, TigerGraph, AWS Kendra, Google Vertex AI, or any other commercial platform already provide a complete 8-layer autonomous research-enrichment pipeline solution?

**Impact:** Build vs. buy decision. If a suitable platform exists, we should license/fork rather than custom build. Blocks all architectural decisions.

**Files:**
- `.meta.md` - Research metadata with objectives and scope
- `prompt.md` - Clipboard-ready research prompt
- `responses/` - Result files (claude.md, perplexity.md, chatgpt.md, gemini.md, grok.md, deepseek.md)

**Status:** Ready to execute
**Priority:** 1 (CRITICAL - blocks all other research)

---

## Research Topic 2: Partial Solutions, Layer-by-Layer Analysis & Academic SOTA

**Directory:** `competitive-landscape-partial-solutions/`

**Gap:** If no single complete platform exists, what are the best open-source tools, academic solutions, and state-of-the-art approaches for each of our 8 pipeline layers? Can we successfully compose best-of-breed tools into a working system?

**Impact:** Layer-by-layer architectural decisions. Enables tool stack recommendations and composition feasibility analysis. Unblocks implementation planning.

**Files:**
- `.meta.md` - Research metadata with objectives and scope
- `prompt.md` - Clipboard-ready research prompt
- `responses/` - Result files (claude.md, perplexity.md, chatgpt.md, gemini.md, grok.md, deepseek.md)

**Status:** Ready to execute
**Priority:** 1 (CRITICAL - follows Topic 1, unblocks Tracks 01-08)

---

## How to Execute Research

### Step 1: Choose Execution Method

**Option A: AI Research Agent (Fastest)**
- Invoke deep-research-analyst with Topic 1 prompt
- Agent executes research, writes to `responses/claude-cli.md`
- Repeat for Topic 2
- Total time: 4-6 hours (parallel execution)

**Option B: External Research Tools (High Control)**
1. Open `[topic]/prompt.md`
2. Copy entire prompt (clipboard-ready)
3. Paste into: Perplexity.ai, ChatGPT, Claude, Gemini
4. Save results to `responses/[tool-name].md`
5. Repeat for second topic

**Option C: Parallel Human Execution (Best Quality)**
- Researcher A: Topic 1 (commercial platforms) - 8 hours
- Researcher B: Topic 2 (tools + SOTA) - 12 hours
- Run simultaneously, total time: 12 hours instead of 20 hours

### Step 2: Update Status

After execution:
1. Update `.meta.md` status from `pending` → `in-progress` → `complete`
2. Update this index status column
3. Document any findings summary in `.meta.md` under `findings` field

### Step 3: Use Findings for Next Phase

- Topic 1 findings inform: **Build vs. Buy decision**
- Topic 2 findings inform: **Tracks 01-08 research** (layer-by-layer research tracks)

---

## Connection to Project Structure

**Technical Blueprint:** `ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md` (Read this FIRST)
- Detailed 8-layer pipeline architecture with JSON examples
- Technical requirements, data structures, and workflows
- Layer-by-layer maturity assessment (novel vs. commoditized)
- **PREREQUISITE** for understanding what you're evaluating
- Located: `/Users/grig/work/peermesh/repo/knowledge-graph-lab-alpha/.dev/_sprint_ai_module_nov13/ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md`

**Planning Documents:** `../../research-tracks/00-COMPETITIVE-LANDSCAPE-RESEARCH.md`
- Explains WHAT needs to be researched and WHY
- Research methodology and success criteria

**Deep Research (This Directory):** Execution infrastructure
- Explains HOW to research: specific prompts, objectives, metadata
- Both prompts include prerequisite reference to architecture document

**Recommended Reading Order:**
1. **First:** ARCHITECTURE-FOR-COMPETITIVE-RESEARCH.md (understand the system)
2. **Second:** Planning doc to understand research questions
3. **Third:** Execute research prompts in this directory
4. **Fourth:** Save findings to `responses/` subdirectories
5. **Finally:** Use findings to complete Tracks 01-08 research

---

## Metadata Format (.meta.md)

Each research topic has a `.meta.md` file with YAML frontmatter:

```yaml
---
gap: [What we don't know - detailed description]
impact: [Parts of project affected]
tags: [relevant, tags, here]
created: YYYY-MM-DD
updated: YYYY-MM-DDTHH:MM:SS
priority: [1-5, where 1 is highest]
status: [pending | in-progress | complete]
findings_summary: [Brief summary if complete]
---
```

This structure enables:
- Automated tracking of research status
- Clear documentation of research objectives
- Integration with project tracking systems
- Handoff capability to other agents

---

## Next Steps

1. **Assign researchers** to Topics 1 and 2
2. **Choose execution method** (agent, external tool, or human)
3. **Execute research** using prompts in each subdirectory
4. **Update status** as research progresses
5. **Document findings** in `responses/` and `.meta.md`
6. **Use results** to inform Tracks 01-08 research

---

**Status:** Ready to execute - awaiting team assignment
**Last Updated:** 2025-11-13
