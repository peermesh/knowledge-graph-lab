# Module 2: AI Knowledge Graph Service

**Assigned Intern**: [Will be filled during deployment]  
**Research Focus**: Autonomous research system architecture and scope management  
**Timeline**: 10 weeks (Research → Development → Integration → Demo)  
**Complexity Level**: ⚠️ **HIGH** - Most technically sophisticated module

## 🎯 Quick Start for Week 1
**Your Week 1 Task**: Complete research brief on autonomous research systems  
**Deadline**: Friday 5PM  
**GitHub Issue**: [Will be added during deployment - Issue #2]

### What You Need to Do RIGHT NOW:
1. Read this entire README to understand the module scope
2. Review the research brief template at `/docs/templates/research-brief-template.md`
3. Focus on the "Week 1 Research Focus" section below
4. Complete your 2-page research brief by Friday

## 🔬 Week 1 Research Assignment

### Your Focus Question
**How can we build an autonomous research system that manages knowledge graphs and entity relationships within realistic scope for a 10-week project, considering the HIGH complexity warning?**

⚠️ **CRITICAL**: This module has the highest complexity. Focus heavily on scope reduction and practical implementation.

### Required Analysis Areas

#### 1. Scope Reduction Strategy Assessment
- **Minimum Viable System**: What's the simplest autonomous research system that adds value?
- **Tiered Implementation**: How to build Basic → Enhanced → Advanced tiers
- **Complexity Management**: Strategies to prevent scope creep and over-engineering
- **Fallback Planning**: Template-based vs. AI-powered approaches with manual override strategies

#### 2. Knowledge Management Platform Evaluation  
- **Enterprise Solutions**: Notion AI, Obsidian, Roam Research integration possibilities
- **Graph Databases**: Neo4j vs PostgreSQL graph extensions vs simple relational approaches
- **Vector Databases**: Qdrant, Chroma, Weaviate for similarity search and RAG
- **API Integrations**: Perplexity API, OpenAI, local LLM options (Ollama)

#### 3. Entity Extraction & NLP Tool Analysis
- **Professional Services**: OpenAI API, Anthropic Claude, Hugging Face hosted models
- **Open Source Options**: spaCy, Stanford NER, Hugging Face transformers locally
- **Cost-Benefit Analysis**: API costs vs local compute vs development time trade-offs
- **Accuracy vs Speed**: Quality requirements for creator economy domain

#### 4. Integration & Architecture Planning
- **Module Independence**: How to maintain WordPress plugin philosophy while sharing knowledge
- **Database Architecture**: Decision framework for knowledge storage and relationships
- **API Design**: Clean interfaces for other modules to access knowledge
- **Performance Considerations**: Scaling knowledge graphs without performance degradation

### Success Criteria for Your Research Brief
- ✅ Tiered implementation plan (Basic → Enhanced → Advanced) with clear scope boundaries
- ✅ AI service cost analysis and provider comparison with budget considerations
- ✅ Knowledge graph schema design specifically for creator economy domain
- ✅ Risk mitigation strategies with simplified fallback approaches
- ✅ Clear integration plan with realistic complexity assessment

### Research Resources & Templates
- **Research Template**: [`/docs/templates/research-brief-template.md`](/docs/templates/research-brief-template.md)
- **Submission Format**: Create your research brief as `/docs/research/module-2-research-brief.md`
- **Module Specification**: [`/raw-materials/today-2025-09-07/intern-project-specs/modules/module-2-knowledge-graph.md`](/raw-materials/today-2025-09-07/intern-project-specs/modules/module-2-knowledge-graph.md)
- **Evaluation Rubric**: Available in docs/templates/ folder
- **GitHub Issue**: Your Week 1 assignment will be tracked via GitHub Issues with Friday 5PM deadline

### Research Submission Process
1. **Use the Template**: Copy `/docs/templates/research-brief-template.md` as your starting point
2. **Create Your Brief**: Save as `/docs/research/module-2-research-brief.md`  
3. **Include Artifacts**: Entity schema diagram, AI service integration plan with cost projections
4. **Submit via GitHub**: Commit your completed research brief and reference it in your assigned GitHub Issue
5. **Deadline**: Friday 5PM - no extensions without prior approval

### Additional Resources
- **Strategic Context**: Review project handover documents for autonomous research vision
- **Database Decisions**: Study the database architecture decision framework
- **Complexity Warnings**: Review fallback strategies in module specifications

## Overview
The AI Knowledge Graph Service transforms raw content into structured knowledge by performing entity extraction, relationship discovery, and knowledge organization. It builds and maintains a graph database of interconnected entities in the creator economy domain, providing intelligent query capabilities and entity resolution through advanced NLP techniques.

## Quick Start

```bash
# Navigate to module directory
cd modules/module-2-knowledge-graph

# Install dependencies
pip install -r requirements.txt

# Run the service locally
python src/main.py

# Service runs on http://localhost:8002
# API docs available at http://localhost:8002/docs
```

## API Endpoints

### Health Check
```http
GET /health
```
Returns service health status and graph statistics.

**Response Example:**
```json
{
  "status": "healthy",
  "service": "knowledge-graph",
  "version": "1.0.0",
  "stats": {
    "total_entities": 1247,
    "total_relationships": 3892,
    "entity_types": ["Platform", "Organization", "Person", "Grant", "Policy", "Event"]
  },
  "timestamp": "2025-09-08T10:00:00Z"
}
```

### Entity Extraction
```http
POST /api/entities/extract
Content-Type: application/json
```

**Request Body:**
```json
{
  "content_id": "content_001",
  "text": "Patreon announced a new creator fund in partnership with Kickstarter...",
  "metadata": {
    "source": "techcrunch",
    "date": "2025-09-07"
  }
}
```

**Response Example:**
```json
{
  "entities": [
    {
      "id": "entity_patreon_001",
      "name": "Patreon",
      "type": "Platform",
      "confidence": 0.95,
      "mentions": [{"start": 0, "end": 7}],
      "attributes": {
        "website": "patreon.com",
        "category": "subscription-platform"
      }
    },
    {
      "id": "entity_fund_001",
      "name": "Patreon Creator Fund",
      "type": "Grant",
      "confidence": 0.88,
      "mentions": [{"start": 24, "end": 36}]
    }
  ],
  "relationships": [
    {
      "source": "entity_patreon_001",
      "target": "entity_fund_001",
      "type": "OPERATES",
      "confidence": 0.92
    }
  ]
}
```

### Entity Resolution
```http
POST /api/entities/resolve
Content-Type: application/json
```

**Request Body:**
```json
{
  "entities": [
    {"name": "Patreon", "context": "platform"},
    {"name": "patreon.com", "context": "website"},
    {"name": "@patreon", "context": "twitter"}
  ]
}
```

**Response Example:**
```json
{
  "resolved_entity": {
    "id": "entity_patreon_master",
    "canonical_name": "Patreon",
    "type": "Platform",
    "aliases": ["patreon.com", "@patreon", "Patreon Inc."],
    "confidence": 0.96,
    "merged_from": ["entity_001", "entity_002", "entity_003"]
  }
}
```

### Knowledge Query
```http
GET /api/knowledge/query?entity=Patreon&depth=2
```
Retrieves entity information and related entities up to specified depth.

**Response Example:**
```json
{
  "entity": {
    "id": "entity_patreon_master",
    "name": "Patreon",
    "type": "Platform",
    "attributes": {
      "founded": "2013",
      "headquarters": "San Francisco, CA",
      "category": "creator-monetization"
    }
  },
  "relationships": [
    {
      "type": "COMPETITOR",
      "target": {
        "id": "entity_substack",
        "name": "Substack",
        "type": "Platform"
      }
    },
    {
      "type": "PARTNERS_WITH",
      "target": {
        "id": "entity_stripe",
        "name": "Stripe",
        "type": "Organization"
      }
    }
  ],
  "stats": {
    "total_connections": 23,
    "relationship_types": ["COMPETITOR", "PARTNERS_WITH", "INTEGRATES_WITH"]
  }
}
```

### Graph Search
```http
POST /api/knowledge/search
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "Find all grants available for creators in Boulder",
  "filters": {
    "entity_types": ["Grant"],
    "location": "Boulder, CO",
    "min_confidence": 0.7
  }
}
```

### Research Context
```http
GET /api/research/context/{topic}
```
Provides research context and suggested entities for a topic.

**Response Example:**
```json
{
  "topic": "creator-monetization",
  "key_entities": [
    {"name": "Patreon", "relevance": 0.95},
    {"name": "Substack", "relevance": 0.92},
    {"name": "OnlyFans", "relevance": 0.88}
  ],
  "suggested_queries": [
    "Platform comparison for newsletter creators",
    "Subscription model trends 2025",
    "Creator fund opportunities"
  ],
  "knowledge_gaps": [
    "Limited data on creator earnings distribution",
    "Missing policy information for Colorado"
  ]
}
```

## Dependencies

### External Services
- **OpenAI API**: For advanced NLP and entity extraction
- **Neo4j** (optional): Graph database for production deployment
- **Hugging Face Models**: For local NER if API unavailable

### Other Modules
This module **requires** from:
- **Module 1 (Ingestion)**: Normalized content and initial entity mentions

This module **provides** to:
- **Module 3 (Reasoning)**: Knowledge graph structure and entity relationships
- **Module 4 (Frontend)**: Entity data and relationship visualizations

## Configuration

### Environment Variables
```bash
# AI Services
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-small

# Database Configuration
GRAPH_DATABASE=sqlite  # or neo4j for production
DATABASE_URL=sqlite:///./knowledge_graph.db
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# NLP Configuration
MIN_ENTITY_CONFIDENCE=0.7
ENTITY_RESOLUTION_THRESHOLD=0.85
MAX_RELATIONSHIP_DEPTH=3

# Service Configuration
KNOWLEDGE_PORT=8002
KNOWLEDGE_HOST=0.0.0.0
```

### Schema Configuration
Domain schemas are defined in `config/schemas/`:
```json
{
  "creator_economy": {
    "entities": {
      "Platform": {
        "attributes": ["name", "website", "category", "founded"],
        "key_relationships": ["COMPETES_WITH", "INTEGRATES_WITH"]
      },
      "Organization": {
        "attributes": ["name", "type", "location", "website"],
        "key_relationships": ["FUNDS", "PARTNERS_WITH"]
      },
      "Person": {
        "attributes": ["name", "role", "affiliations"],
        "key_relationships": ["WORKS_AT", "FOUNDED", "ADVISES"]
      }
    }
  }
}
```

## Testing

### Unit Tests
```bash
# Run unit tests
pytest tests/unit/

# Test entity extraction specifically
pytest tests/unit/test_entity_extraction.py

# Test with coverage
pytest tests/unit/ --cov=src --cov-report=html
```

### Integration Tests
```bash
# Start test environment with mock LLM
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/integration/

# Test graph queries
pytest tests/integration/test_graph_queries.py
```

### Manual Testing with Mock Data
```bash
# Use mock entities and relationships
python src/main.py --use-mock-data

# Mock data loaded from /mock-data/api-responses/module-2-knowledge-graph.json
```

## Troubleshooting

### Common Issues

#### 1. Entity Extraction Accuracy Issues
**Problem**: Poor entity recognition or many false positives
**Solution**:
- Adjust `MIN_ENTITY_CONFIDENCE` threshold
- Fine-tune prompts in `src/prompts/entity_extraction.py`
- Consider using specialized NER models for specific entity types
- Implement entity validation rules in schema

#### 2. Entity Resolution Conflicts
**Problem**: Same entity being created multiple times
**Solution**:
- Lower `ENTITY_RESOLUTION_THRESHOLD` for more aggressive merging
- Improve context clues in resolution algorithm
- Add manual override rules for known problematic entities
- Check alias mapping in `config/entity_aliases.json`

#### 3. Graph Query Performance
**Problem**: Slow queries with deep relationship traversal
**Solution**:
- Limit `MAX_RELATIONSHIP_DEPTH` in configuration
- Add indexes on frequently queried attributes
- Consider moving to Neo4j for complex graph operations
- Implement query result caching

#### 4. OpenAI API Rate Limits
**Problem**: "Rate limit exceeded" errors during batch processing
**Solution**:
- Implement exponential backoff in API calls
- Use batching strategies in `src/services/llm_service.py`
- Consider local models for high-volume operations
- Cache embeddings to reduce API calls

#### 5. Memory Issues with Large Graphs
**Problem**: Service crashes with large entity sets
**Solution**:
- Implement pagination in graph queries
- Use lazy loading for relationship traversal
- Consider graph partitioning strategies
- Monitor memory usage and set limits

### Debug Mode
```bash
# Run with debug logging
LOG_LEVEL=DEBUG python src/main.py

# Enable LLM prompt logging
DEBUG_PROMPTS=true python src/main.py

# Log all entity extractions
DEBUG_ENTITIES=true python src/main.py
```

### Graph Visualization
```bash
# Generate graph visualization (requires graphviz)
python scripts/visualize_graph.py --output graph.png

# Interactive graph explorer
python scripts/graph_explorer.py --port 8080
```

## Architecture Notes

### Design Patterns
- **Repository Pattern**: Abstract graph database operations
- **Strategy Pattern**: Pluggable entity extraction strategies
- **Chain of Responsibility**: Multi-stage entity resolution pipeline
- **Observer Pattern**: Real-time graph update notifications

### AI/ML Components
- **Entity Extraction**: GPT-4 with few-shot prompting
- **Entity Resolution**: Embedding similarity + rule-based matching
- **Relationship Discovery**: Pattern mining + LLM inference
- **Context Building**: RAG with vector similarity search

### Performance Optimizations
- Embedding cache for frequent entities
- Batch processing for LLM calls
- Incremental graph updates
- Query result caching with TTL

### Data Quality Measures
- Confidence scoring for all extractions
- Human-in-the-loop validation hooks
- Automated consistency checks
- Periodic graph cleanup jobs

## Getting Started Guide

### Week 1: Research & Planning (No Coding!)
1. **Complexity Assessment**: This is the most complex module - focus on realistic scope
2. **Read Module Spec**: Study the detailed module specification thoroughly
3. **Technology Research**: Evaluate AI services, graph databases, and entity extraction tools
4. **Scope Planning**: Create a tiered implementation plan to manage complexity
5. **Submit Research Brief**: Complete and submit your analysis by Friday 5PM

### Week 2: Architecture & Environment Setup
```bash
# Navigate to module directory
cd modules/module-2-knowledge-graph

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (based on your research recommendations)
pip install -r requirements.txt

# Set up development environment
python scripts/setup_dev_environment.py

# Initialize knowledge base (will be implemented in Week 3)
python src/initialize_kb.py
```

### Week 3+: Implementation Path
- **Tier 1 (Weeks 3-6)**: Autonomous research foundation with basic knowledge graph
- **Tier 2 (Weeks 7-9)**: Advanced reasoning and user intelligence features
- **Week 10**: Demo preparation with knowledge discovery showcase

### ⚠️ Complexity Management Strategies
1. **Start Small**: Build simple entity extraction before autonomous research
2. **Mock AI First**: Use simulated responses to build interfaces before expensive API calls
3. **Test Incremental**: Validate each component before building complex interactions
4. **Monitor Costs**: Track AI API usage carefully to stay within budget
5. **Plan Fallbacks**: Always have a simpler manual approach ready

## Module Development Tips

1. **Start with Schema**: Define your entity types and relationships first
2. **Mock LLM Responses**: Develop with mock data before using expensive API calls
3. **Test Entity Resolution**: This is the hardest part - test thoroughly
4. **Monitor API Costs**: Track OpenAI usage and optimize prompts
5. **Visualize Often**: Use graph visualization to understand your data
6. **Autonomous Intelligence**: Build the system to learn and improve its research priorities
7. **WordPress Plugin Philosophy**: Maintain module independence while enabling knowledge sharing

## Next Steps for Enhancement

- Implement custom NER models for domain-specific entities
- Add temporal relationship tracking (entity history)
- Build automated knowledge validation pipelines
- Create entity embedding space for similarity search
- Implement federated graph queries across domains