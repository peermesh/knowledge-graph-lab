"""
Configuration settings for the Backend Architecture Module.

This module handles configuration management for the backend service including
database connections, API settings, authentication, and external integrations.
"""

from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application settings
    app_name: str = Field(default="Backend Architecture Module")
    version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    api_v1_prefix: str = Field(default="/api/v1")

    # Database settings
    postgres_url: str = Field(
        default="postgresql+asyncpg://backend_user:backend_password@localhost:5432/backend_module"
    )
    postgres_test_url: str = Field(
        default="postgresql+asyncpg://backend_user:backend_password@localhost:5432/backend_module_test"
    )

    # Message queue settings
    rabbitmq_url: str = Field(default="amqp://guest:guest@localhost:5672/")
    rabbitmq_exchange: str = Field(default="backend_processing")

    # Redis settings (for caching and sessions)
    redis_url: str = Field(default="redis://localhost:6379")
    redis_cache_ttl: int = Field(default=3600)  # 1 hour

    # Authentication settings
    secret_key: str = Field(
        default="your-secret-key-change-in-production"
    )
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)

    # API settings
    max_request_size: str = Field(default="10MB")
    rate_limit_per_minute: int = Field(default=1000)
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"]
    )

    # External service URLs
    ai_module_url: str = Field(default="http://localhost:8001")
    frontend_url: str = Field(default="http://localhost:3000")
    publishing_module_url: str = Field(default="http://localhost:8002")

    # Logging settings
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")

    # WebSocket settings
    websocket_ping_interval: int = Field(default=20)
    websocket_ping_timeout: int = Field(default=10)
    websocket_max_connections: int = Field(default=1000)

    # Monitoring settings
    sentry_dsn: Optional[str] = Field(default=None)
    enable_metrics: bool = Field(default=True)

    # Testing settings
    test_database_url: str = Field(
        default="postgresql+asyncpg://test:test@localhost:5432/test_db"
    )

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
