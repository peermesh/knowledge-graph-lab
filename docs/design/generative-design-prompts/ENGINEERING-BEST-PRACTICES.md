# Engineering Best Practices - Standard Prefix

**Purpose**: Reusable prompt prefix to ensure high-quality code generation across all AI builder tools (Figma Make, v0, Claude, Bolt.new).

---

## Standard Prefix Template

Use this at the **START** of every prompt to AI builders:

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

## Why This Matters

**Without this prefix:**
- ❌ Messy, hard-to-maintain code
- ❌ Accessibility issues (lawsuits, poor UX)
- ❌ Image-based "fake" components instead of real code
- ❌ Absolute positioning that breaks on different screen sizes
- ❌ Copy-paste spaghetti instead of reusable components

**With this prefix:**
- ✅ Clean, maintainable codebase
- ✅ WCAG AA compliant (legal protection + inclusive design)
- ✅ Real HTML/CSS components (searchable, flexible, performant)
- ✅ Responsive layouts that adapt to any screen size
- ✅ DRY architecture with reusable component library

---

## When to Use

**ALWAYS** use this prefix when:
- Generating code with Figma Make
- Creating prototypes with v0, Claude, or Bolt.new
- Asking AI to build any interface component
- Converting designs to implementation

**Even for quick prototypes** - good practices cost nothing extra and save massive time later.

---

## Tool-Specific Notes

### Figma Make
- Place prefix at the very beginning of your comprehensive prompt
- Include AFTER the prefix: Project overview, all page specs, design system
- See: `workflows/figma-make/WORKFLOW-GUIDE.md`

### Figma MCP (Autonomous Agents)
- Prefix is included in Phase 3 implementation rules
- Agent automatically applies these standards
- See: `workflows/figma-mcp/AGENT-WORKFLOW.md`

### AI Builders (v0, Claude, Bolt.new)
- Prefix works best when combined with design kit specifications
- Provide prefix + design specs from docs 03, 02b, 04
- Skip doc 05 to avoid tech stack conflicts
- See: `USAGE-WITH-AI-BUILDERS.md`

---

## Customization

You can extend this prefix for specific needs:

```
Build this following engineering best practices:
- Write all code to WCAG AA accessibility standards
- Create and use reusable components throughout
- Use semantic HTML and proper component architecture
- Avoid absolute positioning; use flexbox/grid layouts
- Build actual code components, not image SVGs
- Keep code clean, maintainable, and well-structured

ADDITIONAL REQUIREMENTS FOR THIS PROJECT:
- Use TypeScript for type safety
- Follow React 18 best practices
- Implement dark mode support
- Use Tailwind CSS for styling
```

**Golden Rule**: Start with the standard prefix, then add project-specific requirements.

---

## Quality Indicators

After generation, verify the output includes:

- ✅ Semantic HTML tags (header, nav, main, section, article, footer)
- ✅ Component files separated from page files
- ✅ CSS using flexbox/grid (NOT absolute positioning)
- ✅ Accessibility attributes (alt text, ARIA labels, focus states)
- ✅ Reusable component patterns (buttons, cards, forms)
- ✅ Actual HTML/CSS code (NOT <svg> image exports)

If output fails these checks → regenerate with the prefix.

---

## Related Documents

- **Figma Make Workflow**: `workflows/figma-make/WORKFLOW-GUIDE.md`
- **Figma MCP Workflow**: `workflows/figma-mcp/AGENT-WORKFLOW.md`
- **AI Builders Usage**: `USAGE-WITH-AI-BUILDERS.md`
- **Workflow Selection**: `workflows/WORKFLOW-SELECTION-GUIDE.md`

---

**Last Updated**: 2025-10-27
**Status**: Production Ready
