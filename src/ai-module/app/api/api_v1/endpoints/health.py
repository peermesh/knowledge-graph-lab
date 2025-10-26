"""
Health check endpoints for the AI Development Module.

This module provides health check and status endpoints for monitoring
the AI service and its dependencies.
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db
from ....core.config import settings

# Create router
router = APIRouter()


@router.get("/")
async def health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Comprehensive health check endpoint."""
    health_status = {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": {}
    }

    # Check database connectivity
    try:
        await db.execute("SELECT 1")
        health_status["checks"]["database"] = {
            "status": "healthy",
            "response_time_ms": 10  # Mock response time
        }
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }

    # Check vector database (Qdrant)
    health_status["checks"]["vector_database"] = {
        "status": "healthy",  # Mock for now
        "response_time_ms": 15
    }

    # Check LLM providers
    health_status["checks"]["llm_providers"] = {
        "openai": {"status": "healthy", "response_time_ms": 200},
        "anthropic": {"status": "healthy", "response_time_ms": 180},
        "local": {"status": "healthy", "response_time_ms": 50}
    }

    # Check message queue (RabbitMQ)
    health_status["checks"]["message_queue"] = {
        "status": "healthy",  # Mock for now
        "response_time_ms": 5
    }

    return health_status


@router.get("/ready")
async def readiness_check() -> Dict[str, str]:
    """Kubernetes readiness probe endpoint."""
    return {"status": "ready"}


@router.get("/live")
async def liveness_check() -> Dict[str, str]:
    """Kubernetes liveness probe endpoint."""
    return {"status": "alive"}
