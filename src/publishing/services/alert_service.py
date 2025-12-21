from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

from ..core.config import settings
from ..clients.redis_client import RedisClient
from .pubsub import PubSub


class AlertService:
    def __init__(self) -> None:
        self.redis_client = RedisClient()
        self.pubsub = PubSub()

    async def create_alert(self, *, content_id: str, target_channels: List[str], priority: str) -> Dict[str, Any]:
        now = datetime.utcnow()
        alert_id = str(uuid.uuid4())
        alert = {
            "id": alert_id,
            "content_id": content_id,
            "target_channels": target_channels,
            "priority": priority,
            "status": "queued",
            "created_at": now.isoformat(),
        }
        
        # Store in Redis with 24-hour TTL
        await self.redis_client.set_json(f"alert:{alert_id}", alert, ttl=86400)
        
        # emit event
        self.pubsub.publish("alerts", f"created:{alert_id}")
        
        # Publish to Redis pub/sub for real-time notifications
        await self.redis_client.publish("alerts:new", alert)
        
        return alert

    async def get_alert(self, alert_id: str) -> Optional[Dict[str, Any]]:
        return await self.redis_client.get_json(f"alert:{alert_id}")

    async def mark_sent(self, alert_id: str) -> bool:
        alert = await self.get_alert(alert_id)
        if not alert:
            return False
        alert["status"] = "sent"
        alert["sent_at"] = datetime.utcnow().isoformat()
        await self.redis_client.set_json(f"alert:{alert_id}", alert, ttl=86400)
        self.pubsub.publish("alerts", f"sent:{alert_id}")
        
        # Publish status update
        await self.redis_client.publish(
            "alerts:status_update",
            {"alert_id": alert_id, "status": "sent"}
        )
        return True

