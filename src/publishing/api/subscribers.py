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
from ..core.database import get_async_session
from ..models.subscriber import Subscriber
from sqlalchemy import select
from .responses import success_response

router = APIRouter()
service = SubscriberService()


@router.get("", response_model=SubscriberListResponse)
async def list_subscribers(limit: int = 50, offset: int = 0):
    subs = await service.list_subscribers(limit=limit, offset=offset)
    return success_response(data={"subscribers": subs})


@router.post("", response_model=SubscriberResponse)
async def create_subscriber(request: SubscriberCreateRequest = Body(...)):
    sub = await service.create_subscriber(
        email=request.email,
        user_id=str(request.user_id) if request.user_id else None,
        preferred_channels=request.preferred_channels,
        topic_interests=request.topic_interests,
        frequency_settings=request.frequency_settings,
    )
    return success_response(data=sub)
