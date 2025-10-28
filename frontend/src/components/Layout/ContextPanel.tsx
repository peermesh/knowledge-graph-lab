import { useLocation } from 'react-router-dom'
import {
  Filter,
  Calendar,
  Tag,
  TrendingUp,
  Info,
  Settings as SettingsIcon,
  HelpCircle,
  Network,
  Layers,
  Clock,
} from 'lucide-react'

import { Button } from '@/components/Common/Button'
import { Input } from '@/components/Common/Input'
import { useGraphStore } from '@/store/useGraphStore'

interface ContextPanelProps {
  className?: string
}

export function ContextPanel({ className = '' }: ContextPanelProps) {
  const location = useLocation()
  const { entities, relationships, selectedEntityIds } = useGraphStore()

  // Determine which context to show based on the current route
  const renderContent = () => {
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
  }

  return (
    <div className={`h-full flex flex-col ${className}`}>
      {renderContent()}
    </div>
  )
}

// Feed page context panel
function FeedContext() {
  return (
    <div className="h-full overflow-auto">
      <div className="p-4 border-b border-border">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Filter className="w-5 h-5" />
          Filters & Refinement
        </h3>
        <p className="text-sm text-muted-foreground mt-1">
          Fine-tune your research feed
        </p>
      </div>

      <div className="p-4 space-y-6">
        {/* Topic Filters */}
        <section>
          <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <Tag className="w-4 h-4" />
            Topics
          </h4>
          <div className="space-y-2">
            {['AI', 'Machine Learning', 'Creator Economy', 'Investment', 'NLP'].map((topic) => (
              <label key={topic} className="flex items-center gap-2 text-sm cursor-pointer hover:bg-muted/50 p-2 rounded">
                <input
                  type="checkbox"
                  className="rounded border-border"
                  defaultChecked={topic === 'AI' || topic === 'Machine Learning'}
                />
                <span>{topic}</span>
              </label>
            ))}
          </div>
          <Button variant="ghost" size="sm" className="mt-2 w-full text-xs">
            + Add Topic
          </Button>
        </section>

        {/* Date Range */}
        <section>
          <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            Date Range
          </h4>
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm cursor-pointer hover:bg-muted/50 p-2 rounded">
              <input type="radio" name="dateRange" className="border-border" defaultChecked />
              <span>Last 7 days</span>
            </label>
            <label className="flex items-center gap-2 text-sm cursor-pointer hover:bg-muted/50 p-2 rounded">
              <input type="radio" name="dateRange" className="border-border" />
              <span>Last 30 days</span>
            </label>
            <label className="flex items-center gap-2 text-sm cursor-pointer hover:bg-muted/50 p-2 rounded">
              <input type="radio" name="dateRange" className="border-border" />
              <span>Last 90 days</span>
            </label>
            <label className="flex items-center gap-2 text-sm cursor-pointer hover:bg-muted/50 p-2 rounded">
              <input type="radio" name="dateRange" className="border-border" />
              <span>Custom range</span>
            </label>
          </div>
        </section>

        {/* Quality Score */}
        <section>
          <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <TrendingUp className="w-4 h-4" />
            Quality Score
          </h4>
          <div className="space-y-3">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                Minimum Quality: 80%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                defaultValue="80"
                className="w-full"
              />
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                Minimum Relevance: 75%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                defaultValue="75"
                className="w-full"
              />
            </div>
          </div>
        </section>

        {/* Content Type */}
        <section>
          <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <Layers className="w-4 h-4" />
            Content Type
          </h4>
          <div className="space-y-2">
            {['Article', 'Insight', 'Report', 'News', 'Research Paper'].map((type) => (
              <label key={type} className="flex items-center gap-2 text-sm cursor-pointer hover:bg-muted/50 p-2 rounded">
                <input type="checkbox" className="rounded border-border" defaultChecked />
                <span>{type}</span>
              </label>
            ))}
          </div>
        </section>

        {/* Actions */}
        <div className="pt-4 border-t border-border space-y-2">
          <Button className="w-full" size="sm">
            Apply Filters
          </Button>
          <Button variant="outline" className="w-full" size="sm">
            Reset All
          </Button>
        </div>
      </div>
    </div>
  )
}

