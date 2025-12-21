"""
Discord API Integration Service.

Delivers notifications and content updates to Discord channels.
Includes placeholder mode for testing without credentials.

Constitution Compliance:
- External Dependencies: Discord API for community notifications
- Multi-Channel Publishing: Discord as a primary delivery channel
- Error Handling: Comprehensive retry and failure tracking
"""

import httpx
import structlog
from typing import Dict, List, Optional
from datetime import datetime

from ..core.config import settings


logger = structlog.get_logger(__name__)


class DiscordService:
    """Discord API service with placeholder mode for testing."""

    def __init__(self):
        """Initialize Discord API client."""
        self.logger = logger
        self.bot_token = settings.DISCORD_BOT_TOKEN
        self.is_placeholder = self._is_placeholder_mode()
        self.base_url = "https://discord.com/api/v10"

        if not self.is_placeholder:
            self.headers = {
                "Authorization": f"Bot {self.bot_token}",
                "Content-Type": "application/json"
            }
            self.logger.info("Discord API client initialized")
        else:
            self.logger.info("Discord service running in placeholder mode")

    def _is_placeholder_mode(self) -> bool:
        """Check if running in placeholder mode (no real credentials)."""
        return (
            not self.bot_token or
            self.bot_token in ("", "placeholder", "placeholder-discord-bot-token", "your-discord-bot-token")
        )

    async def send_message(
        self,
        channel_id: str,
        content: str,
        embeds: Optional[List[Dict]] = None,
        components: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Send message to Discord channel.
        
        Args:
            channel_id: Discord channel ID (e.g., "1234567890")
            content: Message content (plain text)
            embeds: Rich embeds (optional)
            components: Interactive components like buttons (optional)
            
        Returns:
            Dict with status and message details
        """
        if self.is_placeholder:
            return self._send_placeholder_message(channel_id, content, embeds)

        try:
            payload = {"content": content}

            if embeds:
                payload["embeds"] = embeds

            if components:
                payload["components"] = components

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/channels/{channel_id}/messages",
                    headers=self.headers,
                    json=payload,
                    timeout=10.0
                )

            if response.status_code == 200:
                result = response.json()
                self.logger.info(
                    "Discord message sent successfully",
                    channel_id=channel_id,
                    message_id=result.get("id")
                )
                return {
                    "status": "sent",
                    "channel_id": channel_id,
                    "message_id": result.get("id"),
                    "provider": "discord",
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                error_data = response.json()
                error_message = error_data.get("message", "Unknown error")
                self.logger.error(
                    "Discord API error",
                    status_code=response.status_code,
                    error=error_message,
                    channel_id=channel_id
                )
                return {
                    "status": "failed",
                    "error": error_message,
                    "status_code": response.status_code,
                    "provider": "discord"
                }

        except Exception as e:
            self.logger.error("Discord message send failed", error=str(e), channel_id=channel_id)
            return {
                "status": "failed",
                "error": str(e),
                "provider": "discord"
            }

    def _send_placeholder_message(
        self,
        channel_id: str,
        content: str,
        embeds: Optional[List[Dict]] = None
    ) -> Dict:
        """Simulate Discord message in placeholder mode."""
        self.logger.info(
            "🎮 PLACEHOLDER DISCORD MESSAGE (not actually sent)",
            channel_id=channel_id,
            content=content[:100] + "..." if len(content) > 100 else content
        )

        return {
            "status": "simulated",
            "channel_id": channel_id,
            "message_id": f"placeholder-{datetime.utcnow().timestamp()}",
            "provider": "placeholder",
            "timestamp": datetime.utcnow().isoformat(),
            "note": "Message not sent - running in placeholder mode. Configure Discord credentials in .env"
        }

    async def update_message(
        self,
        channel_id: str,
        message_id: str,
        content: str,
        embeds: Optional[List[Dict]] = None
    ) -> Dict:
        """Update an existing Discord message."""
        if self.is_placeholder:
            return {
                "status": "simulated",
                "note": "Update not performed in placeholder mode"
            }

        try:
            payload = {"content": content}

            if embeds:
                payload["embeds"] = embeds

            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.base_url}/channels/{channel_id}/messages/{message_id}",
                    headers=self.headers,
                    json=payload,
                    timeout=10.0
                )

            if response.status_code == 200:
                self.logger.info("Discord message updated", channel_id=channel_id, message_id=message_id)
                return {
                    "status": "updated",
                    "channel_id": channel_id,
                    "message_id": message_id,
                    "provider": "discord"
                }
            else:
                error_data = response.json()
                error_message = error_data.get("message", "Unknown error")
                self.logger.error("Discord update error", error=error_message)
                return {
                    "status": "failed",
                    "error": error_message
                }

        except Exception as e:
            self.logger.error("Discord message update failed", error=str(e))
            return {
                "status": "failed",
                "error": str(e)
            }

    async def send_embed(
        self,
        channel_id: str,
        title: str,
        description: str,
        color: int = 0x5865F2,  # Discord blurple
        fields: Optional[List[Dict]] = None,
        footer: Optional[Dict] = None,
        thumbnail: Optional[str] = None,
        image: Optional[str] = None
    ) -> Dict:
        """Send rich embed message to Discord channel."""
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat()
        }

        if fields:
            embed["fields"] = fields

        if footer:
            embed["footer"] = footer

        if thumbnail:
            embed["thumbnail"] = {"url": thumbnail}

        if image:
            embed["image"] = {"url": image}

        return await self.send_message(channel_id, "", embeds=[embed])


# Global Discord service instance
discord_service = DiscordService()


