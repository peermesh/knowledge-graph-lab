from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime

from ..core.database import Base


class Template(Base):
    __tablename__ = 'templates'
    __table_args__ = {"schema": "publishing_templates"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    template_type = Column(String(32), nullable=False)  # email|slack|discord|webhook
    content_structure = Column(JSONB, nullable=False, default=dict)
    formatting_rules = Column(JSONB, nullable=False, default=dict)
    branding_elements = Column(JSONB, nullable=False, default=dict)
    variable_definitions = Column(JSONB, nullable=False, default=dict)
    usage_count = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
