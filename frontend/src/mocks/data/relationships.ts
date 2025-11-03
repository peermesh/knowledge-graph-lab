import { faker } from '@faker-js/faker'
import type { EntityRelationship } from '@/types'
import { mockEntities } from './entities'

const RELATIONSHIP_TYPES = ['fund', 'partner', 'acquire', 'compete', 'collaborate', 'mention'] as const

export function generateRelationship(): EntityRelationship {
  // Pick two random entities
  const sourceEntity = faker.helpers.arrayElement(mockEntities)
  const targetEntity = faker.helpers.arrayElement(mockEntities.filter(e => e.id !== sourceEntity.id))
  
  const relationshipType = faker.helpers.arrayElement(RELATIONSHIP_TYPES)
  const confidence = faker.number.float({ min: 0.5, max: 1.0, fractionDigits: 2 })
  
  return {
    id: faker.string.uuid(),
    source_entity_id: sourceEntity.id,
    target_entity_id: targetEntity.id,
    relationship_type: relationshipType,
    confidence,
    strength: faker.number.float({ min: 0.3, max: 1.0, fractionDigits: 2 }),
    evidence: faker.lorem.sentence(),
    temporal_context: Math.random() > 0.5 ? {
      start_date: faker.date.past({ years: 2 }).toISOString(),
      end_date: Math.random() > 0.7 ? faker.date.recent({ days: 30 }).toISOString() : undefined,
      duration_days: faker.number.int({ min: 30, max: 730 })
    } : undefined,
    metadata: {
      source: faker.internet.url(),
      context: faker.lorem.paragraph(),
      verified: faker.datatype.boolean({ probability: 0.7 })
    },
    created_at: faker.date.recent({ days: 90 }).toISOString(),
    updated_at: faker.date.recent({ days: 30 }).toISOString()
  }
}

export function generateRelationships(count: number): EntityRelationship[] {
  // Use same seed as entities for consistency
  faker.seed(12345)
  const relationships = Array.from({ length: count }, generateRelationship)
  // Reset seed to allow subsequent calls
  faker.seed(12345)
  return relationships
}

// Lazy generation - only create when first accessed
let _mockRelationships: EntityRelationship[] | null = null

function ensureMockRelationships(): EntityRelationship[] {
  if (!_mockRelationships) {
    console.log('Generating 2,000 mock relationships...')
    _mockRelationships = generateRelationships(2000)
    console.log(`✓ Generated ${_mockRelationships.length} mock relationships`)
  }
  return _mockRelationships
}

// Initialize immediately (but with smaller dataset)
console.log('Initializing mock relationships...')
export const mockRelationships = ensureMockRelationships()

// Helper functions
export function getRelationshipsForEntity(entityId: string, direction: 'source' | 'target' | 'both' = 'both'): EntityRelationship[] {
  if (direction === 'source') {
    return mockRelationships.filter(r => r.source_entity_id === entityId)
  } else if (direction === 'target') {
    return mockRelationships.filter(r => r.target_entity_id === entityId)
  } else {
    return mockRelationships.filter(r => 
      r.source_entity_id === entityId || r.target_entity_id === entityId
    )
  }
}

export function getRelationshipsByType(type: EntityRelationship['relationship_type']): EntityRelationship[] {
  return mockRelationships.filter(r => r.relationship_type === type)
}

export function getRandomRelationship(): EntityRelationship {
  return faker.helpers.arrayElement(mockRelationships)
}

