# Workflow Selection Guide

**Choose the right design-to-code workflow for your needs.**

---

## Quick Decision Tree

```
Do you have a Figma design?
├─ YES
│  ├─ Figma Design exists → Which tool?
│  │  ├─ Want autonomous agent? → Figma MCP Workflow
│  │  ├─ Have Figma Make access? → Figma Make Workflow
│  │  └─ Using v0/Claude/Bolt? → AI Builders Workflow
│  │
│  └─ No Figma yet → Design Kit First (create specs, then Figma)
│
└─ NO
   └─ Start with Design Kit → Generate specs → Then choose workflow above
```

---

## Workflow Comparison

| Workflow | Best For | Time | Control | Tools Needed |
|----------|----------|------|---------|--------------|
| **Figma MCP** | Developers wanting full autonomy | 1-3 hours | Low (agent-driven) | Figma file + MCP server |
| **Figma Make** | Teams with planning time | 30-60 min | High (you plan everything) | Figma file + Figma Make access |
| **AI Builders** | Quick prototypes, no Figma | 20-45 min | Medium (guided) | Design specs (from design kit) |
| **Design Kit** | Starting from scratch | 2-4 hours | Complete | None (templates provided) |

---

## Workflow 1: Figma MCP (Autonomous Agent)

**File**: `workflows/figma-mcp/AGENT-WORKFLOW.md`

### When to Use

- ✅ You have a complete Figma design
- ✅ You want minimal human intervention
- ✅ You trust the agent to make implementation decisions
- ✅ You have Figma MCP server configured

### How It Works

```
Agent discovers Figma structure
    ↓
Agent captures all screens
    ↓
Agent creates implementation plan
    ↓
Agent builds HTML/CSS autonomously
    ↓
Agent tests complete flow
```

### Time Investment

- **Your time**: 15 minutes (provide Figma URL, review output)
- **Agent time**: 1-3 hours (autonomous execution)
- **Planning required**: None (agent handles it)

### Pros

- 🚀 Fully autonomous - set it and forget it
- 🔍 Agent discovers all pages automatically
- 🧪 Built-in quality checks and testing
- 📦 Downloads all assets from Figma
- 🔗 Implements complete navigation flow

### Cons

- 🤖 Less control over implementation choices
- ⏱️ Longer total execution time
- 🔧 Requires MCP server setup
- 🎯 Best for straightforward designs (complex UX may need guidance)

### Prerequisites

- Figma file URL with node IDs
- Figma MCP server configured in Claude
- Image download enabled in Figma MCP settings

---

## Workflow 2: Figma Make (Planning + One-Shot Build)

**File**: `workflows/figma-make/WORKFLOW-GUIDE.md`

### When to Use

- ✅ You have Figma Make access
- ✅ You can invest time in thorough planning
- ✅ You want to build everything in ONE prompt
- ✅ You want complete control over specifications

### How It Works

```
80% Planning with ChatGPT:
    1. App overview
    2. All page architectures
    3. Complete design system
    ↓
5% Building with Figma Make:
    One comprehensive prompt → Complete app
    ↓
15% Minor tweaks (optional)
```

### Time Investment

- **Planning**: 2-4 hours (ChatGPT conversations)
- **Building**: 5-30 minutes (one Figma Make prompt)
- **Refinement**: 30-60 minutes (optional tweaks)

### Pros

- 🎯 One-shot generation (when planned well)
- 📋 Complete control over specifications
- ⚡ Fast build phase (5 minutes)
- 🏗️ Results in clean, maintainable code

### Cons

- 📝 Requires extensive upfront planning
- 💰 Requires Figma Make subscription
- 🧠 You must create comprehensive specs manually
- ⏰ Longest planning phase

### Prerequisites

- Figma Make access
- ChatGPT or Claude for planning phase
- Patience for thorough specification work

### See Also

- 80/5/15 Philosophy: `workflows/PLANNING-FIRST-PHILOSOPHY.md`
- Engineering Best Practices: `workflows/ENGINEERING-BEST-PRACTICES.md`

---

## Workflow 3: AI Builders (v0, Claude, Bolt.new)

**File**: `../USAGE-WITH-AI-BUILDERS.md`

### When to Use

- ✅ You DON'T have a Figma design yet
- ✅ You want to use v0, Claude, or Bolt.new
- ✅ You have design specifications (from design kit)
- ✅ You want iterative prototyping

### How It Works

```
Design Kit Templates (30 minutes):
    Fill docs 03, 02b, 04
    ↓
Combine with Engineering Best Practices prefix
    ↓
Submit to AI Builder (v0/Claude/Bolt)
    ↓
Iterate on generated prototype
```

### Time Investment

- **Design specs**: 30-60 minutes (design kit templates)
- **Generation**: 5-15 minutes (AI builder)
- **Iteration**: 30-90 minutes (refinements)

### Pros

- 🚀 No Figma required
- 🔄 Iterative workflow (easy to adjust)
- 🎨 Design kit templates guide you
- 🛠️ Works with multiple AI tools
- 💰 Free or low-cost options available

### Cons

- 🔁 More iteration needed vs one-shot workflows
- 🎯 Less precise than working from Figma designs
- 📝 Still requires filling design kit templates
- ⚠️ Skip doc 05 to avoid tech stack conflicts

### Prerequisites

- Access to v0, Claude, or Bolt.new
- Design kit templates (provided in repo)
- Basic understanding of design concepts

### Key Documents to Fill

