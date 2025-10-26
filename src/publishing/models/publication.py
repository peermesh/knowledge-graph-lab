from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime

from ..core.database import Base


class Publication(Base):
    __tablename__ = 'publishing_publications'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_type = Column(String(32), nullable=False)  # newsletter|alert|digest|manual
    scheduled_time = Column(DateTime, nullable=False)
    published_time = Column(DateTime, nullable=True)
    status = Column(String(32), nullable=False, default='scheduled')
    content_ids = Column(JSONB, nullable=False, default=list)  # list of content UUIDs
    channels = Column(JSONB, nullable=False, default=list)  # list of channel UUIDs
    channel_results = Column(JSONB, nullable=False, default=dict)
    engagement_metrics = Column(JSONB, nullable=False, default=dict)
    personalization_applied = Column(JSONB, nullable=False, default=dict)
    error_details = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
