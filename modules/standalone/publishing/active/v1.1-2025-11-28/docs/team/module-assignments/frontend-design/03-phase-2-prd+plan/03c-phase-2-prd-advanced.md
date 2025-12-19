# Frontend Design - Phase 2 Advanced (Optional)

## Important Note

**Only work on these features after completing your main PRD assignment!**

These are optional enhancements for developers who finish their core Frontend PRD early and want to add sophisticated features that improve user experience, performance, and accessibility.

---

## Optional Advanced Features

### Advanced Feature 1: Intelligent Caching and Prefetching

**Problem**: Basic API calls can feel slow, especially on mobile connections.

**Solution**: Implement smart caching with predictive prefetching to make the site feel instant.

**Technical Implementation:**

```typescript
class IntelligentCache {
  private cache = new Map<string, CacheEntry>();
  private prefetchQueue = new Set<string>();

  interface CacheEntry {
    data: any;
    timestamp: number;
    ttl: number;
    accessCount: number;
    lastAccess: number;
  }

  async get<T>(key: string, fetcher: () => Promise<T>, ttl = 300000): Promise<T> {
    const entry = this.cache.get(key);
    const now = Date.now();

    // Return cached data if fresh
    if (entry && (now - entry.timestamp) < entry.ttl) {
      entry.accessCount++;
      entry.lastAccess = now;
      return entry.data;
    }

    // Fetch fresh data
    const data = await fetcher();
    this.cache.set(key, {
      data,
      timestamp: now,
      ttl,
      accessCount: 1,
      lastAccess: now
    });

    // Trigger prefetch for related content
    this.schedulePrefetch(key, data);

    return data;
  }

  private schedulePrefetch(key: string, data: any): void {
    // Prefetch related articles based on current article
    if (key.startsWith('article:') && data.topics) {
      const relatedKey = `articles?topics=${data.topics.slice(0, 2).join(',')}`;
      if (!this.cache.has(relatedKey) && !this.prefetchQueue.has(relatedKey)) {
        this.prefetchQueue.add(relatedKey);
        // Prefetch after short delay to not block main thread
        setTimeout(() => this.executePrefetch(relatedKey), 100);
      }
    }
  }

  private async executePrefetch(key: string): Promise<void> {
    try {
      // Implement background prefetch logic
      await this.backgroundFetch(key);
      this.prefetchQueue.delete(key);
    } catch (error) {
      // Silently fail prefetch - it's not critical
      console.debug('Prefetch failed:', key, error);
    }
  }
}
```

**Smart Prefetching Strategy:**
```typescript
class PrefetchManager {
  private observer: IntersectionObserver;

  constructor(private apiClient: ArticleAPIClient, private cache: IntelligentCache) {
    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const articleId = entry.target.getAttribute('data-article-id');
            if (articleId) {
              this.prefetchArticle(articleId);
            }
          }
        });
      },
      { threshold: 0.5, rootMargin: '100px' }
    );
  }

  observeArticleCard(element: HTMLElement, articleId: string): void {
    element.setAttribute('data-article-id', articleId);
    this.observer.observe(element);
  }

  private async prefetchArticle(id: string): Promise<void> {
    const cacheKey = `article:${id}`;
    await this.cache.get(cacheKey, () => this.apiClient.getArticle(id));
  }
}
```

### Advanced Feature 2: Real-time Updates and Live Articles

**Objective**: Keep article lists fresh with real-time updates for breaking news.

**WebSocket Implementation:**
```typescript
class LiveArticleUpdates {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  constructor(
    private dispatch: AppDispatch,
    private wsUrl: string
  ) {}

  connect(): void {
    try {
      this.ws = new WebSocket(this.wsUrl);

      this.ws.onopen = () => {
        console.log('Live updates connected');
        this.reconnectAttempts = 0;
        this.dispatch(setConnectionStatus('connected'));
      };

      this.ws.onmessage = (event) => {
        const update = JSON.parse(event.data);
        this.handleUpdate(update);
      };

      this.ws.onclose = () => {
        this.dispatch(setConnectionStatus('disconnected'));
        this.attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.dispatch(setConnectionStatus('error'));
      };
    } catch (error) {
      console.error('Failed to connect to live updates:', error);
    }
  }

  private handleUpdate(update: LiveUpdate): void {
    switch (update.type) {
      case 'new_article':
        this.dispatch(addNewArticle(update.article));
        this.showNewArticleNotification(update.article);
        break;

      case 'article_updated':
        this.dispatch(updateArticle(update.article));
        break;

      case 'breaking_news':
        this.dispatch(addBreakingNews(update.article));
        this.showBreakingNewsAlert(update.article);
        break;
    }
  }

  private showNewArticleNotification(article: Article): void {
    // Show non-intrusive notification for new articles
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('New Article Available', {
        body: article.headline,
        icon: '/favicon.ico',
        tag: 'new-article'
      });
    }
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      const delay = Math.pow(2, this.reconnectAttempts) * 1000; // Exponential backoff
      setTimeout(() => {
        this.reconnectAttempts++;
        this.connect();
      }, delay);
    }
  }
}
```

