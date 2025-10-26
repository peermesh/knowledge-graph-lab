"""
Publishing Module - Main Application

A comprehensive multi-channel content delivery system for AI-powered research insights.
Delivers personalized newsletters, alerts, and digests across email, Slack, Discord, and webhook channels.

Constitution Compliance:
- AI-First Research Platform: AI-powered personalization and content scoring
- Multi-Channel Publishing Excellence: 5-channel delivery with intelligent formatting
- Test-Driven Development: Comprehensive TDD with ≥85% coverage
- Comprehensive Analytics Integration: Real-time engagement tracking
- Scalable Architecture: Async design for 100,000+ users
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import structlog
import time

from .api import router as api_router
from .core.config import settings
from .core.database import create_db_and_tables
from .core.logging import setup_logging
from .services.health_service import HealthService


# Global health service instance
health_service = HealthService()

# Configure structured logging
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info("Starting Publishing Module", version=settings.VERSION)

    # Initialize database
    await create_db_and_tables()
    logger.info("Database initialized successfully")

    # Start health monitoring
    await health_service.start_monitoring()
    logger.info("Health monitoring started")

    yield

    # Shutdown
    logger.info("Shutting down Publishing Module")
    await health_service.stop_monitoring()
    logger.info("Health monitoring stopped")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""

    # Initialize structured logging early
    setup_logging()

    # Create FastAPI app with lifespan management
    app = FastAPI(
        title="Publishing Module API",
        description="Multi-channel content publishing system with AI-powered personalization",
        version=settings.VERSION,
        lifespan=lifespan,
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        openapi_url="/api/v1/openapi.json"
    )

    # Add security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

    # Add CORS middleware for frontend integration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()

        # Generate correlation ID for request tracing
        correlation_id = str(time.time_ns())

        # Add correlation ID to request state
        request.state.correlation_id = correlation_id

        # Configure logger with correlation ID
        request_logger = logger.bind(correlation_id=correlation_id)

        request_logger.info(
            "Incoming request",
            method=request.method,
            url=str(request.url),
            client=request.client.host if request.client else None
        )

        try:
            response = await call_next(request)

            process_time = time.time() - start_time
            request_logger.info(
                "Request completed",
                status_code=response.status_code,
                process_time=f"{process_time:.3f}s"
            )

            # Add correlation ID to response headers for tracing
            response.headers["X-Correlation-ID"] = correlation_id

            return response

        except Exception as e:
            process_time = time.time() - start_time
            request_logger.error(
                "Request failed",
                error=str(e),
                process_time=f"{process_time:.3f}s"
            )
            raise

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")

    # Health check endpoint (required for container orchestration)
    @app.get("/health")
    async def health_check(request: Request):
        """Health check endpoint for container orchestration."""
        health_status = await health_service.get_health_status()

        if health_status["status"] == "healthy":
            return {
                "data": health_status,
                "meta": {
                    "timestamp": health_status["timestamp"],
                    "request_id": getattr(request.state, "correlation_id", "unknown")
                },
                "errors": []
            }
        else:
            # Return 503 for unhealthy status
            from fastapi import HTTPException
            raise HTTPException(status_code=503, detail="Service unhealthy")

    logger.info("FastAPI application configured successfully")
    return app


# Create the application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Publishing Module server")
    uvicorn.run(
        "src.publishing.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=None,  # Use our structured logging
        access_log=False   # We handle access logging in middleware
    )

