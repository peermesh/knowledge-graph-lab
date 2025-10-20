# Frontend Design - Phase 2 Assignment

## Your Mission

Create a comprehensive PRD that specifies exactly how to build a news article reading website. Your PRD must include complete technical specifications, component designs, API integrations, and implementation details that enable direct Phase 3 development.

---

## Before You Start

Prerequisites:

- [ ] Read the overview document (`03a-phase-2-prd-overview.md`)
- [ ] Review your Phase 1 research on React frameworks and component libraries
- [ ] Understand the corrected architecture: AI creates articles → Backend stores → You display articles

---

## Task 1: Define Backend Integration Contracts

**Objective**: Specify exact API contracts for fetching articles from Backend.

### Backend Coordination Meeting
Schedule a working session with the Backend module owner to define:

**Article API Requirements:**

- Endpoint specifications with complete request/response schemas
- Filter parameters you need (date, topics, article_type, search)
- Sorting options (recency, quality score, relevance)
- Pagination strategy for article lists
- Performance requirements (<300ms response time)

**Required Article Data Fields:**

Document exactly what data you need for display:
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
```

**API Specification Example:**
```http
GET /api/v1/reports?topics=technology,business&article_type=breaking_news&page=1&page_size=20&sort=-generated_at

Authorization: Bearer {api_token}
Content-Type: application/json

Response 200:
{
  "page": 1,
  "page_size": 20,
  "total": 156,
  "has_next": true,
  "items": [...article objects...]
}
```

**Deliverable**: Complete API specification document with examples.

---

## Task 2: Design React Component Architecture

**Objective**: Define complete component hierarchy and data flow.

### Component Structure

**App Architecture:**
```typescript
// App.tsx - Main application component
interface AppProps {}

