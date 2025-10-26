# Data Model: Backend Architecture

**Feature**: Backend Architecture | **Date**: 2025-10-26
**Purpose**: Define database schema and entity relationships for the Knowledge Graph Lab System backend

## Overview

The backend architecture uses PostgreSQL 15+ as the primary data store with comprehensive schema design supporting user authentication, knowledge graph entities, relationships, and operational monitoring. All data models implement user_id isolation for security and proper audit trails for compliance.

## Core Entity Tables

### Users Table

**Purpose**: Manages authentication and authorization for all system users and API access

**Schema**:
- `id` (UUID, PRIMARY KEY) - Unique identifier for each user
- `email` (VARCHAR(255), UNIQUE, NOT NULL) - User's email address for authentication
- `password_hash` (VARCHAR(255), NOT NULL) - Bcrypt-hashed password for secure authentication
- `first_name` (VARCHAR(100), NOT NULL) - User's first name
- `last_name` (VARCHAR(100), NOT NULL) - User's last name
- `role` (VARCHAR(50), NOT NULL, DEFAULT 'user') - User role for authorization (user, admin, moderator)
- `is_active` (BOOLEAN, NOT NULL, DEFAULT true) - Account activation status
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT now()) - Account creation timestamp
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT now()) - Last account update timestamp
- `last_login` (TIMESTAMP, NULL) - Last successful login timestamp

**Indexes**:
- `email` (UNIQUE) - Fast authentication lookups
- `role` - Role-based filtering
- `created_at` - User analytics and reporting
- `last_login` - Active user identification

**Constraints**:
- Email must match valid email pattern (CHECK constraint)
- Role must be one of: 'user', 'admin', 'moderator'
- Password hash cannot be empty

**Constitutional Compliance**: Implements Security & Authentication principle with secure password hashing and role-based access control.

### Entities Table

**Purpose**: Stores extracted entities from AI processing for knowledge graph construction

**Schema**:
- `id` (UUID, PRIMARY KEY) - Unique identifier for each entity
- `name` (TEXT, NOT NULL) - The extracted entity name or text
- `type` (VARCHAR(100), NOT NULL) - Entity type (person, organization, location, concept, etc.)
- `confidence` (DECIMAL(3,2), NOT NULL) - AI extraction confidence score (0.00-1.00)
- `source` (TEXT, NOT NULL) - Original source document/content identifier
- `source_type` (VARCHAR(50), NOT NULL) - Type of source (article, document, web_page, etc.)
- `metadata` (JSONB, NULL) - Additional entity properties and attributes
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT now()) - Entity extraction timestamp
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT now()) - Last entity update timestamp
- `created_by` (UUID, NOT NULL, FOREIGN KEY → users.id) - References users.id for audit trail
- `is_active` (BOOLEAN, NOT NULL, DEFAULT true) - Entity active status

**Indexes**:
- `type` - Entity type filtering and queries
- `source` - Source-based entity retrieval
- `confidence` - Confidence-based filtering
- `created_at` - Temporal entity queries
- `name` (GIN) - Full-text search capabilities
- `(type, confidence)` - Composite index for type-confidence filtering

**Constraints**:
- Confidence score must be between 0.00 and 1.00
- Entity type must be one of predefined valid types
- Name cannot be empty or null

**Constitutional Compliance**: Implements Database Design Excellence with proper indexing and user_id isolation through created_by field.

### Entity Relationships Table

**Purpose**: Defines relationships between entities in the knowledge graph

**Schema**:
- `id` (UUID, PRIMARY KEY) - Unique identifier for each relationship
- `source_entity_id` (UUID, NOT NULL, FOREIGN KEY → entities.id) - References entities.id for relationship source
- `target_entity_id` (UUID, NOT NULL, FOREIGN KEY → entities.id) - References entities.id for relationship target
- `relationship_type` (VARCHAR(100), NOT NULL) - Type of relationship (works_for, located_in, related_to, etc.)
- `confidence` (DECIMAL(3,2), NOT NULL) - AI extraction confidence for this relationship
- `metadata` (JSONB, NULL) - Additional relationship properties and context
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT now()) - Relationship creation timestamp
- `created_by` (UUID, NOT NULL, FOREIGN KEY → users.id) - References users.id for audit trail
- `is_active` (BOOLEAN, NOT NULL, DEFAULT true) - Relationship active status

**Indexes**:
- `source_entity_id` - Source-based relationship queries
- `target_entity_id` - Target-based relationship queries
- `relationship_type` - Relationship type filtering
- `confidence` - Confidence-based filtering
- `(source_entity_id, relationship_type)` - Source-relationship queries
- `(target_entity_id, relationship_type)` - Target-relationship queries

