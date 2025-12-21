from fastapi import APIRouter
from .responses import success_response

router = APIRouter()

@router.get("/ws")
async def ws_stub():
    return success_response(data={"note": "websocket stub"})

