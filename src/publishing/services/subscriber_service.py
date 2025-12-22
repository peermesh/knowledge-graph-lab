from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from ..core.database import async_session_factory
from ..models.subscriber import Subscriber
from .preference_validation import PreferenceValidationService
from .unsubscribe_service import UnsubscribeService
from .notification_service import NotificationService


class SubscriberService:
    def __init__(self) -> None:
        self.validator = PreferenceValidationService()
        self.unsub_service = UnsubscribeService()
        self.notification_service = NotificationService()
    async def create_subscriber(self, email: str, user_id: Optional[str] = None,
                                preferred_channels: Optional[List[str]] = None,
                                topic_interests: Optional[dict] = None,
                                frequency_settings: Optional[dict] = None) -> Subscriber:
        preferred_channels = preferred_channels or []
        topic_interests = topic_interests or {}
        frequency_settings = frequency_settings or {}

        try:
            async with async_session_factory() as session:
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
        except IntegrityError as e:
            # Check if it's a duplicate email error
            if "email" in str(e.orig).lower() or "unique" in str(e.orig).lower():
                raise HTTPException(
                    status_code=409,
                    detail=f"Subscriber with email '{email}' already exists"
                )
            raise HTTPException(
                status_code=409,
                detail="A subscriber with this information already exists"
            )

    async def list_subscribers(self, limit: int = 50, offset: int = 0) -> List[Subscriber]:
        async with async_session_factory() as session:
            result = await session.execute(
                select(Subscriber).order_by(desc(Subscriber.created_at)).limit(limit).offset(offset)
            )
            return result.scalars().all()

    async def update_subscriber_preferences(
        self,
        subscriber_id: str,
        *,
        preferred_channels: Optional[List[str]] = None,
        topic_interests: Optional[Dict[str, Any]] = None,
        frequency_settings: Optional[Dict[str, Any]] = None,
    ) -> Optional[Subscriber]:
        # Validate preferences (no-op validator for now)
        payload = {
            "preferred_channels": preferred_channels,
            "topic_interests": topic_interests,
            "frequency_settings": frequency_settings,
        }
        if not self.validator.validate(payload):
            return None

        async with async_session_factory() as session:
            subscriber = await session.get(Subscriber, subscriber_id)
            if not subscriber:
                return None
            if preferred_channels is not None:
                subscriber.preferred_channels = preferred_channels
            if topic_interests is not None:
                subscriber.topic_interests = topic_interests
            if frequency_settings is not None:
                subscriber.frequency_settings = frequency_settings
            subscriber.updated_at = datetime.utcnow()
            await session.commit()

        # Fire-and-forget notification stub
        self.notification_service.notify_preference_change(subscriber.email)
        return subscriber

    async def unsubscribe(self, email: str) -> bool:
        # Workflow stub: call service, then update status
        if not self.unsub_service.unsubscribe(email):
            return False
        async with async_session_factory() as session:
            result = await session.execute(select(Subscriber).where(Subscriber.email == email))
            subscriber = result.scalars().first()
            if not subscriber:
                return False
            subscriber.subscription_status = "unsubscribed"
            subscriber.updated_at = datetime.utcnow()
            await session.commit()
            return True
