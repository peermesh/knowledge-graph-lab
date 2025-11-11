"""Shared FastAPI dependencies."""

from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.ai.config import settings

# Create SQLAlchemy engine and session factory
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Iterator[Session]:
    """
    Provide a transactional scope around a series of operations.

    Yields a database session and ensures it is closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

