"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2025-10-20

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Note: pgvector extension not available in this PostgreSQL instance
    # Using regular ARRAY types instead of vector types
    
    # Create extracted_entities table
    op.create_table('extracted_entities',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('text', sa.String(length=500), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('confidence', sa.DECIMAL(precision=3, scale=2), nullable=False),
        sa.Column('source_document_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('extraction_method', sa.String(length=50), nullable=False),
        sa.Column('positions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('entity_metadata', postgresql.JSONB(astext_type=sa.Text())),
        sa.Column('vector_embedding', postgresql.ARRAY(sa.Float()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint('confidence >= 0.00 AND confidence <= 1.00', name='check_confidence_range'),
        sa.CheckConstraint("entity_type IN ('organization', 'person', 'funding_amount', 'date', 'location')", name='check_entity_type'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_extracted_entities_text', 'extracted_entities', ['text'])
    op.create_index('ix_extracted_entities_entity_type', 'extracted_entities', ['entity_type'])
    op.create_index('ix_extracted_entities_confidence', 'extracted_entities', ['confidence'])
    op.create_index('ix_extracted_entities_source_document_id', 'extracted_entities', ['source_document_id'])
    op.create_index('ix_extracted_entities_created_at', 'extracted_entities', ['created_at'])
    
    # Create entity_relationships table
    op.create_table('entity_relationships',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('source_entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('target_entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('relationship_type', sa.String(length=50), nullable=False),
        sa.Column('confidence', sa.DECIMAL(precision=3, scale=2), nullable=False),
        sa.Column('strength', sa.DECIMAL(precision=3, scale=2)),
        sa.Column('evidence', sa.TEXT()),
        sa.Column('temporal_context', postgresql.JSONB(astext_type=sa.Text())),
        sa.Column('relationship_metadata', postgresql.JSONB(astext_type=sa.Text())),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint('confidence >= 0.00 AND confidence <= 1.00', name='check_relationship_confidence_range'),
        sa.CheckConstraint('strength IS NULL OR (strength >= 0.00 AND strength <= 1.00)', name='check_strength_range'),
        sa.CheckConstraint('source_entity_id != target_entity_id', name='check_no_self_relationships'),
        sa.CheckConstraint("relationship_type IN ('fund', 'partner', 'acquire', 'compete', 'collaborate', 'mention')", name='check_relationship_type'),
        sa.ForeignKeyConstraint(['source_entity_id'], ['extracted_entities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_entity_id'], ['extracted_entities.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_entity_relationships_source_entity_id', 'entity_relationships', ['source_entity_id'])
    op.create_index('ix_entity_relationships_target_entity_id', 'entity_relationships', ['target_entity_id'])
    op.create_index('ix_entity_relationships_relationship_type', 'entity_relationships', ['relationship_type'])
    op.create_index('ix_entity_relationships_confidence', 'entity_relationships', ['confidence'])
    
    # Create knowledge_graph_nodes table
    op.create_table('knowledge_graph_nodes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('node_type', sa.String(length=50), nullable=False),
        sa.Column('properties', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('vector_embedding', postgresql.ARRAY(sa.Float()), nullable=False),
        sa.Column('degree', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint("node_type IN ('entity', 'concept', 'event')", name='check_node_type'),
        sa.CheckConstraint('degree >= 0', name='check_non_negative_degree'),
        sa.ForeignKeyConstraint(['entity_id'], ['extracted_entities.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_knowledge_graph_nodes_entity_id', 'knowledge_graph_nodes', ['entity_id'], unique=True)
    op.create_index('ix_knowledge_graph_nodes_node_type', 'knowledge_graph_nodes', ['node_type'])
    op.create_index('ix_knowledge_graph_nodes_degree', 'knowledge_graph_nodes', ['degree'])
    
    # Create knowledge_graph_edges table
    op.create_table('knowledge_graph_edges',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('source_node_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('target_node_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('relationship_type', sa.String(length=50), nullable=False),
        sa.Column('properties', postgresql.JSONB(astext_type=sa.Text())),
        sa.Column('confidence', sa.DECIMAL(precision=3, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint('confidence >= 0.00 AND confidence <= 1.00', name='check_edge_confidence_range'),
        sa.CheckConstraint('source_node_id != target_node_id', name='check_no_self_loops'),
        sa.CheckConstraint("relationship_type IN ('fund', 'partner', 'acquire', 'compete', 'collaborate')", name='check_edge_relationship_type'),
        sa.ForeignKeyConstraint(['source_node_id'], ['knowledge_graph_nodes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_node_id'], ['knowledge_graph_nodes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_knowledge_graph_edges_source_node_id', 'knowledge_graph_edges', ['source_node_id'])
    op.create_index('ix_knowledge_graph_edges_target_node_id', 'knowledge_graph_edges', ['target_node_id'])
    op.create_index('ix_knowledge_graph_edges_relationship_type', 'knowledge_graph_edges', ['relationship_type'])
    op.create_index('ix_knowledge_graph_edges_confidence', 'knowledge_graph_edges', ['confidence'])
    
    # Create document_processing_jobs table
    op.create_table('document_processing_jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('priority', sa.String(length=10), nullable=False),
        sa.Column('extraction_config', postgresql.JSONB(astext_type=sa.Text())),
        sa.Column('entities_extracted', sa.Integer()),
        sa.Column('relationships_found', sa.Integer()),
        sa.Column('processing_time_seconds', sa.DECIMAL(precision=8, scale=2)),
        sa.Column('error_message', sa.TEXT()),
        sa.Column('retry_count', sa.Integer(), nullable=False),
        sa.Column('started_at', sa.TIMESTAMP()),
        sa.Column('completed_at', sa.TIMESTAMP()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint("status IN ('pending', 'processing', 'completed', 'failed')", name='check_job_status'),
        sa.CheckConstraint("priority IN ('high', 'normal', 'low')", name='check_job_priority'),
        sa.CheckConstraint('retry_count >= 0', name='check_non_negative_retry_count'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_document_processing_jobs_document_id', 'document_processing_jobs', ['document_id'])
    op.create_index('ix_document_processing_jobs_status', 'document_processing_jobs', ['status'])
    op.create_index('ix_document_processing_jobs_priority', 'document_processing_jobs', ['priority'])
    
    # Create processing_quality_metrics table
    op.create_table('processing_quality_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('job_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('metric_type', sa.String(length=50), nullable=False),
        sa.Column('entity_type', sa.String(length=50)),
        sa.Column('value', sa.DECIMAL(precision=10, scale=4), nullable=False),
        sa.Column('sample_size', sa.Integer()),
        sa.Column('confidence_interval', sa.DECIMAL(precision=5, scale=4)),
        sa.Column('calculated_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('job_metadata', postgresql.JSONB(astext_type=sa.Text())),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint("metric_type IN ('accuracy', 'precision', 'recall', 'latency', 'cost')", name='check_metric_type'),
        sa.CheckConstraint('sample_size IS NULL OR sample_size > 0', name='check_positive_sample_size'),
        sa.ForeignKeyConstraint(['job_id'], ['document_processing_jobs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_processing_quality_metrics_job_id', 'processing_quality_metrics', ['job_id'])
    op.create_index('ix_processing_quality_metrics_metric_type', 'processing_quality_metrics', ['metric_type'])
    op.create_index('ix_processing_quality_metrics_entity_type', 'processing_quality_metrics', ['entity_type'])
    op.create_index('ix_processing_quality_metrics_calculated_at', 'processing_quality_metrics', ['calculated_at'])


def downgrade() -> None:
    op.drop_table('processing_quality_metrics')
    op.drop_table('document_processing_jobs')
    op.drop_table('knowledge_graph_edges')
    op.drop_table('knowledge_graph_nodes')
    op.drop_table('entity_relationships')
    op.drop_table('extracted_entities')
    # Note: pgvector extension was not used

