# Iteration 1: Modern Research Platform - Design Specifications

**Design Philosophy:** Sophisticated, professional, and data-driven with elevated visual design

---

## 🎨 Color Palette

### Primary Colors
- **Indigo 500** `#4F46E5` - Main primary color (buttons, links, highlights)
- **Indigo 100** `#E0E7FF` - Light backgrounds, hover states
- **Indigo 700** `#3730A3` - Dark variants, active states

### Accent Colors
- **Teal 500** `#14B8A6` - Accent for success states, highlights, badges
- **Teal 100** `#CCFBF1` - Light accent backgrounds

### Secondary Colors
- **Amber 500** `#F59E0B` - Warm accent for warnings, special highlights
- **Amber 100** `#FEF3C7` - Light warm backgrounds

### Neutral Colors
- **Slate 50** `#F8FAFC` - Page backgrounds
- **Slate 100** `#F1F5F9` - Card backgrounds
- **Slate 200** `#E2E8F0` - Borders
- **Slate 400** `#94A3B8` - Muted text
- **Slate 600** `#475569` - Secondary text
- **Slate 900** `#0F172A` - Primary text

### Semantic Colors
- **Success:** `#10B981` (Green)
- **Warning:** `#F59E0B` (Amber)
- **Error:** `#EF4444` (Red)
- **Info:** `#3B82F6` (Blue)

---

## 📝 Typography

### Font Families
- **Primary:** `Inter` - Clean, modern sans-serif
- **Monospace:** `JetBrains Mono` - For code and technical content

### Font Sizes
```
xs:   12px  (0.75rem)
sm:   14px  (0.875rem)
base: 16px  (1rem)
lg:   18px  (1.125rem)
xl:   20px  (1.25rem)
2xl:  24px  (1.5rem)
3xl:  30px  (1.875rem)
4xl:  36px  (2.25rem)
```

### Font Weights
- **Normal:** 400 - Body text
- **Medium:** 500 - Subtle emphasis
- **Semibold:** 600 - Headings, labels
- **Bold:** 700 - Strong emphasis

### Line Heights
- **Tight:** 1.25 - Headlines
- **Normal:** 1.5 - Body text
- **Relaxed:** 1.75 - Long-form content

---

## 📐 Spacing System

```
xs:   4px   (0.25rem)
sm:   8px   (0.5rem)
md:   16px  (1rem)
lg:   24px  (1.5rem)
xl:   32px  (2rem)
2xl:  48px  (3rem)
3xl:  64px  (4rem)
```

---

## 🔲 Border Radius

```
sm:  6px  (0.375rem) - Small elements, tags
md:  8px  (0.5rem)   - Buttons, inputs
lg:  12px (0.75rem)  - Cards, panels
xl:  16px (1rem)     - Large containers
full: 9999px         - Pills, avatars
```

---

## 💫 Shadows & Elevation

### Card Shadows
```css
sm:  0 1px 2px 0 rgba(0, 0, 0, 0.05)
md:  0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)
lg:  0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)
xl:  0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)
```

### Usage Guidelines
- **sm:** Subtle elevation for inline elements
- **md:** Standard card elevation
- **lg:** Elevated cards, modals
- **xl:** High-priority content, popovers

---

## 🎭 Component Specifications

### Buttons

#### Primary Button
```
Background: Indigo 500 (#4F46E5)
Text: White
Padding: 12px 24px
Border Radius: 8px
Font Weight: 600
Shadow: md
Hover: Indigo 600 (#4338CA) + shadow-lg

transition: all 200ms ease
```

#### Secondary Button
```
Background: Slate 100 (#F1F5F9)
Text: Slate 900 (#0F172A)
Padding: 12px 24px
Border Radius: 8px
Font Weight: 600
Shadow: sm
Hover: Slate 200 (#E2E8F0) + shadow-md
```

#### Ghost Button
```
Background: Transparent
Text: Slate 700 (#334155)
Padding: 12px 24px
Border Radius: 8px
Font Weight: 500
Hover: Slate 100 (#F1F5F9)
```

### Cards

#### Standard Card
```
Background: White
Border: 1px solid Slate 200 (#E2E8F0)
Border Radius: 12px
Padding: 24px
Shadow: md
Hover: shadow-lg (subtle lift effect)
```

#### Research Item Card (Feed)
```
Background: White
Border: 1px solid Slate 200
Border Radius: 12px
Padding: 20px
Shadow: md
Left Border: 4px solid Teal 500 (accent strip)
Hover: shadow-lg + scale(1.01)
```

### Input Fields

