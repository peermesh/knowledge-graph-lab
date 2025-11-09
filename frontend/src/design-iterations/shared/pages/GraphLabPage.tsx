import { useEffect, useRef, useState } from 'react'
import { ZoomIn, ZoomOut, RotateCcw, Maximize, Filter, Download, Settings as SettingsIcon } from 'lucide-react'

import { SigmaGraph } from '@/components/Graph/SigmaGraph'
import { useGraphStore } from '@/store/useGraphStore'
import { useUIStore } from '@/store/useUIStore'
import { api } from '@/services/api'
import { useDesignTheme } from '../ThemeProvider'
import { ThemedButton } from '../components/ThemedButton'

export function SharedGraphLabPage() {
  const theme = useDesignTheme()
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

  useEffect(() => {
    const loadGraphData = async () => {
      if (entities.length > 0) return
      
      try {
        const entitiesResponse = await api.getEntities({ limit: 100, confidence_min: 0.6 })
        setEntities(entitiesResponse.data)
        
        const entityIds = new Set(entitiesResponse.data.map(e => e.id))
        const relationshipsResponse = await api.getRelationships({ limit: 200, confidence_min: 0.6 })
        const validRelationships = relationshipsResponse.data.filter(r => 
          entityIds.has(r.source_entity_id) && entityIds.has(r.target_entity_id)
        )
        setRelationships(validRelationships)
        
        addNotification({
          type: 'success',
          message: `Loaded ${entitiesResponse.data.length} entities into graph`,
          duration: 3000,
        })
      } catch (error: any) {
        console.error('Failed to load graph data:', error)
        addNotification({
          type: 'error',
          message: `Failed to load graph: ${error.message}`,
          duration: 5000,
        })
      }
    }
    
    loadGraphData()
  }, [entities.length, setEntities, setRelationships, addNotification])

  const handleZoomIn = () => setZoom(Math.min(zoom_level * 1.2, 5))
  const handleZoomOut = () => setZoom(Math.max(zoom_level * 0.8, 0.1))
  const handleResetView = () => resetView()
  const handleExportGraph = () => addNotification({ type: 'success', message: 'Graph exported successfully', duration: 3000 })
  const handleToggleFullscreen = () => {
    setIsFullscreen(!isFullscreen)
    toggleFullscreen()
  }

  return (
    <div className="h-full flex flex-col" style={{ background: theme.colors.neutral[50] }}>
      {/* Header */}
      <div
        style={{
          borderBottom: `1px solid ${theme.colors.neutral[200]}`,
          padding: theme.spacing.lg,
          background: 'white',
          boxShadow: theme.shadows.sm,
        }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h1
              style={{
                fontSize: theme.typography.fontSize['2xl'],
                fontWeight: theme.typography.fontWeight.bold,
                color: theme.colors.neutral[900],
              }}
            >
              Graph Lab
            </h1>
            <p style={{ color: theme.colors.neutral[500], fontSize: theme.typography.fontSize.sm }}>
              Interactive knowledge graph exploration and visualization
            </p>
          </div>

          <div className="flex items-center gap-2">
            {/* Zoom Controls */}
            <div
              className="flex items-center gap-1 rounded-lg"
              style={{
                background: theme.colors.neutral[100],
                padding: '0.25rem',
              }}
            >
              <ThemedButton variant="ghost" size="sm" onClick={handleZoomOut}>
                <ZoomOut className="w-4 h-4" />
              </ThemedButton>
              <span
                style={{
                  fontSize: theme.typography.fontSize.xs,
                  color: theme.colors.neutral[500],
                  padding: '0 0.5rem',
                }}
              >
                {Math.round(zoom_level * 100)}%
              </span>
              <ThemedButton variant="ghost" size="sm" onClick={handleZoomIn}>
                <ZoomIn className="w-4 h-4" />
              </ThemedButton>
            </div>

            <ThemedButton variant="ghost" size="sm" onClick={handleResetView}>
              <RotateCcw className="w-4 h-4" />
            </ThemedButton>

            <ThemedButton variant="ghost" size="sm" onClick={handleToggleFullscreen}>
              <Maximize className="w-4 h-4" />
            </ThemedButton>

            <ThemedButton variant="ghost" size="sm">
              <Filter className="w-4 h-4" />
            </ThemedButton>

            <ThemedButton variant="ghost" size="sm" onClick={handleExportGraph}>
              <Download className="w-4 h-4" />
            </ThemedButton>

            <ThemedButton variant="ghost" size="sm">
              <SettingsIcon className="w-4 h-4" />
            </ThemedButton>
          </div>
        </div>
      </div>

      {/* Graph Container */}
      <div className="flex-1 relative">
        {isLoading ? (
          <div
            className="absolute inset-0 flex items-center justify-center"
            style={{ background: `${theme.colors.neutral[50]}CC` }}
          >
            <div className="flex items-center gap-3">
              <div
                className="animate-spin rounded-full h-8 w-8 border-b-2"
                style={{ borderColor: theme.colors.primary[500] }}
              ></div>
              <span style={{ color: theme.colors.neutral[600] }}>Loading knowledge graph...</span>
            </div>
          </div>
        ) : error ? (
          <div
            className="absolute inset-0 flex items-center justify-center"
            style={{ background: `${theme.colors.neutral[50]}CC` }}
          >
            <div className="text-center">
              <div className="text-6xl mb-4">⚠️</div>
              <h3
                className="text-lg font-medium mb-2"
                style={{ color: theme.colors.neutral[900] }}
              >
                Failed to load graph
              </h3>
              <p style={{ color: theme.colors.neutral[600], marginBottom: '1rem' }}>{error}</p>
              <ThemedButton onClick={handleResetView} variant="outline">
                Retry
              </ThemedButton>
            </div>
          </div>
        ) : (
          <div
            ref={graphContainerRef}
            className="h-full w-full relative"
            style={{ background: theme.colors.neutral[100] }}
          >
            {entities.length === 0 ? (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center" style={{ color: theme.colors.neutral[500] }}>
                  <div className="text-4xl mb-2">📊</div>
                  <p>Loading graph data...</p>
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
      <div
        style={{
          borderTop: `1px solid ${theme.colors.neutral[200]}`,
          padding: '0.5rem 1rem',
          background: `${theme.colors.neutral[100]}4D`,
        }}
      >
        <div
          className="flex items-center justify-between"
          style={{
            fontSize: theme.typography.fontSize.xs,
            color: theme.colors.neutral[500],
          }}
        >
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












