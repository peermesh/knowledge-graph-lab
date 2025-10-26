"""
Pydantic schemas for entity-related API operations.

These schemas define the request and response formats for entity
management and knowledge graph operations.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class EntityBase(BaseModel):
    """Base schema for entity data."""

    name: str = Field(..., description="Entity text value")
    type: str = Field(
        ...,
        description="Entity type",
        regex="^(organization|person|funding_amount|date|location|concept|event)$"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score (0.0-1.0)"
    )
    source: str = Field(..., description="Source document identifier")
    source_type: str = Field(..., description="Type of source document")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional entity properties")
    positions: Optional[List[List[int]]] = Field(
        default=None,
        description="Character positions in source text"
    )


class EntityCreate(EntityBase):
    """Schema for creating new entities."""

    pass


class EntityUpdate(BaseModel):
    """Schema for updating existing entities."""

    name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_active: Optional[bool] = None


class EntityResponse(EntityBase):
    """Schema for entity API responses."""

    id: str
    source_document_id: Optional[str] = None
    extraction_method: str
    vector_embedding: Optional[List[float]] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class EntityListResponse(BaseModel):
    """Schema for paginated entity list responses."""

    entities: List[EntityResponse]
    total_count: int
    page: int
    page_size: int
    has_more: bool
