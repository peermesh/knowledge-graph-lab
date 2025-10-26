import { useEffect, useRef, useState } from 'react'
import {
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Maximize,
  Filter,
  Download,
  Settings
} from 'lucide-react'

import { Button } from '@/components/Common/Button'
import { SigmaGraph } from '@/components/Graph/SigmaGraph'
import { useGraphStore } from '@/store/useGraphStore'
import { useUIStore } from '@/store/useUIStore'
import type { Entity, EntityRelationship } from '@/types'

export function GraphLabPage() {
  const graphContainerRef = useRef<HTMLDivElement>(null)
  const [isFullscreen, setIsFullscreen] = useState(false)

  const {
    entities,
    relationships,
    selectedEntityIds,
    zoom_level,
    setZoom,
    resetView,
    toggleFullscreen,
    isLoading,
    error,
    setEntities,
    setRelationships,
  } = useGraphStore()

  const { addNotification } = useUIStore()

  // Mock data for demonstration
  const mockEntities: Entity[] = [
    {
      id: 'org1',
      name: 'OpenAI',
      type: 'organization',
      confidence: 0.95,
      source: 'article_001',
      source_type: 'article',
      extraction_method: 'llm',
      metadata: { founded: '2015', headquarters: 'San Francisco' },
      created_at: '2025-01-23T10:00:00Z',
      updated_at: '2025-01-23T10:00:00Z',
      is_active: true,
    },
    {
      id: 'person1',
      name: 'Sam Altman',
      type: 'person',
      confidence: 0.92,
      source: 'article_001',
      source_type: 'article',
      extraction_method: 'llm',
      metadata: { title: 'CEO', company: 'OpenAI' },
      created_at: '2025-01-23T10:00:00Z',
      updated_at: '2025-01-23T10:00:00Z',
      is_active: true,
    },
    {
      id: 'org2',
      name: 'Microsoft',
      type: 'organization',
      confidence: 0.88,
      source: 'article_002',
      source_type: 'article',
      extraction_method: 'llm',
      metadata: { founded: '1975', headquarters: 'Redmond' },
      created_at: '2025-01-23T10:00:00Z',
      updated_at: '2025-01-23T10:00:00Z',
      is_active: true,
    },
  ]

  const mockRelationships: EntityRelationship[] = [
    {
      id: 'rel1',
      source_entity_id: 'org1',
      target_entity_id: 'person1',
      relationship_type: 'partner',
      confidence: 0.87,
      strength: 0.8,
      evidence: 'Sam Altman is CEO of OpenAI',
      temporal_context: { start_date: '2019-01-01' },
      metadata: { role: 'CEO' },
      created_at: '2025-01-23T10:00:00Z',
      updated_at: '2025-01-23T10:00:00Z',
    },
    {
      id: 'rel2',
      source_entity_id: 'org1',
      target_entity_id: 'org2',
      relationship_type: 'fund',
      confidence: 0.92,
      strength: 0.9,
      evidence: 'Microsoft invested $10B in OpenAI',
      temporal_context: { start_date: '2023-01-01' },
      metadata: { amount: '$10B', date: '2023' },
      created_at: '2025-01-23T10:00:00Z',
      updated_at: '2025-01-23T10:00:00Z',
    },
  ]

  useEffect(() => {
    // Initialize graph data
    if (entities.length === 0) {
      // Load mock data
      setEntities(mockEntities)
      setRelationships(mockRelationships)
    }
  }, [entities.length, setEntities, setRelationships])

  const handleZoomIn = () => {
    setZoom(Math.min(zoom_level * 1.2, 5))
  }

  const handleZoomOut = () => {
    setZoom(Math.max(zoom_level * 0.8, 0.1))
  }

  const handleResetView = () => {
    resetView()
  }

  const handleExportGraph = () => {
    addNotification({
      type: 'success',
      message: 'Graph exported successfully',
      duration: 3000,
    })
  }

  const handleToggleFullscreen = () => {
    setIsFullscreen(!isFullscreen)
    toggleFullscreen()
  }

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="border-b border-border p-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Graph Lab</h1>
            <p className="text-muted-foreground">
              Interactive knowledge graph exploration and visualization
            </p>
          </div>

          <div className="flex items-center gap-2">
            {/* Graph Controls */}
            <div className="flex items-center gap-1 bg-muted rounded-md p-1">
              <Button variant="ghost" size="sm" onClick={handleZoomOut}>
                <ZoomOut className="w-4 h-4" />
              </Button>
              <span className="text-xs text-muted-foreground px-2">
                {Math.round(zoom_level * 100)}%
              </span>
              <Button variant="ghost" size="sm" onClick={handleZoomIn}>
                <ZoomIn className="w-4 h-4" />
              </Button>
            </div>

            <Button variant="ghost" size="sm" onClick={handleResetView}>
              <RotateCcw className="w-4 h-4" />
            </Button>

            <Button variant="ghost" size="sm" onClick={handleToggleFullscreen}>
              <Maximize className="w-4 h-4" />
            </Button>

            <Button variant="ghost" size="sm">
              <Filter className="w-4 h-4" />
            </Button>

            <Button variant="ghost" size="sm" onClick={handleExportGraph}>
              <Download className="w-4 h-4" />
            </Button>

            <Button variant="ghost" size="sm">
              <Settings className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Graph Container */}
      <div className="flex-1 relative">
        {isLoading ? (
          <div className="absolute inset-0 flex items-center justify-center bg-background/80">
            <div className="flex items-center gap-3">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              <span className="text-muted-foreground">Loading knowledge graph...</span>
            </div>
          </div>
        ) : error ? (
          <div className="absolute inset-0 flex items-center justify-center bg-background/80">
            <div className="text-center">
              <div className="text-destructive text-6xl mb-4">⚠️</div>
              <h3 className="text-lg font-medium text-foreground mb-2">
                Failed to load graph
              </h3>
              <p className="text-muted-foreground mb-4">{error}</p>
              <Button onClick={handleResetView} variant="outline">
                Retry
              </Button>
            </div>
          </div>
        ) : (
          <div ref={graphContainerRef} className="h-full w-full bg-muted relative">
            {/* Fallback UI in case Sigma.js fails */}
            {entities.length === 0 ? (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center text-muted-foreground">
                  <div className="text-4xl mb-2">📊</div>
                  <p>Loading graph data...</p>
                  <p className="text-sm">Check console for debugging info</p>
                </div>
              </div>
            ) : (
              <SigmaGraph
                entities={entities}
                relationships={relationships}
                containerRef={graphContainerRef}
              />
            )}
          </div>
        )}
      </div>

      {/* Status Bar */}
      <div className="border-t border-border p-2 bg-muted/30">
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <div className="flex items-center gap-4">
            <span>Nodes: {entities.length}</span>
            <span>Edges: {relationships.length}</span>
            <span>Selected: {selectedEntityIds.size}</span>
          </div>
          <div className="flex items-center gap-2">
            <span>Zoom: {Math.round(zoom_level * 100)}%</span>
            <span>•</span>
            <span>WebGL</span>
          </div>
        </div>
      </div>
    </div>
  )
}
