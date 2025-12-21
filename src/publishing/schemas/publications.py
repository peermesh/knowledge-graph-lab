"""
Pydantic schemas for Publications API.

Request and response models with comprehensive validation for publication management.
Follows RFC7807 Problem Details for error responses.

Constitution Compliance:
- Comprehensive Analytics Integration: Publication tracking and status models
- Scalable Architecture: Efficient data validation and serialization
- Performance: Optimized for high-volume publication processing
"""

from pydantic import BaseModel, Field, validator, UUID4, EmailStr
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timezone
from enum import Enum


class PublicationType(str, Enum):
    """Publication types supported by the system."""
    NEWSLETTER = "newsletter"
    ALERT = "alert"
    DIGEST = "digest"
    MANUAL = "manual"


class PublicationStatus(str, Enum):
    """Publication status values."""
    SCHEDULED = "scheduled"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ChannelType(str, Enum):
    """Channel types for delivery."""
    EMAIL = "email"
    SLACK = "slack"
    DISCORD = "discord"
    WEBHOOK = "webhook"
    RSS = "rss"


class CreatePublicationRequest(BaseModel):
    """Request model for creating a new publication."""

    content_ids: List[UUID4] = Field(
        default_factory=list,
        description="IDs of content to be published (optional for testing)",
        min_items=0,
        max_items=100
    )

    channels: List[UUID4] = Field(
        ...,
        description="IDs of channels for publication",
        min_items=1,
        max_items=10
    )

    publication_type: PublicationType = Field(
        ...,
        description="Type of publication to create"
    )

    scheduled_time: Optional[datetime] = Field(
        None,
        description="When to publish (defaults to immediate if not specified)"
    )

    personalization_rules: Optional[Dict[str, Any]] = Field(
        None,
        description="Custom personalization rules for this publication"
    )

    template_id: Optional[UUID4] = Field(
        None,
        description="Template to use for formatting"
    )

    @validator("scheduled_time")
    def validate_scheduled_time(cls, v):
        """Ensure scheduled time is in the future."""
        if v:
            # Make comparison timezone-aware
            now = datetime.now(timezone.utc)
            # Normalize v to UTC if it's naive
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)
            if v <= now:
                raise ValueError("Scheduled time must be in the future")
        return v


class UpdatePublicationRequest(BaseModel):
    """Request model for updating a publication."""

    scheduled_time: Optional[datetime] = Field(
        None,
        description="Updated scheduled time"
    )

    personalization_rules: Optional[Dict[str, Any]] = Field(
        None,
        description="Updated personalization rules"
    )

    @validator("scheduled_time")
    def validate_scheduled_time(cls, v):
        """Ensure scheduled time is in the future."""
        if v:
            # Make comparison timezone-aware
            now = datetime.now(timezone.utc)
            # Normalize v to UTC if it's naive
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)
            if v <= now:
                raise ValueError("Scheduled time must be in the future")
        return v


class ChannelResult(BaseModel):
    """Result of publication delivery to a specific channel."""

    status: str = Field(
        ...,
        description="Delivery status for this channel",
        regex="^(success|failed|pending|retrying)$"
    )

    delivered_at: Optional[datetime] = Field(
        None,
        description="When delivery was completed"
    )

    error_message: Optional[str] = Field(
        None,
        description="Error message if delivery failed"
    )

    recipient_count: Optional[int] = Field(
        None,
        description="Number of recipients for this channel",
        ge=0
    )

    engagement_metrics: Optional[Dict[str, Any]] = Field(
        None,
        description="Channel-specific engagement data"
    )

    class Config:
        orm_mode = True


class PublicationData(BaseModel):
    """Publication data model for API responses."""

    id: UUID4
    content_ids: List[UUID4]
    channels: List[UUID4]
    publication_type: PublicationType
    scheduled_time: datetime
    published_time: Optional[datetime]
    status: PublicationStatus
    channel_results: Dict[str, ChannelResult]
    engagement_metrics: Dict[str, Any]
    personalization_applied: Dict[str, Any]
    error_details: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PublicationResponse(BaseModel):
    """Response model for publication operations."""

    data: PublicationData
    meta: Dict[str, Any]
    errors: List[Dict[str, Any]]


