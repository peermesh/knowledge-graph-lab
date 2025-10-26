// Core application types

export interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  role: 'user' | 'admin' | 'moderator' | 'researcher'
  is_active: boolean
  created_at: string
  updated_at: string
  last_login?: string
}

export interface Entity {
  id: string
  name: string
  type: 'organization' | 'person' | 'funding_amount' | 'date' | 'location' | 'concept' | 'event'
  confidence: number
  source: string
  source_type: string
  source_document_id?: string
  extraction_method: string
  positions?: number[][]
  metadata?: Record<string, any>
  vector_embedding?: number[]
  created_at: string
  updated_at: string
  is_active: boolean
}

export interface EntityRelationship {
  id: string
  source_entity_id: string
  target_entity_id: string
  relationship_type: 'fund' | 'partner' | 'acquire' | 'compete' | 'collaborate' | 'mention'
  confidence: number
  strength?: number
  evidence: string
  temporal_context?: {
    start_date?: string
    end_date?: string
    duration_days?: number
  }
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface KnowledgeGraphNode {
  id: string
  entity_id: string
  node_type: 'entity' | 'concept' | 'event'
  properties: Record<string, any>
  vector_embedding?: number[]
  degree: number
  created_at: string
  updated_at: string
}

export interface KnowledgeGraphEdge {
  id: string
  source_node_id: string
  target_node_id: string
  relationship_type: string
  properties?: Record<string, any>
  confidence: number
  created_at: string
  updated_at: string
}

export interface ResearchItem {
  id: string
  title: string
  summary: string
  content_type: 'article' | 'insight' | 'alert' | 'newsletter'
  content_body?: string
  quality_score: number
  relevance_score: number
  entity_tags: string[]
  topics: string[]
  source_url?: string
  published_at: string
  created_at: string
  updated_at: string
  created_by: string
  is_active: boolean
}

export interface APIResponse<T> {
  data: T
  metadata: {
    timestamp: string
    request_id: string
    pagination?: {
      page: number
      page_size: number
      total_count: number
      has_more: boolean
    }
    cache_info?: {
      cached: boolean
      cache_age_seconds?: number
    }
  }
  links?: {
    self: string
    next?: string
    prev?: string
  }
}

export interface APIError {
  code: string
  message: string
  details?: Record<string, any>
  retry_after?: number
}

// UI State Types
export interface UIState {
  theme: 'light' | 'dark' | 'auto'
  sidebarCollapsed: boolean
  rightPanelVisible: boolean
  loading: {
    isActive: boolean
    message?: string
  }
  notifications: AppNotification[]
}

export interface AppNotification {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  message: string
  duration: number
  timestamp: string
  actions?: NotificationAction[]
}

export interface NotificationAction {
  label: string
  action: () => void
  variant?: 'default' | 'destructive'
}

// Graph Visualization Types
export interface GraphConfig {
  node_size_range: [number, number]
  edge_thickness_range: [number, number]
  color_scheme: 'default' | 'type-based' | 'confidence-based'
  animation_duration: number
  clustering_enabled: boolean
  physics_enabled: boolean
}

export interface GraphState {
  current_view: 'list' | 'graph' | 'timeline' | 'table'
  graph_config: GraphConfig
  layout_engine: 'force-directed' | 'hierarchical' | 'circular'
  selected_entities: Set<string>
  highlighted_relationships: Set<string>
  zoom_level: number
  pan_position: { x: number; y: number }
}

// Search and Filter Types
export interface SearchState {
  query: string
  filters: SearchFilters
  results: SearchResults
  suggestions: SearchSuggestion[]
  history: SearchHistory[]
}

export interface SearchFilters {
  entity_types?: string[]
  date_range?: { start: string; end: string }
  confidence_range?: { min: number; max: number }
  relationship_types?: string[]
  metadata_filters?: Record<string, any>
}

export interface SearchResults {
  entities: Entity[]
  relationships: EntityRelationship[]
  total_count: number
  facets: SearchFacets
  execution_time: number
}

export interface SearchFacets {
  entity_types: Record<string, number>
  relationship_types: Record<string, number>
  date_ranges: Record<string, number>
  confidence_ranges: Record<string, number>
}

export interface SearchSuggestion {
  text: string
  type: 'entity' | 'relationship' | 'query'
  relevance_score: number
}

export interface SearchHistory {
  id: string
  query: string
  timestamp: string
  result_count: number
}

// Export Configuration Types
export interface ExportState {
  current_exports: Map<string, ExportJob>
  export_history: ExportRecord[]
  default_formats: ExportFormat[]
  scheduled_exports: any[]
}

export interface ExportJob {
  id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  progress: number
  format: ExportFormat
  data_selection: ExportDataSelection
  created_at: string
  estimated_completion?: string
}

export interface ExportRecord {
  id: string
  format: ExportFormat
  data_count: number
  file_size: number
  download_url: string
  created_at: string
  expires_at: string
}

export type ExportFormat = 'json' | 'csv' | 'pdf' | 'image'

export interface ExportDataSelection {
  entity_ids?: string[]
  relationship_ids?: string[]
  include_metadata: boolean
  include_embeddings: boolean
  date_range?: { start: string; end: string }
}

// WebSocket Types
export interface WebSocketMessage {
  type: 'entity_update' | 'relationship_update' | 'user_activity' | 'system_notification'
  data: any
  timestamp: string
  id: string
  source: 'backend' | 'ai' | 'user'
}

export interface WebSocketState {
  connection_status: 'disconnected' | 'connecting' | 'connected' | 'error'
  subscriptions: Map<string, SubscriptionInfo>
  pending_updates: UpdateQueue
  last_heartbeat: string
}

export interface SubscriptionInfo {
  entity_id: string
  subscription_type: 'entity' | 'relationship' | 'search'
  callback: (update: any) => void
  created_at: string
}

export interface UpdateQueue {
  updates: WebSocketMessage[]
  max_size: number
  flush_interval: number
}

// Form Types
export interface UserPreferences {
  theme: 'light' | 'dark' | 'auto'
  default_view: 'list' | 'graph'
  auto_refresh: boolean
  refresh_interval: number
  notifications: NotificationSettings
  accessibility: AccessibilitySettings
}

export interface NotificationSettings {
  email_enabled: boolean
  slack_enabled: boolean
  discord_enabled: boolean
  browser_enabled: boolean
  frequency: 'real-time' | 'hourly' | 'daily' | 'weekly'
}

export interface AccessibilitySettings {
  high_contrast: boolean
  reduced_motion: boolean
  large_text: boolean
  screen_reader_optimized: boolean
}

// API Service Types
export interface ApiConfig {
  baseURL: string
  timeout: number
  retries: number
  retryDelay: number
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    page: number
    page_size: number
    total_count: number
    has_more: boolean
  }
  execution_time_ms: number
}
