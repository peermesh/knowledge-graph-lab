# AI-Publishing Module Integration: News Report Pipeline

## Overview

The AI module generates standalone news reports that are stored with individual URLs. The Publishing module independently queries these reports to assemble custom email digests for subscribers. This separation ensures clean concerns between content generation and distribution.

## Key Responsibilities

### AI Module Generates
1. **Standalone News Reports**: Complete articles with headlines, leads, and body content
2. **Prompt-Driven Writing**: Uses configurable prompts for different news styles
3. **Metadata & Tags**: Topics, entities, priority levels for categorization
4. **Unique URLs**: Each report has its own accessible URL endpoint

### Backend Stores
1. **Report Storage**: Persists all generated reports with metadata
2. **Query Interface**: Provides API for retrieving reports by various filters
3. **URL Management**: Maintains report URLs and routing

### Publishing Module Handles
1. **Report Selection**: Queries and selects relevant reports for each subscriber
2. **Email Assembly**: Combines multiple reports into digest format
3. **Personalization**: Matches reports to subscriber preferences
4. **Distribution**: Sends assembled emails via SendGrid/AWS SES
5. **Scheduling**: Manages when to send digests and alerts
6. **Analytics**: Tracks engagement with report links

## Data Flow

```
Raw Data → AI Module → News Reports → Backend Storage (with URLs)
                ↓                           ↓
        Entity Extraction            Publishing Queries
        Synthesis & Writing          Reports by Criteria
        Prompt-Based Generation              ↓
                                     Email Assembly
                                            ↓
                                      Subscribers
```

## News Report Structure (AI Generated, Backend Stored)

```json
{
  "report_id": "uuid-123",
  "url": "/reports/2025-09-22/openai-historic-funding-round",
  "generated_at": "2025-09-22T10:00:00Z",
  "report_type": "breaking_news",

  "headline": "OpenAI Raises $10B in Historic Funding Round",

  "lead": "In a landmark deal that reshapes the artificial intelligence landscape, OpenAI has secured $10 billion in funding at a $150 billion valuation, marking the largest AI investment in history.",

  "body": [
    {
      "type": "paragraph",
      "content": "The funding round, led by Microsoft with participation from..."
    },
    {
      "type": "quote",
      "content": "This represents a fundamental shift in how the market values AI companies",
      "attribution": "Jane Smith, Venture Capital Partner"
    },
    {
      "type": "paragraph",
      "content": "Industry analysts suggest this valuation signals..."
    }
  ],

  "metadata": {
    "entities": [
      {"name": "OpenAI", "type": "organization"},
      {"name": "Microsoft", "type": "organization"},
      {"name": "Sam Altman", "type": "person"}
    ],
    "topics": ["AI", "venture_capital", "technology", "funding"],
    "priority": "breaking",
    "relevance_scores": {
      "ai_industry": 0.98,
      "venture_capital": 0.95,
      "technology": 0.89
    }
  },

  "source_documents": ["doc_id_1", "doc_id_2", "doc_id_3"]
}
```

## Publishing Module Email Assembly

```json
// Publishing queries Backend for available reports
GET /api/reports?date=2025-09-22&min_relevance=0.7

// Publishing assembles email from selected reports
{
  "email_id": "digest-456",
  "subscriber_id": "user-123",
  "subject": "Your Daily Tech Digest - 3 Breaking Stories",
  "sections": [
    {
      "type": "headline_summary",
      "report_id": "uuid-123",
      "include": "headline + lead + link"
    },
    {
      "type": "full_excerpt",
      "report_id": "uuid-456",
      "include": "headline + 2_paragraphs + link"
    }
  ]
}
```

## Separation of Concerns

### AI Module
- Generates complete, standalone news reports
- Uses prompts to write in journalistic style
- Has no knowledge of subscribers or emails
- Each report is self-contained with its own URL

### Backend
- Stores all reports with metadata
- Provides query interface for report retrieval
- Manages report URLs and access

### Publishing Module
- Queries reports based on subscriber preferences
- Decides which reports to include in emails
- Formats report excerpts for email presentation
- Handles all subscriber personalization

## Integration Points

### Report Generation & Storage
```
// AI Module generates report
POST /api/reports
{
  "report": {news_report_object}
}

// Backend stores and returns
{
  "id": "uuid-123",
  "url": "/reports/2025-09-22/openai-funding",
  "status": "published"
}
```

### Publishing Module Queries
```
// Get today's reports for digest
GET /api/reports?date=today&type=breaking

// Get reports by topic for subscriber
GET /api/reports?topics=AI,funding&min_relevance=0.8

// Get specific report for inclusion
GET /api/reports/uuid-123
```

## Quality Assurance

### AI Module Ensures
- Minimum confidence threshold (70%) for included content
- Proper tagging coverage (all content tagged)
- Relevance score calculation for all active subscribers
- Report validation before handoff

### Publishing Module Validates
- Report structure compliance
- Subscriber eligibility
- Delivery constraints (rate limits, preferences)
- Template compatibility

## Performance Requirements

### AI Module
- Generate daily report within 10 minutes
- Process 1000 subscriber profiles for relevance scoring
- Support 10 concurrent report generations

### Publishing Module
- Send 10,000 emails within 30 minutes
- Process relevance scores in <100ms per subscriber
- Handle report updates without resending

## Error Handling

### Failed Report Generation
- AI Module retries with fallback models
- Sends partial report if minimum content available
- Notifies Publishing Module of degraded quality

### Personalization Failures
- Default to base report without personalization
- Log subscriber scoring failures for investigation
- Continue with available scored subscribers

## Future Enhancements

### Phase 4
- Real-time report updates
- Interactive content elements
- A/B testing of synthesis approaches

### Phase 5
- Machine learning on engagement data
- Automated report optimization
- Cross-channel content adaptation

## Configuration

### AI Module Settings
```yaml
report_generation:
  synthesis_model: "gpt-4"
  min_confidence: 0.7
  max_sections: 10
  personalization:
    enabled: true
    min_relevance_score: 0.5
```

### Publishing Module Settings
```yaml
report_distribution:
  relevance_threshold: 0.6
  max_recipients_per_batch: 100
  personalization:
    use_ai_scores: true
    combine_with_history: true
```

## Monitoring

### Key Metrics
- Report generation time
- Personalization score distribution
- Tag coverage percentage
- Subscriber relevance match rate
- Content engagement by relevance score

### Alerts
- Report generation failures
- Low relevance scores across all subscribers
- Missing tags or categories
- Integration timeout errors

## Documentation References
- [AI Module Specification](../../modules/ai-development/AI-Development-Spec.md)
- [Publishing Module Specification](../../modules/publishing-tools/Publishing-Tools-Spec.md)
- [System Integration Charter](integration-charter.md)
