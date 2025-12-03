# Figma Make Workflow

# 🎯 THE ACTUAL WORKFLOW

```
ChatGPT (Planning) → Figma Make (One Prompt) → Done ✅

```

**That's it.** If you plan well, Figma Make builds everything correctly in one shot.

---

## 📌 STANDARD FIGMA MAKE PROMPT PREFIX

**Use this at the START of every Figma Make prompt:**

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

## PHASE 1: PLANNING (ChatGPT)

### Step 1: Get Complete App Overview

```
Based on our entire conversation about my app idea, please provide:

1. **App Type & Purpose**: What kind of app is this? What problem does it solve?
2. **Core Features**: List the 5-7 main features/functionalities
3. **User Flow**: Describe the main user journey from start to finish
4. **Page Structure**: Break down the app into distinct pages/screens and list them with a 1-sentence description of each

Format this as a structured document I can reference.

```

---

### Step 2: Define All Page Architectures

```
For ALL pages you identified, create detailed breakdowns:

For EACH page, provide:
- **Page Name**:
- **Purpose**: What does this page accomplish?
- **Layout Structure**: (e.g., "header, left sidebar, main content area, right panel, footer")
- **Key Components**: List the main UI components needed (forms, cards, lists, modals, etc.)
- **Interactive Elements**: What can users do on this page?
- **Navigation**: How do users get to/from this page?
- **Content**: What specific text, data, and images should appear?
- **States**: What loading, error, or empty states are needed?

Be as detailed as possible. Do this for ALL pages in one comprehensive document.

```

---

### Step 3: Create Complete Design System

```
Create a comprehensive design guide for my app that includes:

**1. Color Palette**
- Primary color (with hex code)
- Secondary color (with hex code)
- Accent color (with hex code)
- Background colors (light/dark modes if applicable)
- Text colors (primary, secondary, disabled)
- Status colors (success, error, warning, info)

**2. Typography**
- Font families (heading, body, monospace if needed)
- Font sizes (h1, h2, h3, body, small, etc.)
- Font weights (regular, medium, bold)
- Line heights

**3. Spacing System**
- Define spacing scale (e.g., 4px base: xs=4px, sm=8px, md=16px, lg=24px, xl=32px, etc.)

**4. Component Styles**
- Button styles (primary, secondary, ghost, sizes)
- Input field styles
- Card styles
- Border radius standards
- Shadow/elevation levels

**5. Layout Grid**
- Container max-width
- Grid columns
- Gutter sizes
- Responsive breakpoints

Make this design guide consistent with modern UI/UX best practices and suitable for [describe your app type/industry].

```

---

## PHASE 2: BUILD ENTIRE APP (Figma Make)

### The One Prompt To Rule Them All

```
Build this following engineering best practices:
- Write all code to WCAG AA accessibility standards
- Create and use reusable components throughout
- Use semantic HTML and proper component architecture
- Avoid absolute positioning; use flexbox/grid layouts
- Build actual code components, not image SVGs
- Keep code clean, maintainable, and well-structured

I need you to build a complete application. Here's everything:

**PROJECT OVERVIEW:**
[PASTE APP OVERVIEW FROM CHATGPT - Step 1]

**ALL PAGES & DETAILED SPECIFICATIONS:**
[PASTE ALL PAGE ARCHITECTURES FROM CHATGPT - Step 2]

**DESIGN SYSTEM:**
[PASTE COMPLETE DESIGN GUIDE FROM CHATGPT - Step 3]

Build out all pages as separate page components with full functionality, content, and styling according to the design system. Make this a complete, working prototype.

```

**Result**: You get a complete, functional app. Done. ✅

---

## OPTIONAL: MINOR TWEAKS (If Needed)

If something needs adjustment, use targeted prompts:

### Design Adjustment

```
Build this following engineering best practices:
- Write all code to WCAG AA accessibility standards
- Create and use reusable components throughout
- Use semantic HTML and proper component architecture
- Avoid absolute positioning; use flexbox/grid layouts
- Build actual code components, not image SVGs
- Keep code clean, maintainable, and well-structured

On [PAGE NAME], change [specific element] to [desired state].

```

### Functionality Update

```
Build this following engineering best practices:
- Write all code to WCAG AA accessibility standards
- Create and use reusable components throughout
- Use semantic HTML and proper component architecture
- Avoid absolute positioning; use flexbox/grid layouts
- Build actual code components, not image SVGs
- Keep code clean, maintainable, and well-structured

On [PAGE NAME], add this interaction: [describe what should happen].

```

### Content Change

```
Build this following engineering best practices:
- Write all code to WCAG AA accessibility standards
- Create and use reusable components throughout
- Use semantic HTML and proper component architecture
- Avoid absolute positioning; use flexbox/grid layouts
- Build actual code components, not image SVGs
- Keep code clean, maintainable, and well-structured

On [PAGE NAME], update the copy/content: [specific changes].

```

---

## ✅ SIMPLE CHECKLIST

- [ ]  ChatGPT: Get app overview (Step 1)
- [ ]  ChatGPT: Get all page details (Step 2)
- [ ]  ChatGPT: Create design system (Step 3)
- [ ]  Figma Make: Build entire app with one prompt
- [ ]  (Optional) Make minor tweaks if needed
- [ ]  Done! 🎉

---

## 💡 KEY SUCCESS FACTORS

**The secret to getting it right in one shot:**

1. **Be thorough in planning** - The more detail you give ChatGPT, the better Figma Make builds it
2. **Include everything in Step 2** - Don't leave gaps. Specify content, interactions, states, etc.
3. **Define a complete design system** - Colors, fonts, spacing, components - everything
4. **Copy-paste accurately** - Make sure you give Figma Make all the info from ChatGPT
5. **Use the prefix** - Always include the engineering best practices prefix

**Time breakdown:**

- 80% Planning with ChatGPT
- 5% Building with Figma Make
- 15% Minor tweaks (maybe)

**The better you plan, the less you iterate.** That's the whole game.

---

## 🚨 TROUBLESHOOTING

### If you get messy code:

```
Rebuild this using proper component architecture:
- Break into separate page files
- Use flexbox/grid (no absolute positioning)
- Create reusable components
- No image exports - actual code components only

```

### If the design is off:

Make sure your design guide in Step 3 was detailed enough. If not, add more specifics and regenerate.

### If functionality is missing:

Make sure you specified interactions and behaviors in Step 2. If not, add them and regenerate that section.

---

**Remember**: The prefix goes at the start of EVERY Figma Make prompt!