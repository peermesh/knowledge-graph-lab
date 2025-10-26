"""
API v1 router for the AI Development Module.

This module defines all API endpoints for the AI service including
entity extraction, knowledge graph operations, and health checks.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from .endpoints import entities, health, relationships

# Create API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(entities.router, prefix="/entities", tags=["entities"])
api_router.include_router(relationships.router, prefix="/relationships", tags=["relationships"])
api_router.include_router(health.router, tags=["health"])
