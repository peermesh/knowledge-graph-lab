"""Rate limiting middleware for API endpoints"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Tuple
from datetime import datetime, timedelta
import time
import logging

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using token bucket algorithm.
    
    Limits:
    - 100 requests per minute per user/IP
    - 1000 requests per hour per user/IP
    """
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 100,
        requests_per_hour: int = 1000
    ):
        """
        Initialize rate limiter.
        
        Args:
            app: FastAPI application
            requests_per_minute: Max requests per minute
            requests_per_hour: Max requests per hour
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Storage for rate limit tracking
        # Format: {client_key: (minute_count, minute_reset, hour_count, hour_reset)}
        self.rate_limits: Dict[str, Tuple[int, datetime, int, datetime]] = {}
    
    async def dispatch(self, request: Request, call_next):
        """
        Process request and enforce rate limits.
        
        Args:
            request: Incoming request
            call_next: Next middleware/endpoint
        
        Returns:
            Response
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/ai/v1/health", "/ai/v1/health/live", "/ai/v1/health/ready"]:
            return await call_next(request)
        
        # Get client identifier
        client_key = self._get_client_key(request)
        
        # Check rate limits
        is_allowed, retry_after = self._check_rate_limit(client_key)
        
        if not is_allowed:
            # Rate limit exceeded
            logger.warning(
                f"Rate limit exceeded for {client_key}: "
                f"{request.method} {request.url.path}"
            )
            
            return self._rate_limit_response(retry_after)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining_minute = self._get_remaining_requests(client_key, 'minute')
        remaining_hour = self._get_remaining_requests(client_key, 'hour')
        
        response.headers["X-RateLimit-Limit-Minute"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining-Minute"] = str(remaining_minute)
        response.headers["X-RateLimit-Limit-Hour"] = str(self.requests_per_hour)
        response.headers["X-RateLimit-Remaining-Hour"] = str(remaining_hour)
        
        return response
    
    def _get_client_key(self, request: Request) -> str:
        """
        Get unique client identifier for rate limiting.
        
        Uses authentication if available, falls back to IP address.
        
        Args:
            request: Request object
        
        Returns:
            Client identifier
        """
        # Try to get user ID from auth (if implemented)
        # For now, use IP address
        client_ip = request.client.host if request.client else "unknown"
        
        # Could also use:
        # - JWT token subject (user_id)
        # - API key
        # - Custom client identifier
        
        return f"ip:{client_ip}"
    
    def _check_rate_limit(self, client_key: str) -> Tuple[bool, int]:
        """
        Check if client has exceeded rate limit.
        
        Args:
            client_key: Client identifier
        
        Returns:
            Tuple of (is_allowed, retry_after_seconds)
        """
        now = datetime.utcnow()
        
        if client_key not in self.rate_limits:
            # Initialize rate limit for new client
            self.rate_limits[client_key] = (
                1,  # minute_count
                now + timedelta(minutes=1),  # minute_reset
                1,  # hour_count
                now + timedelta(hours=1)  # hour_reset
            )
            return True, 0
        
        minute_count, minute_reset, hour_count, hour_reset = self.rate_limits[client_key]
        
        # Reset counters if time windows expired
        if now >= minute_reset:
            minute_count = 0
            minute_reset = now + timedelta(minutes=1)
        
        if now >= hour_reset:
            hour_count = 0
            hour_reset = now + timedelta(hours=1)
        
        # Check limits
        if minute_count >= self.requests_per_minute:
            # Minute limit exceeded
            retry_after = int((minute_reset - now).total_seconds())
            return False, max(retry_after, 1)
        
        if hour_count >= self.requests_per_hour:
            # Hour limit exceeded
            retry_after = int((hour_reset - now).total_seconds())
            return False, max(retry_after, 1)
        
        # Increment counters
        minute_count += 1
        hour_count += 1
        
        # Update storage
        self.rate_limits[client_key] = (
            minute_count,
            minute_reset,
            hour_count,
            hour_reset
        )
        
        return True, 0
    
    def _get_remaining_requests(self, client_key: str, window: str) -> int:
        """Get remaining requests for client in time window"""
        if client_key not in self.rate_limits:
            return self.requests_per_minute if window == 'minute' else self.requests_per_hour
        
        minute_count, _, hour_count, _ = self.rate_limits[client_key]
        
        if window == 'minute':
            return max(0, self.requests_per_minute - minute_count)
        else:  # hour
            return max(0, self.requests_per_hour - hour_count)
    
    def _rate_limit_response(self, retry_after: int):
        """Create rate limit exceeded response"""
        from fastapi.responses import JSONResponse
        
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "rate_limit_exceeded",
                "message": "Too many requests. Please try again later.",
                "retry_after_seconds": retry_after
            },
            headers={
                "Retry-After": str(retry_after)
            }
        )
    
    def clear_expired_entries(self):
        """Clean up expired rate limit entries"""
        now = datetime.utcnow()
        expired = []
        
        for client_key, (_, minute_reset, _, hour_reset) in self.rate_limits.items():
            # If both windows have expired, remove entry
            if now >= minute_reset and now >= hour_reset:
                expired.append(client_key)
        
        for client_key in expired:
            del self.rate_limits[client_key]
        
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired rate limit entries")


def create_rate_limiter(
    requests_per_minute: int = 100,
    requests_per_hour: int = 1000
) -> RateLimitMiddleware:
    """
    Create configured rate limiter middleware.
    
    Args:
        requests_per_minute: Max requests per minute
        requests_per_hour: Max requests per hour
    
    Returns:
        RateLimitMiddleware instance
    """
    logger.info(
        f"Rate limiter configured: {requests_per_minute}/min, {requests_per_hour}/hour"
    )
    
    return lambda app: RateLimitMiddleware(
        app,
        requests_per_minute=requests_per_minute,
        requests_per_hour=requests_per_hour
    )

