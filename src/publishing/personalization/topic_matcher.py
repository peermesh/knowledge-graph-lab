from typing import List, Dict, Any


class TopicMatcher:
    def filter_by_topics(self, contents: List[Dict[str, Any]], topics: List[str]) -> List[Dict[str, Any]]:
        wanted = set(topics or [])
        return [c for c in contents if wanted.intersection(set(c.get("topics", [])))]

