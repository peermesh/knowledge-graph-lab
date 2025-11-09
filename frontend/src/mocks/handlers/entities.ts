import { http, HttpResponse } from 'msw'
import { mockEntities, searchEntities, getEntitiesByType } from '../data/entities'
import { faker } from '@faker-js/faker'
import type { Entity } from '@/types'

export const entityHandlers = [
  // Get entities with pagination and filters
  http.get('/api/v1/entities', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, faker.number.int({ min: 100, max: 300 })))
    
    const url = new URL(request.url)
    const limit = parseInt(url.searchParams.get('limit') || '20')
    const offset = parseInt(url.searchParams.get('offset') || '0')
    const entityType = url.searchParams.get('entity_type')
    const confidenceMin = parseFloat(url.searchParams.get('confidence_min') || '0')
    const source = url.searchParams.get('source')
    const searchQuery = url.searchParams.get('q')
    
    // Start with all active entities
    let filtered = mockEntities.filter(e => e.is_active)
    
    // Apply filters
    if (entityType) {
      filtered = filtered.filter(e => e.type === entityType)
    }
    
    if (confidenceMin > 0) {
      filtered = filtered.filter(e => e.confidence >= confidenceMin)
    }
    
    if (source) {
      filtered = filtered.filter(e => e.source_type === source)
    }
    
    if (searchQuery) {
      const lowerQuery = searchQuery.toLowerCase()
      filtered = filtered.filter(e => 
        e.name.toLowerCase().includes(lowerQuery) ||
        (e.metadata && JSON.stringify(e.metadata).toLowerCase().includes(lowerQuery))
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
      execution_time_ms: faker.number.int({ min: 50, max: 200 })
    })
  }),
  
  // Get single entity by ID
  http.get('/api/v1/entities/:id', async ({ params }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 150))
    
    const entity = mockEntities.find(e => e.id === params.id)
    
    if (!entity) {
      return HttpResponse.json(
        {
          error: 'Not found',
          message: 'Entity not found'
        },
        { status: 404 }
      )
    }
    
    return HttpResponse.json(entity)
  }),
  
  // Create new entity
  http.post('/api/v1/entities', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 400))
    
    const body = await request.json() as Partial<Entity>
    
    // Validate required fields
    if (!body.name || !body.type) {
      return HttpResponse.json(
        {
          error: 'Validation error',
          message: 'Name and type are required'
        },
        { status: 400 }
      )
    }
    
    // Create new entity
    const newEntity: Entity = {
      id: faker.string.uuid(),
      name: body.name,
      type: body.type,
      confidence: body.confidence || 0.8,
      source: body.source || 'manual_entry',
      source_type: body.source_type || 'manual',
      extraction_method: 'manual',
      positions: body.positions,
      metadata: body.metadata || {},
      vector_embedding: body.vector_embedding,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      is_active: true
    }
    
    // Add to mock entities
    mockEntities.push(newEntity)
    
    return HttpResponse.json(newEntity, { status: 201 })
  }),
  
  // Update entity
  http.put('/api/v1/entities/:id', async ({ params, request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 350))
    
    const body = await request.json() as Partial<Entity>
    const index = mockEntities.findIndex(e => e.id === params.id)
    
    if (index === -1) {
      return HttpResponse.json(
        {
          error: 'Not found',
          message: 'Entity not found'
        },
        { status: 404 }
      )
    }
    
    // Update entity
    mockEntities[index] = {
      ...mockEntities[index],
      ...body,
      id: mockEntities[index].id, // Don't allow ID changes
      updated_at: new Date().toISOString()
    }
    
    return HttpResponse.json(mockEntities[index])
  }),
  
  // Delete entity (soft delete)
  http.delete('/api/v1/entities/:id', async ({ params }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 250))
    
    const index = mockEntities.findIndex(e => e.id === params.id)
    
    if (index === -1) {
      return HttpResponse.json(
        {
          error: 'Not found',
          message: 'Entity not found'
        },
        { status: 404 }
      )
    }
    
    // Soft delete
    mockEntities[index].is_active = false
    mockEntities[index].updated_at = new Date().toISOString()
    
    return HttpResponse.json({ success: true, message: 'Entity deleted' })
  }),
  
  // Extract entities from text (mock AI extraction)
  http.post('/api/v1/entities/extract', async ({ request }) => {
    // Simulate longer processing for AI extraction
    await new Promise(resolve => setTimeout(resolve, faker.number.int({ min: 800, max: 1500 })))
    
    const body = await request.json() as { content: string; document_type?: string }
    
    // Mock extraction: return random entities
    const extractedCount = faker.number.int({ min: 3, max: 10 })
    const extractedEntities = faker.helpers.arrayElements(mockEntities, extractedCount)
    
    return HttpResponse.json({
      job_id: faker.string.uuid(),
      entities: extractedEntities,
      relationships: [], // Would include relationships in real implementation
      processing_time_ms: faker.number.int({ min: 800, max: 1500 })
    })
  })
]














