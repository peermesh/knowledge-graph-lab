"""Initial database schema for Backend Architecture Module.

This migration creates all the core tables for user management,
entity storage, authentication, and API monitoring.
"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision = '20250123_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create initial database schema."""

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('last_login', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_users_email_role', 'email', 'role'),
        sa.Index('idx_users_last_login', 'last_login'),
        sa.CheckConstraint(
            "role IN ('user', 'admin', 'moderator', 'researcher')",
            name='check_user_role'
        ),
        sa.CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$'",
            name='check_email_format'
        )
    )

    # Create entities table
    op.create_table(
        'entities',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('type', sa.String(100), nullable=False),
        sa.Column('confidence', sa.DECIMAL(3, 2), nullable=False),
        sa.Column('source', sa.Text(), nullable=False),
        sa.Column('source_type', sa.String(50), nullable=False),
        sa.Column('source_document_id', sa.String(), nullable=True),
        sa.Column('extraction_method', sa.String(50), nullable=False),
        sa.Column('positions', sa.JSON(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('vector_embedding', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_entities_type_confidence', 'type', 'confidence'),
        sa.Index('idx_entities_source', 'source'),
        sa.Index('idx_entities_created_at', 'created_at'),
        sa.CheckConstraint(
            'confidence >= 0.00 AND confidence <= 1.00',
            name='check_confidence_range'
        ),
        sa.CheckConstraint(
            "type IN ('organization', 'person', 'funding_amount', 'date', 'location', 'concept', 'event')",
            name='check_entity_type'
        )
    )

    # Create entity_relationships table
    op.create_table(
        'entity_relationships',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('source_entity_id', sa.String(), nullable=False),
        sa.Column('target_entity_id', sa.String(), nullable=False),
        sa.Column('relationship_type', sa.String(50), nullable=False),
        sa.Column('confidence', sa.DECIMAL(3, 2), nullable=False),
        sa.Column('strength', sa.DECIMAL(3, 2), nullable=True),
        sa.Column('evidence', sa.Text(), nullable=False),
        sa.Column('temporal_context', sa.JSON(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_relationships_source_target', 'source_entity_id', 'target_entity_id'),
        sa.Index('idx_relationships_type_confidence', 'relationship_type', 'confidence'),
        sa.CheckConstraint(
            'confidence >= 0.00 AND confidence <= 1.00',
            name='check_relationship_confidence_range'
        ),
        sa.CheckConstraint(
            "relationship_type IN ('fund', 'partner', 'acquire', 'compete', 'collaborate', 'mention')",
            name='check_relationship_type'
        ),
        sa.CheckConstraint(
            'source_entity_id != target_entity_id',
            name='check_no_self_relationship'
        )
    )

    # Create user_sessions table
    op.create_table(
        'user_sessions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('session_id', sa.String(255), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=False),
        sa.Column('refresh_token', sa.Text(), nullable=False),
        sa.Column('ip_address', sa.String(45), nullable=False),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('device_info', sa.Text(), nullable=True),
        sa.Column('expires_at', sa.Text(), nullable=False),
        sa.Column('refresh_expires_at', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_sessions_user_active', 'user_id', 'is_active'),
        sa.Index('idx_sessions_expires_at', 'expires_at'),
        sa.CheckConstraint(
            'is_active IN (true, false)',
            name='check_session_active'
        ),
        sa.UniqueConstraint('session_id', name='unique_session_id')
    )

    # Create api_requests table
    op.create_table(
        'api_requests',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('endpoint', sa.String(500), nullable=False),
        sa.Column('method', sa.String(10), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=False),
        sa.Column('response_time_ms', sa.Integer(), nullable=False),
        sa.Column('request_size_bytes', sa.Integer(), nullable=False),
        sa.Column('response_size_bytes', sa.Integer(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=False),  # Using String for INET compatibility
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_api_requests_endpoint_method', 'endpoint', 'method'),
        sa.Index('idx_api_requests_user_timestamp', 'user_id', 'created_at'),
        sa.Index('idx_api_requests_status_code', 'status_code'),
        sa.CheckConstraint(
            'status_code >= 100 AND status_code <= 599',
            name='check_status_code_range'
        ),
        sa.CheckConstraint(
            'response_time_ms >= 0',
            name='check_response_time_positive'
        ),
        sa.CheckConstraint(
            "method IN ('GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD')",
            name='check_http_method'
        )
    )

    # Add foreign key constraints
    op.create_foreign_key(
        'fk_sessions_user',
        'user_sessions', 'users',
        ['user_id'], ['id']
    )
    op.create_foreign_key(
        'fk_api_requests_user',
        'api_requests', 'users',
        ['user_id'], ['id']
    )
    op.create_foreign_key(
        'fk_relationships_source_entity',
        'entity_relationships', 'entities',
        ['source_entity_id'], ['id']
    )
    op.create_foreign_key(
        'fk_relationships_target_entity',
        'entity_relationships', 'entities',
        ['target_entity_id'], ['id']
    )


def downgrade():
    """Remove initial database schema."""

    # Drop tables in reverse order to handle foreign key constraints
    op.drop_table('api_requests')
    op.drop_table('user_sessions')
    op.drop_table('entity_relationships')
    op.drop_table('entities')
    op.drop_table('users')
