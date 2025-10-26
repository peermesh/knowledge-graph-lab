"""Health check API endpoints"""

from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai/v1", tags=["health"])


class ComponentHealth(BaseModel):
    """Health status for a component"""
    status: str  # healthy, degraded, unhealthy
    response_time_ms: int
    error_message: str = None


class HealthResponse(BaseModel):
    """Complete health check response"""
    status: str  # healthy, degraded, unhealthy
    version: str
    timestamp: str
    checks: Dict[str, ComponentHealth]


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check for AI module.
    
    Checks:
    - Database connectivity
    - Vector database (Qdrant) connectivity
    - LLM API availability
    - Message queue connectivity
    """
    checks = {}
    overall_status = "healthy"
    
    # Check database
    db_health = await _check_database()
    checks["database"] = db_health
    if db_health.status != "healthy":
        overall_status = "degraded" if overall_status == "healthy" else "unhealthy"
    
    # Check vector database
    vector_db_health = await _check_vector_db()
    checks["vector_db"] = vector_db_health
    if vector_db_health.status != "healthy":
        overall_status = "degraded" if overall_status == "healthy" else "unhealthy"
    
    # Check LLM APIs
    llm_health = await _check_llm_apis()
    checks["llm_apis"] = llm_health
    if llm_health.status != "healthy":
        overall_status = "degraded"  # LLM issues are degraded, not critical
    
    # Check message queue
    mq_health = await _check_message_queue()
    checks["message_queue"] = mq_health
    if mq_health.status != "healthy":
        overall_status = "degraded" if overall_status == "healthy" else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat(),
        checks=checks
    )


async def _check_database() -> ComponentHealth:
    """Check PostgreSQL database connectivity"""
    try:
        from src.ai.config import settings
        from sqlalchemy import create_engine, text
        
        start_time = time.time()
        
        # Create connection
        engine = create_engine(settings.database_url, pool_pre_ping=True)
        
        # Test query
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        response_time = int((time.time() - start_time) * 1000)
        
        return ComponentHealth(
            status="healthy",
            response_time_ms=response_time
        )
    
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return ComponentHealth(
            status="unhealthy",
            response_time_ms=0,
            error_message=str(e)
        )


async def _check_vector_db() -> ComponentHealth:
    """Check Qdrant vector database connectivity"""
    try:
        from src.ai.integrations.vector_db import vector_db_client
        
        start_time = time.time()
        
        # Check collection exists
        collections = vector_db_client.client.get_collections()
        
        response_time = int((time.time() - start_time) * 1000)
        
        return ComponentHealth(
            status="healthy",
            response_time_ms=response_time
        )
    
    except Exception as e:
        logger.error(f"Vector DB health check failed: {e}")
        return ComponentHealth(
            status="unhealthy",
            response_time_ms=0,
            error_message=str(e)
        )


async def _check_llm_apis() -> ComponentHealth:
    """Check LLM API availability"""
    try:
        from src.ai.config import settings
        
        start_time = time.time()
        
        # Simple check: verify API keys are configured
        if not settings.openai_api_key:
            return ComponentHealth(
                status="degraded",
                response_time_ms=0,
                error_message="OpenAI API key not configured"
            )
        
        # Could make actual API call for deeper check
        # For now, just verify configuration
        response_time = int((time.time() - start_time) * 1000)
        
        return ComponentHealth(
            status="healthy",
            response_time_ms=response_time
        )
    
    except Exception as e:
        logger.error(f"LLM API health check failed: {e}")
        return ComponentHealth(
            status="degraded",
            response_time_ms=0,
            error_message=str(e)
        )


async def _check_message_queue() -> ComponentHealth:
    """Check RabbitMQ connectivity"""
    try:
        from src.ai.integrations.message_queue import message_queue
        
        start_time = time.time()
        
        # Check connection is established
        if message_queue.connection and not message_queue.connection.is_closed:
            response_time = int((time.time() - start_time) * 1000)
            
            return ComponentHealth(
                status="healthy",
                response_time_ms=response_time
            )
        else:
            return ComponentHealth(
                status="unhealthy",
                response_time_ms=0,
                error_message="No active connection to RabbitMQ"
            )
    
    except Exception as e:
        logger.error(f"Message queue health check failed: {e}")
        return ComponentHealth(
            status="unhealthy",
            response_time_ms=0,
            error_message=str(e)
        )


@router.get("/health/live")
async def liveness_probe():
    """
    Liveness probe for container orchestration.
    
    Returns 200 if service is running (even if degraded).
    """
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness_probe():
    """
    Readiness probe for container orchestration.
    
    Returns 200 only if service is ready to accept traffic.
    """
    # Check critical dependencies
    db_health = await _check_database()
    
    if db_health.status == "healthy":
        return {"status": "ready"}
    else:
        return status.HTTP_503_SERVICE_UNAVAILABLE

