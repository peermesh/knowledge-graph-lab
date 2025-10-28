from typing import Dict, Any
from datetime import datetime, timezone

from ..state import IN_MEMORY_ENGAGEMENT


class EngagementTracker:
    def track(self, metric: Dict[str, Any]) -> None:
        """Track an engagement metric (open/click) in memory (DEBUG mode)."""
        event_type = metric.get("type")  # "open" or "click"
        publication_id = metric.get("publication_id")
        if not event_type or not publication_id:
            return None

        store = IN_MEMORY_ENGAGEMENT.setdefault(publication_id, {"open": 0, "click": 0})
        if event_type in store:
            store[event_type] += 1
        store.setdefault("last_event_at", datetime.now(timezone.utc).isoformat())
        return None

