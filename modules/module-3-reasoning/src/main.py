"""
Knowledge Graph Lab - Module 3: Reasoning Engine & Content Synthesis
FastAPI application for intelligent content generation and decision making
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from .api import reasoning, content, digests, health
from .core.config import settings
from .core.database import init_db
from .services.reasoning_service import ReasoningService

# Global reasoning service instance
reasoning_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    global reasoning_service
    
    # Startup
    await init_db()
    reasoning_service = ReasoningService()
    await reasoning_service.initialize()
    
    yield
    
    # Shutdown
    if reasoning_service:
        await reasoning_service.cleanup()

app = FastAPI(
    title="KGL Reasoning & Content Synthesis Service",
    description="AI-powered content generation and intelligent decision making",
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
app.include_router(reasoning.router, prefix="/api/reasoning", tags=["reasoning"])
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(digests.router, prefix="/api/digests", tags=["digests"])

@app.get("/")
async def root():
    """Service information endpoint"""
    return {
        "service": "KGL Reasoning & Content Synthesis",
        "version": "1.0.0", 
        "status": "operational",
        "capabilities": [
            "Research priority intelligence",
            "Topic clustering and analysis",
            "Personalized digest generation",
            "Multi-channel content creation",
            "Conversational AI interface"
        ],
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=settings.DEBUG
    )