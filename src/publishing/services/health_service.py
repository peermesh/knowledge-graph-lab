"""
Health monitoring service for Publishing Module.

Provides comprehensive health checks for container orchestration, monitoring,
and alerting. Follows async patterns and integrates with external services.

Constitution Compliance:
- Comprehensive Analytics Integration: Health metrics and monitoring
- Scalable Architecture: Service health tracking for horizontal scaling
- Performance: Efficient health checks without impacting response times
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import structlog

from ..core.config import settings
from ..core.database import get_db_health
from ..integrations.aws_ses import check_ses_health
from ..clients.redis_client import RedisClient
from ..clients.ai_client import AIClient


class HealthService:
    """Service for monitoring application and external service health."""

    def __init__(self):
        """Initialize health service with monitoring state."""
        self.logger = structlog.get_logger(__name__)
        self.start_time = time.time()
        self.monitoring_active = False
        self.health_check_interval = 30  # seconds
        self.redis_client = RedisClient()
        self.ai_client = AIClient()

    async def start_monitoring(self) -> None:
        """Start continuous health monitoring."""
        self.monitoring_active = True
        self.logger.info("Starting health monitoring service")

        # Start background health check task
        asyncio.create_task(self._continuous_health_check())

    async def stop_monitoring(self) -> None:
        """Stop health monitoring."""
        self.monitoring_active = False
        self.logger.info("Health monitoring service stopped")

    async def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status of all components."""

        # Overall status starts as healthy
        overall_status = "healthy"
        issues = []

        # Check database health
        try:
            db_health = await get_db_health()
            if db_health.get("status") != "connected":
                overall_status = "unhealthy"
                issues.append(f"Database: {db_health.get('error', 'disconnected')}")
        except Exception as e:
            overall_status = "unhealthy"
            issues.append(f"Database check failed: {str(e)}")

        # Check Redis health
        try:
            redis_health = await self.redis_client.ping()
            if not redis_health:
                overall_status = "degraded"
                issues.append("Redis: connection failed")
        except Exception as e:
            overall_status = "degraded"
            issues.append(f"Redis check failed: {str(e)}")

        # Check external services
        external_services = {}

        # AWS SES health
        try:
            ses_health = await check_ses_health()
            external_services["aws_ses"] = "connected" if ses_health else "disconnected"
            if not ses_health:
                overall_status = "degraded"
                issues.append("AWS SES: service unavailable")
        except Exception as e:
            external_services["aws_ses"] = "error"
            overall_status = "degraded"
            issues.append(f"AWS SES check failed: {str(e)}")

        # AI Module health
        try:
            ai_health = await self.ai_client.health_check()
            external_services["ai_module"] = "connected" if ai_health else "disconnected"
            if not ai_health:
                overall_status = "degraded"
                issues.append("AI Module: service unavailable")
        except Exception as e:
            external_services["ai_module"] = "error"
            overall_status = "degraded"
            issues.append(f"AI Module check failed: {str(e)}")

        # Calculate uptime
        uptime_seconds = int(time.time() - self.start_time)

        health_data = {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.VERSION,
            "uptime_seconds": uptime_seconds,
            "database_status": db_health.get("status", "unknown") if 'db_health' in locals() else "unknown",
            "external_services": external_services
        }

        if issues:
            health_data["issues"] = issues

        # Log health status for monitoring
        self.logger.info(
            "Health check completed",
            status=overall_status,
            uptime_seconds=uptime_seconds,
            issues=len(issues) if issues else 0
        )

        return health_data

    async def _continuous_health_check(self) -> None:
        """Background task for continuous health monitoring."""
        while self.monitoring_active:
            try:
                health_status = await self.get_health_status()

                # Log warnings for degraded or unhealthy status
                if health_status["status"] == "degraded":
                    self.logger.warning("Health status degraded", health_data=health_status)
                elif health_status["status"] == "unhealthy":
                    self.logger.error("Health status unhealthy", health_data=health_status)

                # Wait for next check interval
                await asyncio.sleep(self.health_check_interval)

            except Exception as e:
                self.logger.error("Health monitoring task failed", error=str(e))
                await asyncio.sleep(self.health_check_interval)

    async def get_detailed_health_report(self) -> Dict[str, Any]:
        """Get detailed health report with performance metrics."""

        health_status = await self.get_health_status()

        # Add additional performance metrics
        try:
            # Database connection pool metrics
            from ..core.database import engine
            health_status["database_metrics"] = {
                "pool_size": engine.pool.size(),
                "checked_in": engine.pool.checkedin(),
                "checked_out": engine.pool.checkedout(),
                "overflow": engine.pool.overflow(),
                "invalid": engine.pool.invalid()
            }
        except Exception as e:
            health_status["database_metrics"] = {"error": str(e)}

        # Memory and performance metrics
        try:
            import psutil
            process = psutil.Process()
            health_status["system_metrics"] = {
                "memory_usage_mb": process.memory_info().rss / 1024 / 1024,
                "cpu_percent": process.cpu_percent(),
                "open_files": len(process.open_files())
            }
        except ImportError:
            health_status["system_metrics"] = {"error": "psutil not available"}
        except Exception as e:
            health_status["system_metrics"] = {"error": str(e)}

        return health_status

    async def get_service_dependencies(self) -> Dict[str, Any]:
        """Get status of all service dependencies."""
        dependencies = {
            "database": await get_db_health(),
            "redis": await self.redis_client.ping(),
            "external_services": {}
        }

        # Check external services
        services_to_check = [
            ("aws_ses", check_ses_health),
            ("ai_module", self.ai_client.health_check)
        ]

        for service_name, health_check_func in services_to_check:
            try:
                dependencies["external_services"][service_name] = await health_check_func()
            except Exception as e:
                dependencies["external_services"][service_name] = {"status": "error", "error": str(e)}

        return dependencies

    def is_ready_for_traffic(self) -> bool:
        """Check if the service is ready to handle traffic."""
        # Basic readiness check - can be extended with more sophisticated logic
        return self.monitoring_active

