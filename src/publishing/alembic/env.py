from logging.config import fileConfig

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool

from alembic import context

# Add path setup for imports
import sys
import os
from pathlib import Path
# Add the project root to sys.path (go up from alembic/env.py -> publishing -> src -> root)
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Get database URL from environment variables (avoid importing settings which triggers database init)
# Construct database URL manually to avoid importing database module
db_user = os.getenv('DATABASE_USER', 'publishing_user')
db_password = os.getenv('DATABASE_PASSWORD', 'publishing_pass')
db_host = os.getenv('DATABASE_HOST', 'localhost')
db_port = os.getenv('DATABASE_PORT', '5432')
db_name = os.getenv('DATABASE_NAME', 'publishing_db')

# Import Base and models
# Note: This will create an async engine, but that's OK - we just need the Base metadata
from src.publishing.core.database import Base

# Import all models to ensure they're registered with Base
from src.publishing.models import channel, publication, subscriber, template, analytics  # noqa: F401

# Import all models to ensure they're registered with Base
from src.publishing.models import channel, publication, subscriber, template, analytics  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata from your models
target_metadata = Base.metadata

# Set database URL (convert to sync format for Alembic)
# Alembic works with synchronous engines, so we use postgresql:// not postgresql+asyncpg://
sync_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
config.set_main_option('sqlalchemy.url', sync_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    Note: Alembic doesn't support async SQLAlchemy directly, so we use
    a synchronous engine for migrations. The database URL is already
    converted to sync format above.
    """
    # Create sync engine for migrations (Alembic doesn't support async directly)
    # The URL is already converted to sync format in the config above
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
