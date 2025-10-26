from fastapi import APIRouter
from datetime import datetime
import uuid

router = APIRouter()

@router.get("/overview")
async def overview():
    return {
        "data": {"widgets": []},
        "meta": {"timestamp": datetime.utcnow().isoformat(), "request_id": str(uuid.uuid4())},
        "errors": []
    }
