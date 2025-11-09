import { faker } from '@faker-js/faker'
import type { ResearchItem } from '@/types'
import { mockUsers } from './users'
import { mockEntities } from './entities'

const CONTENT_TYPES = ['article', 'insight', 'alert', 'newsletter'] as const

export function generateResearchItem(): ResearchItem {
  const contentType = faker.helpers.arrayElement(CONTENT_TYPES)
  
  // Pick random entities for tags
  const numTags = faker.number.int({ min: 2, max: 8 })
  const taggedEntities = faker.helpers.arrayElements(mockEntities, numTags)
  const entity_tags = taggedEntities.map(e => e.name)
  
  // Generate topics
  const topics = Array.from(
    { length: faker.number.int({ min: 2, max: 5 }) }, 
    () => faker.helpers.arrayElement([
      'AI & Machine Learning',
      'Healthcare Innovation',
      'Financial Technology',
      'Climate & Sustainability',
      'Biotechnology',
      'Quantum Computing',
      'Space Technology',
      'Cybersecurity',
      'Blockchain',
      'Robotics',
      'Clean Energy',
      'EdTech'
    ])
  )
  
  const user = faker.helpers.arrayElement(mockUsers)
  
  return {
    id: faker.string.uuid(),
    title: faker.helpers.arrayElement([
      `${faker.company.name()} ${faker.helpers.arrayElement(['Announces', 'Launches', 'Develops', 'Partners with'])} ${faker.company.buzzPhrase()}`,
      `Breakthrough in ${faker.commerce.department()}: ${faker.company.catchPhrase()}`,
      `${faker.person.fullName()} ${faker.helpers.arrayElement(['Leads', 'Joins', 'Invests in'])} ${faker.company.buzzNoun()} Initiative`,
      `New Study Shows ${faker.company.buzzPhrase()}`,
      `${faker.location.city()} Becomes Hub for ${faker.commerce.department()}`
    ]),
    summary: faker.lorem.paragraph({ min: 2, max: 4 }),
    content_type: contentType,
    content_body: Math.random() > 0.3 ? faker.lorem.paragraphs({ min: 3, max: 8 }, '\n\n') : undefined,
    quality_score: faker.number.float({ min: 0.4, max: 1.0, fractionDigits: 2 }),
    relevance_score: faker.number.float({ min: 0.3, max: 1.0, fractionDigits: 2 }),
    entity_tags,
    topics: Array.from(new Set(topics)), // Remove duplicates
    source_url: faker.internet.url(),
    published_at: faker.date.recent({ days: 60 }).toISOString(),
    created_at: faker.date.recent({ days: 30 }).toISOString(),
    updated_at: faker.date.recent({ days: 15 }).toISOString(),
    created_by: user.id,
    is_active: faker.datatype.boolean({ probability: 0.95 }) // 95% active
  }
}

export function generateResearchItems(count: number): ResearchItem[] {
  // Seed for consistency
  faker.seed(13579)
  const items = Array.from({ length: count }, generateResearchItem)
  // Reset seed
  faker.seed()
  
  // Sort by published_at descending (newest first)
  return items.sort((a, b) => 
    new Date(b.published_at).getTime() - new Date(a.published_at).getTime()
  )
}

// Pre-generate 1,000 research items
console.log('Generating 1,000 mock research items...')
export const mockResearchItems = generateResearchItems(1000)
console.log(`✓ Generated ${mockResearchItems.length} mock research items`)

// Helper functions
export function getResearchItemsByType(type: ResearchItem['content_type']): ResearchItem[] {
  return mockResearchItems.filter(r => r.content_type === type && r.is_active)
}

export function getResearchItemsByTopic(topic: string): ResearchItem[] {
  return mockResearchItems.filter(r => 
    r.is_active && r.topics.includes(topic)
  )
}

export function searchResearchItems(query: string): ResearchItem[] {
  const lowerQuery = query.toLowerCase()
  return mockResearchItems.filter(r => 
    r.is_active && (
      r.title.toLowerCase().includes(lowerQuery) ||
      r.summary.toLowerCase().includes(lowerQuery) ||
      r.topics.some(t => t.toLowerCase().includes(lowerQuery))
    )
  )
}

export function getTopResearchItems(limit: number = 20): ResearchItem[] {
  return mockResearchItems
    .filter(r => r.is_active)
    .sort((a, b) => b.quality_score * b.relevance_score - a.quality_score * a.relevance_score)
    .slice(0, limit)
}

export function getRandomResearchItem(): ResearchItem {
  return faker.helpers.arrayElement(mockResearchItems.filter(r => r.is_active))
}














