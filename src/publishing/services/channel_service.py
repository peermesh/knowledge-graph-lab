from typing import Optional
from uuid import UUID
from ..models.channel import Channel
from ..core.database import get_async_session
from sqlalchemy import select


class ChannelService:
    async def get_channel(self, channel_id: str) -> Optional[Channel]:
        async with get_async_session() as session:
            try:
                uuid_value = UUID(channel_id)
            except Exception:
                return None
            result = await session.execute(select(Channel).where(Channel.id == uuid_value))
            return result.scalar_one_or_none()
