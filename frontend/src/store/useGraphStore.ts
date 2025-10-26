import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

import type { Entity, EntityRelationship, GraphState } from '@/types'

interface GraphStore extends GraphState {
  // Data
  entities: Entity[]
  relationships: EntityRelationship[]
  isLoading: boolean
  error: string | null

  // Selection and highlighting
  selectedEntityIds: Set<string>
  highlightedRelationshipIds: Set<string>

  // View state
  zoom_level: number
  pan_position: { x: number; y: number }
  isFullscreen: boolean

  // Actions
  setEntities: (entities: Entity[]) => void
  setRelationships: (relationships: EntityRelationship[]) => void
  addEntity: (entity: Entity) => void
  updateEntity: (entityId: string, updates: Partial<Entity>) => void
  removeEntity: (entityId: string) => void

  selectEntity: (entityId: string) => void
  deselectEntity: (entityId: string) => void
  clearSelection: () => void

  highlightRelationship: (relationshipId: string) => void
  unhighlightRelationship: (relationshipId: string) => void
  clearHighlights: () => void

  setZoom: (zoom: number) => void
  setPan: (pan: { x: number; y: number }) => void
  resetView: () => void
  toggleFullscreen: () => void

  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  resetGraph: () => void
}

const initialState: GraphState = {
  current_view: 'graph',
  graph_config: {
    node_size_range: [10, 50],
    edge_thickness_range: [1, 5],
    color_scheme: 'default',
    animation_duration: 300,
    clustering_enabled: false,
    physics_enabled: true,
  },
  layout_engine: 'force-directed',
  selected_entities: new Set(),
  highlighted_relationships: new Set(),
  zoom_level: 1,
  pan_position: { x: 0, y: 0 },
}

export const useGraphStore = create<GraphStore>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,

        // Data management
        entities: [],
        relationships: [],
        isLoading: false,
        error: null,

        selectedEntityIds: new Set(),
        highlightedRelationshipIds: new Set(),

        zoom_level: 1,
        pan_position: { x: 0, y: 0 },
        isFullscreen: false,

        setEntities: (entities: Entity[]) => {
          set({ entities }, false, 'setEntities')
        },

        setRelationships: (relationships: EntityRelationship[]) => {
          set({ relationships }, false, 'setRelationships')
        },

        addEntity: (entity: Entity) => {
          set(
            (state) => ({
              entities: [...state.entities, entity],
            }),
            false,
            'addEntity'
          )
        },

        updateEntity: (entityId: string, updates: Partial<Entity>) => {
          set(
            (state) => ({
              entities: state.entities.map((entity) =>
                entity.id === entityId ? { ...entity, ...updates } : entity
              ),
            }),
            false,
            'updateEntity'
          )
        },

        removeEntity: (entityId: string) => {
          set(
            (state) => ({
              entities: state.entities.filter((entity) => entity.id !== entityId),
              selectedEntityIds: new Set(
                Array.from(state.selectedEntityIds).filter((id) => id !== entityId)
              ),
            }),
            false,
            'removeEntity'
          )
        },

        selectEntity: (entityId: string) => {
          set(
            (state) => ({
              selectedEntityIds: new Set([...state.selectedEntityIds, entityId]),
            }),
            false,
            'selectEntity'
          )
        },

        deselectEntity: (entityId: string) => {
          set(
            (state) => ({
              selectedEntityIds: new Set(
                Array.from(state.selectedEntityIds).filter((id) => id !== entityId)
              ),
            }),
            false,
            'deselectEntity'
          )
        },

        clearSelection: () => {
          set({ selectedEntityIds: new Set() }, false, 'clearSelection')
        },

        highlightRelationship: (relationshipId) => {
          set(
            (state) => ({
              highlightedRelationshipIds: new Set([...state.highlightedRelationshipIds, relationshipId]),
            }),
            false,
            'highlightRelationship'
          )
        },

        unhighlightRelationship: (relationshipId) => {
          set(
            (state) => ({
              highlightedRelationshipIds: new Set(
                Array.from(state.highlightedRelationshipIds).filter((id) => id !== relationshipId)
              ),
            }),
            false,
            'unhighlightRelationship'
          )
        },

        clearHighlights: () => {
          set({ highlightedRelationshipIds: new Set() }, false, 'clearHighlights')
        },

        setZoom: (zoom) => {
          set({ zoom_level: zoom }, false, 'setZoom')
        },

        setPan: (pan) => {
          set({ pan_position: pan }, false, 'setPan')
        },

        resetView: () => {
          set(
            {
              zoom_level: 1,
              pan_position: { x: 0, y: 0 },
              selectedEntityIds: new Set(),
              highlightedRelationshipIds: new Set(),
            },
            false,
            'resetView'
          )
        },

        toggleFullscreen: () => {
          set(
            (state) => ({ isFullscreen: !state.isFullscreen }),
            false,
            'toggleFullscreen'
          )
        },

        setLoading: (isLoading) => {
          set({ isLoading }, false, 'setLoading')
        },

        setError: (error) => {
          set({ error }, false, 'setError')
        },

        resetGraph: () => {
          set(
            {
              ...initialState,
              entities: [],
              relationships: [],
              isLoading: false,
              error: null,
              selectedEntityIds: new Set(),
              highlightedRelationshipIds: new Set(),
              zoom_level: 1,
              pan_position: { x: 0, y: 0 },
              isFullscreen: false,
            },
            false,
            'resetGraph'
          )
        },
      }),
      {
        name: 'graph-store',
        partialize: (state) => ({
          graph_config: state.graph_config,
          layout_engine: state.layout_engine,
          zoom_level: state.zoom_level,
          pan_position: state.pan_position,
        }),
      }
    ),
    {
      name: 'graph-store',
    }
  )
)