**Constraints**:
- Source and target entity IDs must be different (no self-relationships)
- Confidence score must be between 0.00 and 1.00
- Relationship type must be one of predefined valid types

**Constitutional Compliance**: Implements Database Design Excellence with proper foreign key relationships and user_id isolation.

## Operational Tables

### API Access Logs Table

**Purpose**: Tracks API usage patterns, performance monitoring, and security auditing

**Schema**:
- `id` (UUID, PRIMARY KEY) - Unique identifier for each API request
- `user_id` (UUID, NULL, FOREIGN KEY → users.id) - References users.id (null for unauthenticated requests)
- `endpoint` (VARCHAR(500), NOT NULL) - API endpoint path that was accessed
- `method` (VARCHAR(10), NOT NULL) - HTTP method (GET, POST, PUT, DELETE, etc.)
- `status_code` (INTEGER, NOT NULL) - HTTP response status code
- `response_time_ms` (INTEGER, NOT NULL) - Response time in milliseconds
- `request_size_bytes` (INTEGER, NOT NULL) - Size of request payload in bytes
- `response_size_bytes` (INTEGER, NOT NULL) - Size of response payload in bytes
- `ip_address` (INET, NOT NULL) - Client IP address for security tracking
- `user_agent` (TEXT, NULL) - Client user agent string
- `timestamp` (TIMESTAMP, NOT NULL, DEFAULT now()) - Request timestamp
- `error_message` (TEXT, NULL) - Error message if request failed

**Indexes**:
- `endpoint` - Endpoint-based analytics
- `status_code` - Error rate monitoring
- `user_id` - User activity tracking
- `timestamp` - Time-based analytics and retention policies
- `ip_address` - Security monitoring and threat detection
- `(endpoint, timestamp)` - Endpoint performance trends
- `(status_code, timestamp)` - Error rate trends

**Constraints**:
- Response time must be positive integer
- Status code must be valid HTTP status code (100-599)
- Request and response sizes must be non-negative

**Constitutional Compliance**: Implements Observability & Monitoring principle with comprehensive request tracking and performance metrics.

### Database Schemas Table

**Purpose**: Version control for database schema changes and rollback capabilities

**Schema**:
- `id` (UUID, PRIMARY KEY) - Unique identifier for each schema version
- `version` (VARCHAR(50), NOT NULL, UNIQUE) - Schema version identifier (e.g., "1.0.0", "1.1.0")
- `name` (VARCHAR(255), NOT NULL) - Descriptive name for the schema version
- `description` (TEXT, NOT NULL) - Description of changes in this version
- `ddl_statements` (JSONB, NOT NULL) - Array of DDL statements for this version
- `rollback_statements` (JSONB, NOT NULL) - Array of DDL statements to rollback this version
- `migration_script` (TEXT, NOT NULL) - Complete migration script for this version
- `checksum` (VARCHAR(128), NOT NULL) - SHA-256 hash of migration script for integrity
- `applied_at` (TIMESTAMP, NOT NULL, DEFAULT now()) - When this version was applied
- `applied_by` (UUID, NOT NULL, FOREIGN KEY → users.id) - References users.id for audit trail
- `is_rollback` (BOOLEAN, NOT NULL, DEFAULT false) - Whether this is a rollback operation

**Indexes**:
- `version` (UNIQUE) - Version lookup
- `applied_at` - Migration history queries
- `applied_by` - User migration tracking
- `is_rollback` - Rollback operation filtering

**Constraints**:
- Version must follow semantic versioning pattern (e.g., "1.2.3")
- Checksum must be valid SHA-256 hash
- DDL and rollback statements cannot be empty arrays

**Constitutional Compliance**: Implements Database Design Excellence with version-controlled schema management and audit trails.

### Module Integrations Table

**Purpose**: Tracks integration status and configuration between Backend and other modules

**Schema**:
- `id` (UUID, PRIMARY KEY) - Unique identifier for each integration
- `module_name` (VARCHAR(100), NOT NULL) - Name of the integrated module (ai, frontend, publishing)
- `integration_type` (VARCHAR(100), NOT NULL) - Type of integration (api, websocket, message_queue)
- `status` (VARCHAR(50), NOT NULL) - Current integration status (active, inactive, error)
- `configuration` (JSONB, NOT NULL) - Integration configuration parameters
- `last_health_check` (TIMESTAMP, NOT NULL, DEFAULT now()) - Last health check timestamp
- `health_status` (VARCHAR(50), NOT NULL, DEFAULT 'unknown') - Health check result
- `error_message` (TEXT, NULL) - Last error message if integration failed
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT now()) - Integration creation timestamp
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT now()) - Last integration update

