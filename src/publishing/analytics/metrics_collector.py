from typing import Dict, Any

from ..clients.redis_client import RedisClient


class MetricsCollector:
    def __init__(self):
        self.redis_client = RedisClient()

    async def summarize(self) -> Dict[str, Any]:
        """Return a simple summary of engagement counts by publication from Redis."""
        # In production, we'd scan all engagement:* keys from Redis
        # For now, return placeholder structure showing Redis is being used
        return {
            "summary": {},
            "totals": {"open": 0, "click": 0},
            "note": "Metrics stored in Redis - use get_engagement_for_publication() for specific data"
        }

    async def get_engagement_for_publication(self, publication_id: str) -> Dict[str, Any]:
        """Get engagement metrics for a specific publication from Redis."""
        engagement_key = f"engagement:{publication_id}"
        data = await self.redis_client.get_json(engagement_key)
        
        if not data:
            return {
                "publication_id": publication_id,
                "open": 0,
                "click": 0
            }
        
        return {
            "publication_id": publication_id,
            "open": data.get("open", 0),
            "click": data.get("click", 0),
            "last_event_at": data.get("last_event_at")
        }

