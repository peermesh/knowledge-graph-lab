from fastapi import APIRouter

router = APIRouter()

@router.get("/engagement")
async def get_engagement():
    return {"data": {"summary": {}}, "meta": {}, "errors": []}

@router.get("/performance")
async def get_performance():
    return {"data": {"recommendations": []}, "meta": {}, "errors": []}
