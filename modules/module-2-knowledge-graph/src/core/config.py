"""
Configuration management for knowledge graph service
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Service Configuration
    DEBUG: bool = True
    SERVICE_NAME: str = "kgl-knowledge-graph"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./knowledge_graph.db"
    
    # Vector Database (Qdrant)
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_NAME: str = "kgl_knowledge"
    EMBEDDING_DIMENSION: int = 384  # sentence-transformers dimension
    
    # Redis for caching and queues
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # Frontend dev server
        "http://localhost:8000",  # Main API gateway
        "http://localhost:8001",  # Ingestion service
    ]
    
    # AI/ML Configuration
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    PERPLEXITY_API_KEY: str = ""
    
    # Embedding Model
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Research Configuration
    MAX_RESEARCH_DEPTH: int = 3  # How deep to go in autonomous research
    RESEARCH_BATCH_SIZE: int = 5  # Number of topics to research simultaneously
    
    # Entity Extraction
    NER_MODEL: str = "en_core_web_sm"  # spaCy model
    CUSTOM_ENTITY_TYPES: List[str] = [
        "PLATFORM", "CREATOR", "ORGANIZATION", "POLICY", "GRANT", "EVENT"
    ]
    
    # Knowledge Graph
    MAX_RELATIONSHIPS_PER_ENTITY: int = 50
    RELATIONSHIP_CONFIDENCE_THRESHOLD: float = 0.7
    
    # Research Priorities
    DEFAULT_RESEARCH_DOMAINS: List[str] = [
        "creator-economy",
        "platform-policies", 
        "monetization-strategies",
        "content-regulation"
    ]
    
    # Geographic Scope
    DEFAULT_LOCATIONS: List[str] = ["Boulder, CO", "Colorado", "United States"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()