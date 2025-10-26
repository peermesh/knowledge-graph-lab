from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, desc
from ..core.database import get_async_session
from ..models.subscriber import Subscriber


class SubscriberService:
    async def create_subscriber(self, email: str, user_id: Optional[str] = None,
                                preferred_channels: Optional[List[str]] = None,
                                topic_interests: Optional[dict] = None,
                                frequency_settings: Optional[dict] = None) -> Subscriber:
        preferred_channels = preferred_channels or []
        topic_interests = topic_interests or {}
        frequency_settings = frequency_settings or {}

        async with get_async_session() as session:
            subscriber = Subscriber(
                email=email,
                user_id=user_id,
                preferred_channels=preferred_channels,
                topic_interests=topic_interests,
                frequency_settings=frequency_settings,
                subscription_status="active",
            )
            session.add(subscriber)
            await session.commit()
            return subscriber

    async def list_subscribers(self, limit: int = 50, offset: int = 0) -> List[Subscriber]:
        async with get_async_session() as session:
            result = await session.execute(
                select(Subscriber).order_by(desc(Subscriber.created_at)).limit(limit).offset(offset)
            )
            return result.scalars().all()
