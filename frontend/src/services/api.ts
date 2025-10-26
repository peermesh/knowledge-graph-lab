import axios, { AxiosInstance } from 'axios'

import type {
  Entity,
  EntityRelationship,
  User,
  ResearchItem,
  PaginatedResponse
} from '@/types'

class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code: string,
    public details?: Record<string, any>
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

class ApiClient {
  private client: AxiosInstance
  private baseURL: string

  constructor(baseURL: string = '/api/v1') {
    this.baseURL = baseURL
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = localStorage.getItem('access_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }

        // Add request ID for tracing
        config.headers['X-Request-ID'] = crypto.randomUUID()

        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error) => {
        if (error.response) {
          const { status, data } = error.response

          // Handle authentication errors
          if (status === 401) {
            // Clear stored tokens
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')

            // Redirect to login if not already there
            if (window.location.pathname !== '/login') {
              window.location.href = '/login'
            }
          }

          // Transform API errors
          const apiError = new ApiError(
            data.message || error.message,
            status,
            data.code || 'UNKNOWN_ERROR',
            data.details
          )

          return Promise.reject(apiError)
        }

        return Promise.reject(error)
      }
    )
  }

  private async request<T>(
    method: 'GET' | 'POST' | 'PUT' | 'DELETE',
    url: string,
    data?: any,
    params?: Record<string, any>
  ): Promise<T> {
    const response = await this.client.request({
      method,
      url,
      data,
      params,
    })

    return response.data
  }

  // Authentication methods
  async login(email: string, password: string) {
    return this.request<{ access_token: string; refresh_token: string; user: User }>(
      'POST',
      '/auth/login',
      { email, password }
    )
  }

  async refreshToken(refreshToken: string) {
    return this.request<{ access_token: string; expires_in: number }>(
      'POST',
      '/auth/refresh',
      { refresh_token: refreshToken }
    )
  }

  async logout() {
    return this.request('POST', '/auth/logout')
  }

  async getCurrentUser() {
    return this.request<User>('GET', '/auth/me')
  }

  // Entity methods
  async getEntities(params?: {
    entity_type?: string
    confidence_min?: number
    source?: string
    limit?: number
    offset?: number
  }) {
    return this.request<PaginatedResponse<Entity>>('GET', '/entities', undefined, params)
  }

  async getEntity(entityId: string) {
    return this.request<Entity>('GET', `/entities/${entityId}`)
  }

  async createEntity(entity: Partial<Entity>) {
    return this.request<Entity>('POST', '/entities', entity)
  }

  async updateEntity(entityId: string, updates: Partial<Entity>) {
    return this.request<Entity>('PUT', `/entities/${entityId}`, updates)
  }

  async deleteEntity(entityId: string) {
    return this.request('DELETE', `/entities/${entityId}`)
  }

  async extractEntities(content: string, documentType: string = 'text') {
    return this.request<{
      job_id: string
      entities: Entity[]
      relationships: EntityRelationship[]
    }>('POST', '/entities/extract', {
      content,
      document_type: documentType,
    })
  }

  // Relationship methods
  async getRelationships(params?: {
    source_entity?: string
    target_entity?: string
    relationship_type?: string
    confidence_min?: number
    limit?: number
  }) {
    return this.request<PaginatedResponse<EntityRelationship>>('GET', '/relationships', undefined, params)
  }

  async createRelationship(relationship: Partial<EntityRelationship>) {
    return this.request<EntityRelationship>('POST', '/relationships', relationship)
  }

  async getEntityRelationships(entityId: string, direction: 'source' | 'target' | 'both' = 'both') {
    return this.request<{ entity_id: string; relationships: EntityRelationship[]; count: number }>(
      'GET',
      `/entities/${entityId}/relationships`,
      undefined,
      { direction }
    )
  }

  // Knowledge Graph methods
  async queryKnowledgeGraph(query: string, filters?: any) {
    return this.request<any>('GET', '/relationships/graph/query', undefined, {
      query,
      filters: JSON.stringify(filters || {}),
    })
  }

  async traverseGraph(startEntity: string, options?: any) {
    return this.request<any>('GET', '/relationships/graph/traversal', undefined, {
      start_entity: startEntity,
      ...options,
    })
  }

  // Search methods
  async searchEntities(query: string, filters?: any) {
    return this.request<any>('GET', '/search/entities', undefined, {
      q: query,
      filters: JSON.stringify(filters || {}),
    })
  }

  async searchRelationships(query: string, filters?: any) {
    return this.request<any>('GET', '/search/relationships', undefined, {
      query,
      filters: JSON.stringify(filters || {}),
    })
  }

  // User management methods
  async getUsers(params?: any) {
    return this.request<User[]>('GET', '/users', undefined, params)
  }

  async getUser(userId: string) {
    return this.request<User>('GET', `/users/${userId}`)
  }

  async updateUser(userId: string, updates: Partial<User>) {
    return this.request<User>('PUT', `/users/${userId}`, updates)
  }

  async deleteUser(userId: string) {
    return this.request('DELETE', `/users/${userId}`)
  }

  // Feed methods
  async getFeed(params?: {
    limit?: number
    offset?: number
    filters?: any
  }) {
    return this.request<PaginatedResponse<ResearchItem>>('GET', '/feed', undefined, params)
  }

  async saveResearchItem(itemId: string) {
    return this.request('POST', `/user/saved/${itemId}`)
  }

  async getSavedItems() {
    return this.request<ResearchItem[]>('GET', '/user/saved')
  }

  // Engagement methods
  async logEngagement(action: string, targetType: string, targetId: string, metadata?: any) {
    return this.request('POST', '/engagement', {
      action,
      target_type: targetType,
      target_id: targetId,
      metadata,
    })
  }

  // Health check
  async healthCheck() {
    return this.request<any>('GET', '/health')
  }
}

