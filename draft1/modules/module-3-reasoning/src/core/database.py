"""
Database models for reasoning service
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from datetime import datetime
import enum

from .config import settings

# Database engine
engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DigestFrequency(str, enum.Enum):
    """Digest frequency options"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class ContentStatus(str, enum.Enum):
    """Content generation status"""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    PUBLISHED = "published"

class UserProfile(Base):
    """User preferences and personalization data"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)  # External user ID
    
    # Interest and preference settings
    interests = Column(JSON)  # List of interest categories
    preferred_frequency = Column(String, default=settings.DEFAULT_DIGEST_FREQUENCY)
    preferred_length = Column(String, default="medium")  # short, medium, long
    
    # Platform preferences
    email_enabled = Column(Boolean, default=True)
    social_platforms = Column(JSON)  # List of enabled social platforms
    
    # Personalization data
    engagement_history = Column(JSON)  # Track what user engages with
    feedback_scores = Column(JSON)    # User ratings on content
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class TopicCluster(Base):
    """Discovered topic clusters from content analysis"""
    __tablename__ = "topic_clusters"
    
    id = Column(Integer, primary_key=True, index=True)
    cluster_name = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    
    # Cluster characteristics
    keywords = Column(JSON)  # List of key terms
    entity_ids = Column(JSON)  # Related entity IDs from knowledge graph
    similarity_score = Column(Float, default=0.0)
    
    # Importance and trends
    priority_score = Column(Float, default=5.0)
    trend_direction = Column(String, default="stable")  # rising, falling, stable
    last_updated = Column(DateTime, default=func.now())
    
    # Content generation
    content_generated = Column(Integer, default=0)  # Number of content pieces generated
    avg_engagement = Column(Float, default=0.0)     # Average user engagement
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ContentItem(Base):
    """Generated content items (digests, social posts, etc.)"""
    __tablename__ = "content_items"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(String, unique=True, index=True)
    
    # Content metadata
    content_type = Column(String, nullable=False)  # "digest", "social_post", "summary"
    platform = Column(String)  # Target platform (email, twitter, linkedin, etc.)
    title = Column(String)
    content_text = Column(Text, nullable=False)
    
    # Generation parameters
    user_id = Column(String, index=True)  # Target user (null for general content)
    topic_cluster_id = Column(Integer)    # Source topic cluster
    template_used = Column(String)
    model_used = Column(String)
    generation_prompt = Column(Text)
    
    # Quality and performance metrics
    quality_score = Column(Float, default=0.0)
    engagement_score = Column(Float, default=0.0)
    fact_check_score = Column(Float, default=0.0)
    bias_score = Column(Float, default=0.0)
    
    # Publication status
    status = Column(String, default=ContentStatus.PENDING.value)
    scheduled_for = Column(DateTime)
    published_at = Column(DateTime)
    
    # Source attribution
    source_entities = Column(JSON)  # Entity IDs used in generation
    source_urls = Column(JSON)      # Source URLs for fact-checking
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ResearchPriority(Base):
    """Priority queue for research topics"""
    __tablename__ = "research_priorities"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    
    # Priority calculation factors
    user_interest_score = Column(Float, default=0.0)
    recency_score = Column(Float, default=0.0)
    novelty_score = Column(Float, default=0.0)
    importance_score = Column(Float, default=0.0)
    credibility_score = Column(Float, default=0.0)
    
    # Calculated priority
    final_priority = Column(Float, default=0.0)
    
    # Research status
    research_requested = Column(Boolean, default=False)
    last_research_request = Column(DateTime)
    
    # Context and justification
    reasoning = Column(Text)  # Why this topic is prioritized
    knowledge_gaps = Column(JSON)  # Specific gaps to address
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ContentFeedback(Base):
    """User feedback on generated content"""
    __tablename__ = "content_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False)
    
    # Feedback metrics
    rating = Column(Integer)  # 1-5 rating
    relevance_score = Column(Integer)  # 1-5 relevance
    accuracy_score = Column(Integer)   # 1-5 accuracy
    
    # Qualitative feedback
    feedback_text = Column(Text)
    improvement_suggestions = Column(Text)
    
    # Engagement indicators
    time_spent_reading = Column(Integer)  # seconds
    clicked_links = Column(JSON)          # which links were clicked
    shared = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())

class GenerationJob(Base):
    """Background content generation jobs"""
    __tablename__ = "generation_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    
    # Job parameters
    job_type = Column(String, nullable=False)  # "digest", "social_batch", "summary"
    user_id = Column(String)  # Target user if personalized
    parameters = Column(JSON)  # Generation parameters
    
    # Status tracking
    status = Column(String, default="pending")
    progress = Column(Float, default=0.0)
    error_message = Column(Text)
    
    # Results
    content_ids_generated = Column(JSON)  # List of generated content IDs
    total_items_generated = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

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