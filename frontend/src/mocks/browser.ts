import { setupWorker } from 'msw/browser'
import { authHandlers } from './handlers/auth'
import { entityHandlers } from './handlers/entities'
import { relationshipHandlers } from './handlers/relationships'
import { feedHandlers } from './handlers/feed'

// Combine all handlers
export const handlers = [
  ...authHandlers,
  ...entityHandlers,
  ...relationshipHandlers,
  ...feedHandlers
]

// Setup the Service Worker with all handlers
export const worker = setupWorker(...handlers)

// Log when MSW is active
console.log('🔧 MSW (Mock Service Worker) initialized with', handlers.length, 'handlers')














