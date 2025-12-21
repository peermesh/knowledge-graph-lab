# Frontend Design Module - Product Requirements Document (PRD)

**Module Name**: Frontend Design
**Version**: 0.1.0
**Owner(s)**: Frontend Module Specialist, UI/UX Team

---

**Purpose**: This template defines the structure for a comprehensive Product Requirements Document (PRD). Complete all sections below to create a source document ready for SpecKit processing (target: 600-800 lines for comprehensive modules, 300-500 for simpler modules).

**Why this matters**: SpecKit produces dramatically better results when given rich, detailed input that focuses on WHAT (not HOW). This template balances completeness with brevity—providing enough detail for implementation without over-specifying the solution.

**Who should use this**: Developers and module owners preparing functional and technical requirements for their modules (AI, Backend, Frontend, Publishing).

**⚠️ KEY PRINCIPLE**: Describe observable behavior and requirements, not implementation details. The `/plan` command and implementation team handle the HOW.

---

## Important: Length and Detail Guidance

**Comprehensive Spec (Phase 3 - WO-3):**
- Expected: 800-1,500 lines (detailed, implementation-focused)
- Purpose: Provide rich input for quality refinement
- Don't worry about length - capture all necessary detail

**Final Spec (Phase 4 - WO-4):**
- Target: 500-700 lines (refined, requirements-focused)
- Purpose: Implementation-ready PRD matching case study quality
- Achieved by: Removing implementation details, tightening language, eliminating redundancy

**What This Means:**
- It's NORMAL for this template to produce 1,000+ lines initially
- Quality refinement (WO-4) will reduce it to 500-700 lines
- Focus on completeness here, refinement comes later

---

## Section 1: Problem Statement (50-100 lines)

**Purpose**: Establish context - what problem are you solving and why it matters.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ Current situation described with quantified pain points (e.g., "2 hours/day wasted", "20% failure rate")
- ✅ Who is affected identified (specific user roles, scale expectations)
- ✅ Goals stated with measurable outcomes (e.g., "reduce time by 90%", "increase success to 99.9%")
- ✅ Problem statement is specific (not "improve efficiency" but "reduce manual sync time from 2 hours to 10 minutes")
- ✅ Business value clear (why solving this problem matters)
- ✅ Scale context provided (number of users, records, requests)

**This section is INCOMPLETE if:**
- ❌ Problem is vague or generic ("users want better experience")
- ❌ No quantified metrics (no numbers, percentages, or time estimates)
- ❌ Who is affected is unclear (just "users" without specificity)
- ❌ Goals are aspirational without measurable targets ("make things faster")
- ❌ Current situation not described (no baseline to improve from)
- ❌ Includes market research or competitive analysis (save for separate docs)

### What to include:

