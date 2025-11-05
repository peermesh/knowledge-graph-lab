# Planning-First Philosophy: The 80/5/15 Rule

**Core Principle**: "The better you plan, the less you iterate. That's the whole game."

---

## The 80/5/15 Time Investment

Proven time breakdown for design-to-code workflows:

```
80% - Planning & Specification (ChatGPT, Claude, Design Kit)
 5% - Building & Generation (Figma Make, v0, Bolt.new)
15% - Minor Tweaks & Refinements
```

---

## Why This Works

### Traditional Approach (FAILS)
```
10% - Rough planning
20% - Initial build
70% - Endless iteration fixing problems
```

**Result**: Frustration, wasted time, incomplete features

### Planning-First Approach (SUCCEEDS)
```
80% - Comprehensive planning
 5% - One-shot generation
15% - Polish & minor fixes
```

**Result**: Working product, predictable timeline, high quality

---

## The 80%: What Planning Means

### Three Planning Phases

**Phase 1: App Overview (20% of planning time)**
- App type and purpose
- Core features (5-7 main functionalities)
- User flow from start to finish
- Page structure with descriptions

**Phase 2: Page Architectures (50% of planning time)**
- Detailed breakdown for EVERY page
- Layout structure
- Key components
- Interactive elements
- Navigation flow
- Content specifications
- All states (loading, error, empty)

**Phase 3: Design System (30% of planning time)**
- Complete color palette with hex codes
- Typography system (fonts, sizes, weights, line heights)
- Spacing scale
- Component styles (buttons, inputs, cards)
- Layout grid and responsive breakpoints

### Output Artifacts

From this planning, you should have:
- ✅ Written document: App overview
- ✅ Written document: All page specifications
- ✅ Written document: Complete design system
- ✅ Total: 3-5 pages of comprehensive specs

**These documents become your "one comprehensive prompt" input.**

---

## The 5%: Building Execution

Once planning is complete:

```
# One comprehensive prompt
[Engineering Best Practices Prefix]
+ [App Overview]
+ [All Page Specifications]
+ [Complete Design System]
= Working Application
```

**Time**: 5-30 minutes depending on tool
**Iterations**: Ideally ONE (if planning was thorough)

---

## The 15%: Refinement

After one-shot generation, typical refinements:

- Design tweaks (colors, spacing, fonts)
- Content updates (copy changes)
- Interaction improvements (hover states, transitions)
- Edge case handling

**NOT refactoring architecture** - that should be right from planning.

---

## Planning Checklist

Before you start building, ensure you can answer:

### App Level
- [ ] What problem does this solve?
- [ ] Who are the users?
- [ ] What are the 5-7 core features?
- [ ] What's the main user journey?

### Page Level
- [ ] Do I have specs for ALL pages?
- [ ] Is the layout structure defined for each page?
- [ ] Are all interactive elements documented?
- [ ] Is navigation flow mapped out?
- [ ] Are loading/error/empty states specified?

### Design Level
- [ ] Do I have exact color codes?
- [ ] Are font families and sizes specified?
- [ ] Is the spacing system defined?
- [ ] Are component variants documented?
- [ ] Are responsive breakpoints clear?

**If you can't check ALL boxes → you're not ready to build.**

---

## Common Planning Mistakes

### Mistake 1: Vague Feature Descriptions
❌ "A dashboard with data"
✅ "A dashboard with: (1) Revenue chart (line graph, last 30 days), (2) Active users count (big number + 7-day trend), (3) Recent transactions table (5 rows, pagination)"

### Mistake 2: Incomplete Page Specs
❌ "Need a contact page"
✅ "Contact page with: Hero section (title + subtitle), Form (name, email, message fields + submit button), Confirmation modal on success, Error states for each field, Footer with social links"

### Mistake 3: No Design System
❌ "Make it look modern"
✅ "Primary: #3B82F6, Secondary: #10B981, BG: #F9FAFB, Text: #1F2937, Font: Inter (headings: 600, body: 400), Spacing: 8px base scale, Border radius: 8px, Shadows: md elevation"

---

## Tool Compatibility

This philosophy applies across all tools:

### Design Kit + AI Builders (v0, Claude, Bolt.new)
- Use design kit templates for 80% planning phase
- Fill docs 03 (visual), 02b (layouts), 04 (interaction)
- Export combined spec as input to AI builder
- Result: Working prototype in minutes

### Figma Make Workflow
- Use ChatGPT for 80% planning (3 steps)
- Paste comprehensive spec into Figma Make
- Result: Complete app in one prompt

### Figma MCP (Autonomous)
- Agent handles discovery automatically
- You provide: High-level concept + design preferences
- Agent executes planning → building → testing
- Result: Autonomous implementation

**All benefit from upfront thoroughness.**

---

## ROI Analysis

**10-hour project example:**

### Without Planning-First
```
1 hour   - Rough planning
2 hours  - Initial build
7 hours  - Iteration hell (fixing architecture, missing specs, design inconsistencies)
---
Result: Barely functional, likely needs rebuild
```

### With Planning-First
```
8 hours  - Comprehensive planning
30 mins  - One-shot generation
1.5 hours - Minor refinements
---
Result: Production-ready, maintainable, complete
```

**Planning-first costs LESS time and produces BETTER results.**

---

## Integration with Design Kit

The design kit templates are designed to support this philosophy:

**Design Kit Docs = Planning Artifacts**

| Design Kit Doc | Planning Phase | Time Investment |
|----------------|----------------|-----------------|
| 01-design-philosophy.md | Context setting | 10% |
| 02b-page-layouts.md | Page architectures | 30% |
| 03-visual-design-requirements.md | Design system | 25% |
| 04-interaction-design.md | Interactive specs | 20% |
| 05-implementation-guidelines.md | Tech constraints | 15% |

**Total: ~80% of project time**

Then export docs 03 + 02b + 04 → AI builder → 5% build time.

---

## Key Insights

1. **"Plan well, build once"** beats "build fast, iterate forever"
2. **Comprehensive specs = shorter timelines** (counterintuitive but proven)
3. **Gaps in planning = exponential iteration costs**
4. **Document everything before building anything**
5. **AI tools are incredibly good at execution, weak at planning** - do the planning yourself

---

## Further Reading

- **Figma Make Workflow**: `workflows/figma-make/WORKFLOW-GUIDE.md` (see "KEY SUCCESS FACTORS" section)
- **Engineering Practices**: `workflows/ENGINEERING-BEST-PRACTICES.md`
- **Workflow Selection**: `workflows/WORKFLOW-SELECTION-GUIDE.md`

---

**Last Updated**: 2025-10-27
**Status**: Battle-Tested Wisdom
