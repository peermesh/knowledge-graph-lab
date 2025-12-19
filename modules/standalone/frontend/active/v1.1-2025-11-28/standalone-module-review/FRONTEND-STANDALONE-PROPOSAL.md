# Frontend Standalone Module - Production Readiness Proposal

**Date:** November 3, 2025  
**Status:** 📋 AWAITING APPROVAL  
**Version:** 2.0 (Corrected Scope)  
**Module:** Frontend Only - No Backend Modifications

---

## 🎯 Executive Summary

Transform the Knowledge Graph Lab frontend into a **fully functioning, production-ready standalone module** that operates independently with zero backend dependencies. The module will use API mocking, client-side data generation, and simulated real-time capabilities to create a complete, deployable frontend experience.

**Timeline:** 4 weeks  
**Team:** 1-2 frontend developers  
**Scope:** `frontend/` directory only  
**Backend Required:** None

---

## 📊 Current State Assessment

### ✅ What Works:
- React + TypeScript foundation
- Component architecture (Layout, Feed, Graph, etc.)
- Zustand state management
- Tailwind CSS styling
- Vite build system
- Basic Docker setup

### ❌ Critical Gaps for Standalone Operation:

1. **No Mock API Layer**
   - Services expect real backend
   - No offline development capability
   - Can't demo without backend running

2. **No Realistic Data**
   - Empty initial state
   - Hardcoded mock data in components
   - No data generation system

3. **No Simulated Real-Time**
   - WebSocket service exists but needs real server
   - No way to simulate live updates
   - Static data only

4. **Incomplete Authentication UI**
   - No Login/Register pages
   - Protected routes not implemented
   - Auth state management incomplete

5. **No Component Documentation**
   - Components not documented
   - No design system reference
   - Hard to develop in isolation

6. **Minimal Test Coverage**
   - Only 4 test files
   - No integration tests
   - No E2E tests

7. **No Production Optimization**
   - Build not optimized
   - No performance monitoring
   - Missing production configs

**Current Standalone Capability:** 20%

---

## 🚀 Solution Overview

### Approach: Mock-First Standalone Architecture

Transform the frontend into a self-contained module that:
- ✅ Generates its own data
- ✅ Mocks all API responses
- ✅ Simulates real-time updates
- ✅ Requires zero backend services
- ✅ Can be deployed as static files
- ✅ Is fully testable in isolation

---

## 📋 Implementation Plan

### **PHASE 1: Mock API Layer & Data Generation** (Week 1)

#### 1.1 Install Dependencies

```bash
npm install --save-dev msw@^2.0.11 @faker-js/faker@^8.3.1
```

**MSW (Mock Service Worker):** Intercepts HTTP requests at network level  
**Faker:** Generates realistic mock data

#### 1.2 Create Mock Infrastructure

**Directory Structure:**
```
frontend/src/mocks/
├── browser.ts              # MSW browser setup
├── handlers/              # API mock handlers
│   ├── auth.ts           # Login, register, logout
│   ├── entities.ts       # Entity CRUD operations
│   ├── relationships.ts  # Relationship operations
│   ├── feed.ts          # Research feed
│   └── users.ts         # User management
└── data/                 # Data generators
    ├── entities.ts       # Generate entities
    ├── relationships.ts  # Generate relationships
    ├── users.ts         # Generate users
    └── research.ts      # Generate research items
```

#### 1.3 Implement Data Generators

**File:** `frontend/src/mocks/data/entities.ts`

```typescript
import { faker } from '@faker-js/faker'
import type { Entity } from '@/types'

const ENTITY_TYPES = ['organization', 'person', 'concept', 'location', 'event'] as const

export function generateEntity(): Entity {
  const type = faker.helpers.arrayElement(ENTITY_TYPES)
  
  return {
    id: faker.string.uuid(),
    name: type === 'organization' ? faker.company.name() 
        : type === 'person' ? faker.person.fullName()
        : faker.commerce.productName(),
    type,
    confidence: faker.number.float({ min: 0.5, max: 1.0, precision: 0.01 }),
    source: faker.internet.url(),
    source_type: faker.helpers.arrayElement(['web', 'api', 'manual']),
    extraction_method: 'mock_generator',
    metadata: {
      category: faker.commerce.department(),
      tags: Array.from({ length: faker.number.int({ min: 1, max: 5 }) }, 
        () => faker.word.noun())
    },
    created_at: faker.date.recent({ days: 90 }).toISOString(),
    updated_at: faker.date.recent({ days: 30 }).toISOString(),
    is_active: faker.datatype.boolean(0.9) // 90% active
  }
}

export function generateEntities(count: number): Entity[] {
  return Array.from({ length: count }, generateEntity)
}

// Pre-generate 10,000 entities
export const mockEntities = generateEntities(10000)
```

