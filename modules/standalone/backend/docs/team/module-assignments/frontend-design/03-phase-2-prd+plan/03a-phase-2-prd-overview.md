# Frontend Design - Phase 2 Overview

## What You're Building

You're building the **web interface** that displays news articles to readers. Think of it as the user-facing website where people browse, search, and read the articles that the AI creates and Backend stores.

## System Architecture

```
AI Module → Creates Articles → Backend Storage → Your Frontend
                                     ↓              ↓
                               REST APIs      Display Articles
                                     ↓              ↓
                               Article Data    Web Pages
```

**Key Point**: You create the website experience for reading articles, not content creation or email functionality.

---

## What You'll Create in Phase 2

Your PRD must specify complete technical implementations for:

### 1. Article Display System
- **Article List Page**: Browse articles with filtering and search
- **Article Detail Page**: Full article view with metadata
- **Navigation Components**: Header, breadcrumbs, pagination
- **Responsive Design**: Works on desktop, tablet, and mobile

### 2. Backend API Integration
- **Data Fetching**: HTTP client for Backend APIs
- **Loading States**: Show progress indicators during API calls
- **Error Handling**: User-friendly error messages
- **Caching Strategy**: Optimize performance with smart caching

### 3. User Interface Components
- **Article Cards**: Compact article previews for lists
- **Article Reader**: Full-text article display with typography
- **Search Interface**: Filter by topic, date, article type
- **Topic Navigation**: Browse articles by category

### 4. State Management
- **Application State**: Current articles, filters, search results
- **URL State**: Browser navigation and bookmarkable URLs
- **Loading State**: Track API request status
- **Error State**: Handle and display error conditions

### 5. User Experience Features
- **Responsive Layout**: Adapts to different screen sizes
- **Accessibility**: Screen reader support, keyboard navigation
- **Performance**: Fast loading, smooth interactions
- **SEO Optimization**: Search engine friendly URLs and metadata

---

## Technical Requirements

### Frontend Technology Stack
Based on Phase 1 research:
- **Framework**: React with TypeScript for type safety
- **State Management**: Redux Toolkit for predictable state updates
- **Routing**: React Router for URL navigation
- **HTTP Client**: Axios for API communication
- **Styling**: CSS Modules or Styled Components
- **Build Tools**: Vite or Create React App

### Component Architecture
```
App
├── Header (navigation, search)
├── ArticleListPage
│   ├── FilterBar (topics, dates, types)
│   ├── ArticleGrid
│   │   └── ArticleCard (preview)
│   └── Pagination
├── ArticleDetailPage
│   ├── ArticleHeader (headline, metadata)
│   ├── ArticleContent (formatted text)
│   └── RelatedArticles
└── Footer (links, copyright)
```

### Data Models (TypeScript Interfaces)
```typescript
interface Article {
  id: string;
  headline: string;
  summary: string;
  body: ArticleBody[];
  url: string;
  topics: string[];
  article_type: 'breaking_news' | 'analysis' | 'feature' | 'roundup';
  quality_score: number;
  generated_at: string;
  entities: {
    people: string[];
    companies: string[];
    places: string[];
  };
}

interface ArticleBody {
  type: 'paragraph' | 'quote' | 'list' | 'image';
  content: string;
  attribution?: string;
}

interface ArticleFilters {
  topics: string[];
  article_types: string[];
  date_range: {
    from: string;
    to: string;
  };
  search_query: string;
}
```

### API Integration Specifications
```typescript
class ArticleAPIClient {
  async getArticles(filters: ArticleFilters, page: number = 1): Promise<ArticleListResponse> {
    const params = new URLSearchParams({
      topics: filters.topics.join(','),
      types: filters.article_types.join(','),
      date_from: filters.date_range.from,
      date_to: filters.date_range.to,
      q: filters.search_query,
      page: page.toString(),
      page_size: '20'
    });

    const response = await axios.get(`/api/v1/reports?${params}`);
    return response.data;
  }

  async getArticle(id: string): Promise<Article> {
    const response = await axios.get(`/api/v1/reports/${id}`);
    return response.data;
  }
}

interface ArticleListResponse {
  page: number;
  page_size: number;
  total: number;
  has_next: boolean;
  items: Article[];
}
```

---

## Your 5 Main Features

### Feature 1: Article List & Browse
**Purpose**: Let users discover and browse available articles

**Key Components**:
- Article grid with responsive cards
- Filter sidebar (topics, dates, types)
- Search functionality
- Pagination controls

**User Stories**:
- As a reader, I want to see recent articles so I can find interesting content
- As a reader, I want to filter by topic so I can find relevant articles
- As a reader, I want to search by keywords so I can find specific information

### Feature 2: Article Detail View
**Purpose**: Display full articles with rich formatting

**Key Components**:
- Full article header with metadata
- Formatted article body with proper typography
- Share buttons and article actions
- Related articles suggestions

**User Stories**:
- As a reader, I want to read full articles with clear formatting
- As a reader, I want to see article metadata like topics and publish date
- As a reader, I want to find related articles on similar topics

### Feature 3: Navigation & URL Structure
**Purpose**: Provide intuitive navigation and bookmarkable URLs

**URL Structure**:
```
/                           # Homepage with recent articles
/articles                   # Article list with filters
/articles?topic=technology  # Filtered article list
/articles/2025-09-22/slug   # Individual article
/search?q=artificial+intelligence  # Search results
```