**MUST fill (3 docs, ~30 minutes)**:
1. `03-visual-design-requirements.md` - Colors, typography, spacing
2. `02b-page-layouts.md` - Page structure and components
3. `04-interaction-design.md` - Interactions and states

**SKIP** (to avoid conflicts):
- `05-implementation-guidelines.md` - Let AI builder choose tech stack

---

## Workflow 4: Design Kit (Start from Scratch)

**File**: `../README.md`

### When to Use

- ✅ You have NO design yet (pure concept)
- ✅ You want to create comprehensive design specs
- ✅ You need documentation for handoff
- ✅ You're starting from requirements/discovery

### How It Works

```
Use scaffold script:
    .dev/kits/design-kit/scripts/bash/scaffold-workspace.sh
    ↓
Fill all templates (or design-focused subset)
    ↓
Validate specifications
    ↓
Handoff to implementation (choose workflow 1, 2, or 3)
```

### Time Investment

- **Full specification**: 2-4 hours (all 10 templates)
- **Design-focused**: 30-60 minutes (3 templates for AI builders)
- **Minimal**: 15-30 minutes (quick specs)

### Pros

- 📝 Creates comprehensive documentation
- 🎯 Forces you to think through all details
- 🔄 Reusable specifications across tools
- 🤝 Perfect for team handoffs
- ✅ Includes validation scripts

### Cons

- ⏱️ Most time-intensive upfront
- 📋 Requires discipline to fill templates
- 🧠 You must make all design decisions

### Prerequisites

- Design kit installed (git submodule)
- Bash scripts accessible
- Time to thoughtfully fill templates

### Output Artifacts

Generates complete workspace with all templates:
- Design philosophy and principles
- Information architecture
- Page layouts and specifications
- Visual design requirements
- Interaction design patterns
- Implementation guidelines
- Accessibility standards
- Component specifications
- Data flow documentation
- Testing requirements

---

## Decision Matrix

### Choose Figma MCP if:
- [ ] You have complete Figma designs
- [ ] You want autonomous execution
- [ ] You trust agent decisions
- [ ] You have MCP server access

### Choose Figma Make if:
- [ ] You have Figma Make subscription
- [ ] You can invest 80% time in planning
- [ ] You want one-shot generation
- [ ] You need complete control over specs

### Choose AI Builders if:
- [ ] You don't have Figma designs
- [ ] You want iterative prototyping
- [ ] You're using v0/Claude/Bolt.new
- [ ] You can fill 3 design kit templates

### Choose Design Kit First if:
- [ ] You're starting from pure concept
- [ ] You need comprehensive documentation
- [ ] You're doing team handoffs
- [ ] You want maximum control

---

## Hybrid Approaches

### Design Kit → Figma → Figma MCP
1. Create specs with design kit (2-4 hours)
2. Create Figma designs from specs (2-3 hours)
3. Run Figma MCP for autonomous build (1 hour)

**Best for**: Teams with designers + developers

### Design Kit → AI Builders (Direct)
1. Fill 3 design-focused templates (30 min)
2. Submit to AI builder with best practices prefix (5 min)
3. Iterate on prototype (30-60 min)

**Best for**: Solo developers, quick prototypes

### Figma Make (Planning) → AI Builders (Build)
1. Use ChatGPT planning workflow from Figma Make (2-4 hours)
2. Use planning outputs as input to v0/Claude instead
3. Iterate on generated code

**Best for**: No Figma Make access but want planning rigor

---

## Common Scenarios

### Scenario 1: "I have a Figma design from a designer"
→ **Figma MCP Workflow** (fastest, autonomous)

### Scenario 2: "I want to prototype an idea quickly"
→ **AI Builders Workflow** (30 min design kit + v0/Claude)

### Scenario 3: "I need pixel-perfect implementation"
→ **Figma Make Workflow** (extensive planning, one-shot build)

### Scenario 4: "I'm starting from scratch with no design"
→ **Design Kit Workflow** → Then choose builder workflow

### Scenario 5: "I need documentation for a team handoff"
→ **Design Kit Workflow** (full 10 templates)

---

## Tool Requirements Summary

| Workflow | Required Tools | Optional Tools |
|----------|----------------|----------------|
| Figma MCP | Claude Code + Figma MCP + Figma file | - |
| Figma Make | Figma Make + ChatGPT/Claude + Figma file | - |
| AI Builders | v0 or Claude or Bolt.new | Design kit templates |
| Design Kit | Bash + Text editor | Git (for submodule) |

---

## Next Steps

1. **Identify your starting point**: Figma design? Pure concept? Requirements?
2. **Review time constraints**: Hours available? Days? Weeks?
3. **Check tool access**: What tools do you have available?
4. **Pick workflow**: Use decision matrix above
5. **Read detailed guide**: Navigate to specific workflow file
6. **Execute**: Follow step-by-step instructions

---

## Related Documents

- **Engineering Best Practices**: `ENGINEERING-BEST-PRACTICES.md`
- **Planning Philosophy**: `PLANNING-FIRST-PHILOSOPHY.md`
- **Figma Make Guide**: `figma-make/WORKFLOW-GUIDE.md`
- **Figma MCP Guide**: `figma-mcp/AGENT-WORKFLOW.md`
- **AI Builders Usage**: `../USAGE-WITH-AI-BUILDERS.md`
- **Design Kit README**: `../README.md`

---

**Last Updated**: 2025-10-27
**Status**: Production Ready