**Similar generators for:**
- `relationships.ts` - 50,000 relationships
- `users.ts` - 100 users
- `research.ts` - 1,000 research items

#### 1.4 Implement Mock Handlers

**File:** `frontend/src/mocks/handlers/auth.ts`

```typescript
import { http, HttpResponse } from 'msw'
import { mockUsers } from '../data/users'

export const authHandlers = [
  // Login
  http.post('/api/v1/auth/login', async ({ request }) => {
    const { email, password } = await request.json()
    
    // Simulate auth check
    const user = mockUsers.find(u => u.email === email)
    
    if (!user || password.length < 6) {
      return HttpResponse.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      )
    }
    
    // Generate mock tokens
    const accessToken = `mock_access_${Date.now()}_${user.id}`
    const refreshToken = `mock_refresh_${Date.now()}_${user.id}`
    
    return HttpResponse.json({
      access_token: accessToken,
      refresh_token: refreshToken,
      token_type: 'bearer',
      expires_in: 3600,
      user: {
        id: user.id,
        email: user.email,
        first_name: user.first_name,
        last_name: user.last_name,
        role: user.role
      }
    })
  }),
  
  // Register
  http.post('/api/v1/auth/register', async ({ request }) => {
    const userData = await request.json()
    
    // Simulate delay
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const newUser = {
      id: faker.string.uuid(),
      ...userData,
      role: 'user',
      created_at: new Date().toISOString()
    }
    
    mockUsers.push(newUser)
    
    return HttpResponse.json(newUser, { status: 201 })
  }),
  
  // Refresh token
  http.post('/api/v1/auth/refresh', async ({ request }) => {
    const { refresh_token } = await request.json()
    
    if (!refresh_token || !refresh_token.startsWith('mock_refresh_')) {
      return HttpResponse.json(
        { error: 'Invalid refresh token' },
        { status: 401 }
      )
    }
    
    // Extract user ID from token
    const userId = refresh_token.split('_').pop()
    
    return HttpResponse.json({
      access_token: `mock_access_${Date.now()}_${userId}`,
      token_type: 'bearer',
      expires_in: 3600
    })
  }),
  
  // Get current user
  http.get('/api/v1/auth/me', ({ request }) => {
    const authHeader = request.headers.get('Authorization')
    
    if (!authHeader || !authHeader.startsWith('Bearer mock_access_')) {
      return HttpResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }
    
    // Extract user ID from token
    const token = authHeader.replace('Bearer ', '')
    const userId = token.split('_').pop()
    const user = mockUsers.find(u => u.id === userId)
    
    if (!user) {
      return HttpResponse.json(
        { error: 'User not found' },
        { status: 404 }
      )
    }
    
    return HttpResponse.json(user)
  })
]
```

**File:** `frontend/src/mocks/handlers/entities.ts`

