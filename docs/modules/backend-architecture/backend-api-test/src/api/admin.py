from fastapi import APIRouter, Depends

from src.services.auth_dep import require_admin


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/ping")
def admin_ping(_sub: str = Depends(require_admin)):
    return {"status": "ok", "role": "Admin"}

