from fastapi import APIRouter

router = APIRouter()

# Placeholder endpoints for channels (to satisfy router include)
@router.get("")
async def list_channels():
    return {"data": {"channels": []}, "meta": {}, "errors": []}