**Live Update UI Components:**
```typescript
function LiveUpdateIndicator() {
  const connectionStatus = useSelector(selectConnectionStatus);
  const newArticlesCount = useSelector(selectNewArticlesCount);

  return (
    <div className="live-update-indicator">
      <div className={`connection-status ${connectionStatus}`}>
        {connectionStatus === 'connected' && <OnlineIcon />}
        {connectionStatus === 'disconnected' && <OfflineIcon />}
        {connectionStatus === 'error' && <ErrorIcon />}
      </div>

      {newArticlesCount > 0 && (
        <button
          className="new-articles-banner"
          onClick={() => dispatch(loadNewArticles())}
        >
          {newArticlesCount} new article{newArticlesCount > 1 ? 's' : ''} available
          <RefreshIcon />
        </button>
      )}
    </div>
  );
}
```

### Advanced Feature 3: Advanced Search with Autocomplete

**Smart Search Implementation:**
```typescript
class AdvancedSearchEngine {
  private searchIndex: Map<string, SearchEntry[]> = new Map();
  private searchHistory: string[] = [];

  interface SearchEntry {
    id: string;
    type: 'article' | 'topic' | 'entity';
    title: string;
    content: string;
    relevanceScore: number;
  }

  async searchWithSuggestions(query: string): Promise<SearchResults> {
    const suggestions = await this.generateSuggestions(query);
    const results = await this.performSearch(query);

    return {
      query,
      suggestions,
      results,
      filters: await this.generateSmartFilters(results)
    };
  }

  private async generateSuggestions(query: string): Promise<SearchSuggestion[]> {
    const suggestions: SearchSuggestion[] = [];

    // Recent searches
    const recentMatches = this.searchHistory.filter(term =>
      term.toLowerCase().includes(query.toLowerCase())
    ).slice(0, 3);

    suggestions.push(...recentMatches.map(term => ({
      type: 'recent',
      text: term,
      icon: 'history'
    })));

    // Topic suggestions
    const topicMatches = await this.findMatchingTopics(query);
    suggestions.push(...topicMatches.map(topic => ({
      type: 'topic',
      text: topic,
      icon: 'tag'
    })));

    // Entity suggestions (people, companies)
    const entityMatches = await this.findMatchingEntities(query);
    suggestions.push(...entityMatches.map(entity => ({
      type: 'entity',
      text: entity.name,
      icon: entity.type === 'person' ? 'person' : 'building'
    })));

    return suggestions.slice(0, 8); // Limit suggestions
  }

  private async performSearch(query: string): Promise<Article[]> {
    // Combine multiple search strategies
    const [
      titleMatches,
      contentMatches,
      semanticMatches
    ] = await Promise.all([
      this.searchByTitle(query),
      this.searchByContent(query),
      this.semanticSearch(query)
    ]);

    // Merge and rank results
    const allResults = new Map<string, Article>();

    titleMatches.forEach(article => {
      allResults.set(article.id, { ...article, searchScore: article.relevanceScore * 1.5 });
    });

    contentMatches.forEach(article => {
      const existing = allResults.get(article.id);
      if (existing) {
        existing.searchScore = Math.max(existing.searchScore, article.relevanceScore);
      } else {
        allResults.set(article.id, { ...article, searchScore: article.relevanceScore });
      }
    });

    semanticMatches.forEach(article => {
      const existing = allResults.get(article.id);
      if (existing) {
        existing.searchScore += article.relevanceScore * 0.3; // Boost semantic matches
      } else {
        allResults.set(article.id, { ...article, searchScore: article.relevanceScore * 0.3 });
      }
    });

    return Array.from(allResults.values())
      .sort((a, b) => b.searchScore - a.searchScore)
      .slice(0, 50); // Limit results
  }
}
```

