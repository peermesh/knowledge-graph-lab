from fastapi import APIRouter, Query
from datetime import datetime
import uuid

from ..services.analytics_service import AnalyticsService
from .responses import success_response

router = APIRouter()
service = AnalyticsService()

@router.get("/engagement")
async def get_engagement(channel_id: str = Query(None, description="Filter by channel ID")):
    correlation_id = str(uuid.uuid4())
    return success_response(
        data=await service.get_engagement_summary(channel_id=channel_id),
        request_id=correlation_id
    )

@router.get("/engagement/channel/{channel_id}")
async def get_channel_engagement(channel_id: str):
    correlation_id = str(uuid.uuid4())
    return success_response(
        data=await service.get_engagement_for_channel(channel_id),
        request_id=correlation_id
    )

@router.get("/performance")
async def get_performance():
    correlation_id = str(uuid.uuid4())
    return success_response(
        data=service.get_performance(),
        request_id=correlation_id
    )


@router.get("/engagement/track/open")
@router.post("/engagement/track/open")
async def track_open(
    publication_id: str = Query(..., description="Publication ID"),
    channel_id: str = Query(None, description="Channel ID (optional, for channel-specific tracking)"),
    user_id: str = Query(None)
):
    """Track email open event. Returns a 1x1 transparent pixel for tracking.
    
    This endpoint can be called via GET (for tracking pixels) or POST (for API calls).
    """
    correlation_id = str(uuid.uuid4())
    await service.track_open(publication_id, channel_id=channel_id, user_id=user_id)
    
    # Return a 1x1 transparent pixel for GET requests (tracking pixel)
    from fastapi.responses import Response
    # 1x1 transparent GIF pixel
    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x04\x01\x00\x3b'
    
    return Response(content=pixel, media_type="image/gif")


@router.get("/engagement/track/click")
@router.post("/engagement/track/click")
async def track_click(
    publication_id: str = Query(..., description="Publication ID"),
    channel_id: str = Query(None, description="Channel ID (optional, for channel-specific tracking)"),
    url: str = Query(..., description="Clicked URL to redirect to"),
    user_id: str = Query(None),
):
    """Track email click event and redirect to the original URL.
    
    This endpoint tracks the click event and then redirects to the original URL.
    """
    from fastapi.responses import RedirectResponse
    
    correlation_id = str(uuid.uuid4())
    await service.track_click(publication_id, channel_id=channel_id, url=url, user_id=user_id)
    
    # Redirect to the original URL after tracking
    return RedirectResponse(url=url, status_code=302)
