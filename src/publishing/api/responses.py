"""
Standardized API Response Wrapper Module.

Provides centralized response formatting functions to ensure consistency
across all API endpoints with data/meta/errors structure.

Constitution Compliance:
- Performance: Optimized response formatting
- Scalable Architecture: Centralized response logic
- Comprehensive Analytics: Request ID tracking for all responses
"""

from typing import Any, Optional, Dict, List
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid


class Meta(BaseModel):
    """Metadata for API responses."""
    timestamp: str
    request_id: Optional[str] = None
    # Additional metadata can be added here


class StandardResponse(BaseModel):
    """Standard response envelope format."""
    data: Any
    meta: Meta
    errors: List[Dict[str, Any]] = []


def success_response(
    data: Any,
    request_id: Optional[str] = None,
    additional_meta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized success response.
    
    Args:
        data: The response data
        request_id: Optional request ID (generates UUID if not provided)
        additional_meta: Additional metadata fields to include
    
    Returns:
        Dictionary with data, meta, and errors fields
    
    Example:
        >>> success_response({"channels": []})
        {
            "data": {"channels": []},
            "meta": {
                "timestamp": "2025-11-17T12:00:00.123456+00:00",
                "request_id": "550e8400-e29b-41d4-a716-446655440000"
            },
            "errors": []
        }
    """
    if request_id is None:
        request_id = str(uuid.uuid4())
    
    meta = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id
    }
    
    if additional_meta:
        meta.update(additional_meta)
    
    return {
        "data": data,
        "meta": meta,
        "errors": []
    }


def error_response(
    errors: List[Dict[str, Any]],
    request_id: Optional[str] = None,
    additional_meta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        errors: List of error dictionaries
        request_id: Optional request ID
        additional_meta: Additional metadata fields
    
    Returns:
        Dictionary with data (null), meta, and errors fields
    
    Example:
        >>> error_response([{"code": "404", "message": "Not found"}])
        {
            "data": None,
            "meta": {
                "timestamp": "2025-11-17T12:00:00.123456+00:00",
                "request_id": "550e8400-e29b-41d4-a716-446655440000"
            },
            "errors": [{"code": "404", "message": "Not found"}]
        }
    """
    if request_id is None:
        request_id = str(uuid.uuid4())
    
    meta = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id
    }
    
    if additional_meta:
        meta.update(additional_meta)
    
    return {
        "data": None,
        "meta": meta,
        "errors": errors
    }