**Search UI with Autocomplete:**
```typescript
function AdvancedSearchBar() {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const searchEngine = useRef(new AdvancedSearchEngine());

  const debouncedSearch = useCallback(
    debounce(async (searchQuery: string) => {
      if (searchQuery.length > 2) {
        const results = await searchEngine.current.searchWithSuggestions(searchQuery);
        setSuggestions(results.suggestions);
        setShowSuggestions(true);
      } else {
        setShowSuggestions(false);
      }
    }, 300),
    []
  );

  const handleKeyDown = (e: KeyboardEvent) => {
    if (!showSuggestions) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev =>
          prev < suggestions.length - 1 ? prev + 1 : prev
        );
        break;

      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
        break;

      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0) {
          handleSuggestionSelect(suggestions[selectedIndex]);
        } else {
          performSearch(query);
        }
        break;

      case 'Escape':
        setShowSuggestions(false);
        setSelectedIndex(-1);
        break;
    }
  };

  return (
    <div className="advanced-search-container">
      <div className="search-input-wrapper">
        <SearchIcon />
        <input
          type="text"
          placeholder="Search articles, topics, or people..."
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            debouncedSearch(e.target.value);
          }}
          onKeyDown={handleKeyDown}
          onFocus={() => query.length > 2 && setShowSuggestions(true)}
          aria-label="Search articles"
          aria-autocomplete="list"
          aria-expanded={showSuggestions}
        />
        {query && (
          <button
            className="clear-search"
            onClick={() => {
              setQuery('');
              setShowSuggestions(false);
            }}
            aria-label="Clear search"
          >
            <CloseIcon />
          </button>
        )}
      </div>

      {showSuggestions && suggestions.length > 0 && (
        <ul className="search-suggestions" role="listbox">
          {suggestions.map((suggestion, index) => (
            <li
              key={`${suggestion.type}-${suggestion.text}`}
              className={`suggestion-item ${index === selectedIndex ? 'selected' : ''}`}
              role="option"
              aria-selected={index === selectedIndex}
              onClick={() => handleSuggestionSelect(suggestion)}
            >
              <Icon name={suggestion.icon} />
              <span className="suggestion-text">{suggestion.text}</span>
              <span className="suggestion-type">{suggestion.type}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### Advanced Feature 4: Personalization and Reading Analytics

**User Behavior Tracking:**
```typescript
class ReadingAnalytics {
  private readingData: Map<string, ReadingSession> = new Map();

  interface ReadingSession {
    articleId: string;
    startTime: number;
    endTime?: number;
    scrollDepth: number;
    timeSpent: number;
    interactionEvents: InteractionEvent[];
  }

  interface InteractionEvent {
    type: 'scroll' | 'click' | 'share' | 'bookmark';
    timestamp: number;
    data?: any;
  }

  startReading(articleId: string): void {
    const session: ReadingSession = {
      articleId,
      startTime: Date.now(),
      scrollDepth: 0,
      timeSpent: 0,
      interactionEvents: []
    };

    this.readingData.set(articleId, session);
    this.trackScrollBehavior(articleId);
  }

  endReading(articleId: string): ReadingMetrics {
    const session = this.readingData.get(articleId);
    if (!session) return null;

    session.endTime = Date.now();
    session.timeSpent = session.endTime - session.startTime;

    const metrics = this.calculateReadingMetrics(session);
    this.sendAnalytics(metrics);

    return metrics;
  }

  private trackScrollBehavior(articleId: string): void {
    let lastScrollTime = Date.now();
    let maxScrollDepth = 0;

    const handleScroll = throttle(() => {
      const session = this.readingData.get(articleId);
      if (!session) return;

      const scrollPercent = this.calculateScrollPercent();
      maxScrollDepth = Math.max(maxScrollDepth, scrollPercent);
      session.scrollDepth = maxScrollDepth;

      // Track reading pace
      const now = Date.now();
      if (now - lastScrollTime > 1000) { // Active reading
        session.interactionEvents.push({
          type: 'scroll',
          timestamp: now,
          data: { scrollPercent }
        });
      }
      lastScrollTime = now;
    }, 500);

    window.addEventListener('scroll', handleScroll);

    // Cleanup when user leaves
    return () => window.removeEventListener('scroll', handleScroll);
  }

