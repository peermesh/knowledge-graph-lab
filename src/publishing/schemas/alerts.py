from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, UUID4
from datetime import datetime


class CreateAlertRequest(BaseModel):
    content_id: UUID4 = Field(..., description="ID of content that triggered the alert")
    target_channels: List[UUID4] = Field(..., description="Channels to send alert to", min_items=1, max_items=5)
    priority: str = Field("high", description="Alert priority", regex="^(low|medium|high|critical)$")
    personalization_rules: Optional[Dict[str, Any]] = Field(None, description="Personalization for alert targeting")


class AlertData(BaseModel):
    id: UUID4
    content_id: UUID4
    target_channels: List[UUID4]
    priority: str
    status: str
    created_at: datetime


class AlertResponse(BaseModel):
    data: AlertData
    meta: Dict[str, Any]
    errors: List[Dict[str, Any]]

