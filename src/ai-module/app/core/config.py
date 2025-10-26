"""
Configuration settings for the AI Development Module.

This module handles configuration management for the AI service including
database connections, API settings, and external service integrations.
"""

from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application settings
    app_name: str = Field(default="AI Development Module")
    version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    api_v1_prefix: str = Field(default="/api/v1")

    # Database settings
    postgres_url: str = Field(
        default="postgresql+asyncpg://ai_user:ai_password@localhost:5432/ai_module"
    )
    postgres_test_url: str = Field(
        default="postgresql+asyncpg://ai_user:ai_password@localhost:5432/ai_module_test"
    )

    # Vector database settings
    qdrant_url: str = Field(default="http://localhost:6333")
    qdrant_api_key: Optional[str] = Field(default=None)

    # Message queue settings
    rabbitmq_url: str = Field(default="amqp://guest:guest@localhost:5672/")
    rabbitmq_exchange: str = Field(default="ai_processing")

    # LLM provider settings
    openai_api_key: str = Field(default="your-openai-api-key-here")
    anthropic_api_key: str = Field(default="your-anthropic-api-key-here")
    default_llm_provider: str = Field(default="openai")  # openai, anthropic, local

    # Processing settings
    max_batch_size: int = Field(default=50)
    max_concurrent_jobs: int = Field(default=10)
    job_timeout_seconds: int = Field(default=300)
    max_retries: int = Field(default=3)

    # Performance settings
    embedding_dimensions: int = Field(default=768)
    confidence_threshold: float = Field(default=0.7)
    similarity_threshold: float = Field(default=0.8)

    # Security settings
    secret_key: str = Field(
        default="your-secret-key-change-in-production"
    )
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)

    # External service URLs
    backend_api_url: str = Field(default="http://localhost:8000")
    frontend_url: str = Field(default="http://localhost:3000")

    # Logging settings
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")

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
