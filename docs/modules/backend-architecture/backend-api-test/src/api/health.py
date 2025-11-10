import logging
from fastapi import APIRouter
from sqlalchemy import text

from src.services.db import engine


router = APIRouter(prefix="/health", tags=["health"])
logger = logging.getLogger("health")


@router.get("/ready")
def readiness():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        status = "ok"
        deps = {"database": "ok"}
    except Exception:
        status = "degraded"
        deps = {"database": "error"}
    logger.info("health_ready", extra={"status": status, "dependencies": deps})
    return {"status": status, "dependencies": deps}