**Current Situation**:
*   What exists today (or doesn't exist) that necessitates this module.
*   Why the current approach is inadequate.
*   What specific pain points users or the system face.
*   Quantify the problem where possible (e.g., "developers waste 2 hours per day manually syncing data," "20% of requests fail due to...").

**Who is Affected**:
*   Primary users of this module (e.g., "backend developers," "content editors," "end-users on mobile").
*   Their environment and constraints.
*   Scale expectations (e.g., "10,000 daily active users," "1 million records," "20+ concurrent agents").

**Goals**:
*   What success looks like for the module.
*   Measurable outcomes (e.g., "reduce data sync time by 90%," "increase request success rate to 99.9%," "decrease dashboard load time to <500ms").

### What to Include (Requirements Focus):
✅ User pain points with quantified impact
✅ Current workflow and why it's inadequate
✅ Who is affected and their constraints
✅ Measurable goals and success metrics
✅ Scale expectations (users, records, concurrency)
✅ Business value and rationale

### What to Exclude (Implementation Details):
❌ Market research and competitive analysis
❌ Detailed cost-benefit calculations
❌ Historical context beyond immediate problem
❌ Team structure or organizational charts
❌ Project management methodology
❌ Technology selection rationale (save for Section 8)

### Level of Detail (Example):

**Good** (requirements-focused):
```
Current Situation: Developers manually maintain project tracking spreadsheets,
spending 2 hours/day on updates. 20% of status reports contain outdated information
due to sync delays.

Who is Affected: 15 backend developers managing 40+ active projects across 3 teams.

Goals: Centralized project tracking with real-time updates, reducing manual sync
time by 90% and eliminating data staleness.
```

**Too detailed** (implementation-focused):
```
Current Situation: The company uses Google Sheets (spreadsheet ID: 1a2b3c...)
with 47 columns tracking various metrics. Data is entered using Apps Script
triggers that run every 15 minutes. The sync process involves OAuth2 authentication
with refresh tokens stored in ~/.credentials/. Error rate analysis shows 18.7%
of requests fail due to rate limiting (HTTP 429). We compared 7 project management
tools (Jira, Asana, Linear, ...) with feature matrices and cost projections.
```

### 1.1 Current Situation

Currently, knowledge workers and researchers interact with the Knowledge Graph Lab through fragmented, inefficient interfaces that severely limit their ability to extract insights from entity relationships and data patterns. The existing approach requires users to navigate multiple disconnected systems, manually correlate data across different views, and struggle with outdated or incomplete information displays.

**Quantified Pain Points:**
- Users spend 20-30 minutes daily switching between 3-5 different tools to complete basic knowledge graph workflows
- Entity relationship exploration requires manual correlation across separate list views, graph views, and detail pages
- Real-time updates are missed because users must manually refresh multiple interfaces to see current data
- Complex entity relationships (6+ degrees of separation) become nearly impossible to navigate without proper visualization tools
- Mobile users are severely limited, with 80% of desktop features unavailable on mobile devices

**Current Manual Processes:**
1. **Data Discovery**: Users manually search across multiple APIs and databases to find relevant entities
2. **Relationship Mapping**: Manual correlation of entity connections using spreadsheets or basic list views
3. **Pattern Analysis**: Limited visualization capabilities force users to mentally map complex relationships
4. **Real-time Monitoring**: Manual refresh cycles miss important updates and changes to entity data
5. **Cross-device Access**: Inconsistent experiences across desktop, tablet, and mobile platforms

**Technical Limitations:**
- No unified dashboard for comprehensive entity overview and relationship exploration
- Limited graph visualization capabilities for large-scale knowledge graphs (1000+ nodes)
- Inefficient real-time update mechanisms causing data staleness issues
- Poor mobile responsiveness limiting accessibility for field researchers
- Inconsistent state management across different interface components

### 1.2 Users Affected

**Primary Users (Core Knowledge Workers):**
- **Researchers** (50-100 people): Daily users conducting entity relationship analysis and pattern discovery
- **Data Analysts** (20-40 people): Regular users creating reports and insights from knowledge graph data
- **Product Managers** (10-20 people): Weekly users making decisions based on entity relationship insights

**Secondary Users (Supporting Roles):**
- **System Administrators** (5-10 people): Weekly users configuring dashboards and managing user permissions
- **Content Creators** (15-25 people): Monthly users exploring entity relationships for content development
- **External Partners** (variable): Occasional users accessing shared knowledge graphs

**Scale Context:**
- **Daily Active Users**: 85-165 knowledge workers interacting with entity data
- **Dashboard Interactions**: 1,000-5,000 daily sessions across all platforms
- **Entity Relationships**: 50,000-200,000 relationships actively explored monthly
- **Mobile Usage**: 30-40% of users access via mobile devices for field research

**Usage Patterns:**
- **Peak Hours**: 9 AM - 5 PM weekdays with 60% of daily interactions
- **Session Duration**: Average 15-25 minutes per research session
- **Feature Usage**: 70% entity exploration, 20% dashboard customization, 10% data export

### 1.3 Goals and Success Metrics

**Primary Goals:**
1. **Unified Experience**: Single dashboard interface eliminating need for multiple tool switching
2. **Efficient Exploration**: Enable complex entity relationship discovery in under 5 minutes
3. **Real-time Awareness**: Live updates with sub-second latency for collaborative work
4. **Mobile Accessibility**: Full feature parity across all device types and screen sizes
5. **Performance Excellence**: Sub-2-second load times for 1000+ node graph visualizations

**Measurable Success Metrics:**
1. **Task Completion Time**: Reduce entity relationship discovery from 20-30 minutes to under 5 minutes (75% improvement)
2. **Context Switching**: Eliminate manual tool switching, reducing workflow time by 60%
3. **Real-time Updates**: Achieve 500ms latency for WebSocket updates (current: manual refresh only)
4. **Mobile Adoption**: Increase mobile usage from 15% to 40% of total sessions
5. **Graph Performance**: Render 1000+ node graphs in under 3 seconds (current: fails above 500 nodes)
6. **User Satisfaction**: Achieve 4.2/5 satisfaction score for dashboard usability (current: 3.1/5)
7. **Feature Utilization**: 80% of users actively use advanced filtering and search (current: 35%)
8. **Error Reduction**: Reduce failed graph loads from 12% to under 2% through performance optimization

**Timeline Milestones:**
- **MVP (Month 2)**: Core dashboard with basic entity visualization and real-time updates
- **Enhanced (Month 4)**: Advanced filtering, mobile optimization, and export capabilities
- **Mature (Month 6)**: Full feature parity across devices with advanced collaboration features

### 1.4 Business Value

**Operational Efficiency:**
Solving the fragmented interface problem will enable knowledge workers to complete research tasks 60% faster, reducing total research time from 25-35 hours to 10-14 hours per week per user. This efficiency gain across 85-165 users represents 2,000-4,000 hours of reclaimed productivity annually.

**Decision Quality:**
Real-time entity relationship visibility will improve decision-making speed and accuracy by providing immediate access to current data patterns. Product managers will make decisions 3x faster with 25% higher confidence, leading to better product outcomes and faster time-to-market for data-driven features.

**Collaborative Impact:**
Unified real-time interfaces will enable better cross-team collaboration on knowledge graph analysis. Teams will identify patterns and insights 40% faster through shared exploration sessions, reducing duplicate work and improving knowledge sharing across the organization.

**Technical Benefits:**
- **Scalability**: Support for 10x larger knowledge graphs without performance degradation
- **Maintainability**: Single codebase instead of multiple fragmented interfaces
- **Accessibility**: WCAG 2.1 AA compliance for broader user accessibility
- **Mobile Reach**: Enable field research capabilities previously impossible

**Strategic Value:**
The unified frontend will become the primary interface for all knowledge graph interactions, establishing the Knowledge Graph Lab as the central hub for organizational intelligence and research activities. This positions the platform as the go-to tool for entity relationship analysis and pattern discovery across all departments.

---

## Section 2: User Stories (5-10 stories)

**Purpose**: Describe how the module will be used in practice from a user's perspective.

**⚠️ CRITICAL**: SpecKit expects a formal user story format. Use the structure below exactly.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ 5-10 user stories covering all major workflows
- ✅ Each story follows "As a... I need... So that..." format
- ✅ User roles are specific with context (not just "user")
- ✅ Acceptance criteria are quantified (specific numbers, times, counts)
- ✅ Stories focus on WHAT capability is needed (not HOW to implement)
- ✅ Stories cover main user journeys end-to-end
- ✅ Edge cases mentioned in acceptance criteria where relevant

**This section is INCOMPLETE if:**
- ❌ Fewer than 5 stories (insufficient coverage of workflows)
- ❌ Stories lack quantified acceptance criteria ("fast" instead of "<2 seconds")
- ❌ Stories describe implementation ("using React form") instead of capability
- ❌ User roles are generic ("as a user") without context
- ❌ Stories missing "So that" benefit statement
- ❌ Acceptance criteria are vague ("works correctly")
- ❌ Major workflows not represented (gap in user journey coverage)

### User Story Format (REQUIRED):

**US-[N]: [Short Descriptive Title]**

As a [specific user type with context],
I need [specific capability or feature],
So that [measurable benefit or value].

**Acceptance**: [Quantified success criteria with specific numbers, times, or counts]

### What to Include (Requirements Focus):
✅ User role with specific context
✅ Capability or feature needed (WHAT, not HOW)
✅ Measurable benefit or value
✅ Quantified acceptance criteria
✅ 5-10 stories covering main workflows
✅ Given/When/Then format for acceptance

### What to Exclude (Implementation Details):
❌ UI mockups or wireframes
❌ Button labels or screen layouts
❌ Database queries or API calls
❌ Technology-specific implementation
❌ Internal system architecture
❌ Code structure or module organization

### Level of Detail (Example):

**Good** (requirements-focused):
```
US-1: Project Status Update

As a backend developer managing multiple projects,
I need to update project status in one centralized location,
So that all stakeholders see current information without manual sync.

Acceptance:
- Update completes in <2 seconds
- Changes visible to all users within 5 seconds
- Supports 20+ concurrent updates
```

**Too detailed** (implementation-focused):
```
US-1: Project Status Update via React Form

As a backend developer using Chrome browser on MacBook Pro,
I need a React form component with Material-UI TextField and Select components,
calling PUT /api/projects/:id with JWT authentication in Authorization header,
So that the PostgreSQL database updates the projects table via Prisma ORM,
triggering WebSocket broadcast through Socket.io to subscribed clients.

Acceptance:
- Form renders in <100ms (React.lazy with Suspense)
- API endpoint uses Express middleware for auth validation
- Database update uses transaction isolation level READ_COMMITTED
- WebSocket broadcast uses Redis pub/sub for horizontal scaling
```

### User Story Format (REQUIRED):

**US-1: Dashboard Overview Access**

As a knowledge worker starting my daily research session,
I need to view a personalized dashboard showing recent entity activity and key insights,
So that I can quickly orient myself to current data patterns and identify areas needing attention.

**Acceptance**:
- Dashboard loads in under 2 seconds showing personalized content
- Displays 5-10 most relevant recent entities based on my usage patterns
- Shows real-time activity indicators for entities updated in last 24 hours
- Provides quick access to entity exploration and relationship mapping
- Maintains dashboard state across browser sessions

**US-2: Entity Relationship Exploration**

As a researcher investigating complex entity connections,
I need to explore entity relationships through interactive graph visualization,
So that I can discover hidden patterns and insights in knowledge graph data.

**Acceptance**:
- Graph visualization renders complex relationships (1000+ nodes) in under 3 seconds
- Supports interactive filtering by relationship strength, entity types, and date ranges
- Enables drill-down into specific relationship details with metadata display
- Provides smooth zoom and pan controls for large graph navigation
- Exports relationship data in multiple formats (JSON, CSV, PDF)

**US-3: Real-time Collaboration**

As a data analyst working with team members on entity analysis,
I need to see real-time updates to entity data and relationships,
So that collaborative research sessions remain synchronized and productive.

**Acceptance**:
- WebSocket connection maintains real-time synchronization with 500ms latency
- Shows other users currently viewing the same entities or relationships
- Displays live updates to entity metadata and connection changes
- Supports shared annotation and bookmarking of interesting patterns
- Maintains update history for audit trail of collaborative changes

**US-4: Mobile Entity Access**

As a field researcher using mobile devices for on-site data collection,
I need full access to entity exploration and relationship mapping capabilities,
So that I can conduct research and analysis anywhere without desktop limitations.

**Acceptance**:
- Mobile interface provides 95% feature parity with desktop experience
- Touch-optimized graph interactions work smoothly on iOS and Android devices
- Responsive design adapts to phone, tablet, and desktop screen sizes
- Offline mode caches recently viewed entities for limited functionality
- Syncs changes when network connection is restored

**US-5: Advanced Search and Filtering**

As a product manager researching market trends and competitive landscapes,
I need advanced search and filtering capabilities across entity data,
So that I can quickly identify relevant patterns and make data-driven decisions.

**Acceptance**:
- Search interface supports complex queries with multiple filter criteria
- Autocomplete suggests relevant entities and relationship types during search
- Advanced filters include date ranges, confidence scores, and entity types
- Search results display in both list and graph visualization formats
- Saves and shares search configurations for recurring analysis needs

**US-6: Dashboard Customization**

As a system administrator managing user experiences across the organization,
I need to configure dashboard layouts and visualization preferences,
So that different user roles see relevant information in optimal formats.

**Acceptance**:
- Dashboard layout supports customizable widget arrangements and sizing
- Role-based permission system controls access to different dashboard features
- Visualization preferences (colors, layouts, interaction styles) are configurable
- Default dashboard configurations can be set for different user groups
- User-specific customizations persist across sessions and devices

**US-7: Data Export and Integration**

As a content creator developing reports and presentations from entity insights,
I need to export entity data and visualizations in multiple formats,
So that I can integrate findings into documents, presentations, and external systems.

**Acceptance**:
- Export functionality supports JSON, CSV, PDF, and image formats
- Large datasets (10,000+ entities) export progressively without blocking UI
- Maintains data relationships and metadata in exported formats
- Provides API endpoints for programmatic access to entity data
- Supports scheduled exports for recurring reporting needs

**US-8: Performance Monitoring**

As a technical lead ensuring system reliability and user experience,
I need visibility into frontend performance and user interaction patterns,
So that I can optimize the interface and address performance issues proactively.

**Acceptance**:
- Real-time performance metrics display for dashboard load times and interactions
- Error tracking captures and categorizes frontend failures and slow operations
- User engagement analytics show feature utilization and interaction patterns
- Performance alerts notify when metrics exceed defined thresholds
- Historical performance data supports trend analysis and optimization planning

---

## Section 3: Complete Data Model (if applicable)

**Purpose**: Define exactly what data your module stores and how it's structured.

**⚠️ CRITICAL**: SpecKit preserves complete data models perfectly. Do not skimp on details here. Provide full DDL or schemas.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ All tables/collections listed with descriptions
- ✅ All columns/fields with data types specified
- ✅ Primary keys identified for all tables
- ✅ Foreign keys documented with relationships explained
- ✅ Major constraints listed (UNIQUE, NOT NULL, CHECK constraints with reasoning)
- ✅ Indexes mentioned for performance-critical queries
- ✅ Relationships between entities clear (1-to-many, many-to-many)
- ✅ If stateless: Explicitly stated "No persistent data model"

**This section is INCOMPLETE if:**
- ❌ Tables listed without column definitions
- ❌ Data types missing or vague ("string" instead of "VARCHAR(255)")
- ❌ Primary keys not identified
- ❌ Foreign key relationships unclear or missing
- ❌ Constraints not documented (why UNIQUE? why NOT NULL?)
- ❌ Includes complete CREATE TABLE SQL (use high-level description instead)
- ❌ Indexes listed without explaining why they're needed
- ❌ Relationships between tables ambiguous

### What to include:

*   **For SQL Databases**: Provide complete `CREATE TABLE` statements (DDL), including all columns, types, constraints (`NOT NULL`, `UNIQUE`), primary keys, foreign keys, and indexes.
*   **For NoSQL Databases**: Provide complete JSON schemas for each document type.
*   **If Stateless**: Explicitly state "No persistent data model - this module is stateless" and describe any significant in-memory data structures.

### What to Include (Requirements Focus):
✅ Table names and brief descriptions
✅ Column names with data types
✅ Primary keys and foreign keys (which columns)
✅ Major constraints (UNIQUE, NOT NULL, CHECK)
✅ Integration schemas (JSON examples with field types)
✅ Relationships between entities (1-to-many, many-to-many)

### What to Exclude (Implementation Details):
❌ Complete CREATE TABLE statements with all syntax
❌ Index creation statements (mention indexes exist, not full DDL)
❌ Database migration scripts
❌ Query optimization details (EXPLAIN ANALYZE output)
❌ Backup and restore procedures
❌ Performance tuning parameters

### Level of Detail (Example):

**Good** (requirements-focused):
```
Table: users
Purpose: Store user subscription information
Columns:
  - id (UUID, primary key, auto-generated)
  - email (VARCHAR(255), unique, not null, email format)
  - created_at (TIMESTAMP, not null, defaults to now)

Foreign keys: None
Indexes: email (for lookup performance)
Constraints: Email must match valid email pattern
```

**Too detailed** (implementation-focused):
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
ANALYZE users;
```

## Frontend Data Model and State Management

The Frontend Design module manages client-side state and temporary data structures for optimal user experience. It does not maintain persistent storage - all data comes from Backend APIs and AI processing results.

### Core Data Entities

#### 1. Dashboard Configuration
```typescript
interface DashboardConfig {
  id: string;
  user_id: string;
  layout: WidgetLayout[];
  preferences: UserPreferences;
  widgets: WidgetConfig[];
  created_at: string;
  updated_at: string;
}

interface WidgetLayout {
  id: string;
  type: 'entity-list' | 'graph-view' | 'activity-feed' | 'metrics' | 'search';
  position: { x: number; y: number; width: number; height: number };
  settings: Record<string, any>;
}

interface UserPreferences {
  theme: 'light' | 'dark' | 'auto';
  default_view: 'list' | 'graph';
  auto_refresh: boolean;
  refresh_interval: number; // seconds
  notifications: NotificationSettings;
  accessibility: AccessibilitySettings;
}
```

#### 2. Entity State Management
```typescript
interface EntityState {
  entities: Map<string, EntityData>;
  relationships: Map<string, RelationshipData>;
  loading: Set<string>; // Entity IDs currently being loaded
  errors: Map<string, ErrorInfo>;
  cache: EntityCache;
}

interface EntityData {
  id: string;
  name: string;
  type: string;
  description?: string;
  confidence: number;
  metadata: Record<string, any>;
  relationships: string[]; // Related entity IDs
  position?: { x: number; y: number }; // For graph layout
  size?: number; // Visual size based on importance
  last_updated: string;
  source: 'api' | 'websocket' | 'cache';
}

interface RelationshipData {
  id: string;
  source_id: string;
  target_id: string;
  type: string;
  strength: number;
  label?: string;
  metadata: Record<string, any>;
  direction: 'unidirectional' | 'bidirectional';
}
```

#### 3. Search and Filter State
```typescript
interface SearchState {
  query: string;
  filters: SearchFilters;
  results: SearchResults;
  suggestions: SearchSuggestion[];
  history: SearchHistory[];
}

interface SearchFilters {
  entity_types?: string[];
  date_range?: { start: string; end: string };
  confidence_range?: { min: number; max: number };
  relationship_types?: string[];
  metadata_filters?: Record<string, any>;
}

interface SearchResults {
  entities: EntityData[];
  relationships: RelationshipData[];
  total_count: number;
  facets: SearchFacets;
  execution_time: number;
}

interface SearchSuggestion {
  text: string;
  type: 'entity' | 'relationship' | 'query';
  relevance_score: number;
}
```

#### 4. Real-time Update Management
```typescript
interface RealtimeState {
  connection_status: 'disconnected' | 'connecting' | 'connected' | 'error';
  subscriptions: Map<string, SubscriptionInfo>;
  pending_updates: UpdateQueue;
  last_heartbeat: string;
}

interface SubscriptionInfo {
  entity_id: string;
  subscription_type: 'entity' | 'relationship' | 'search';
  callback: (update: any) => void;
  created_at: string;
}

interface UpdateQueue {
  updates: RealtimeUpdate[];
  max_size: number;
  flush_interval: number; // milliseconds
}
```

#### 5. User Session Management
```typescript
interface UserSession {
  user_id: string;
  session_id: string;
  auth_token: string;
  refresh_token: string;
  permissions: UserPermissions;
  preferences: UserPreferences;
  activity_log: UserActivity[];
  expires_at: string;
}

interface UserPermissions {
  can_view: string[]; // Entity types user can access
  can_edit: string[]; // Dashboard configurations user can modify
  can_export: boolean;
  can_administer: boolean;
  role: 'viewer' | 'editor' | 'admin' | 'researcher';
}
```

#### 6. Visualization State
```typescript
interface VisualizationState {
  current_view: 'list' | 'graph' | 'timeline' | 'table';
  graph_config: GraphConfig;
  layout_engine: 'force-directed' | 'hierarchical' | 'circular';
  selected_entities: Set<string>;
  highlighted_relationships: Set<string>;
  zoom_level: number;
  pan_position: { x: number; y: number };
}

interface GraphConfig {
  node_size_range: [number, number];
  edge_thickness_range: [number, number];
  color_scheme: 'default' | 'type-based' | 'confidence-based';
  animation_duration: number;
  clustering_enabled: boolean;
  physics_enabled: boolean;
}
```

#### 7. Export Configuration
```typescript
interface ExportState {
  current_exports: Map<string, ExportJob>;
  export_history: ExportRecord[];
  default_formats: ExportFormat[];
  scheduled_exports: ScheduledExport[];
}

interface ExportJob {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number; // 0-100
  format: ExportFormat;
  data_selection: ExportDataSelection;
  created_at: string;
  estimated_completion?: string;
}
```

### State Management Architecture

#### Redux Store Structure
```typescript
interface RootState {
  auth: UserSession;
  dashboard: DashboardConfig;
  entities: EntityState;
  search: SearchState;
  realtime: RealtimeState;
  visualization: VisualizationState;
  export: ExportState;
  ui: UIState;
}

interface UIState {
  loading: GlobalLoadingState;
  errors: GlobalErrorState;
  modals: ModalState;
  notifications: NotificationState;
  responsive: ResponsiveState;
}
```

#### Cache Strategy
- **Browser Storage**: Dashboard configurations and user preferences
- **Memory Cache**: Recently viewed entities and search results
- **Service Worker Cache**: Static assets and offline data
- **CDN Cache**: Static assets with long-term caching headers

#### Data Flow Patterns
1. **Initial Load**: Dashboard → API calls → Redux state update → UI render
2. **Real-time Updates**: WebSocket → Redux state update → UI re-render
3. **User Interactions**: UI events → Redux actions → State update → API calls
4. **Search Operations**: Query → API call → Results caching → UI update
5. **Export Operations**: Selection → Background processing → Download trigger

### Integration Data Contracts

#### Backend API Response Formats
All API responses follow consistent patterns for frontend consumption:

```typescript
interface APIResponse<T> {
  data: T;
  metadata: {
    timestamp: string;
    request_id: string;
    pagination?: PaginationInfo;
    cache_info?: CacheInfo;
  };
  links?: {
    self: string;
    next?: string;
    prev?: string;
  };
}
```

#### WebSocket Message Formats
Real-time updates use structured message formats:

```typescript
interface WebSocketMessage {
  type: 'entity_update' | 'relationship_update' | 'user_activity' | 'system_notification';
  data: any;
  timestamp: string;
  id: string;
  source: 'backend' | 'ai' | 'user';
}
```

This data model ensures efficient state management, optimal performance, and seamless integration with backend services and real-time updates.

---

## Section 4: Acceptance Scenarios (3-5 detailed scenarios)

**Purpose**: Show step-by-step execution of key user stories.

**⚠️ CRITICAL**: SpecKit expects `Given/When/Then` format for testability. These scenarios should directly validate the acceptance criteria of your User Stories from Section 2.

**⚠️ CRITICAL**: Keep scenarios brief (15-20 lines max per scenario). Focus on WHAT happens, not HOW it's implemented.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ 3-5 scenarios covering main user stories from Section 2
- ✅ Each scenario follows Given/When/Then format (BDD style)
- ✅ Given conditions include specific example data (not placeholders)
- ✅ When actions are concrete with actual parameters
- ✅ Then outcomes are measurable and observable
- ✅ Measurement criteria specified for success
- ✅ Scenarios are brief (15-20 lines max, not 60+ lines with SQL)
- ✅ Scenarios validate acceptance criteria from user stories

**This section is INCOMPLETE if:**
- ❌ Fewer than 3 scenarios (insufficient coverage)
- ❌ Scenarios don't follow Given/When/Then structure
- ❌ Given conditions use placeholders ("[user]") instead of examples ("user@example.com")
- ❌ Scenarios include SQL queries or implementation code
- ❌ Then outcomes are vague ("works correctly") instead of specific ("returns HTTP 200 with user_id field")
- ❌ Scenarios exceed 20 lines (too detailed, focused on HOW not WHAT)
- ❌ No measurement criteria (how to verify success?)
- ❌ Scenarios don't map to user stories from Section 2

### Scenario Format (REQUIRED):

#### Scenario [N]: [Descriptive Title matching a User Story]

**Given** [specific starting conditions with actual data values]
- [Condition 1, e.g., A user with email "test@example.com" exists]

**When** [a specific action is taken with actual parameters]
- [e.g., The user submits a POST request to /login with email "test@example.com" and password "password123"]

**Then** [specific, measurable, and observable outcomes]
- [Assertion 1, e.g., The system returns an HTTP 200 status code]

**Measurement**: [How to verify - specific metric]

### What to Include (Requirements Focus):
✅ Given/When/Then format (BDD style)
✅ Specific starting conditions with example data
✅ Observable actions and outcomes
✅ Measurable success criteria
✅ 3-5 scenarios covering main workflows
✅ 15-20 lines max per scenario

### What to Exclude (Implementation Details):
❌ Complete test code or test frameworks
❌ SQL queries or database operations
❌ API endpoint implementations
❌ Error handling code
❌ Retry logic or circuit breakers
❌ 60+ line scenarios with SQL setup

### Level of Detail (Example):

See examples below in original template section.

---

### Examples

❌ **TOO MUCH** (60+ lines with SQL statements, detailed implementation):
```
Scenario 1: Weekly Digest Delivery
Given:
- Database has the following records:
  - User table: INSERT INTO users (id, email, digest_interval, tags) VALUES (1, 'user@example.com', 'weekly', '["creator economy", "AI"]');
  - Articles table: INSERT INTO articles (id, title, url, tags, published_date) VALUES ...
  - [30 more lines of SQL setup]
When:
- Scheduler executes at Monday 9:00 AM
- System queries: SELECT * FROM articles WHERE tags @> ANY(SELECT tags FROM users WHERE digest_interval = 'weekly')
- [20 more lines of SQL queries and implementation details]
Then:
- Email queue contains record with specific HTML template structure
- [10 more lines of implementation assertions]
```

✅ **JUST RIGHT** (15-20 lines, focused on observable behavior):
```
Scenario 1: Weekly Digest Delivery
Given:
- User configured weekly digest for tags "creator economy" and "AI"
- 5 matching articles published in the past 7 days
- Scheduled time: Monday 9:00 AM

When:
- Scheduled time arrives
- Digest generation job executes

Then:
- Email delivered within 2 minutes
- Email contains 3-5 matching articles
- Each article includes: title, summary, link
- Email includes unsubscribe link
- User's next_digest_date updated to next Monday 9:00 AM

Measurement: 95% of digests delivered within 15 minutes of scheduled time
```

---

## Section 5: Performance Targets (quantified)

**Purpose**: Define the measurable performance requirements.

**⚠️ CRITICAL**: Every target MUST be quantified with numbers and units.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ Response times quantified with percentiles (p50, p95, p99)
- ✅ Throughput targets with units (requests/second, records/minute)
- ✅ Scalability limits specified (max users, max records, max concurrency)
- ✅ Resource constraints documented (memory, CPU, storage limits)
- ✅ Availability targets stated (uptime %, acceptable downtime)
- ✅ All targets have numbers and units (not "fast" but "<200ms p95")
- ✅ Targets are realistic for expected usage patterns

**This section is INCOMPLETE if:**
- ❌ Targets use qualitative terms ("fast", "responsive", "scalable")
- ❌ No percentiles specified for response times (p50/p95/p99)
- ❌ Throughput without units ("500" instead of "500 requests/second")
- ❌ Scalability limits vague ("lots of users" instead of "10,000 concurrent")
- ❌ Includes benchmark results or load test output (state targets, not test results)
- ❌ Server specifications listed (CPU/RAM) instead of behavior requirements
- ❌ Targets unrealistic (requiring impossible performance)
- ❌ Missing key dimension (response time stated but no throughput target)

### What to include:

**Response Times**:
*   API endpoint latency: e.g., `< 200ms for 95th percentile`

**Throughput**:
*   Requests per second: e.g., `Handles 500 requests/sec`

**Scalability Limits**:
*   Maximum records/documents: e.g., `Scales to 10 million documents`

### What to Include (Requirements Focus):
✅ Quantified response times (with percentiles)
✅ Throughput targets (requests/second, records/minute)
✅ Scalability limits (max users, max records)
✅ Resource constraints (memory, CPU, storage)
✅ Concurrency requirements
✅ Availability targets (uptime %)

### What to Exclude (Implementation Details):
❌ Benchmark results or load test output
❌ Server specifications (CPU cores, RAM GB)
❌ Database tuning parameters
❌ Caching strategies (Redis config, TTL values)
❌ Network configuration details
❌ Infrastructure sizing calculations

### Level of Detail (Example):

**Good** (requirements-focused):
```
Response Times:
- API endpoints: <200ms (p95), <500ms (p99)
- Database queries: <50ms (p95)

Throughput:
- 500 requests/second sustained
- 1000 requests/second peak (5-minute burst)

Scalability:
- 10,000 concurrent users
- 1 million records in database
- 100 concurrent updates
```

**Too detailed** (implementation-focused):
```
Response Times:
- API endpoints: <200ms on AWS t3.medium with 2 vCPU and 4GB RAM
- Achieved via Nginx reverse proxy with gzip compression level 6
- Redis cache (cache-aside pattern) with 15-minute TTL
- Connection pooling: min 10, max 100 connections

Throughput:
- Load test results: ApacheBench -n 10000 -c 100 shows 523 req/sec
- Tested on m5.xlarge EC2 instances in us-east-1
- Database: PostgreSQL 14 with shared_buffers=256MB, work_mem=4MB
- Horizontal scaling via AWS ALB distributing to 3 instances
```

---

## Section 6: Implementation Phases (3-5 high-level milestones)

**Purpose**: Identify major delivery milestones - WHAT to deliver, not HOW to build it.

**⚠️ SIMPLIFIED**: This section defines high-level milestones only. The `/plan` command creates detailed implementation phases with tasks and sequences.

**⚠️ NO TIME ESTIMATES**: Focus on deliverables and dependencies, not duration estimates.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ 3-5 high-level phases (milestones, not day-by-day tasks)
- ✅ Each phase has clear goal (what it achieves)
- ✅ Deliverables are specific and testable per phase
- ✅ Dependencies between phases identified
- ✅ Phases are logically grouped (related deliverables together)
- ✅ MVP-focused sequence (core functionality first)
- ✅ No time estimates or schedules (focus on WHAT not WHEN)

**This section is INCOMPLETE if:**
- ❌ More than 5 phases (too granular, should be high-level milestones)
- ❌ Phases include day-by-day or hour-by-hour schedules
- ❌ Deliverables are vague ("make progress", "work on feature")
- ❌ Dependencies unclear or missing
- ❌ Phases describe HOW to build (technology details, implementation approach)
- ❌ Includes sprint planning or story points
- ❌ Individual developer assignments listed
- ❌ Phases out of logical order (later work blocking earlier work)

### What to include:

For each phase (aim for 3-5 phases):

**Phase [N]: [Phase Name]**

**Goal**: [What this phase achieves - the outcome, not the process]

**Deliverables**:
- [Specific output 1, e.g., "Complete database schema committed"]
- [Specific output 2, e.g., "API endpoints functional"]

**Dependencies**:
- [What must be complete before starting this phase]

### What to Include (Requirements Focus):
✅ 3-5 high-level milestones
✅ What each phase delivers (outcomes)
✅ Dependencies between phases
✅ Logical grouping of deliverables
✅ MVP-focused sequence
✅ Phase goals (not durations)

### What to Exclude (Implementation Details):
❌ Day-by-day or hour-by-hour schedules
❌ Individual developer assignments
❌ Sprint planning or story points
❌ Detailed task breakdowns (save for `/plan`)
❌ Technology evaluation criteria
❌ Team coordination logistics

### Level of Detail (Example):

**Good** (requirements-focused):
```
Phase 1: Core Infrastructure
Goal: Establish foundational data storage and job scheduling
Deliverables:
- Database schema deployed
- Basic CRUD API endpoints
- Job scheduler configured
Dependencies: None

Phase 2: Digest Generation Logic
Goal: Implement content matching and email composition
Deliverables:
- Article matching algorithm
- Email template system
- Content ranking logic
Dependencies: Phase 1 complete
```

**Too detailed** (implementation-focused):
```
Phase 1: Core Infrastructure (Sprint 1-2, Days 1-10)
Goal: Establish foundational data storage using PostgreSQL 14 with Prisma ORM
Deliverables:
- Day 1-2: Developer environment setup with Docker Compose
- Day 3-4: Database schema (migrations written in Prisma DSL)
- Day 5-6: CRUD endpoints (Express router with Joi validation)
- Day 7-8: Celery setup (RabbitMQ message broker, 4 worker processes)
- Day 9-10: Testing and code review
Team: 2 backend developers (Alice on DB, Bob on API)
Technology evaluation: Considered Bull vs Celery (Celery chosen for Python integration)
Dependencies: AWS RDS instance provisioned, VPC configured
```

---

### Example

**Phase 1: Core Infrastructure**
**Goal**: Establish foundational data storage and job scheduling
**Deliverables**:
- Database schema deployed
- Basic CRUD API endpoints
- Job scheduler (Celery) configured
**Dependencies**: None

**Phase 2: Digest Generation Logic**
**Goal**: Implement content matching and email composition
**Deliverables**:
- Article matching algorithm
- Email template system
- Content ranking logic
**Dependencies**: Phase 1 complete

---

## Section 7: Edge Cases (10-15 cases, 2-3 lines each)

**Purpose**: Document failure modes, boundary conditions, and unusual situations.

**⚠️ BRIEF FORMAT**: State the situation and expected behavior. Do NOT include implementation details, error handling code, or retry logic specifics.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ 10-15 edge cases covering main scenarios
- ✅ Each edge case in format "EC-N: [Situation] → [Expected behavior]"
- ✅ Each edge case is 2-3 lines (not 15+ lines with code)
- ✅ Failure scenarios covered (API timeouts, service outages, network errors)
- ✅ Boundary conditions covered (empty data, maximum limits, null values)
- ✅ Concurrency issues covered (simultaneous updates, overlapping jobs)
- ✅ Data quality issues covered (invalid input, malformed data, type mismatches)
- ✅ Edge cases are realistic (not theoretical "what if aliens attack?")

**This section is INCOMPLETE if:**
- ❌ Fewer than 10 edge cases (insufficient coverage)
- ❌ Edge cases include detailed error handling code or retry logic
- ❌ Edge cases exceed 3 lines (too detailed, implementation-focused)
- ❌ Only happy path scenarios (no failure modes documented)
- ❌ Edge cases are too general ("handle errors appropriately")
- ❌ Missing critical scenarios (e.g., external API failure not covered)
- ❌ Edge cases include exception class hierarchies or logging details
- ❌ Vague expected behavior ("do the right thing" instead of specific action)

### Format (REQUIRED):

**EC-[N]**: [Situation] → [Expected behavior]

### What to include:

**Failure Scenarios** - External dependencies fail:
- API timeouts, service outages, network errors

**Boundary Conditions** - Empty or extreme data:
- No matching records, maximum limits reached, null values

**Concurrency Issues** - Race conditions or conflicts:
- Simultaneous updates, overlapping jobs

**Data Quality Issues** - Invalid or malformed data:
- Missing required fields, type mismatches

### What to Include (Requirements Focus):
✅ Situation description (what happens)
✅ Expected behavior (what system does)
✅ 10-15 edge cases covering main scenarios
✅ 2-3 lines per edge case
✅ Failure modes and boundary conditions
✅ Concurrency and data quality issues

### What to Exclude (Implementation Details):
❌ Complete error handling code
❌ Retry logic specifics (exponential backoff algorithms)
❌ Exception class hierarchies
❌ Logging implementation details
❌ Circuit breaker configurations
❌ Detailed recovery procedures

### Level of Detail (Example):

**Good** (requirements-focused):
```
EC-1: SES API timeout → Retry 3x with backoff, mark failed if all attempts fail, alert admin
EC-2: No matching articles for user's tags → Skip user this cycle, log INFO, don't increment schedule
EC-3: User changes interval during processing → Lock row, update takes effect next cycle
EC-4: Article URL returns 404 → Exclude from digest, log WARNING, mark article inactive
EC-5: Email template rendering fails → Use plain text fallback, alert admin
EC-6: Database connection lost → Pause job, retry connection 5x, fail job if persistent
```

**Too detailed** (implementation-focused):
```
EC-1: SES API Timeout Handling
When the AWS SES API times out during email sending:
1. Catch the boto3.exceptions.ReadTimeoutError exception
2. Implement exponential backoff: retry after 1s, 2s, 4s
3. Log each retry attempt with timestamp and error details
4. After 3 failed attempts, mark email as failed in database
5. Update email_queue table: SET status='failed', error_message=...
6. Trigger CloudWatch alarm if failure rate exceeds 5%
7. Send notification to admin via SNS topic
```

---

### Examples

❌ **TOO MUCH** (Implementation details and code):
```
EC-1: SES API Timeout Handling
When the AWS SES API times out during email sending:
1. Catch the boto3.exceptions.ReadTimeoutError exception
2. Implement exponential backoff: retry after 1s, 2s, 4s
3. Log each retry attempt with timestamp and error details
4. After 3 failed attempts, mark email as failed in database
5. Update email_queue table: SET status='failed', error_message=...
6. Trigger CloudWatch alarm if failure rate exceeds 5%
7. Send notification to admin via SNS topic
```

✅ **JUST RIGHT** (Situation → behavior, 2-3 lines):
```
**EC-1**: SES API timeout → Retry 3x with backoff, mark failed if all attempts fail, alert admin
**EC-2**: No matching articles for user's tags → Skip user this cycle, log INFO, don't increment schedule
**EC-3**: User changes interval during processing → Lock row, update takes effect next cycle
**EC-4**: Article URL returns 404 → Exclude from digest, log WARNING, mark article inactive
**EC-5**: Email template rendering fails → Use plain text fallback, alert admin
**EC-6**: Database connection lost → Pause job, retry connection 5x, fail job if persistent
```

---

## Section 8: Technology Constraints

**Purpose**: Document the required technologies and constraints (the **WHAT**, not the *why*).

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ Required language and version specified (e.g., "Python 3.11+")
- ✅ Required database and version specified (e.g., "PostgreSQL 15+")
- ✅ Required external services/APIs listed (e.g., "AWS SES for email")
- ✅ Required libraries with version constraints (e.g., "celery>=5.3.0")
- ✅ Deployment constraints clear (e.g., "Must run as Docker container")
- ✅ Platform constraints stated (e.g., "AWS ECS", "Linux only")
- ✅ Constraints are requirements, not preferences

**This section is INCOMPLETE if:**
- ❌ Technology choices explained (WHY instead of WHAT)
- ❌ Includes comparison matrices or evaluation criteria
- ❌ Alternative options listed (should only state requirements, not alternatives)
- ❌ Missing version constraints ("Python" instead of "Python 3.11+")
- ❌ Includes detailed library configuration (state library, not config)
- ❌ Performance benchmarks comparing technologies
- ❌ Team skill assessments or organizational preferences
- ❌ Vague constraints ("modern database" instead of specific requirement)

### What to include:

**Required Technologies**:
*   Primary technologies that MUST be used (e.g., "Language: Python 3.11+", "Database: PostgreSQL 15+").

**External Dependencies**:
*   Required external services or libraries (e.g., "Requires access to the Stripe API v3," "Must use the `requests` library v2.28+").

**Constraints**:
*   Things the system MUST or MUST NOT do (e.g., "Must be deployable as a Docker container," "Cannot write to the local filesystem").

### What to Include (Requirements Focus):
✅ Required language and version
✅ Required database and version
✅ Required external services/APIs
✅ Required libraries (with version constraints)
✅ Deployment constraints (Docker, serverless, etc.)
✅ Platform constraints (cloud provider, OS)

### What to Exclude (Implementation Details):
❌ Technology comparison matrices
❌ Why technology was chosen (evaluation criteria)
❌ Alternative options considered
❌ Detailed library configuration
❌ Performance benchmarks comparing options
❌ Team skill assessments

### Level of Detail (Example):

**Good** (requirements-focused):
```
Language: Python 3.11+
Database: PostgreSQL 15+
External Services: AWS SES for email delivery
Required Libraries:
- celery>=5.3.0 (job scheduling)
- psycopg2>=2.9.0 (database driver)

Constraints:
- Must be deployable as Docker container
- Cannot write to local filesystem (use S3 for storage)
- Must run on AWS ECS
```

**Too detailed** (implementation-focused):
```
Language: Python 3.11+ (chosen over Node.js and Go)
Evaluation: Python scored 8/10 (Node.js 6/10, Go 7/10)
Criteria: Team expertise (5 Python devs, 2 Node devs), library ecosystem, AI integration

Database: PostgreSQL 15+ (chosen over MySQL and MongoDB)
Comparison matrix:
| Feature | PostgreSQL | MySQL | MongoDB |
|---------|-----------|-------|---------|
| JSON support | Native | Limited | Native |
| ACID | Full | Full | Eventual |
| Performance | 10k qps | 8k qps | 15k qps |
Benchmark: pgbench results show 9,847 TPS on m5.xlarge

External Services: AWS SES (evaluated vs SendGrid, Mailgun)
Cost analysis: SES $0.10/1000 emails, SendGrid $0.85/1000
```

---

## Section 9: Testing Strategy (approach only, not full test suite)

**Purpose**: Describe the testing APPROACH and targets. Do NOT design the complete test suite.

**⚠️ SIMPLIFIED**: State WHAT to test and target metrics. The implementation team designs specific test cases.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ Unit test approach defined (what modules/functions to test)
- ✅ Integration test approach defined (what workflows to test end-to-end)
- ✅ Performance test approach defined (what operations to test under load)
- ✅ Acceptance test approach defined (how to validate scenarios from Section 4)
- ✅ Coverage targets specified (percentage or scope, e.g., ">80% line coverage")
- ✅ What to test stated, not HOW to test (no specific test code)
- ✅ Success criteria for test suite defined

**This section is INCOMPLETE if:**
- ❌ Includes complete test suite with individual test names
- ❌ Includes specific test code or pseudo-code
- ❌ Test framework configuration details (Jest config, pytest fixtures)
- ❌ Mocking strategies or stub implementations
- ❌ CI/CD pipeline configuration
- ❌ Coverage targets missing or vague ("good coverage")
- ❌ No mention of performance or acceptance testing (only unit tests)
- ❌ Test data generation scripts or fixtures

### What to include:

**Unit Tests**:
*   What key modules/functions require unit tests (not specific test cases)
*   Target coverage (e.g., ">80% line coverage for business logic")

**Integration Tests**:
*   What workflows to test end-to-end (e.g., "User signup through first digest delivery")
*   What external integrations to test (e.g., "SES email delivery, database transactions")

**Load/Performance Tests**:
*   What operations to test under load (reference Section 5 targets)
*   Expected scale (e.g., "1000 concurrent digest generations")

**Acceptance Tests**:
*   How to validate Acceptance Scenarios from Section 4
*   Success criteria (e.g., "All scenarios pass in staging environment")

### What to Include (Requirements Focus):
✅ Testing approach for each layer (unit, integration, acceptance)
✅ Coverage targets (percentage or scope)
✅ What to test (modules, workflows, integrations)
✅ Performance test targets (from Section 5)
✅ Success criteria for test suite
✅ Acceptance scenario validation approach

### What to Exclude (Implementation Details):
❌ Complete test suite with individual test names
❌ Specific test code or pseudo-code
❌ Test framework configuration (Jest config, pytest fixtures)
❌ Mocking strategies or stub implementations
❌ CI/CD pipeline configuration
❌ Test data generation scripts

### Level of Detail (Example):

**Good** (requirements-focused):
```
Unit Tests:
- Article matching algorithm
- Email template rendering
- Content ranking logic
- Target: >80% line coverage for business logic

Integration Tests:
- End-to-end: User signup → preference setting → first digest delivery
- External: SES email delivery, PostgreSQL transactions
- Target: All critical workflows covered

Performance Tests:
- 500 requests/sec sustained (per Section 5)
- 1000 concurrent digest generations
- Target: Meet all Section 5 performance targets

Acceptance Tests:
- Validate all scenarios from Section 4
- Success: All scenarios pass in staging environment
```

**Too detailed** (implementation-focused):
```
Unit Tests (Jest framework):
- describe('ArticleMatcher', () => {
    test('should match articles by tag', async () => { ... })
    test('should handle empty tag array', async () => { ... })
    test('should respect date filters', async () => { ... })
  })
- Mock implementation: jest.mock('../services/database')
- Fixtures: __fixtures__/articles.json (127 test records)
- Coverage: nyc --reporter=html --reporter=text
- CI: Run on every PR via GitHub Actions workflow

Integration Tests (Supertest + testcontainers):
- beforeAll(): Start PostgreSQL container, seed database
- Test 1: POST /signup → GET /preferences → Celery job triggers → SES sends email
- Test 2: PUT /preferences → Immediate reschedule → Next digest uses new tags
- Cleanup: afterAll() tears down containers, cleans temp files
```

---

### What NOT to include:
- Detailed test case designs
- Specific test code or pseudo-code
- Complete test suite breakdown with individual test names
- Mocking strategies or test infrastructure details

---

## Section 10: Open Questions and Assumptions

**Purpose**: Document remaining unknowns and assumptions made during PRD creation.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ All open questions listed with resolution path
- ✅ All assumptions documented with rationale
- ✅ Assumptions categorized by type (business logic, integration, technical)
- ✅ Each assumption explains why it was made and impact if wrong
- ✅ Owner identified for resolving each open question
- ✅ Priority assigned to questions (critical/important/nice-to-have)
- ✅ Validation plan for assumptions (how/when to verify)

**This section is INCOMPLETE if:**
- ❌ Open questions without resolution path or owner
- ❌ Assumptions made but not documented (hidden assumptions are dangerous)
- ❌ Assumptions without rationale (why was this assumption necessary?)
- ❌ No priority on open questions (which ones block implementation?)
- ❌ Assumptions without impact analysis (what if assumption is wrong?)
- ❌ No validation plan (how will assumptions be verified?)
- ❌ Questions that should have been answered during research still open
- ❌ Section empty when assumptions were clearly made (dishonest documentation)

---

## Section 11: Success Criteria

**Purpose**: Define measurable completion criteria for the entire module.

### Completeness Guidance

**This section is COMPLETE when it includes:**
- ✅ User-facing metrics with target values (completion rates, satisfaction scores)
- ✅ Technical metrics with target values (error rates, response times, uptime)
- ✅ Measurement methods specified for each metric
- ✅ Completion checklist referencing other sections
- ✅ Launch readiness criteria clear (what must be true to ship?)
- ✅ MVP success definition specific and measurable
- ✅ All metrics align with Section 1 goals and Section 5 performance targets

**This section is INCOMPLETE if:**
- ❌ Metrics without target values ("improve completion rate" vs ">90%")
- ❌ Vague measurement methods ("we'll track it somehow")
- ❌ No user-facing success metrics (only technical metrics)
- ❌ No technical success metrics (only business metrics)
- ❌ Completion checklist missing or incomplete
- ❌ Metrics don't align with earlier sections (inconsistent targets)
- ❌ Includes specific monitoring tools/dashboards (state WHAT to measure, not HOW)
- ❌ No definition of what "done" means for this module

### User-Facing Success

**Metrics with Target Values**:
*   [Metric 1]: [Target value with units]
    - Example: "User signup completion rate: >90%"
*   [Metric 2]: [Target value with units]
    - Example: "Digest open rate: >25%"

**Measurement Method**:
*   How will these metrics be tracked? (e.g., "Analytics dashboard, weekly reports")

### Technical Success

**Metrics with Target Values**:
*   [Metric 1]: [Target value with units]
    - Example: "API error rate: <0.1%"
*   [Metric 2]: [Target value with units]
    - Example: "P95 response time: <200ms"
*   [Metric 3]: [Target value with units]
    - Example: "System uptime: >99.9%"

**Measurement Method**:
*   How will these metrics be monitored? (e.g., "CloudWatch dashboards, PagerDuty alerts")

### Completion Criteria

The module is considered DONE when:
*   [ ] All user stories from Section 2 implemented and demonstrated
*   [ ] All acceptance scenarios from Section 4 pass in staging
*   [ ] All performance targets from Section 5 validated under load
*   [ ] All edge cases from Section 7 have defined behavior
*   [ ] Testing strategy from Section 9 executed successfully
*   [ ] Documentation complete (API docs, runbooks, user guides)
*   [ ] Code reviewed and merged to main branch
*   [ ] Deployed to production and monitored for 48 hours

### What to Include (Requirements Focus):
✅ Quantified user-facing metrics (completion rates, satisfaction scores)
✅ Quantified technical metrics (error rates, response times, uptime)
✅ Measurement methods for each metric
✅ Completion checklist (from other sections)
✅ Launch readiness criteria
✅ MVP success definition

### What to Exclude (Implementation Details):
❌ Specific measurement tools (Datadog vs New Relic)
❌ Dashboard JSON configurations
❌ Alert threshold tuning details
❌ Monitoring infrastructure setup
❌ Analytics implementation code
❌ Metric collection pipeline architecture

### Level of Detail (Example):

**Good** (requirements-focused):
```
User-Facing Success:
- User signup completion: >90%
- Digest open rate: >25%
- User retention (30 days): >60%
Measurement: Analytics dashboard, weekly reports

Technical Success:
- API error rate: <0.1%
- P95 response time: <200ms
- System uptime: >99.9%
Measurement: Monitoring dashboard, automated alerts

Completion Criteria:
- All user stories implemented
- All acceptance scenarios pass
- All performance targets met
- 48 hours production monitoring passed
```

**Too detailed** (implementation-focused):
```
User-Facing Success:
- User signup completion: >90% (tracked via Google Analytics 4)
  - Event: signup_complete (custom dimension: source_channel)
  - Dashboard: https://analytics.google.com/dashboard/xyz123
  - BigQuery export: daily at 3 AM UTC
  - Retention analysis: Segment.io cohort builder
- Digest open rate: >25% (AWS SES open tracking + Pixel)
  - Implementation: 1x1 transparent GIF embedded in email
  - Tracking URL: https://tracker.example.com/open?id={user_id}
  - Storage: Redshift table email_events with 90-day TTL

Technical Success:
- API error rate: <0.1% (Datadog APM + custom instrumentation)
  - Metric: aws.apigateway.5xxError / aws.apigateway.count
  - Alert: PagerDuty P2 if error rate >0.5% for 5 minutes
  - Dashboard: Datadog screenboard ID 1234567
```

---

## Validation Checklist

Before submitting this PRD to SpecKit, verify:

### Completeness
- [ ] All 11 sections are complete (Sections 1-9, 11; Section 10 is reserved).
- [ ] Module information (name, version, owners) is filled in.
- [ ] The "Success Criteria" section (Section 11) is filled out.
- [ ] Target length achieved (600-800 lines for comprehensive specs, 300-500 for simpler modules).
- [ ] No [NEEDS CLARIFICATION] markers remain.

### Quality
- [ ] All requirements are specific and testable.
- [ ] All performance targets are quantified with numbers.
- [ ] All technology choices are constraints (WHAT not WHY).
- [ ] Data model is complete with types and relationships.
- [ ] Acceptance scenarios are brief (15-20 lines each) and focus on observable behavior.
- [ ] Edge cases use EC-N format (2-3 lines each, situation → behavior).
- [ ] Implementation phases are high-level milestones without time estimates.
- [ ] Testing strategy describes approach, not detailed test cases.

### Consistency
- [ ] No contradictions between sections.
- [ ] User stories align with acceptance scenarios.
- [ ] Performance targets align with scale requirements.
- [ ] Testing strategy covers all critical scenarios.
- [ ] Success criteria (Section 11) aligns with user stories and acceptance scenarios.

### Readiness
- [ ] Document reviewed by module owner.
- [ ] Technical feasibility validated.
- [ ] Dependencies identified and understood.
- [ ] Document avoids over-specification (no SQL in scenarios, no code in edge cases, no detailed test suites).

### What to Include (Requirements Focus):
✅ All sections complete and substantive
✅ All checklists filled with concrete verification
✅ Cross-section consistency verified
✅ Requirements-focused throughout (WHAT not HOW)
✅ No placeholders or TBD markers
✅ Module owner sign-off

### What to Exclude (Implementation Details):
❌ Premature validation of implementation approach
❌ Technology evaluation details
❌ Team capacity or resource planning
❌ Project management artifacts
❌ Cost estimates or budgets
❌ Stakeholder approval workflows

### Level of Detail (Example):

**Good** (requirements-focused checklist):
```
Completeness:
- All 10 sections filled (Section 10 is placeholder)
- 625 lines total (within 600-800 target)
- No TBD or [NEEDS CLARIFICATION] markers
- Module: Publishing, Owner: Backend team

Quality:
- All 7 user stories have quantified acceptance criteria
- All 5 acceptance scenarios use Given/When/Then
- 12 edge cases in EC-N format (2-3 lines each)
- Performance targets: All have numbers and units

Consistency:
- User stories US-2, US-3, US-5 map to Scenarios 1, 2, 3
- Performance targets reference scale from Problem Statement
- Testing strategy covers all acceptance scenarios
```

**Too detailed** (implementation-focused):
```
Not applicable - validation checklist should be quick yes/no checks,
not detailed implementation validation. Save implementation validation
for Phase 4 (WO-4) quality comparison against case study.
```