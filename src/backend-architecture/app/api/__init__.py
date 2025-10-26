"""
API package for the Backend Architecture Module.

This package contains all API endpoints organized by version and functionality.
"""

from .api_v1.api import api_router

__all__ = ["api_router"]
