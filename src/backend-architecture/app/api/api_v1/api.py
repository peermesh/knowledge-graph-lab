"""
API v1 router for the Backend Architecture Module.

This module defines all API endpoints for the backend service including
authentication, user management, entities, and system operations.
"""

from fastapi import APIRouter

from .endpoints import auth, entities, health, users

# Create API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(entities.router, prefix="/entities", tags=["entities"])
api_router.include_router(health.router, tags=["health"])
