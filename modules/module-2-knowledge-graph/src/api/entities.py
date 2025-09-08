"""
Entity management API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import json

from ..core.database import get_db, Entity, Relationship, EntityType

router = APIRouter()

class EntityCreate(BaseModel):
    """Request model for creating an entity"""
    name: str
    entity_type: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}
    source_urls: Optional[List[str]] = []

class EntityUpdate(BaseModel):
    """Request model for updating an entity"""
    name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None

class RelationshipCreate(BaseModel):
    """Request model for creating a relationship"""
    source_id: int
    target_id: int
    relationship_type: str
    context: Optional[str] = None
    confidence_score: float = 0.7
    source_urls: Optional[List[str]] = []

@router.get("/types")
async def list_entity_types():
    """
    Get list of supported entity types
    """
    return {
        "entity_types": [
            {
                "type": "platform",
                "description": "Social media platforms, content platforms",
                "examples": ["YouTube", "TikTok", "Instagram", "Substack"]
            },
            {
                "type": "creator",
                "description": "Content creators, influencers, artists",
                "examples": ["Individual creators", "Content teams"]
            },
            {
                "type": "organization",
                "description": "Companies, nonprofits, institutions",
                "examples": ["Creator funds", "Talent agencies", "Platform companies"]
            },
            {
                "type": "policy",
                "description": "Policies, regulations, terms of service",
                "examples": ["Platform policies", "Government regulations"]
            },
            {
                "type": "grant",
                "description": "Funding opportunities, grants, programs",
                "examples": ["Creator funds", "Grant programs"]
            },
            {
                "type": "event",
                "description": "Events, launches, announcements",
                "examples": ["Feature launches", "Policy changes", "Conferences"]
            },
            {
                "type": "topic",
                "description": "General topics and themes",
                "examples": ["Creator rights", "Monetization", "Content moderation"]
            }
        ]
    }

@router.post("/", response_model=dict)
async def create_entity(
    entity_data: EntityCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new entity in the knowledge graph
    """
    # Validate entity type
    if entity_data.entity_type not in [e.value for e in EntityType]:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid entity type. Must be one of: {[e.value for e in EntityType]}"
        )
    
    # Check if entity already exists
    existing = db.query(Entity).filter(
        Entity.name == entity_data.name,
        Entity.entity_type == entity_data.entity_type
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Entity '{entity_data.name}' of type '{entity_data.entity_type}' already exists"
        )
    
    # Create new entity
    entity = Entity(
        name=entity_data.name,
        entity_type=entity_data.entity_type,
        description=entity_data.description,
        metadata=json.dumps(entity_data.metadata) if entity_data.metadata else "{}",
        source_urls=json.dumps(entity_data.source_urls) if entity_data.source_urls else "[]",
        confidence_score=0.5  # Default confidence for manually created entities
    )
    
    db.add(entity)
    db.commit()
    db.refresh(entity)
    
    return {
        "id": entity.id,
        "message": f"Entity '{entity.name}' created successfully",
        "entity_type": entity.entity_type
    }

