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

