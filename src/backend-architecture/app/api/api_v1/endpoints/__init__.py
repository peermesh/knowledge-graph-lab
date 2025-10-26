"""
API endpoint modules for the Backend Architecture Module.

This package contains all API endpoint implementations organized
by functionality (auth, entities, users, health, etc.).
"""

from .auth import router as auth_router
from .entities import router as entities_router
from .health import router as health_router
from .users import router as users_router

__all__ = ["auth_router", "entities_router", "health_router", "users_router"]
