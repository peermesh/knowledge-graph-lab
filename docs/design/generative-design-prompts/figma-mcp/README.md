# Figma MCP Workflow

**Autonomous agent builds complete application from Figma design**

---

## Quick Overview

This workflow uses an autonomous agent with Figma MCP integration to discover, plan, and implement a complete application from a Figma file.

**Time**: 1-3 hours (mostly agent autonomous work)
**Your involvement**: 15 minutes (provide URL, review output)
**Output**: Complete HTML/CSS application with navigation and assets

---

## Autonomous Execution

The agent handles everything:

```
✅ Discovers all pages from Figma
✅ Captures screenshots for reference
✅ Downloads all images and icons
✅ Creates implementation plan
✅ Builds HTML/CSS autonomously
✅ Implements navigation flow
✅ Tests complete user journey
```

You just provide the Figma URL and review the finished product.

---

## Workflow Overview

### Phase 1: Discovery & Planning (Agent)

**Agent automatically:**
1. Gets page structure from Figma (node 0:1)
2. Captures screenshots of all screens
3. Analyzes and categorizes (actual pages vs promotional material)
4. Identifies entry point (Home/Landing/Onboarding page)
5. Creates `page-links.md` with all Figma URLs
6. (Optional) Creates `design-guide.md` if >10 pages

### Phase 2: Implementation Planning (Agent)

**Agent creates task list:**
- Project structure setup
- Download all assets from Figma
- Global styles with design tokens
- Reusable components (header, footer, buttons, cards)
- Individual pages (referencing page-links.md)
- Testing and validation

### Phase 3: Autonomous Execution (Agent)

**Agent implements:**
- Clean HTML5 semantic structure
- Organized CSS (reset, variables, global, components, pages)
- Downloaded images and SVG icons from Figma
- Responsive layouts (mobile-first)
- Complete navigation flow
- Hover and focus states

### Phase 4: Quality Assurance (Agent)

**Agent verifies:**
- All pages implemented
- Navigation links work
- Images load correctly
- Responsive on all screen sizes
- HTML validation passes
- Accessibility standards met

---

## Prerequisites

**Required:**
- Figma file URL with node IDs
- Figma MCP server configured in Claude Code
- Image download enabled in Figma MCP settings

**Setup:**
1. Open Figma Desktop app
2. Preferences → MCP Server Settings
3. Enable "Download" option for images
4. Restart Claude Code to load MCP server

---

## How to Start

**Simple command:**
```
"Build this Figma design: [FIGMA_URL]"
```

**Agent responds:**
```
"Starting Figma to HTML implementation.
Running get_metadata on node 0:1 to discover all pages..."
```

Then sits back and watches the agent work autonomously.

---

## Key Features

### Automatic Asset Management
- Downloads ALL images from Figma
- Saves to `/assets/images/` with descriptive names
- Converts icons to SVG files
- Preserves image quality and formats
- Proper alt text for accessibility

### Smart Page Recognition
- Distinguishes actual pages from promotional material
- Identifies entry point (index.html)
- Maps navigation flow
- Excludes social media graphics, app store assets

### Navigation Flow
- Implements working links between all pages
- Header/footer consistent across pages
- Buttons and CTAs connect to correct targets
- User can navigate complete app flow

### Component Reusability
- Identifies patterns across pages
- Creates reusable component CSS
- Consistent styling throughout
- Easy to maintain and extend

---

## Agent Workflow Steps

Detailed guide in `AGENT-WORKFLOW.md` includes:

**Phase 1**: Discovery & Planning
- Get page structure, capture screenshots
- Analyze and categorize pages
- Create page-links.md
- Conditional design-guide.md creation

**Phase 2**: Implementation Task Plan
- Uses built-in task tracking
- Setup → Components → Pages → Testing

**Phase 3**: Implementation Rules
- HTML structure standards
- CSS organization
- Image and icon handling
- Component implementation
- Page implementation workflow

**Phase 4**: Execution Order
- Step-by-step autonomous execution

**Phase 5**: Quality Checklist
- Comprehensive validation before completion

**Phase 6**: Launch & Test Flow
- Open index.html and test complete user journey

---

## Pros & Cons

### Pros
- 🚀 Fully autonomous - minimal human intervention
- 🔍 Agent discovers structure automatically
- 🧪 Built-in quality checks and testing
- 📦 Downloads all assets from Figma
- 🔗 Implements complete navigation
- ⏱️ Your time: only 15 minutes

### Cons
- 🤖 Less control over implementation choices
- ⏱️ Longer total execution time (1-3 hours)
- 🔧 Requires MCP server setup
- 🎯 Best for straightforward designs
- 🧠 Complex UX may need human guidance

---

## When to Use This Workflow

✅ **Use Figma MCP if:**
- You have complete Figma designs
- You want minimal human intervention
- You trust the agent to make decisions
- You have MCP server access
- You have 1-3 hours for autonomous execution

❌ **Consider alternatives if:**
- You want complete control → Use Figma Make workflow
- You don't have Figma → Use AI Builders workflow
- You need faster build → Use Figma Make (5 min build after planning)
- You want to review each step → Use AI Builders workflow

---

## Output Structure

```
project/
├── index.html              # Entry point (home/landing page)
├── about.html
├── contact.html
├── [other-pages].html
├── css/
│   ├── reset.css          # CSS reset
│   ├── variables.css      # Design tokens
│   ├── global.css         # Global styles
│   ├── components.css     # Reusable components
│   └── pages/
│       ├── home.css
│       ├── about.css
│       └── contact.css
├── assets/
│   ├── images/            # Downloaded from Figma
│   └── icons/             # SVG icons from Figma
├── page-links.md          # Figma URL reference
└── design-guide.md        # Design system (if >10 pages)
```

---

## Critical Reminders (For Agent)

🖼️ **IMAGES**: Download ALL images and icons from Figma using MCP download feature

📋 **LINKS**: Store all page Figma links in page-links.md

📝 **TASKS**: Use built-in task management system

🎨 **DESIGN GUIDE**: Only create if >10 pages

📱 **RESPONSIVE**: Every page works on mobile, tablet, desktop

🔗 **NAVIGATION**: All pages connected with working links

🏠 **ENTRY POINT**: index.html is the main/home page

🧪 **TEST FLOW**: Open index.html and test complete journey

✅ **AUTONOMOUS**: Complete entire implementation without asking for input

---

## Related Documents

- **Full Agent Workflow**: `AGENT-WORKFLOW.md` (in this directory)
- **Engineering Best Practices**: `../ENGINEERING-BEST-PRACTICES.md`
- **Workflow Selection**: `../WORKFLOW-SELECTION-GUIDE.md`

---

**Last Updated**: 2025-10-27
**Status**: Production Ready
