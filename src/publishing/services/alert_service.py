from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

from ..core.config import settings
from ..state import IN_MEMORY_ALERTS


class AlertService:
    def create_alert(self, *, content_id: str, target_channels: List[str], priority: str) -> Dict[str, Any]:
        now = datetime.utcnow()
        alert_id = str(uuid.uuid4())
        alert = {
            "id": alert_id,
            "content_id": content_id,
            "target_channels": target_channels,
            "priority": priority,
            "status": "queued",
            "created_at": now,
        }
        if settings.DEBUG:
            IN_MEMORY_ALERTS[alert_id] = alert
        else:
            # TODO: Persist to DB when production path is implemented
            IN_MEMORY_ALERTS[alert_id] = alert
        return alert

    def get_alert(self, alert_id: str) -> Optional[Dict[str, Any]]:
        if settings.DEBUG:
            return IN_MEMORY_ALERTS.get(alert_id)
        return IN_MEMORY_ALERTS.get(alert_id)

