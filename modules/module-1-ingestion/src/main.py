"""
Knowledge Graph Lab - Module 1: Data Ingestion Service
FastAPI application for web scraping, API integration, and content normalization
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from .api import ingestion, sources, health
from .core.config import settings
from .core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="KGL Data Ingestion Service",
    description="Ethical web scraping and data normalization for autonomous research",
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
app.include_router(ingestion.router, prefix="/api/ingest", tags=["ingestion"])
app.include_router(sources.router, prefix="/api/sources", tags=["sources"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "KGL Data Ingestion",
        "version": "1.0.0", 
        "status": "operational",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.DEBUG
    )