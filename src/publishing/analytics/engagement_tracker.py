from typing import Dict, Any
from datetime import datetime, timezone

from ..clients.redis_client import RedisClient


class EngagementTracker:
    def __init__(self):
        self.redis_client = RedisClient()

    async def track(self, metric: Dict[str, Any]) -> None:
        """Track an engagement metric (open/click) in Redis.
        
        Tracks engagement by both publication and channel (if provided).
        Keys:
        - engagement:pub:{publication_id} - publication-level metrics
        - engagement:channel:{channel_id} - channel-level metrics
        """
        event_type = metric.get("type")  # "open" or "click"
        publication_id = metric.get("publication_id")
        channel_id = metric.get("channel_id")
        user_id = metric.get("user_id")
        url = metric.get("url")
        
        if not event_type or not publication_id:
            return None

        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Track at publication level
        pub_engagement_key = f"engagement:pub:{publication_id}"
        pub_store = await self.redis_client.get_json(pub_engagement_key)
        
        if not pub_store:
            pub_store = {
                "open": 0, 
                "click": 0, 
                "publication_id": publication_id,
                "channel_id": channel_id  # Store associated channel for reference
            }
        
        # Increment counter
        if event_type in ["open", "click"]:
            pub_store[event_type] = pub_store.get(event_type, 0) + 1
        
        pub_store["last_event_at"] = timestamp
        if user_id:
            pub_store["last_user_id"] = user_id
        if url:
            pub_store["last_url"] = url
        
        # Store back in Redis (24-hour TTL)
        await self.redis_client.set_json(pub_engagement_key, pub_store, ttl=86400)
        
        # Track at channel level (if channel_id provided)
        if channel_id:
            channel_engagement_key = f"engagement:channel:{channel_id}"
            channel_store = await self.redis_client.get_json(channel_engagement_key)
            
            if not channel_store:
                channel_store = {
                    "open": 0,
                    "click": 0,
                    "channel_id": channel_id,
                    "publication_ids": []  # Track which publications contributed
                }
            
            # Increment counter
            if event_type in ["open", "click"]:
                channel_store[event_type] = channel_store.get(event_type, 0) + 1
            
            channel_store["last_event_at"] = timestamp
            
            # Track unique publications for this channel
            if publication_id not in channel_store.get("publication_ids", []):
                if "publication_ids" not in channel_store:
                    channel_store["publication_ids"] = []
                channel_store["publication_ids"].append(publication_id)
            
            # Store back in Redis (24-hour TTL)
            await self.redis_client.set_json(channel_engagement_key, channel_store, ttl=86400)
        
        # Publish event for real-time analytics
        await self.redis_client.publish(
            "engagement:events",
            {
                "publication_id": publication_id,
                "channel_id": channel_id,
                "event_type": event_type,
                "timestamp": timestamp,
                "user_id": user_id,
                "url": url
            }
        )
        
        return None

