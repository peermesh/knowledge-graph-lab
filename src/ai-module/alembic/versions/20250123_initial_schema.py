"""Initial database schema for AI Development Module.

This migration creates all the core tables for entity extraction,
relationship management, and knowledge graph operations.
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
        sa.CheckConstraint('confidence >= 0.00 AND confidence <= 1.00', name='check_confidence_range'),
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
        sa.CheckConstraint('confidence >= 0.00 AND confidence <= 1.00', name='check_relationship_confidence_range'),
        sa.CheckConstraint(
            "relationship_type IN ('fund', 'partner', 'acquire', 'compete', 'collaborate', 'mention')",
            name='check_relationship_type'
        ),
        sa.CheckConstraint('source_entity_id != target_entity_id', name='check_no_self_relationship')
    )

    # Create knowledge_graph_nodes table
    op.create_table(
        'knowledge_graph_nodes',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('entity_id', sa.String(), nullable=False),
        sa.Column('node_type', sa.String(50), nullable=False),
        sa.Column('properties', sa.JSON(), nullable=False),
        sa.Column('vector_embedding', sa.JSON(), nullable=True),
        sa.Column('degree', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_nodes_type_degree', 'node_type', 'degree'),
        sa.CheckConstraint(
            "node_type IN ('entity', 'concept', 'event')",
            name='check_node_type'
        ),
        sa.UniqueConstraint('entity_id', name='unique_entity_node')
    )

    # Create knowledge_graph_edges table
    op.create_table(
        'knowledge_graph_edges',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('source_node_id', sa.String(), nullable=False),
        sa.Column('target_node_id', sa.String(), nullable=False),
        sa.Column('relationship_type', sa.String(50), nullable=False),
        sa.Column('properties', sa.JSON(), nullable=True),
        sa.Column('confidence', sa.DECIMAL(3, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_edges_source_target', 'source_node_id', 'target_node_id'),
        sa.Index('idx_edges_type_confidence', 'relationship_type', 'confidence'),
        sa.CheckConstraint('confidence >= 0.00 AND confidence <= 1.00', name='check_edge_confidence_range'),
        sa.CheckConstraint('source_node_id != target_node_id', name='check_no_self_edge')
    )

    # Create document_processing_jobs table
    op.create_table(
        'document_processing_jobs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('document_id', sa.String(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('priority', sa.String(10), nullable=False),
        sa.Column('extraction_config', sa.JSON(), nullable=False),
        sa.Column('entities_extracted', sa.Integer(), nullable=False),
        sa.Column('relationships_found', sa.Integer(), nullable=False),
        sa.Column('processing_time_seconds', sa.DECIMAL(8, 2), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=False),
        sa.Column('started_at', sa.Text(), nullable=True),
        sa.Column('completed_at', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_jobs_status_priority', 'status', 'priority'),
        sa.Index('idx_jobs_created_at', 'created_at'),
        sa.CheckConstraint(
            "status IN ('pending', 'processing', 'completed', 'failed', 'cancelled')",
            name='check_job_status'
        ),
        sa.CheckConstraint(
            "priority IN ('high', 'normal', 'low')",
            name='check_job_priority'
        ),
        sa.CheckConstraint('retry_count >= 0', name='check_retry_count')
    )

    # Create processing_quality_metrics table
    op.create_table(
        'processing_quality_metrics',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('metric_type', sa.String(50), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=True),
        sa.Column('value', sa.DECIMAL(10, 4), nullable=False),
        sa.Column('sample_size', sa.Integer(), nullable=True),
        sa.Column('confidence_interval', sa.DECIMAL(5, 4), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_metrics_job_type', 'job_id', 'metric_type'),
        sa.Index('idx_metrics_entity_type', 'entity_type', 'metric_type'),
        sa.CheckConstraint(
            "metric_type IN ('accuracy', 'precision', 'recall', 'latency', 'cost', 'throughput')",
            name='check_metric_type'
        ),
        sa.CheckConstraint('value >= 0', name='check_metric_value_positive')
    )

    # Add foreign key constraints
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
    op.create_foreign_key(
        'fk_nodes_entity',
        'knowledge_graph_nodes', 'entities',
        ['entity_id'], ['id']
    )
    op.create_foreign_key(
        'fk_edges_source_node',
        'knowledge_graph_edges', 'knowledge_graph_nodes',
        ['source_node_id'], ['id']
    )
    op.create_foreign_key(
        'fk_edges_target_node',
        'knowledge_graph_edges', 'knowledge_graph_nodes',
        ['target_node_id'], ['id']
    )
    op.create_foreign_key(
        'fk_jobs_metrics',
        'processing_quality_metrics', 'document_processing_jobs',
        ['job_id'], ['id']
    )


def downgrade():
    """Remove initial database schema."""

    # Drop tables in reverse order to handle foreign key constraints
    op.drop_table('processing_quality_metrics')
    op.drop_table('document_processing_jobs')
    op.drop_table('knowledge_graph_edges')
    op.drop_table('knowledge_graph_nodes')
    op.drop_table('entity_relationships')
    op.drop_table('entities')
