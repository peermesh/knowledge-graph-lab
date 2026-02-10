# WO-COLLECTIONS-005: Presentation Templates - Visual Presets

**Phase:** v1.0
**Priority:** P2 - Enhancement
**Estimated Effort:** 3-4 days
**Dependencies:** WO-COLLECTIONS-002 (Widgets)
**Blocks:** Template marketplace, custom branding

---

## Objective

Create pre-built visual presentation templates that users can apply to collections for instant professional-looking infographics.

---

## Scope

### In Scope
- 6 built-in templates
- Template preview system
- Template application to collections
- Basic customization (colors, fonts)
- Template switching

### Out of Scope
- Custom template builder
- Template sharing/marketplace
- Animation customization

---

## Deliverables

### D1: Template Definition System

**File:** `types/presentationTemplates.ts`

```typescript
export interface PresentationTemplate {
  id: string;
  name: string;
  description: string;
  thumbnail: string;  // Preview image URL
  applicableTypes: CollectionType[];
  layout: LayoutConfig;
  widgets: WidgetPlacement[];
  theme: ThemeConfig;
  isSystem: boolean;
}

export interface LayoutConfig {
  type: 'list' | 'grid' | 'masonry' | 'timeline' | 'radial' | 'flow';
  columns?: number;
  gap: number;
  padding: number;
  headerHeight: number;
}

export interface WidgetPlacement {
  widgetId: string;
  zone: 'header' | 'summary' | 'items' | 'footer' | 'sidebar';
  order: number;
  span?: number;  // Grid column span
}

export interface ThemeConfig {
  colorScheme: 'light' | 'dark' | 'auto';
  primaryColor: string;
  accentColor: string;
  backgroundColor: string;
  fontFamily: string;
  borderRadius: number;
  shadows: 'none' | 'subtle' | 'prominent';
}
```

### D2: Built-in Templates

**File:** `data/presentationTemplates.ts`

