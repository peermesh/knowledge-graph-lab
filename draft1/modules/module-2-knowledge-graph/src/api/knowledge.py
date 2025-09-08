"""
Knowledge graph query and search API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from ..core.database import get_db, Entity, Relationship
from ..services.rag_service import RAGService

router = APIRouter()

class EntityResponse(BaseModel):
    """Entity data response model"""
    id: int
    name: str
    entity_type: str
    description: Optional[str]
    confidence_score: float
    metadata: Dict[str, Any]
    created_at: str

class RelationshipResponse(BaseModel):
    """Relationship data response model"""
    id: int
    source_entity: EntityResponse
    target_entity: EntityResponse
    relationship_type: str
    confidence_score: float
    context: Optional[str]

class KnowledgeSearchRequest(BaseModel):
    """Request model for knowledge search"""
    query: str
    entity_types: Optional[List[str]] = None
    domains: Optional[List[str]] = None
    location: Optional[str] = None
    limit: int = 20

class SummaryRequest(BaseModel):
    """Request model for knowledge summary generation"""
    topic: str
    focus_areas: Optional[List[str]] = None
    max_entities: int = 10
    include_relationships: bool = True

@router.get("/search", response_model=List[EntityResponse])
async def search_knowledge(
    q: str = Query(..., description="Search query"),
    entity_type: Optional[str] = Query(None, description="Filter by entity type"),
    location: Optional[str] = Query(None, description="Filter by location"),
    limit: int = Query(20, description="Maximum results"),
    db: Session = Depends(get_db)
):
    """
    Search the knowledge graph using text queries
    
    Performs semantic search across entities and their descriptions.
    """
    query = db.query(Entity)
    
    # Text search across name and description
    search_filter = or_(
        Entity.name.ilike(f"%{q}%"),
        Entity.description.ilike(f"%{q}%")
    )
    query = query.filter(search_filter)
    
    # Filter by entity type
    if entity_type:
        query = query.filter(Entity.entity_type == entity_type)
    
    # Location filtering would require parsing metadata JSON
    # For now, simple string search in metadata
    if location:
        query = query.filter(Entity.metadata.ilike(f"%{location}%"))
    
    entities = query.order_by(Entity.confidence_score.desc()).limit(limit).all()
    
    return [
        EntityResponse(
            id=entity.id,
            name=entity.name,
            entity_type=entity.entity_type,
            description=entity.description,
            confidence_score=entity.confidence_score,
            metadata=_parse_metadata(entity.metadata),
            created_at=entity.created_at.isoformat()
        ) for entity in entities
    ]

@router.get("/entities", response_model=List[EntityResponse])
async def list_entities(
    entity_type: Optional[str] = None,
    domain: Optional[str] = None,
    location: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    List entities with filtering options
    """
    query = db.query(Entity)
    
    if entity_type:
        query = query.filter(Entity.entity_type == entity_type)
    
    # Domain and location filtering would require proper metadata parsing
    if domain:
        query = query.filter(Entity.metadata.ilike(f"%{domain}%"))
    
    if location:
        query = query.filter(Entity.metadata.ilike(f"%{location}%"))
    
    entities = query.order_by(Entity.created_at.desc()).limit(limit).all()
    
    return [
        EntityResponse(
            id=entity.id,
            name=entity.name,
            entity_type=entity.entity_type,
            description=entity.description,
            confidence_score=entity.confidence_score,
            metadata=_parse_metadata(entity.metadata),
            created_at=entity.created_at.isoformat()
        ) for entity in entities
    ]

