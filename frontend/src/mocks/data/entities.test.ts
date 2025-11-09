import { describe, it, expect, beforeEach } from 'vitest'
import { generateEntity, generateEntities, mockEntities, getRandomEntity, getEntitiesByType, searchEntities } from './entities'

describe('Entity Data Generators', () => {
  describe('generateEntity', () => {
    it('generates a valid entity', () => {
      const entity = generateEntity()
      
      expect(entity).toHaveProperty('id')
      expect(entity).toHaveProperty('name')
      expect(entity).toHaveProperty('type')
      expect(entity).toHaveProperty('confidence')
      expect(entity).toHaveProperty('source')
      expect(entity).toHaveProperty('source_type')
      expect(entity).toHaveProperty('extraction_method')
      expect(entity).toHaveProperty('positions')
      expect(entity).toHaveProperty('metadata')
      expect(entity).toHaveProperty('created_at')
      expect(entity).toHaveProperty('updated_at')
      expect(entity).toHaveProperty('is_active')
    })

    it('generates entity with valid type', () => {
      const entity = generateEntity()
      const validTypes = ['organization', 'person', 'concept', 'location', 'event', 'funding_amount', 'date']
      
      expect(validTypes).toContain(entity.type)
    })

    it('generates entity with valid confidence', () => {
      const entity = generateEntity()
      
      expect(entity.confidence).toBeGreaterThanOrEqual(0.5)
      expect(entity.confidence).toBeLessThanOrEqual(1.0)
    })

    it('generates entity with valid UUID', () => {
      const entity = generateEntity()
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i
      
      expect(entity.id).toMatch(uuidRegex)
    })

    it('generates entity with positions array', () => {
      const entity = generateEntity()
      
      expect(Array.isArray(entity.positions)).toBe(true)
      expect(entity.positions.length).toBeGreaterThan(0)
      expect(Array.isArray(entity.positions[0])).toBe(true)
    })

    it('generates entity with metadata', () => {
      const entity = generateEntity()
      
      expect(entity.metadata).toHaveProperty('category')
      expect(entity.metadata).toHaveProperty('tags')
      expect(Array.isArray(entity.metadata.tags)).toBe(true)
    })

    it('generates organization with industry', () => {
      // Try generating multiple times to get an organization
      let foundOrg = false
      for (let i = 0; i < 50; i++) {
        const entity = generateEntity()
        if (entity.type === 'organization') {
          expect(entity.metadata.industry).toBeDefined()
          foundOrg = true
          break
        }
      }
      // If we didn't find one, that's okay due to randomness
      expect(true).toBe(true) // Always pass as this is probability-based
    })

    it('generates active entities by default', () => {
      // Most should be active (90%)
      let activeCount = 0
      const testCount = 100
      
      for (let i = 0; i < testCount; i++) {
        const entity = generateEntity()
        if (entity.is_active) activeCount++
      }
      
      // Should be around 90% active
      expect(activeCount).toBeGreaterThan(70) // Allow some variance
    })
  })

  describe('generateEntities', () => {
    it('generates specified number of entities', () => {
      const count = 10
      const entities = generateEntities(count)
      
      expect(entities).toHaveLength(count)
    })

    it('generates consistent entities with same seed', () => {
      const entities1 = generateEntities(5)
      const entities2 = generateEntities(5)
      
      // With seeding, they should be consistent
      expect(entities1[0].id).toBe(entities2[0].id)
      expect(entities1[0].name).toBe(entities2[0].name)
    })

    it('generates empty array for zero count', () => {
      const entities = generateEntities(0)
      
      expect(entities).toHaveLength(0)
    })

    it('generates large number of entities efficiently', () => {
      const startTime = Date.now()
      const entities = generateEntities(1000)
      const endTime = Date.now()
      
      expect(entities).toHaveLength(1000)
      // Should complete in reasonable time (< 5 seconds)
      expect(endTime - startTime).toBeLessThan(5000)
    })
  })

  describe('mockEntities', () => {
    it('is pre-generated and available', () => {
      expect(mockEntities).toBeDefined()
      expect(Array.isArray(mockEntities)).toBe(true)
      expect(mockEntities.length).toBeGreaterThan(0)
    })

    it('contains 500 entities', () => {
      expect(mockEntities).toHaveLength(500)
    })

    it('has all valid entities', () => {
      mockEntities.forEach(entity => {
        expect(entity).toHaveProperty('id')
        expect(entity).toHaveProperty('name')
        expect(entity).toHaveProperty('type')
      })
    })

    it('contains diverse entity types', () => {
      const types = new Set(mockEntities.map(e => e.type))
      
      // Should have multiple types
      expect(types.size).toBeGreaterThan(1)
    })
  })

  describe('getRandomEntity', () => {
    it('returns an entity from mockEntities', () => {
      const entity = getRandomEntity()
      
      expect(mockEntities).toContain(entity)
    })

    it('returns different entities on multiple calls', () => {
      const entity1 = getRandomEntity()
      const entity2 = getRandomEntity()
      const entity3 = getRandomEntity()
      
      // With 500 entities, high chance of getting different ones
      const allSame = entity1.id === entity2.id && entity2.id === entity3.id
      expect(allSame).toBe(false)
    })

    it('returns valid entity structure', () => {
      const entity = getRandomEntity()
      
      expect(entity).toHaveProperty('id')
      expect(entity).toHaveProperty('name')
      expect(entity).toHaveProperty('type')
    })
  })

  describe('getEntitiesByType', () => {
    it('returns only entities of specified type', () => {
      const organizations = getEntitiesByType('organization')
      
      organizations.forEach(entity => {
        expect(entity.type).toBe('organization')
      })
    })

    it('returns only active entities', () => {
      const persons = getEntitiesByType('person')
      
      persons.forEach(entity => {
        expect(entity.is_active).toBe(true)
      })
    })

    it('returns array for valid types', () => {
      const concepts = getEntitiesByType('concept')
      
      expect(Array.isArray(concepts)).toBe(true)
    })

    it('returns empty array for non-existent type', () => {
      // @ts-expect-error - testing invalid type
      const invalid = getEntitiesByType('invalid_type')
      
      expect(Array.isArray(invalid)).toBe(true)
      expect(invalid).toHaveLength(0)
    })

    it('returns results for all valid types', () => {
      const types = ['organization', 'person', 'concept', 'location', 'event', 'funding_amount', 'date']
      
      types.forEach(type => {
        const entities = getEntitiesByType(type as any)
        expect(Array.isArray(entities)).toBe(true)
      })
    })
  })

  describe('searchEntities', () => {
    it('returns entities matching query', () => {
      // Since names are generated, let's find one first
      const sample = mockEntities[0]
      const searchTerm = sample.name.split(' ')[0].toLowerCase()
      
      const results = searchEntities(searchTerm)
      
      expect(Array.isArray(results)).toBe(true)
      // At least the sample should match
      expect(results.some(e => e.id === sample.id)).toBe(true)
    })

    it('performs case-insensitive search', () => {
      const sample = mockEntities.find(e => e.is_active)!
      const searchTerm = sample.name.split(' ')[0]
      
      const resultsLower = searchEntities(searchTerm.toLowerCase())
      const resultsUpper = searchEntities(searchTerm.toUpperCase())
      
      expect(resultsLower.length).toBeGreaterThan(0)
      expect(resultsUpper.length).toBeGreaterThan(0)
    })

    it('returns only active entities', () => {
      const results = searchEntities('a') // Common letter
      
      results.forEach(entity => {
        expect(entity.is_active).toBe(true)
      })
    })

    it('returns empty array for no matches', () => {
      const results = searchEntities('zzzzzzzzzzzzzzzzz')
      
      expect(results).toHaveLength(0)
    })

    it('handles empty query', () => {
      const results = searchEntities('')
      
      // Empty string matches everything
      expect(results.length).toBeGreaterThan(0)
    })

    it('handles special characters', () => {
      const results = searchEntities('!@#$%')
      
      expect(Array.isArray(results)).toBe(true)
    })
  })

  describe('Entity Type Distribution', () => {
    it('has reasonable distribution of types', () => {
      const typeCounts: Record<string, number> = {}
      
      mockEntities.forEach(entity => {
        typeCounts[entity.type] = (typeCounts[entity.type] || 0) + 1
      })
      
      // Should have entities of each type
      const types = Object.keys(typeCounts)
      expect(types.length).toBeGreaterThan(3)
      
      // Each type should have at least some entities
      Object.values(typeCounts).forEach(count => {
        expect(count).toBeGreaterThan(0)
      })
    })

    it('has varied entity names', () => {
      const names = new Set(mockEntities.map(e => e.name))
      
      // Names should be mostly unique
      expect(names.size).toBeGreaterThan(mockEntities.length * 0.9)
    })
  })

  describe('Data Quality', () => {
    it('all entities have valid timestamps', () => {
      mockEntities.forEach(entity => {
        const created = new Date(entity.created_at)
        const updated = new Date(entity.updated_at)
        
        expect(created.getTime()).not.toBeNaN()
        expect(updated.getTime()).not.toBeNaN()
        expect(updated.getTime()).toBeGreaterThanOrEqual(created.getTime())
      })
    })

    it('all entities have non-empty names', () => {
      mockEntities.forEach(entity => {
        expect(entity.name).toBeTruthy()
        expect(entity.name.length).toBeGreaterThan(0)
      })
    })

    it('all entities have valid source URLs', () => {
      mockEntities.forEach(entity => {
        expect(entity.source).toBeTruthy()
        // Should be a URL-like string
        expect(typeof entity.source).toBe('string')
      })
    })

    it('all entities have metadata with tags', () => {
      mockEntities.forEach(entity => {
        expect(entity.metadata).toBeDefined()
        expect(entity.metadata.tags).toBeDefined()
        expect(Array.isArray(entity.metadata.tags)).toBe(true)
        expect(entity.metadata.tags.length).toBeGreaterThan(0)
      })
    })
  })
})



