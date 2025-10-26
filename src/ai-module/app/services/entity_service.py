"""
Entity service for business logic operations.

This module contains the business logic for entity extraction,
validation, and management operations.
"""

import uuid
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Entity, EntityRelationship, KnowledgeGraphNode


class EntityService:
    """Service class for entity operations."""

    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db

    async def create_entity(
        self,
        name: str,
        entity_type: str,
        confidence: float,
        source: str,
        source_type: str,
        metadata: Optional[dict] = None,
        positions: Optional[List[List[int]]] = None
    ) -> Entity:
        """Create a new entity."""
        entity = Entity(
            name=name,
            type=entity_type,
            confidence=confidence,
            source=source,
            source_type=source_type,
            metadata=metadata or {},
            positions=positions,
            extraction_method="llm"
        )

        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)

        return entity

    async def get_entity_by_id(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID."""
        result = await self.db.execute(
            "SELECT * FROM entities WHERE id = :entity_id AND is_active = true",
            {"entity_id": entity_id}
        )
        return result.first()

    async def search_entities(
        self,
        query: str,
        entity_types: Optional[List[str]] = None,
        confidence_min: Optional[float] = None,
        limit: int = 50
    ) -> List[Entity]:
        """Search entities by text query."""
        # TODO: Implement full-text search with vector similarity
        # For now, simple name matching

        search_query = "SELECT * FROM entities WHERE is_active = true AND name ILIKE :query"
        params = {"query": f"%{query}%"}

        if entity_types:
            search_query += " AND type = ANY(:entity_types)"
            params["entity_types"] = entity_types

        if confidence_min is not None:
            search_query += " AND confidence >= :confidence_min"
            params["confidence_min"] = confidence_min

        search_query += " ORDER BY confidence DESC LIMIT :limit"
        params["limit"] = limit

        result = await self.db.execute(search_query, params)
        return result.fetchall()

    async def create_relationship(
        self,
        source_entity_id: str,
        target_entity_id: str,
        relationship_type: str,
        confidence: float,
        evidence: str,
        strength: Optional[float] = None,
        metadata: Optional[dict] = None
    ) -> EntityRelationship:
        """Create a relationship between two entities."""
        relationship = EntityRelationship(
            source_entity_id=source_entity_id,
            target_entity_id=target_entity_id,
            relationship_type=relationship_type,
            confidence=confidence,
            strength=strength,
            evidence=evidence,
            metadata=metadata or {}
        )

        self.db.add(relationship)
        await self.db.commit()
        await self.db.refresh(relationship)

        return relationship
