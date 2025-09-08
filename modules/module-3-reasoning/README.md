# Module 3: Reasoning Engine Service

## Overview
The Reasoning Engine Service provides intelligent decision-making capabilities for the Knowledge Graph Lab, including frontier queue management for research prioritization, topic clustering for content organization, and automated digest generation. It uses AI to determine what to research next, synthesize insights from the knowledge graph, and generate personalized content for different audiences.

## Quick Start

```bash
# Navigate to module directory
cd modules/module-3-reasoning

# Install dependencies
pip install -r requirements.txt

# Run the service locally
python src/main.py

# Service runs on http://localhost:8003
# API docs available at http://localhost:8003/docs
```

## API Endpoints

### Health Check
```http
GET /health
```
Returns service health status and reasoning statistics.

**Response Example:**
```json
{
  "status": "healthy",
  "service": "reasoning",
  "version": "1.0.0",
  "stats": {
    "queue_size": 145,
    "topics_identified": 23,
    "digests_generated_today": 5,
    "average_reasoning_time_ms": 320
  },
  "timestamp": "2025-09-08T10:00:00Z"
}
```

### Frontier Queue - Get Next Research Items
```http
GET /api/frontier/next?count=5&domain=creator-economy
```
Returns prioritized list of items to research next.

**Response Example:**
```json
{
  "recommendations": [
    {
      "id": "frontier_001",
      "type": "entity_investigation",
      "target": "Beehiiv",
      "priority_score": 0.92,
      "reasoning": "Newsletter platform with rapid growth, limited current knowledge",
      "suggested_queries": [
        "Beehiiv pricing model vs Substack",
        "Beehiiv creator success stories",
        "Beehiiv API capabilities"
      ],
      "knowledge_gaps": ["pricing tiers", "user demographics", "integration options"],
      "estimated_value": "high"
    },
    {
      "id": "frontier_002",
      "type": "topic_exploration",
      "target": "AI-assisted content creation",
      "priority_score": 0.88,
      "reasoning": "Emerging trend with high creator interest, minimal coverage",
      "suggested_sources": ["techcrunch", "creator-economy-report", "producthunt"]
    }
  ],
  "metadata": {
    "total_candidates": 145,
    "filtering_criteria": "relevance > 0.7 AND recency < 7 days",
    "next_update": "2025-09-08T11:00:00Z"
  }
}
```

### Frontier Queue - Add Research Candidate
```http
POST /api/frontier/add
Content-Type: application/json
```

**Request Body:**
```json
{
  "type": "entity",
  "identifier": "New Platform XYZ",
  "source": "user_suggestion",
  "metadata": {
    "category": "creator-tools",
    "urgency": "medium"
  }
}
```

### Topic Clustering
```http
POST /api/topics/cluster
Content-Type: application/json
```

**Request Body:**
```json
{
  "content_ids": ["content_001", "content_002", "content_003"],
  "num_clusters": 5,
  "method": "kmeans"
}
```

**Response Example:**
```json
{
  "clusters": [
    {
      "id": "cluster_001",
      "name": "Newsletter Monetization",
      "size": 23,
      "key_terms": ["subscription", "newsletter", "paid content", "audience"],
      "representative_content": ["content_001", "content_045"],
      "coherence_score": 0.85
    },
    {
      "id": "cluster_002",
      "name": "Platform Comparisons",
      "size": 18,
      "key_terms": ["comparison", "features", "pricing", "migration"],
      "representative_content": ["content_002", "content_033"]
    }
  ],
  "unclustered_items": 3,
  "silhouette_score": 0.72
}
```

### Topic Discovery
```http
GET /api/topics/trending?timeframe=7d&min_mentions=5
```
Identifies trending topics based on recent content.

**Response Example:**
```json
{
  "trending_topics": [
    {
      "topic": "Creator Burnout Solutions",
      "mention_count": 47,
      "growth_rate": 2.3,
      "key_entities": ["Mental Health Apps", "Time Management Tools"],
      "sentiment": "concerned",
      "example_content": ["content_089", "content_091"]
    },
    {
      "topic": "AI Content Detection",
      "mention_count": 38,
      "growth_rate": 1.8,
      "sentiment": "mixed"
    }
  ],
  "emerging_topics": [
    {
      "topic": "Web3 Creator Platforms",
      "first_seen": "2025-09-01",
      "trajectory": "rising"
    }
  ]
}
```

