"""
API router for Publishing Module.

Centralized API routing with proper error handling, validation, and response formatting.
Follows RFC7807 Problem Details for error responses and standard data/meta/errors format.

Constitution Compliance:
- Comprehensive Analytics Integration: API endpoints for engagement tracking
- Scalable Architecture: Async endpoints with proper error handling
- Performance: Optimized response times and structured logging
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import structlog
import time
from typing import Dict, Any
from datetime import datetime
import uuid

from ..core.config import settings
from ..core.logging import get_logger

# Import API routers for each domain
from . import publications, channels, subscribers, analytics

# Create main API router
router = APIRouter()

# Configure structured logging
logger = get_logger(__name__)


@router.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "data": {
            "name": "Publishing Module API",
            "version": settings.VERSION,
            "description": "Multi-channel content publishing system with AI-powered personalization",
            "health": "/health",
            "docs": "/api/v1/docs"
        },
        "meta": {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid.uuid4())
        },
        "errors": []
    }


# Include all domain routers
router.include_router(
    publications.router,
    prefix="/publications",
    tags=["publications"]
)

router.include_router(
    channels.router,
    prefix="/channels",
    tags=["channels"]
)

router.include_router(
    subscribers.router,
    prefix="/subscribers",
    tags=["subscribers"]
)

router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["analytics"]
)

# Health endpoints are included in the main app, not here


# Global exception handler for consistent error responses
@router.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions with proper error formatting."""

    correlation_id = getattr(request.state, 'correlation_id', str(uuid.uuid4()))

    # Log the error with full context
    logger.error(
        "Unhandled exception",
        correlation_id=correlation_id,
        error_type=type(exc).__name__,
        error_message=str(exc),
        url=str(request.url),
        method=request.method
    )

    # Return RFC7807 Problem Details format
    return JSONResponse(
        status_code=500,
        content={
            "data": {},
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": correlation_id
            },
            "errors": [{
                "type": "https://api.knowledge-graph-lab.com/errors/internal-server-error",
                "title": "Internal Server Error",
                "status": 500,
                "detail": "An unexpected error occurred while processing your request",
                "instance": str(request.url)
            }]
        }
    )


# Request validation middleware
async def validate_request(request: Request):
    """Validate incoming requests for security and format."""
    # Check for required headers
    if not request.headers.get("content-type"):
        if request.method in ["POST", "PUT", "PATCH"]:
            raise HTTPException(
                status_code=400,
                detail="Content-Type header is required"
            )

    # Validate request size (prevent DoS attacks)
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(
            status_code=413,
            detail="Request too large"
        )


# Add request validation to all routes
for route in router.routes:
    if hasattr(route, 'endpoint'):
        original_endpoint = route.endpoint

        async def validated_endpoint(request: Request):
            await validate_request(request)
            return await original_endpoint(request)

        route.endpoint = validated_endpoint


logger.info("API router configured successfully", routes=len(router.routes))

