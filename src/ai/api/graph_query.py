"""Knowledge graph query API endpoints"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import logging

from src.ai.api.dependencies import get_db
from src.ai.services.graph_query import graph_query
from src.ai.services.vector_search import vector_search

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai/v1", tags=["knowledge-graph"])


# Request/Response Models
class QueryFilters(BaseModel):
    """Filters for knowledge graph queries"""
    entity_types: Optional[List[str]] = None
    relationship_types: Optional[List[str]] = None
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    date_range: Optional[Dict[str, str]] = None
    limit: int = Field(default=50, ge=1, le=100)


class GraphQueryRequest(BaseModel):
    """Request for knowledge graph query"""
    query: str = Field(min_length=1, max_length=500)
    query_type: str = Field(description="entity_search, similarity_search, or relationship_query")
    filters: Optional[QueryFilters] = Field(default=None)


class RelationshipSummary(BaseModel):
    """Summary of an entity relationship"""
    target_entity: str
    target_entity_id: str
    relationship_type: str
    confidence: float
    direction: str  # incoming, outgoing, or bidirectional


class EntityWithRelationships(BaseModel):
    """Entity with its relationships"""
    id: str
    text: str
    type: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None
    relationships: Optional[List[RelationshipSummary]] = None


class GraphNode(BaseModel):
    """Node in knowledge graph visualization"""
    id: str
    label: str
    type: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None


class GraphEdge(BaseModel):
    """Edge in knowledge graph visualization"""
    source: str
    target: str
    type: str
    confidence: float
    weight: Optional[float] = None


class KnowledgeGraphVisualization(BaseModel):
    """Graph structure for visualization"""
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    layout: str = "force_directed"


class GraphQueryResponse(BaseModel):
    """Response from knowledge graph query"""
    query_id: str
    total_results: int
    execution_time_ms: int
    entities: List[EntityWithRelationships]
    knowledge_graph: Optional[KnowledgeGraphVisualization] = None


class SimilarityRequest(BaseModel):
    """Request for similarity search"""
    entity_id: Optional[str] = None
    text: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0)


class SimilarEntity(BaseModel):
    """Entity with similarity score"""
    entity: EntityWithRelationships
    similarity_score: float


class SimilarityResponse(BaseModel):
    """Response from similarity search"""
    similar_entities: List[SimilarEntity]
    execution_time_ms: int


@router.post("/graph/query", response_model=GraphQueryResponse)
async def query_graph(request: GraphQueryRequest, db: Session = Depends(get_db)):
    """
    Query knowledge graph for entities and relationships.
    
    Supports three query types:
    - entity_search: Search entities by text
    - similarity_search: Find similar entities using embeddings
    - relationship_query: Query specific relationships
    """
    import uuid
    import time
    
    start_time = time.time()
    query_id = str(uuid.uuid4())
    
    try:
        filters = request.filters or QueryFilters()
        
        if request.query_type == "entity_search":
            # Search entities by text
            results = await graph_query.query_entities(
                db=db,
                query_text=request.query,
                entity_types=filters.entity_types,
                confidence_threshold=filters.confidence_threshold,
                limit=filters.limit
            )
        
        elif request.query_type == "similarity_search":
            # Find similar entities using vector search
            results = await vector_search.search_similar_by_text(
                db=db,
                query_text=request.query,
                limit=filters.limit,
                confidence_threshold=filters.confidence_threshold,
                entity_types=filters.entity_types
            )
            # Convert similarity results to entity format
            results = [r['entity'] for r in results]
        
        elif request.query_type == "relationship_query":
            # Query specific relationships
            results = await graph_query.query_entities(
                db=db,
                query_text=request.query,
                entity_types=filters.entity_types,
                confidence_threshold=filters.confidence_threshold,
                limit=filters.limit
            )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid query_type: {request.query_type}"
            )
        
        # Convert results to response format
        entities = []
        for result in results:
            relationships = []
            for rel in result.get('relationships', []):
                relationships.append(RelationshipSummary(
                    target_entity=rel['target_entity'],
                    target_entity_id=rel['target_entity_id'],
                    relationship_type=rel['relationship_type'],
                    confidence=rel['confidence'],
                    direction=rel['direction']
                ))
            
            entities.append(EntityWithRelationships(
                id=result['id'],
                text=result['text'],
                type=result['type'],
                confidence=result['confidence'],
                metadata=result.get('metadata'),
                relationships=relationships if relationships else None
            ))
        
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        return GraphQueryResponse(
            query_id=query_id,
            total_results=len(entities),
            execution_time_ms=execution_time_ms,
            entities=entities
        )
    
    except Exception as e:
        logger.error(f"Graph query failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Graph query failed: {str(e)}"
        )


@router.get("/graph/entity/{entity_id}")
async def get_entity(
    entity_id: str,
    include_relationships: bool = True,
    relationship_depth: int = Query(default=1, ge=1, le=3),
    db: Session = Depends(get_db)
):
    """
    Get entity details with optional relationship traversal.
    
    Args:
        entity_id: Entity UUID
        include_relationships: Include relationships in response
        relationship_depth: Degrees of relationships to include (1-3)
    """
    try:
        result = await graph_query.get_entity_by_id(
            db=db,
            entity_id=entity_id,
            include_relationships=include_relationships,
            relationship_depth=relationship_depth
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Entity {entity_id} not found"
            )
        
        # Convert to response format
        relationships = []
        for rel in result.get('relationships', []):
            relationships.append(RelationshipSummary(
                target_entity=rel['target_entity'],
                target_entity_id=rel['target_entity_id'],
                relationship_type=rel['relationship_type'],
                confidence=rel['confidence'],
                direction=rel['direction']
            ))
        
        entity = EntityWithRelationships(
            id=result['id'],
            text=result['text'],
            type=result['type'],
            confidence=result['confidence'],
            metadata=result.get('metadata'),
            relationships=relationships if relationships else None
        )
        
        return {"entity": entity}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get entity failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Get entity failed: {str(e)}"
        )


@router.post("/graph/similarity", response_model=SimilarityResponse)
async def find_similar(request: SimilarityRequest, db: Session = Depends(get_db)):
    """
    Find entities similar to a given entity or text.
    
    Provide either entity_id or text, not both.
    """
    import time
    
    start_time = time.time()
    
    try:
        # Validate request
        if not request.entity_id and not request.text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Must provide either entity_id or text"
            )
        
        if request.entity_id and request.text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provide only one of entity_id or text, not both"
            )
        
        # Perform similarity search
        if request.entity_id:
            results = await vector_search.search_similar_by_entity(
                db=db,
                entity_id=request.entity_id,
                limit=request.limit,
                confidence_threshold=request.confidence_threshold
            )
        else:
            results = await vector_search.search_similar_by_text(
                db=db,
                query_text=request.text,
                limit=request.limit,
                confidence_threshold=request.confidence_threshold
            )
        
        # Convert to response format
        similar_entities = []
        for result in results:
            entity_data = result['entity']
            entity = EntityWithRelationships(
                id=entity_data['id'],
                text=entity_data['text'],
                type=entity_data['type'],
                confidence=entity_data['confidence'],
                metadata=entity_data.get('metadata')
            )
            
            similar_entities.append(SimilarEntity(
                entity=entity,
                similarity_score=result['similarity_score']
            ))
        
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        return SimilarityResponse(
            similar_entities=similar_entities,
            execution_time_ms=execution_time_ms
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Similarity search failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Similarity search failed: {str(e)}"
        )

