"""
TopicMatcher for topic-based content filtering.

Provides topic-based filtering for personalized content delivery.
"""
from typing import List, Dict, Any


class TopicMatcher:
    """Topic-based content filtering and matching service."""

    def filter_by_topics(
        self,
        contents: List[Dict[str, Any]],
        topics: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Filter content by matching topics.
        
        Args:
            contents: Content items with 'topics' list
            topics: Desired topic filters
            
        Returns:
            Content matching at least one topic
        """
        wanted = set(topics or [])
        return [
            c for c in contents
            if wanted.intersection(set(c.get("topics", [])))
        ]

