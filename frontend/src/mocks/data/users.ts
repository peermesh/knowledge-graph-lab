import { faker } from '@faker-js/faker'
import type { User } from '@/types'

const ROLES = ['user', 'admin', 'moderator', 'researcher'] as const

export function generateUser(): User {
  const firstName = faker.person.firstName()
  const lastName = faker.person.lastName()
  const email = faker.internet.email({ firstName, lastName }).toLowerCase()
  
  return {
    id: faker.string.uuid(),
    email,
    first_name: firstName,
    last_name: lastName,
    role: faker.helpers.arrayElement(ROLES),
    is_active: faker.datatype.boolean({ probability: 0.95 }), // 95% active
    created_at: faker.date.past({ years: 2 }).toISOString(),
    updated_at: faker.date.recent({ days: 30 }).toISOString(),
    last_login: Math.random() > 0.3 ? faker.date.recent({ days: 7 }).toISOString() : undefined
  }
}

export function generateUsers(count: number): User[] {
  // Seed for consistency
  faker.seed(67890)
  const users = Array.from({ length: count }, generateUser)
  // Reset seed
  faker.seed()
  return users
}

// Pre-generate 100 users
console.log('Generating 100 mock users...')
export const mockUsers = generateUsers(100)

// Add a default admin user for testing
mockUsers.unshift({
  id: 'admin-test-user',
  email: 'admin@test.com',
  first_name: 'Admin',
  last_name: 'User',
  role: 'admin',
  is_active: true,
  created_at: new Date('2023-01-01').toISOString(),
  updated_at: new Date().toISOString(),
  last_login: new Date().toISOString()
})

// Add a default regular user for testing
mockUsers.unshift({
  id: 'regular-test-user',
  email: 'user@test.com',
  first_name: 'Test',
  last_name: 'User',
  role: 'user',
  is_active: true,
  created_at: new Date('2023-01-01').toISOString(),
  updated_at: new Date().toISOString(),
  last_login: new Date().toISOString()
})

console.log(`✓ Generated ${mockUsers.length} mock users`)

// Helper functions
export function getUserByEmail(email: string): User | undefined {
  return mockUsers.find(u => u.email.toLowerCase() === email.toLowerCase())
}

export function getUserById(id: string): User | undefined {
  return mockUsers.find(u => u.id === id)
}

export function getActiveUsers(): User[] {
  return mockUsers.filter(u => u.is_active)
}

export function getUsersByRole(role: User['role']): User[] {
  return mockUsers.filter(u => u.role === role && u.is_active)
}

export function getRandomUser(): User {
  return faker.helpers.arrayElement(mockUsers)
}














