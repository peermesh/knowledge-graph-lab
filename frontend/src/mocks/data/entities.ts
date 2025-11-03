import { faker } from '@faker-js/faker'
import type { Entity } from '@/types'

const ENTITY_TYPES = ['organization', 'person', 'concept', 'location', 'event', 'funding_amount', 'date'] as const

export function generateEntity(): Entity {
  const type = faker.helpers.arrayElement(ENTITY_TYPES)
  
  let name: string
  switch (type) {
    case 'organization':
      name = faker.company.name()
      break
    case 'person':
      name = faker.person.fullName()
      break
    case 'location':
      name = faker.location.city() + ', ' + faker.location.country()
      break
    case 'date':
      name = faker.date.recent({ days: 365 }).toISOString().split('T')[0]
      break
    case 'funding_amount':
      name = '$' + faker.finance.amount({ min: 100000, max: 100000000, dec: 0 })
      break
    default:
      name = faker.commerce.productName()
  }
  
  return {
    id: faker.string.uuid(),
    name,
    type,
    confidence: faker.number.float({ min: 0.5, max: 1.0, fractionDigits: 2 }),
    source: faker.internet.url(),
    source_type: faker.helpers.arrayElement(['web', 'api', 'manual', 'extraction']),
    extraction_method: 'mock_generator',
    positions: [[faker.number.int({ min: 0, max: 1000 }), faker.number.int({ min: 0, max: 100 })]],
    metadata: {
      category: faker.commerce.department(),
      tags: Array.from({ length: faker.number.int({ min: 1, max: 5 }) }, 
        () => faker.word.noun()),
      industry: type === 'organization' ? faker.company.buzzNoun() : undefined,
      location: type === 'person' || type === 'organization' ? faker.location.city() : undefined
    },
    created_at: faker.date.recent({ days: 90 }).toISOString(),
    updated_at: faker.date.recent({ days: 30 }).toISOString(),
    is_active: faker.datatype.boolean({ probability: 0.9 }) // 90% active
  }
}

export function generateEntities(count: number): Entity[] {
  // Seed for consistency during development
  faker.seed(12345)
  const entities = Array.from({ length: count }, generateEntity)
  // Reset seed to allow subsequent calls
  faker.seed(12345)
  return entities
}

// Lazy generation - only create when first accessed
let _mockEntities: Entity[] | null = null

function ensureMockEntities(): Entity[] {
  if (!_mockEntities) {
    console.log('Generating 500 mock entities...')
    _mockEntities = generateEntities(500)
    console.log(`✓ Generated ${_mockEntities.length} mock entities`)
  }
  return _mockEntities
}

// Initialize immediately (but with smaller dataset)
console.log('Initializing mock entities...')
export const mockEntities = ensureMockEntities()

// Helper to get random entity
export function getRandomEntity(): Entity {
  return faker.helpers.arrayElement(mockEntities)
}

// Helper to get entities by type
export function getEntitiesByType(type: Entity['type']): Entity[] {
  return mockEntities.filter(e => e.type === type && e.is_active)
}

// Helper to search entities
export function searchEntities(query: string): Entity[] {
  const lowerQuery = query.toLowerCase()
  return mockEntities.filter(e => 
    e.is_active && e.name.toLowerCase().includes(lowerQuery)
  )
}

