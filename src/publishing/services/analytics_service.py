from typing import Dict, Any

from ..analytics.engagement_tracker import EngagementTracker
from ..analytics.metrics_collector import MetricsCollector
from ..optimization.performance_analyzer import PerformanceAnalyzer


class AnalyticsService:
    def __init__(self) -> None:
        self.tracker = EngagementTracker()
        self.collector = MetricsCollector()
        self.analyzer = PerformanceAnalyzer()

    async def get_engagement_summary(self, channel_id: str = None) -> Dict[str, Any]:
        return await self.collector.summarize(channel_id=channel_id)
    
    async def get_engagement_for_channel(self, channel_id: str) -> Dict[str, Any]:
        return await self.collector.get_engagement_for_channel(channel_id)

    def get_performance(self) -> Dict[str, Any]:
        return self.analyzer.recommendations()

    async def track_open(self, publication_id: str, channel_id: str = None, user_id: str = None) -> None:
        await self.tracker.track({
            "type": "open", 
            "publication_id": publication_id, 
            "channel_id": channel_id,
            "user_id": user_id
        })

    async def track_click(self, publication_id: str, channel_id: str = None, url: str = None, user_id: str = None) -> None:
        await self.tracker.track({
            "type": "click", 
            "publication_id": publication_id, 
            "channel_id": channel_id,
            "user_id": user_id, 
            "url": url
        })