@router.put("/{entity_id}")
async def update_entity(
    entity_id: int,
    update_data: EntityUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing entity
    """
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    # Update fields if provided
    if update_data.name is not None:
        entity.name = update_data.name
    if update_data.description is not None:
        entity.description = update_data.description
    if update_data.metadata is not None:
        entity.metadata = json.dumps(update_data.metadata)
    if update_data.confidence_score is not None:
        entity.confidence_score = max(0.0, min(1.0, update_data.confidence_score))
    
    db.commit()
    
    return {"message": f"Entity '{entity.name}' updated successfully"}

@router.delete("/{entity_id}")
async def delete_entity(
    entity_id: int,
    cascade: bool = False,
    db: Session = Depends(get_db)
):
    """
    Delete an entity from the knowledge graph
    
    If cascade=True, also deletes all relationships involving this entity.
    """
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    entity_name = entity.name
    
    if cascade:
        # Delete all relationships involving this entity
        db.query(Relationship).filter(
            (Relationship.source_id == entity_id) | (Relationship.target_id == entity_id)
        ).delete()
    else:
        # Check if entity has relationships
        relationship_count = db.query(Relationship).filter(
            (Relationship.source_id == entity_id) | (Relationship.target_id == entity_id)
        ).count()
        
        if relationship_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Entity has {relationship_count} relationships. Use cascade=true to delete them."
            )
    
    db.delete(entity)
    db.commit()
    
    return {"message": f"Entity '{entity_name}' deleted successfully"}

@router.post("/relationships")
async def create_relationship(
    rel_data: RelationshipCreate,
    db: Session = Depends(get_db)
):
    """
    Create a relationship between two entities
    """
    # Verify both entities exist
    source = db.query(Entity).filter(Entity.id == rel_data.source_id).first()
    target = db.query(Entity).filter(Entity.id == rel_data.target_id).first()
    
    if not source:
        raise HTTPException(status_code=404, detail=f"Source entity {rel_data.source_id} not found")
    if not target:
        raise HTTPException(status_code=404, detail=f"Target entity {rel_data.target_id} not found")
    
    # Check if relationship already exists
    existing = db.query(Relationship).filter(
        Relationship.source_id == rel_data.source_id,
        Relationship.target_id == rel_data.target_id,
        Relationship.relationship_type == rel_data.relationship_type
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Relationship already exists between these entities"
        )
    
    # Create relationship
    relationship = Relationship(
        source_id=rel_data.source_id,
        target_id=rel_data.target_id,
        relationship_type=rel_data.relationship_type,
        context=rel_data.context,
        confidence_score=rel_data.confidence_score,
        source_urls=json.dumps(rel_data.source_urls) if rel_data.source_urls else "[]"
    )
    
    db.add(relationship)
    db.commit()
    
    return {
        "message": f"Relationship '{rel_data.relationship_type}' created between '{source.name}' and '{target.name}'",
        "relationship_id": relationship.id
    }

@router.get("/relationships/types")
async def list_relationship_types(db: Session = Depends(get_db)):
    """
    Get list of relationship types currently in use
    """
    from sqlalchemy import distinct
    
    relationship_types = db.query(distinct(Relationship.relationship_type)).all()
    
    return {
        "relationship_types": [rt[0] for rt in relationship_types],
        "common_types": [
            "owns", "created_by", "regulates", "funds", "competes_with",
            "partners_with", "acquired_by", "sponsors", "influences", "mentions"
        ]
    }

@router.delete("/relationships/{relationship_id}")
async def delete_relationship(
    relationship_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific relationship
    """
    relationship = db.query(Relationship).filter(Relationship.id == relationship_id).first()
    
    if not relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")
    
    source_name = relationship.source_entity.name
    target_name = relationship.target_entity.name
    rel_type = relationship.relationship_type
    
    db.delete(relationship)
    db.commit()
    
    return {
        "message": f"Relationship '{rel_type}' between '{source_name}' and '{target_name}' deleted"
    }

@router.get("/{entity_id}/similar")
async def find_similar_entities(
    entity_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Find entities similar to the given entity
    
    This is a placeholder - in a full implementation, this would use
    vector similarity search on entity embeddings.
    """
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    # Simple similarity based on entity type and partial name matching
    similar = db.query(Entity).filter(
        Entity.id != entity_id,
        Entity.entity_type == entity.entity_type
    ).limit(limit).all()
    
    return {
        "target_entity": {
            "id": entity.id,
            "name": entity.name,
            "type": entity.entity_type
        },
        "similar_entities": [
            {
                "id": e.id,
                "name": e.name,
                "type": e.entity_type,
                "confidence_score": e.confidence_score,
                "similarity_score": 0.5  # Placeholder
            } for e in similar
        ]
    }