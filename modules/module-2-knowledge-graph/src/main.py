"""
Knowledge Graph Lab - Module 2: AI Knowledge Graph & Research System
FastAPI application for autonomous research and knowledge graph management
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from .api import research, knowledge, entities, health
from .core.config import settings
from .core.database import init_db
from .services.research_service import ResearchService

# Global research service instance
research_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    global research_service
    
    # Startup
    await init_db()
    research_service = ResearchService()
    await research_service.initialize()
    
    yield
    
    # Shutdown
    if research_service:
        await research_service.cleanup()

app = FastAPI(
    title="KGL AI Knowledge Graph Service",
    description="Autonomous research system with intelligent knowledge graph",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])
app.include_router(entities.router, prefix="/api/entities", tags=["entities"])

@app.get("/")
async def root():
    """Service information endpoint"""
    return {
        "service": "KGL AI Knowledge Graph",
        "version": "1.0.0", 
        "status": "operational",
        "capabilities": [
            "Autonomous research",
            "Knowledge graph construction",
            "Entity relationship mapping",
            "RAG-based query answering"
        ],
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=settings.DEBUG
    )