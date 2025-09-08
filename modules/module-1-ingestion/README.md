# Module 1: Data Ingestion Service

## Overview
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

## Module Development Tips

1. **Start Simple**: Begin with RSS feeds before tackling complex web scraping
2. **Mock First**: Use mock data to develop the API before implementing real ingestion
3. **Test Early**: Write tests as you develop each adapter
4. **Document APIs**: Keep the OpenAPI/Swagger docs updated
5. **Monitor Everything**: Add logging and metrics from the start

## Next Steps for Enhancement

- Implement advanced source discovery algorithms
- Add support for authenticated APIs (OAuth, API keys)
- Create custom extractors for specific platforms
- Build a source quality scoring system
- Add real-time streaming data support