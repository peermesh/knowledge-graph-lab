"""
Health check and monitoring endpoints for knowledge graph service
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text, func
import time

from ..core.database import get_db, Entity, Relationship, ResearchTopic
from ..core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Basic health check endpoint
    """
    return {
        "service": "KGL Knowledge Graph Service",
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": time.time()
    }

@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check including all system components
    """
    health_status = {
        "service": "KGL Knowledge Graph Service",
        "version": settings.VERSION,
        "timestamp": time.time(),
        "components": {}
    }
    
    # Check database connectivity
    try:
        db.execute(text("SELECT 1"))
        health_status["components"]["database"] = {
            "status": "healthy",
            "type": "sqlite" if "sqlite" in settings.DATABASE_URL else "postgresql"
        }
    except Exception as e:
        health_status["components"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Check Qdrant vector database
    try:
        # TODO: Implement actual Qdrant connectivity check
        health_status["components"]["vector_db"] = {
            "status": "not_implemented",
            "url": settings.QDRANT_URL,
            "collection": settings.QDRANT_COLLECTION_NAME
        }
    except Exception as e:
        health_status["components"]["vector_db"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Check AI model availability
    if settings.OPENAI_API_KEY:
        health_status["components"]["openai"] = {
            "status": "configured",
            "key_present": bool(settings.OPENAI_API_KEY)
        }
    else:
        health_status["components"]["openai"] = {
            "status": "not_configured",
            "message": "No API key provided"
        }
    
    # Check knowledge graph data
    try:
        entity_count = db.query(func.count(Entity.id)).scalar()
        relationship_count = db.query(func.count(Relationship.id)).scalar()
        topic_count = db.query(func.count(ResearchTopic.id)).scalar()
        
        health_status["components"]["knowledge_graph"] = {
            "status": "healthy",
            "entities": entity_count,
            "relationships": relationship_count,
            "research_topics": topic_count
        }
    except Exception as e:
        health_status["components"]["knowledge_graph"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Overall status
    unhealthy_components = [
        comp for comp, data in health_status["components"].items()
        if data["status"] == "unhealthy"
    ]
    
    health_status["status"] = "unhealthy" if unhealthy_components else "healthy"
    
    return health_status

@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    """
    Service metrics for monitoring and observability
    """
    try:
        # Entity metrics
        entity_metrics = {}
        for entity_type in ["platform", "creator", "organization", "policy", "grant", "event", "topic"]:
            count = db.query(Entity).filter(Entity.entity_type == entity_type).count()
            entity_metrics[entity_type] = count
        
        total_entities = sum(entity_metrics.values())
        total_relationships = db.query(Relationship).count()
        
        # Research metrics
        research_metrics = {
            "total_topics": db.query(ResearchTopic).count(),
            "pending_topics": db.query(ResearchTopic).filter(ResearchTopic.status == "pending").count(),
            "completed_topics": db.query(ResearchTopic).filter(ResearchTopic.status == "completed").count(),
        }
        
        # Quality metrics
        avg_entity_confidence = db.query(func.avg(Entity.confidence_score)).scalar() or 0.0
        avg_relationship_confidence = db.query(func.avg(Relationship.confidence_score)).scalar() or 0.0
        
        return {
            "service": "KGL Knowledge Graph Service",
            "timestamp": time.time(),
            "metrics": {
                "entities": {
                    "total": total_entities,
                    "by_type": entity_metrics,
                    "average_confidence": round(avg_entity_confidence, 3)
                },
                "relationships": {
                    "total": total_relationships,
                    "average_confidence": round(avg_relationship_confidence, 3)
                },
                "research": research_metrics,
                "graph_stats": {
                    "density": round(total_relationships / max(total_entities, 1), 3),
                    "avg_connections_per_entity": round((total_relationships * 2) / max(total_entities, 1), 2)
                }
            }
        }
        
    except Exception as e:
        return {
            "service": "KGL Knowledge Graph Service",
            "timestamp": time.time(),
            "error": f"Failed to collect metrics: {str(e)}",
            "metrics": {}
        }