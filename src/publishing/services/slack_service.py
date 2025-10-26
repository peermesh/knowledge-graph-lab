from typing import Dict, Any
import httpx
from ..core.config import settings


class SlackService:
    def __init__(self):
        self.base_url = "https://slack.com/api"
        self.token = settings.SLACK_BOT_TOKEN

    async def send_message(self, channel: str, text: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        payload = {"channel": channel, "text": text}
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(f"{self.base_url}/chat.postMessage", json=payload, headers=headers)
            return r.json()
