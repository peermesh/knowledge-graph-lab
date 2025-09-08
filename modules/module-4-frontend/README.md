# Module 4: Frontend Application

## Overview
The Frontend Application provides the user interface for the Knowledge Graph Lab, enabling users to explore the knowledge graph, view research insights, manage subscriptions, and interact with AI-generated content. Built with Next.js and React, it offers a modern, responsive interface for both desktop and mobile users, with real-time updates and interactive visualizations.

## Quick Start

```bash
# Navigate to module directory
cd modules/module-4-frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Application runs on http://localhost:3000
# API routes available at http://localhost:3000/api/*
```

## Application Features

### Knowledge Graph Explorer
Interactive visualization of entities and their relationships with:
- **Pan and zoom** navigation
- **Entity filtering** by type (Platform, Organization, Person, Grant, Policy, Event)
- **Relationship highlighting** on hover
- **Detail panels** showing entity attributes
- **Search functionality** for quick entity location
- **Export capabilities** for graph snapshots

### Research Dashboard
Real-time overview of research activities:
- **Frontier queue status** with upcoming research priorities
- **Recent discoveries** and newly added entities
- **Topic clusters** with trending analysis
- **Knowledge gaps** identification
- **Research velocity** metrics and charts

### Digest Builder
Personal content digest management:
- **Preference configuration** for topics and frequency
- **Preview mode** for digest content
- **Subscription management** with email/webhook options
- **Historical digests** archive
- **Feedback system** for content improvement

### User Profile & Settings
Personalization and configuration:
- **Interest selection** from predefined topics
- **Notification preferences** for different content types
- **API key management** for external integrations
- **Export options** for personal data
- **Theme selection** (light/dark mode)

## API Routes

### Authentication
```typescript
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/session
POST /api/auth/refresh
```

### User Management
```typescript
GET    /api/users/profile
PUT    /api/users/profile
GET    /api/users/preferences
PUT    /api/users/preferences
DELETE /api/users/account
```

### Knowledge Graph Interface
```typescript
GET  /api/graph/entities?type={type}&limit={limit}
GET  /api/graph/entity/{id}
GET  /api/graph/relationships/{entityId}
POST /api/graph/search
GET  /api/graph/export?format={json|csv|graphml}
```

### Digest Management
```typescript
GET    /api/digests
GET    /api/digests/{id}
POST   /api/digests/generate
PUT    /api/digests/{id}/preferences
DELETE /api/digests/{id}
POST   /api/digests/{id}/feedback
```

### Research Insights
```typescript
GET /api/research/frontier
GET /api/research/topics/trending
GET /api/research/gaps
GET /api/research/metrics
```

## Dependencies

### Frontend Libraries
- **Next.js 14**: React framework with app router
- **React 18**: UI library with concurrent features
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Shadcn/ui**: Component library
- **D3.js/Force Graph**: Graph visualization
- **React Query**: Data fetching and caching
- **Zustand**: State management

### Backend Connections
This module **requires** from:
- **Module 1 (Ingestion)**: Content and source statistics
- **Module 2 (Knowledge Graph)**: Entity data and relationships
- **Module 3 (Reasoning)**: Digests, insights, and recommendations

This module **provides**:
- User interface for all system interactions
- Authentication and session management
- User preferences and configuration storage
- Feedback collection for system improvement

## Configuration

### Environment Variables
```bash
# API Endpoints
NEXT_PUBLIC_INGESTION_API=http://localhost:8001
NEXT_PUBLIC_KNOWLEDGE_API=http://localhost:8002
NEXT_PUBLIC_REASONING_API=http://localhost:8003

# Authentication
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-here
JWT_SECRET=your-jwt-secret

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/kgl_frontend

# External Services
NEXT_PUBLIC_POSTHOG_KEY=your-posthog-key
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn

# Feature Flags
NEXT_PUBLIC_ENABLE_EXPORT=true
NEXT_PUBLIC_ENABLE_SOCIAL_SHARING=true
NEXT_PUBLIC_MAX_GRAPH_NODES=500
```

### Build Configuration
```json
// next.config.js
{
  "reactStrictMode": true,
  "images": {
    "domains": ["localhost", "api.kgl.dev"]
  },
  "experimental": {
    "serverActions": true
  }
}
```

## Component Structure