export function App(): JSX.Element {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/articles" element={<ArticleListPage />} />
          <Route path="/articles/:slug" element={<ArticleDetailPage />} />
          <Route path="/search" element={<SearchResultsPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}
```

**Component Hierarchy:**
```
App
├── Layout
│   ├── Header
│   │   ├── Navigation
│   │   ├── SearchBar
│   │   └── TopicMenu
│   └── Footer
├── HomePage
│   ├── FeaturedArticles
│   └── RecentArticles
├── ArticleListPage
│   ├── FilterSidebar
│   │   ├── TopicFilter
│   │   ├── DateFilter
│   │   └── TypeFilter
│   ├── ArticleGrid
│   │   └── ArticleCard (repeated)
│   └── Pagination
├── ArticleDetailPage
│   ├── ArticleHeader
│   ├── ArticleContent
│   ├── ArticleMeta
│   └── RelatedArticles
└── SearchResultsPage
    ├── SearchFilters
    ├── SearchResults
    └── SearchPagination
```

**Component Props Interfaces:**
```typescript
interface ArticleCardProps {
  article: Article;
  variant?: 'compact' | 'featured' | 'list';
  onRead?: (articleId: string) => void;
}

interface FilterSidebarProps {
  filters: ArticleFilters;
  onFilterChange: (filters: ArticleFilters) => void;
  availableTopics: string[];
}

interface ArticleDetailProps {
  articleId: string;
  onRelatedClick?: (articleId: string) => void;
}
```

**Deliverable**: Complete component architecture with TypeScript interfaces.

---

## Task 3: Design State Management System

**Objective**: Specify Redux store structure and data flow.

### Redux Store Structure

**Store Schema:**
```typescript
interface RootState {
  articles: ArticlesState;
  filters: FiltersState;
  ui: UIState;
  routing: RoutingState;
}

interface ArticlesState {
  // Article lists
  list: {
    items: Article[];
    pagination: PaginationInfo;
    loading: boolean;
    error: string | null;
    lastFetch: number;
  };

  // Individual articles
  byId: Record<string, Article>;
  currentArticle: {
    id: string | null;
    loading: boolean;
    error: string | null;
  };

  // Related articles
  related: Record<string, string[]>;
}

interface FiltersState {
  topics: string[];
  article_types: ArticleType[];
  date_range: {
    from: string;
    to: string;
  };
  search_query: string;
  sort_by: 'recency' | 'quality' | 'relevance';
}

interface UIState {
  theme: 'light' | 'dark';
  sidebar_open: boolean;
  mobile_menu_open: boolean;
  toast_messages: ToastMessage[];
}
```

**Actions and Reducers:**
```typescript
// Article Actions
export const fetchArticles = createAsyncThunk(
  'articles/fetchList',
  async (params: ArticleListParams) => {
    const response = await articleApi.getArticles(params);
    return response.data;
  }
);

export const fetchArticleById = createAsyncThunk(
  'articles/fetchById',
  async (id: string) => {
    const response = await articleApi.getArticle(id);
    return response.data;
  }
);

// Filter Actions
export const updateFilters = createAction<Partial<FiltersState>>('filters/update');
export const resetFilters = createAction('filters/reset');
export const setSearchQuery = createAction<string>('filters/setSearch');
```

**Deliverable**: Complete Redux store specification with actions and reducers.

---

## Task 4: Design API Integration Layer

**Objective**: Specify complete HTTP client for Backend communication.

### API Client Implementation

**HTTP Client Class:**
```typescript
class ArticleAPIClient {
  private baseURL: string;
  private token: string;

  constructor(baseURL: string, token: string) {
    this.baseURL = baseURL;
    this.token = token;
  }

  async getArticles(params: ArticleListParams): Promise<ArticleListResponse> {
    const url = new URL(`${this.baseURL}/api/v1/reports`);

    // Add query parameters
    if (params.topics?.length) {
      url.searchParams.append('topics', params.topics.join(','));
    }
    if (params.article_types?.length) {
      url.searchParams.append('types', params.article_types.join(','));
    }
    if (params.date_from) {
      url.searchParams.append('date_from', params.date_from);
    }
    if (params.date_to) {
      url.searchParams.append('date_to', params.date_to);
    }
    if (params.search_query) {
      url.searchParams.append('q', params.search_query);
    }

    url.searchParams.append('page', params.page.toString());
    url.searchParams.append('page_size', params.page_size.toString());
    url.searchParams.append('sort', params.sort || '-generated_at');

    const response = await fetch(url.toString(), {
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new APIError(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  async getArticle(id: string): Promise<Article> {
    const response = await fetch(`${this.baseURL}/api/v1/reports/${id}`, {
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 404) {
        throw new ArticleNotFoundError(`Article ${id} not found`);
      }
      throw new APIError(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  async searchArticles(query: string, filters: ArticleFilters): Promise<ArticleListResponse> {
    // Implementation for search endpoint
    const params = { ...filters, search_query: query, page: 1, page_size: 20 };
    return this.getArticles(params);
  }
}
```

**Error Handling Strategy:**
```typescript
class APIError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = 'APIError';
  }
}

class ArticleNotFoundError extends APIError {
  constructor(message: string) {
    super(message, 404);
    this.name = 'ArticleNotFoundError';
  }
}

// Error handling in components
function useArticleWithErrorHandling(id: string) {
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiClient.getArticle(id)
      .then(setArticle)
      .catch((err) => {
        if (err instanceof ArticleNotFoundError) {
          setError('Article not found');
        } else {
          setError('Failed to load article. Please try again.');
        }
      })
      .finally(() => setLoading(false));
  }, [id]);

  return { article, loading, error };
}
```

**Deliverable**: Complete API client specification with error handling.

---

## Task 5: Design Responsive UI Components

**Objective**: Specify responsive design implementation for all screen sizes.

### Responsive Breakpoints

**CSS Variables and Breakpoints:**
```css
:root {
  /* Breakpoints */
  --breakpoint-mobile: 320px;
  --breakpoint-tablet: 768px;
  --breakpoint-desktop: 1024px;
  --breakpoint-wide: 1440px;

  /* Container sizes */
  --container-mobile: 100%;
  --container-tablet: 720px;
  --container-desktop: 960px;
  --container-wide: 1200px;
}

/* Responsive containers */
.container {
  width: 100%;
  max-width: var(--container-wide);
  margin: 0 auto;
  padding: 0 1rem;
}

@media (min-width: 768px) {
  .container {
    padding: 0 2rem;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 0 3rem;
  }
}
```

**Responsive Grid System:**
```css
.article-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: 1fr; /* Mobile: single column */
}

@media (min-width: 768px) {
  .article-grid {
    grid-template-columns: repeat(2, 1fr); /* Tablet: two columns */
  }
}

@media (min-width: 1024px) {
  .article-grid {
    grid-template-columns: repeat(3, 1fr); /* Desktop: three columns */
  }
}

@media (min-width: 1440px) {
  .article-grid {
    grid-template-columns: repeat(4, 1fr); /* Wide: four columns */
  }
}
```

**Mobile Navigation:**
```typescript
function MobileNavigation() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        className="mobile-menu-toggle"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle navigation menu"
      >
        <HamburgerIcon />
      </button>

      <nav className={`mobile-nav ${isOpen ? 'open' : ''}`}>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/articles">Articles</Link></li>
          <li><Link to="/search">Search</Link></li>
        </ul>
      </nav>

      {isOpen && (
        <div
          className="mobile-nav-overlay"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
}
```

**Deliverable**: Complete responsive design specifications with CSS and components.

---

## Task 6: Design Accessibility Implementation

**Objective**: Specify WCAG 2.1 AA compliance implementation.

### Accessibility Features

**Keyboard Navigation:**
```typescript
function ArticleCard({ article, onRead }: ArticleCardProps) {
  const handleKeyPress = (event: KeyboardEvent) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      onRead?.(article.id);
    }
  };

  return (
    <article
      className="article-card"
      tabIndex={0}
      onClick={() => onRead?.(article.id)}
      onKeyPress={handleKeyPress}
      role="button"
      aria-label={`Read article: ${article.headline}`}
    >
      <header>
        <h3>{article.headline}</h3>
        <div className="article-meta">
          <time dateTime={article.generated_at}>
            {formatDate(article.generated_at)}
          </time>
          <span className="topics" aria-label="Topics">
            {article.topics.join(', ')}
          </span>
        </div>
      </header>
      <p className="summary">{article.summary}</p>
    </article>
  );
}
```

**Screen Reader Support:**
```typescript
function ArticleFilters({ filters, onFilterChange }: FilterProps) {
  return (
    <aside className="filters" role="complementary" aria-label="Article filters">
      <h2>Filter Articles</h2>

      <fieldset>
        <legend>Topics</legend>
        {availableTopics.map(topic => (
          <label key={topic}>
            <input
              type="checkbox"
              checked={filters.topics.includes(topic)}
              onChange={(e) => handleTopicChange(topic, e.target.checked)}
              aria-describedby={`topic-${topic}-description`}
            />
            {topic}
            <span
              id={`topic-${topic}-description`}
              className="sr-only"
            >
              Filter by {topic} articles
            </span>
          </label>
        ))}
      </fieldset>
    </aside>
  );
}
```

**Color Contrast and Focus States:**
```css
/* High contrast focus indicators */
*:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Color contrast ratios */
.article-card {
  background: var(--color-surface); /* #ffffff */
  color: var(--color-text-primary); /* #1a202c - 15:1 contrast */
}

.article-meta {
  color: var(--color-text-secondary); /* #4a5568 - 7:1 contrast */
}

/* Screen reader only content */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

**Deliverable**: Complete accessibility implementation specification.

---

## Task 7: Design Performance and SEO

**Objective**: Specify performance optimization and SEO implementation.

### Performance Optimization

**Code Splitting and Lazy Loading:**
```typescript
// Route-based code splitting
const ArticleListPage = lazy(() => import('./pages/ArticleListPage'));
const ArticleDetailPage = lazy(() => import('./pages/ArticleDetailPage'));
const SearchResultsPage = lazy(() => import('./pages/SearchResultsPage'));

function App() {
  return (
    <Router>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/articles" element={<ArticleListPage />} />
          <Route path="/articles/:slug" element={<ArticleDetailPage />} />
          <Route path="/search" element={<SearchResultsPage />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

// Image lazy loading
function ArticleImage({ src, alt, className }: ImageProps) {
  const [loaded, setLoaded] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && imgRef.current) {
          imgRef.current.src = src;
          setLoaded(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, [src]);

  return (
    <img
      ref={imgRef}
      alt={alt}
      className={`${className} ${loaded ? 'loaded' : 'loading'}`}
      loading="lazy"
    />
  );
}
```

**Caching Strategy:**
```typescript
// API response caching
const articleCache = new Map<string, { data: Article; timestamp: number }>();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

async function getCachedArticle(id: string): Promise<Article> {
  const cached = articleCache.get(id);
  const now = Date.now();

  if (cached && (now - cached.timestamp) < CACHE_DURATION) {
    return cached.data;
  }

  const article = await apiClient.getArticle(id);
  articleCache.set(id, { data: article, timestamp: now });
  return article;
}

// Virtual scrolling for long lists
function VirtualizedArticleList({ articles }: { articles: Article[] }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={articles.length}
      itemSize={200}
      itemData={articles}
    >
      {ArticleListItem}
    </FixedSizeList>
  );
}
```

**SEO Implementation:**
```typescript
// SEO head management
function SEOHead({ article }: { article?: Article }) {
  const title = article
    ? `${article.headline} - News Site`
    : 'Latest News - News Site';

  const description = article?.summary || 'Stay informed with the latest news and analysis';

  const url = article
    ? `https://newssite.com/articles/${article.url}`
    : 'https://newssite.com';

  return (
    <Helmet>
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:url" content={url} />
      <meta property="og:type" content="article" />
      <meta name="twitter:card" content="summary_large_image" />
      <link rel="canonical" href={url} />
    </Helmet>
  );
}

// Structured data for search engines
function ArticleStructuredData({ article }: { article: Article }) {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": article.headline,
    "description": article.summary,
    "url": `https://newssite.com/articles/${article.url}`,
    "datePublished": article.generated_at,
    "author": {
      "@type": "Organization",
      "name": "News Site"
    }
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
    />
  );
}
```

**Deliverable**: Complete performance and SEO specification.

---

## Task 8: Write Complete PRD

**Objective**: Assemble all specifications into a comprehensive PRD.

### PRD Structure

**Section 1: System Overview (1-2 pages)**

- Frontend module purpose and scope
- Architecture overview with component relationships
- Success metrics and performance requirements

**Section 2: Functional Requirements (3-4 pages)**

- Feature 1: Article List & Browse
- Feature 2: Article Detail View
- Feature 3: Navigation & URL Structure
- Feature 4: Responsive Design
- Feature 5: Performance & Accessibility

**Section 3: Technical Specifications (4-5 pages)**

- React component hierarchy with TypeScript interfaces
- Redux store structure with actions and reducers
- API integration layer with request/response examples
- Responsive design implementation with CSS specifications

**Section 4: User Experience Design (2-3 pages)**

- Wireframes or mockups for all major pages
- User flow diagrams for common tasks
- Error state designs and messaging
- Loading state indicators and animations

**Section 5: Quality Assurance (2-3 pages)**

- Accessibility compliance plan (WCAG 2.1 AA)
- Performance budgets and optimization strategies
- Testing plan for components and user flows
- Browser compatibility requirements

**Section 6: Implementation Guidelines (1-2 pages)**

- Development setup and build configuration
- Deployment and hosting requirements
- Monitoring and analytics integration
- Maintenance and update procedures

---

## Quality Standards

### PRD Quality Standards

Use the [SpecKit templates](../../../../speckit/README.md) to create your comprehensive PRD. Your PRD must include:

- [ ] **Complete Component Specs**: All components with TypeScript interfaces
- [ ] **State Management**: Full Redux store structure with actions
- [ ] **API Integration**: Complete HTTP client with error handling
- [ ] **Responsive Design**: CSS specifications for all breakpoints
- [ ] **Accessibility**: WCAG 2.1 AA compliance implementation

### Implementation Readiness

- [ ] **Component Library**: Ready-to-implement React components
- [ ] **Routing Configuration**: Complete React Router setup
- [ ] **Build Configuration**: Webpack/Vite configuration specifications
- [ ] **Testing Framework**: Jest and React Testing Library setup
- [ ] **Performance Monitoring**: Metrics and optimization requirements

---

## Submission Requirements

### Deliverables Structure
```
deliverables/
├── PRD.md                              # Main specification document
├── components/
│   ├── component-hierarchy.md          # Complete component structure
│   ├── component-interfaces.ts         # TypeScript interfaces
│   └── styling-guide.md                # CSS architecture and design system
├── api/
│   ├── api-client.ts                   # HTTP client specification
│   └── api-contracts.yaml              # OpenAPI spec for Backend integration
├── state/
│   ├── redux-store.ts                  # Store structure and actions
│   └── data-flow.md                    # State management patterns
└── ux/
    ├── wireframes/                     # Page mockups and user flows
    ├── accessibility-plan.md           # WCAG compliance specification
    └── performance-requirements.md     # Performance budgets and metrics
```

### Quality Checklist

Before submission:

- [ ] All components have TypeScript interfaces and props specifications
- [ ] Complete Redux store with actions, reducers, and selectors
- [ ] API client handles all error scenarios with user-friendly messages
- [ ] Responsive design works on mobile, tablet, and desktop
- [ ] Accessibility features support keyboard navigation and screen readers
- [ ] Performance optimization includes lazy loading and caching
- [ ] SEO implementation with meta tags and structured data

---

## Timeline

**Week 1:**

- Days 1-2: Backend coordination and API contract definition
- Days 3-4: Component architecture and state management design
- Day 5: Responsive design and accessibility planning

**Week 2:**

- Days 1-3: Complete PRD writing with technical specifications
- Day 4: Internal review and testing with mock data
- Day 5: Final refinements and submission

---

## Success Criteria

Your PRD enables Phase 3 developers to:

- Implement the complete frontend application from specifications
- Integrate seamlessly with Backend APIs using provided contracts
- Deploy a responsive, accessible website that provides excellent user experience
- Create a news reading platform that handles all user scenarios gracefully

**Remember**: Your specifications must be complete enough for implementation without requiring additional design decisions.

