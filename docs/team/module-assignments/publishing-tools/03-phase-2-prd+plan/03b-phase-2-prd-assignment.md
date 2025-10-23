# Publishing Tools - Phase 2 Assignment

## Your Mission

Create a comprehensive PRD that specifies exactly how to build a newsletter publishing system. Your PRD must include complete technical specifications, API contracts, database schemas, and implementation details that enable direct Phase 3 development.

---

## Before You Start

Prerequisites:

- [ ] Read the overview document (`03a-phase-2-prd-overview.md`)
- [ ] Review your Phase 1 research on email services and template engines
- [ ] Understand the corrected architecture: AI creates articles → Backend stores → You query and assemble

---

## Task 1: Define Backend Integration Contracts

**Objective**: Specify exact API contracts for querying articles from Backend.

### Backend Coordination Meeting
Schedule a working session with the Backend module owner to define:

**Article Query Requirements:**

- Endpoint specifications with complete request/response schemas
- Filter parameters you need (date, topics, quality, article type)
- Sorting options (recency, quality score, relevance)
- Pagination strategy for large result sets
- Performance requirements (<200ms response time)

**Required Article Data Fields:**

Document exactly what data you need for newsletter assembly:
```json
{
  "id": "uuid",
  "headline": "string (5-80 chars)",
  "summary": "string (50-200 chars)",
  "url": "/reports/2025-09-22/article-slug",
  "topics": ["technology", "business"],
  "article_type": "breaking_news|analysis|feature|roundup",
  "quality_score": "float (0.0-1.0)",
  "generated_at": "ISO timestamp",
  "entities": {
    "people": ["Elon Musk"],
    "companies": ["Tesla", "SpaceX"],
    "places": ["Austin", "Texas"]
  }
}
```

**API Specification Example:**
```http
GET /api/v1/reports?date_from=2025-09-22&topics=technology,business&min_quality=0.8&sort=-generated_at&page=1&page_size=20

Authorization: Bearer {service_token}
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

## Task 2: Design Newsletter Data Models

**Objective**: Define complete database schemas for your publishing system.

### Core Entities

**Subscribers Table:**
```sql
CREATE TABLE subscribers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    confirmed BOOLEAN DEFAULT false,
    topic_preferences TEXT[] DEFAULT '{}',
    frequency VARCHAR(20) DEFAULT 'weekly' CHECK (frequency IN ('daily', 'weekly', 'breaking')),
    subscribed_at TIMESTAMP DEFAULT NOW(),
    confirmed_at TIMESTAMP,
    last_sent_at TIMESTAMP,
    unsubscribed_at TIMESTAMP,
    bounce_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_subscribers_email ON subscribers(email);
CREATE INDEX idx_subscribers_confirmed ON subscribers(confirmed) WHERE confirmed = true;
CREATE INDEX idx_subscribers_frequency ON subscribers(frequency, confirmed);
```

**Newsletter Templates Table:**
```sql
CREATE TABLE newsletter_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    template_type VARCHAR(20) NOT NULL CHECK (template_type IN ('daily_digest', 'weekly_roundup', 'breaking_news')),
    subject_template VARCHAR(200) NOT NULL,
    html_template TEXT NOT NULL,
    text_template TEXT NOT NULL,
    max_articles INTEGER DEFAULT 10,
    section_config JSONB DEFAULT '{}',
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Newsletter Deliveries Table:**
```sql
CREATE TABLE newsletter_deliveries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID REFERENCES newsletter_templates(id),
    subject_line VARCHAR(200) NOT NULL,
    article_ids UUID[] NOT NULL,
    recipient_count INTEGER NOT NULL,
    sent_at TIMESTAMP DEFAULT NOW(),
    delivery_stats JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Deliverable**: Complete database schema with indexes and constraints.

---

## Task 3: Design Article Selection Algorithm

**Objective**: Specify how to intelligently select articles for newsletters.

### Selection Criteria

**Ranking Algorithm:**

Define a scoring system for article selection:
```python
def calculate_article_score(article, subscriber_preferences, current_time):
    """
    Calculate relevance score for article selection
    Returns float 0.0-1.0
    """
    score = 0.0

    # Quality score weight (40%)
    score += article.quality_score * 0.4

    # Recency weight (30%)
    hours_old = (current_time - article.generated_at).total_seconds() / 3600
    recency_score = max(0, (24 - hours_old) / 24)  # Linear decay over 24 hours
    score += recency_score * 0.3

    # Topic preference weight (30%)
    preference_match = len(set(article.topics) & set(subscriber_preferences)) / len(article.topics)
    score += preference_match * 0.3

    return min(score, 1.0)