```typescript
import { http, HttpResponse } from 'msw'
import { mockEntities } from '../data/entities'

export const entityHandlers = [
  // Get entities with pagination
  http.get('/api/v1/entities', ({ request }) => {
    const url = new URL(request.url)
    const limit = parseInt(url.searchParams.get('limit') || '20')
    const offset = parseInt(url.searchParams.get('offset') || '0')
    const entityType = url.searchParams.get('entity_type')
    const confidenceMin = parseFloat(url.searchParams.get('confidence_min') || '0')
    
    // Filter
    let filtered = mockEntities.filter(e => 
      e.is_active &&
      e.confidence >= confidenceMin &&
      (!entityType || e.type === entityType)
    )
    
    // Paginate
    const paginated = filtered.slice(offset, offset + limit)
    
    return HttpResponse.json({
      data: paginated,
      pagination: {
        page: Math.floor(offset / limit) + 1,
        page_size: limit,
        total_count: filtered.length,
        has_more: offset + limit < filtered.length
      },
      execution_time_ms: Math.random() * 100 + 50
    })
  }),
  
  // Get single entity
  http.get('/api/v1/entities/:id', ({ params }) => {
    const entity = mockEntities.find(e => e.id === params.id)
    
    if (!entity) {
      return HttpResponse.json(
        { error: 'Entity not found' },
        { status: 404 }
      )
    }
    
    return HttpResponse.json(entity)
  }),
  
  // Create entity
  http.post('/api/v1/entities', async ({ request }) => {
    const data = await request.json()
    
    const newEntity = {
      id: faker.string.uuid(),
      ...data,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      is_active: true
    }
    
    mockEntities.push(newEntity)
    
    return HttpResponse.json(newEntity, { status: 201 })
  }),
  
  // Update entity
  http.put('/api/v1/entities/:id', async ({ params, request }) => {
    const updates = await request.json()
    const index = mockEntities.findIndex(e => e.id === params.id)
    
    if (index === -1) {
      return HttpResponse.json(
        { error: 'Entity not found' },
        { status: 404 }
      )
    }
    
    mockEntities[index] = {
      ...mockEntities[index],
      ...updates,
      updated_at: new Date().toISOString()
    }
    
    return HttpResponse.json(mockEntities[index])
  }),
  
  // Delete entity
  http.delete('/api/v1/entities/:id', ({ params }) => {
    const index = mockEntities.findIndex(e => e.id === params.id)
    
    if (index === -1) {
      return HttpResponse.json(
        { error: 'Entity not found' },
        { status: 404 }
      )
    }
    
    mockEntities[index].is_active = false
    
    return HttpResponse.json({ success: true })
  })
]
```

#### 1.5 Setup MSW

**File:** `frontend/src/mocks/browser.ts`

```typescript
import { setupWorker } from 'msw/browser'
import { authHandlers } from './handlers/auth'
import { entityHandlers } from './handlers/entities'
import { relationshipHandlers } from './handlers/relationships'
import { feedHandlers } from './handlers/feed'

export const worker = setupWorker(
  ...authHandlers,
  ...entityHandlers,
  ...relationshipHandlers,
  ...feedHandlers
)
```

**File:** `frontend/src/main.tsx` (modify)

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

// Start MSW in development
async function enableMocking() {
  if (import.meta.env.DEV) {
    const { worker } = await import('./mocks/browser')
    return worker.start({
      onUnhandledRequest: 'bypass' // Don't warn about unhandled requests
    })
  }
}

enableMocking().then(() => {
  ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  )
})
```

**Deliverables Week 1:**
- ✅ MSW configured and running
- ✅ 10,000 mock entities generated
- ✅ 50,000 mock relationships generated
- ✅ Auth, entity, relationship API endpoints mocked
- ✅ Frontend works without backend

---

### **PHASE 2: Simulated Real-Time & Authentication UI** (Week 2)

#### 2.1 Create Mock WebSocket Service

**File:** `frontend/src/services/mockWebSocket.ts`

```typescript
import { mockEntities } from '@/mocks/data/entities'
import { faker } from '@faker-js/faker'

type MessageHandler = (data: any) => void

export class MockWebSocketService {
  private listeners: Map<string, MessageHandler[]> = new Map()
  private connected: boolean = false
  private simulationInterval: NodeJS.Timeout | null = null
  
  async connect(): Promise<void> {
    // Simulate connection delay
    await new Promise(resolve => setTimeout(resolve, 300))
    
    this.connected = true
    this.emit('system_notification', {
      message: 'Connected to Knowledge Graph Lab (Mock Mode)'
    })
    
    // Start simulating updates
    this.startSimulation()
  }
  
  disconnect(): void {
    this.connected = false
    if (this.simulationInterval) {
      clearInterval(this.simulationInterval)
      this.simulationInterval = null
    }
  }
  
  subscribe(messageType: string, handler: MessageHandler): void {
    if (!this.listeners.has(messageType)) {
      this.listeners.set(messageType, [])
    }
    this.listeners.get(messageType)!.push(handler)
  }
  
