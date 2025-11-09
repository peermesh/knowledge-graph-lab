import { http, HttpResponse } from 'msw'
import { 
  mockResearchItems, 
  getResearchItemsByType, 
  getResearchItemsByTopic,
  getTopResearchItems,
  searchResearchItems
} from '../data/research'
import { faker } from '@faker-js/faker'

// Track saved items per user (in-memory store)
const userSavedItems: Map<string, Set<string>> = new Map()

export const feedHandlers = [
  // Get research feed
  http.get('/api/v1/feed', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, faker.number.int({ min: 200, max: 400 })))
    
    const url = new URL(request.url)
    const limit = parseInt(url.searchParams.get('limit') || '20')
    const offset = parseInt(url.searchParams.get('offset') || '0')
    const contentType = url.searchParams.get('content_type')
    const topic = url.searchParams.get('topic')
    const sortBy = url.searchParams.get('sort_by') || 'published_at' // published_at, quality_score, relevance_score
    
    // Start with active items
    let filtered = mockResearchItems.filter(r => r.is_active)
    
    // Apply filters
    if (contentType) {
      filtered = filtered.filter(r => r.content_type === contentType)
    }
    
    if (topic) {
      filtered = filtered.filter(r => r.topics.includes(topic))
    }
    
    // Sort
    if (sortBy === 'quality_score') {
      filtered = filtered.sort((a, b) => b.quality_score - a.quality_score)
    } else if (sortBy === 'relevance_score') {
      filtered = filtered.sort((a, b) => b.relevance_score - a.relevance_score)
    } else if (sortBy === 'published_at') {
      filtered = filtered.sort((a, b) => 
        new Date(b.published_at).getTime() - new Date(a.published_at).getTime()
      )
    }
    
    // Paginate
    const total = filtered.length
    const paginated = filtered.slice(offset, offset + limit)
    
    return HttpResponse.json({
      data: paginated,
      pagination: {
        page: Math.floor(offset / limit) + 1,
        page_size: limit,
        total_count: total,
        has_more: offset + limit < total
      },
      execution_time_ms: faker.number.int({ min: 150, max: 350 })
    })
  }),
  
  // Get trending feed items
  http.get('/api/v1/feed/trending', async () => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 300))
    
    const trending = getTopResearchItems(20)
    
    return HttpResponse.json({
      data: trending,
      generated_at: new Date().toISOString()
    })
  }),
  
  // Save research item
  http.post('/api/v1/user/saved/:itemId', async ({ params, request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 200))
    
    const authHeader = request.headers.get('Authorization')
    if (!authHeader) {
      return HttpResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }
    
    // Extract user ID from token
    const token = authHeader.replace('Bearer ', '')
    const userId = token.split('_').pop() || 'anonymous'
    
    // Check if item exists
    const item = mockResearchItems.find(r => r.id === params.itemId)
    if (!item) {
      return HttpResponse.json(
        { error: 'Research item not found' },
        { status: 404 }
      )
    }
    
    // Add to saved items
    if (!userSavedItems.has(userId)) {
      userSavedItems.set(userId, new Set())
    }
    userSavedItems.get(userId)!.add(params.itemId as string)
    
    return HttpResponse.json({
      success: true,
      message: 'Item saved',
      saved_at: new Date().toISOString()
    })
  }),
  
  // Remove saved item
  http.delete('/api/v1/user/saved/:itemId', async ({ params, request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 200))
    
    const authHeader = request.headers.get('Authorization')
    if (!authHeader) {
      return HttpResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }
    
    // Extract user ID from token
    const token = authHeader.replace('Bearer ', '')
    const userId = token.split('_').pop() || 'anonymous'
    
    // Remove from saved items
    if (userSavedItems.has(userId)) {
      userSavedItems.get(userId)!.delete(params.itemId as string)
    }
    
    return HttpResponse.json({
      success: true,
      message: 'Item removed from saved'
    })
  }),
  
  // Get saved items
  http.get('/api/v1/user/saved', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 250))
    
    const authHeader = request.headers.get('Authorization')
    if (!authHeader) {
      return HttpResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }
    
    // Extract user ID from token
    const token = authHeader.replace('Bearer ', '')
    const userId = token.split('_').pop() || 'anonymous'
    
    // Get saved item IDs
    const savedIds = userSavedItems.get(userId) || new Set()
    
    // Get actual items
    const savedItems = mockResearchItems.filter(r => savedIds.has(r.id))
    
    return HttpResponse.json({
      data: savedItems,
      count: savedItems.length
    })
  }),
  
  // Log engagement
  http.post('/api/v1/engagement', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 150))
    
    const body = await request.json() as {
      action: string
      target_type: string
      target_id: string
      metadata?: Record<string, any>
    }
    
    // Just acknowledge - in real system this would be stored
    return HttpResponse.json({
      success: true,
      message: 'Engagement logged',
      engagement_id: faker.string.uuid(),
      timestamp: new Date().toISOString()
    })
  }),
  
  // Search feed
  http.get('/api/v1/search/feed', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 300))
    
    const url = new URL(request.url)
    const query = url.searchParams.get('q') || ''
    const limit = parseInt(url.searchParams.get('limit') || '20')
    
    const results = searchResearchItems(query).slice(0, limit)
    
    return HttpResponse.json({
      query,
      results,
      count: results.length,
      execution_time_ms: faker.number.int({ min: 200, max: 400 })
    })
  })
]














