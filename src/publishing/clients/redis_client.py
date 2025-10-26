"""
Redis client for Publishing Module.

High-performance Redis integration for caching, pub/sub messaging, and session management.
Optimized for async operations and connection pooling.

Constitution Compliance:
- Technology Standards: Redis 7.0+ for caching and messaging
- Scalable Architecture: Connection pooling and async operations
- Performance: Sub-millisecond response times for cache operations
"""

import asyncio
import json
from typing import Any, Dict, List, Optional, Union
import structlog
import redis.asyncio as redis
from redis.exceptions import ConnectionError, TimeoutError

from ..core.config import settings


class RedisClient:
    """Async Redis client with connection management and error handling."""

    def __init__(self):
        """Initialize Redis client with connection configuration."""
        self.logger = structlog.get_logger(__name__)
        self.client: Optional[redis.Redis] = None
        self.connection_url = settings.REDIS_URL

    async def connect(self) -> None:
        """Establish connection to Redis."""
        try:
            self.client = redis.from_url(
                self.connection_url,
                decode_responses=True,
                socket_timeout=5.0,
                socket_connect_timeout=5.0,
                retry_on_timeout=True,
                max_connections=settings.MAX_CONNECTIONS
            )

            # Test connection
            await self.client.ping()
            self.logger.info("Redis connection established successfully")

        except Exception as e:
            self.logger.error("Failed to connect to Redis", error=str(e))
            raise

    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self.client:
            await self.client.close()
            self.logger.info("Redis connection closed")

    async def ping(self) -> bool:
        """Test Redis connectivity."""
        try:
            if not self.client:
                await self.connect()

            result = await self.client.ping()
            return result
        except Exception as e:
            self.logger.error("Redis ping failed", error=str(e))
            return False

    async def get(self, key: str) -> Optional[str]:
        """Get value from Redis cache."""
        try:
            if not self.client:
                await self.connect()

            return await self.client.get(key)
        except Exception as e:
            self.logger.error("Redis get failed", key=key, error=str(e))
            return None

    async def set(self, key: str, value: Union[str, Dict, List], ttl: int = None) -> bool:
        """Set value in Redis cache with optional TTL."""
        try:
            if not self.client:
                await self.connect()

            # Convert complex objects to JSON
            if isinstance(value, (dict, list)):
                value = json.dumps(value, default=str)

            if ttl:
                return await self.client.setex(key, ttl, value)
            else:
                return await self.client.set(key, value)

        except Exception as e:
            self.logger.error("Redis set failed", key=key, error=str(e))
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from Redis."""
        try:
            if not self.client:
                await self.connect()

            result = await self.client.delete(key)
            return result > 0
        except Exception as e:
            self.logger.error("Redis delete failed", key=key, error=str(e))
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        try:
            if not self.client:
                await self.connect()

            return await self.client.exists(key) > 0
        except Exception as e:
            self.logger.error("Redis exists check failed", key=key, error=str(e))
            return False

    async def expire(self, key: str, ttl: int) -> bool:
        """Set TTL for a key."""
        try:
            if not self.client:
                await self.connect()

            return await self.client.expire(key, ttl)
        except Exception as e:
            self.logger.error("Redis expire failed", key=key, error=str(e))
            return False

    # Pub/Sub functionality for real-time messaging
    async def publish(self, channel: str, message: Union[str, Dict, List]) -> int:
        """Publish message to Redis channel."""
        try:
            if not self.client:
                await self.connect()

            # Convert complex objects to JSON
            if isinstance(message, (dict, list)):
                message = json.dumps(message, default=str)

            result = await self.client.publish(channel, message)
            self.logger.debug("Published to Redis channel", channel=channel, subscribers=result)
            return result

        except Exception as e:
            self.logger.error("Redis publish failed", channel=channel, error=str(e))
            return 0

    async def subscribe(self, channel: str) -> redis.client.PubSub:
        """Subscribe to Redis channel for real-time messaging."""
        try:
            if not self.client:
                await self.connect()

            pubsub = self.client.pubsub()
            await pubsub.subscribe(channel)
            self.logger.info("Subscribed to Redis channel", channel=channel)
            return pubsub

        except Exception as e:
            self.logger.error("Redis subscribe failed", channel=channel, error=str(e))
            raise

    # Cache management utilities
    async def get_json(self, key: str) -> Optional[Dict[str, Any]]:
        """Get JSON object from Redis cache."""
        try:
            value = await self.get(key)
            if value:
                return json.loads(value)
            return None
        except (json.JSONDecodeError, Exception) as e:
            self.logger.error("Redis get_json failed", key=key, error=str(e))
            return None

    async def set_json(self, key: str, value: Dict[str, Any], ttl: int = None) -> bool:
        """Set JSON object in Redis cache."""
        return await self.set(key, value, ttl)

    # Batch operations for performance
    async def mget(self, keys: List[str]) -> List[Optional[str]]:
        """Get multiple values from Redis in a single operation."""
        try:
            if not self.client:
                await self.connect()

            return await self.client.mget(keys)
        except Exception as e:
            self.logger.error("Redis mget failed", keys=keys, error=str(e))
            return [None] * len(keys)

    async def mset(self, key_value_pairs: Dict[str, str]) -> bool:
        """Set multiple key-value pairs in a single operation."""
        try:
            if not self.client:
                await self.connect()

            return await self.client.mset(key_value_pairs)
        except Exception as e:
            self.logger.error("Redis mset failed", error=str(e))
            return False

    # Health and monitoring
    async def get_info(self) -> Dict[str, Any]:
        """Get Redis server information."""
        try:
            if not self.client:
                await self.connect()

            return await self.client.info()
        except Exception as e:
            self.logger.error("Redis info failed", error=str(e))
            return {"status": "error", "error": str(e)}

    async def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage information."""
        try:
            if not self.client:
                await self.connect()

            info = await self.client.info("memory")
            return {
                "used_memory": info.get("used_memory_human", "unknown"),
                "used_memory_peak": info.get("used_memory_peak_human", "unknown"),
                "used_memory_rss": info.get("used_memory_rss_human", "unknown"),
                "memory_fragmentation_ratio": info.get("mem_fragmentation_ratio", "unknown")
            }
        except Exception as e:
            self.logger.error("Redis memory info failed", error=str(e))
            return {"status": "error", "error": str(e)}