```
Background: White
Border: 1px solid Slate 300 (#CBD5E1)
Border Radius: 8px
Padding: 10px 16px
Font Size: 14px
Text Color: Slate 900

Focus:
  Border: 2px solid Indigo 500
  Shadow: 0 0 0 3px rgba(79, 70, 229, 0.1)
  Outline: none
```

### Badges & Tags

#### Entity Tag
```
Background: Slate 100
Text: Slate 700
Padding: 6px 12px
Border Radius: 6px
Font Size: 12px
Font Weight: 500

Hover:
  Background: Slate 200
  cursor: pointer
```

#### Status Badge
```
Success: Teal 100 background, Teal 700 text
Warning: Amber 100 background, Amber 700 text
Error: Red 100 background, Red 700 text
Info: Blue 100 background, Blue 700 text

Padding: 4px 10px
Border Radius: 6px
Font Size: 12px
Font Weight: 600
```

---

## 📄 Page-Specific Guidelines

### Feed Page

**Header**
- Background: White with border-bottom (Slate 200)
- Title: 3xl (30px), Bold, Slate 900
- Subtitle: sm (14px), Slate 600
- Search Bar: Full width input with search icon
- Action Buttons: Primary + Secondary styles

**Research Cards**
- 4px left border accent (Teal 500)
- Quality/Relevance metrics with progress bars
- Entity tags with hover states
- Action buttons (Save, View, Share) - ghost style
- Update timestamp in muted text

**Right Panel (Filters)**
- White background with subtle border
- Section headers with icons
- Checkbox groups with custom styling
- Range sliders with Indigo track
- Apply/Reset buttons at bottom

### Graph Lab Page

**Toolbar**
- Semi-transparent background with backdrop blur
- Icon buttons with tooltips
- Zoom controls grouped
- Active state: Indigo 500 background

**Graph Canvas**
- Background: Gradient from Slate 50 to Slate 100
- Nodes: Colored by type with shadow-md
- Edges: Slate 300 with hover highlight
- Selected state: Indigo 500 border

**Details Panel**
- White card with shadow-lg
- Property list with alternating backgrounds
- Expand/collapse animation
- Relationship list with type badges

### Settings Page

**Section Cards**
- White background, shadow-md
- Header with icon (Indigo 500)
- Form labels: Semibold, Slate 700
- Helper text: sm, Slate 500
- Dividers: Slate 200

**Theme Toggle**
- Button group with border
- Active state: Indigo 500 border + background
- Icons with descriptive labels

**Danger Zone**
- Red 50 background
- Red 200 border
- Red 700 text for title
- Destructive button styling

---

## 🎯 Key Differentiators from TailAdmin

1. **Custom Color Palette** - Indigo/Teal instead of default blue
2. **Enhanced Shadows** - More prominent elevation
3. **Accent Strips** - Left border accents on cards
4. **Refined Spacing** - More generous padding and margins
5. **Gradient Effects** - Subtle gradients on backgrounds
6. **Custom Focus States** - Indigo ring with transparency
7. **Sophisticated Typography** - Inter font with varied weights
8. **Animated Interactions** - Smooth transitions and hover effects

---

## 🚀 Implementation Notes

### CSS Variables (Applied via theme.ts)
```css
:root {
  --v1-primary: #4F46E5;
  --v1-accent: #14B8A6;
  --v1-secondary: #F59E0B;
  /* ... all colors defined */
}
```

### Tailwind Utilities (Primary)
```
bg-[#4F46E5]
text-[#0F172A]
border-[#E2E8F0]
shadow-[0_4px_6px_-1px_rgba(0,0,0,0.1)]
rounded-[12px]
```

### Animation Timing
```
Default: 200ms ease
Hover: 150ms ease
Focus: 100ms ease
Card Lift: 300ms cubic-bezier(0.4, 0, 0.2, 1)
```

---

## 📸 Visual Reference

### Color Swatches
- Primary: ![#4F46E5](https://via.placeholder.com/100x50/4F46E5/FFFFFF?text=Indigo)
- Accent: ![#14B8A6](https://via.placeholder.com/100x50/14B8A6/FFFFFF?text=Teal)
- Secondary: ![#F59E0B](https://via.placeholder.com/100x50/F59E0B/FFFFFF?text=Amber)

---

## ✅ Quality Checklist

- [ ] All colors use defined palette
- [ ] Consistent spacing (8px grid)
- [ ] Shadows used appropriately
- [ ] Typography hierarchy clear
- [ ] Interactive elements have hover/focus states
- [ ] Animations smooth and purposeful
- [ ] Cards have proper elevation
- [ ] Contrast ratios meet WCAG AA (4.5:1 minimum)

---

**Last Updated:** November 3, 2025  
**Status:** Ready for Implementation  
**Designer:** AI Design Iterations System














