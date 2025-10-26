import { useEffect, useRef } from 'react'
import Graph from 'graphology'
import { Sigma } from 'sigma'

import type { Entity, EntityRelationship } from '@/types'

interface SigmaGraphProps {
  entities: Entity[]
  relationships: EntityRelationship[]
  containerRef: React.RefObject<HTMLDivElement>
  className?: string
}

export function SigmaGraph({
  entities,
  relationships,
  containerRef,
  className = '',
}: SigmaGraphProps) {
  const sigmaRef = useRef<Sigma | null>(null)
  const graphRef = useRef<Graph | null>(null)

  useEffect(() => {
    if (!containerRef.current) return

    // Create graphology graph
    const graph = new Graph()

    // Add entities as nodes
    entities.forEach((entity) => {
      const baseSize = Math.max(10, Math.min(50, entity.confidence * 40 + 10))
      const nodeColor = getNodeColor(entity.type, entity.confidence)
      const nodeSize = getNodeSize(entity.type, baseSize)

      graph.addNode(entity.id, {
        label: entity.name,
        size: nodeSize,
        color: nodeColor,
        // Don't specify type - let Sigma.js use defaults
        entityType: entity.type, // Store original type for reference
        confidence: entity.confidence,
        x: Math.random() * 100 - 50, // Random initial position
        y: Math.random() * 100 - 50,
      })
    })

    // Add relationships as edges
    relationships.forEach((relationship) => {
      const edgeColor = getEdgeColor(relationship.relationship_type, relationship.confidence)

      graph.addEdge(relationship.source_entity_id, relationship.target_entity_id, {
        label: relationship.relationship_type,
        color: edgeColor,
        size: Math.max(1, relationship.confidence * 5),
        // Don't specify type - let Sigma.js use defaults
        relationshipType: relationship.relationship_type, // Store original type for reference
        confidence: relationship.confidence,
      })
    })

    // Create Sigma instance
    const sigma = new Sigma(graph, containerRef.current, {
      allowInvalidContainer: true,
      renderLabels: true,
      renderEdgeLabels: false,
    })

    // Configure camera
    sigma.getCamera().setState({
      x: 0,
      y: 0,
      angle: 0,
      ratio: 1,
    })

    // Store references
    graphRef.current = graph
    sigmaRef.current = sigma

    // Cleanup
    return () => {
      if (sigmaRef.current) {
        sigmaRef.current.kill()
        sigmaRef.current = null
      }
      graphRef.current = null
    }
  }, [entities, relationships, containerRef])

  // Update node positions when entities change
  useEffect(() => {
    if (!graphRef.current || !sigmaRef.current) return

    // Update node positions and properties
    entities.forEach((entity) => {
      const baseSize = Math.max(10, Math.min(50, entity.confidence * 40 + 10))
      const nodeColor = getNodeColor(entity.type, entity.confidence)
      const nodeSize = getNodeSize(entity.type, baseSize)

      graphRef.current!.mergeNodeAttributes(entity.id, {
        label: entity.name,
        size: nodeSize,
        color: nodeColor,
        // Don't specify type - let Sigma.js use defaults
        entityType: entity.type, // Store original type for reference
        confidence: entity.confidence,
      })
    })

    // Trigger re-render
    sigmaRef.current.refresh()
  }, [entities])

  // Update edges when relationships change
  useEffect(() => {
    if (!graphRef.current || !sigmaRef.current) return

    // Clear existing edges
    graphRef.current.forEachEdge((edge) => {
      graphRef.current!.dropEdge(edge)
    })

    // Add new edges
    relationships.forEach((relationship) => {
      const edgeColor = getEdgeColor(relationship.relationship_type, relationship.confidence)

      graphRef.current!.addEdge(relationship.source_entity_id, relationship.target_entity_id, {
        label: relationship.relationship_type,
        color: edgeColor,
        size: Math.max(1, relationship.confidence * 5),
        // Don't specify type - let Sigma.js use defaults
        relationshipType: relationship.relationship_type, // Store original type for reference
        confidence: relationship.confidence,
      })
    })

    // Trigger re-render
    sigmaRef.current.refresh()
  }, [relationships])

  return (
    <div
      ref={containerRef}
      className={`w-full h-full ${className}`}
      style={{
        minHeight: '400px',
        position: 'relative',
        backgroundColor: '#f8f9fa',
        border: '1px solid #e5e7eb'
      }}
    >
      {/* Canvas will be inserted here by Sigma.js */}
      {entities.length === 0 && (
        <div className="absolute inset-0 flex items-center justify-center bg-background/80">
          <div className="text-center text-muted-foreground">
            <div className="text-4xl mb-2">🔄</div>
            <p>Initializing graph...</p>
            <p className="text-sm">Loading entities and relationships</p>
          </div>
        </div>
      )}
    </div>
  )
}

function getNodeSize(entityType: string, baseSize: number): number {
  // Different entity types can have different base sizes for visual distinction
  const sizeMultiplier: Record<string, number> = {
    organization: 1.2,    // Larger for organizations
    person: 1.0,         // Standard size for people
    funding_amount: 1.5,  // Largest for funding amounts
    date: 0.8,           // Smaller for dates
    location: 1.1,       // Slightly larger for locations
    concept: 1.0,        // Standard for concepts
    event: 1.3,          // Larger for events
  }
  return baseSize * (sizeMultiplier[entityType] || 1.0)
}

// Helper functions for styling
function getNodeColor(entityType: string, confidence: number): string {
  const baseColors: Record<string, string> = {
    organization: '#3B82F6', // blue
    person: '#10B981',       // green
    funding_amount: '#F59E0B', // amber
    date: '#8B5CF6',         // violet
    location: '#EF4444',     // red
    concept: '#06B6D4',      // cyan
    event: '#84CC16',        // lime
  }

  const baseColor = baseColors[entityType] || '#6B7280'
  const opacity = Math.max(0.3, confidence)

  // Convert hex to rgba
  const hex = baseColor.replace('#', '')
  const r = parseInt(hex.substr(0, 2), 16)
  const g = parseInt(hex.substr(2, 2), 16)
  const b = parseInt(hex.substr(4, 2), 16)

  return `rgba(${r}, ${g}, ${b}, ${opacity})`
}

function getEdgeColor(relationshipType: string, confidence: number): string {
  const typeColors: Record<string, string> = {
    fund: '#F59E0B',      // amber
    partner: '#10B981',   // green
    acquire: '#EF4444',   // red
    compete: '#8B5CF6',   // violet
    collaborate: '#06B6D4', // cyan
    mention: '#6B7280',   // gray
  }

  const baseColor = typeColors[relationshipType] || '#6B7280'
  const opacity = Math.max(0.3, confidence)

  // Convert hex to rgba
  const hex = baseColor.replace('#', '')
  const r = parseInt(hex.substr(0, 2), 16)
  const g = parseInt(hex.substr(2, 2), 16)
  const b = parseInt(hex.substr(4, 2), 16)

  return `rgba(${r}, ${g}, ${b}, ${opacity})`
}