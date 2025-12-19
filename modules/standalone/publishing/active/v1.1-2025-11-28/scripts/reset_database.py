#!/usr/bin/env python3
"""
Reset the publishing module database.

This script drops all tables and recreates them from scratch.
Useful for testing and development.

Usage:
    python3 scripts/reset_database.py

Warning: This will delete all data in the database!
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.publishing.core.database import drop_db_and_tables, create_db_and_tables
from src.publishing.core.config import settings
import structlog

logger = structlog.get_logger(__name__)


async def reset_database():
    """Drop and recreate all database tables."""
    logger.info("Starting database reset", database=settings.DATABASE_NAME)
    
    try:
        # Drop all tables
        logger.warning("⚠️  Dropping all database tables...")
        await drop_db_and_tables()
        
        # Recreate all tables
        logger.info("Creating fresh database tables...")
        await create_db_and_tables()
        
        logger.info("✅ Database reset completed successfully!")
        logger.info(f"Database: {settings.DATABASE_NAME}")
        logger.info(f"Host: {settings.DATABASE_HOST}:{settings.DATABASE_PORT}")
        
    except Exception as e:
        logger.error("❌ Database reset failed", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    print("=" * 60)
    print("⚠️  WARNING: This will delete ALL data in the database!")
    print("=" * 60)
    print(f"Database: {settings.DATABASE_NAME}")
    print(f"Host: {settings.DATABASE_HOST}:{settings.DATABASE_PORT}")
    print("=" * 60)
    
    response = input("\nAre you sure you want to continue? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("Reset cancelled.")
        sys.exit(0)
    
    print("\nResetting database...")
    asyncio.run(reset_database())
    print("\n✅ Done! Database has been reset to a fresh state.")

