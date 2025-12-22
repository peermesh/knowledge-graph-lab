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
    # #region agent log
    import json, time
    try:
        with open('/Users/benschreiber/Desktop/knowledge-graph-lab/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"id":"log_subscriber_entry","timestamp":int(time.time()*1000),"location":"subscribers.py:27","message":"create_subscriber called","data":{"email":request.email},"sessionId":"debug-session","runId":"run1","hypothesisId":"C"})+"\n")
    except (FileNotFoundError, OSError):
        pass
    # #endregion
    sub = await service.create_subscriber(
        email=request.email,
        user_id=str(request.user_id) if request.user_id else None,
        preferred_channels=request.preferred_channels,
        topic_interests=request.topic_interests,
        frequency_settings=request.frequency_settings,
    )
    # #region agent log
    try:
        with open('/Users/benschreiber/Desktop/knowledge-graph-lab/.cursor/debug.log', 'a') as f:
            f.write(json.dumps({"id":"log_subscriber_exit","timestamp":int(time.time()*1000),"location":"subscribers.py:35","message":"create_subscriber returning","data":{"subscriber_id":sub.get("id") if isinstance(sub, dict) else None},"sessionId":"debug-session","runId":"run1","hypothesisId":"C"})+"\n")
    except (FileNotFoundError, OSError):
        pass
    # #endregion
    return success_response(data=sub)
