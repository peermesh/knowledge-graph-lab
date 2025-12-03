# Knowledge Graph Lab - System Overview

## Executive Summary

**The Problem**: The creator economy operates like a city without a map. Millions of creators waste 10+ hours weekly searching for opportunities, grants, and partnerships across hundreds of fragmented information sources.

**Our Solution**: Knowledge Graph Lab is an AI-powered research platform that automatically discovers, understands, and delivers personalized insights about creator economy opportunities.

**Core Value**: Transform scattered information chaos into actionable intelligence, enabling creators to focus on creating while opportunities find them.

**Target Users**: Content creators, investors, researchers, platforms, and policymakers who need to navigate the complex creator economy landscape.

**MVP Outcome**: A system that monitors RSS feeds and websites, extracts entities and relationships using AI, builds a knowledge graph of opportunities, and delivers personalized email notifications to users based on their preferences.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           KNOWLEDGE GRAPH LAB SYSTEM                           │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CONTENT       │    │    BACKEND       │    │       AI        │    │   PUBLISHING    │
│   SOURCES       │    │  ARCHITECTURE    │    │  DEVELOPMENT    │    │     TOOLS       │
│                 │    │                  │    │                 │    │                 │
│ • RSS Feeds     │────│ • Data Ingestion │────│ • Entity Extract │────│ • Email Template│
│ • Website APIs  │    │ • PostgreSQL DB  │    │ • Relationship   │    │ • ESP Integration│
│ • Documents     │    │ • Vector Store   │    │   Mapping       │    │ • Personalization│
│ • Social Media  │    │ • REST APIs      │    │ • Knowledge      │    │ • Analytics     │
│                 │    │ • Authentication │    │   Graph Build   │    │ • Scheduling    │
└─────────────────┘    └─────────┬────────┘    └─────────┬───────┘    └─────────┬───────┘
                                 │                       │                      │
                       ┌─────────▼────────┐             │                      │
                       │    FRONTEND      │             │                      │
                       │     DESIGN       │◄────────────┘                      │
                       │                  │                                     │
                       │ • React Web UI   │◄────────────────────────────────────┘
                       │ • Graph Viz      │
                       │ • Search/Filter  │
                       │ • User Prefs     │
                       │ • Real-time      │
                       └──────────────────┘
                                 │
                       ┌─────────▼────────┐
                       │      USERS       │
                       │                  │
                       │ • Creators       │
                       │ • Investors      │
                       │ • Researchers    │
                       │ • Platforms      │
                       └──────────────────┘

