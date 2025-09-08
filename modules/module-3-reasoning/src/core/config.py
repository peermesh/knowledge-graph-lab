"""
Configuration management for reasoning service
"""

from pydantic_settings import BaseSettings
from typing import List, Dict
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Service Configuration
    DEBUG: bool = True
    SERVICE_NAME: str = "kgl-reasoning"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./reasoning.db"
    
    # Redis for caching and queues
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # Frontend dev server
        "http://localhost:8000",  # Main API gateway
        "http://localhost:8001",  # Ingestion service
        "http://localhost:8002",  # Knowledge graph service
    ]
    
    # AI/ML Configuration
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # Content Generation Models
    DEFAULT_MODEL: str = "gpt-4"
    FALLBACK_MODEL: str = "gpt-3.5-turbo"
    LOCAL_MODEL_ENDPOINT: str = ""  # For Ollama or local models
    
    # Content Generation Settings
    MAX_DIGEST_LENGTH: int = 2000  # Maximum words in a digest
    MAX_SOCIAL_LENGTH: int = 280   # Maximum characters for social posts
    CONTENT_TEMPERATURE: float = 0.7  # AI creativity level
    
    # Priority Scoring
    PRIORITY_WEIGHTS: Dict[str, float] = {
        "user_interest": 0.3,
        "recency": 0.25,
        "novelty": 0.2,
        "importance": 0.15,
        "credibility": 0.1
    }
    
    # Topic Clustering
    CLUSTERING_SIMILARITY_THRESHOLD: float = 0.7
    MIN_CLUSTER_SIZE: int = 3
    MAX_CLUSTERS_PER_DOMAIN: int = 20
    
    # User Personalization
    DEFAULT_USER_INTERESTS: List[str] = [
        "creator-economy",
        "platform-updates",
        "monetization"
    ]
    
    # Content Templates
    EMAIL_TEMPLATE_PATH: str = "templates/email/"
    SOCIAL_TEMPLATE_PATH: str = "templates/social/"
    
    # External Service URLs
    KNOWLEDGE_GRAPH_URL: str = "http://localhost:8002"
    INGESTION_SERVICE_URL: str = "http://localhost:8001"
    
    # Content Quality Control
    MIN_CONTENT_QUALITY_SCORE: float = 0.6
    ENABLE_FACT_CHECKING: bool = True
    ENABLE_BIAS_DETECTION: bool = True
    
    # Digest Generation
    DIGEST_FREQUENCY_OPTIONS: List[str] = ["daily", "weekly", "monthly"]
    DEFAULT_DIGEST_FREQUENCY: str = "weekly"
    MAX_ENTITIES_PER_DIGEST: int = 15
    
    # Social Media Platforms
    SUPPORTED_PLATFORMS: Dict[str, Dict[str, int]] = {
        "twitter": {"max_length": 280, "max_hashtags": 3},
        "linkedin": {"max_length": 3000, "max_hashtags": 5},
        "instagram": {"max_length": 2200, "max_hashtags": 10},
        "facebook": {"max_length": 63206, "max_hashtags": 3}
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()