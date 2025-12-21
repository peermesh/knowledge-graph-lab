# Knowledge Graph Lab UI - Phase 6 Complete

A beautifully designed research knowledge management prototype with editorial magazine aesthetics.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server  
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

Visit http://localhost:5173 to see the app.

## Features

### 🎨 Editorial Design
- Warm paper tones with cream/beige backgrounds
- Fraunces display font for headings
- Source Sans 3 for body text  
- Deep teal (ink-600) accent color
- Amber highlights for important elements
- Subtle paper texture throughout

### 🔄 Three-Mode Navigation
1. **Discover** - Research feed with AI suggestions
2. **Organize** - Hierarchical domain management
3. **Publish** - Review and approve publications

### ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `1` | Go to Discover mode |
| `2` | Go to Organize mode |
| `3` | Go to Publish mode |
| `N` | New domain (Organize) |
| `Enter` | Approve publication (Publish) |
| `Backspace` | Skip publication (Publish) |

Press `?` button (bottom-right on desktop) to view shortcuts anytime.

### 💾 State Management

All data persists to localStorage:
- User preferences
- Domain structure
- Onboarding completion
- Destination settings

State survives page refreshes.

## Phase 6 Highlights

### Cross-Mode Integration
- Assign findings to domains from Discover mode
- Clickable domain tags navigate to Organize
- Real-time count updates
- Toast notifications for feedback

### Empty States
- Discover: "Your research stream awaits"
- Organize: "Create your first domain"
- Publish: "All caught up!"

### Loading States
- Skeleton loaders for cards
- Pulse animations
- Smooth transitions

### Accessibility
- Full keyboard navigation
- ARIA labels on all buttons
- Focus-visible states
- Screen reader friendly
- WCAG AA contrast

## Technologies

- React 19.2.0
- TypeScript 5.9.3
- Vite 7.3.0
- Tailwind CSS 4.1.18
- React Router 7.11.0

## Documentation

See `PHASE_6_COMPLETION.md` for detailed implementation notes.

## Build Info

**Production Build:**
- JavaScript: 338 KB (102 KB gzipped)
- CSS: 22 KB (4.4 KB gzipped)
- Build time: ~1.5 seconds
- Zero TypeScript errors ✅

## License

Prototype for demonstration purposes.
