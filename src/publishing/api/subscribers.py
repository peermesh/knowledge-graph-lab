from fastapi import APIRouter, Body
from datetime import datetime
import uuid
from ..services.subscriber_service import SubscriberService
from ..schemas.subscribers import (
    SubscriberCreateRequest,
    SubscriberListResponse,
    SubscriberResponse,
)
from ..core.config import settings
from ..state import IN_MEMORY_SUBSCRIBERS

router = APIRouter()
service = SubscriberService()


@router.get("", response_model=SubscriberListResponse)
async def list_subscribers(limit: int = 50, offset: int = 0):
    if settings.DEBUG:
        return {
            "data": {"subscribers": IN_MEMORY_SUBSCRIBERS[:limit]},
            "meta": {"timestamp": datetime.utcnow().isoformat()},
            "errors": [],
        }

    subs = await service.list_subscribers(limit=limit, offset=offset)
    return {
        "data": {"subscribers": subs},
        "meta": {"timestamp": datetime.utcnow().isoformat()},
        "errors": [],
    }


@router.post("", response_model=SubscriberResponse)
async def create_subscriber(request: SubscriberCreateRequest = Body(...)):
    if settings.DEBUG:
        now = datetime.utcnow().isoformat()
        sub = {
            "id": str(uuid.uuid4()),
            "email": request.email,
            "user_id": str(request.user_id) if request.user_id else None,
            "preferred_channels": request.preferred_channels,
            "topic_interests": request.topic_interests,
            "frequency_settings": request.frequency_settings,
            "subscription_status": "active",
            "created_at": now,
            "updated_at": now,
        }
        IN_MEMORY_SUBSCRIBERS.append(sub)
        return {"data": sub, "meta": {"timestamp": now}, "errors": []}

    sub = await service.create_subscriber(
        email=request.email,
        user_id=str(request.user_id) if request.user_id else None,
        preferred_channels=request.preferred_channels,
        topic_interests=request.topic_interests,
        frequency_settings=request.frequency_settings,
    )
    return {
        "data": sub,
        "meta": {"timestamp": datetime.utcnow().isoformat()},
        "errors": [],
    }
