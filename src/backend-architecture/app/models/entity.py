"""
Entity model for the Backend Architecture Module.

This model stores entities from the AI module and provides
the foundation for the knowledge graph data structure.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy import DECIMAL, TEXT, VARCHAR, Boolean, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Entity(Base):
    """Model for extracted entities stored in the backend."""

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

    # Vector embedding for similarity search (from AI module)
    vector_embedding: Mapped[Optional[List[float]]] = mapped_column(JSONB, nullable=True)

    # Status and lifecycle
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

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