class PublicationListData(BaseModel):
    """Data model for publication list responses."""

    publications: List[PublicationData]
    total_count: int
    limit: int
    offset: int


class PublicationListResponse(BaseModel):
    """Response model for publication list operations."""

    data: PublicationListData
    meta: Dict[str, Any]
    errors: List[Dict[str, Any]]


# Newsletter-specific schemas
class NewsletterContent(BaseModel):
    """Content item for newsletter generation."""

    id: UUID4
    title: str
    summary: str
    url: str
    published_at: datetime
    quality_score: float
    relevance_score: float
    topics: List[str]


class NewsletterRequest(BaseModel):
    """Request model for newsletter generation."""

    subscriber_ids: Optional[List[UUID4]] = Field(
        None,
        description="Specific subscribers (if not provided, sends to all active subscribers)"
    )

    topic_filters: Optional[List[str]] = Field(
        None,
        description="Filter content by topics"
    )

    quality_threshold: float = Field(
        0.7,
        description="Minimum quality score for content inclusion",
        ge=0.0,
        le=1.0
    )

    max_articles: int = Field(
        10,
        description="Maximum number of articles per newsletter",
        ge=1,
        le=50
    )

    scheduled_time: datetime = Field(
        ...,
        description="When to send the newsletter"
    )

    template_id: Optional[UUID4] = Field(
        None,
        description="Template to use for newsletter formatting"
    )


# Alert-specific schemas
class AlertRequest(BaseModel):
    """Request model for creating real-time alerts."""

    content_id: UUID4 = Field(
        ...,
        description="ID of content that triggered the alert"
    )

    priority: str = Field(
        "high",
        description="Alert priority level",
        regex="^(low|medium|high|critical)$"
    )

    target_channels: List[UUID4] = Field(
        ...,
        description="Channels to send alert to",
        min_items=1,
        max_items=5
    )

    personalization_rules: Optional[Dict[str, Any]] = Field(
        None,
        description="Personalization rules for alert targeting"
    )


# Bulk operation schemas
class BulkPublicationRequest(BaseModel):
    """Request model for bulk publication operations."""

    publications: List[CreatePublicationRequest] = Field(
        ...,
        description="List of publications to create",
        min_items=1,
        max_items=50
    )

    batch_name: Optional[str] = Field(
        None,
        description="Name for this batch operation"
    )


class BulkPublicationResponse(BaseModel):
    """Response model for bulk publication operations."""

    data: Dict[str, Any]
    meta: Dict[str, Any]
    errors: List[Dict[str, Any]]


# Performance and monitoring schemas
class PublicationMetrics(BaseModel):
    """Publication performance metrics."""

    publication_id: UUID4
    channel_type: ChannelType
    metric_type: str  # open, click, unsubscribe, bounce, complaint
    metric_value: float
    user_id: Optional[UUID4]
    metadata: Dict[str, Any]
    recorded_at: datetime


class PerformanceMetricsRequest(BaseModel):
    """Request model for performance metrics queries."""

    start_date: datetime = Field(
        ...,
        description="Start date for metrics query"
    )

    end_date: datetime = Field(
        ...,
        description="End date for metrics query"
    )

    channel_types: Optional[List[ChannelType]] = Field(
        None,
        description="Filter by channel types"
    )

    publication_types: Optional[List[PublicationType]] = Field(
        None,
        description="Filter by publication types"
    )

    group_by: Optional[str] = Field(
        "day",
        description="Group results by time period",
        regex="^(hour|day|week|month)$"
    )


class TestNewsletterRequest(BaseModel):
    """Request model for testing newsletter delivery."""

    test_email: Optional[EmailStr] = Field(
        None,
        description="Override: send test to specific email instead of all subscribers"
    )

