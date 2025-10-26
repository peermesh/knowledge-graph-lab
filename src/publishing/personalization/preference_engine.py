class PersonalizationEngine:
    async def score(self, user_profile: dict, content: list) -> list:
        # Placeholder scoring logic for tests; returns content unchanged
        return content
from typing import Dict, Any, List

class PersonalizationEngine:
    def match_content(self, subscriber_profile: Dict[str, Any], content_candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Placeholder: return as-is
        return content_candidates