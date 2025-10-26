"""
Structured logging configuration for Publishing Module.

Provides comprehensive logging with correlation IDs, structured JSON format,
and proper log levels for production and development environments.

Constitution Compliance:
- Comprehensive Analytics Integration: Structured logging for observability
- Scalable Architecture: Efficient logging for high-volume operations
- Performance: Optimized logging without impacting response times
"""

import logging
import sys
import structlog
from datetime import datetime
from typing import Dict, Any
import json

from .config import settings


def setup_logging() -> None:
    """Configure structured logging for the application."""

    # Configure Python standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    )

    # Configure structlog for structured logging
    if settings.LOG_FORMAT.lower() == "json":
        # JSON formatter for production
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
            ),
            context_class=dict,
            logger_factory=structlog.WriteLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        # Human-readable formatter for development
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.dev.ConsoleRenderer()
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
            ),
            context_class=dict,
            logger_factory=structlog.WriteLoggerFactory(),
            cache_logger_on_first_use=True,
        )


def get_logger(name: str = __name__) -> structlog.BoundLogger:
    """Get a structured logger instance with context binding."""
    return structlog.get_logger(name)


class CorrelationIDFilter:
    """Filter to add correlation IDs to all log records."""

    def __init__(self, correlation_id: str = None):
        self.correlation_id = correlation_id

    def __call__(self, logger: structlog.BoundLogger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Add correlation ID to log event if available."""
        if self.correlation_id:
            event_dict["correlation_id"] = self.correlation_id
        return event_dict


def log_request_start(correlation_id: str, method: str, url: str, client_ip: str = None) -> None:
    """Log the start of a request with correlation ID."""
    logger = get_logger("publishing.requests")
    logger.info(
        "Request started",
        correlation_id=correlation_id,
        method=method,
        url=url,
        client_ip=client_ip,
        timestamp=datetime.utcnow().isoformat()
    )


def log_request_complete(correlation_id: str, method: str, url: str, status_code: int, duration_ms: float) -> None:
    """Log the completion of a request."""
    logger = get_logger("publishing.requests")
    logger.info(
        "Request completed",
        correlation_id=correlation_id,
        method=method,
        url=url,
        status_code=status_code,
        duration_ms=duration_ms,
        timestamp=datetime.utcnow().isoformat()
    )


def log_publication_event(correlation_id: str, publication_id: str, event_type: str, details: Dict[str, Any]) -> None:
    """Log publishing-related events (creation, delivery, failure, etc.)."""
    logger = get_logger("publishing.publications")
    logger.info(
        "Publication event",
        correlation_id=correlation_id,
        publication_id=publication_id,
        event_type=event_type,
        details=details,
        timestamp=datetime.utcnow().isoformat()
    )


def log_external_service_call(correlation_id: str, service_name: str, operation: str, success: bool, duration_ms: float, error: str = None) -> None:
    """Log external service calls (AWS SES, Slack, Discord, AI module)."""
    logger = get_logger("publishing.external_services")

    if success:
        logger.info(
            "External service call successful",
            correlation_id=correlation_id,
            service=service_name,
            operation=operation,
            duration_ms=duration_ms,
            timestamp=datetime.utcnow().isoformat()
        )
    else:
        logger.error(
            "External service call failed",
            correlation_id=correlation_id,
            service=service_name,
            operation=operation,
            duration_ms=duration_ms,
            error=error,
            timestamp=datetime.utcnow().isoformat()
        )


def log_ai_integration(correlation_id: str, operation: str, content_id: str, success: bool, score: float = None, error: str = None) -> None:
    """Log AI module integration events."""
    logger = get_logger("publishing.ai_integration")

    if success:
        logger.info(
            "AI integration successful",
            correlation_id=correlation_id,
            operation=operation,
            content_id=content_id,
            score=score,
            timestamp=datetime.utcnow().isoformat()
        )
    else:
        logger.error(
            "AI integration failed",
            correlation_id=correlation_id,
            operation=operation,
            content_id=content_id,
            error=error,
            timestamp=datetime.utcnow().isoformat()
        )


def log_personalization_event(correlation_id: str, subscriber_id: str, content_ids: list, personalization_rules: Dict[str, Any]) -> None:
    """Log personalization engine events."""
    logger = get_logger("publishing.personalization")
    logger.info(
        "Personalization applied",
        correlation_id=correlation_id,
        subscriber_id=subscriber_id,
        content_ids=content_ids,
        personalization_rules=personalization_rules,
        timestamp=datetime.utcnow().isoformat()
    )


def log_analytics_event(correlation_id: str, event_type: str, data: Dict[str, Any]) -> None:
    """Log analytics and engagement tracking events."""
    logger = get_logger("publishing.analytics")
    logger.info(
        "Analytics event",
        correlation_id=correlation_id,
        event_type=event_type,
        data=data,
        timestamp=datetime.utcnow().isoformat()
    )


def log_security_event(correlation_id: str, event_type: str, user_id: str, details: Dict[str, Any]) -> None:
    """Log security-related events (authentication, authorization, etc.)."""
    logger = get_logger("publishing.security")
    logger.warning(
        "Security event",
        correlation_id=correlation_id,
        event_type=event_type,
        user_id=user_id,
        details=details,
        timestamp=datetime.utcnow().isoformat()
    )


def log_performance_metric(correlation_id: str, metric_name: str, value: float, unit: str, context: Dict[str, Any] = None) -> None:
    """Log performance metrics for monitoring and optimization."""
    logger = get_logger("publishing.performance")

    context = context or {}
    context.update({
        "correlation_id": correlation_id,
        "metric_name": metric_name,
        "value": value,
        "unit": unit,
        "timestamp": datetime.utcnow().isoformat()
    })

    logger.info("Performance metric", **context)


# Utility functions for common logging patterns
def log_function_call(logger: structlog.BoundLogger, func_name: str, args: Dict[str, Any] = None) -> None:
    """Log function call entry with arguments."""
    logger.debug(
        "Function call",
        function=func_name,
        arguments=args or {},
        timestamp=datetime.utcnow().isoformat()
    )


def log_function_return(logger: structlog.BoundLogger, func_name: str, result_summary: str = None) -> None:
    """Log function return."""
    logger.debug(
        "Function return",
        function=func_name,
        result_summary=result_summary,
        timestamp=datetime.utcnow().isoformat()
    )


def log_function_error(logger: structlog.BoundLogger, func_name: str, error: Exception) -> None:
    """Log function error with exception details."""
    logger.error(
        "Function error",
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(error),
        timestamp=datetime.utcnow().isoformat()
    )

