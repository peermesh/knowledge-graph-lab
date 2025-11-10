from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from src.services.security import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


class TokenRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/token")
def issue_token(req: TokenRequest):
    # Placeholder: accept any input for scaffolding; wire real auth in later tasks
    if not req.email or not req.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    role = "Admin" if req.email.lower().startswith("admin@") else "User"
    token = create_access_token(subject=req.email, role=role)
    return {"access_token": token, "token_type": "bearer"}

