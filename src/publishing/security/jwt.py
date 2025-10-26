from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from ..core.config import settings


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(token: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)) -> dict:
    if token is None or token.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Authentication required")

    jwt_token = token.credentials

    # Delegate validation to Backend module auth service
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(f"{settings.BACKEND_MODULE_URL}/api/v1/auth/validate", headers={"Authorization": f"Bearer {jwt_token}"})

        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return resp.json().get("data", {})