  unsubscribe(messageType: string, handler: MessageHandler): void {
    const handlers = this.listeners.get(messageType)
    if (handlers) {
      const index = handlers.indexOf(handler)
      if (index > -1) {
        handlers.splice(index, 1)
      }
    }
  }
  
  private emit(type: string, data: any): void {
    const handlers = this.listeners.get(type) || []
    handlers.forEach(handler => {
      try {
        handler(data)
      } catch (error) {
        console.error(`Error in ${type} handler:`, error)
      }
    })
  }
  
  private startSimulation(): void {
    // Simulate entity updates every 5 seconds
    this.simulationInterval = setInterval(() => {
      if (!this.connected) return
      
      // Random entity update
      if (Math.random() > 0.5) {
        const entity = faker.helpers.arrayElement(mockEntities)
        this.emit('entity_update', {
          entity_id: entity.id,
          action: 'updated',
          entity
        })
      }
      
      // Random graph update
      if (Math.random() > 0.7) {
        this.emit('graph_update', {
          nodes_changed: faker.number.int({ min: 1, max: 5 }),
          edges_changed: faker.number.int({ min: 1, max: 10 })
        })
      }
      
      // Random feed update
      if (Math.random() > 0.8) {
        this.emit('feed_update', {
          new_items: faker.number.int({ min: 1, max: 3 })
        })
      }
    }, 5000)
  }
  
  get isConnected(): boolean {
    return this.connected
  }
  
  get connectionState(): string {
    return this.connected ? 'connected' : 'disconnected'
  }
}

// Export singleton
export const mockWebSocketService = new MockWebSocketService()
```

**File:** `frontend/src/services/websocket.ts` (modify to use mock)

```typescript
import { MockWebSocketService, mockWebSocketService } from './mockWebSocket'

// Use mock in development, real WebSocket in production
export const websocketService = import.meta.env.DEV 
  ? mockWebSocketService 
  : websocketService // original implementation
```

#### 2.2 Build Authentication Pages

**File:** `frontend/src/pages/Login/LoginPage.tsx`

```typescript
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/Common/Button'
import { Input } from '@/components/Common/Input'
import { api } from '@/services/api'
import { useUserStore } from '@/store/useUserStore'

export function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  
  const navigate = useNavigate()
  const setUser = useUserStore(state => state.setUser)
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    
    try {
      const response = await api.login(email, password)
      
      // Store tokens
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)
      
      // Update user state
      setUser(response.user)
      
      // Navigate to feed
      navigate('/feed')
    } catch (err: any) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-lg">
        <div>
          <h2 className="text-3xl font-bold text-center">
            Knowledge Graph Lab
          </h2>
          <p className="mt-2 text-center text-gray-600">
            Sign in to your account
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
              {error}
            </div>
          )}
          
          <div className="space-y-4">
            <Input
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
            
            <Input
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
          </div>
          
          <Button
            type="submit"
            className="w-full"
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </Button>
          
          <div className="text-center">
            <a href="/register" className="text-blue-600 hover:text-blue-500">
              Don't have an account? Register
            </a>
          </div>
        </form>
        
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded">
          <p className="text-sm text-blue-800 font-semibold">Demo Mode</p>
          <p className="text-xs text-blue-600 mt-1">
            Use any email and password (min 6 characters) to login
          </p>
        </div>
      </div>
    </div>
  )
}
```

**File:** `frontend/src/pages/Register/RegisterPage.tsx`

Similar structure for registration.

#### 2.3 Implement Protected Routes

**File:** `frontend/src/components/Auth/ProtectedRoute.tsx`

```typescript
import { Navigate } from 'react-router-dom'
import { useUserStore } from '@/store/useUserStore'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const user = useUserStore(state => state.user)
  const token = localStorage.getItem('access_token')
  
  if (!user || !token) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}
```

**Deliverables Week 2:**
- ✅ Mock WebSocket service with simulated updates
- ✅ Login/Register pages implemented
- ✅ Protected routes working
- ✅ Real-time updates visible in UI
- ✅ Complete auth flow functional

---

### **PHASE 3: Component Library & Documentation** (Week 3)

#### 3.1 Install Storybook

```bash
npx storybook@latest init --yes
```

#### 3.2 Create Component Stories

**File:** `frontend/src/components/Common/Button.stories.tsx`

```typescript
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './Button'