@router.get("/entities/{entity_id}", response_model=EntityResponse)
async def get_entity(entity_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific entity
    """
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return EntityResponse(
        id=entity.id,
        name=entity.name,
        entity_type=entity.entity_type,
        description=entity.description,
        confidence_score=entity.confidence_score,
        metadata=_parse_metadata(entity.metadata),
        created_at=entity.created_at.isoformat()
    )

@router.get("/entities/{entity_id}/relationships", response_model=List[RelationshipResponse])
async def get_entity_relationships(
    entity_id: int,
    relationship_type: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get all relationships for a specific entity
    """
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    # Get both outgoing and incoming relationships
    query = db.query(Relationship).filter(
        or_(
            Relationship.source_id == entity_id,
            Relationship.target_id == entity_id
        )
    )
    
    if relationship_type:
        query = query.filter(Relationship.relationship_type == relationship_type)
    
    relationships = query.order_by(Relationship.confidence_score.desc()).limit(limit).all()
    
    result = []
    for rel in relationships:
        # Determine source and target based on perspective
        source = rel.source_entity
        target = rel.target_entity
        
        result.append(RelationshipResponse(
            id=rel.id,
            source_entity=EntityResponse(
                id=source.id,
                name=source.name,
                entity_type=source.entity_type,
                description=source.description,
                confidence_score=source.confidence_score,
                metadata=_parse_metadata(source.metadata),
                created_at=source.created_at.isoformat()
            ),
            target_entity=EntityResponse(
                id=target.id,
                name=target.name,
                entity_type=target.entity_type,
                description=target.description,
                confidence_score=target.confidence_score,
                metadata=_parse_metadata(target.metadata),
                created_at=target.created_at.isoformat()
            ),
            relationship_type=rel.relationship_type,
            confidence_score=rel.confidence_score,
            context=rel.context
        ))
    
    return result

@router.post("/summary")
async def generate_knowledge_summary(
    request: SummaryRequest,
    db: Session = Depends(get_db)
):
    """
    Generate an AI summary of knowledge about a specific topic
    
    Uses RAG to find relevant entities and relationships, then generates
    a coherent summary using an AI model.
    """
    try:
        rag_service = RAGService()
        
        summary = await rag_service.generate_summary(
            topic=request.topic,
            focus_areas=request.focus_areas,
            max_entities=request.max_entities,
            include_relationships=request.include_relationships
        )
        
        return {
            "topic": request.topic,
            "summary": summary,
            "generated_at": func.now().isoformat(),
            "model_used": "GPT-4"  # This would be dynamic
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")

@router.post("/query")
async def query_knowledge(
    query: str,
    context_limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Natural language query against the knowledge base
    
    Uses RAG to find relevant information and generate an AI response.
    """
    try:
        rag_service = RAGService()
        
        response = await rag_service.answer_query(
            query=query,
            context_limit=context_limit
        )
        
        return {
            "query": query,
            "answer": response["answer"],
            "sources": response["sources"],
            "confidence": response.get("confidence", 0.0),
            "generated_at": func.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")

@router.get("/stats")
async def get_knowledge_stats(db: Session = Depends(get_db)):
    """
    Get statistics about the knowledge graph
    """
    # Count entities by type
    entity_counts = {}
    for entity_type in ["platform", "creator", "organization", "policy", "grant", "event", "topic"]:
        count = db.query(Entity).filter(Entity.entity_type == entity_type).count()
        entity_counts[entity_type] = count
    
    total_entities = db.query(Entity).count()
    total_relationships = db.query(Relationship).count()
    
    # Average confidence scores
    avg_entity_confidence = db.query(func.avg(Entity.confidence_score)).scalar() or 0.0
    avg_relationship_confidence = db.query(func.avg(Relationship.confidence_score)).scalar() or 0.0
    
    return {
        "total_entities": total_entities,
        "total_relationships": total_relationships,
        "entity_counts": entity_counts,
        "average_confidence": {
            "entities": round(avg_entity_confidence, 3),
            "relationships": round(avg_relationship_confidence, 3)
        },
        "graph_density": round(total_relationships / max(total_entities, 1), 3)
    }

def _parse_metadata(metadata_str: Optional[str]) -> Dict[str, Any]:
    """Parse metadata JSON string safely"""
    if not metadata_str:
        return {}
    
    try:
        import json
        return json.loads(metadata_str)
    except (json.JSONDecodeError, TypeError):
        return {}