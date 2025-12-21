from pydantic import BaseModel, Field, UUID4, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime


class SubscriberCreateRequest(BaseModel):
    email: EmailStr
    user_id: Optional[UUID4] = None
    preferred_channels: Optional[List[str]] = Field(default_factory=list)
    topic_interests: Optional[Dict[str, float]] = Field(default_factory=dict)
    frequency_settings: Optional[Dict[str, Any]] = Field(default_factory=dict)


class SubscriberData(BaseModel):
    id: UUID4
    email: EmailStr
    user_id: Optional[UUID4]
    preferred_channels: List[str]
    topic_interests: Dict[str, float]
    frequency_settings: Dict[str, Any]
    subscription_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SubscriberListData(BaseModel):
    subscribers: List[SubscriberData]


class SubscriberResponse(BaseModel):
    data: SubscriberData
    meta: Dict[str, Any]
    errors: List[Dict[str, Any]]


class SubscriberListResponse(BaseModel):
    data: SubscriberListData
    meta: Dict[str, Any]
    errors: List[Dict[str, Any]]
