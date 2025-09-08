# Mock Data Directory

## Overview
This directory contains mock data and API response examples for testing and development of the Knowledge Graph Lab modules. Use this data to develop and test without requiring external API connections or complete module integration.

## Directory Structure

```
mock-data/
├── api-responses/          # Mock API responses for each module
│   ├── module-1-ingestion.json
│   ├── module-2-knowledge-graph.json
│   ├── module-3-reasoning.json
│   └── module-4-frontend.json
├── content/                # Sample content for ingestion
│   ├── articles/
│   ├── rss-feeds/
│   └── scraped-pages/
├── entities/              # Sample entity data
│   ├── platforms/
│   ├── organizations/
│   ├── people/
│   ├── grants/
│   └── sample_entities.json
├── relationships/         # Sample relationship data
│   ├── platform-connections/
│   └── entity-relationships/
└── users/                # Sample user profiles and preferences
    ├── profiles/
    └── preferences/
```

## Usage Instructions

### For Development

#### 1. Running Modules with Mock Data
Each module can be started in mock mode to use this data instead of real services:

```bash
# Module 1: Ingestion
cd modules/module-1-ingestion
python src/main.py --use-mock-data

# Module 2: Knowledge Graph
cd modules/module-2-knowledge-graph
python src/main.py --use-mock-data

# Module 3: Reasoning
cd modules/module-3-reasoning
python src/main.py --use-mock-data

# Module 4: Frontend
cd modules/module-4-frontend
npm run dev:mock
```

#### 2. Loading Mock Data in Code
```python
import json
from pathlib import Path

# Load mock API response
mock_data_path = Path(__file__).parent.parent.parent / "mock-data"
with open(mock_data_path / "api-responses/module-1-ingestion.json") as f:
    mock_responses = json.load(f)

# Use specific mock response
ingestion_response = mock_responses["ingest_single_url"]["response_success"]
```

#### 3. Frontend Development with Mock APIs
```javascript
// In development, use mock data
const useMockData = process.env.NEXT_PUBLIC_USE_MOCK === 'true';

const fetchEntities = async () => {
  if (useMockData) {
    // Load from mock-data/api-responses/module-2-knowledge-graph.json
    const mockData = await import('@/mock-data/api-responses/module-2-knowledge-graph.json');
    return mockData.graph_entities.response;
  }
  
  // Real API call
  return fetch(`${KNOWLEDGE_API}/api/graph/entities`).then(r => r.json());
};
```

### For Testing

#### Unit Tests with Mock Data
```python
import pytest
from unittest.mock import patch

@patch('src.services.ingestion_service.fetch_url')
def test_ingestion_with_mock(mock_fetch):
    # Load mock response
    with open('mock-data/api-responses/module-1-ingestion.json') as f:
        mock_data = json.load(f)
    
    mock_fetch.return_value = mock_data['ingest_single_url']['response_success']
    
    # Test your service
    result = ingest_url('https://example.com')
    assert result['status'] == 'processing'
```

#### Integration Tests
```python
# Use mock data for predictable integration tests
def test_full_pipeline():
    # Load mock content
    content = load_mock_file('content/articles/creator-economy-news.json')
    
    # Load expected entities
    entities = load_mock_file('entities/sample_entities.json')
    
    # Test the pipeline
    ingested = ingestion_service.process(content)
    extracted = knowledge_service.extract_entities(ingested)
    
    assert len(extracted) == len(entities)
```

## API Response Examples

### Module 1: Ingestion
Located in `api-responses/module-1-ingestion.json`

Key endpoints mocked:
- `GET /health` - Service health check
- `POST /api/ingest/url` - Single URL ingestion
- `POST /api/ingest/bulk` - Bulk URL ingestion
- `GET /api/ingest/status/{job_id}` - Job status checking
- `GET /api/sources` - List data sources
- `GET /api/content` - Query ingested content

### Module 2: Knowledge Graph
Located in `api-responses/module-2-knowledge-graph.json`

Key endpoints mocked:
- `POST /api/entities/extract` - Entity extraction from text
- `POST /api/entities/resolve` - Entity resolution/deduplication
- `GET /api/knowledge/query` - Query knowledge graph
- `POST /api/knowledge/search` - Search for entities
- `GET /api/research/context/{topic}` - Get research context

### Module 3: Reasoning
Located in `api-responses/module-3-reasoning.json`

Key endpoints mocked:
- `GET /api/frontier/next` - Get next research priorities
- `POST /api/topics/cluster` - Cluster content into topics
- `GET /api/topics/trending` - Get trending topics
- `POST /api/digest/generate` - Generate user digest
- `POST /api/newsletter/create` - Create newsletter content

### Module 4: Frontend
Located in `api-responses/module-4-frontend.json`

Key endpoints mocked:
- `POST /api/auth/login` - User authentication
- `GET /api/users/profile` - User profile data
- `GET /api/graph/entities` - List entities for visualization
- `GET /api/digests` - User's digest history
- `GET /api/research/dashboard` - Dashboard metrics

## Sample Data

### Entities
The `entities/sample_entities.json` file contains 50+ sample entities including:
- **Platforms**: Patreon, Substack, YouTube, TikTok, etc.
- **Organizations**: Venture funds, accelerators, advocacy groups
- **People**: Founders, CEOs, notable creators
- **Grants**: Creator funds, government grants, platform funds
- **Policies**: Legislative items, platform policies

### Relationships
Sample relationships between entities:
- FOUNDED_BY
- COMPETES_WITH
- PARTNERS_WITH
- INVESTS_IN
- OPERATES
- INTEGRATES_WITH

### Content
Sample articles and content for ingestion testing:
- Tech news articles about creator economy
- Platform announcements
- Grant opportunities
- Policy updates
- Creator success stories

## Updating Mock Data

### Guidelines for Adding Mock Data

1. **Keep it realistic**: Use actual data structures from your APIs
2. **Cover edge cases**: Include error responses and edge conditions
3. **Maintain consistency**: Entity IDs should match across files
4. **Document changes**: Update this README when adding new mock data
5. **Version control**: Commit mock data changes with feature changes

### Mock Data Generator Script
```bash
# Generate new mock entities
python scripts/generate_mock_data.py --type entities --count 10

# Generate mock content
python scripts/generate_mock_data.py --type content --category news

# Generate mock API responses from OpenAPI spec
python scripts/generate_from_openapi.py --spec api/openapi.yaml
```

## Best Practices

1. **Isolation**: Each test should use its own copy of mock data
2. **Immutability**: Don't modify mock files during tests
3. **Completeness**: Include all required fields in mock responses
4. **Realism**: Use realistic values (dates, amounts, etc.)
5. **Organization**: Group related mock data together
6. **Documentation**: Comment complex mock structures

## Troubleshooting

### Mock Data Not Loading
- Check file paths are correct
- Verify JSON is valid (use jsonlint)
- Ensure mock mode is enabled

### Inconsistent Test Results
- Mock data might have been modified
- Check for hardcoded dates that have expired
- Verify random seeds are set for reproducibility

### Missing Mock Endpoints
- Check `api-responses/` for the endpoint
- Add missing endpoint to appropriate JSON file
- Submit PR with new mock data

## Contributing Mock Data

When adding new features:
1. Create corresponding mock data
2. Add examples to `api-responses/`
3. Update this README
4. Include in tests
5. Submit with feature PR

## Mock Data Maintenance

Regular maintenance tasks:
- [ ] Weekly: Update dates in time-sensitive mocks
- [ ] Monthly: Review and update entity data
- [ ] Quarterly: Audit mock data completeness
- [ ] Per release: Sync mock data with API changes