const meta: Meta<typeof Button> = {
  title: 'Common/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost']
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg']
    },
  },
}

export default meta
type Story = StoryObj<typeof Button>

export const Primary: Story = {
  args: {
    children: 'Primary Button',
    variant: 'primary',
  },
}

export const Secondary: Story = {
  args: {
    children: 'Secondary Button',
    variant: 'secondary',
  },
}

export const Loading: Story = {
  args: {
    children: 'Loading...',
    disabled: true,
  },
}
```

**Create stories for all components:**
- Button, Input, Badge
- EntityCard, ResearchItemCard
- SigmaGraph, NodeDetailsPanel
- Layout, ThreePanelLayout

#### 3.3 Visual Regression Testing

```bash
npm install --save-dev chromatic
```

**File:** `.storybook/main.ts`

Configure Chromatic for visual regression tests.

**Deliverables Week 3:**
- ✅ Storybook configured
- ✅ 20+ component stories
- ✅ Interactive component playground
- ✅ Visual regression testing setup
- ✅ Component documentation

---

### **PHASE 4: Comprehensive Testing & Production Build** (Week 4)

#### 4.1 Unit Tests

**File:** `frontend/src/components/Common/__tests__/Button.test.tsx`

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Button } from '../Button'

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })
  
  it('calls onClick when clicked', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    
    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
  
  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>)
    const button = screen.getByText('Click me')
    expect(button).toBeDisabled()
  })
})
```

**Create 50+ unit tests** for all components and utilities.

#### 4.2 Integration Tests

**File:** `frontend/tests/integration/auth-flow.test.tsx`

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { server } from '@/mocks/server'
import { LoginPage } from '@/pages/Login/LoginPage'

beforeAll(() => server.listen())
afterAll(() => server.close())

describe('Authentication Flow', () => {
  it('logs in successfully with valid credentials', async () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    )
    
    // Fill form
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'password123' }
    })
    
    // Submit
    fireEvent.click(screen.getByText('Sign in'))
    
    // Verify token stored
    await waitFor(() => {
      const token = localStorage.getItem('access_token')
      expect(token).toContain('mock_access_')
    })
  })
  
  it('shows error with invalid credentials', async () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    )
    
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: '123' } // Too short
    })
    
    fireEvent.click(screen.getByText('Sign in'))
    
    await waitFor(() => {
      expect(screen.getByText(/Invalid credentials/i)).toBeInTheDocument()
    })
  })
})
```

**Create 20+ integration tests** for key user flows.

#### 4.3 E2E Tests

**File:** `frontend/tests/e2e/user-journey.spec.ts`

```typescript
import { test, expect } from '@playwright/test'

test('complete user journey', async ({ page }) => {
  // Navigate to login
  await page.goto('http://localhost:5173/login')
  
  // Login
  await page.fill('input[type="email"]', 'test@example.com')
  await page.fill('input[type="password"]', 'password123')
  await page.click('button[type="submit"]')
  
  // Wait for navigation to feed
  await expect(page).toHaveURL(/.*feed/)
  
  // Verify feed loaded
  await expect(page.locator('h1')).toContainText('Research Feed')
  
  // Navigate to graph
  await page.click('text=Lab')
  await expect(page).toHaveURL(/.*lab/)
  
  // Verify graph rendered
  await expect(page.locator('canvas')).toBeVisible()
  
  // Open settings
  await page.click('text=Settings')
  await expect(page).toHaveURL(/.*settings/)
  
  // Logout
  await page.click('text=Logout')
  await expect(page).toHaveURL(/.*login/)
})
```

**Create 5+ E2E test scenarios.**

#### 4.4 Production Build Optimization

**File:** `frontend/vite.config.ts` (optimize)

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    target: 'es2015',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console logs
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'graph-vendor': ['sigma', 'graphology'],
          'ui-vendor': ['zustand', '@headlessui/react'],
        },
      },
    },
    chunkSizeWarningLimit: 1000,
  },
  server: {
    port: 5173,
    host: true,
  },
  preview: {
    port: 5173,
    host: true,
  },
})
```