// Graph Lab page context panel
function GraphLabContext() {
  const { entities, relationships, selectedEntityIds } = useGraphStore()

  const selectedEntities = Array.from(selectedEntityIds)
    .map(id => entities.find(e => e.id === id))
    .filter(Boolean)

  return (
    <div className="h-full overflow-auto">
      <div className="p-4 border-b border-border">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Network className="w-5 h-5" />
          Graph Details
        </h3>
        <p className="text-sm text-muted-foreground mt-1">
          Explore node properties and relationships
        </p>
      </div>

      <div className="p-4 space-y-6">
        {/* Graph Statistics */}
        <section>
          <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <TrendingUp className="w-4 h-4" />
            Graph Statistics
          </h4>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between p-2 bg-muted/50 rounded">
              <span className="text-muted-foreground">Total Nodes:</span>
              <span className="font-medium">{entities.length}</span>
            </div>
            <div className="flex justify-between p-2 bg-muted/50 rounded">
              <span className="text-muted-foreground">Total Edges:</span>
              <span className="font-medium">{relationships.length}</span>
            </div>
            <div className="flex justify-between p-2 bg-muted/50 rounded">
              <span className="text-muted-foreground">Selected:</span>
              <span className="font-medium">{selectedEntityIds.size}</span>
            </div>
          </div>
        </section>

        {/* Selected Node Details */}
        {selectedEntities.length > 0 ? (
          <section>
            <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
              <Info className="w-4 h-4" />
              Selected Node{selectedEntities.length > 1 ? 's' : ''}
            </h4>
            <div className="space-y-3">
              {selectedEntities.map((entity) => (
                <div key={entity.id} className="p-3 bg-muted/50 rounded border border-border">
                  <div className="font-medium text-sm mb-2">{entity.name}</div>
                  <div className="space-y-1 text-xs">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Type:</span>
                      <span className="capitalize">{entity.type}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Confidence:</span>
                      <span>{(entity.confidence * 100).toFixed(0)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Method:</span>
                      <span className="uppercase">{entity.extraction_method}</span>
                    </div>
                  </div>
                  {entity.metadata && Object.keys(entity.metadata).length > 0 && (
                    <div className="mt-2 pt-2 border-t border-border">
                      <div className="text-xs text-muted-foreground mb-1">Metadata:</div>
                      <div className="text-xs space-y-1">
                        {Object.entries(entity.metadata).map(([key, value]) => (
                          <div key={key} className="flex justify-between">
                            <span className="text-muted-foreground">{key}:</span>
                            <span className="max-w-[150px] truncate">{String(value)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        ) : (
          <section className="p-4 bg-muted/30 rounded-lg text-center">
            <Info className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">
              Select a node to view its properties
            </p>
          </section>
        )}

        {/* Node Type Filter */}
        <section>
          <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <Filter className="w-4 h-4" />
            Filter by Type
          </h4>
          <div className="space-y-2">
            {['All', 'Person', 'Organization', 'Location', 'Concept'].map((type) => (
              <label key={type} className="flex items-center gap-2 text-sm cursor-pointer hover:bg-muted/50 p-2 rounded">
                <input
                  type="radio"
                  name="nodeType"
                  className="border-border"
                  defaultChecked={type === 'All'}
                />
                <span>{type}</span>
              </label>
            ))}
          </div>
        </section>

        {/* Relationship Filters */}
        <section>
          <h4 className="text-sm font-semibold mb-3 flex items-center gap-2">
            <Network className="w-4 h-4" />
            Relationships
          </h4>
          <div className="space-y-2 text-sm">
            <label className="flex items-center gap-2 cursor-pointer hover:bg-muted/50 p-2 rounded">
              <input type="checkbox" className="rounded border-border" defaultChecked />
              <span>Show edge labels</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer hover:bg-muted/50 p-2 rounded">
              <input type="checkbox" className="rounded border-border" defaultChecked />
              <span>Highlight connections</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer hover:bg-muted/50 p-2 rounded">
              <input type="checkbox" className="rounded border-border" />
              <span>Cluster by type</span>
            </label>
          </div>
        </section>

        {/* Export Options */}
        <section className="pt-4 border-t border-border">
          <h4 className="text-sm font-semibold mb-3">Export Options</h4>
          <div className="space-y-2">
            <Button variant="outline" className="w-full" size="sm">
              Export as JSON
            </Button>
            <Button variant="outline" className="w-full" size="sm">
              Export as CSV
            </Button>
            <Button variant="outline" className="w-full" size="sm">
              Export as PNG
            </Button>
          </div>
        </section>
      </div>
    </div>
  )
}

// Settings page context panel
function SettingsContext() {
  return (
    <div className="h-full overflow-auto">
      <div className="p-4 border-b border-border">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <HelpCircle className="w-5 h-5" />
          Help & Tips
        </h3>
        <p className="text-sm text-muted-foreground mt-1">
          Settings guidance and shortcuts
        </p>
      </div>

      <div className="p-4 space-y-4">
        <div className="p-4 bg-primary/10 rounded-lg">
          <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
            <Info className="w-4 h-4" />
            Quick Tips
          </h4>
          <ul className="text-sm space-y-2 text-muted-foreground">
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Use email notifications to stay updated on research topics</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Configure newsletter frequency based on your preference</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Export your data regularly for backup</span>
            </li>
          </ul>
        </div>

        <div className="p-4 bg-muted/50 rounded-lg">
          <h4 className="text-sm font-semibold mb-2 flex items-center gap-2">
            <SettingsIcon className="w-4 h-4" />
            Keyboard Shortcuts
          </h4>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between items-center">
              <span className="text-muted-foreground">Save changes</span>
              <kbd className="px-2 py-1 bg-background rounded text-xs border border-border">
                Ctrl + S
              </kbd>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-muted-foreground">Toggle theme</span>
              <kbd className="px-2 py-1 bg-background rounded text-xs border border-border">
                Ctrl + Shift + T
              </kbd>
            </div>
          </div>
        </div>

        <div className="p-4 bg-amber-500/10 rounded-lg border border-amber-500/20">
          <h4 className="text-sm font-semibold mb-2 flex items-center gap-2 text-amber-700 dark:text-amber-400">
            <Clock className="w-4 h-4" />
            Recent Changes
          </h4>
          <p className="text-xs text-muted-foreground">
            Last updated: Just now
          </p>
        </div>

        <div className="pt-4 border-t border-border">
          <Button variant="outline" className="w-full" size="sm">
            View Documentation
          </Button>
        </div>
      </div>
    </div>
  )
}

// Default context panel (fallback)
function DefaultContext() {
  return (
    <div className="h-full overflow-auto">
      <div className="p-4 border-b border-border">
        <h3 className="text-lg font-semibold">Context Panel</h3>
        <p className="text-sm text-muted-foreground mt-1">
          Dynamic contextual information
        </p>
      </div>

      <div className="p-4">
        <div className="p-8 text-center text-muted-foreground">
          <Info className="w-12 h-12 mx-auto mb-4 opacity-50" />
          <p className="text-sm">
            Navigate to a page to see contextual information and controls
          </p>
        </div>
      </div>
    </div>
  )
}

