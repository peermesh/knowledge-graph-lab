-- Knowledge Graph Lab Database Schema
-- Comprehensive schema for all modules with optimized indexes and relationships

-- =============================================================================
-- CORE ENTITY TABLES
-- =============================================================================

-- Entities table (creators, platforms, organizations, grants, policies)
CREATE TABLE entities (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    metadata JSON NOT NULL DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    KEY idx_entities_type (type),
    KEY idx_entities_name (name),
    KEY idx_entities_created_at (created_at)
);

-- Relationships table
CREATE TABLE relationships (
    id VARCHAR(50) PRIMARY KEY,
    source_id VARCHAR(50) NOT NULL,
    target_id VARCHAR(50) NOT NULL,
    relationship_type VARCHAR(100) NOT NULL,
    metadata JSON NOT NULL DEFAULT '{}',
    confidence DECIMAL(3,2) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (source_id) REFERENCES entities(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES entities(id) ON DELETE CASCADE,
    
    -- Indexes
    KEY idx_relationships_source (source_id),
    KEY idx_relationships_target (target_id),
    KEY idx_relationships_type (relationship_type),
    KEY idx_relationships_confidence (confidence),
    KEY idx_relationships_created_at (created_at),
    
    -- Unique constraint to prevent duplicate relationships
    UNIQUE KEY uk_relationships (source_id, target_id, relationship_type)
);

-- =============================================================================
-- CONTENT MANAGEMENT TABLES
-- =============================================================================

-- Content table (articles, news, social posts)
CREATE TABLE content (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    content_text TEXT,
    metadata JSON NOT NULL DEFAULT '{}',
    source_url VARCHAR(1000),
    published_date TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quality_score DECIMAL(3,2),
    
    -- Indexes
    KEY idx_content_type (content_type),
    KEY idx_content_published_date (published_date),
    KEY idx_content_ingested_at (ingested_at),
    KEY idx_content_quality_score (quality_score),
    KEY idx_content_source_url (source_url(255)),
    FULLTEXT KEY idx_content_title_text (title, content_text)
);

-- Content entities mapping (many-to-many between content and entities)
CREATE TABLE content_entities (
    id VARCHAR(50) PRIMARY KEY,
    content_id VARCHAR(50) NOT NULL,
    entity_id VARCHAR(50) NOT NULL,
    relevance_score DECIMAL(3,2) DEFAULT 1.0,
    extraction_method VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (content_id) REFERENCES content(id) ON DELETE CASCADE,
    FOREIGN KEY (entity_id) REFERENCES entities(id) ON DELETE CASCADE,
    
    -- Indexes
    KEY idx_content_entities_content (content_id),
    KEY idx_content_entities_entity (entity_id),
    KEY idx_content_entities_relevance (relevance_score),
    
    -- Unique constraint
    UNIQUE KEY uk_content_entities (content_id, entity_id)
);

-- =============================================================================
-- USER MANAGEMENT TABLES
-- =============================================================================

-- KGL Users table (extends the basic users table)
CREATE TABLE kgl_users (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    user_type VARCHAR(50) NOT NULL,
    metadata JSON NOT NULL DEFAULT '{}',
    preferences JSON NOT NULL DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_active TIMESTAMP,
    
    -- Indexes
    KEY idx_kgl_users_email (email),
    KEY idx_kgl_users_type (user_type),
    KEY idx_kgl_users_created_at (created_at),
    KEY idx_kgl_users_last_active (last_active)
);

-- User interactions table
CREATE TABLE user_interactions (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    interaction_type VARCHAR(100) NOT NULL,
    target_type VARCHAR(50), -- 'entity', 'content', 'system'
    target_id VARCHAR(50),
    metadata JSON NOT NULL DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES kgl_users(id) ON DELETE CASCADE,
    
    -- Indexes
    KEY idx_user_interactions_user (user_id),
    KEY idx_user_interactions_type (interaction_type),
    KEY idx_user_interactions_target (target_type, target_id),
    KEY idx_user_interactions_created_at (created_at)
);

-- User interests (derived from interactions and explicit preferences)
CREATE TABLE user_interests (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    interest_topic VARCHAR(255) NOT NULL,
    interest_score DECIMAL(3,2) NOT NULL DEFAULT 0.5,
    confidence DECIMAL(3,2) NOT NULL DEFAULT 0.5,
    source VARCHAR(100) NOT NULL, -- 'explicit', 'behavioral', 'inferred'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES kgl_users(id) ON DELETE CASCADE,
    
    -- Indexes
    KEY idx_user_interests_user (user_id),
    KEY idx_user_interests_topic (interest_topic),
    KEY idx_user_interests_score (interest_score),
    KEY idx_user_interests_source (source),
    KEY idx_user_interests_updated_at (updated_at),
    
    -- Unique constraint
    UNIQUE KEY uk_user_interests (user_id, interest_topic)
);

-- =============================================================================
-- KNOWLEDGE GRAPH SPECIFIC TABLES
-- =============================================================================

-- Entity embeddings for similarity calculations
CREATE TABLE entity_embeddings (
    entity_id VARCHAR(50) PRIMARY KEY,
    embedding_vector JSON NOT NULL,
    embedding_model VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (entity_id) REFERENCES entities(id) ON DELETE CASCADE,
    
    -- Indexes
    KEY idx_entity_embeddings_model (embedding_model),
    KEY idx_entity_embeddings_created_at (created_at)
);

-- Research queue for AI-driven research tasks
CREATE TABLE research_queue (
    id VARCHAR(50) PRIMARY KEY,
    query TEXT NOT NULL,
    priority_score DECIMAL(3,2) NOT NULL DEFAULT 0.5,
    status VARCHAR(50) NOT NULL DEFAULT 'queued',
    user_id VARCHAR(50),
    context JSON DEFAULT '{}',
    assigned_at TIMESTAMP,
    completed_at TIMESTAMP,
    results JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES kgl_users(id) ON DELETE SET NULL,
    
    -- Indexes
    KEY idx_research_queue_priority (priority_score DESC),
    KEY idx_research_queue_status (status),
    KEY idx_research_queue_user (user_id),
    KEY idx_research_queue_created_at (created_at),
    KEY idx_research_queue_assigned_at (assigned_at),
    FULLTEXT KEY idx_research_queue_query (query)
);

-- Knowledge gaps tracking
CREATE TABLE knowledge_gaps (
    id VARCHAR(50) PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    description TEXT,
    gap_score DECIMAL(3,2) NOT NULL,
    urgency DECIMAL(3,2) NOT NULL,
    user_demand INTEGER DEFAULT 0,
    identified_by VARCHAR(50), -- 'system', 'user', 'research'
    metadata JSON DEFAULT '{}',
    status VARCHAR(50) DEFAULT 'identified',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    KEY idx_knowledge_gaps_topic (topic),
    KEY idx_knowledge_gaps_score (gap_score DESC),
    KEY idx_knowledge_gaps_urgency (urgency DESC),
    KEY idx_knowledge_gaps_demand (user_demand DESC),
    KEY idx_knowledge_gaps_status (status),
    KEY idx_knowledge_gaps_created_at (created_at)
);

-- =============================================================================
-- PERSONALIZATION AND CONTENT SYNTHESIS TABLES
-- =============================================================================

-- Generated digests for users
CREATE TABLE user_digests (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    digest_content JSON NOT NULL,
    generation_method VARCHAR(100) NOT NULL,
    relevance_score DECIMAL(3,2),
    delivered_channels JSON DEFAULT '[]',
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP,
    feedback_score INTEGER, -- 1-5 rating
    
    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES kgl_users(id) ON DELETE CASCADE,
    
    -- Indexes
    KEY idx_user_digests_user (user_id),
    KEY idx_user_digests_generated_at (generated_at),
    KEY idx_user_digests_delivered_at (delivered_at),
    KEY idx_user_digests_relevance (relevance_score),
    KEY idx_user_digests_feedback (feedback_score)
);

-- Content recommendations for users
CREATE TABLE content_recommendations (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    content_id VARCHAR(50) NOT NULL,
    recommendation_score DECIMAL(3,2) NOT NULL,
    reasoning TEXT,
    recommendation_type VARCHAR(50), -- 'trending', 'personalized', 'similar'
    viewed BOOLEAN DEFAULT FALSE,
    clicked BOOLEAN DEFAULT FALSE,
    feedback_rating INTEGER, -- 1-5 rating
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    viewed_at TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES kgl_users(id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES content(id) ON DELETE CASCADE,
    
    -- Indexes
    KEY idx_content_recommendations_user (user_id),
    KEY idx_content_recommendations_content (content_id),
    KEY idx_content_recommendations_score (recommendation_score DESC),
    KEY idx_content_recommendations_type (recommendation_type),
    KEY idx_content_recommendations_viewed (viewed),
    KEY idx_content_recommendations_created_at (created_at),
    
    -- Unique constraint
    UNIQUE KEY uk_content_recommendations (user_id, content_id, recommendation_type)
);

-- =============================================================================
-- INGESTION AND PROCESSING TABLES
-- =============================================================================

-- Ingestion sources configuration
CREATE TABLE ingestion_sources (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL, -- 'rss', 'web', 'api', 'social'
    source_url VARCHAR(1000) NOT NULL,
    config JSON DEFAULT '{}',
    active BOOLEAN DEFAULT TRUE,
    last_processed TIMESTAMP,
    next_scheduled TIMESTAMP,
    processing_frequency INTEGER DEFAULT 3600, -- seconds
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    KEY idx_ingestion_sources_type (source_type),
    KEY idx_ingestion_sources_active (active),
    KEY idx_ingestion_sources_next_scheduled (next_scheduled),
    KEY idx_ingestion_sources_last_processed (last_processed)
);

-- Processing jobs tracking
CREATE TABLE processing_jobs (
    id VARCHAR(50) PRIMARY KEY,
    job_type VARCHAR(50) NOT NULL, -- 'ingestion', 'entity_extraction', 'personalization'
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    source_id VARCHAR(50),
    target_id VARCHAR(50),
    config JSON DEFAULT '{}',
    progress DECIMAL(5,2) DEFAULT 0.0,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (source_id) REFERENCES ingestion_sources(id) ON DELETE SET NULL,
    
    -- Indexes
    KEY idx_processing_jobs_type (job_type),
    KEY idx_processing_jobs_status (status),
    KEY idx_processing_jobs_source (source_id),
    KEY idx_processing_jobs_created_at (created_at),
    KEY idx_processing_jobs_started_at (started_at)
);

-- =============================================================================
-- ANALYTICS AND MONITORING TABLES
-- =============================================================================

-- System metrics
CREATE TABLE system_metrics (
    id VARCHAR(50) PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,4) NOT NULL,
    metric_unit VARCHAR(50),
    component VARCHAR(50) NOT NULL, -- 'module_1', 'module_2', etc.
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    KEY idx_system_metrics_name (metric_name),
    KEY idx_system_metrics_component (component),
    KEY idx_system_metrics_recorded_at (recorded_at),
    KEY idx_system_metrics_composite (component, metric_name, recorded_at)
);

-- User engagement metrics
CREATE TABLE engagement_metrics (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    metric_type VARCHAR(100) NOT NULL, -- 'page_view', 'content_click', 'digest_open'
    metric_value DECIMAL(10,4) DEFAULT 1.0,
    context JSON DEFAULT '{}',
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES kgl_users(id) ON DELETE CASCADE,
    
    -- Indexes
    KEY idx_engagement_metrics_user (user_id),
    KEY idx_engagement_metrics_type (metric_type),
    KEY idx_engagement_metrics_recorded_at (recorded_at),
    KEY idx_engagement_metrics_composite (user_id, metric_type, recorded_at)
);

-- =============================================================================
-- VIEWS FOR COMMON QUERIES
-- =============================================================================

-- View for entity relationships with names
CREATE VIEW entity_relationships_view AS
SELECT 
    r.id,
    r.source_id,
    se.name as source_name,
    se.type as source_type,
    r.target_id,
    te.name as target_name,
    te.type as target_type,
    r.relationship_type,
    r.confidence,
    r.metadata,
    r.created_at
FROM relationships r
JOIN entities se ON r.source_id = se.id
JOIN entities te ON r.target_id = te.id;

-- View for user content recommendations with details
CREATE VIEW user_recommendations_view AS
SELECT 
    cr.id,
    cr.user_id,
    u.name as user_name,
    cr.content_id,
    c.title as content_title,
    c.content_type,
    cr.recommendation_score,
    cr.reasoning,
    cr.recommendation_type,
    cr.viewed,
    cr.clicked,
    cr.created_at
FROM content_recommendations cr
JOIN kgl_users u ON cr.user_id = u.id
JOIN content c ON cr.content_id = c.id;

-- View for knowledge graph statistics
CREATE VIEW knowledge_graph_stats AS
SELECT 
    'entities' as metric_type,
    type as metric_category,
    COUNT(*) as metric_value
FROM entities 
GROUP BY type
UNION ALL
SELECT 
    'relationships' as metric_type,
    relationship_type as metric_category,
    COUNT(*) as metric_value
FROM relationships 
GROUP BY relationship_type
UNION ALL
SELECT 
    'content' as metric_type,
    content_type as metric_category,
    COUNT(*) as metric_value
FROM content 
GROUP BY content_type;

-- =============================================================================
-- TABLE COMMENTS FOR DOCUMENTATION
-- =============================================================================

ALTER TABLE entities COMMENT = 'Core entities: creators, platforms, organizations, grants, policies';
ALTER TABLE relationships COMMENT = 'Relationships between entities with confidence scores';
ALTER TABLE content COMMENT = 'All content items: articles, news, social posts';
ALTER TABLE content_entities COMMENT = 'Mapping between content and mentioned entities';
ALTER TABLE kgl_users COMMENT = 'KGL-specific user profiles and preferences';
ALTER TABLE user_interactions COMMENT = 'Tracking of all user interactions';
ALTER TABLE user_interests COMMENT = 'Derived and explicit user interests';
ALTER TABLE entity_embeddings COMMENT = 'Vector embeddings for entity similarity';
ALTER TABLE research_queue COMMENT = 'Queue for AI-driven research tasks';
ALTER TABLE knowledge_gaps COMMENT = 'Identified gaps in knowledge coverage';
ALTER TABLE user_digests COMMENT = 'Generated personalized content digests';
ALTER TABLE content_recommendations COMMENT = 'Content recommendations for users';
ALTER TABLE ingestion_sources COMMENT = 'Configuration for content ingestion sources';
ALTER TABLE processing_jobs COMMENT = 'Tracking of background processing jobs';
ALTER TABLE system_metrics COMMENT = 'System performance and health metrics';
ALTER TABLE engagement_metrics COMMENT = 'User engagement tracking';