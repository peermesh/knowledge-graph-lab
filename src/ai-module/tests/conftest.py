"""
Pytest configuration and fixtures for AI module tests.

This module provides test configuration, database setup, and
common fixtures for testing the AI module.
"""

import asyncio
import os
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Test database configuration
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://test:test@localhost:5432/test_db"
)

# Create test database engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,  # Don't echo SQL in tests
)

# Test session factory
TestingSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(autouse=True)
async def clean_db():
    """Clean database before each test."""
    # Clear all data between tests
    async with test_engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: sync_conn.execute("DELETE FROM entities"))
        await conn.run_sync(lambda sync_conn: sync_conn.execute("DELETE FROM entity_relationships"))
        await conn.run_sync(lambda sync_conn: sync_conn.execute("DELETE FROM knowledge_graph_nodes"))
        await conn.run_sync(lambda sync_conn: sync_conn.execute("DELETE FROM knowledge_graph_edges"))


@pytest.fixture
def sample_entity_data():
    """Provide sample entity data for tests."""
    return {
        "name": "Test Organization",
        "type": "organization",
        "confidence": 0.95,
        "source": "test_document",
        "source_type": "text",
        "extraction_method": "llm",
        "metadata": {"description": "A test organization"},
        "positions": [[0, 16]]
    }


@pytest.fixture
def sample_relationship_data():
    """Provide sample relationship data for tests."""
    return {
        "source_entity_id": "test-source-id",
        "target_entity_id": "test-target-id",
        "relationship_type": "partner",
        "confidence": 0.87,
        "evidence": "Test evidence text",
        "strength": 0.8,
        "metadata": {"context": "Business partnership"}
    }
