from fastapi import APIRouter
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
