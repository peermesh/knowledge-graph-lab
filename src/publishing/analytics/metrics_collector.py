from typing import Dict, Any

from ..clients.redis_client import RedisClient


class MetricsCollector:
    def __init__(self):
        self.redis_client = RedisClient()

    async def summarize(self, channel_id: str = None) -> Dict[str, Any]:
        """Return a summary of engagement counts.
        
        If channel_id is provided, returns metrics for that specific channel.
        Otherwise, returns aggregated metrics for all publications and channels.
        """
        try:
            # Check Redis connection
            ping_result = await self.redis_client.ping()
            if not ping_result:
                return {
                    "summary": {},
                    "totals": {"open": 0, "click": 0},
                    "note": "Redis not available"
                }
            
            # Ensure Redis client is connected
            if not self.redis_client.client:
                await self.redis_client.connect()
            
            # If channel_id provided, return channel-specific metrics
            if channel_id:
                return await self._get_channel_summary(channel_id)
            
            # Aggregate totals from all publications and channels
            totals = {"open": 0, "click": 0}
            publication_summary = {}
            channel_summary = {}
            
            # Scan for publication-level keys
            pub_keys = []
            async for key in self.redis_client.client.scan_iter(match="engagement:pub:*"):
                pub_keys.append(key)
            
            # Scan for channel-level keys
            channel_keys = []
            async for key in self.redis_client.client.scan_iter(match="engagement:channel:*"):
                channel_keys.append(key)
            
            # Aggregate publication metrics
            for key in pub_keys:
                data = await self.redis_client.get_json(key)
                if data:
                    publication_id = data.get("publication_id", key.split(":")[-1])
                    open_count = data.get("open", 0)
                    click_count = data.get("click", 0)
                    
                    totals["open"] += open_count
                    totals["click"] += click_count
                    
                    publication_summary[publication_id] = {
                        "open": open_count,
                        "click": click_count,
                        "channel_id": data.get("channel_id"),
                        "last_event_at": data.get("last_event_at")
                    }
            
            # Aggregate channel metrics
            for key in channel_keys:
                data = await self.redis_client.get_json(key)
                if data:
                    channel_id = data.get("channel_id", key.split(":")[-1])
                    open_count = data.get("open", 0)
                    click_count = data.get("click", 0)
                    
                    channel_summary[channel_id] = {
                        "open": open_count,
                        "click": click_count,
                        "publication_count": len(data.get("publication_ids", [])),
                        "publication_ids": data.get("publication_ids", []),
                        "last_event_at": data.get("last_event_at")
                    }
            
            return {
                "summary": publication_summary,
                "channels": channel_summary,
                "totals": totals,
                "publication_count": len(publication_summary),
                "channel_count": len(channel_summary),
                "note": "Metrics aggregated from Redis (publications and channels)"
            }
        except Exception as e:
            # If Redis scan fails, return placeholder
            return {
                "summary": {},
                "totals": {"open": 0, "click": 0},
                "note": f"Redis scan failed: {str(e)}"
            }
    
    async def _get_channel_summary(self, channel_id: str) -> Dict[str, Any]:
        """Get engagement summary for a specific channel."""
        channel_key = f"engagement:channel:{channel_id}"
        channel_data = await self.redis_client.get_json(channel_key)
        
        if not channel_data:
            return {
                "channel_id": channel_id,
                "summary": {},
                "totals": {"open": 0, "click": 0},
                "publication_count": 0,
                "note": f"No engagement data found for channel {channel_id}"
            }
        
        # Get engagement data for each publication in this channel
        publication_summary = {}
        for pub_id in channel_data.get("publication_ids", []):
            pub_key = f"engagement:pub:{pub_id}"
            pub_data = await self.redis_client.get_json(pub_key)
            if pub_data:
                publication_summary[pub_id] = {
                    "open": pub_data.get("open", 0),
                    "click": pub_data.get("click", 0),
                    "last_event_at": pub_data.get("last_event_at")
                }
        
        return {
            "channel_id": channel_id,
            "summary": publication_summary,
            "totals": {
                "open": channel_data.get("open", 0),
                "click": channel_data.get("click", 0)
            },
            "publication_count": len(channel_data.get("publication_ids", [])),
            "publication_ids": channel_data.get("publication_ids", []),
            "last_event_at": channel_data.get("last_event_at"),
            "note": f"Metrics for channel {channel_id}"
        }

    async def get_engagement_for_publication(self, publication_id: str) -> Dict[str, Any]:
        """Get engagement metrics for a specific publication from Redis."""
        engagement_key = f"engagement:pub:{publication_id}"
        data = await self.redis_client.get_json(engagement_key)
        
        if not data:
            return {
                "publication_id": publication_id,
                "open": 0,
                "click": 0
            }
        
        return {
            "publication_id": publication_id,
            "channel_id": data.get("channel_id"),
            "open": data.get("open", 0),
            "click": data.get("click", 0),
            "last_event_at": data.get("last_event_at"),
            "last_user_id": data.get("last_user_id"),
            "last_url": data.get("last_url")
        }
    
    async def get_engagement_for_channel(self, channel_id: str) -> Dict[str, Any]:
        """Get engagement metrics for a specific channel from Redis."""
        channel_key = f"engagement:channel:{channel_id}"
        data = await self.redis_client.get_json(channel_key)
        
        if not data:
            return {
                "channel_id": channel_id,
                "open": 0,
                "click": 0,
                "publication_count": 0
            }
        
        return {
            "channel_id": channel_id,
            "open": data.get("open", 0),
            "click": data.get("click", 0),
            "publication_count": len(data.get("publication_ids", [])),
            "publication_ids": data.get("publication_ids", []),
            "last_event_at": data.get("last_event_at")
        }