```
src/
├── app/                    # Next.js app router pages
│   ├── (auth)/            # Authentication pages
│   ├── dashboard/         # Main dashboard
│   ├── graph/            # Knowledge graph explorer
│   ├── digests/          # Digest management
│   ├── settings/         # User settings
│   └── api/              # API routes
├── components/            # React components
│   ├── ui/               # Base UI components
│   ├── graph/            # Graph visualization
│   ├── dashboard/        # Dashboard widgets
│   └── shared/           # Shared components
├── lib/                   # Utilities and helpers
│   ├── api/              # API client functions
│   ├── hooks/            # Custom React hooks
│   └── utils/            # Helper functions
├── styles/                # Global styles
└── types/                 # TypeScript definitions
```

## Testing

### Unit Tests
```bash
# Run unit tests
npm test

# Run with coverage
npm run test:coverage

# Test specific component
npm test -- Button.test.tsx
```

### Integration Tests
```bash
# Run Cypress tests
npm run cypress:open

# Headless testing
npm run cypress:run

# Component testing
npm run cypress:component
```

### E2E Tests
```bash
# Start all backend services first
docker-compose up -d

# Run E2E tests
npm run test:e2e

# Run specific E2E flow
npm run test:e2e -- --spec "cypress/e2e/digest-flow.cy.ts"
```

## Troubleshooting

### Common Issues

#### 1. API Connection Failures
**Problem**: "Failed to fetch" errors in the UI
**Solution**:
- Verify all backend services are running
- Check CORS configuration in backend services
- Ensure environment variables are correctly set
- Check network tab for specific error responses

#### 2. Graph Visualization Performance
**Problem**: Slow or laggy graph rendering with many nodes
**Solution**:
- Limit initial node count with `NEXT_PUBLIC_MAX_GRAPH_NODES`
- Implement node clustering for large graphs
- Use WebGL renderer for better performance
- Enable progressive loading of relationships

#### 3. Authentication Issues
**Problem**: Users getting logged out unexpectedly
**Solution**:
- Check JWT expiration settings
- Verify `NEXTAUTH_SECRET` is consistent
- Implement proper token refresh logic
- Check for clock skew between client and server

#### 4. State Management Conflicts
**Problem**: UI not updating after actions
**Solution**:
- Check React Query cache invalidation
- Verify Zustand store subscriptions
- Look for missing dependencies in useEffect
- Enable React DevTools for debugging

#### 5. Build Failures
**Problem**: TypeScript or build errors
**Solution**:
- Run `npm run type-check` to find TS errors
- Clear `.next` cache folder
- Check for circular dependencies
- Verify all environment variables are defined

### Development Tools
```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Format code
npm run format

# Analyze bundle size
npm run analyze

# Check accessibility
npm run a11y
```

### Performance Monitoring
```bash
# Lighthouse CI
npm run lighthouse

# Bundle analysis
npm run build:analyze

# Runtime performance
# Use React DevTools Profiler in browser
```

## Deployment

### Production Build
```bash
# Create optimized build
npm run build

# Start production server
npm start

# Docker deployment
docker build -t kgl-frontend .
docker run -p 3000:3000 kgl-frontend
```

### Environment-Specific Configs
```bash
# Development
cp .env.development.local.example .env.development.local

# Staging
cp .env.staging.example .env.staging

# Production
cp .env.production.example .env.production
```

## UI/UX Guidelines

### Design Principles
1. **Clarity First**: Information hierarchy and clear navigation
2. **Responsive Design**: Mobile-first approach
3. **Accessibility**: WCAG 2.1 AA compliance
4. **Performance**: < 3s initial load time
5. **Feedback**: Clear loading and error states

### Component Standards
- Use Shadcn/ui components as base
- Maintain consistent spacing (8px grid)
- Follow color system for semantic meaning
- Implement proper keyboard navigation
- Add aria-labels for screen readers

### Interactive Elements
- Hover states for all clickable elements
- Loading skeletons for async content
- Toast notifications for user actions
- Confirmation dialogs for destructive actions
- Optimistic updates where appropriate

## Module Development Tips

1. **Component First**: Build and test components in isolation using Storybook
2. **Type Safety**: Define TypeScript types for all API responses
3. **Mock Data**: Use MSW for API mocking during development
4. **Performance**: Use React.memo and useMemo appropriately
5. **Accessibility**: Test with screen readers and keyboard navigation

## Next Steps for Enhancement

- Implement real-time updates with WebSockets
- Add collaborative features for team research
- Build mobile native apps with React Native
- Create browser extension for quick content addition
- Implement advanced graph analysis tools
- Add data export in multiple formats
- Build custom visualization builders
- Create public sharing capabilities for research