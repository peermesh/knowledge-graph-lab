# Publishing Module - Data Model

**Created**: 2025-10-23
**Feature**: Publishing Module
**Status**: Complete

## Core Entities

### Publishing Channels

**Purpose**: Define available publishing channels and their configuration for multi-channel content delivery.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier for the channel
- `name` (VARCHAR(100), NOT NULL, UNIQUE): Human-readable channel name
- `channel_type` (ENUM: email|slack|discord|webhook|rss): Type of delivery channel
- `is_active` (BOOLEAN, NOT NULL, DEFAULT true): Whether channel is available for publishing
- `configuration` (JSONB, NOT NULL): API keys, endpoints, and channel-specific settings
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT now()): Channel creation timestamp
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT now()): Last modification timestamp

**Relationships**:
- Referenced by content_publications.channel_results
- Used in subscriber_profiles.preferred_channels

**Constraints**:
- channel_type must be valid enum value
- name must be unique across all channels

**Indexes**:
- channel_type (for filtering by delivery type)
- is_active (for active channels only)

---

### Subscriber Profiles

**Purpose**: Store user subscription preferences and personalization data for targeted content delivery.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier for subscriber profile
- `user_id` (UUID, NOT NULL, Foreign Key → users.id): Reference to user account
- `email` (VARCHAR(255), UNIQUE, NOT NULL): Primary email for delivery
- `preferred_channels` (JSONB, NOT NULL): Array of preferred delivery channels with settings
- `topic_interests` (JSONB, NOT NULL): Key-value pairs of research topics and interest levels (0.0-1.0)
- `frequency_settings` (JSONB, NOT NULL): Delivery frequency preferences by channel
- `personalization_data` (JSONB, NOT NULL): Engagement history and preference learning data
- `subscription_status` (ENUM: active|paused|unsubscribed, NOT NULL, DEFAULT active): Current subscription state
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT now()): Profile creation timestamp
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT now()): Last modification timestamp

**Relationships**:
- References users.id via user_id
- Referenced by publishing_analytics.user_id

**Constraints**:
- email must match valid email pattern
- subscription_status must be valid enum value
- topic_interests values must be between 0.0 and 1.0

**Indexes**:
- user_id (for user lookups)
- email (for email-based operations)
- subscription_status (for active subscribers)

---

### Content Publications

**Purpose**: Track all content publication attempts and their outcomes across multiple channels.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier for publication record
- `content_id` (UUID, NOT NULL, Foreign Key → content.id): Reference to source content
- `publication_type` (ENUM: newsletter|alert|digest|manual, NOT NULL): Type of publication
- `scheduled_time` (TIMESTAMP, NOT NULL): When publication should occur
- `published_time` (TIMESTAMP, NULL): Actual publication completion time
- `status` (ENUM: scheduled|processing|completed|failed|cancelled, NOT NULL, DEFAULT scheduled): Current publication status
- `channel_results` (JSONB, NOT NULL): Delivery results per channel (success/failure details)
- `engagement_metrics` (JSONB, NOT NULL): Opens, clicks, unsubscribes by channel
- `personalization_applied` (JSONB, NOT NULL): Personalization decisions made for this publication
- `error_details` (TEXT, NULL): Error information if publication failed
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT now()): Publication record creation
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT now()): Last status update

**Relationships**:
- References content.id via content_id
- Referenced by publishing_analytics.publication_id

**Constraints**:
- status must be valid enum value
- scheduled_time must be in the future when status is 'scheduled'

**Indexes**:
- content_id (for content publication history)
- scheduled_time (for scheduling operations)
- status (for active publications)

---

### Content Templates

**Purpose**: Store reusable templates for different content types and delivery channels.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier for template
- `name` (VARCHAR(200), NOT NULL): Human-readable template name
- `template_type` (ENUM: email|slack|discord|webhook, NOT NULL): Target channel type
- `content_structure` (JSONB, NOT NULL): Template structure and variable definitions
- `formatting_rules` (JSONB, NOT NULL): Channel-specific formatting requirements
- `branding_elements` (JSONB, NOT NULL): Logos, colors, and styling information
- `variable_definitions` (JSONB, NOT NULL): Available template variables and their types
- `usage_count` (INTEGER, NOT NULL, DEFAULT 0): Number of times template has been used
- `is_active` (BOOLEAN, NOT NULL, DEFAULT true): Whether template is available
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT now()): Template creation timestamp
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT now()): Last modification timestamp

**Relationships**:
- Used in content_publications for formatting

**Constraints**:
- template_type must be valid enum value
- variable_definitions must include all required variables

**Indexes**:
- template_type (for channel-specific template filtering)
- is_active (for available templates only)

---

### Publishing Analytics

**Purpose**: Store engagement and performance metrics for analysis and optimization.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier for analytics record
- `publication_id` (UUID, NOT NULL, Foreign Key → content_publications.id): Reference to publication
- `channel_type` (ENUM: email|slack|discord|webhook|rss, NOT NULL): Channel where engagement occurred
- `metric_type` (ENUM: open|click|unsubscribe|bounce|complaint, NOT NULL): Type of engagement event
- `metric_value` (DECIMAL, NOT NULL): Numeric value of the metric (count, rate, etc.)
- `user_id` (UUID, NULL, Foreign Key → users.id): User who generated the metric (NULL for anonymous)
- `metadata` (JSONB, NOT NULL): Additional context (timestamp, device, location)
- `recorded_at` (TIMESTAMP, NOT NULL, DEFAULT now()): When metric was recorded

**Relationships**:
- References content_publications.id via publication_id
- References users.id via user_id (optional)

**Constraints**:
- metric_type must be valid enum value
- metric_value must be non-negative

**Indexes**:
- publication_id (for publication-specific metrics)
- channel_type (for channel-specific analytics)
- recorded_at (for time-series analysis)
- user_id (for user-specific engagement tracking)

## Data Flow Architecture

### Publication Workflow
1. Content created → Analyzed for quality and relevance
2. Subscriber profiles queried → Personalized content selection
3. Content templates applied → Channel-specific formatting
4. Publishing channels configured → Multi-channel delivery initiated
5. Publication status tracked → Results recorded in content_publications
6. User engagement captured → Analytics recorded for optimization

### Personalization Engine
1. User preferences retrieved from subscriber_profiles
2. Content analyzed against topic_interests and personalization_data
3. Engagement history reviewed from publishing_analytics
4. Optimal delivery channels and timing determined
5. Content personalized and queued for publication

## Performance Considerations

**Query Optimization**:
- Composite indexes on frequently queried combinations (user_id + subscription_status)
- Partitioning strategy for time-series data in publishing_analytics
- Efficient JSONB queries for personalization matching

**Scalability Requirements**:
- Support 100,000+ active subscribers
- Handle 1,000+ concurrent newsletter generations
- Process 500+ real-time alerts per second
- Maintain <200ms response time for personalization queries

## Integration Points

**External Systems**:
- AWS SES for email delivery and bounce tracking
- Slack/Discord APIs for message delivery
- AI module for content quality scoring and personalization
- User management system for subscriber profile synchronization