### Digest Generation
```http
POST /api/digest/generate
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "user_001",
  "preferences": {
    "topics": ["platform-news", "monetization", "creator-tools"],
    "length": "medium",
    "tone": "professional"
  },
  "timeframe": "weekly",
  "format": "email"
}
```

**Response Example:**
```json
{
  "digest_id": "digest_20250908_001",
  "user_id": "user_001",
  "sections": [
    {
      "title": "Platform Updates This Week",
      "content": "**Patreon Launches New Analytics Dashboard**\n\nPatreon unveiled comprehensive creator analytics...",
      "key_points": [
        "Real-time earnings tracking",
        "Audience demographics insights",
        "Churn prediction features"
      ],
      "entities_mentioned": ["Patreon", "Creator Analytics"],
      "read_time": "2 min"
    },
    {
      "title": "Funding Opportunities",
      "content": "**New $10M Creator Fund Announced**\n\nA coalition of platforms announced...",
      "action_items": [
        "Application deadline: September 30",
        "Eligibility: 10k+ followers"
      ]
    }
  ],
  "summary": "This week saw major platform updates and new funding opportunities...",
  "total_read_time": "5 min",
  "generated_at": "2025-09-08T10:00:00Z"
}
```

### Newsletter Generation
```http
POST /api/newsletter/create
Content-Type: application/json
```

**Request Body:**
```json
{
  "template": "weekly_roundup",
  "target_audience": "creators",
  "topics": ["platform-updates", "success-stories", "tools"],
  "max_items": 5
}
```

### Social Media Content
```http
POST /api/social/generate
Content-Type: application/json
```

**Request Body:**
```json
{
  "platform": "twitter",
  "content_type": "thread",
  "topic": "creator-economy-trends",
  "tone": "informative"
}
```

**Response Example:**
```json
{
  "content": [
    {
      "tweet": "🧵 5 Creator Economy Trends You Can't Ignore in 2025:\n\n1/ AI-Powered Content Creation",
      "position": 1
    },
    {
      "tweet": "The rise of AI tools isn't replacing creators - it's amplifying them. Tools like @ClaudeAI and @midjourney are becoming essential parts of the creator toolkit.",
      "position": 2
    }
  ],
  "hashtags": ["CreatorEconomy", "ContentCreation", "AI"],
  "best_time_to_post": "2025-09-08T14:00:00Z"
}
```

## Dependencies

### External Services
- **OpenAI/Anthropic APIs**: For reasoning and content generation
- **LangChain**: For complex reasoning chains
- **Sentence Transformers**: For topic clustering

### Other Modules
This module **requires** from:
- **Module 1 (Ingestion)**: Raw content for analysis
- **Module 2 (Knowledge Graph)**: Entity relationships and knowledge structure

This module **provides** to:
- **Module 4 (Frontend)**: Generated digests, newsletters, and insights
- **Module 1 (Ingestion)**: Research priorities for targeted data collection

## Configuration

### Environment Variables
```bash
# AI Services
OPENAI_API_KEY=your_api_key_here
ANTHROPIC_API_KEY=your_api_key_here
REASONING_MODEL=gpt-4-turbo-preview

# Reasoning Configuration
FRONTIER_QUEUE_SIZE=200
PRIORITY_THRESHOLD=0.7
REASONING_TEMPERATURE=0.7
MAX_REASONING_TOKENS=2000

# Clustering Configuration
MIN_CLUSTER_SIZE=3
MAX_CLUSTERS=20
CLUSTERING_METHOD=kmeans

# Content Generation
DIGEST_MAX_LENGTH=1000
NEWSLETTER_TEMPLATE_DIR=./templates/newsletters
SOCIAL_CHAR_LIMITS={"twitter": 280, "linkedin": 3000}

# Service Configuration
REASONING_PORT=8003
REASONING_HOST=0.0.0.0
DATABASE_URL=sqlite:///./reasoning.db
```

### Reasoning Rules Configuration
Rules are defined in `config/reasoning_rules.json`:
```json
{
  "frontier_priorities": {
    "new_platform": 0.9,
    "funding_opportunity": 0.85,
    "policy_change": 0.8,
    "trending_topic": 0.75,
    "competitor_update": 0.7
  },
  "research_triggers": {
    "knowledge_age_days": 30,
    "min_entity_mentions": 3,
    "confidence_threshold": 0.6
  }
}
```