Legend:
────► Data Flow
◄──── User Interface
```

**Key Data Stores**:
- **PostgreSQL**: Users, configurations, metadata, processed content
- **Vector Database (Qdrant)**: Document embeddings for semantic search
- **Redis**: Caching, session management, job queues
- **Knowledge Graph**: Entities, relationships, confidence scores

**External Integrations**:
- **Content Sources**: RSS feeds, website APIs, document uploads
- **AI Services**: OpenAI/Anthropic for entity extraction, embedding generation
- **Email Services**: SendGrid/Mailgun for newsletter delivery
- **Monitoring**: Logging, metrics, alerting systems

---

## Module Breakdown

### Backend Architecture Module

**Primary Purpose**: Provide the foundational infrastructure that enables all other modules to function reliably and securely.

**Key Responsibilities**:
- **Data Ingestion**: Monitor and collect content from RSS feeds, APIs, and document uploads
- **Database Management**: Store and retrieve structured data, user preferences, and processed content
- **API Development**: Provide REST endpoints for frontend and integration with other modules
- **Authentication**: Manage user accounts, JWT tokens, and role-based access control
- **Queue Management**: Handle asynchronous processing jobs for AI and publishing workflows

**Inputs**:
- Content from external sources (RSS feeds, website APIs, document uploads)
- API requests from frontend for data retrieval and user management
- Processed data from AI module (entities, relationships, confidence scores)
- Publishing status updates from publishing tools module

**Outputs**:
- Structured data via REST APIs for frontend consumption
- Raw content queued for AI processing
- User preference data for publishing personalization
- Authentication tokens and session management
- Real-time updates via WebSocket connections

**MVP Scope (Phase 3)**:
- REST API with CRUD operations for users, content, and entities
- JWT authentication system
- PostgreSQL database with core schemas
- Basic content ingestion from 5+ RSS feeds
- Docker containerization for local development

**Technology Stack**:
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for sessions and job queues
- **Authentication**: JWT with refresh tokens
- **Deployment**: Docker containers

**Integration Points**:
- **→ AI Module**: Provides raw content via job queues, receives structured entities/relationships
- **→ Frontend**: Provides REST APIs, WebSocket updates, authentication
- **→ Publishing**: Provides user preferences, content metadata, analytics data
- **← External Sources**: Ingests content via RSS, APIs, file uploads

### AI Development Module

**Primary Purpose**: Transform unstructured text into structured knowledge by extracting entities, mapping relationships, and building the knowledge graph.

**Key Responsibilities**:
- **Entity Extraction**: Identify organizations, people, funding amounts, dates, locations, grants, partnerships
- **Relationship Mapping**: Discover connections between entities (funding, partnerships, competition, collaboration)
- **Confidence Scoring**: Assign reliability scores based on source credibility and extraction certainty
- **Knowledge Graph Construction**: Build and maintain the graph database of entities and relationships
- **Semantic Search**: Generate embeddings and enable similarity-based content discovery

**Inputs**:
- Raw documents from backend (HTML, PDF, plain text) via processing queues
- Processing job requests with document IDs and metadata
- User feedback on entity accuracy for model improvement
- Vector database connection for embedding storage

**Outputs**:
- Structured JSON with extracted entities, relationships, and confidence scores
- Knowledge graph updates with new entities and relationship mappings
- Document embeddings for semantic search capabilities
- Processing status updates and error reports
- Insights and patterns discovered from relationship analysis

**MVP Scope (Phase 3)**:
- Extract 5 core entity types (organizations, people, amounts, dates, locations) with 80% accuracy
- Process 100 documents per hour
- Basic confidence scoring (high/medium/low)
- Integration with backend processing pipeline
- Target cost: $0.10 per document processed

**Technology Stack**:
- **LLM Integration**: OpenAI GPT-4 or Anthropic Claude
- **Vector Database**: Qdrant for embeddings
- **Framework**: LangChain or LlamaIndex for RAG pipeline
- **Processing**: Python with async processing
- **Knowledge Graph**: Neo4j or PostgreSQL with graph extensions

**Integration Points**:
- **← Backend**: Receives raw content via job queues, database connections
- **→ Backend**: Returns structured data, processing status updates
- **→ Frontend**: Provides entity/relationship data for visualization
- **→ Publishing**: Provides insights and content analysis for personalization

### Frontend Design Module

**Primary Purpose**: Provide an intuitive user interface that makes complex knowledge graph data accessible and actionable for end users.

**Key Responsibilities**:
- **Knowledge Graph Visualization**: Interactive display of entities, relationships, and connections
- **Search and Discovery**: Enable users to find relevant opportunities through text search and filtering
- **User Preference Management**: Interface for users to set interests, content types, and notification preferences
- **Real-time Updates**: Display live content processing and new opportunity notifications
- **Responsive Design**: Ensure usability across desktop, tablet, and mobile devices

**Inputs**:
- Entity and relationship data from backend APIs
- User authentication tokens and session data
- Real-time updates via WebSocket connections
- User interaction events (clicks, searches, preferences)
- Published content and analytics data

**Outputs**:
- User interface interactions and form submissions
- Search queries and filter parameters to backend
- User preference updates for personalization
- Analytics events for usage tracking
- Authentication requests and session management

**MVP Scope (Phase 3)**:
- Basic search interface for entities and opportunities
- Simple knowledge graph visualization (network diagram)
- User registration, login, and preference management
- Responsive design for desktop and mobile
- Real-time notifications for new opportunities

**Technology Stack**:
- **Framework**: React with TypeScript
- **State Management**: Redux Toolkit or Zustand
- **Visualization**: D3.js or React Flow for graph display
- **Styling**: Tailwind CSS or Material-UI
- **Real-time**: WebSocket client for live updates

**Integration Points**:
- **← Backend**: Consumes REST APIs, WebSocket updates, authentication
- **→ Backend**: Sends user interactions, preference updates, search queries
- **← AI**: Displays entity/relationship data and confidence scores
- **← Publishing**: Shows published content and analytics dashboards

### Publishing Tools Module

**Primary Purpose**: Deliver personalized insights and opportunities to users through email and other distribution channels.

**Key Responsibilities**:
- **Email Template Management**: Create and maintain responsive email templates for different content types
- **Personalization Engine**: Customize content based on user preferences, behavior, and profile data
- **Multi-channel Distribution**: Send content via email (MVP), with future support for social media and web
- **Analytics and Tracking**: Monitor email opens, clicks, and user engagement
- **Content Scheduling**: Automate delivery timing based on user preferences and optimal engagement windows

**Inputs**:
- User preference data and profiles from backend
- Processed insights and opportunities from AI module
- Content metadata and analytics from backend
- User engagement data (opens, clicks, unsubscribes)
- Scheduling triggers and automation rules

**Outputs**:
- Formatted email content sent via Email Service Provider (ESP)
- Engagement analytics and performance metrics
- User behavior data for backend storage
- Delivery status reports and error notifications
- Personalized content recommendations

**MVP Scope (Phase 3)**:
- Send templated emails via chosen ESP (SendGrid/Mailgun)
- Track email opens and clicks for basic analytics
- Store web-viewable copies of sent emails
- Basic personalization based on user interests
- Triggered sending via cron jobs or worker processes

**Technology Stack**:
- **Email Service**: SendGrid, Mailgun, or Amazon SES
- **Templates**: MJML for responsive email design
- **Processing**: Python/Node.js for content generation
- **Analytics**: Custom tracking with UTM parameters
- **Scheduling**: Celery or similar job queue system

**Integration Points**:
- **← Backend**: Receives user data, content metadata, scheduling triggers
- **← AI**: Receives insights, content analysis, personalization signals
- **→ Backend**: Returns engagement analytics, delivery status, user feedback
- **→ Users**: Delivers email content and manages subscriptions

---

## Integration Flow Diagrams

### Content Processing Flow
```
1. External Source → Backend Ingestion
   ├─ RSS Feed Monitor (every 30 minutes)
   ├─ API Polling (hourly)
   └─ Document Upload (user-triggered)

