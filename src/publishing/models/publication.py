from sqlalchemy import Column, String, DateTime, Text, JSON
import uuid
from datetime import datetime

from ..core.database import Base


class Publication(Base):
    __tablename__ = 'publishing_publications'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    publication_type = Column(String(32), nullable=False)  # newsletter|alert|digest|manual
    scheduled_time = Column(DateTime, nullable=False)
    published_time = Column(DateTime, nullable=True)
    status = Column(String(32), nullable=False, default='scheduled')
    content_ids = Column(JSON, nullable=False, default=list)  # list of content UUIDs
    channels = Column(JSON, nullable=False, default=list)  # list of channel UUIDs
    channel_results = Column(JSON, nullable=False, default=dict)
    engagement_metrics = Column(JSON, nullable=False, default=dict)
    personalization_applied = Column(JSON, nullable=False, default=dict)
    error_details = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
