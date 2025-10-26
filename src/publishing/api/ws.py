from fastapi import APIRouter

router = APIRouter()

@router.get("/ws")
async def ws_stub():
    return {"data": {"note": "websocket stub"}, "meta": {}, "errors": []}

