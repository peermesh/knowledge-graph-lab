"""
API endpoint modules for the AI Development Module.

This package contains all API endpoint implementations organized
by functionality (entities, relationships, health, etc.).
"""

from .entities import router as entities_router
from .health import router as health_router
from .relationships import router as relationships_router

__all__ = ["entities_router", "health_router", "relationships_router"]