**File:** `frontend/Dockerfile` (production)

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**File:** `frontend/nginx.conf`

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

**Deliverables Week 4:**
- ✅ 50+ unit tests
- ✅ 20+ integration tests
- ✅ 5+ E2E test scenarios
- ✅ 80%+ code coverage
- ✅ Production Docker build
- ✅ Optimized bundle size
- ✅ Fast load times (< 2s)

---

## 📦 Complete Dependency List

### Production Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "zustand": "^4.4.7",
    "axios": "^1.6.2",
    "sigma": "^2.4.0",
    "graphology": "^0.25.4",
    "@headlessui/react": "^1.7.17",
    "@heroicons/react": "^2.1.1",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.1.0"
  }
}
```

### Development Dependencies

```json
{
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8",
    "typescript": "^5.2.2",
    
    "msw": "^2.0.11",
    "@faker-js/faker": "^8.3.1",
    
    "@storybook/react": "^7.6.3",
    "@storybook/react-vite": "^7.6.3",
    "@storybook/addon-essentials": "^7.6.3",
    "chromatic": "^10.0.0",
    
    "vitest": "^1.0.4",
    "@vitest/ui": "^1.0.4",
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/user-event": "^14.5.1",
    "happy-dom": "^12.10.3",
    
    "@playwright/test": "^1.40.1",
    
    "tailwindcss": "^3.3.6",
    "postcss": "^8.4.32",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.55.0",
    "prettier": "^3.1.1"
  }
}
```

**Total:** ~30 npm packages (all frontend)

---

## 📁 Final Directory Structure

```
frontend/
├── src/
│   ├── components/         ✅ Existing + new
│   ├── pages/             ✅ Existing + Login/Register
│   ├── services/          ✅ Existing + mockWebSocket
│   ├── store/             ✅ Existing
│   ├── types/             ✅ Existing
│   ├── utils/             ✅ Existing
│   │
│   ├── mocks/             🆕 NEW
│   │   ├── browser.ts
│   │   ├── server.ts      (for tests)
│   │   ├── handlers/
│   │   │   ├── auth.ts
│   │   │   ├── entities.ts
│   │   │   ├── relationships.ts
│   │   │   ├── feed.ts
│   │   │   └── users.ts
│   │   └── data/
│   │       ├── entities.ts
│   │       ├── relationships.ts
│   │       ├── users.ts
│   │       └── research.ts
│   │
│   └── main.tsx           ✏️ Modified (MSW setup)
│
├── tests/                 🆕 NEW
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
│
├── .storybook/           🆕 NEW
│   ├── main.ts
│   └── preview.ts
│
├── public/               ✅ Existing
├── docker-compose.yml    ✅ Existing
├── Dockerfile            ✏️ Modified (production build)
├── nginx.conf            ✏️ Modified (optimization)
├── package.json          ✏️ Modified (new deps)
├── vite.config.ts        ✏️ Modified (optimization)
└── standalone-module-review/
    ├── 2025-10-28-overview.md
    ├── SCOPE-ANALYSIS.md
    ├── CLEANUP-RECOMMENDATIONS.md
    └── FRONTEND-STANDALONE-PROPOSAL.md (this)
