"""Knowledge graph node and edge models"""

from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship as orm_relationship

# Optional pgvector support
try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    Vector = lambda dim: ARRAY(DECIMAL, dimensions=1)

from .base import Base, TimestampMixin


class KnowledgeGraphNode(Base, TimestampMixin):
    """Represents a node in the knowledge graph"""
    
    __tablename__ = "knowledge_graph_nodes"
    
    entity_id = Column(
        UUID(as_uuid=True),
        ForeignKey('extracted_entities.id', ondelete='CASCADE'),
        unique=True,
        nullable=False,
        index=True
    )
    node_type = Column(String(50), nullable=False, index=True)
    properties = Column(JSONB, nullable=False)
    vector_embedding = Column(Vector(768), nullable=False)
    degree = Column(Integer, nullable=False, default=0, index=True)
    
    # Relationship to ExtractedEntity
    entity = orm_relationship("ExtractedEntity", backref="graph_node")
    
    __table_args__ = (
        CheckConstraint(
            "node_type IN ('entity', 'concept', 'event')",
            name='check_node_type'
        ),
        CheckConstraint(
            'degree >= 0',
            name='check_non_negative_degree'
        ),
    )
    
    def __repr__(self):
        return f"<KnowledgeGraphNode(id={self.id}, type={self.node_type}, degree={self.degree})>"


class KnowledgeGraphEdge(Base, TimestampMixin):
    """Represents an edge in the knowledge graph"""
    
    __tablename__ = "knowledge_graph_edges"
    
    source_node_id = Column(
        UUID(as_uuid=True),
        ForeignKey('knowledge_graph_nodes.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    target_node_id = Column(
        UUID(as_uuid=True),
        ForeignKey('knowledge_graph_nodes.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    relationship_type = Column(String(50), nullable=False, index=True)
    properties = Column(JSONB)
    confidence = Column(DECIMAL(3, 2), nullable=False, index=True)
    
    # Relationships to KnowledgeGraphNode
    source_node = orm_relationship(
        "KnowledgeGraphNode",
        foreign_keys=[source_node_id],
        backref="outgoing_edges"
    )
    target_node = orm_relationship(
        "KnowledgeGraphNode",
        foreign_keys=[target_node_id],
        backref="incoming_edges"
    )
    
    __table_args__ = (
        CheckConstraint(
            'confidence >= 0.00 AND confidence <= 1.00',
            name='check_edge_confidence_range'
        ),
        CheckConstraint(
            'source_node_id != target_node_id',
            name='check_no_self_loops'
        ),
        CheckConstraint(
            "relationship_type IN ('fund', 'partner', 'acquire', 'compete', 'collaborate')",
            name='check_edge_relationship_type'
        ),
    )
    
    def __repr__(self):
        return (f"<KnowledgeGraphEdge(id={self.id}, "
                f"type={self.relationship_type}, "
                f"confidence={self.confidence})>")

