from fastapi import APIRouter
from datetime import datetime
import uuid
from .responses import success_response

router = APIRouter()

@router.get("/overview")
async def overview():
    return success_response(
        data={"widgets": []},
        request_id=str(uuid.uuid4())
    )
