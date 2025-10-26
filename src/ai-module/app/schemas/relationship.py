"""
Pydantic schemas for relationship-related API operations.

These schemas define the request and response formats for entity
relationship management and knowledge graph operations.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class RelationshipBase(BaseModel):
    """Base schema for entity relationships."""

    source_entity_id: str = Field(..., description="Source entity ID")
    target_entity_id: str = Field(..., description="Target entity ID")
    relationship_type: str = Field(
        ...,
        regex="^(fund|partner|acquire|compete|collaborate|mention)$",
        description="Relationship type"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score (0.0-1.0)"
    )
    strength: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Relationship strength (0.0-1.0)"
    )
    evidence: str = Field(..., description="Supporting evidence from source")
    temporal_context: Optional[Dict[str, Any]] = Field(
        None,
        description="Temporal context (dates, duration)"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional relationship properties"
    )


class RelationshipCreate(RelationshipBase):
    """Schema for creating new relationships."""

    @validator('source_entity_id', 'target_entity_id')
    def validate_entity_ids_different(cls, v, values):
        """Ensure source and target entities are different."""
        if 'source_entity_id' in values and v == values['source_entity_id']:
            raise ValueError('Source and target entities must be different')
        return v


class RelationshipResponse(RelationshipBase):
    """Schema for relationship API responses."""

    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class KnowledgeGraphQueryRequest(BaseModel):
    """Schema for knowledge graph queries."""

    query: str = Field(..., description="Search query or entity identifier")
    query_type: str = Field(
        default="entity_search",
        regex="^(entity_search|similarity_search|relationship_query)$",
        description="Type of query to perform"
    )
    filters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Query filters"
    )
    max_hops: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Maximum relationship hops for traversal"
    )
    limit: int = Field(
        default=50,
        ge=1,
        le=100,
        description="Maximum number of results"
    )


class KnowledgeGraphQueryResponse(BaseModel):
    """Schema for knowledge graph query responses."""

    query_id: str
    total_results: int
    execution_time_ms: int
    results: Dict[str, Any] = Field(description="Query results")
    knowledge_graph: Dict[str, Any] = Field(description="Graph visualization data")

    class Config:
        from_attributes = True


class GraphTraversalRequest(BaseModel):
    """Schema for graph traversal requests."""

    start_entity: str = Field(..., description="Starting entity ID")
    max_hops: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Maximum hops from start entity"
    )
    relationship_types: Optional[List[str]] = Field(
        None,
        description="Filter by relationship types"
    )
    entity_types: Optional[List[str]] = Field(
        None,
        description="Filter by entity types"
    )
    confidence_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold"
    )


class GraphTraversalResponse(BaseModel):
    """Schema for graph traversal responses."""

    nodes: List[Dict[str, Any]] = Field(description="Graph nodes")
    edges: List[Dict[str, Any]] = Field(description="Graph edges")
    path_count: int = Field(description="Number of paths found")
    execution_time_ms: int = Field(description="Query execution time")
    metadata: Dict[str, Any] = Field(description="Additional query metadata")

    class Config:
        from_attributes = True
