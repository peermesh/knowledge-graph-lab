# AI Builders Workflow (v0, Claude, Bolt.new)

**Quick prototyping workflow using AI code generators without Figma.**

---

## Overview

This workflow uses design kit templates as input to AI builders like v0, Claude Code, or Bolt.new for rapid prototype generation.

**Time**: 30-90 minutes total
**Output**: Interactive prototype with working components

---

## When to Use This Workflow

- ✅ You DON'T have a Figma design
- ✅ You want to use v0, Claude, or Bolt.new
- ✅ You have 30-60 minutes for design specs
- ✅ You want iterative prototyping
- ✅ You're comfortable with some iteration

---

## Workflow Steps

### Step 1: Create Design Workspace (5 minutes)

```bash
# From project root
.dev/kits/design-kit/scripts/bash/scaffold-workspace.sh \
  "Your Interface Name" workspace-name
```

This creates: `.dev/ux-ui-design/workspace-name/` with all templates.

### Step 2: Fill Design-Focused Templates (30 minutes)

**MUST FILL** (these are your AI builder input):

1. **03-visual-design-requirements.md**
   - Color palette (primary, secondary, accent, backgrounds)
   - Typography (font families, sizes, weights)
   - Spacing scale (4px, 8px, 16px, 24px, 32px)
   - Component styles (buttons, cards, inputs)
   - Border radius, shadows, elevation

2. **02b-page-layouts.md**
   - List all pages/screens
   - For each page: layout structure, components, content sections
   - Navigation flow between pages
   - Responsive behavior (mobile, tablet, desktop)

3. **04-interaction-design.md**
   - Interactive elements (buttons, forms, modals)
   - User actions and system responses
   - Loading states, error states, empty states
   - Animations and transitions
   - Form validation

**SKIP** (causes tech stack conflicts):
- ❌ `05-implementation-guidelines.md` - Let AI builder choose the tech stack

**OPTIONAL** (provide context but not required):
- `01-design-philosophy.md` - Overall principles and goals
- `03a-component-specifications.md` - Detailed component breakdown

### Step 3: Prepare AI Builder Prompt (5 minutes)

Combine these elements:

```
[Engineering Best Practices Prefix from workflows/ENGINEERING-BEST-PRACTICES.md]

PROJECT SPECIFICATIONS:
[Paste relevant sections from 03-visual-design-requirements.md]

PAGE LAYOUTS:
[Paste page specifications from 02b-page-layouts.md]

INTERACTIONS:
[Paste key interactions from 04-interaction-design.md]

Build a complete, working prototype with all pages connected via navigation.
```

### Step 4: Submit to AI Builder (5-15 minutes)

**v0.dev**:
1. Go to v0.dev
2. Paste your combined prompt
3. Wait for generation
4. Preview and iterate

**Claude (Code Mode)**:
1. Start Claude Code session
2. Paste your combined prompt
3. Claude builds component files
4. Test in browser

**Bolt.new**:
1. Go to bolt.new
2. Paste your combined prompt
3. Instant preview generated
4. Iterate with additional prompts

### Step 5: Iterate and Refine (30-60 minutes)

**Typical iterations:**
- Adjust colors: "Change primary color to #3B82F6"
- Fix layout: "Make the hero section full-width with centered content"
- Add interactions: "Add hover effect to cards"
- Update content: "Change the headline to..."
- Mobile fixes: "Stack navigation vertically on mobile"

**Best practices:**
- Make ONE change at a time
- Be specific about what element to change
- Reference page names clearly
- Test each change before moving on

---

## Tips for Success

### Make Specifications Precise

❌ **Vague**: "Use a nice blue color"
✅ **Precise**: "Primary color: #3B82F6 (blue-500)"

❌ **Vague**: "Add some padding"
✅ **Precise**: "Padding: 24px vertical, 16px horizontal"

❌ **Vague**: "Make it responsive"
✅ **Precise**: "Mobile (<640px): Stack vertically, single column. Desktop (>1024px): 3-column grid with 24px gaps"

### Start Simple, Add Complexity

1. **First prompt**: Basic structure, layout, colors
2. **Second prompt**: Add components, refine spacing
3. **Third prompt**: Add interactions, states, animations

Better to iterate than to overload one prompt.

### Use Engineering Best Practices Prefix

**ALWAYS** start your prompt with the prefix from `workflows/ENGINEERING-BEST-PRACTICES.md`:

```
Build this following engineering best practices:
- Write all code to WCAG AA accessibility standards
- Create and use reusable components throughout
- Use semantic HTML and proper component architecture
- Avoid absolute positioning; use flexbox/grid layouts
- Build actual code components, not image SVGs
- Keep code clean, maintainable, and well-structured
```

This ensures quality output from the start.

---

## Tool-Specific Guidance

