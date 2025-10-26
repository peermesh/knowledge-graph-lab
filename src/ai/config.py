"""Configuration management for AI module"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "postgresql://ai_user:password@localhost:5432/ai_module"
    
    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    
    # RabbitMQ
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672"
    
    # LLM Providers
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Configuration
    env: str = "development"
    log_level: str = "INFO"
    processing_workers: int = 4
    max_daily_cost: float = 50.00
    
    # Performance
    max_concurrent_jobs: int = 100
    entity_extraction_timeout_seconds: int = 300
    graph_query_timeout_seconds: int = 30
    
    # Confidence Thresholds
    medium_confidence_threshold: float = 0.70
    high_confidence_threshold: float = 0.85
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env file


# Global settings instance
settings = Settings()

