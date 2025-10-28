# ContextPanel Component

## Overview

The `ContextPanel` component provides dynamic, page-specific contextual information and controls in the right panel of the three-panel layout. It automatically adapts its content based on the current route.

## Features

### Page-Specific Content

The ContextPanel displays different content based on the current page:

#### Feed Page (`/feed`)
- **Topic Filters**: Checkboxes for filtering by topics (AI, Machine Learning, Creator Economy, etc.)
- **Date Range Filters**: Radio buttons for selecting time periods (Last 7/30/90 days, Custom)
- **Quality Score Sliders**: Adjust minimum quality and relevance scores
- **Content Type Filters**: Filter by article, insight, report, news, research paper
- **Action Buttons**: Apply filters, reset all

#### Graph Lab Page (`/lab`)
- **Graph Statistics**: Display total nodes, edges, and selected items
- **Selected Node Details**: 
  - Node name, type, and confidence score
  - Extraction method
  - Metadata information
- **Node Type Filter**: Radio buttons to filter by entity type (Person, Organization, Location, Concept)
- **Relationship Controls**: Toggle edge labels, highlight connections, cluster by type
- **Export Options**: Export graph as JSON, CSV, or PNG

#### Settings Page (`/settings`)
- **Help & Tips**: Quick tips for using settings effectively
- **Keyboard Shortcuts**: Common shortcuts reference
- **Recent Changes**: Timestamp of last settings update
- **Documentation Link**: Quick access to full documentation

#### Default/Other Pages
- Displays a placeholder message prompting users to navigate to a specific page

## Usage

The ContextPanel is automatically integrated into the `ThreePanelLayout` component:

```tsx
import { ContextPanel } from './ContextPanel'

// In ThreePanelLayout
<ResizablePanel
  defaultWidth={320}
  minWidth={200}
  maxWidth={500}
  side="right"
  className="border-l border-border bg-card"
>
  <ContextPanel />
</ResizablePanel>
```

## Implementation Details

### Route Detection

The component uses React Router's `useLocation()` hook to determine the current page:

```tsx
const location = useLocation()

switch (location.pathname) {
  case '/feed':
    return <FeedContext />
  case '/lab':
    return <GraphLabContext />
  case '/settings':
    return <SettingsContext />
  default:
    return <DefaultContext />
}
```

### State Management

The component integrates with Zustand stores:
- `useGraphStore()`: Access graph entities, relationships, and selected nodes
- Can be extended to use `useUserStore()` or `useUIStore()` as needed

### Styling

- Uses Tailwind CSS for consistent styling
- Follows the design system's card/muted patterns
- Responsive and scrollable for long content
- Icons from `lucide-react`

## Future Enhancements

1. **Interactive Filters**: Connect filter controls to actual state management and API calls
2. **Real-time Updates**: Add WebSocket support for live graph statistics
3. **Saved Filter Presets**: Allow users to save and load filter configurations
4. **Context History**: Track and display recently viewed nodes/items
5. **Custom Widgets**: Allow users to add custom widgets to the context panel
6. **Keyboard Navigation**: Add keyboard shortcuts for common actions
7. **Export Preferences**: Remember user's preferred export format

## Related Components

- `ThreePanelLayout`: Parent layout component
- `ResizablePanel`: Provides resize functionality for the context panel
- `FeedPage`, `GraphLabPage`, `SettingsPage`: Pages that use the context panel

## Data Flow

```
Route Change
    ↓
useLocation() detects new path
    ↓
ContextPanel renders appropriate context
    ↓
Context component reads from Zustand stores
    ↓
User interacts with controls
    ↓
Actions dispatch to stores/API
    ↓
UI updates reflect changes
```

## Testing Considerations

When testing the ContextPanel:
1. Mock `useLocation()` to test different routes
2. Mock Zustand stores for graph data
3. Test filter interactions and state updates
4. Verify accessibility (keyboard navigation, ARIA labels)
5. Test responsive behavior with different panel widths

## Performance Notes

- Context switching is lightweight (no heavy re-renders)
- Graph statistics update reactively via Zustand
- Consider virtualizing long lists of filters if performance becomes an issue
- Export actions should be async with loading states

