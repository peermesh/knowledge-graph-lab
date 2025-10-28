from fastapi import APIRouter, Query
from datetime import datetime
import uuid

from ..services.analytics_service import AnalyticsService

router = APIRouter()
service = AnalyticsService()

@router.get("/engagement")
async def get_engagement():
    correlation_id = str(uuid.uuid4())
    return {
        "data": service.get_engagement_summary(),
        "meta": {"timestamp": datetime.utcnow().isoformat(), "request_id": correlation_id},
        "errors": [],
    }

@router.get("/performance")
async def get_performance():
    correlation_id = str(uuid.uuid4())
    return {
        "data": service.get_performance(),
        "meta": {"timestamp": datetime.utcnow().isoformat(), "request_id": correlation_id},
        "errors": [],
    }


@router.post("/engagement/track/open")
async def track_open(publication_id: str = Query(..., description="Publication ID"), user_id: str = Query(None)):
    correlation_id = str(uuid.uuid4())
    service.track_open(publication_id, user_id)
    return {
        "data": {"tracked": True, "type": "open", "publication_id": publication_id},
        "meta": {"timestamp": datetime.utcnow().isoformat(), "request_id": correlation_id},
        "errors": [],
    }


@router.post("/engagement/track/click")
async def track_click(
    publication_id: str = Query(..., description="Publication ID"),
    url: str = Query(None, description="Clicked URL"),
    user_id: str = Query(None),
):
    correlation_id = str(uuid.uuid4())
    service.track_click(publication_id, url, user_id)
    return {
        "data": {"tracked": True, "type": "click", "publication_id": publication_id},
        "meta": {"timestamp": datetime.utcnow().isoformat(), "request_id": correlation_id},
        "errors": [],
    }
