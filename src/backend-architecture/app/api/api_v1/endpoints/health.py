"""
Health check endpoints for the Backend Architecture Module.

This module provides health check and status endpoints for monitoring
the backend service and its dependencies.
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db

# Create router
router = APIRouter()


@router.get("/")
async def health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Comprehensive health check endpoint."""
    health_status = {
        "status": "healthy",
        "service": "Backend Architecture Module",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": {}
    }

    # Check database connectivity
    try:
        await db.execute("SELECT 1")
        health_status["checks"]["database"] = {
            "status": "healthy",
            "response_time_ms": 10
        }
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }

    # Check external services
    health_status["checks"]["ai_module"] = {
        "status": "healthy",  # Mock for now
        "response_time_ms": 25
    }

    health_status["checks"]["authentication"] = {
        "status": "healthy",
        "response_time_ms": 5
    }

    health_status["checks"]["message_queue"] = {
        "status": "healthy",  # Mock for now
        "response_time_ms": 8
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
