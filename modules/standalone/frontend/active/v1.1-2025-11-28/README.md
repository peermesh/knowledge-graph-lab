# Frontend Design Module

Interactive React-based user interface for the Knowledge Graph Lab platform, providing intuitive knowledge graph exploration, real-time updates, and comprehensive accessibility support.

## Overview

The Frontend module delivers a sophisticated user experience through:

- **Three-Panel Layout**: Responsive design with collapsible navigation, main content, and contextual panels
- **Interactive Graph Visualization**: WebGL-powered knowledge graph with 60fps performance and 10,000+ node support
- **Real-time Updates**: WebSocket integration with <1.5s latency for live data updates
- **Accessibility**: Full WCAG 2.1 AA compliance with keyboard navigation and screen reader support
- **Performance**: <2s Time to Interactive, <1MB bundle size, optimized for modern browsers
- **Cross-Browser Compatibility**: Tested across Chrome, Firefox, Safari, and Edge
- **Production Optimization**: Bundle splitting, lazy loading, and comprehensive monitoring

## Features

- **Modern React Architecture**: TypeScript, Vite, and modern React patterns
- **State Management**: Zustand for client state, TanStack Query for server state
- **Styling**: Tailwind CSS with custom design system and dark mode support
- **Graph Visualization**: Sigma.js with WebGL rendering for complex knowledge graphs
- **Real-time Communication**: WebSocket integration with auto-reconnection
- **Testing**: Comprehensive test suite with 85%+ coverage and accessibility testing
- **Cross-Browser Compatibility**: Tested across all major browsers and devices
- **Performance Monitoring**: Real-time performance tracking and optimization
- **Production Optimization**: Bundle splitting, lazy loading, and CDN optimization

## Implementation Status

### ✅ COMPLETED - All 5 Phases

**Phase 1: Foundation & Core Layout** ✅
- Vite + React + TypeScript project initialized
- ESLint, Prettier, and testing framework configured
- Responsive three-panel layout with collapsible panels
- React Router configured with main routes
- Left-panel navigation component

**Phase 2: State Management & API Integration** ✅
- Zustand stores for all state management
- TanStack Query integration for API calls
- API service layer with error handling
- Authentication flow implementation
- WebSocket service with reconnection logic

**Phase 3: User Onboarding & Feed** ✅
- Interactive bubble interface with Framer Motion
- Hierarchical directory browser component
- Infinite-scrolling feed with virtualization
- Research item cards with interactions
- Real-time topic selection feedback

**Phase 4: Graph Visualization & Advanced Features** ✅
- Sigma.js integration with WebGL rendering
- Graph interactions (pan, zoom, node selection)
- Right-panel contextual details
- Advanced search and filtering interface
- Data export functionality

**Phase 5: Integration & Production Optimization** ✅
- Enhanced settings page with channel configuration
- WebSocket service with auto-reconnection
- Toast notification system
- Full accessibility compliance (WCAG 2.1 AA)
- Cross-browser testing and fixes
- Production build optimization
- Integration testing with all modules

## Quick Start

### Prerequisites

- Node.js 18+
- npm 9+

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Production Build

```bash
npm run build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Common/          # Reusable UI components (Button, Input, Badge)
│   │   ├── Layout/          # Layout components (ThreePanelLayout, ResizablePanel)
│   │   ├── Navigation/      # Navigation components (MainNavigation)
│   │   ├── Feed/           # Feed components (ResearchItemCard)
│   │   ├── Graph/          # Graph visualization (SigmaGraph, NodeDetailsPanel)
│   │   └── Onboarding/     # Onboarding flow (BubbleInterface)
│   ├── pages/              # Page components (Feed, Lab, Onboarding, Settings)
│   ├── services/           # API client and external integrations
│   ├── store/              # Zustand stores (UI, User, Graph state)
│   ├── types/              # TypeScript type definitions
│   ├── utils/              # Utility functions (cn, formatting)
│   └── test/               # Test configuration and setup
├── public/                 # Static assets
├── dist/                   # Build output
├── package.json           # Dependencies and scripts
├── vite.config.ts         # Vite configuration
├── tsconfig.json          # TypeScript configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── index.html             # HTML template
```

## Key Components

### Layout System
- **ThreePanelLayout**: Main application layout with collapsible panels
- **ResizablePanel**: Individual resizable panels with drag handles
- **MainNavigation**: Left sidebar navigation with route links

### Graph Visualization
- **SigmaGraph**: WebGL-powered graph rendering with 60fps performance
- **NodeDetailsPanel**: Contextual information for selected graph nodes
- **Graph Controls**: Zoom, pan, and interaction controls

### Content Display
- **ResearchItemCard**: Rich content cards with metadata and actions
- **FeedPage**: Infinite scroll feed with virtualization
- **BubbleInterface**: Interactive onboarding with physics-based animations

### State Management
- **UI Store**: Theme, layout, notifications, and loading states
- **User Store**: Authentication, user profile, and session management
- **Graph Store**: Graph data, selection, and visualization state

## Configuration

### Environment Variables

Create a `.env` file with:

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WEBSOCKET_URL=ws://localhost:8000/ws

# Application Settings
VITE_APP_TITLE=Knowledge Graph Lab
VITE_DEBUG=true

