# Design-to-Code Workflows

**Choose the right workflow for your design implementation needs**

---

## Quick Start

**Don't know which workflow to use?** → Read `WORKFLOW-SELECTION-GUIDE.md`

**Have a Figma design?** → Choose between `figma-mcp/` or `figma-make/`

**No Figma yet?** → Use `ai-builders/` workflow with design kit templates

**Starting from scratch?** → Use design kit templates first, then choose a workflow

---

## Available Workflows

### 1. Figma MCP Workflow
**Directory**: `figma-mcp/`

**Best for**: Autonomous agent execution from Figma designs

- ⏱️ **Time**: 1-3 hours (mostly autonomous)
- 🤖 **Control**: Low (agent-driven)
- 🎯 **Prerequisites**: Figma file + MCP server

**When to use**: You have Figma designs and want minimal human intervention.

[Read Full Guide →](figma-mcp/README.md)

---

### 2. Figma Make Workflow
**Directory**: `figma-make/`

**Best for**: One-shot generation with comprehensive planning

- ⏱️ **Time**: 3-5 hours (80% planning)
- 🎯 **Control**: High (you plan everything)
- 💰 **Prerequisites**: Figma file + Figma Make subscription

**When to use**: You want complete control and one-shot generation after thorough planning.

[Read Full Guide →](figma-make/README.md)

---

### 3. AI Builders Workflow
**Directory**: `ai-builders/`

**Best for**: Quick prototyping with v0, Claude, Bolt.new

- ⏱️ **Time**: 30-90 minutes
- 🔄 **Control**: Medium (iterative)
- 🎨 **Prerequisites**: Design specs (from design kit)

**When to use**: You don't have Figma designs and want to use AI code generators.

[Read Full Guide →](ai-builders/README.md)

---

## Core Principles

### Engineering Best Practices
**File**: `ENGINEERING-BEST-PRACTICES.md`

Universal prompt prefix for all workflows ensuring:
- WCAG AA accessibility standards
- Reusable component architecture
- Semantic HTML and proper structure
- Flexbox/grid layouts (no absolute positioning)
- Clean, maintainable code

[Read Best Practices →](ENGINEERING-BEST-PRACTICES.md)

---

### Planning-First Philosophy
**File**: `PLANNING-FIRST-PHILOSOPHY.md`

The 80/5/15 rule:
- 80% Planning & specification
- 5% Building & generation
- 15% Minor tweaks

**Key insight**: "The better you plan, the less you iterate."

[Read Philosophy →](PLANNING-FIRST-PHILOSOPHY.md)

---

## Decision Matrix

| I have... | I want... | Use this workflow |
|-----------|-----------|-------------------|
| Figma design | Autonomous build | **Figma MCP** |
| Figma design | One-shot build with planning | **Figma Make** |
| Design specs | Quick prototype | **AI Builders** |
| Just an idea | Comprehensive docs | **Design Kit first** |

---

## Workflow Selection Guide

**File**: `WORKFLOW-SELECTION-GUIDE.md`

Comprehensive guide covering:
- Decision tree for workflow selection
- Detailed comparison table
- Tool requirements
- Common scenarios
- Hybrid approaches
- Step-by-step selection process

[Read Selection Guide →](WORKFLOW-SELECTION-GUIDE.md)

---

## Integration with Design Kit

All workflows integrate seamlessly with the design kit:

**Design Kit Templates** → **Workflow Execution** → **Working Prototype**

1. **Start with design kit** (optional but recommended)
   - Create workspace: `scripts/bash/scaffold-workspace.sh`
   - Fill templates (all 10 or design-focused subset)
   - Validate: `scripts/bash/validate-specs.sh`

2. **Choose workflow based on tools available**
   - Figma + MCP → Autonomous agent workflow
   - Figma + Figma Make → Planning-first workflow
   - Design specs only → AI builders workflow

3. **Execute and iterate**
   - Follow workflow-specific guide
   - Apply engineering best practices
   - Test and refine

---

## Directory Structure

```
workflows/
├── README.md (this file)
├── WORKFLOW-SELECTION-GUIDE.md
├── ENGINEERING-BEST-PRACTICES.md
├── PLANNING-FIRST-PHILOSOPHY.md
├── figma-mcp/
│   ├── README.md
│   └── AGENT-WORKFLOW.md
├── figma-make/
│   ├── README.md
│   └── WORKFLOW-GUIDE.md
└── ai-builders/
    └── README.md
```

---

## Quick Reference Commands

### Design Kit Scaffolding
```bash
# Create new design workspace
.dev/kits/design-kit/scripts/bash/scaffold-workspace.sh \
  "Interface Name" workspace-name

# Validate specifications
.dev/kits/design-kit/scripts/bash/validate-specs.sh \
  .dev/ux-ui-design/workspace-name/
```

### Workflow Execution

**Figma MCP** (with agent):
```
"Build this Figma design: [FIGMA_URL]"
```

**Figma Make** (after planning):
```
[Paste comprehensive prompt with prefix + planning outputs]
```

**AI Builders** (v0/Claude/Bolt):
```
[Paste best practices prefix + design specs from templates 03, 02b, 04]
```

---

## Success Metrics

After workflow completion, verify:

- ✅ All pages/screens implemented
- ✅ Navigation working between pages
- ✅ Design system applied consistently
- ✅ Responsive on mobile/tablet/desktop
- ✅ Accessibility standards met
- ✅ Code is clean and maintainable
- ✅ Assets loaded correctly
- ✅ Interactive elements have proper states

---

## Next Steps

1. **Choose workflow**: Use selection guide if uncertain
2. **Read workflow README**: Navigate to specific workflow directory
3. **Follow detailed guide**: Execute step-by-step instructions
4. **Apply best practices**: Always use engineering best practices prefix
5. **Test thoroughly**: Verify all success metrics
6. **Iterate**: Make targeted refinements as needed

---

## Related Documentation

- **Design Kit Main Guide**: `../USAGE-WITH-AI-BUILDERS.md`
- **Design Kit README**: `../README.md`
- **Template Documentation**: `../templates/`
- **Example Outputs**: `../examples/`

---

**Last Updated**: 2025-10-27
**Status**: Production Ready
**Version**: 1.0
