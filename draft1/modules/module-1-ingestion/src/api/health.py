"""
Health check and monitoring endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import time

from ..core.database import get_db
from ..core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Basic health check endpoint
    """
    return {
        "service": "KGL Ingestion Service",
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": time.time()
    }

@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check including database connectivity
    """
    health_status = {
        "service": "KGL Ingestion Service",
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
    
    # Check configuration
    health_status["components"]["configuration"] = {
        "status": "healthy",
        "debug_mode": settings.DEBUG,
        "request_delay": settings.REQUEST_DELAY,
        "max_concurrent": settings.MAX_CONCURRENT_REQUESTS
    }
    
    # TODO: Add Redis connectivity check
    health_status["components"]["redis"] = {
        "status": "not_implemented",
        "message": "Redis connectivity check not yet implemented"
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
    Basic service metrics for monitoring
    """
    # TODO: Implement actual metrics collection
    return {
        "service": "KGL Ingestion Service",
        "metrics": {
            "total_jobs": 0,
            "pending_jobs": 0,
            "completed_jobs": 0,
            "failed_jobs": 0,
            "active_sources": 0,
            "content_items": 0
        },
        "timestamp": time.time()
    }