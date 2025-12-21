**Non-canonical during concept phase — authoritative conceptual PRDs live in .dev/peermesh-canvases/**

# Frontend Module PRD - MVP Version

## Module Owner: Developer 2

## Executive Summary
Build a React frontend with two pages: Admin Dashboard for monitoring and User Signup for email subscriptions. Total time: 100 hours.

## Goals (MVP)
1. Create admin dashboard showing system stats
2. Create user signup page for email digests
3. Connect to Backend API
4. Use Material-UI for quick styling
5. Run in Docker container

## User Stories

### Phase 1 (Weeks 1-6): Core Features
- As an admin, I can see dashboard with counts (sources, entities, subscribers)
- As an admin, I can add new RSS feed sources
- As a user, I can sign up for email digests
- As a user, I can see a success message after signup
- As an admin, I can see list of recent entities

### Phase 2 (Weeks 7-10): Enhancements
- Add search functionality
- Improve UI/UX design
- Add loading states
- Add error handling
- Make responsive for mobile

## Technical Requirements

### Stack
- React 18 (Create React App)
- Material-UI v5
- Axios for API calls
- React Router for navigation
- Docker

### Pages

#### 1. Admin Dashboard (/admin)
```
+----------------------------------+
|        Knowledge Graph Lab       |
+----------------------------------+
| Stats Overview:                  |
| • Sources: 5                     |
| • Entities: 42                   |
| • Subscribers: 10                |
+----------------------------------+
| Add New Source:                  |
| [URL input] [Add RSS Feed]       |
+----------------------------------+
| Recent Entities:                 |
| • YouTube (platform)             |
| • Creator Fund (grant)           |
| • TikTok (platform)              |
+----------------------------------+
```

#### 2. User Signup (/signup)
```
+----------------------------------+
|   Get Creator Economy Updates    |
+----------------------------------+
| Stay informed about:             |
| ✓ Grant opportunities            |
| ✓ Platform updates               |
| ✓ Creator programs               |
+----------------------------------+
| Email: [___________]             |
|                                  |
| Topics (optional):               |
| ☐ YouTube  ☐ TikTok  ☐ Twitch   |
|                                  |
| [Subscribe]                      |
+----------------------------------+
```

## Implementation Plan

### Week 1-2: Setup
- [ ] Create React app with CRA
- [ ] Setup Docker container
- [ ] Install Material-UI
- [ ] Create basic routing

### Week 3-4: Dashboard Page
- [ ] Create dashboard layout
- [ ] Connect to Backend API
- [ ] Display stats from API
- [ ] Add source input form

### Week 5-6: Signup Page
- [ ] Create signup form
- [ ] Handle form submission
- [ ] Show success message
- [ ] Add basic validation

### Week 7-8: Enhancement
- [ ] Improve UI design
- [ ] Add loading spinners
- [ ] Error handling
- [ ] Make responsive

### Week 9-10: Integration
- [ ] Test with real Backend
- [ ] Fix integration issues
- [ ] Add search feature

### Week 11-12: Demo Prep
- [ ] End-to-end testing
- [ ] Bug fixes
- [ ] Polish UI

## API Integration

### Backend Endpoints Used
```javascript
// Get dashboard stats
GET http://localhost:8000/api/dashboard

// Get entities list
GET http://localhost:8000/api/entities

// Add RSS source
POST http://localhost:8000/api/sources

// Subscribe user (via Publisher module)
POST http://localhost:8002/api/subscribers
```

## Success Criteria
- [ ] Dashboard loads in < 2 seconds
- [ ] Can add RSS feed source
- [ ] Can sign up for digest
- [ ] Works on desktop and mobile
- [ ] No console errors

## Dependencies
- Backend Module: Provides all data APIs
- Publisher Module: Handles email subscriptions

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| Complex state management | Start simple, no Redux |
| UI design time | Use Material-UI components |
| API integration issues | Use mock data first |
| Responsive design | Focus on desktop first |

## Resources Provided
1. React starter template
2. Material-UI examples
3. Mock API responses
4. Docker configuration
5. Design mockups

## Example Code Structure
```
frontend/
├── Dockerfile
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── App.js           # Main app with routing
│   ├── index.js         # Entry point
│   ├── api/
│   │   └── backend.js   # API calls
│   ├── pages/
│   │   ├── Dashboard.js # Admin dashboard
│   │   └── Signup.js    # User signup
│   └── components/
│       ├── StatsCard.js # Reusable components
│       └── EntityList.js
└── tests/
    └── App.test.js      # Basic tests
```

## Getting Started
```bash
# Clone repo
git clone <repo>
cd modules/frontend

# Install dependencies
npm install

# Run development
npm start

# Build Docker
docker build -t frontend .

# Run Docker
docker run -p 3000:3000 frontend
```

## Mock Data for Development
```javascript
// Mock dashboard response
const mockDashboard = {
  sources_count: 5,
  entities_count: 42,
  subscribers_count: 10,
  last_updated: new Date().toISOString()
};

// Mock entities response
const mockEntities = [
  { id: 1, name: "YouTube", type: "platform" },
  { id: 2, name: "Creator Fund", type: "grant" },
  { id: 3, name: "TikTok", type: "platform" }
];
```

## Questions to Resolve
1. What fields for signup form? (Email minimum)
2. How to handle authentication? (Skip for MVP)
3. What stats to show on dashboard? (Keep simple)

## Notes
- Focus on functionality over beauty
- Use Material-UI for quick styling
- Mock API calls until Backend ready
- Ask for help if stuck on React concepts