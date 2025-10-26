"""
Entity relationship model for the Backend Architecture Module.

This model defines relationships between entities and supports
the knowledge graph structure with confidence scoring and evidence.
"""

from typing import Any, Dict, Optional

from sqlalchemy import DECIMAL, TEXT, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class EntityRelationship(Base):
    """Model for relationships between extracted entities."""

    __tablename__ = "entity_relationships"

    # Relationship endpoints
    source_entity_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )
    target_entity_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )

    # Relationship data
    relationship_type: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False,
        index=True
    )
    confidence: Mapped[float] = mapped_column(
        DECIMAL(3, 2),
        nullable=False
    )
    strength: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 2), nullable=True)

    # Evidence and context
    evidence: Mapped[str] = mapped_column(TEXT, nullable=False)
    temporal_context: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "confidence >= 0.00 AND confidence <= 1.00",
            name="check_relationship_confidence_range"
        ),
        CheckConstraint(
            "relationship_type IN ('fund', 'partner', 'acquire', 'compete', 'collaborate', 'mention')",
            name="check_relationship_type"
        ),
        CheckConstraint(
            "source_entity_id != target_entity_id",
            name="check_no_self_relationship"
        ),
        Index("idx_relationships_source_target", "source_entity_id", "target_entity_id"),
        Index("idx_relationships_type_confidence", "relationship_type", "confidence"),
    )

    def __repr__(self) -> str:
        return (
            "<EntityRelationship("
            f"id={self.id}, "
            f"source={self.source_entity_id}, "
            f"target={self.target_entity_id}, "
            f"type='{self.relationship_type}', "
            f"confidence={self.confidence}"
            ")>"
        )
