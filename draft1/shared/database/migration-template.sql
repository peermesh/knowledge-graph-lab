-- Migration Template for Knowledge Graph Lab
-- Use this template for database schema changes

-- Migration: [MIGRATION_NAME]
-- Date: [YYYY-MM-DD]
-- Description: [Brief description of changes]
-- Author: [Your name]

-- =============================================================================
-- MIGRATION UP (Apply changes)
-- =============================================================================

-- Example: Add new column to entities table
-- ALTER TABLE entities ADD COLUMN new_field VARCHAR(255) AFTER name;

-- Example: Create new table
-- CREATE TABLE new_table (
--     id VARCHAR(50) PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Example: Add index
-- CREATE INDEX idx_new_table_name ON new_table(name);

-- Example: Insert default data
-- INSERT INTO new_table (id, name) VALUES ('default_001', 'Default Entry');

-- =============================================================================
-- MIGRATION DOWN (Rollback changes) 
-- =============================================================================

-- Example: Remove column
-- ALTER TABLE entities DROP COLUMN new_field;

-- Example: Drop table
-- DROP TABLE IF EXISTS new_table;

-- Example: Remove index
-- DROP INDEX IF EXISTS idx_new_table_name ON new_table;

-- =============================================================================
-- MIGRATION METADATA
-- =============================================================================

-- Record this migration in the migration history
INSERT INTO system_metrics (id, metric_name, metric_value, metric_unit, component, recorded_at)
VALUES (
    CONCAT('migration_', UNIX_TIMESTAMP()),
    'migration_applied',
    1.0,
    'count',
    'database',
    CURRENT_TIMESTAMP
) ON DUPLICATE KEY UPDATE 
recorded_at = CURRENT_TIMESTAMP;

-- Add migration record (if you have a migrations table)
-- INSERT INTO migrations (name, applied_at) VALUES ('[MIGRATION_NAME]', CURRENT_TIMESTAMP);

-- =============================================================================
-- NOTES AND CONSIDERATIONS
-- =============================================================================

-- 1. Always test migrations on a development database first
-- 2. Create backups before applying migrations to production
-- 3. Consider foreign key constraints when dropping/modifying tables
-- 4. Update relevant application code before/after migration
-- 5. Document any manual steps required
-- 6. Test rollback procedures

-- Manual steps required after migration:
-- - [List any manual steps needed]
-- - [Update configuration files]
-- - [Restart services]
-- - [Run data migration scripts]

-- Rollback considerations:
-- - [Note any data that will be lost on rollback]
-- - [Dependencies that must be addressed first]

-- Performance impact:
-- - [Expected duration of migration]
-- - [Tables that will be locked]
-- - [Recommended maintenance window]