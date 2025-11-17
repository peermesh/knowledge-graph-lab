from typing import Optional
from ..models.channel import Channel
from ..core.database import async_session_factory
from sqlalchemy import select


class ChannelService:
    async def get_channel(self, channel_id: str) -> Optional[Channel]:
        async with async_session_factory() as session:
            # Convert channel_id to string for comparison (database stores as VARCHAR)
            channel_id_str = str(channel_id) if channel_id else None
            result = await session.execute(select(Channel).where(Channel.id == channel_id_str))
            return result.scalar_one_or_none()
