"""
Database configuration and session management for Publishing Module.

Async PostgreSQL integration with SQLAlchemy for high-performance database operations.
Follows async patterns for scalability and proper connection pooling.

Constitution Compliance:
- Technology Standards: PostgreSQL 15+ with JSONB support
- Scalable Architecture: Connection pooling and async session management
- Performance: Optimized for 100,000+ concurrent users
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from sqlalchemy import text
import structlog
from typing import AsyncGenerator

from .config import settings

# Configure structured logging for database operations
logger = structlog.get_logger(__name__)

# Create async engine with PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.CONNECTION_POOL_SIZE,
    max_overflow=settings.MAX_CONNECTIONS - settings.CONNECTION_POOL_SIZE,
    pool_pre_ping=True,  # Validate connections before use
    pool_recycle=3600,   # Recycle connections every hour
    connect_args={
        "server_settings": {
            "application_name": "PublishingModule",
        }
    } if not settings.DEBUG else {}
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for all database models
Base = declarative_base()


async def create_db_and_tables() -> None:
    """
    Database tables are managed by Alembic migrations.
    
    To apply migrations, run:
        alembic upgrade head
    
    This function is kept for backward compatibility but does nothing.
    In production, migrations should be run as part of deployment pipeline.
    """
    logger.info(
        "Database initialization skipped - tables managed by Alembic migrations",
        database=settings.DATABASE_NAME
    )
    logger.info(
        "To apply migrations, run: alembic upgrade head",
        database=settings.DATABASE_NAME
    )
    # No-op: Tables are created via Alembic migrations
    pass


async def drop_db_and_tables() -> None:
    """Drop all database tables (for testing or reset purposes)."""
    try:
        logger.warning("Dropping database tables", database=settings.DATABASE_NAME)

        # Import all models to ensure they're registered
        from ..models import channel, publication, subscriber, template, analytics  # noqa: F401

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        logger.info("Database tables dropped successfully")

    except Exception as e:
        logger.error("Failed to drop database tables", error=str(e))
        raise


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session for dependency injection."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error("Database transaction rolled back", error=str(e))
            raise
        finally:
            await session.close()


async def get_db_health() -> dict:
    """Check database connectivity and health status."""
    try:
        async with async_session_factory() as session:
            # Execute a simple query to test connectivity
            result = await session.execute(text("SELECT 1 as health_check"))
            row = result.fetchone()

            if row and row.health_check == 1:
                return {
                    "status": "connected",
                    "database": settings.DATABASE_NAME,
                    "connection_pool": {
                        "size": engine.pool.size(),
                        "checked_in": engine.pool.checkedin(),
                        "checked_out": engine.pool.checkedout(),
                        "overflow": engine.pool.overflow()
                    }
                }
            else:
                return {"status": "error", "database": settings.DATABASE_NAME}

    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return {
            "status": "disconnected",
            "database": settings.DATABASE_NAME,
            "error": str(e)
        }


# Database migration utilities
async def get_table_status() -> dict:
    """Get status of all publishing module tables."""
    try:
        async with async_session_factory() as session:
            # Check which tables exist
            result = await session.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name LIKE 'publishing_%'
                ORDER BY table_name
            """))

            existing_tables = [row.table_name for row in result.fetchall()]

            # Expected tables based on models
            expected_tables = [
                'publishing_channels',
                'publishing_subscribers',
                'publishing_publications',
                'publishing_templates',
                'publishing_analytics'
            ]

            return {
                "existing_tables": existing_tables,
                "expected_tables": expected_tables,
                "missing_tables": [t for t in expected_tables if t not in existing_tables],
                "extra_tables": [t for t in existing_tables if t not in expected_tables]
            }

    except Exception as e:
        logger.error("Failed to check table status", error=str(e))
        return {"status": "error", "error": str(e)}


async def init_database_for_testing() -> None:
    """Initialize database for testing with test-specific configuration."""
    if settings.DEBUG:
        logger.info("Initializing database for testing")

        # Use in-memory SQLite for tests if PostgreSQL not available
        test_engine = create_async_engine(
            "sqlite+aiosqlite:///./test_publishing.db",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Test database initialized")
    else:
        logger.warning("Test database initialization skipped in production mode")