  private calculateReadingMetrics(session: ReadingSession): ReadingMetrics {
    const readingSpeed = this.estimateReadingSpeed(session);
    const engagement = this.calculateEngagement(session);
    const completion = session.scrollDepth / 100;

    return {
      articleId: session.articleId,
      timeSpent: session.timeSpent,
      scrollDepth: session.scrollDepth,
      readingSpeed,
      engagement,
      completion,
      interactionCount: session.interactionEvents.length
    };
  }
}
```

**Personalized Recommendations:**
```typescript
class PersonalizationEngine {
  private userProfile: UserProfile;

  interface UserProfile {
    preferredTopics: TopicScore[];
    readingBehavior: ReadingBehavior;
    timePreferences: TimePreferences;
    engagementHistory: EngagementData[];
  }

  async getPersonalizedArticles(candidateArticles: Article[]): Promise<Article[]> {
    const scoredArticles = candidateArticles.map(article => ({
      ...article,
      personalScore: this.calculatePersonalScore(article)
    }));

    return scoredArticles
      .sort((a, b) => b.personalScore - a.personalScore)
      .slice(0, 20);
  }

  private calculatePersonalScore(article: Article): number {
    let score = article.quality_score; // Base quality

    // Topic preferences
    const topicScore = this.getTopicPreferenceScore(article.topics);
    score += topicScore * 0.3;

    // Reading time match
    const timeScore = this.getReadingTimeScore(article);
    score += timeScore * 0.2;

    // Recency preference
    const recencyScore = this.getRecencyScore(article);
    score += recencyScore * 0.2;

    // Engagement prediction
    const engagementScore = this.predictEngagement(article);
    score += engagementScore * 0.3;

    return Math.min(score, 1.0);
  }

  private getTopicPreferenceScore(topics: string[]): number {
    const userTopics = this.userProfile.preferredTopics;
    let totalScore = 0;

    topics.forEach(topic => {
      const preference = userTopics.find(ut => ut.topic === topic);
      if (preference) {
        totalScore += preference.score;
      }
    });

    return totalScore / topics.length;
  }

  private predictEngagement(article: Article): number {
    // Use historical data to predict if user will engage with this article
    const similarArticles = this.userProfile.engagementHistory.filter(
      eng => eng.topics.some(topic => article.topics.includes(topic))
    );

    if (similarArticles.length === 0) return 0.5; // Neutral

    const avgEngagement = similarArticles.reduce(
      (sum, eng) => sum + eng.engagementScore, 0
    ) / similarArticles.length;

    return avgEngagement;
  }
}
```

### Advanced Feature 5: Offline Support and Progressive Web App

**Service Worker Implementation:**
```typescript
// service-worker.ts
const CACHE_NAME = 'news-app-v1';
const OFFLINE_CACHE = 'offline-articles';

const STATIC_RESOURCES = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/offline.html'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(STATIC_RESOURCES))
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Handle API requests
  if (request.url.includes('/api/v1/reports')) {
    event.respondWith(handleAPIRequest(request));
    return;
  }

  // Handle navigation requests
  if (request.mode === 'navigate') {
    event.respondWith(handleNavigationRequest(request));
    return;
  }

  // Handle static resources
  event.respondWith(handleStaticRequest(request));
});

