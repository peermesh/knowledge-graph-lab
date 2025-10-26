"""
Pydantic schemas for authentication and authorization.

These schemas define the request and response formats for
authentication, user management, and authorization operations.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    """Base schema for user data."""

    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    role: str = Field(
        default="user",
        regex="^(user|admin|moderator|researcher)$",
        description="User role"
    )


class UserCreate(UserBase):
    """Schema for creating new users."""

    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters)"
    )

    @validator('password')
    def validate_password(cls, v):
        """Validate password complexity."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")


class UserResponse(UserBase):
    """Schema for user API responses."""

    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication tokens."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")


class TokenData(BaseModel):
    """Schema for token payload data."""

    user_id: str
    email: str
    role: str
    exp: Optional[int] = None


class RefreshTokenRequest(BaseModel):
    """Schema for token refresh requests."""

    refresh_token: str = Field(..., description="Refresh token")


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[str] = Field(None, regex="^(user|admin|moderator|researcher)$")
    is_active: Optional[bool] = None


class PasswordChange(BaseModel):
    """Schema for password change requests."""

    current_password: str = Field(..., description="Current password")
    new_password: str = Field(
        ...,
        min_length=8,
        description="New password (minimum 8 characters)"
    )

    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password complexity."""
        if len(v) < 8:
            raise ValueError('New password must be at least 8 characters')
        return v
