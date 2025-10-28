from typing import Dict, Any

from ..analytics.engagement_tracker import EngagementTracker
from ..analytics.metrics_collector import MetricsCollector
from ..optimization.performance_analyzer import PerformanceAnalyzer


class AnalyticsService:
    def __init__(self) -> None:
        self.tracker = EngagementTracker()
        self.collector = MetricsCollector()
        self.analyzer = PerformanceAnalyzer()

    def get_engagement_summary(self) -> Dict[str, Any]:
        return self.collector.summarize()

    def get_performance(self) -> Dict[str, Any]:
        return self.analyzer.recommendations()

    def track_open(self, publication_id: str, user_id: str = None) -> None:
        self.tracker.track({"type": "open", "publication_id": publication_id, "user_id": user_id})

    def track_click(self, publication_id: str, url: str = None, user_id: str = None) -> None:
        self.tracker.track({"type": "click", "publication_id": publication_id, "user_id": user_id, "url": url})

