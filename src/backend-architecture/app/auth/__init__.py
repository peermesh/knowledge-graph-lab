"""
Authentication package for the Backend Architecture Module.

This package contains authentication utilities, security functions,
and session management for the backend service.
"""

from .security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    verify_password,
    get_password_hash,
    generate_session_id,
    check_permission,
)

__all__ = [
    "create_access_token",
    "create_refresh_token",
    "verify_token",
    "verify_password",
    "get_password_hash",
    "generate_session_id",
    "check_permission",
]