async function handleAPIRequest(request: Request): Promise<Response> {
  try {
    // Try network first
    const networkResponse = await fetch(request);

    if (networkResponse.ok) {
      // Cache successful responses
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    // Network failed, try cache
    const cachedResponse = await caches.match(request);

    if (cachedResponse) {
      // Add offline indicator to response
      return new Response(cachedResponse.body, {
        status: cachedResponse.status,
        statusText: cachedResponse.statusText,
        headers: {
          ...cachedResponse.headers,
          'X-Served-By': 'cache'
        }
      });
    }

    // Return offline fallback
    return new Response(JSON.stringify({
      error: 'Offline',
      message: 'This content is not available offline'
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
```

**Offline UI Components:**
```typescript
function OfflineIndicator() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [hasOfflineContent, setHasOfflineContent] = useState(false);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Check for cached articles
    checkOfflineContent().then(setHasOfflineContent);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  if (isOnline) return null;

  return (
    <div className="offline-indicator">
      <OfflineIcon />
      <span>You're offline</span>
      {hasOfflineContent && (
        <button onClick={() => navigate('/offline')}>
          View saved articles
        </button>
      )}
    </div>
  );
}

function OfflineArticleManager() {
  const [savedArticles, setSavedArticles] = useState<Article[]>([]);

  const saveForOffline = async (article: Article) => {
    const cache = await caches.open(OFFLINE_CACHE);

    // Cache the article data
    await cache.put(
      `/api/v1/reports/${article.id}`,
      new Response(JSON.stringify(article))
    );

    // Cache any images
    if (article.images) {
      for (const image of article.images) {
        try {
          await cache.add(image.url);
        } catch (error) {
          console.warn('Failed to cache image:', image.url);
        }
      }
    }

    // Update saved articles list
    const updated = [...savedArticles, article];
    setSavedArticles(updated);

    // Store in IndexedDB for persistence
    await storeOfflineArticle(article);
  };

  const removeFromOffline = async (articleId: string) => {
    const cache = await caches.open(OFFLINE_CACHE);
    await cache.delete(`/api/v1/reports/${articleId}`);

    setSavedArticles(prev => prev.filter(a => a.id !== articleId));
    await removeOfflineArticle(articleId);
  };

  return (
    <div className="offline-manager">
      <h3>Saved for Offline Reading</h3>
      {savedArticles.map(article => (
        <div key={article.id} className="offline-article-item">
          <h4>{article.headline}</h4>
          <p>{article.summary}</p>
          <button onClick={() => removeFromOffline(article.id)}>
            Remove
          </button>
        </div>
      ))}
    </div>
  );
}
```

---

## Implementation Guidelines

### Development Approach
- **Incremental Development**: Implement one advanced feature at a time
- **Feature Flags**: Use configuration flags to enable/disable advanced features
- **Backward Compatibility**: Ensure basic article browsing always works
- **Performance Monitoring**: Track impact of advanced features on page load times

### Testing Strategy
- **A/B Testing**: Test advanced features against baseline experience
- **Performance Testing**: Ensure advanced features don't slow down core functionality
- **Accessibility Testing**: Validate that enhancements improve rather than hurt accessibility
- **Cross-Browser Testing**: Test advanced features across different browsers and devices

### Maintenance Considerations
- **Progressive Enhancement**: Advanced features should enhance, not replace basic functionality
- **Fallback Strategies**: Provide graceful degradation when advanced features fail
- **Monitoring**: Track feature usage and performance impact
- **User Feedback**: Collect feedback on advanced features and iterate

---

## Advanced PRD Sections

If including advanced features in your PRD:

### Section 7: Advanced User Experience (2-3 pages)
- Intelligent caching and prefetching strategies
- Real-time updates and live article feeds
- Advanced search with autocomplete and suggestions

### Section 8: Personalization and Analytics (2-3 pages)
- User behavior tracking and reading analytics
- Personalized content recommendations
- Learning algorithms for improving user experience

### Section 9: Progressive Web App Features (1-2 pages)
- Offline support and service worker implementation
- Background sync for article updates
- Push notifications for breaking news

---

## Success Criteria for Advanced Work

Advanced features are successful when they:

- [ ] **Measurably improve user engagement** (time spent reading, articles per session)
- [ ] **Don't compromise performance** or basic functionality
- [ ] **Are well-documented** with clear implementation specifications
- [ ] **Provide genuine value** to users and don't feel like unnecessary complexity
- [ ] **Scale efficiently** with growing content and user base

---

## Integration with Core System

### Architectural Considerations
- **Modular Design**: Advanced features should be optional plugins
- **Performance Isolation**: Advanced processing shouldn't block basic article loading
- **Fallback Strategies**: Core functionality must work if advanced features fail
- **Configuration Management**: Easy to enable/disable features per environment

### Data Requirements
- **Extended Analytics**: Additional tracking for personalization and optimization
- **User Profiling**: Enhanced user data models for personalization
- **Feature Flags**: Configuration system for enabling/disabling advanced features
- **Performance Metrics**: Monitoring data for advanced feature impact

---

## Remember

Advanced features should **enhance** your core article reading experience, not replace it. A fast, accessible website that reliably displays articles is more important than sophisticated features that introduce complexity or reduce reliability.

**Focus on delivering excellent basic functionality first, then selectively add advanced features that provide measurable value to users.**