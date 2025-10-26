"""
Relationship API endpoints for the AI Development Module.

This module provides REST API endpoints for entity relationship
management and knowledge graph traversal operations.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db
from ....schemas.relationship import (
    RelationshipCreate,
    RelationshipResponse,
    KnowledgeGraphQueryRequest,
    KnowledgeGraphQueryResponse,
    GraphTraversalRequest,
    GraphTraversalResponse,
)

# Create router
router = APIRouter()


@router.post("/", response_model=RelationshipResponse)
async def create_relationship(
    relationship: RelationshipCreate,
    db: AsyncSession = Depends(get_db)
) -> RelationshipResponse:
    """Create a new entity relationship."""
    # Validate that source and target entities exist
    source_result = await db.execute(
        "SELECT id FROM entities WHERE id = :entity_id AND is_active = true",
        {"entity_id": relationship.source_entity_id}
    )

    if not source_result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source entity {relationship.source_entity_id} not found"
        )

    target_result = await db.execute(
        "SELECT id FROM entities WHERE id = :entity_id AND is_active = true",
        {"entity_id": relationship.target_entity_id}
    )

    if not target_result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target entity {relationship.target_entity_id} not found"
        )

    # Check if relationship already exists
    existing = await db.execute(
        """
        SELECT id FROM entity_relationships
        WHERE source_entity_id = :source_id
        AND target_entity_id = :target_id
        AND relationship_type = :rel_type
        """,
        {
            "source_id": relationship.source_entity_id,
            "target_id": relationship.target_entity_id,
            "rel_type": relationship.relationship_type
        }
    )

    if existing.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Relationship already exists between these entities"
        )

    # Create relationship using raw SQL for now
    from ....models import EntityRelationship

    db_relationship = EntityRelationship(
        source_entity_id=relationship.source_entity_id,
        target_entity_id=relationship.target_entity_id,
        relationship_type=relationship.relationship_type,
        confidence=relationship.confidence,
        strength=relationship.strength,
        evidence=relationship.evidence,
        temporal_context=relationship.temporal_context,
        metadata=relationship.metadata or {}
    )

    db.add(db_relationship)
    await db.commit()
    await db.refresh(db_relationship)

    return RelationshipResponse.from_orm(db_relationship)


@router.get("/")
async def list_relationships(
    source_entity: str = Query(None, description="Filter by source entity ID"),
    target_entity: str = Query(None, description="Filter by target entity ID"),
    relationship_type: str = Query(None, description="Filter by relationship type"),
    confidence_min: float = Query(None, ge=0.0, le=1.0, description="Minimum confidence"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """List entity relationships with filtering."""

    # Build query
    query = "SELECT * FROM entity_relationships WHERE 1=1"
    params = {}

    if source_entity:
        query += " AND source_entity_id = :source_entity"
        params["source_entity"] = source_entity

    if target_entity:
        query += " AND target_entity_id = :target_entity"
        params["target_entity"] = target_entity

    if relationship_type:
        query += " AND relationship_type = :relationship_type"
        params["relationship_type"] = relationship_type

    if confidence_min is not None:
        query += " AND confidence >= :confidence_min"
        params["confidence_min"] = confidence_min

    query += " ORDER BY created_at DESC LIMIT :limit OFFSET :offset"
    params.update({"limit": limit, "offset": offset})

    # Get total count
    count_query = query.replace("SELECT *", "SELECT COUNT(*)", 1).replace(
        "ORDER BY created_at DESC LIMIT :limit OFFSET :offset", ""
    )
    total_result = await db.execute(count_query, params)
    total_count = total_result.scalar()

    # Get relationships
    result = await db.execute(query, params)
    relationships = result.fetchall()

    return {
        "relationships": [dict(rel) for rel in relationships],
        "total_count": total_count,
        "page": (offset // limit) + 1,
        "page_size": limit,
        "has_more": (offset + limit) < total_count
    }


@router.get("/graph/query", response_model=KnowledgeGraphQueryResponse)
async def query_knowledge_graph(
    request: KnowledgeGraphQueryRequest,
    db: AsyncSession = Depends(get_db)
) -> KnowledgeGraphQueryResponse:
    """Query knowledge graph for entity relationships."""

    # TODO: Implement actual knowledge graph querying
    # For now, return mock response

    return KnowledgeGraphQueryResponse(
        query_id=str(__import__("uuid").uuid4()),
        total_results=0,
        execution_time_ms=150,
        results={"entities": [], "relationships": []},
        knowledge_graph={"nodes": [], "edges": []}
    )


@router.get("/graph/traversal", response_model=GraphTraversalResponse)
async def traverse_graph(
    request: GraphTraversalRequest,
    db: AsyncSession = Depends(get_db)
) -> GraphTraversalResponse:
    """Traverse knowledge graph from starting entity."""

    # TODO: Implement actual graph traversal
    # For now, return mock response

    return GraphTraversalResponse(
        nodes=[],
        edges=[],
        path_count=0,
        execution_time_ms=200,
        metadata={
            "start_entity": request.start_entity,
            "max_hops": request.max_hops,
            "filters_applied": request.dict()
        }
    )
