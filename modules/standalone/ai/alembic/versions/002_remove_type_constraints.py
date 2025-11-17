"""Remove hardcoded type constraints for flexible entity and relationship types

Revision ID: 002
Revises: 001
Create Date: 2025-11-02

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Remove CHECK constraints that limit entity types and relationship types
    to support flexible type detection per spec FR-001 and FR-004
    """
    # Drop hardcoded entity type constraint from extracted_entities
    op.drop_constraint('check_entity_type', 'extracted_entities', type_='check')
    
    # Drop hardcoded relationship type constraint from entity_relationships
    op.drop_constraint('check_relationship_type', 'entity_relationships', type_='check')
    
    # Drop hardcoded node type constraint from knowledge_graph_nodes
    op.drop_constraint('check_node_type', 'knowledge_graph_nodes', type_='check')
    
    # Drop hardcoded relationship type constraint from knowledge_graph_edges
    op.drop_constraint('check_edge_relationship_type', 'knowledge_graph_edges', type_='check')
    
    print("✓ Removed hardcoded type constraints - system now supports flexible entity and relationship types")


def downgrade() -> None:
    """
    Restore the original CHECK constraints
    """
    # Restore entity type constraint
    op.create_check_constraint(
        'check_entity_type',
        'extracted_entities',
        "entity_type IN ('organization', 'person', 'funding_amount', 'date', 'location')"
    )
    
    # Restore relationship type constraint
    op.create_check_constraint(
        'check_relationship_type',
        'entity_relationships',
        "relationship_type IN ('fund', 'partner', 'acquire', 'compete', 'collaborate', 'mention')"
    )
    
    # Restore node type constraint
    op.create_check_constraint(
        'check_node_type',
        'knowledge_graph_nodes',
        "node_type IN ('entity', 'concept', 'event')"
    )
    
    # Restore edge relationship type constraint
    op.create_check_constraint(
        'check_edge_relationship_type',
        'knowledge_graph_edges',
        "relationship_type IN ('fund', 'partner', 'acquire', 'compete', 'collaborate')"
    )