// Create and export singleton instance
export const apiClient = new ApiClient()

// Export convenience functions
export const api = {
  // Authentication
  login: (email: string, password: string) => apiClient.login(email, password),
  refreshToken: (token: string) => apiClient.refreshToken(token),
  logout: () => apiClient.logout(),
  getCurrentUser: () => apiClient.getCurrentUser(),

  // Entities
  getEntities: (params?: any) => apiClient.getEntities(params),
  getEntity: (id: string) => apiClient.getEntity(id),
  createEntity: (entity: Partial<Entity>) => apiClient.createEntity(entity),
  updateEntity: (id: string, updates: Partial<Entity>) => apiClient.updateEntity(id, updates),
  deleteEntity: (id: string) => apiClient.deleteEntity(id),
  extractEntities: (content: string, type?: string) => apiClient.extractEntities(content, type),

  // Relationships
  getRelationships: (params?: any) => apiClient.getRelationships(params),
  createRelationship: (relationship: Partial<EntityRelationship>) => apiClient.createRelationship(relationship),
  getEntityRelationships: (id: string, direction?: string) => apiClient.getEntityRelationships(id, direction as any),

  // Knowledge Graph
  queryGraph: (query: string, filters?: any) => apiClient.queryKnowledgeGraph(query, filters),
  traverseGraph: (startEntity: string, options?: any) => apiClient.traverseGraph(startEntity, options),

  // Search
  searchEntities: (query: string, filters?: any) => apiClient.searchEntities(query, filters),
  searchRelationships: (query: string, filters?: any) => apiClient.searchRelationships(query, filters),

  // Users
  getUsers: (params?: any) => apiClient.getUsers(params),
  getUser: (id: string) => apiClient.getUser(id),
  updateUser: (id: string, updates: Partial<User>) => apiClient.updateUser(id, updates),
  deleteUser: (id: string) => apiClient.deleteUser(id),

  // Feed
  getFeed: (params?: any) => apiClient.getFeed(params),
  saveItem: (id: string) => apiClient.saveResearchItem(id),
  getSavedItems: () => apiClient.getSavedItems(),

  // Engagement
  logEngagement: (action: string, targetType: string, targetId: string, metadata?: any) =>
    apiClient.logEngagement(action, targetType, targetId, metadata),

  // Health
  healthCheck: () => apiClient.healthCheck(),
}