### v0.dev

**Strengths:**
- React + Tailwind CSS (production-ready stack)
- Instant preview with hot reload
- Component isolation
- Easy to iterate

**Limitations:**
- Limited to React ecosystem
- Requires Next.js knowledge for advanced features

**Best for**: Modern React apps, component libraries

### Claude Code

**Strengths:**
- Can use any tech stack
- Full project scaffolding
- Understands complex architectures
- Can read existing codebases

**Limitations:**
- Requires local development environment
- More manual testing needed

**Best for**: Custom tech stacks, integration with existing projects

### Bolt.new

**Strengths:**
- Instant full-stack prototypes
- Supports multiple frameworks
- Built-in preview environment
- No local setup needed

**Limitations:**
- Less control over tech stack choices
- Cloud-only development

**Best for**: Quick demos, client presentations, MVPs

---

## Example: Contact Page Specification

### Input to AI Builder

```
Build this following engineering best practices:
- Write all code to WCAG AA accessibility standards
- Create and use reusable components throughout
- Use semantic HTML and proper component architecture
- Avoid absolute positioning; use flexbox/grid layouts
- Build actual code components, not image SVGs
- Keep code clean, maintainable, and well-structured

VISUAL DESIGN:
- Primary color: #3B82F6 (blue-600)
- Secondary color: #10B981 (green-500)
- Background: #F9FAFB (gray-50)
- Text: #1F2937 (gray-800)
- Font: Inter (headings: 600, body: 400)
- Spacing scale: 8px base (sm: 8px, md: 16px, lg: 24px, xl: 32px)
- Border radius: 8px
- Shadow: 0 1px 3px rgba(0,0,0,0.1)

PAGE LAYOUT (Contact Page):
- Header: Logo (left) + Navigation links (center) + CTA button (right)
- Hero section: Centered headline + subtitle
- Contact form: Name, Email, Message fields + Submit button
- Info section: Address, Phone, Email in 3-column grid
- Footer: Logo + Links + Social icons + Copyright

INTERACTIONS:
- Form validation: Show error below field on blur
- Submit button: Disabled state while submitting, success message on completion
- Hover states: Buttons lift slightly (transform: translateY(-2px))
- Focus states: Blue outline on all interactive elements

Build a complete Contact page with all elements functional.
```

### Expected Output

- Fully styled Contact page
- Working form with validation
- Responsive layout (mobile-first)
- Hover and focus states
- Clean, maintainable code

### Iterations

If something's off:
```
"Make the hero section background gradient from blue to purple"
"Add a phone icon next to the phone number"
"Change form button to green (#10B981)"
```

---

## Quality Checklist

Before considering the prototype complete:

- [ ] All pages specified in 02b-page-layouts.md are implemented
- [ ] Colors match 03-visual-design-requirements.md exactly
- [ ] Typography follows specified system
- [ ] Spacing is consistent throughout
- [ ] Components are reusable (not copy-pasted)
- [ ] Navigation works between all pages
- [ ] Interactive elements have hover/focus states
- [ ] Form validation works (if applicable)
- [ ] Responsive on mobile, tablet, desktop
- [ ] No accessibility warnings in browser console
- [ ] Code is clean and readable

---

## Troubleshooting

### "Output doesn't match my design specs"

→ Be more specific in your prompt. Include exact hex codes, pixel values, and layout descriptions.

### "Colors look wrong"

→ Always use hex codes, not color names. "Blue" is ambiguous, "#3B82F6" is precise.

### "Layout breaks on mobile"

→ Add explicit mobile specs: "On mobile (<640px): Stack all columns vertically, full-width components"

### "Components aren't reusable"

→ Explicitly request: "Create a reusable Button component with variants (primary, secondary, outline)"

### "Generated code uses weird tech stack"

→ Specify upfront: "Build using React + Tailwind CSS" or "Use vanilla HTML/CSS/JavaScript"

### "Missing interactions"

→ Review 04-interaction-design.md - ensure all interactions are documented clearly

---

## Related Documents

- **Engineering Best Practices**: `../ENGINEERING-BEST-PRACTICES.md`
- **Planning Philosophy**: `../PLANNING-FIRST-PHILOSOPHY.md`
- **Workflow Selection**: `../WORKFLOW-SELECTION-GUIDE.md`
- **Design Kit Main Guide**: `../../USAGE-WITH-AI-BUILDERS.md`

---

## Next Steps After Prototype

Once you have a working prototype:

1. **User Testing**: Get feedback on usability and design
2. **Refinement**: Iterate based on feedback
3. **Production Planning**: Create implementation work order
4. **Handoff**: Export specs + prototype for development team

Or continue to production implementation with chosen tech stack.

---

**Last Updated**: 2025-10-27
**Status**: Production Ready
