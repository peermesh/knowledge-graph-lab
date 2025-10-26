"""
Knowledge graph models for storing graph nodes and edges.

These models represent the processed knowledge graph structure
with vector embeddings for similarity search capabilities.
"""

from typing import Any, Dict, Optional

from sqlalchemy import DECIMAL, INTEGER, CheckConstraint, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class KnowledgeGraphNode(Base):
    """Model for knowledge graph nodes (processed entities)."""

    __tablename__ = "knowledge_graph_nodes"

    # Entity reference
    entity_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("entities.id"),
        nullable=False,
        unique=True,
        index=True
    )

    # Node properties
    node_type: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False,
        index=True
    )
    properties: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # Vector embedding for similarity search
    vector_embedding: Mapped[Optional[List[float]]] = mapped_column(JSONB, nullable=True)

    # Graph metrics
    degree: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        default=0,
        index=True
    )

    # Relationships
    entity: Mapped["Entity"] = relationship("Entity", back_populates="graph_node")
    outgoing_edges: Mapped[List["KnowledgeGraphEdge"]] = relationship(
        "KnowledgeGraphEdge",
        foreign_keys="[KnowledgeGraphEdge.source_node_id]",
        back_populates="source_node"
    )
    incoming_edges: Mapped[List["KnowledgeGraphEdge"]] = relationship(
        "KnowledgeGraphEdge",
        foreign_keys="[KnowledgeGraphEdge.target_node_id]",
        back_populates="target_node"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "node_type IN ('entity', 'concept', 'event')",
            name="check_node_type"
        ),
        Index("idx_nodes_type_degree", "node_type", "degree"),
    )

    def __repr__(self) -> str:
        return f"<KnowledgeGraphNode(id={self.id}, entity={self.entity_id}, type='{self.node_type}', degree={self.degree})>"


class KnowledgeGraphEdge(Base):
    """Model for knowledge graph edges (processed relationships)."""

    __tablename__ = "knowledge_graph_edges"

    # Edge endpoints
    source_node_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("knowledge_graph_nodes.id"),
        nullable=False,
        index=True
    )
    target_node_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("knowledge_graph_nodes.id"),
        nullable=False,
        index=True
    )

    # Edge properties
    relationship_type: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False,
        index=True
    )
    properties: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    confidence: Mapped[float] = mapped_column(
        DECIMAL(3, 2),
        nullable=False
    )

    # Relationships
    source_node: Mapped["KnowledgeGraphNode"] = relationship(
        "KnowledgeGraphNode",
        foreign_keys=[source_node_id],
        back_populates="outgoing_edges"
    )
    target_node: Mapped["KnowledgeGraphNode"] = relationship(
        "KnowledgeGraphNode",
        foreign_keys=[target_node_id],
        back_populates="incoming_edges"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "confidence >= 0.00 AND confidence <= 1.00",
            name="check_edge_confidence_range"
        ),
        CheckConstraint(
            "source_node_id != target_node_id",
            name="check_no_self_edge"
        ),
        Index("idx_edges_source_target", "source_node_id", "target_node_id"),
        Index("idx_edges_type_confidence", "relationship_type", "confidence"),
    )

    def __repr__(self) -> str:
        return (
            "<KnowledgeGraphEdge("
            f"id={self.id}, "
            f"source={self.source_node_id}, "
            f"target={self.target_node_id}, "
            f"type='{self.relationship_type}', "
            f"confidence={self.confidence}"
            ")>"
        )
