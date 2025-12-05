from sqlalchemy import Column, String, Boolean, DateTime, JSON
import uuid
from datetime import datetime

from ..core.database import Base


class Channel(Base):
    __tablename__ = 'channels'
    __table_args__ = {"schema": "publishing_channels"}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    channel_type = Column(String(32), nullable=False)  # email|slack|discord|webhook|rss
    is_active = Column(Boolean, nullable=False, default=True)
    configuration = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
