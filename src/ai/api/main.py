"""FastAPI application - main entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.ai.api.extraction import router as extraction_router
from src.ai.api.graph_query import router as graph_router
from src.ai.api.websocket import router as websocket_router
from src.ai.api.quality import router as quality_router
from src.ai.api.health import router as health_router
from src.ai.api.middleware.rate_limit import RateLimitMiddleware
from src.ai.lib.logging_config import setup_structured_logging
from src.ai.config import settings

# Configure structured logging
if settings.env == "production":
    setup_structured_logging(settings.log_level)
else:
    # Use simple logging for development
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Development Module",
    description="""
# AI Development Module API

Transform unstructured text into structured knowledge through entity extraction, 
relationship mapping, and knowledge graph construction.

## Features

- **Entity Extraction**: Extract organizations, people, funding amounts, dates, and locations with confidence scoring
- **Knowledge Graph**: Query and traverse entity relationships with 3-degree depth
- **Vector Search**: Find similar entities using semantic embeddings
- **Real-time Updates**: WebSocket support for live graph updates
- **Quality Monitoring**: Track extraction accuracy and performance metrics
- **Multi-language**: Support for English, Spanish, French, and Chinese

## Performance

- 100-200 documents/hour processing capacity
- <5 seconds (p95) entity extraction latency
- <2 seconds (p95) knowledge graph query latency
- 500+ concurrent queries supported

## Rate Limits

- 100 requests per minute per client
- 1000 requests per hour per client

## Authentication

All endpoints except /health require JWT bearer token authentication.

## Getting Started

1. Start services: `docker-compose up -d`
2. Configure environment: Copy `.env.example` to `.env` and add API keys
3. Run migrations: `alembic upgrade head`
4. Start API: `uvicorn src.ai.api.main:app --reload`
5. View docs: http://localhost:8000/docs

## API Documentation

- **Swagger UI**: `/docs` (interactive API testing)
- **ReDoc**: `/redoc` (detailed documentation)
- **OpenAPI Spec**: `/openapi.json` (machine-readable)

## Support

- GitHub: https://github.com/knowledge-graph-lab/ai-module
- Documentation: See `specs/001-docs-team-deliverables/quickstart.md`
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "AI Module Team",
        "email": "ai-team@knowledge-graph-lab.com",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {
            "name": "entity-extraction",
            "description": "Extract entities and relationships from documents"
        },
        {
            "name": "knowledge-graph",
            "description": "Query and traverse the knowledge graph"
        },
        {
            "name": "quality",
            "description": "Monitor extraction quality and performance"
        },
        {
            "name": "health",
            "description": "Health check endpoints for monitoring"
        },
        {
            "name": "websocket",
            "description": "Real-time graph updates via WebSocket"
        }
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=100,
    requests_per_hour=1000
)

# Include routers
app.include_router(extraction_router)
app.include_router(graph_router)
app.include_router(websocket_router)
app.include_router(quality_router)
app.include_router(health_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AI Development Module",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ai-module",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