```

**Selection Rules by Newsletter Type:**

**Daily Digest:**

- Query articles from last 24 hours
- Minimum quality score: 0.7
- Maximum 8 articles
- At least 1 breaking news if available
- Balance across topic categories

**Weekly Roundup:**

- Query articles from last 7 days
- Minimum quality score: 0.8
- Maximum 15 articles
- Prefer analysis and feature articles
- Include top performers by engagement

**Breaking News Alert:**

- Query articles from last 2 hours
- Only breaking_news type
- Minimum quality score: 0.9
- Maximum 3 articles
- Immediate delivery trigger

**Deliverable**: Complete selection algorithm specification with pseudo-code.

---

## Task 4: Design Template Engine

**Objective**: Specify newsletter template system with variable substitution.

### Template Structure

**HTML Template Example:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{newsletter_title}}</title>
    <style>
        /* Responsive email styles */
        @media screen and (max-width: 600px) {
            .container { width: 100% !important; }
        }
        .article { margin-bottom: 20px; border-bottom: 1px solid #eee; }
        .breaking { background-color: #fff3cd; padding: 10px; }
    </style>
</head>
<body>
    <div class="container" style="max-width: 600px; margin: 0 auto;">
        <header>
            <h1>{{newsletter_title}}</h1>
            <p style="color: #666;">{{formatted_date}}</p>
        </header>

        {{#breaking_section}}
        <section class="breaking">
            <h2>🚨 Breaking News</h2>
            {{#breaking_articles}}
            <div class="article">
                <h3><a href="{{full_url}}" style="color: #d73502;">{{headline}}</a></h3>
                <p>{{summary}}</p>
                <p style="font-size: 12px; color: #999;">
                    {{topics_display}} • {{time_ago}}
                </p>
            </div>
            {{/breaking_articles}}
        </section>
        {{/breaking_section}}

        <section class="main-content">
            <h2>Today's Top Stories</h2>
            {{#main_articles}}
            <div class="article">
                <h3><a href="{{full_url}}" style="color: #0066cc;">{{headline}}</a></h3>
                <p>{{summary}}</p>
                <p style="font-size: 12px; color: #999;">
                    {{topics_display}} • {{article_type_display}} • {{time_ago}}
                </p>
            </div>
            {{/main_articles}}
        </section>

        <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #999;">
                This email was sent to {{subscriber_email}}.<br>
                <a href="{{unsubscribe_url}}">Unsubscribe</a> |
                <a href="{{preferences_url}}">Manage Preferences</a>
            </p>
        </footer>
    </div>
</body>
</html>
```

**Template Variables:**

Document all available template variables:
```python
template_context = {
    "newsletter_title": "Tech Daily Digest",
    "formatted_date": "September 22, 2025",
    "subscriber_email": "user@example.com",
    "unsubscribe_url": "https://site.com/unsubscribe?token=...",
    "preferences_url": "https://site.com/preferences?token=...",
    "breaking_section": {
        "visible": True,
        "breaking_articles": [...]
    },
    "main_articles": [
        {
            "headline": "Article title",
            "summary": "Article summary",
            "full_url": "https://site.com/reports/2025-09-22/article-slug",
            "topics_display": "Technology, Business",
            "article_type_display": "Breaking News",
            "time_ago": "2 hours ago"
        }
    ]
}
```

**Deliverable**: Complete template specifications with examples.

---

## Task 5: Design Email Delivery System

**Objective**: Specify reliable email delivery with tracking and error handling.

### Email Service Integration

**SendGrid API Integration:**
```python
class EmailDeliveryService:
    def __init__(self, api_key: str):
        self.client = sendgrid.SendGridAPIClient(api_key=api_key)

    def send_newsletter(self, newsletter: Newsletter, recipients: List[Subscriber]) -> DeliveryResult:
        """
        Send newsletter to recipient list with tracking
        """
        # Batch recipients into groups of 1000
        for batch in self.batch_recipients(recipients, 1000):
            try:
                response = self.client.mail.send.post(request_body={
                    "personalizations": self.build_personalizations(batch),
                    "from": {"email": "newsletter@yoursite.com", "name": "Your Newsletter"},
                    "subject": newsletter.subject_line,
                    "content": [
                        {"type": "text/html", "value": newsletter.html_content},
                        {"type": "text/plain", "value": newsletter.text_content}
                    ],
                    "tracking_settings": {
                        "click_tracking": {"enable": True},
                        "open_tracking": {"enable": True}
                    }
                })
                self.log_delivery_attempt(newsletter.id, batch, response)
            except Exception as e:
                self.handle_delivery_error(newsletter.id, batch, e)
```

**Error Handling Strategy:**

- Temporary failures: Retry with exponential backoff (max 3 attempts)
- Permanent failures: Mark subscriber as bounced, require reconfirmation
- Rate limiting: Implement queue with throttling
- Bounce handling: Process webhook notifications from email service

**Analytics Tracking:**
```python
class DeliveryAnalytics:
    def track_open(self, newsletter_id: UUID, subscriber_id: UUID, timestamp: datetime):
        """Record email open event"""

    def track_click(self, newsletter_id: UUID, subscriber_id: UUID, url: str, timestamp: datetime):
        """Record link click event"""

    def track_bounce(self, newsletter_id: UUID, subscriber_id: UUID, bounce_type: str):
        """Record bounce event (hard/soft)"""

    def track_unsubscribe(self, subscriber_id: UUID, newsletter_id: UUID, timestamp: datetime):
        """Record unsubscribe event"""
```

**Deliverable**: Complete email delivery system specification.

