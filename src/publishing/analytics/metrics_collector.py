from typing import Dict, Any

from ..state import IN_MEMORY_ENGAGEMENT


class MetricsCollector:
    def summarize(self) -> Dict[str, Any]:
        """Return a simple summary of engagement counts by publication."""
        summary = {
            pub_id: {"open": data.get("open", 0), "click": data.get("click", 0)}
            for pub_id, data in IN_MEMORY_ENGAGEMENT.items()
        }
        totals = {
            "open": sum(v.get("open", 0) for v in IN_MEMORY_ENGAGEMENT.values()),
            "click": sum(v.get("click", 0) for v in IN_MEMORY_ENGAGEMENT.values()),
        }
        return {"summary": summary, "totals": totals}

