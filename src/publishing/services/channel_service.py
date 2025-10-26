from typing import Optional
from ..models.channel import Channel
from ..core.database import get_async_session
from sqlalchemy import select


class ChannelService:
    async def get_channel(self, channel_id: str) -> Optional[Channel]:
        async with get_async_session() as session:
            result = await session.execute(select(Channel).where(Channel.id == channel_id))
            return result.scalar_one_or_none()
