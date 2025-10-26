"""
Core module for Publishing Module application.

Contains configuration, database, and logging setup for the publishing system.
Constitution compliance: All core services follow async patterns for scalability.
"""

from .config import settings
from .database import create_db_and_tables, get_async_session
from .logging import setup_logging

__all__ = [
    "settings",
    "create_db_and_tables",
    "get_async_session",
    "setup_logging"
]

