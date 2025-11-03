import { http, HttpResponse } from 'msw'
import { mockRelationships, getRelationshipsForEntity, getRelationshipsByType } from '../data/relationships'
import { mockEntities } from '../data/entities'
import { faker } from '@faker-js/faker'
import type { EntityRelationship } from '@/types'

export const relationshipHandlers = [
  // Get relationships with filters
  http.get('/api/v1/relationships', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, faker.number.int({ min: 150, max: 350 })))
    
    const url = new URL(request.url)
    const limit = parseInt(url.searchParams.get('limit') || '20')
    const offset = parseInt(url.searchParams.get('offset') || '0')
    const sourceEntity = url.searchParams.get('source_entity')
    const targetEntity = url.searchParams.get('target_entity')
    const relationshipType = url.searchParams.get('relationship_type')
    const confidenceMin = parseFloat(url.searchParams.get('confidence_min') || '0')
    
    // Create entity ID set for efficient lookup
    const entityIds = new Set(mockEntities.map(e => e.id))
    
    // Start with all relationships, but filter out ones referencing non-existent entities
    let filtered = mockRelationships.filter(r => 
      entityIds.has(r.source_entity_id) && entityIds.has(r.target_entity_id)
    )
    
    // Apply filters
    if (sourceEntity) {
      filtered = filtered.filter(r => r.source_entity_id === sourceEntity)
    }
    
    if (targetEntity) {
      filtered = filtered.filter(r => r.target_entity_id === targetEntity)
    }
    
    if (relationshipType) {
      filtered = filtered.filter(r => r.relationship_type === relationshipType)
    }
    
    if (confidenceMin > 0) {
      filtered = filtered.filter(r => r.confidence >= confidenceMin)
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
      execution_time_ms: faker.number.int({ min: 80, max: 250 })
    })
  }),
  
  // Get relationships for a specific entity
  http.get('/api/v1/entities/:id/relationships', async ({ params, request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 200))
    
    const url = new URL(request.url)
    const direction = (url.searchParams.get('direction') || 'both') as 'source' | 'target' | 'both'
    
    const relationships = getRelationshipsForEntity(params.id as string, direction)
    
    // Get entity details
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
    
    return HttpResponse.json({
      entity_id: params.id,
      relationships,
      count: relationships.length
    })
  }),
  
  // Create new relationship
  http.post('/api/v1/relationships', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 400))
    
    const body = await request.json() as Partial<EntityRelationship>
    
    // Validate required fields
    if (!body.source_entity_id || !body.target_entity_id || !body.relationship_type) {
      return HttpResponse.json(
        {
          error: 'Validation error',
          message: 'source_entity_id, target_entity_id, and relationship_type are required'
        },
        { status: 400 }
      )
    }
    
    // Check if entities exist
    const sourceExists = mockEntities.some(e => e.id === body.source_entity_id)
    const targetExists = mockEntities.some(e => e.id === body.target_entity_id)
    
    if (!sourceExists || !targetExists) {
      return HttpResponse.json(
        {
          error: 'Validation error',
          message: 'Source or target entity not found'
        },
        { status: 400 }
      )
    }
    
    // Create new relationship
    const newRelationship: EntityRelationship = {
      id: faker.string.uuid(),
      source_entity_id: body.source_entity_id,
      target_entity_id: body.target_entity_id,
      relationship_type: body.relationship_type,
      confidence: body.confidence || 0.8,
      strength: body.strength,
      evidence: body.evidence || 'Manually created relationship',
      temporal_context: body.temporal_context,
      metadata: body.metadata || {},
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    // Add to mock relationships
    mockRelationships.push(newRelationship)
    
    return HttpResponse.json(newRelationship, { status: 201 })
  }),
  
  // Query knowledge graph
  http.get('/api/v1/relationships/graph/query', async ({ request }) => {
    // Simulate network delay for complex query
    await new Promise(resolve => setTimeout(resolve, faker.number.int({ min: 300, max: 600 })))
    
    const url = new URL(request.url)
    const query = url.searchParams.get('query') || ''
    const filtersParam = url.searchParams.get('filters')
    const filters = filtersParam ? JSON.parse(filtersParam) : {}
    
    // Mock graph query - return some entities and their relationships
    const resultEntities = faker.helpers.arrayElements(mockEntities, faker.number.int({ min: 5, max: 15 }))
    const resultRelationships = resultEntities.flatMap(entity => 
      getRelationshipsForEntity(entity.id).slice(0, 3)
    )
    
    return HttpResponse.json({
      entities: resultEntities,
      relationships: resultRelationships,
      query_metadata: {
        execution_time_ms: faker.number.int({ min: 300, max: 600 }),
        result_count: resultEntities.length
      }
    })
  }),
  
  // Graph traversal
  http.get('/api/v1/relationships/graph/traversal', async ({ request }) => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, faker.number.int({ min: 400, max: 800 })))
    
    const url = new URL(request.url)
    const startEntity = url.searchParams.get('start_entity')
    const maxDepth = parseInt(url.searchParams.get('max_depth') || '3')
    
    if (!startEntity) {
      return HttpResponse.json(
        {
          error: 'Validation error',
          message: 'start_entity is required'
        },
        { status: 400 }
      )
    }
    
    // Find start entity
    const start = mockEntities.find(e => e.id === startEntity)
    if (!start) {
      return HttpResponse.json(
        {
          error: 'Not found',
          message: 'Start entity not found'
        },
        { status: 404 }
      )
    }
    
    // Mock traversal - get relationships and connected entities
    const visited = new Set<string>([startEntity])
    const entities = [start]
    const relationships: EntityRelationship[] = []
    
    // Simple BFS traversal simulation
    let currentLevel = [startEntity]
    for (let depth = 0; depth < maxDepth && currentLevel.length > 0; depth++) {
      const nextLevel: string[] = []
      
      for (const entityId of currentLevel) {
        const entityRels = getRelationshipsForEntity(entityId).slice(0, 5)
        
        for (const rel of entityRels) {
          relationships.push(rel)
          
          // Add connected entities
          const connectedId = rel.source_entity_id === entityId 
            ? rel.target_entity_id 
            : rel.source_entity_id
          
          if (!visited.has(connectedId)) {
            visited.add(connectedId)
            const connectedEntity = mockEntities.find(e => e.id === connectedId)
            if (connectedEntity) {
              entities.push(connectedEntity)
              nextLevel.push(connectedId)
            }
          }
        }
      }
      
      currentLevel = nextLevel.slice(0, 10) // Limit breadth
    }
    
    return HttpResponse.json({
      start_entity: start,
      entities,
      relationships,
      depth_reached: Math.min(maxDepth, 3),
      total_nodes: entities.length,
      total_edges: relationships.length
    })
  })
]

