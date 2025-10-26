from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime

from ..core.database import Base


class Subscriber(Base):
    __tablename__ = 'publishing_subscribers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    preferred_channels = Column(JSONB, nullable=False, default=list)
    topic_interests = Column(JSONB, nullable=False, default=dict)
    frequency_settings = Column(JSONB, nullable=False, default=dict)
    personalization_data = Column(JSONB, nullable=False, default=dict)
    subscription_status = Column(String(32), nullable=False, default='active')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