2. Backend → Content Storage
   ├─ Raw content in PostgreSQL
   ├─ Job queued in Redis
   └─ Metadata extracted

3. Backend → AI Processing Queue
   ├─ Document ID + metadata
   ├─ Processing priority
   └─ Retry configuration

4. AI Module → Entity Extraction
   ├─ Chunk document (1000-2000 tokens)
   ├─ Extract entities via LLM
   ├─ Map relationships
   └─ Assign confidence scores

5. AI Module → Knowledge Graph Update
   ├─ New entities added
   ├─ Relationships connected
   ├─ Confidence scores updated
   └─ Embeddings generated

6. AI Module → Backend Results
   ├─ Structured JSON data
   ├─ Processing status
   └─ Error reports

7. Backend → Frontend Notification
   ├─ WebSocket update
   ├─ New entity count
   └─ Processing completion
```

**Data Formats**:
- **Raw Content**: HTML, PDF, plain text with metadata
- **Entity JSON**: `{"id": "uuid", "name": "string", "type": "enum", "confidence": 0.85}`
- **Relationship JSON**: `{"from": "entity_id", "to": "entity_id", "type": "funds", "confidence": 0.72}`

**Performance Requirements**:
- Process 100 documents/hour
- Entity extraction: < 30 seconds per document
- Knowledge graph update: < 5 seconds per entity batch

### Publishing Flow
```
1. Scheduler → Content Selection
   ├─ Daily opportunity digest (8 AM user timezone)
   ├─ Breaking news alerts (real-time)
   └─ Weekly summary (Sunday 6 PM)

