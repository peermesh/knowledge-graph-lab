from typing import Dict, Any
import httpx
from ..core.config import settings


class DiscordService:
    def __init__(self):
        self.base_url = "https://discord.com/api/v10"
        self.token = settings.DISCORD_BOT_TOKEN

    async def send_message(self, channel_id: str, content: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bot {self.token}", "Content-Type": "application/json"}
        payload = {"content": content}
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(f"{self.base_url}/channels/{channel_id}/messages", json=payload, headers=headers)
            return r.json()