```

---

## ✅ Acceptance Criteria

### Phase 1 Complete When:
- [ ] MSW intercepts all API calls
- [ ] 10,000 entities generated and accessible
- [ ] All CRUD operations work without backend
- [ ] Feed displays 1,000 research items
- [ ] API responses include realistic delays

### Phase 2 Complete When:
- [ ] Mock WebSocket connects successfully
- [ ] Real-time updates appear in UI every 5 seconds
- [ ] Login/Register pages functional
- [ ] Protected routes redirect to login
- [ ] Token refresh works

### Phase 3 Complete When:
- [ ] Storybook runs on port 6006
- [ ] 20+ component stories exist
- [ ] All components documented
- [ ] Visual regression tests configured
- [ ] Components can be developed in isolation

### Phase 4 Complete When:
- [ ] Test coverage > 80%
- [ ] All tests pass
- [ ] Production build < 500KB gzipped
- [ ] Docker image < 50MB
- [ ] Page load < 2 seconds
- [ ] Lighthouse score > 90

---

## 📊 Success Metrics

### Performance Targets
- **Initial Load:** < 2 seconds
- **Time to Interactive:** < 3 seconds
- **Bundle Size:** < 500KB gzipped
- **Lighthouse Performance:** > 90
- **Lighthouse Accessibility:** > 95

### Quality Targets
- **Test Coverage:** > 80%
- **Component Documentation:** 100%
- **Zero Console Errors:** ✅
- **Zero TypeScript Errors:** ✅

### Capability Targets
- **Standalone Operation:** 100% (no backend needed)
- **Mock Data Realism:** 95% realistic
- **Real-time Simulation:** Works perfectly
- **Production Ready:** Fully deployable

---

## ⏱️ Timeline Summary

| Phase | Duration | Focus | Key Deliverables |
|-------|----------|-------|------------------|
| **Phase 1** | Week 1 | Mock API & Data | MSW, 10K entities, all endpoints |
| **Phase 2** | Week 2 | Real-time & Auth | Mock WS, Login, Protected routes |
| **Phase 3** | Week 3 | Components | Storybook, 20+ stories, docs |
| **Phase 4** | Week 4 | Testing & Prod | 80% coverage, Docker, optimization |

**Total:** 4 weeks with 1-2 frontend developers

---

## 🎯 Deployment Options

### Option 1: Static Site
```bash
npm run build
# Deploy dist/ to any static host (Netlify, Vercel, S3)
```

### Option 2: Docker
```bash
docker build -t kg-lab-frontend .
docker run -p 80:80 kg-lab-frontend
```

### Option 3: Nginx
```bash
npm run build
cp -r dist/* /var/www/html/
```

---

## 🚀 Post-Implementation

### What You Get:
- ✅ **Fully standalone frontend** - Zero backend dependencies
- ✅ **10,000+ mock entities** - Realistic data for development
- ✅ **Real-time simulation** - Live updates without WebSocket server
- ✅ **Complete auth flow** - Login, register, protected routes
- ✅ **Component library** - Storybook with 20+ stories
- ✅ **80%+ test coverage** - Unit, integration, E2E tests
- ✅ **Production optimized** - Fast load, small bundle
- ✅ **Docker ready** - One command deployment

### What You DON'T Get (Correctly):
- ❌ No backend modifications
- ❌ No database setup
- ❌ No Python code
- ❌ No infrastructure changes
- ❌ No dependencies on other teams

---

## 💰 Resource Requirements

### Team
- **Size:** 1-2 frontend developers
- **Skills:** React, TypeScript, Testing, Docker basics
- **Duration:** Full-time for 4 weeks

### Infrastructure
- **Development:** Node.js 18+, npm
- **Production:** Any static hosting or Docker
- **Cost:** Minimal (hosting only)

---

## 📋 Approval Checklist

Before approving:
- [ ] Timeline acceptable (4 weeks)
- [ ] Team available (1-2 frontend devs)
- [ ] Scope understood (frontend only)
- [ ] No backend work required
- [ ] Can be deployed standalone
- [ ] Success criteria clear

---

## 🎬 Next Steps

### If Approved:
1. **Week 0:** Install dependencies, setup MSW
2. **Week 1:** Implement mock layer and data generation
3. **Week 2:** Build auth UI and mock WebSocket
4. **Week 3:** Setup Storybook and document components
5. **Week 4:** Write tests and optimize production build

### Daily Workflow:
- Morning: Check progress, plan tasks
- Development: Implement features
- Testing: Write tests for new code
- Evening: Commit, update documentation

---

## ✅ Conclusion

This proposal creates a **true standalone frontend module** that:
- Operates without any backend
- Generates its own realistic data
- Simulates real-time capabilities
- Is fully tested and documented
- Can be deployed anywhere

**Timeline:** 4 weeks  
**Scope:** Frontend directory only  
**Dependencies:** No backend required  
**Result:** Production-ready standalone module

---

**📋 STATUS: AWAITING APPROVAL**

Ready to transform the frontend into a fully independent, production-ready standalone module.