2. Publishing Module → User Matching
   ├─ Query user preferences
   ├─ Filter opportunities by interests
   ├─ Rank by relevance score
   └─ Apply engagement history

3. Publishing Module → Content Generation
   ├─ Select email template
   ├─ Populate with personalized data
   ├─ Generate subject line
   └─ Add tracking parameters

4. Publishing Module → ESP Delivery
   ├─ Send via SendGrid/Mailgun
   ├─ Track delivery status
   ├─ Handle bounces/complaints
   └─ Store web archive copy

5. User → Email Interaction
   ├─ Open tracking pixel
   ├─ Click link tracking
   ├─ Unsubscribe handling
   └─ Reply processing

6. Publishing Module → Analytics Update
   ├─ Engagement metrics to backend
   ├─ User behavior updates
   ├─ Content performance data
   └─ A/B test results
```

**Personalization Logic**:
- **User Profile**: Content type, audience size, location, goals
- **Behavior History**: Previous opens, clicks, engagement patterns
- **Relevance Score**: AI-generated match between opportunity and user
- **Timing Optimization**: Send when user historically engages most

### User Interaction Flow
```
1. User → Frontend Login
   ├─ Email/password authentication
   ├─ JWT token request
   └─ Session establishment

2. Frontend → Backend Authentication
   ├─ Validate credentials
   ├─ Generate JWT tokens
   ├─ Return user profile
   └─ Initialize session

3. User → Search Query
   ├─ Text search input
   ├─ Filter selections
   └─ Sort preferences

4. Frontend → Backend API
   ├─ GET /api/v1/search?q=grants&type=funding
   ├─ Authentication headers
   └─ Pagination parameters

5. Backend → AI Semantic Search
   ├─ Generate query embedding
   ├─ Vector similarity search
   ├─ Graph traversal for related entities
   └─ Confidence score filtering

6. Backend → Frontend Results
   ├─ Paginated entity list
   ├─ Relationship data
   ├─ Relevance scores
   └─ Total result count

7. Frontend → User Display
   ├─ Search results list
   ├─ Interactive graph visualization
   ├─ Filter controls
   └─ Pagination controls