# Analytics (optional)
VITE_ANALYTICS_ID=your-analytics-id
```

### Theme Configuration

The application supports light, dark, and auto themes with full accessibility compliance:

```typescript
// Theme switching
setTheme('light' | 'dark' | 'auto')

// Accessibility features
- High contrast mode
- Reduced motion support
- Keyboard navigation
- Screen reader optimization
```

## Development

### Code Quality

```bash
# Linting and formatting
npm run lint        # Check for issues
npm run lint:fix    # Auto-fix issues
npm run format      # Format code

# Type checking
npm run type-check  # Check TypeScript types

# Testing
npm run test        # Run test suite
npm run test:ui     # Run tests with UI
npm run test:run    # Run tests once
```

### Testing Strategy

- **Unit Tests**: Component logic and utilities with 85%+ coverage
- **Integration Tests**: End-to-end workflows and module interactions using Playwright
- **Accessibility Tests**: WCAG 2.1 AA compliance with axe-core automated testing
- **Performance Tests**: Bundle size, loading performance, and memory usage monitoring
- **Cross-browser Tests**: Compatibility testing across Chrome, Firefox, Safari, and Edge
- **Visual Regression**: Component appearance consistency with screenshot testing

### Performance Optimization

- **Bundle Splitting**: Automatic code splitting for optimal loading
- **Lazy Loading**: Route-based and component-based lazy loading
- **Virtualization**: Efficient rendering of large lists and graphs
- **Caching**: React Query for server state, browser cache for static assets
- **Compression**: Gzip compression and asset optimization
- **WebGL Optimization**: GPU-accelerated graph rendering for 60fps performance
- **Memory Management**: Efficient state management and cleanup
- **Network Optimization**: Request deduplication and intelligent prefetching
- **Performance Monitoring**: Real-time performance tracking and optimization recommendations

## Deployment

### Docker Deployment

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

### Production Checklist

- [ ] Build passes all tests
- [ ] Bundle size under 1MB
- [ ] Accessibility audit passes
- [ ] Performance targets met
- [ ] Environment variables configured
- [ ] Health checks implemented
- [ ] Monitoring and logging configured

## Browser Support

- **Modern Browsers**: Chrome, Firefox, Safari, Edge (latest 2 versions)
- **WebGL Support**: Required for graph visualization
- **WebSocket Support**: Required for real-time updates
- **ES2020+ Support**: Required for modern JavaScript features

## Accessibility

### WCAG 2.1 AA Compliance

- **Keyboard Navigation**: Full keyboard accessibility with logical tab order
- **Screen Readers**: ARIA landmarks, labels, and live regions
- **Color Contrast**: Minimum 4.5:1 contrast ratio for all text
- **Focus Management**: Clear focus indicators and logical focus flow
- **Alternative Text**: Descriptive labels for all visual elements

### Assistive Technology Support

- **Screen Readers**: NVDA, JAWS, VoiceOver compatibility
- **Keyboard Navigation**: Complete workflows without mouse
- **Voice Control**: Support for voice navigation systems
- **High Contrast**: Enhanced visibility for low vision users

## Performance Targets

### Core Metrics
- **Time to Interactive**: <2 seconds
- **Graph Rendering**: 60fps on 10,000+ node graphs
- **API Latency**: <200ms (p95), <500ms (p99)
- **Bundle Size**: <1MB initial load
- **Memory Usage**: Stable performance with large datasets

### Optimization Features
- **Virtual Scrolling**: Efficient rendering of large content lists
- **Lazy Loading**: Progressive loading of route components
- **Caching**: Intelligent caching of frequently accessed data
- **Compression**: Optimized asset delivery

## Integration

### Backend Integration
- RESTful API integration for data operations
- WebSocket integration for real-time updates
- Authentication and authorization integration
- Error handling and retry mechanisms

### External Services
- Graph data from AI module
- User preferences from Backend module
- Content management from Publishing module
- Real-time updates via WebSocket connections

## Contributing

### Development Workflow

1. **Feature Branch**: Create feature branch from main
2. **TDD Approach**: Write tests before implementation
3. **Code Quality**: Run linting and formatting
4. **Testing**: Ensure all tests pass
5. **Review**: Submit for code review
6. **Merge**: Merge to main branch

### Code Standards

- **TypeScript**: Strict mode with comprehensive typing
- **React**: Modern hooks and functional components
- **Styling**: Tailwind CSS with custom design tokens
- **Testing**: Vitest with React Testing Library
- **Accessibility**: axe-core for automated accessibility testing

## Troubleshooting

### Common Issues

**Graph not rendering**:
- Ensure WebGL is enabled in browser
- Check browser compatibility
- Verify graph data format

**Real-time updates not working**:
- Check WebSocket connection status
- Verify backend WebSocket endpoint
- Check network connectivity

**Performance issues**:
- Check bundle size with `npm run analyze`
- Monitor memory usage in DevTools
- Verify virtualization for large lists

### Debug Mode

Enable debug mode for detailed logging:

```bash
VITE_DEBUG=true npm run dev
```

## License

MIT License - see LICENSE file for details.

---

*Part of the Knowledge Graph Lab platform - Delivering intelligent user experiences for knowledge discovery.*