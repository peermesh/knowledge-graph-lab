# Figma Make Workflow

**One comprehensive prompt → Complete application**

---

## Quick Overview

This workflow uses extensive planning with ChatGPT to create perfect specifications, then builds the entire app with Figma Make in ONE prompt.

**Time**: 3-5 hours total (80% planning, 5% building, 15% tweaks)
**Output**: Production-ready, maintainable application

---

## The 80/5/15 Rule

```
80% (2-4 hours) - Planning with ChatGPT
 5% (5-30 min)  - Building with Figma Make
15% (30-60 min) - Minor refinements
```

**Key insight**: "The better you plan, the less you iterate."

---

## Workflow Overview

### Phase 1: Planning with ChatGPT (80%)

**Step 1: Get Complete App Overview**
- App type and purpose
- Core features (5-7 main functionalities)
- User flow from start to finish
- Page structure with descriptions

**Step 2: Define All Page Architectures**
- Detailed breakdown for EVERY page
- Layout structure for each
- Key components needed
- Interactive elements
- Navigation flow
- Content specifications
- All states (loading, error, empty)

**Step 3: Create Complete Design System**
- Color palette (with hex codes)
- Typography system (fonts, sizes, weights, line heights)
- Spacing scale (4px base recommended)
- Component styles (buttons, inputs, cards)
- Layout grid and responsive breakpoints

### Phase 2: Build with Figma Make (5%)

One comprehensive prompt combining:
```
[Engineering Best Practices Prefix]
+ [App Overview from Step 1]
+ [All Page Architectures from Step 2]
+ [Complete Design System from Step 3]
= Complete Working Application
```

### Phase 3: Optional Refinements (15%)

Targeted tweaks if needed:
- Design adjustments
- Functionality updates
- Content changes

---

## Prerequisites

**Required:**
- Figma Make subscription/access
- ChatGPT or Claude for planning
- Time for thorough planning (2-4 hours)

**Recommended:**
- Understanding of web design principles
- Clear project vision
- Patience for comprehensive specification

---

## Key Success Factors

1. **Be thorough in planning** - Don't skip details
2. **Include everything in Step 2** - All pages, all interactions, all states
3. **Define a complete design system** - Exact colors, fonts, spacing
4. **Copy-paste accurately** - Give Figma Make all the info
5. **Use the engineering best practices prefix** - ALWAYS

---

## Standard Figma Make Prompt Prefix

**Use at the START of every Figma Make prompt:**

```
Build this following engineering best practices:
- Write all code to WCAG AA accessibility standards
- Create and use reusable components throughout
- Use semantic HTML and proper component architecture
- Avoid absolute positioning; use flexbox/grid layouts
- Build actual code components, not image SVGs
- Keep code clean, maintainable, and well-structured
```

---

## Full Workflow Guide

See `WORKFLOW-GUIDE.md` in this directory for:
- Complete ChatGPT prompt templates for all 3 planning steps
- The comprehensive Figma Make build prompt
- Optional tweak prompts
- Troubleshooting guide
- Success checklist

---

## Pros & Cons

### Pros
- 🎯 One-shot generation when planned correctly
- 📋 Complete control over specifications
- ⚡ Fast build phase (5 minutes)
- 🏗️ Clean, maintainable code output
- 🔄 Minimal iteration needed

### Cons
- 📝 Requires extensive upfront planning
- 💰 Requires Figma Make subscription
- 🧠 You must create comprehensive specs
- ⏰ Longest planning phase of all workflows

---

## When to Use This Workflow

✅ **Use Figma Make if:**
- You have Figma Make subscription
- You can invest 80% time in planning
- You want one-shot generation
- You need complete control over specs
- You value clean, maintainable code

❌ **Consider alternatives if:**
- You want autonomous execution → Use Figma MCP workflow
- You don't have Figma designs → Use AI Builders workflow
- You want quick prototyping → Use Design Kit + AI Builders

---

## Related Documents

- **Full Workflow Guide**: `WORKFLOW-GUIDE.md` (in this directory)
- **Engineering Best Practices**: `../ENGINEERING-BEST-PRACTICES.md`
- **Planning Philosophy**: `../PLANNING-FIRST-PHILOSOPHY.md`
- **Workflow Selection**: `../WORKFLOW-SELECTION-GUIDE.md`

---

**Last Updated**: 2025-10-27
**Status**: Battle-Tested Wisdom
