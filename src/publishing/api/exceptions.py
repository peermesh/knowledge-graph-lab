"""
RFC7807 Problem Details for HTTP APIs - Error Handling Module.

Provides standardized error response formatting according to RFC7807 standard.
Ensures consistent error handling across all API endpoints.

Constitution Compliance:
- API Standards: RFC7807 compliant error responses
- Comprehensive Analytics: Trace ID integration for error tracking
- Scalable Architecture: Centralized error handling
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional


def create_problem_detail(
    status: int,
    title: str,
    detail: str,
    instance: str,
    type_uri: Optional[str] = None,
    trace_id: Optional[str] = None
) -> dict:
    """
    Create RFC7807 Problem Details object.
    
    Args:
        status: HTTP status code
        title: Short human-readable summary
        detail: Human-readable explanation
        instance: URI reference identifying the specific occurrence
        type_uri: Optional custom type URI (defaults to httpstatuses.com)
        trace_id: Optional trace ID for request tracking
    
    Returns:
        Dictionary with RFC7807 Problem Details structure
    """
    if type_uri is None:
        type_uri = f"https://httpstatuses.com/{status}"
    
    problem = {
        "type": type_uri,
        "title": title,
        "status": status,
        "detail": detail,
        "instance": instance
    }
    
    if trace_id:
        problem["traceId"] = trace_id
    
    return problem


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTPException with RFC7807 Problem Details format.
    
    This handler specifically handles FastAPI HTTPException instances
    and formats them according to RFC7807 standard.
    
    Args:
        request: FastAPI Request object
        exc: HTTPException instance
    
    Returns:
        JSONResponse with RFC7807 Problem Details format
    """
    # Get trace ID from request state if available
    trace_id = getattr(request.state, "correlation_id", None)
    
    # Determine title based on status code
    title = f"HTTP {exc.status_code}"
    if exc.status_code == 400:
        title = "Bad Request"
    elif exc.status_code == 401:
        title = "Unauthorized"
    elif exc.status_code == 403:
        title = "Forbidden"
    elif exc.status_code == 404:
        title = "Not Found"
    elif exc.status_code == 409:
        title = "Conflict"
    elif exc.status_code == 422:
        title = "Unprocessable Entity"
    elif exc.status_code == 500:
        title = "Internal Server Error"
    elif exc.status_code == 503:
        title = "Service Unavailable"
    
    problem = create_problem_detail(
        status=exc.status_code,
        title=title,
        detail=exc.detail if exc.detail else f"An error occurred: {title}",
        instance=str(request.url.path),
        trace_id=trace_id
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=problem,
        headers={"Content-Type": "application/problem+json"}
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle uncaught exceptions with RFC7807 Problem Details format.
    
    This is a fallback handler for exceptions that aren't HTTPException.
    
    Args:
        request: FastAPI Request object
        exc: Exception instance
    
    Returns:
        JSONResponse with RFC7807 Problem Details format
    """
    trace_id = getattr(request.state, "correlation_id", None)
    
    problem = create_problem_detail(
        status=500,
        title="Internal Server Error",
        detail=f"An unexpected error occurred: {str(exc)}",
        instance=str(request.url.path),
        type_uri="https://api.knowledge-graph-lab.com/errors/internal-server-error",
        trace_id=trace_id
    )
    
    return JSONResponse(
        status_code=500,
        content=problem,
        headers={"Content-Type": "application/problem+json"}
    )


# Alias for backward compatibility (if needed)
async def rfc7807_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Alias for generic_exception_handler for backward compatibility.
    
    Deprecated: Use generic_exception_handler or http_exception_handler directly.
    """
    return await generic_exception_handler(request, exc)
