from fastapi import APIRouter, HTTPException, Body, Path
from datetime import datetime
import uuid

from ..core.logging import get_logger
from ..services.alert_service import AlertService
from ..schemas.alerts import CreateAlertRequest, AlertResponse
from .responses import success_response


logger = get_logger(__name__)
router = APIRouter()
service = AlertService()


@router.post("", response_model=AlertResponse)
async def create_alert(request: CreateAlertRequest = Body(...)):
    correlation_id = str(uuid.uuid4())
    try:
        alert = service.create_alert(
            content_id=str(request.content_id),
            target_channels=[str(c) for c in request.target_channels],
            priority=request.priority,
        )
        return success_response(data=alert, request_id=correlation_id)
    except Exception as e:
        logger.error("Create alert failed", error=str(e), request_id=correlation_id)
        raise HTTPException(status_code=500, detail="Failed to create alert")


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: str = Path(...)):
    correlation_id = str(uuid.uuid4())
    alert = service.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return success_response(data=alert, request_id=correlation_id)

