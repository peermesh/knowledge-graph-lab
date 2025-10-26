"""
Configuration settings for Publishing Module.

Environment-based configuration with validation for all external services and
application settings. Follows 12-factor app principles.

Constitution Compliance:
- Technology Standards: Python 3.11+, PostgreSQL 15+, Redis 7.0+
- External Dependencies: AWS SES, Slack/Discord APIs
- Security: JWT authentication, secure credential management
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable validation."""

    # Application Info
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    PORT: int = 8080

    # Security
    SECRET_KEY: str
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Database (PostgreSQL 15+ with JSONB support)
    DATABASE_URL: str
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "publishing"
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    # Redis (7.0+ for caching and pub/sub)
    REDIS_URL: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None

    # Celery (5.3.0+ for background tasks)
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # AWS SES (Email service)
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    SES_SENDER_EMAIL: str = "noreply@knowledge-graph-lab.com"

    # Slack API
    SLACK_BOT_TOKEN: Optional[str] = None
    SLACK_CLIENT_ID: Optional[str] = None
    SLACK_CLIENT_SECRET: Optional[str] = None

    # Discord API
    DISCORD_BOT_TOKEN: Optional[str] = None
    DISCORD_CLIENT_ID: Optional[str] = None
    DISCORD_CLIENT_SECRET: Optional[str] = None

    # AI Module Integration
    AI_MODULE_URL: str = "http://localhost:8001"
    AI_API_KEY: Optional[str] = None

    # Backend Module Integration (JWT authentication)
    BACKEND_MODULE_URL: str = "http://localhost:8000"
    BACKEND_API_KEY: Optional[str] = None

    # Performance and Scaling
    MAX_WORKERS: int = 4
    CONNECTION_POOL_SIZE: int = 20
    MAX_CONNECTIONS: int = 100

    # Analytics and Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v, values):
        """Assemble database URL from individual components if not provided."""
        if v:
            return v

        return (
            f"postgresql+asyncpg://{values.get('DATABASE_USER')}:"
            f"{values.get('DATABASE_PASSWORD')}@"
            f"{values.get('DATABASE_HOST', 'localhost')}:"
            f"{values.get('DATABASE_PORT', 5432)}/"
            f"{values.get('DATABASE_NAME', 'publishing')}"
        )

    @validator("REDIS_URL", pre=True)
    def assemble_redis_url(cls, v, values):
        """Assemble Redis URL from individual components if not provided."""
        if v:
            return v

        auth = f":{values.get('REDIS_PASSWORD')}@" if values.get('REDIS_PASSWORD') else ""
        return f"redis://{auth}{values.get('REDIS_HOST', 'localhost')}:{values.get('REDIS_PORT', 6379)}"

    @validator("CELERY_BROKER_URL", pre=True)
    def assemble_celery_broker_url(cls, v, values):
        """Use Redis URL as Celery broker if not specified."""
        return v or values.get("REDIS_URL", "redis://localhost:6379")

    @validator("CELERY_RESULT_BACKEND", pre=True)
    def assemble_celery_result_backend(cls, v, values):
        """Use Redis URL as Celery result backend if not specified."""
        return v or values.get("REDIS_URL", "redis://localhost:6379")

    @validator("DEBUG", pre=True)
    def parse_debug(cls, v):
        """Parse DEBUG as boolean."""
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return bool(v)

    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        """Parse ALLOWED_HOSTS as list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",") if host.strip()]
        return v or ["localhost", "127.0.0.1"]

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS as list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v or ["http://localhost:3000"]


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()