```typescript
export const BUILT_IN_TEMPLATES: PresentationTemplate[] = [
  {
    id: 'top-10-listicle',
    name: 'Top 10 Listicle',
    description: 'Clean numbered list with score bars and trends',
    applicableTypes: ['ranking'],
    layout: { type: 'list', gap: 16, padding: 24, headerHeight: 120 },
    widgets: [
      { widgetId: 'collection-header', zone: 'header', order: 0 },
      { widgetId: 'stats-row', zone: 'summary', order: 0 },
      { widgetId: 'ranking-card', zone: 'items', order: 0 },
    ],
    theme: {
      colorScheme: 'light',
      primaryColor: '#3b82f6',
      accentColor: '#10b981',
      backgroundColor: '#ffffff',
      fontFamily: 'Inter',
      borderRadius: 8,
      shadows: 'subtle',
    },
    isSystem: true,
  },
  {
    id: 'comparison-showdown',
    name: 'Comparison Showdown',
    description: 'Side-by-side matrix with dimension scores',
    applicableTypes: ['comparison'],
    layout: { type: 'grid', columns: 3, gap: 24, padding: 24, headerHeight: 100 },
    widgets: [
      { widgetId: 'comparison-header', zone: 'header', order: 0 },
      { widgetId: 'dimension-legend', zone: 'summary', order: 0 },
      { widgetId: 'comparison-card', zone: 'items', order: 0, span: 1 },
    ],
    theme: {
      colorScheme: 'light',
      primaryColor: '#8b5cf6',
      accentColor: '#f59e0b',
      backgroundColor: '#fafafa',
      fontFamily: 'Inter',
      borderRadius: 12,
      shadows: 'prominent',
    },
    isSystem: true,
  },
  {
    id: 'ecosystem-map',
    name: 'Ecosystem Map',
    description: 'Radial diagram showing tool connections',
    applicableTypes: ['ecosystem'],
    layout: { type: 'radial', gap: 0, padding: 48, headerHeight: 80 },
    widgets: [
      { widgetId: 'ecosystem-title', zone: 'header', order: 0 },
      { widgetId: 'category-legend', zone: 'sidebar', order: 0 },
      { widgetId: 'ecosystem-node', zone: 'items', order: 0 },
      { widgetId: 'integration-lines', zone: 'items', order: 1 },
    ],
    theme: {
      colorScheme: 'dark',
      primaryColor: '#06b6d4',
      accentColor: '#f472b6',
      backgroundColor: '#0f172a',
      fontFamily: 'JetBrains Mono',
      borderRadius: 50,
      shadows: 'none',
    },
    isSystem: true,
  },
  {
    id: 'timeline-story',
    name: 'Timeline Story',
    description: 'Horizontal scrolling timeline with events',
    applicableTypes: ['timeline'],
    layout: { type: 'timeline', gap: 32, padding: 24, headerHeight: 100 },
    widgets: [
      { widgetId: 'timeline-header', zone: 'header', order: 0 },
      { widgetId: 'timeline-event', zone: 'items', order: 0 },
      { widgetId: 'timeline-connector', zone: 'items', order: 1 },
    ],
    theme: {
      colorScheme: 'light',
      primaryColor: '#f97316',
      accentColor: '#3b82f6',
      backgroundColor: '#fffbeb',
      fontFamily: 'Georgia',
      borderRadius: 4,
      shadows: 'subtle',
    },
    isSystem: true,
  },
  {
    id: 'network-graph',
    name: 'Network Graph',
    description: 'Force-directed graph of people/entities',
    applicableTypes: ['network'],
    layout: { type: 'radial', gap: 0, padding: 32, headerHeight: 60 },
    widgets: [
      { widgetId: 'network-title', zone: 'header', order: 0 },
      { widgetId: 'network-node', zone: 'items', order: 0 },
      { widgetId: 'relationship-edge', zone: 'items', order: 1 },
      { widgetId: 'influence-legend', zone: 'sidebar', order: 0 },
    ],
    theme: {
      colorScheme: 'dark',
      primaryColor: '#a855f7',
      accentColor: '#22d3ee',
      backgroundColor: '#18181b',
      fontFamily: 'Inter',
      borderRadius: 99,
      shadows: 'none',
    },
    isSystem: true,
  },
  {
    id: 'minimal-cards',
    name: 'Minimal Cards',
    description: 'Clean, simple card grid for any collection',
    applicableTypes: ['*'],  // Universal
    layout: { type: 'grid', columns: 2, gap: 16, padding: 16, headerHeight: 80 },
    widgets: [
      { widgetId: 'minimal-header', zone: 'header', order: 0 },
      { widgetId: 'minimal-card', zone: 'items', order: 0 },
    ],
    theme: {
      colorScheme: 'auto',
      primaryColor: '#64748b',
      accentColor: '#64748b',
      backgroundColor: 'transparent',
      fontFamily: 'system-ui',
      borderRadius: 6,
      shadows: 'subtle',
    },
    isSystem: true,
  },
];
```

### D3: Template Renderer

**File:** `components/collections/TemplateRenderer.tsx`

```tsx
export function TemplateRenderer({
  collection,
  template,
  customTheme,
}: Props) {
  const theme = { ...template.theme, ...customTheme };

  return (
    <ThemeProvider theme={theme}>
      <TemplateContainer layout={template.layout}>
        {/* Header Zone */}
        <Zone name="header">
          {template.widgets
            .filter(w => w.zone === 'header')
            .sort((a, b) => a.order - b.order)
            .map(w => renderWidget(w.widgetId, collection, theme))}
        </Zone>

        {/* Summary Zone */}
        <Zone name="summary">
          {template.widgets
            .filter(w => w.zone === 'summary')
            .map(w => renderWidget(w.widgetId, collection, theme))}
        </Zone>

        {/* Items Zone */}
        <ItemsGrid layout={template.layout}>
          {collection.items.map(item => (
            template.widgets
              .filter(w => w.zone === 'items')
              .map(w => renderWidget(w.widgetId, item, theme, w.span))
          ))}
        </ItemsGrid>

        {/* Sidebar Zone (if applicable) */}
        {template.widgets.some(w => w.zone === 'sidebar') && (
          <Sidebar>
            {template.widgets
              .filter(w => w.zone === 'sidebar')
              .map(w => renderWidget(w.widgetId, collection, theme))}
          </Sidebar>
        )}
      </TemplateContainer>
    </ThemeProvider>
  );
}
```

