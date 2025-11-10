from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

from src.api.health import router as health_router
from src.api.auth import router as auth_router
from src.api.entities import router as entities_router
from src.api.admin import router as admin_router
from src.models.base import Base
from src.services.db import engine
from src.api.middleware import request_id_middleware


app = FastAPI(title="Backend Module API (MVP)")


@app.on_event("startup")
def on_startup() -> None:
    # Create tables for MVP; switch to migrations in production flows
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(entities_router)
app.include_router(admin_router)


@app.middleware("http")
async def add_request_id(request, call_next):
    return await request_id_middleware(request, call_next)


@app.get("/contracts/openapi.yaml", include_in_schema=False)
def get_openapi_yaml() -> FileResponse:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(base_dir, "specs", "001-backend-module-app", "contracts", "openapi.yaml")
    return FileResponse(path)

