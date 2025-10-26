from typing import Dict, Any


class WebhookService:
    def send(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "ok"}

