# Module 1: Data Ingestion Service

**Assigned Intern**: [Will be filled during deployment]  
**Research Focus**: Ethical & scalable data ingestion technology stack  
**Timeline**: 10 weeks (Research → Development → Integration → Demo)

## 🎯 Quick Start for Week 1
**Your Week 1 Task**: Complete research brief on data ingestion technologies  
**Deadline**: Friday 5PM  
**GitHub Issue**: [Will be added during deployment - Issue #1]

### What You Need to Do RIGHT NOW:
1. Read this entire README to understand the module scope
2. Review the research brief template at `/raw-materials/today-2025-09-07/04-intern-materials/week1-research-briefs.md`
3. Start researching the technologies listed in the "Week 1 Research Focus" section below
4. Complete your 2-page research brief by Friday

## 🔬 Week 1 Research Assignment

### Your Focus Question
**What technology stack and implementation approach will enable ethical, scalable data ingestion within our 10-week timeline while handling legal/compliance requirements?**

### Required Analysis Areas

#### 1. Professional Platform Comparison
- **ScrapingBee**: API-based web scraping service (analyze cost, features, learning curve)
- **Apify**: Web scraping and automation platform (evaluate complexity, capabilities)
- **Airbyte**: Open-source data integration platform (assess setup time, connector availability)
- **Fivetran**: Managed data pipeline service (review pricing, supported sources)

#### 2. Open Source Tool Evaluation
- **Scrapy vs Playwright vs Beautiful Soup**: Compare scraping frameworks (complexity, features, community)
- **FastAPI vs Flask**: API framework selection (performance, ease of use, async support)
- **Celery vs RQ vs Dramatiq**: Queue system comparison (scalability, setup complexity)
- **Content extraction libraries**: Newspaper3k, Readability, Trafilatura (quality, maintenance)

#### 3. Legal & Ethical Framework Assessment
- robots.txt compliance strategies
- Rate limiting implementation approaches
- GDPR/privacy considerations for content storage
- Terms of service analysis for target platforms

#### 4. AI Assistance Integration
- How can GitHub Copilot/Cursor accelerate adapter development?
- Which parts can be generated vs. require manual coding?
- Cost-benefit analysis of AI-powered vs traditional approaches

### Success Criteria for Your Research Brief
- ✅ Technology recommendation matrix with 1-5 scoring
- ✅ Implementation timeline showing AI assistance multipliers
- ✅ Legal compliance checklist with risk mitigation strategies
- ✅ Integration complexity assessment with other modules
- ✅ Clear fallback plan if primary approach fails

### Research Resources & Templates
- **Research Template**: [`/docs/templates/research-brief-template.md`](/docs/templates/research-brief-template.md)
- **Submission Format**: Create your research brief as `/docs/research/module-1-research-brief.md`
- **Module Specification**: [`/raw-materials/today-2025-09-07/intern-project-specs/modules/module-1-ingestion.md`](/raw-materials/today-2025-09-07/intern-project-specs/modules/module-1-ingestion.md)
- **Evaluation Rubric**: Available in docs/templates/ folder
- **GitHub Issue**: Your Week 1 assignment will be tracked via GitHub Issues with Friday 5PM deadline

### Research Submission Process
1. **Use the Template**: Copy `/docs/templates/research-brief-template.md` as your starting point
2. **Create Your Brief**: Save as `/docs/research/module-1-research-brief.md`
3. **Follow the Format**: Use the provided template structure exactly
4. **Submit via GitHub**: Commit your completed research brief and reference it in your assigned GitHub Issue
5. **Deadline**: Friday 5PM - no extensions without prior approval

### Additional Resources
- **Strategic Context**: Review the project handover documents in `/docs/handovers/` for background
- **Architecture Decisions**: Database selection framework in project documentation
- **Integration Points**: Study other module specifications to understand dependencies

## 📋 Module Overview
The Data Ingestion Service is the data acquisition layer of the Knowledge Graph Lab, responsible for fetching, normalizing, and processing content from multiple sources. It implements ethical scraping practices, respects rate limits, and provides clean, structured data to downstream modules through a RESTful API.

## Quick Start

```bash
# Navigate to module directory
cd modules/module-1-ingestion

# Install dependencies
pip install -r requirements.txt

# Run the service locally
python src/main.py

# Service runs on http://localhost:8001
# API docs available at http://localhost:8001/docs
```

## API Endpoints

### Health Check
```http
GET /health
```
Returns service health status and metadata.

**Response Example:**
```json
{
  "status": "healthy",
  "service": "ingestion",
  "version": "1.0.0",
  "timestamp": "2025-09-08T10:00:00Z"
}
```

### Ingest Single URL
```http
POST /api/ingest/url
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://example.com/article",
  "source_type": "web",
  "metadata": {
    "tags": ["creator-economy", "platform"],
    "priority": "high"
  }
}
```

**Response Example:**
```json
{
  "job_id": "ing_20250908_001",
  "status": "processing",
  "url": "https://example.com/article",
  "created_at": "2025-09-08T10:00:00Z",
  "estimated_completion": "2025-09-08T10:00:30Z"
}
```

### Bulk Ingestion
```http
POST /api/ingest/bulk
Content-Type: application/json
```

**Request Body:**
```json
{
  "urls": [
    "https://example.com/article1",
    "https://example.com/article2"
  ],
  "source_type": "web",
  "batch_name": "creator_platforms_batch_01"
}
```

### Check Ingestion Status
```http
GET /api/ingest/status/{job_id}
```

**Response Example:**
```json
{
  "job_id": "ing_20250908_001",
  "status": "completed",
  "progress": 100,
  "content": {
    "title": "The Future of Creator Platforms",
    "content": "Normalized article content...",
    "extracted_entities": ["Patreon", "Substack", "Creator Fund"],
    "metadata": {
      "author": "Jane Doe",
      "published_date": "2025-09-07",
      "word_count": 1250
    }
  },
  "completed_at": "2025-09-08T10:00:28Z"
}
```

### Source Management
```http
GET /api/sources
```
Lists all configured data sources.

```http
POST /api/sources
```
Add a new data source configuration.

**Request Body:**
```json
{
  "name": "TechCrunch RSS",
  "type": "rss",
  "url": "https://techcrunch.com/feed/",
  "frequency": "hourly",
  "categories": ["tech", "startups"]
}
```

### Content Retrieval (for other modules)
```http
GET /api/content?domain=creator-economy&location=boulder&limit=10
```

**Response Example:**
```json
{
  "total": 42,
  "items": [
    {
      "id": "content_001",
      "url": "https://example.com/article",
      "title": "Boulder's Growing Creator Economy",
      "content": "Normalized content text...",
      "domain": "creator-economy",
      "location": "boulder",
      "ingested_at": "2025-09-08T09:30:00Z",
      "quality_score": 0.85
    }
  ],
  "next_page": "/api/content?domain=creator-economy&offset=10"
}
```

## Dependencies

### External Services
- **Perplexity API**: For AI-powered web search and content discovery
- **RSS Feeds**: Various creator economy and tech news sources
- **Web Scraping**: Target sites with robots.txt compliance

### Other Modules
This module **provides** to:
- **Module 2 (Knowledge Graph)**: Clean, normalized content with extracted entities
- **Module 3 (Reasoning)**: Raw content for analysis and frontier queue decisions

This module **requires** from:
- None (it's the entry point for external data)

## Configuration

### Environment Variables
```bash
# API Keys
PERPLEXITY_API_KEY=your_api_key_here

# Service Configuration
INGESTION_PORT=8001
INGESTION_HOST=0.0.0.0
DATABASE_URL=sqlite:///./ingestion.db

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=60
RESPECT_ROBOTS_TXT=true
USER_AGENT="KGL-Bot/1.0 (Educational)"

# Content Processing
MIN_CONTENT_LENGTH=100
MAX_CONTENT_LENGTH=50000
DUPLICATE_THRESHOLD=0.85
```

### Source Configuration
Sources are configured via the API or in `config/sources.json`:
```json
{
  "sources": [
    {
      "id": "perplexity_api",
      "type": "api",
      "endpoint": "https://api.perplexity.ai/search",
      "rate_limit": 100,
      "priority": "high"
    },
    {
      "id": "creator_news_rss",
      "type": "rss",
      "url": "https://creatornews.com/feed",
      "frequency": "daily"
    }
  ]
}
```

## Testing

### Unit Tests
```bash
# Run unit tests
pytest tests/unit/

# Run with coverage
pytest tests/unit/ --cov=src --cov-report=html
```

### Integration Tests
```bash
# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/integration/

# Cleanup
docker-compose -f docker-compose.test.yml down
```

### Manual Testing with Mock Data
```bash
# Use mock data for testing without external dependencies
python src/main.py --use-mock-data

# Mock data responses are loaded from /mock-data/api-responses/module-1-ingestion.json
```

## Troubleshooting

### Common Issues

#### 1. Rate Limiting Errors
**Problem**: "429 Too Many Requests" errors from external sources
**Solution**: 
- Check `MAX_REQUESTS_PER_MINUTE` in environment variables
- Implement exponential backoff in `src/core/rate_limiter.py`
- Use the job queue system to spread requests over time

#### 2. Content Extraction Failures
**Problem**: Unable to extract content from JavaScript-heavy sites
**Solution**:
- Ensure Playwright is properly installed: `playwright install chromium`
- Check if the site requires specific headers or cookies
- Fall back to Perplexity API for problematic sites

#### 3. Database Connection Issues
**Problem**: "Database is locked" errors with SQLite
**Solution**:
- For development, ensure only one instance is running
- For production, consider migrating to PostgreSQL
- Check file permissions on the database file

#### 4. Memory Issues with Large Content
**Problem**: Service crashes when processing large documents
**Solution**:
- Adjust `MAX_CONTENT_LENGTH` to limit document size
- Implement streaming processing for large files
- Use chunking for PDF and document processing

#### 5. Duplicate Content Detection Not Working
**Problem**: Same content being ingested multiple times
**Solution**:
- Verify `DUPLICATE_THRESHOLD` is appropriately set (0.8-0.9 recommended)
- Check that content hashing is working in `src/services/deduplication.py`
- Clear the duplicate cache if it becomes corrupted

### Debug Mode
```bash
# Run with debug logging
LOG_LEVEL=DEBUG python src/main.py

# Enable SQL query logging
DEBUG_SQL=true python src/main.py
```

### Health Check Monitoring
```bash
# Check service health
curl http://localhost:8001/health

# Check specific adapter status
curl http://localhost:8001/health/adapters
```

## Architecture Notes

### Design Patterns
- **Adapter Pattern**: Pluggable source adapters for different data types
- **Queue Pattern**: Background job processing for long-running operations
- **Repository Pattern**: Data access abstraction for easy database switching

### Performance Considerations
- Async/await for concurrent processing
- Connection pooling for database and HTTP requests
- Redis caching for frequently accessed content
- Batch processing for bulk operations

### Security Measures
- Input validation on all endpoints
- SQL injection prevention via parameterized queries
- XSS protection in content processing
- API key rotation support
- Rate limiting per API key

## Getting Started Guide

### Week 1: Research & Planning (No Coding!)
1. **Environment Setup**: No development environment needed yet - focus on research
2. **Read Module Spec**: Study the detailed module specification linked above
3. **Research Technologies**: Use the research assignment framework to evaluate tools
4. **Document Findings**: Use the research brief template to document your analysis
5. **Submit Brief**: Complete and submit your 2-page research brief by Friday 5PM

### Week 2: Development Environment Setup
```bash
# Navigate to module directory
cd modules/module-1-ingestion

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (will be created based on your research)
pip install -r requirements.txt

# Set up development database
python scripts/setup_dev_db.py

# Run initial service (will be implemented in Week 3)
python src/main.py
```

### Week 3+: Implementation Path
- **Tier 1 (Weeks 3-6)**: Core data ingestion pipeline with ethical scraping
- **Tier 2 (Weeks 7-9)**: Advanced features and PeerMesh integration
- **Week 10**: Demo preparation and integration testing

## Module Development Tips

1. **Start Simple**: Begin with RSS feeds before tackling complex web scraping
2. **Mock First**: Use mock data to develop the API before implementing real ingestion
3. **Test Early**: Write tests as you develop each adapter
4. **Document APIs**: Keep the OpenAPI/Swagger docs updated
5. **Monitor Everything**: Add logging and metrics from the start
6. **WordPress Plugin Philosophy**: Build this module to be independent and reusable
7. **Legal First**: Always implement ethical scraping and compliance measures from day one

## Next Steps for Enhancement

- Implement advanced source discovery algorithms
- Add support for authenticated APIs (OAuth, API keys)
- Create custom extractors for specific platforms
- Build a source quality scoring system
- Add real-time streaming data support