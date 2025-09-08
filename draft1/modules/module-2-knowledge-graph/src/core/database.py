"""
Database models and configuration for knowledge graph service
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from .config import settings

# Database engine
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EntityType(str, enum.Enum):
    """Entity type enumeration"""
    PLATFORM = "platform"
    CREATOR = "creator"  
    ORGANIZATION = "organization"
    POLICY = "policy"
    GRANT = "grant"
    EVENT = "event"
    TOPIC = "topic"

class Entity(Base):
    """Knowledge graph entity"""
    __tablename__ = "entities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    entity_type = Column(String, nullable=False)  # EntityType enum value
    description = Column(Text)
    
    # Metadata
    confidence_score = Column(Float, default=0.0)
    source_urls = Column(Text)  # JSON array of source URLs
    metadata = Column(Text)  # JSON metadata (location, domain, etc.)
    
    # Vector embedding ID (references Qdrant)
    embedding_id = Column(String, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    outgoing_relationships = relationship("Relationship", foreign_keys="Relationship.source_id", back_populates="source_entity")
    incoming_relationships = relationship("Relationship", foreign_keys="Relationship.target_id", back_populates="target_entity")

class Relationship(Base):
    """Knowledge graph relationships between entities"""
    __tablename__ = "relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    target_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    relationship_type = Column(String, nullable=False)  # "owns", "created_by", "regulates", etc.
    
    # Relationship strength and context
    confidence_score = Column(Float, default=0.0)
    context = Column(Text)  # Description of the relationship
    source_urls = Column(Text)  # JSON array of supporting sources
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Foreign key relationships
    source_entity = relationship("Entity", foreign_keys=[source_id], back_populates="outgoing_relationships")
    target_entity = relationship("Entity", foreign_keys=[target_id], back_populates="incoming_relationships")

class ResearchTopic(Base):
    """Research topics and their priorities"""
    __tablename__ = "research_topics"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, unique=True, index=True, nullable=False)
    domain = Column(String, nullable=False)  # "creator-economy", "policy", etc.
    
    # Priority and status
    priority_score = Column(Float, default=5.0)  # 1-10 scale
    status = Column(String, default="pending")  # pending, researching, completed, archived
    
    # Research depth and progress
    research_depth = Column(Integer, default=0)
    last_researched = Column(DateTime)
    next_research_due = Column(DateTime)
    
    # Geographic scope
    location_scope = Column(String, default="global")  # global, national, state, local
    
    # Associated entities discovered through research
    related_entities = Column(Text)  # JSON array of entity IDs
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ResearchSession(Base):
    """Individual research sessions and their results"""
    __tablename__ = "research_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    topic_id = Column(Integer, ForeignKey("research_topics.id"))
    
    # Research parameters
    research_prompt = Column(Text, nullable=False)
    model_used = Column(String)  # GPT-4, Claude, etc.
    
    # Results
    raw_response = Column(Text)  # Full AI response
    entities_discovered = Column(Integer, default=0)
    relationships_discovered = Column(Integer, default=0)
    quality_score = Column(Float, default=0.0)
    
    # Status and timing
    status = Column(String, default="pending")  # pending, processing, completed, failed
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    
    # Relationship to topic
    topic = relationship("ResearchTopic")

class KnowledgeGap(Base):
    """Identified gaps in knowledge that need research"""
    __tablename__ = "knowledge_gaps"
    
    id = Column(Integer, primary_key=True, index=True)
    gap_description = Column(Text, nullable=False)
    gap_type = Column(String)  # "entity_missing", "relationship_unclear", "outdated_info"
    
    # Priority and context
    priority_score = Column(Float, default=5.0)
    context = Column(Text)  # Why this gap is important
    
    # Related entities/topics
    related_entity_ids = Column(Text)  # JSON array
    suggested_research_topics = Column(Text)  # JSON array
    
    # Status tracking
    status = Column(String, default="identified")  # identified, researching, filled, archived
    resolution_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    resolved_at = Column(DateTime)

async def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()