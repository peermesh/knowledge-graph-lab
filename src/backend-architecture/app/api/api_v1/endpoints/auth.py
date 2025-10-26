"""
Authentication API endpoints for the Backend Architecture Module.

This module provides authentication endpoints including login, logout,
token refresh, and user registration.
"""

from datetime import datetime, timedelta
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ....auth.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
    generate_session_id
)
from ....core.database import get_db
from ....models import User, UserSession
from ....schemas.auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    RefreshTokenRequest,
    PasswordChange,
    UserUpdate
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Create router
router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Register a new user."""
    # Check if user already exists
    existing = await db.execute(
        "SELECT * FROM users WHERE email = :email",
        {"email": user_data.email}
    )
    if existing.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Create new user
    user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        is_active=True
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return UserResponse.from_orm(user)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Token:
    """Authenticate user and return tokens."""
    # Find user by email
    result = await db.execute(
        "SELECT * FROM users WHERE email = :email AND is_active = true",
        {"email": form_data.username}
    )
    user = result.first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Update last login
    user.last_login = datetime.utcnow().isoformat()
    await db.commit()

    # Create tokens
    token_data = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    # Create session
    session = UserSession(
        user_id=user.id,
        session_id=generate_session_id(),
        access_token=access_token,
        refresh_token=refresh_token,
        ip_address="127.0.0.1",  # In real implementation, get from request
        expires_at=(datetime.utcnow() + timedelta(minutes=30)).isoformat(),
        refresh_expires_at=(datetime.utcnow() + timedelta(days=7)).isoformat()
    )

    db.add(session)
    await db.commit()

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=1800  # 30 minutes
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
) -> Token:
    """Refresh access token using refresh token."""
    # Verify refresh token
    payload = verify_token(refresh_request.refresh_token, "refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Find user
    result = await db.execute(
        "SELECT * FROM users WHERE id = :user_id AND is_active = true",
        {"user_id": payload["user_id"]}
    )
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Create new tokens
    token_data = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    # Update session
    await db.execute(
        """
        UPDATE user_sessions
        SET access_token = :access_token,
            refresh_token = :refresh_token,
            updated_at = NOW()
        WHERE user_id = :user_id AND is_active = true
        """,
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id
        }
    )
    await db.commit()

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=1800
    )


@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """Logout user and invalidate session."""
    # Verify token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # Deactivate user sessions
    await db.execute(
        "UPDATE user_sessions SET is_active = false WHERE user_id = :user_id",
        {"user_id": payload["user_id"]}
    )
    await db.commit()

    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Get current user information."""
    # Verify token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # Get user
    result = await db.execute(
        "SELECT * FROM users WHERE id = :user_id AND is_active = true",
        {"user_id": payload["user_id"]}
    )
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse.from_orm(user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Update current user information."""
    # Verify token and get user
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    result = await db.execute(
        "SELECT * FROM users WHERE id = :user_id AND is_active = true",
        {"user_id": payload["user_id"]}
    )
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update fields
    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(user, field, value)

        await db.commit()
        await db.refresh(user)

    return UserResponse.from_orm(user)


@router.post("/change-password")
async def change_password(
    password_change: PasswordChange,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """Change user password."""
    # Verify token and get user
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    result = await db.execute(
        "SELECT * FROM users WHERE id = :user_id AND is_active = true",
        {"user_id": payload["user_id"]}
    )
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verify current password
    if not verify_password(password_change.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Update password
    user.password_hash = get_password_hash(password_change.new_password)
    await db.commit()

    return {"message": "Password changed successfully"}