---

## Task 6: Design Subscriber Management

**Objective**: Specify complete subscriber lifecycle management.

### Subscription Flow

**Double Opt-in Process:**

1. User submits email and preferences
2. System sends confirmation email with unique token
3. User clicks confirmation link
4. System activates subscription
5. System sends welcome email with first newsletter

**API Endpoints:**
```python
# Subscription endpoints
POST /api/v1/subscribe
{
    "email": "user@example.com",
    "topic_preferences": ["technology", "business"],
    "frequency": "daily"
}

GET /api/v1/confirm/{token}
# Activates subscription

POST /api/v1/unsubscribe
{
    "email": "user@example.com",
    "token": "unsubscribe_token"
}

PUT /api/v1/preferences/{token}
{
    "topic_preferences": ["technology"],
    "frequency": "weekly"
}
```

**Preference Management:**

- Topic-based segmentation
- Frequency preferences (daily/weekly/breaking only)
- Unsubscribe categories (all vs specific types)
- Re-engagement campaigns for inactive subscribers

**Deliverable**: Complete subscriber management specification.

---

## Task 7: Write Complete PRD

**Objective**: Assemble all specifications into a comprehensive PRD.

### PRD Structure

**Section 1: System Overview (1-2 pages)**

- Publishing module purpose and scope
- Architecture overview with module interactions
- Success metrics and performance requirements

**Section 2: Functional Requirements (3-4 pages)**

- Feature 1: Article Query & Selection
- Feature 2: Newsletter Assembly
- Feature 3: Template Management
- Feature 4: Subscriber Management
- Feature 5: Email Delivery & Tracking

**Section 3: Technical Specifications (4-5 pages)**

- Database schemas with complete DDL
- API specifications with request/response examples
- Integration contracts with Backend module
- Email service provider integration

**Section 4: Newsletter Templates (2-3 pages)**

- Template engine specification
- HTML/text template examples
- Variable substitution system
- Responsive design requirements

**Section 5: Operational Requirements (2-3 pages)**

- Delivery performance requirements
- Error handling and retry logic
- Monitoring and alerting specifications
- Privacy compliance (GDPR, CAN-SPAM)

**Section 6: Testing & Quality Assurance (1-2 pages)**

- Unit testing requirements for selection algorithms
- Integration testing with Backend APIs
- Email delivery testing procedures
- Template rendering validation

---

## Quality Standards

### PRD Quality Standards

Use the [SpecKit templates](../../../../speckit/README.md) to create your comprehensive PRD. Your PRD must include:

- [ ] **Complete Data Types**: All fields specify exact types (VARCHAR(255), JSONB, etc.)
- [ ] **API Schemas**: Full request/response examples with status codes
- [ ] **Error Handling**: Specific error scenarios with handling procedures
- [ ] **Performance Metrics**: Quantifiable requirements (<200ms, 99.9% uptime)
- [ ] **Integration Contracts**: Exact specifications for Backend communication

### Implementation Readiness

- [ ] **Database Migration Scripts**: Ready-to-run DDL statements
- [ ] **Configuration Examples**: Complete environment variable specifications
- [ ] **Algorithm Pseudo-code**: Detailed logic for article selection
- [ ] **Template Examples**: Working HTML/text email templates
- [ ] **Monitoring Specifications**: Metrics and alerting requirements

---

## Submission Requirements

### Deliverables Structure
```
deliverables/
├── PRD.md                              # Main specification document
├── api-contracts/
│   ├── backend-integration.yaml       # OpenAPI spec for Backend queries
│   └── email-service-integration.yaml # SendGrid/SES integration spec
├── database/
│   ├── schema.sql                      # Complete database DDL
│   └── sample-data.sql                 # Test data for development
├── templates/
│   ├── daily-digest.html              # Daily newsletter template
│   ├── weekly-roundup.html            # Weekly newsletter template
│   └── breaking-news.html             # Breaking news template
└── algorithms/
    ├── article-selection.py           # Selection algorithm specification
    └── personalization.py             # Personalization logic
```

### Quality Checklist

Before submission:

- [ ] All backend integration points documented with examples
- [ ] Complete database schema with proper indexes and constraints
- [ ] Email templates tested with sample data
- [ ] Article selection algorithm has quantifiable criteria
- [ ] Error handling covers all failure scenarios
- [ ] Performance requirements are measurable
- [ ] Privacy compliance measures specified

---

## Timeline

**Week 1:**

- Days 1-2: Backend coordination and API contract definition
- Days 3-4: Database schema design and article selection algorithms
- Day 5: Email template design and delivery system specification

**Week 2:**

- Days 1-3: Complete PRD writing and technical specifications
- Day 4: Internal review and testing with mock data
- Day 5: Final refinements and submission

---

## Success Criteria

Your PRD enables Phase 3 developers to:

- Implement the complete publishing system from specifications
- Integrate seamlessly with Backend APIs using provided contracts
- Deploy email delivery with proper error handling and monitoring
- Create newsletters that provide genuine value to subscribers

**Remember**: Your specifications must be complete enough for implementation without requiring additional design decisions.