**Indexes**:
- `module_name` - Module-specific integration queries
- `status` - Active integration filtering
- `last_health_check` - Health check monitoring
- `integration_type` - Integration type filtering
- `(module_name, integration_type)` - Specific integration lookups

**Constraints**:
- Module name must be one of predefined valid modules
- Integration type must be one of predefined valid types
- Status must be one of predefined valid statuses

**Constitutional Compliance**: Implements Infrastructure as Code principle with comprehensive integration tracking and monitoring.

## Entity Relationships

### User → Entities (One-to-Many)
- **Relationship**: A user can create many entities
- **Foreign Key**: `entities.created_by` → `users.id`
- **Purpose**: Audit trail for entity creation
- **Security**: Enforces user data isolation

### User → Entity Relationships (One-to-Many)
- **Relationship**: A user can create many entity relationships
- **Foreign Key**: `entity_relationships.created_by` → `users.id`
- **Purpose**: Audit trail for relationship creation
- **Security**: Enforces user data isolation

### User → API Access Logs (One-to-Many)
- **Relationship**: A user can have many API access logs
- **Foreign Key**: `api_access_logs.user_id` → `users.id` (nullable)
- **Purpose**: Track user API activity
- **Security**: User activity monitoring

### User → Database Schemas (One-to-Many)
- **Relationship**: A user can apply many database schema changes
- **Foreign Key**: `database_schemas.applied_by` → `users.id`
- **Purpose**: Audit trail for schema changes
- **Security**: Track who made database changes

### Entity → Entity Relationships (One-to-Many Bidirectional)
- **Relationship**: An entity can be the source of many relationships
- **Foreign Key**: `entity_relationships.source_entity_id` → `entities.id`
- **Purpose**: Knowledge graph navigation from source to targets

- **Relationship**: An entity can be the target of many relationships
- **Foreign Key**: `entity_relationships.target_entity_id` → `entities.id`
- **Purpose**: Knowledge graph navigation from targets to sources

## Data Flow

### User Registration and Authentication
1. User submits registration data
2. System creates user record with hashed password
3. User logs in with email/password
4. System validates credentials and issues JWT tokens
5. All subsequent requests include user_id for data isolation

### Entity Extraction and Storage
1. AI module submits content for processing
2. System creates entity records with confidence scores
3. System establishes relationships between entities
4. All operations tracked with user_id for audit and isolation

### Knowledge Graph Queries
1. Frontend requests entity data with user context
2. System filters results by user_id for security
3. System traverses relationships for graph navigation
4. System logs all API access for monitoring

## Security Considerations

### Data Isolation
- All user data filtered by `user_id` at database level
- Entity creation requires valid user authentication
- API access logs track user activity for security monitoring
- Database-level constraints prevent unauthorized data access

### Audit Trails
- All entity and relationship creation tracked with `created_by`
- Database schema changes logged with `applied_by`
- API access comprehensively logged for security analysis
- Timestamp fields on all records for temporal analysis

### Performance Optimization
- Strategic indexes on frequently queried fields
- Composite indexes for common query patterns
- GIN indexes for JSONB and full-text search
- Connection pooling for high-concurrency scenarios

## Migration Strategy

### Initial Schema
- Create all core tables with proper constraints
- Establish indexes for optimal query performance
- Set up foreign key relationships with cascade options
- Configure audit triggers for timestamp management

### Version Control
- Use Alembic for migration management
- Each schema change gets version number and description
- Rollback scripts maintained for all migrations
- Checksum validation for migration integrity

### Zero-Downtime Deployment
- Blue-green deployment strategy for schema changes
- Migration scripts designed for minimal locking
- Health checks validate schema state after migrations
- Rollback procedures tested before production deployment

## Integration Points

### AI Module
- Submits content for entity extraction
- Retrieves processed entities and relationships
- Provides confidence scores and metadata
- Handles batch processing and error recovery

### Frontend Module
- Requests entity data with user filtering
- Navigates knowledge graph relationships
- Receives real-time updates via WebSocket
- Handles authentication token refresh

### Publishing Module
- Stores published content and metadata
- Tracks user engagement and interactions
- Provides content filtering and search
- Manages publishing workflow and status

This data model provides a solid foundation for the Knowledge Graph Lab System while maintaining constitutional compliance for security, performance, and maintainability.
