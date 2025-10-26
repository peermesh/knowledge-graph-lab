from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime

from ..core.database import Base


class Analytics(Base):
    __tablename__ = 'publishing_analytics'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    publication_id = Column(UUID(as_uuid=True), nullable=False)
    channel_type = Column(String(32), nullable=False)  # email|slack|discord|webhook|rss
    metric_type = Column(String(32), nullable=False)  # open|click|unsubscribe|bounce|complaint
    metric_value = Column(Float, nullable=False, default=0.0)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    metadata = Column(JSONB, nullable=False, default=dict)
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
