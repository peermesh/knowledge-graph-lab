"""Relationship data model for entity relationships"""

from sqlalchemy import Column, String, DECIMAL, TEXT, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship as orm_relationship

from .base import Base, TimestampMixin


class EntityRelationship(Base, TimestampMixin):
    """Represents a relationship between two entities"""
    
    __tablename__ = "entity_relationships"
    
    source_entity_id = Column(
        UUID(as_uuid=True),
        ForeignKey('extracted_entities.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    target_entity_id = Column(
        UUID(as_uuid=True),
        ForeignKey('extracted_entities.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    relationship_type = Column(String(50), nullable=False, index=True)
    confidence = Column(DECIMAL(3, 2), nullable=False, index=True)
    strength = Column(DECIMAL(3, 2))
    evidence = Column(TEXT)
    temporal_context = Column(JSONB)
    relationship_metadata = Column(JSONB)
    
    # Relationships to ExtractedEntity
    source_entity = orm_relationship(
        "ExtractedEntity",
        foreign_keys=[source_entity_id],
        backref="outgoing_relationships"
    )
    target_entity = orm_relationship(
        "ExtractedEntity",
        foreign_keys=[target_entity_id],
        backref="incoming_relationships"
    )
    
    __table_args__ = (
        CheckConstraint(
            'confidence >= 0.00 AND confidence <= 1.00',
            name='check_relationship_confidence_range'
        ),
        CheckConstraint(
            'strength IS NULL OR (strength >= 0.00 AND strength <= 1.00)',
            name='check_strength_range'
        ),
        CheckConstraint(
            'source_entity_id != target_entity_id',
            name='check_no_self_relationships'
        ),
        # Flexible relationship types - no hardcoded constraint (FR-004)
    )
    
    def __repr__(self):
        return (f"<EntityRelationship(id={self.id}, "
                f"type={self.relationship_type}, "
                f"confidence={self.confidence})>")