### D4: Template Picker UI

**File:** `components/collections/TemplatePicker.tsx`

```tsx
export function TemplatePicker({
  collection,
  currentTemplateId,
  onSelect,
}: Props) {
  const applicableTemplates = BUILT_IN_TEMPLATES.filter(
    t => t.applicableTypes.includes(collection.type) ||
         t.applicableTypes.includes('*')
  );

  return (
    <div className="template-picker">
      <h3>Choose Presentation</h3>
      <div className="template-grid">
        {applicableTemplates.map(template => (
          <TemplateCard
            key={template.id}
            template={template}
            isSelected={template.id === currentTemplateId}
            onClick={() => onSelect(template.id)}
          >
            <img src={template.thumbnail} alt={template.name} />
            <span>{template.name}</span>
            <span className="description">{template.description}</span>
          </TemplateCard>
        ))}
      </div>
    </div>
  );
}
```

### D5: Theme Customizer

**File:** `components/collections/ThemeCustomizer.tsx`

```tsx
export function ThemeCustomizer({
  baseTheme,
  customizations,
  onChange,
}: Props) {
  return (
    <div className="theme-customizer">
      <ColorPicker
        label="Primary Color"
        value={customizations.primaryColor || baseTheme.primaryColor}
        onChange={color => onChange({ ...customizations, primaryColor: color })}
      />
      <ColorPicker
        label="Accent Color"
        value={customizations.accentColor || baseTheme.accentColor}
        onChange={color => onChange({ ...customizations, accentColor: color })}
      />
      <Select
        label="Color Scheme"
        value={customizations.colorScheme || baseTheme.colorScheme}
        options={['light', 'dark', 'auto']}
        onChange={scheme => onChange({ ...customizations, colorScheme: scheme })}
      />
      <FontPicker
        label="Font"
        value={customizations.fontFamily || baseTheme.fontFamily}
        onChange={font => onChange({ ...customizations, fontFamily: font })}
      />
    </div>
  );
}
```

---

## Visual Reference

```
Template Picker:
┌─────────────────────────────────────────────────────────┐
│ Choose Presentation                                      │
├─────────────────────────────────────────────────────────┤
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
│ │ ▓▓▓▓▓▓▓▓▓▓▓▓ │ │ ░░▓░░▓░░▓░░ │ │    ◉         │     │
│ │ ▓ 1. Item   ▓ │ │ ▓▓▓ ▓▓▓ ▓▓▓ │ │  ◉   ◉      │     │
│ │ ▓ 2. Item   ▓ │ │ ░░░ ░░░ ░░░ │ │ ◉  ◉  ◉     │     │
│ │ ▓ 3. Item   ▓ │ │ ▓▓▓ ▓▓▓ ▓▓▓ │ │    ◉         │     │
│ │              │ │              │ │              │     │
│ │ Top 10      │ │ Comparison   │ │ Ecosystem    │     │
│ │ Listicle    │ │ Showdown     │ │ Map          │     │
│ └──────────────┘ └──────────────┘ └──────────────┘     │
│       ✓ Selected                                        │
└─────────────────────────────────────────────────────────┘
```

---

## Acceptance Criteria

- [ ] All 6 templates render correctly
- [ ] Template picker shows only applicable templates
- [ ] Selected template persists on collection
- [ ] Theme customization works (colors, fonts)
- [ ] Templates respond to data changes
- [ ] Mobile-responsive layouts
- [ ] Template switching is instant (no reload)

---

## Next Work Order

→ **WO-COLLECTIONS-006: Faceted Index - Master Navigation**