```

**Real-time Features**:
- **WebSocket Updates**: New opportunities, processing status
- **Live Search**: As-you-type search suggestions
- **Graph Interaction**: Click to explore entity relationships
- **Notification Badges**: Unread opportunity count

---

## MVP Scope Definition

### MVP User Story
**"As a gaming content creator, I want to receive weekly email digests of relevant funding opportunities, grants, and partnership possibilities so that I can focus on creating content while staying informed about opportunities that match my audience size and content type."**

### Phase 3 Deliverables

**Backend Architecture MVP**:
- ✅ REST API with user authentication (JWT)
- ✅ PostgreSQL database with core schemas (users, content, entities)
- ✅ Content ingestion from 5+ RSS feeds (automated monitoring)
- ✅ Message queue for AI processing jobs
- ✅ Docker containerization for local development

**AI Development MVP**:
- ✅ Entity extraction for organizations, people, amounts, dates, locations
- ✅ Basic relationship mapping (funding, partnership, mention)
- ✅ Confidence scoring (high/medium/low categories)
- ✅ Processing pipeline handling 100 documents/hour
- ✅ Integration with backend job queue

**Frontend Design MVP**:
- ✅ User registration and authentication interface
- ✅ Basic search functionality for entities and opportunities
- ✅ Simple list view of search results with filtering
- ✅ User preference management (interests, notification settings)
- ✅ Responsive design for desktop and mobile

**Publishing Tools MVP**:
- ✅ Email template system using MJML
- ✅ Integration with ESP (SendGrid or Mailgun)
- ✅ Weekly digest generation and sending
- ✅ Basic analytics (open/click tracking)
- ✅ Web archive of sent emails

### Integration Requirements
- **Backend ↔ AI**: Job queue processing with status updates
- **Backend ↔ Frontend**: REST API with authentication
- **Backend ↔ Publishing**: User preference data and content metadata
- **AI → Publishing**: Entity/relationship data for content personalization

### Success Metrics
- **Technical**: System processes 500+ documents/week with 80% entity extraction accuracy
- **User**: 10+ users receive personalized weekly digests
- **Operational**: 99% uptime, < 2 second API response times
- **Content**: Knowledge graph contains 1000+ entities with mapped relationships

### Explicitly OUT of Scope (Phase 2+ Features)

**Content Sources**:
- ❌ Social media APIs (Twitter, LinkedIn, Instagram)
- ❌ Complex document parsing (academic papers, presentations)
- ❌ Real-time news feeds
- ❌ User-generated content submission

**AI Capabilities**:
- ❌ Advanced NLP (sentiment analysis, topic modeling)
- ❌ Predictive analytics and trend forecasting
- ❌ Multi-language support beyond English
- ❌ Custom model fine-tuning

**Publishing Features**:
- ❌ Social media posting and distribution
- ❌ Advanced email templates with dynamic content
- ❌ A/B testing for email optimization
- ❌ SMS or push notification delivery

**Frontend Features**:
- ❌ Advanced graph visualization (3D, interactive layouts)
- ❌ Collaborative features (sharing, commenting)
- ❌ Advanced analytics dashboards
- ❌ Mobile application (web-only for MVP)

**Infrastructure**:
- ❌ Production deployment and scaling
- ❌ Advanced monitoring and alerting
- ❌ Multi-tenant architecture
- ❌ Geographic content distribution

---

## Technology Stack Overview

### Backend Infrastructure
- **API Framework**: FastAPI (Python) - async support, automatic documentation
- **Database**: PostgreSQL - ACID compliance, JSON support, full-text search
- **Caching**: Redis - session storage, job queues, rate limiting
- **Authentication**: JWT with refresh tokens, role-based access control
- **Queue System**: Celery with Redis broker for async processing

### Frontend Application
- **Framework**: React 18 with TypeScript - component reusability, type safety
- **State Management**: Redux Toolkit - predictable state updates, dev tools
- **Styling**: Tailwind CSS - utility-first, responsive design
- **Visualization**: D3.js - flexible data visualization, graph layouts
- **Build Tool**: Vite - fast development, optimized builds

### AI/ML Pipeline
- **LLM Integration**: OpenAI GPT-4 or Anthropic Claude - entity extraction, relationship mapping
- **Vector Database**: Qdrant - semantic search, embedding storage
- **RAG Framework**: LangChain - document processing, prompt management
- **Embedding Models**: OpenAI text-embedding-ada-002 - semantic similarity
- **Knowledge Graph**: Neo4j or PostgreSQL with graph extensions

### Publishing Infrastructure
- **Email Service**: SendGrid or Mailgun - deliverability, analytics
- **Template Engine**: MJML - responsive email design
- **Content Processing**: Python/Node.js - personalization logic
- **Analytics**: Custom tracking with UTM parameters
- **Scheduling**: Cron jobs or Celery beat for automated sending

### Development & Deployment
- **Containerization**: Docker and Docker Compose - consistent environments
- **Version Control**: Git with GitHub - collaboration, CI/CD
- **Testing**: pytest (Python), Jest (JavaScript) - unit and integration tests
- **Documentation**: OpenAPI/Swagger - API documentation
- **Monitoring**: Structured logging, health checks, metrics collection

### Infrastructure Rationale
- **Python Backend**: Excellent AI/ML ecosystem, async support, rapid development
- **React Frontend**: Large ecosystem, excellent developer experience, component reusability
- **PostgreSQL**: Mature, reliable, supports both relational and graph data
- **Redis**: Fast caching and job queues, simple deployment
- **Docker**: Consistent development and deployment environments

---

## Development Phases

### Phase 1: Research & Discovery (Weeks 1-2)
**Status**: Current phase
**Focus**: Technology evaluation and architectural decisions

**Module Activities**:
- **Backend**: Evaluate FastAPI vs Flask, PostgreSQL schemas, Docker setup
- **Frontend**: Compare React frameworks, visualization libraries, state management
- **AI**: Research LLM providers, vector databases, RAG frameworks
- **Publishing**: Evaluate ESPs, email template systems, analytics tools

**Deliverables**: Research briefs with technology recommendations, cost analysis, integration plans

### Phase 2: Planning & Design (Weeks 3-4)
**Focus**: Detailed specifications and API design
**Integration Requirements**: Cross-module API contracts, data format agreements

**Module Activities**:
- **Backend**: Complete API specification, database schema design, authentication flow
- **Frontend**: Component architecture, page layouts, state management design
- **AI**: Processing pipeline design, entity schemas, confidence scoring system
- **Publishing**: Template design, personalization logic, analytics specification

**Deliverables**: Product Requirements Documents (PRDs) ready for implementation (created using [SpecKit templates](../../speckit/README.md))

### Phase 3: MVP Development (Weeks 5-8)
**Focus**: Independent module development with basic integration
**Integration Milestones**: Week 6 (API contracts), Week 7 (data flow), Week 8 (end-to-end testing)

**Module Activities**:
- **Backend**: Core API implementation, database setup, basic ingestion
- **Frontend**: User interface implementation, API integration, basic visualization
- **AI**: Entity extraction pipeline, knowledge graph construction, backend integration
- **Publishing**: Email system implementation, template engine, ESP integration

**Success Criteria**: Each module works independently, basic cross-module integration functional

### Phase 4: Enhancement & Optimization (Weeks 9-12)
**Focus**: Feature completion, performance optimization, user experience polish
**Integration Requirements**: Advanced features requiring cross-module coordination

**Module Activities**:
- **Backend**: Performance optimization, advanced API features, monitoring
- **Frontend**: Enhanced visualization, user experience improvements, real-time features
- **AI**: Accuracy improvements, advanced relationship mapping, semantic search
- **Publishing**: Advanced personalization, analytics dashboard, A/B testing

**Deliverables**: Demo-ready system with enhanced features and optimized performance

### Phase 5: Integration & Production (Weeks 13-16)
**Focus**: Full system integration, production deployment, comprehensive testing
**Integration Requirements**: End-to-end workflows, shared infrastructure, unified monitoring

**Team Collaboration**:
- **Week 13**: Integration planning and API finalization
- **Week 14**: Cross-module feature implementation
- **Week 15**: End-to-end testing and performance validation
- **Week 16**: Production deployment and system monitoring

**Deliverables**: Production-ready integrated system with complete documentation

### Integration Dependencies

**Phase 2 Dependencies**:
- AI needs backend API specifications for job queue integration
- Frontend needs backend API contracts for component development
- Publishing needs user preference schemas from backend

**Phase 3 Dependencies**:
- AI processing depends on backend job queue implementation
- Frontend display depends on backend API data formats
- Publishing personalization depends on AI entity/relationship data

**Phase 4 Dependencies**:
- Advanced frontend features require real-time backend updates
- AI improvements need user feedback integration from frontend
- Publishing optimization requires engagement analytics from all modules

**Phase 5 Dependencies**:
- All modules must be feature-complete before integration
- Shared infrastructure decisions require team coordination
- Production deployment needs all modules containerized and tested

---

This system overview provides the foundational understanding needed for effective team coordination and module development. Each team member should be able to see how their work contributes to the overall product vision while understanding the specific integration points and dependencies that will guide development priorities.