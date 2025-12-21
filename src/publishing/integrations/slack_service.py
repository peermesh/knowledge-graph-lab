"""
Slack API Integration Service.

Delivers notifications and content updates to Slack channels.
Includes placeholder mode for testing without credentials.

Constitution Compliance:
- External Dependencies: Slack API for team notifications
- Multi-Channel Publishing: Slack as a primary delivery channel
- Error Handling: Comprehensive retry and failure tracking
"""

import httpx
import structlog
from typing import Dict, List, Optional
from datetime import datetime

from ..core.config import settings


logger = structlog.get_logger(__name__)


class SlackService:
    """Slack API service with placeholder mode for testing."""

    def __init__(self):
        """Initialize Slack API client."""
        self.logger = logger
        self.bot_token = settings.SLACK_BOT_TOKEN
        self.is_placeholder = self._is_placeholder_mode()
        self.base_url = "https://slack.com/api"

        if not self.is_placeholder:
            self.headers = {
                "Authorization": f"Bearer {self.bot_token}",
                "Content-Type": "application/json"
            }
            self.logger.info("Slack API client initialized")
        else:
            self.logger.info("Slack service running in placeholder mode")

    def _is_placeholder_mode(self) -> bool:
        """Check if running in placeholder mode (no real credentials)."""
        return (
            not self.bot_token or
            self.bot_token in ("", "placeholder", "placeholder-slack-bot-token", "xoxb-your-bot-token")
        )

    async def send_message(
        self,
        channel: str,
        text: str,
        blocks: Optional[List[Dict]] = None,
        thread_ts: Optional[str] = None
    ) -> Dict:
        """
        Send message to Slack channel.
        
        Args:
            channel: Channel ID or name (e.g., "#general" or "C1234567890")
            text: Plain text message (also used as fallback for blocks)
            blocks: Rich message blocks (optional)
            thread_ts: Thread timestamp for replies (optional)
            
        Returns:
            Dict with status and message details
        """
        if self.is_placeholder:
            return self._send_placeholder_message(channel, text, blocks)

        try:
            payload = {
                "channel": channel,
                "text": text
            }

            if blocks:
                payload["blocks"] = blocks

            if thread_ts:
                payload["thread_ts"] = thread_ts

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat.postMessage",
                    headers=self.headers,
                    json=payload,
                    timeout=10.0
                )

            result = response.json()

            if result.get("ok"):
                self.logger.info(
                    "Slack message sent successfully",
                    channel=channel,
                    ts=result.get("ts")
                )
                return {
                    "status": "sent",
                    "channel": channel,
                    "ts": result.get("ts"),
                    "provider": "slack",
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                error = result.get("error", "unknown_error")
                self.logger.error("Slack API error", error=error, channel=channel)
                return {
                    "status": "failed",
                    "error": error,
                    "provider": "slack"
                }

        except Exception as e:
            self.logger.error("Slack message send failed", error=str(e), channel=channel)
            return {
                "status": "failed",
                "error": str(e),
                "provider": "slack"
            }

    def _send_placeholder_message(
        self,
        channel: str,
        text: str,
        blocks: Optional[List[Dict]] = None
    ) -> Dict:
        """Simulate Slack message in placeholder mode."""
        self.logger.info(
            "💬 PLACEHOLDER SLACK MESSAGE (not actually sent)",
            channel=channel,
            text=text[:100] + "..." if len(text) > 100 else text
        )

        return {
            "status": "simulated",
            "channel": channel,
            "ts": f"placeholder-{datetime.utcnow().timestamp()}",
            "provider": "placeholder",
            "timestamp": datetime.utcnow().isoformat(),
            "note": "Message not sent - running in placeholder mode. Configure Slack credentials in .env"
        }

    async def update_message(
        self,
        channel: str,
        ts: str,
        text: str,
        blocks: Optional[List[Dict]] = None
    ) -> Dict:
        """Update an existing Slack message."""
        if self.is_placeholder:
            return {
                "status": "simulated",
                "note": "Update not performed in placeholder mode"
            }

        try:
            payload = {
                "channel": channel,
                "ts": ts,
                "text": text
            }

            if blocks:
                payload["blocks"] = blocks

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat.update",
                    headers=self.headers,
                    json=payload,
                    timeout=10.0
                )

            result = response.json()

            if result.get("ok"):
                self.logger.info("Slack message updated", channel=channel, ts=ts)
                return {
                    "status": "updated",
                    "channel": channel,
                    "ts": ts,
                    "provider": "slack"
                }
            else:
                error = result.get("error", "unknown_error")
                self.logger.error("Slack update error", error=error, channel=channel)
                return {
                    "status": "failed",
                    "error": error
                }

        except Exception as e:
            self.logger.error("Slack message update failed", error=str(e))
            return {
                "status": "failed",
                "error": str(e)
            }

    async def send_direct_message(self, user_id: str, text: str) -> Dict:
        """Send direct message to a user."""
        if self.is_placeholder:
            return self._send_placeholder_message(f"@{user_id}", text, None)

        # Open DM channel first
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/conversations.open",
                    headers=self.headers,
                    json={"users": user_id},
                    timeout=10.0
                )

            result = response.json()
            if result.get("ok"):
                channel_id = result["channel"]["id"]
                return await self.send_message(channel_id, text)
            else:
                error = result.get("error", "unknown_error")
                return {
                    "status": "failed",
                    "error": f"Failed to open DM: {error}"
                }

        except Exception as e:
            self.logger.error("Slack DM failed", error=str(e), user=user_id)
            return {
                "status": "failed",
                "error": str(e)
            }


# Global Slack service instance
slack_service = SlackService()


