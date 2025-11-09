import { describe, it, expect } from 'vitest'
import { generateRelationship, generateRelationships, mockRelationships, getRelationshipsForEntity, getRelationshipsByType, getRandomRelationship } from './relationships'
import { mockEntities } from './entities'

describe('Relationship Data Generators', () => {
  describe('generateRelationship', () => {
    it('generates a valid relationship', () => {
      const relationship = generateRelationship()
      
      expect(relationship).toHaveProperty('id')
      expect(relationship).toHaveProperty('source_entity_id')
      expect(relationship).toHaveProperty('target_entity_id')
      expect(relationship).toHaveProperty('relationship_type')
      expect(relationship).toHaveProperty('confidence')
      expect(relationship).toHaveProperty('strength')
      expect(relationship).toHaveProperty('evidence')
      expect(relationship).toHaveProperty('metadata')
      expect(relationship).toHaveProperty('created_at')
      expect(relationship).toHaveProperty('updated_at')
    })

    it('generates relationship with valid type', () => {
      const relationship = generateRelationship()
      const validTypes = ['fund', 'partner', 'acquire', 'compete', 'collaborate', 'mention']
      
      expect(validTypes).toContain(relationship.relationship_type)
    })

    it('generates relationship with valid confidence', () => {
      const relationship = generateRelationship()
      
      expect(relationship.confidence).toBeGreaterThanOrEqual(0.5)
      expect(relationship.confidence).toBeLessThanOrEqual(1.0)
    })

    it('generates relationship with valid strength', () => {
      const relationship = generateRelationship()
      
      expect(relationship.strength).toBeGreaterThanOrEqual(0.3)
      expect(relationship.strength).toBeLessThanOrEqual(1.0)
    })

    it('generates relationship with different source and target', () => {
      const relationship = generateRelationship()
      
      expect(relationship.source_entity_id).not.toBe(relationship.target_entity_id)
    })

    it('generates relationship with valid UUID', () => {
      const relationship = generateRelationship()
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i
      
      expect(relationship.id).toMatch(uuidRegex)
    })

    it('references existing entities', () => {
      const relationship = generateRelationship()
      const entityIds = mockEntities.map(e => e.id)
      
      expect(entityIds).toContain(relationship.source_entity_id)
      expect(entityIds).toContain(relationship.target_entity_id)
    })

    it('has evidence text', () => {
      const relationship = generateRelationship()
      
      expect(relationship.evidence).toBeTruthy()
      expect(typeof relationship.evidence).toBe('string')
      expect(relationship.evidence.length).toBeGreaterThan(0)
    })

    it('has metadata object', () => {
      const relationship = generateRelationship()
      
      expect(typeof relationship.metadata).toBe('object')
      expect(relationship.metadata).not.toBeNull()
    })
  })

  describe('generateRelationships', () => {
    it('generates specified number of relationships', () => {
      const count = 10
      const relationships = generateRelationships(count)
      
      expect(relationships).toHaveLength(count)
    })

    it('generates consistent relationships with same seed', () => {
      const relationships1 = generateRelationships(5)
      const relationships2 = generateRelationships(5)
      
      // With seeding, they should be consistent
      expect(relationships1[0].id).toBe(relationships2[0].id)
      expect(relationships1[0].relationship_type).toBe(relationships2[0].relationship_type)
    })

    it('generates empty array for zero count', () => {
      const relationships = generateRelationships(0)
      
      expect(relationships).toHaveLength(0)
    })

    it('generates large number of relationships efficiently', () => {
      const startTime = Date.now()
      const relationships = generateRelationships(1000)
      const endTime = Date.now()
      
      expect(relationships).toHaveLength(1000)
      // Should complete in reasonable time (< 5 seconds)
      expect(endTime - startTime).toBeLessThan(5000)
    })
  })

  describe('mockRelationships', () => {
    it('is pre-generated and available', () => {
      expect(mockRelationships).toBeDefined()
      expect(Array.isArray(mockRelationships)).toBe(true)
      expect(mockRelationships.length).toBeGreaterThan(0)
    })

    it('contains 2000 relationships', () => {
      expect(mockRelationships).toHaveLength(2000)
    })

    it('has all valid relationships', () => {
      mockRelationships.forEach(rel => {
        expect(rel).toHaveProperty('id')
        expect(rel).toHaveProperty('source_entity_id')
        expect(rel).toHaveProperty('target_entity_id')
        expect(rel).toHaveProperty('relationship_type')
      })
    })

    it('contains diverse relationship types', () => {
      const types = new Set(mockRelationships.map(r => r.relationship_type))
      
      // Should have multiple types
      expect(types.size).toBeGreaterThan(1)
    })

    it('all relationships reference valid entities', () => {
      const entityIds = new Set(mockEntities.map(e => e.id))
      
      mockRelationships.forEach(rel => {
        expect(entityIds.has(rel.source_entity_id)).toBe(true)
        expect(entityIds.has(rel.target_entity_id)).toBe(true)
      })
    })
  })

  describe('getRandomRelationship', () => {
    it('returns a relationship from mockRelationships', () => {
      const relationship = getRandomRelationship()
      
      expect(mockRelationships).toContain(relationship)
    })

    it('returns different relationships on multiple calls', () => {
      const rel1 = getRandomRelationship()
      const rel2 = getRandomRelationship()
      const rel3 = getRandomRelationship()
      
      // With 2000 relationships, high chance of getting different ones
      const allSame = rel1.id === rel2.id && rel2.id === rel3.id
      expect(allSame).toBe(false)
    })

    it('returns valid relationship structure', () => {
      const relationship = getRandomRelationship()
      
      expect(relationship).toHaveProperty('id')
      expect(relationship).toHaveProperty('source_entity_id')
      expect(relationship).toHaveProperty('target_entity_id')
    })
  })

  describe('getRelationshipsForEntity', () => {
    it('returns relationships for source entities', () => {
      const entityId = mockRelationships[0].source_entity_id
      const relationships = getRelationshipsForEntity(entityId, 'source')
      
      relationships.forEach(rel => {
        expect(rel.source_entity_id).toBe(entityId)
      })
    })

    it('returns relationships for target entities', () => {
      const entityId = mockRelationships[0].target_entity_id
      const relationships = getRelationshipsForEntity(entityId, 'target')
      
      relationships.forEach(rel => {
        expect(rel.target_entity_id).toBe(entityId)
      })
    })

    it('returns relationships for both directions', () => {
      const entityId = mockRelationships[0].source_entity_id
      const relationships = getRelationshipsForEntity(entityId, 'both')
      
      relationships.forEach(rel => {
        const isSource = rel.source_entity_id === entityId
        const isTarget = rel.target_entity_id === entityId
        expect(isSource || isTarget).toBe(true)
      })
    })

    it('defaults to both directions', () => {
      const entityId = mockRelationships[0].source_entity_id
      const relationshipsDefault = getRelationshipsForEntity(entityId)
      const relationshipsBoth = getRelationshipsForEntity(entityId, 'both')
      
      expect(relationshipsDefault.length).toBe(relationshipsBoth.length)
    })

    it('returns empty array for non-existent entity', () => {
      const relationships = getRelationshipsForEntity('non-existent-id')
      
      expect(relationships).toHaveLength(0)
    })

    it('returns array for valid entity', () => {
      const entityId = mockEntities[0].id
      const relationships = getRelationshipsForEntity(entityId)
      
      expect(Array.isArray(relationships)).toBe(true)
    })
  })

  describe('getRelationshipsByType', () => {
    it('returns only relationships of specified type', () => {
      const fundRels = getRelationshipsByType('fund')
      
      fundRels.forEach(rel => {
        expect(rel.relationship_type).toBe('fund')
      })
    })

    it('returns array for valid types', () => {
      const types = ['fund', 'partner', 'acquire', 'compete', 'collaborate', 'mention']
      
      types.forEach(type => {
        const relationships = getRelationshipsByType(type as any)
        expect(Array.isArray(relationships)).toBe(true)
      })
    })

    it('returns empty array for non-existent type', () => {
      // @ts-expect-error - testing invalid type
      const invalid = getRelationshipsByType('invalid_type')
      
      expect(Array.isArray(invalid)).toBe(true)
      expect(invalid).toHaveLength(0)
    })

    it('returns results for each valid type', () => {
      const types = ['fund', 'partner', 'acquire', 'compete', 'collaborate', 'mention']
      
      types.forEach(type => {
        const relationships = getRelationshipsByType(type as any)
        expect(relationships.length).toBeGreaterThan(0)
      })
    })
  })

  describe('Relationship Type Distribution', () => {
    it('has reasonable distribution of types', () => {
      const typeCounts: Record<string, number> = {}
      
      mockRelationships.forEach(rel => {
        typeCounts[rel.relationship_type] = (typeCounts[rel.relationship_type] || 0) + 1
      })
      
      // Should have relationships of each type
      const types = Object.keys(typeCounts)
      expect(types.length).toBeGreaterThan(3)
      
      // Each type should have at least some relationships
      Object.values(typeCounts).forEach(count => {
        expect(count).toBeGreaterThan(0)
      })
    })
  })

  describe('Data Quality', () => {
    it('all relationships have valid timestamps', () => {
      mockRelationships.forEach(rel => {
        const created = new Date(rel.created_at)
        const updated = new Date(rel.updated_at)
        
        expect(created.getTime()).not.toBeNaN()
        expect(updated.getTime()).not.toBeNaN()
        expect(updated.getTime()).toBeGreaterThanOrEqual(created.getTime())
      })
    })

    it('all relationships have non-empty evidence', () => {
      mockRelationships.forEach(rel => {
        expect(rel.evidence).toBeTruthy()
        expect(rel.evidence.length).toBeGreaterThan(0)
      })
    })

    it('all relationships have different source and target', () => {
      mockRelationships.forEach(rel => {
        expect(rel.source_entity_id).not.toBe(rel.target_entity_id)
      })
    })

    it('temporal context is valid when present', () => {
      mockRelationships.forEach(rel => {
        if (rel.temporal_context) {
          expect(rel.temporal_context.start_date).toBeTruthy()
          
          if (rel.temporal_context.end_date) {
            const start = new Date(rel.temporal_context.start_date)
            const end = new Date(rel.temporal_context.end_date)
            expect(end.getTime()).toBeGreaterThanOrEqual(start.getTime())
          }
          
          if (rel.temporal_context.duration_days) {
            expect(rel.temporal_context.duration_days).toBeGreaterThan(0)
          }
        }
      })
    })
  })

  describe('Graph Structure', () => {
    it('creates connected graph', () => {
      // Check that entities are connected
      const connectedEntities = new Set<string>()
      
      mockRelationships.forEach(rel => {
        connectedEntities.add(rel.source_entity_id)
        connectedEntities.add(rel.target_entity_id)
      })
      
      // Most entities should be connected
      expect(connectedEntities.size).toBeGreaterThan(mockEntities.length * 0.5)
    })

    it('has no self-loops', () => {
      const selfLoops = mockRelationships.filter(rel => 
        rel.source_entity_id === rel.target_entity_id
      )
      
      expect(selfLoops).toHaveLength(0)
    })

    it('some entities have multiple relationships', () => {
      const entityRelCounts: Record<string, number> = {}
      
      mockRelationships.forEach(rel => {
        entityRelCounts[rel.source_entity_id] = (entityRelCounts[rel.source_entity_id] || 0) + 1
        entityRelCounts[rel.target_entity_id] = (entityRelCounts[rel.target_entity_id] || 0) + 1
      })
      
      const multipleRelEntities = Object.values(entityRelCounts).filter(count => count > 1)
      expect(multipleRelEntities.length).toBeGreaterThan(0)
    })
  })
})