**Navigation Components**:
- Header with main navigation
- Breadcrumb navigation
- Topic-based menu
- Search bar in header

### Feature 4: Responsive Design
**Purpose**: Ensure great experience across all devices

**Breakpoints**:
- Mobile: 320px - 768px (single column, stack filters)
- Tablet: 768px - 1024px (two columns, sidebar filters)
- Desktop: 1024px+ (multi-column grid, full sidebar)

**Responsive Behavior**:
- Article grid adapts from 1-3 columns based on screen size
- Navigation collapses to hamburger menu on mobile
- Filter sidebar converts to dropdown on mobile

### Feature 5: Performance & Accessibility
**Purpose**: Fast, accessible experience for all users

**Performance Features**:
- Lazy loading for article images
- Virtual scrolling for long article lists
- Optimistic UI updates
- Smart caching of article data

**Accessibility Features**:
- ARIA labels for screen readers
- Keyboard navigation support
- High contrast mode support
- Alt text for all images

---

## Module Integration Points

### With Backend Module
**API Integration**:
- Article list endpoint with filtering and pagination
- Individual article endpoint by ID or slug
- Search endpoint for keyword queries
- Topic listing endpoint for navigation

**Performance Requirements**:
- Article list loads in <500ms
- Individual articles load in <300ms
- Search results return in <800ms

**Error Handling**:
- Graceful degradation when Backend is unavailable
- User-friendly error messages
- Retry mechanisms for failed requests

### With Publishing Module (Indirect)
**Email Link Integration**:
- Handle traffic from newsletter links
- Consistent URL structure between email and website
- Track article views from email referrals

---

## Success Criteria

Your Phase 2 PRD is complete when it specifies:

### Technical Implementation
- [ ] Complete React component hierarchy with props interfaces
- [ ] Redux store structure with actions and reducers
- [ ] API client with TypeScript interfaces
- [ ] Routing configuration with URL patterns
- [ ] CSS architecture with responsive breakpoints

### User Experience
- [ ] Wireframes or mockups for all major pages
- [ ] User flow diagrams for common tasks
- [ ] Error state designs and messaging
- [ ] Loading state indicators and animations
- [ ] Accessibility compliance plan (WCAG 2.1 AA)

### Performance & Quality
- [ ] Performance budgets and optimization strategies
- [ ] Testing plan for components and user flows
- [ ] Browser compatibility requirements
- [ ] SEO optimization specifications

---

## Design System Foundation

### Typography Scale
```css
/* Heading hierarchy */
.headline-1 { font-size: 2.5rem; line-height: 1.2; }  /* Article titles */
.headline-2 { font-size: 2rem; line-height: 1.3; }   /* Section headers */
.headline-3 { font-size: 1.5rem; line-height: 1.4; } /* Subsections */

/* Body text */
.body-large { font-size: 1.125rem; line-height: 1.6; } /* Article content */
.body-regular { font-size: 1rem; line-height: 1.5; }   /* General text */
.body-small { font-size: 0.875rem; line-height: 1.4; } /* Metadata */
```

### Color Palette
```css
/* Primary colors */
--color-primary: #0066cc;      /* Links, buttons */
--color-primary-dark: #0052a3; /* Hover states */

/* Semantic colors */
--color-success: #10b981;      /* Success messages */
--color-warning: #f59e0b;      /* Warning messages */
--color-error: #ef4444;        /* Error messages */

/* Neutral colors */
--color-text-primary: #1a202c;   /* Main text */
--color-text-secondary: #4a5568; /* Supporting text */
--color-background: #ffffff;      /* Page background */
--color-surface: #f7fafc;        /* Card backgrounds */
```

### Component States
```css
/* Interactive states */
.button:hover { opacity: 0.8; }
.button:focus { outline: 2px solid var(--color-primary); }
.button:disabled { opacity: 0.5; cursor: not-allowed; }

/* Loading states */
.loading { animation: pulse 2s ease-in-out infinite; }
.skeleton { background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%); }
```

---

## Key Architectural Decisions

### State Management Strategy
- **Global State**: Current articles, filters, user preferences
- **Local State**: Component-specific UI state (dropdowns, modals)
- **URL State**: Filters and navigation state synced with browser URL
- **Cache State**: Article data cached in Redux with TTL expiration

### URL and Navigation Strategy
- **SEO-Friendly URLs**: `/articles/2025-09-22/article-title-slug`
- **Filter State in URLs**: Bookmarkable search and filter combinations
- **Client-Side Routing**: React Router with history API
- **Deep Linking**: Direct links to specific articles and filtered views

### Performance Strategy
- **Code Splitting**: Lazy load routes and heavy components
- **Image Optimization**: WebP format with fallbacks, lazy loading
- **API Optimization**: Request deduplication, background prefetching
- **Bundle Optimization**: Tree shaking, module federation

---

## Next Steps

1. **Read Assignment**: Review detailed tasks in `03b-phase-2-prd-assignment.md`
2. **Backend Coordination**: Meet with Backend owner to finalize API contracts
3. **Design Research**: Analyze successful news websites for UX patterns
4. **Component Planning**: Design reusable component library structure
5. **Prototype Creation**: Build key components to validate architecture

Your PRD must provide complete specifications that enable Phase 3 developers to build a professional, accessible, and performant web application.