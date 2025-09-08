"""
Configuration management for ingestion service
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Service Configuration
    DEBUG: bool = True
    SERVICE_NAME: str = "kgl-ingestion"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./ingestion.db"
    
    # Redis for job queuing
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # Frontend dev server
        "http://localhost:8000",  # Main API gateway
    ]
    
    # Scraping Configuration
    USER_AGENT: str = "KGL-Research-Bot/1.0"
    REQUEST_DELAY: float = 1.0  # Delay between requests (seconds)
    MAX_CONCURRENT_REQUESTS: int = 3
    REQUEST_TIMEOUT: int = 30
    
    # API Keys (from environment)
    PERPLEXITY_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # Content Processing
    MAX_CONTENT_LENGTH: int = 50000  # Max characters per document
    MIN_CONTENT_LENGTH: int = 100    # Minimum viable content length
    
    # Rate Limiting
    RATE_LIMIT_PER_DOMAIN: int = 10  # Requests per minute per domain
    RESPECT_ROBOTS_TXT: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()