# KGL Pipeline Debugger: Documentation Index

**Status:** Design complete, ready for review

---

## Documents

| # | Document | Purpose | Status |
|---|----------|---------|--------|
| 00 | [VISION.md](./00-VISION.md) | What we're building, the missing reasoning layer, UI mockup | ✅ Complete |
| 01 | [ARCHITECTURE.md](./01-ARCHITECTURE.md) | System layers, API design, module contracts, Docker setup | ✅ Complete |
| 02 | [DATA-FLOW.md](./02-DATA-FLOW.md) | Feedback loops, convergence criteria, stage-level I/O | ✅ Complete |
| 03 | [PIPELINE-SCHEMATIC.md](./03-PIPELINE-SCHEMATIC.md) | Stages, transforms, mixins, config reference | ✅ Complete |
| 04 | [SPRINT-PLAN.md](./04-SPRINT-PLAN.md) | 14-day build plan, daily targets, definition of done | ✅ Complete |
| 05 | [EXPLORATION-LAYER.md](./05-EXPLORATION-LAYER.md) | Pre-research discovery, user profiling, question crystallization | ✅ Complete |
| 06 | [REASONING-ENGINE.md](./06-REASONING-ENGINE.md) | Outer loop control, convergence, decisions | ✅ Complete |
| 07 | [INPUT-GATE.md](./07-INPUT-GATE.md) | Security boundary, prompt injection prevention, input validation | ✅ Complete |
| 08 | [OUTPUT-GATE.md](./08-OUTPUT-GATE.md) | Publishing, syndication, scheduled delivery, user preferences | ✅ Complete |

---

## Architecture Overview

```
                         UNTRUSTED ZONE
                              │
╔═════════════════════════════╪═════════════════════════════════════════════╗
║                       INPUT GATE                                           ║
║  Validate → Sanitize → Normalize → Log → Queue                            ║
║  (Security boundary - converts all input to known data structures)        ║
╚═════════════════════════════╪═════════════════════════════════════════════╝
                              │
                         TRUSTED ZONE
                              │
┌─────────────────────────────┼─────────────────────────────────────────────┐
│                       EXPLORATION LAYER                                    │
│  Dialogue → User Profile → Context Map → Crystallize → ResearchQuestion  │
└─────────────────────────────┼─────────────────────────────────────────────┘
                              │
┌─────────────────────────────┼─────────────────────────────────────────────┐
│                       REASONING ENGINE                                     │
│  State Monitor → Evaluate → Decide → Refine                               │
│                              │                                             │
│              ┌───────────────┼───────────────┐                            │
│              ▼               ▼               ▼                            │
│          CONTINUE         OUTPUT           ASK                            │
│              │               │               │                            │
│  ┌───────────┴───────────────┴───────────────┴───────────────────────┐   │
│  │                      INNER LOOP                                    │   │
│  │  QUERY → GAPS → SEARCH → INGEST → EXTRACT → RELATE → KG → SYNTH  │   │
│  └───────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────┼─────────────────────────────────────────────┘
                              │
╔═════════════════════════════╪═════════════════════════════════════════════╝
║                       OUTPUT GATE                                          ║
║  Classify → Schedule → Format → Deliver → Track                           ║
║  (Publishing/syndication - user-controlled delivery)                      ║
╚═════════════════════════════╪═════════════════════════════════════════════╝
                              │
                         EXTERNAL WORLD
                    (Devices, Inboxes, Feeds)
```

---

## The Five Layers

### 1. Input Gate (Security Boundary)
Single flow-through point for ALL external input. Creates a "logic gap" where everything is converted to known data structures before entering the queue.

- **Validate:** Schema, types, bounds
- **Sanitize:** Prompt injection, XSS, SQLi prevention
- **Normalize:** Convert to typed KnownInput structures
- **Log:** Complete audit trail for debugging
- **Queue:** Only validated data enters processing

**Key principle:** LLMs never see raw user input—only typed structures that cannot be misinterpreted as instructions.

### 2. Exploration Layer (Pre-Research)
Discover what user actually needs before they know it.

- **Dialogue:** Surface latent needs through conversation
- **Profile:** Psychological + factual user model  
- **Context:** Org, stakeholders, constraints
- **Crystallize:** Vague → concrete research questions

### 3. Reasoning Engine (Outer Loop)
Control iteration and convergence.

- **State Monitor:** Track confidence, coverage, cost
- **Evaluate:** Score current answer
- **Decide:** CONTINUE | OUTPUT | ASK
- **Refine:** Adjust strategy for next iteration

### 4. Processing Pipeline (Inner Loop)
Execute research.

- Query → Gaps → Search → Ingest → Extract → Relate → KG Merge → Synth

### 5. Output Gate (Publishing & Syndication)
User-controlled delivery of outputs.

- **Classify:** Type, audience, urgency
- **Schedule:** Timing, batching, quiet hours (user sets these)
- **Format:** Email, push, Slack, RSS, webhooks
- **Deliver:** Per-channel queues with rate limiting
- **Track:** Opens, clicks, delivery status

---

## Key Insights

### Security: The Logic Gap
Most AI systems pass raw user input to LLMs. This enables prompt injection. The Input Gate creates a hard boundary: nothing passes through unchanged. Everything becomes typed data structures.

### Research: Know What You Don't Know
Most research tools assume you know what you're looking for. The Exploration Layer helps you figure that out first, then the Reasoning Engine iteratively researches until confident.

### Delivery: User Control
Users configure their own delivery preferences: which channels, what timing, quiet hours, frequency limits. The Output Gate respects all of these.

---

## Convergence Criteria

The Reasoning Engine stops when ANY of:
- Confidence ≥ 85%
- Coverage ≥ 90%
- Diminishing returns (last 2 loops < 5% new info)
- Max iterations reached (10)
- Budget exhausted ($0.50 default)
- User interrupt

---

## Related KGL Docs

- [Publishing-Tools-Spec.md](../../modules/publishing-tools/Publishing-Tools-Spec.md) — Publishing module specification (complements Output Gate)
- [security-compliance.md](../../modules/shared/common/security-compliance.md) — Security standards
- [Research Synthesis](../../research/ai-pipeline/RESEARCH-SYNTHESIS.md) — 8-layer pipeline research
- [Foundation Docs](../../foundation/) — Vision, architecture, principles

---

## Document Alignment Notes

### Output Gate ↔ Publishing-Tools-Spec

The Output Gate (08-OUTPUT-GATE.md) provides the **technical architecture** for the publishing layer, while Publishing-Tools-Spec.md defines the **module responsibilities and interfaces**.

| Output Gate Component | Publishing-Tools-Spec Coverage |
|----------------------|-------------------------------|
| Classify | Personalization Engine (relevance scores, filtering) |
| Schedule | Scheduling System (digests, summaries, instant alerts) |
| Format | Content Formatting (HTML, Slack, plain text) |
| Delivery Queue | Multi-Channel Distribution |
| Transport Layer | External APIs (SendGrid, Slack, webhooks) |
| Tracker | Analytics Tracking (open rates, clicks, engagement) |

Both documents are aligned and should be maintained together.

---

## Interactive Visualization

Open **[pipeline-visual.html](./pipeline-visual.html)** in a browser to explore the 5-layer architecture interactively:

- Click any component to view Summary, Settings, Docs, and Metrics
- Visual representation of all layers and their relationships
- Realistic settings and configuration options
