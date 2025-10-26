class PersonalizationEngine:
    async def score(self, user_profile: dict, content: list) -> list:
        # Placeholder scoring logic for tests; returns content unchanged
        return content
from typing import Dict, Any, List

class PersonalizationEngine:
    def match_content(self, subscriber_profile: Dict[str, Any], content_candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Minimal scoring: filter by topics if provided
        interests = set((subscriber_profile or {}).get("topics", []))
        if not interests:
            return content_candidates
        return [c for c in content_candidates if interests.intersection(set(c.get("topics", [])))]