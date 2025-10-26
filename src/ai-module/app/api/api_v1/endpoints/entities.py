"""
Entity API endpoints for the AI Development Module.

This module provides REST API endpoints for entity management including
CRUD operations, search, and extraction from documents.
"""

import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db
from ....models import Entity
from ....schemas.entity import (
    EntityCreate,
    EntityResponse,
    EntityUpdate,
    EntityListResponse,
    EntityExtractionRequest,
    EntityExtractionResponse,
)

# Create router
router = APIRouter()


@router.post("/", response_model=EntityResponse)
async def create_entity(
    entity: EntityCreate,
    db: AsyncSession = Depends(get_db)
) -> EntityResponse:
    """Create a new entity."""
    # Check if entity with same name and type already exists
    existing = await db.execute(
        "SELECT * FROM entities WHERE name = :name AND type = :type AND is_active = true",
        {"name": entity.name, "type": entity.type}
    )
    if existing.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Entity with name '{entity.name}' and type '{entity.type}' already exists"
        )

    # Create new entity
    db_entity = Entity(
        name=entity.name,
        type=entity.type,
        confidence=entity.confidence,
        source=entity.source,
        source_type=entity.source_type,
        source_document_id=entity.metadata.get("source_document_id") if entity.metadata else None,
        extraction_method="manual",  # Manual creation via API
        positions=entity.positions,
        metadata=entity.metadata or {},
        vector_embedding=None,  # Will be generated asynchronously
    )

    db.add(db_entity)
    await db.commit()
    await db.refresh(db_entity)

    return EntityResponse.from_orm(db_entity)


@router.get("/", response_model=EntityListResponse)
async def list_entities(
    entity_type: Optional[str] = Query(None, description="Filter by entity type"),
    confidence_min: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum confidence score"),
    source: Optional[str] = Query(None, description="Filter by source"),
    limit: int = Query(50, ge=1, le=100, description="Results per page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db)
) -> EntityListResponse:
    """List entities with filtering and pagination."""

    # Build query
    query = "SELECT * FROM entities WHERE is_active = true"
    params = {}

    if entity_type:
        query += " AND type = :entity_type"
        params["entity_type"] = entity_type

    if confidence_min is not None:
        query += " AND confidence >= :confidence_min"
        params["confidence_min"] = confidence_min

    if source:
        query += " AND source = :source"
        params["source"] = source

    query += " ORDER BY created_at DESC LIMIT :limit OFFSET :offset"
    params.update({"limit": limit, "offset": offset})

    # Get total count
    count_query = query.replace("SELECT *", "SELECT COUNT(*)", 1).replace(
        "ORDER BY created_at DESC LIMIT :limit OFFSET :offset", ""
    )
    total_result = await db.execute(count_query, params)
    total_count = total_result.scalar()

    # Get entities
    result = await db.execute(query, params)
    entities = result.fetchall()

    # Calculate pagination info
    has_more = (offset + limit) < total_count

    return EntityListResponse(
        entities=[EntityResponse.from_orm(entity) for entity in entities],
        total_count=total_count,
        page=(offset // limit) + 1,
        page_size=limit,
        has_more=has_more
    )


@router.get("/{entity_id}", response_model=EntityResponse)
async def get_entity(
    entity_id: str,
    db: AsyncSession = Depends(get_db)
) -> EntityResponse:
    """Get entity by ID."""
    result = await db.execute(
        "SELECT * FROM entities WHERE id = :entity_id AND is_active = true",
        {"entity_id": entity_id}
    )

    entity = result.first()
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity with ID {entity_id} not found"
        )

    return EntityResponse.from_orm(entity)


@router.put("/{entity_id}", response_model=EntityResponse)
async def update_entity(
    entity_id: str,
    entity_update: EntityUpdate,
    db: AsyncSession = Depends(get_db)
) -> EntityResponse:
    """Update an existing entity."""
    # Get existing entity
    result = await db.execute(
        "SELECT * FROM entities WHERE id = :entity_id AND is_active = true",
        {"entity_id": entity_id}
    )

    entity = result.first()
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity with ID {entity_id} not found"
        )

    # Update fields
    update_data = entity_update.dict(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(entity, field, value)

        await db.commit()
        await db.refresh(entity)

    return EntityResponse.from_orm(entity)


@router.delete("/{entity_id}")
async def delete_entity(
    entity_id: str,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Soft delete an entity (mark as inactive)."""
    result = await db.execute(
        "SELECT * FROM entities WHERE id = :entity_id AND is_active = true",
        {"entity_id": entity_id}
    )

    entity = result.first()
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity with ID {entity_id} not found"
        )

    # Soft delete
    entity.is_active = False
    await db.commit()

    return {"message": f"Entity {entity_id} deleted successfully"}


@router.post("/extract", response_model=EntityExtractionResponse)
async def extract_entities(
    request: EntityExtractionRequest,
    db: AsyncSession = Depends(get_db)
) -> EntityExtractionResponse:
    """Extract entities from document content."""

    # TODO: Implement actual entity extraction logic
    # For now, return a mock response

    job_id = str(uuid.uuid4())

    # Create processing job
    from ....models import DocumentProcessingJob

    job = DocumentProcessingJob(
        document_id=request.document_id,
        status="processing",
        priority=request.priority,
        extraction_config=request.extraction_config.dict(),
    )

    db.add(job)
    await db.commit()

    # Mock entity extraction results
    mock_entities = [
        {
            "id": str(uuid.uuid4()),
            "name": "Example Corp",
            "type": "organization",
            "confidence": 0.95,
            "source": request.document_id or "manual",
            "source_type": request.document_type,
            "extraction_method": "llm",
            "metadata": {},
            "positions": [[0, 12]],
            "created_at": "2025-01-23T12:00:00Z",
            "updated_at": "2025-01-23T12:00:00Z",
            "is_active": True
        }
    ]

    return EntityExtractionResponse(
        job_id=job_id,
        status="completed",
        entities=mock_entities,
        relationships=[],
        processing_time_seconds=2.5
    )