## Testing

### Unit Tests
```bash
# Run unit tests
pytest tests/unit/

# Test reasoning logic specifically
pytest tests/unit/test_frontier_queue.py
pytest tests/unit/test_digest_generation.py

# Run with coverage
pytest tests/unit/ --cov=src --cov-report=html
```

### Integration Tests
```bash
# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/integration/

# Test with mock LLM responses
pytest tests/integration/ --use-mock-llm
```

### Manual Testing with Mock Data
```bash
# Use mock reasoning responses
python src/main.py --use-mock-data

# Mock data loaded from /mock-data/api-responses/module-3-reasoning.json
```

## Troubleshooting

### Common Issues

#### 1. Poor Frontier Queue Prioritization
**Problem**: System suggests irrelevant or outdated research targets
**Solution**:
- Review and adjust priority weights in `config/reasoning_rules.json`
- Check recency filters and knowledge age thresholds
- Analyze queue history for patterns in bad recommendations
- Implement feedback loop for priority adjustment

#### 2. Topic Clustering Incoherence
**Problem**: Clusters don't make semantic sense or are too broad
**Solution**:
- Adjust `MIN_CLUSTER_SIZE` and `MAX_CLUSTERS` parameters
- Try different clustering algorithms (DBSCAN, hierarchical)
- Improve content embeddings quality
- Add domain-specific stop words

#### 3. Digest Generation Quality Issues
**Problem**: Generated digests are repetitive or miss important content
**Solution**:
- Review and improve prompt templates in `src/prompts/digest_prompts.py`
- Adjust content selection algorithms
- Implement diversity scoring in content selection
- Add user feedback mechanism for improvement

#### 4. LLM Response Timeouts
**Problem**: Reasoning requests timeout on complex operations
**Solution**:
- Break complex reasoning into smaller steps
- Implement caching for common reasoning patterns
- Use faster models for initial filtering
- Add timeout handling and fallback strategies

#### 5. Memory Issues with Large Queues
**Problem**: Service crashes with large frontier queues
**Solution**:
- Implement queue size limits and pruning strategies
- Use database-backed queue instead of in-memory
- Add pagination to queue operations
- Monitor memory usage and set alerts

### Debug Mode
```bash
# Run with debug logging
LOG_LEVEL=DEBUG python src/main.py

# Log all reasoning decisions
DEBUG_REASONING=true python src/main.py

# Save reasoning traces
SAVE_REASONING_TRACES=true python src/main.py
```

### Reasoning Inspection
```bash
# Inspect frontier queue state
python scripts/inspect_queue.py

# Analyze reasoning patterns
python scripts/analyze_reasoning.py --days 7

# Export reasoning metrics
python scripts/export_metrics.py --format csv
```

## Architecture Notes

### Design Patterns
- **Strategy Pattern**: Different reasoning strategies for different content types
- **Chain of Responsibility**: Multi-stage reasoning pipeline
- **Template Method**: Digest generation with customizable sections
- **Observer Pattern**: Real-time updates on reasoning decisions

### AI/ML Components
- **Frontier Queue**: Multi-armed bandit with Thompson sampling
- **Topic Clustering**: K-means with TF-IDF or sentence embeddings
- **Content Generation**: Template-based with LLM enhancement
- **Priority Scoring**: Weighted feature combination with learning

### Performance Optimizations
- Reasoning result caching with TTL
- Batch processing for clustering operations
- Async processing for digest generation
- Precomputed embeddings for common content

### Quality Assurance
- A/B testing for reasoning strategies
- User feedback integration
- Reasoning explanation generation
- Continuous learning from outcomes

## Module Development Tips

1. **Start with Rules**: Build rule-based reasoning before adding ML
2. **Test with Small Datasets**: Validate logic before scaling
3. **Monitor LLM Costs**: Reasoning can be expensive - optimize prompts
4. **Build Incrementally**: Start with simple prioritization, add complexity
5. **Track Decisions**: Log all reasoning for analysis and improvement

## Next Steps for Enhancement

- Implement reinforcement learning for frontier queue optimization
- Add multi-agent reasoning for complex decisions
- Build explanation generation for reasoning transparency
- Create personalized reasoning models per user
- Implement causal reasoning for trend prediction