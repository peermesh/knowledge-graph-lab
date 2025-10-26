"""
Database configuration and session management for the AI Development Module.

This module handles PostgreSQL database connections, session management,
and database utilities for the AI service.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .config import settings


# Database engine configuration
engine = create_async_engine(
    settings.postgres_url,
    echo=settings.debug,
    poolclass=StaticPool if settings.debug else None,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for database session management."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables() -> None:
    """Create all database tables."""
    from app.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    """Drop all database tables (for testing)."""
    from app.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
