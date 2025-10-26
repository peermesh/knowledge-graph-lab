"""Entity data model for extracted entities"""

from sqlalchemy import Column, String, DECIMAL, TIMESTAMP, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy import ForeignKey

# Optional pgvector support
try:
    from pgvector.sqlalchemy import Vector
    PGVECTOR_AVAILABLE = True
except ImportError:
    # Fallback to ARRAY type if pgvector not installed
    Vector = lambda dim: ARRAY(DECIMAL, dimensions=1)
    PGVECTOR_AVAILABLE = False

from .base import Base, TimestampMixin


class ExtractedEntity(Base, TimestampMixin):
    """Represents an entity extracted from documents"""
    
    __tablename__ = "extracted_entities"
    
    text = Column(String(500), nullable=False, index=True)
    entity_type = Column(
        String(50),
        nullable=False,
        index=True
    )
    confidence = Column(
        DECIMAL(3, 2),
        nullable=False,
        index=True
    )
    source_document_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )
    extraction_method = Column(String(50), nullable=False)
    positions = Column(JSONB, nullable=False)
    entity_metadata = Column(JSONB)
    vector_embedding = Column(Vector(768), nullable=False)
    
    __table_args__ = (
        CheckConstraint(
            'confidence >= 0.00 AND confidence <= 1.00',
            name='check_confidence_range'
        ),
        CheckConstraint(
            "entity_type IN ('organization', 'person', 'funding_amount', 'date', 'location')",
            name='check_entity_type'
        ),
    )
    
    def __repr__(self):
        return f"<ExtractedEntity(id={self.id}, text={self.text}, type={self.entity_type}, confidence={self.confidence})>"

