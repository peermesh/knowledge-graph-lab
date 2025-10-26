from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def list_subscribers():
    return {"data": {"subscribers": []}, "meta": {}, "errors": []}
