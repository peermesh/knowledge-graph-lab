from sqlalchemy import Column, String, DateTime, JSON
import uuid
from datetime import datetime

from ..core.database import Base


class Subscriber(Base):
    __tablename__ = 'subscribers'
    __table_args__ = {"schema": "publishing_subscribers"}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    preferred_channels = Column(JSON, nullable=False, default=list)
    topic_interests = Column(JSON, nullable=False, default=dict)
    frequency_settings = Column(JSON, nullable=False, default=dict)
    personalization_data = Column(JSON, nullable=False, default=dict)
    subscription_status = Column(String(32), nullable=False, default='active')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
