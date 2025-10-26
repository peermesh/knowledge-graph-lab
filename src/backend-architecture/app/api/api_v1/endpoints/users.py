"""
User management API endpoints for the Backend Architecture Module.

This module provides endpoints for user administration including
user listing, role management, and user status management.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....auth.security import verify_token
from ....core.database import get_db
from ....schemas.auth import UserCreate, UserResponse, UserUpdate

# Create router
router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def list_users(
    role: str = Query(None, description="Filter by user role"),
    is_active: bool = Query(True, description="Filter by active status"),
    limit: int = Query(50, ge=1, le=100, description="Results per page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db)
) -> List[UserResponse]:
    """List users with filtering and pagination."""

    # Build query
    query = "SELECT * FROM users WHERE 1=1"
    params = {}

    if role:
        query += " AND role = :role"
        params["role"] = role

    if is_active is not None:
        query += " AND is_active = :is_active"
        params["is_active"] = is_active

    query += " ORDER BY created_at DESC LIMIT :limit OFFSET :offset"
    params.update({"limit": limit, "offset": offset})

    # Get users
    result = await db.execute(query, params)
    users = result.fetchall()

    return [UserResponse.from_orm(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Get user by ID."""
    result = await db.execute(
        "SELECT * FROM users WHERE id = :user_id",
        {"user_id": user_id}
    )
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    return UserResponse.from_orm(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Update user information (admin only)."""
    # Get existing user
    result = await db.execute(
        "SELECT * FROM users WHERE id = :user_id",
        {"user_id": user_id}
    )
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    # Update fields
    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(user, field, value)

        await db.commit()
        await db.refresh(user)

    return UserResponse.from_orm(user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Delete user (admin only)."""
    # Check if user exists
    result = await db.execute(
        "SELECT * FROM users WHERE id = :user_id",
        {"user_id": user_id}
    )
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    # Soft delete (deactivate)
    user.is_active = False
    await db.commit()

    return {"message": f"User {user_id} deleted successfully"}
