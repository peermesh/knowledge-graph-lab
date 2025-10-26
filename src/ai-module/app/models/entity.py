"""
Entity model for storing extracted entities from AI processing.

This model represents entities extracted from documents including
organizations, people, funding amounts, dates, and locations.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy import DECIMAL, TEXT, VARCHAR, Boolean, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Entity(Base):
    """Model for extracted entities from document processing."""

    __tablename__ = "entities"

    # Core entity data
    name: Mapped[str] = mapped_column(TEXT, nullable=False, index=True)
    type: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        index=True
    )
    confidence: Mapped[float] = mapped_column(
        DECIMAL(3, 2),
        nullable=False
    )

    # Source information
    source: Mapped[str] = mapped_column(TEXT, nullable=False)
    source_type: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    source_document_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True
    )

    # Processing information
    extraction_method: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False,
        default="llm"
    )
    positions: Mapped[Optional[List[List[int]]]] = mapped_column(JSONB, nullable=True)

    # Additional metadata
    metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Vector embedding for similarity search
    vector_embedding: Mapped[Optional[List[float]]] = mapped_column(JSONB, nullable=True)

    # Status and lifecycle
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relationships
    relationships: Mapped[List["EntityRelationship"]] = relationship(
        "EntityRelationship",
        foreign_keys="[EntityRelationship.source_entity_id]",
        back_populates="source_entity",
        cascade="all, delete-orphan"
    )

    target_relationships: Mapped[List["EntityRelationship"]] = relationship(
        "EntityRelationship",
        foreign_keys="[EntityRelationship.target_entity_id]",
        back_populates="target_entity",
        cascade="all, delete-orphan"
    )

    graph_node: Mapped[Optional["KnowledgeGraphNode"]] = relationship(
        "KnowledgeGraphNode",
        back_populates="entity",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "confidence >= 0.00 AND confidence <= 1.00",
            name="check_confidence_range"
        ),
        CheckConstraint(
            "type IN ('organization', 'person', 'funding_amount', 'date', 'location', 'concept', 'event')",
            name="check_entity_type"
        ),
        Index("idx_entities_type_confidence", "type", "confidence"),
        Index("idx_entities_source", "source"),
        Index("idx_entities_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Entity(id={self.id}, name='{self.name}', type='{self.type}', confidence={self.confidence})>"
