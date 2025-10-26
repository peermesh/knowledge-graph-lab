from pydantic import BaseModel, Field, UUID4
from typing import Optional, Dict, Any


class ChannelCreateRequest(BaseModel):
    name: str = Field(..., max_length=100)
    channel_type: str = Field(..., regex="^(email|slack|discord|webhook|rss)$")
    configuration: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True


class ChannelResponse(BaseModel):
    data: Dict[str, Any]
    meta: Dict[str, Any]
    errors: list
