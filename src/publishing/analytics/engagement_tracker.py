from typing import Dict, Any
from datetime import datetime, timezone

from ..clients.redis_client import RedisClient


class EngagementTracker:
    def __init__(self):
        self.redis_client = RedisClient()

    async def track(self, metric: Dict[str, Any]) -> None:
        """Track an engagement metric (open/click) in Redis."""
        event_type = metric.get("type")  # "open" or "click"
        publication_id = metric.get("publication_id")
        if not event_type or not publication_id:
            return None

        # Get current engagement data from Redis
        engagement_key = f"engagement:{publication_id}"
        store = await self.redis_client.get_json(engagement_key)
        
        if not store:
            store = {"open": 0, "click": 0, "publication_id": publication_id}
        
        # Increment counter
        if event_type in ["open", "click"]:
            store[event_type] = store.get(event_type, 0) + 1
        
        store["last_event_at"] = datetime.now(timezone.utc).isoformat()
        
        # Store back in Redis (24-hour TTL)
        await self.redis_client.set_json(engagement_key, store, ttl=86400)
        
        # Publish event for real-time analytics
        await self.redis_client.publish(
            "engagement:events",
            {
                "publication_id": publication_id,
                "event_type": event_type,
                "timestamp": store["last_event_at"]
            }
        )
        
        return None

