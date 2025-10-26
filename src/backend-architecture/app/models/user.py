"""
User model for authentication and authorization.

This model manages user accounts, authentication credentials,
and role-based permissions for the backend system.
"""

from typing import List, Optional

from sqlalchemy import VARCHAR, Boolean, CheckConstraint, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    """Model for system users with authentication and authorization."""

    __tablename__ = "users"

    # Authentication fields
    email: Mapped[str] = mapped_column(
        VARCHAR(255),
        unique=True,
        nullable=False,
        index=True
    )
    password_hash: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False
    )

    # User profile
    first_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    last_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    role: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False,
        default="user",
        index=True
    )

    # Account status
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_login: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    sessions: Mapped[List["UserSession"]] = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    api_requests: Mapped[List["APIRequest"]] = relationship(
        "APIRequest",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "role IN ('user', 'admin', 'moderator', 'researcher')",
            name="check_user_role"
        ),
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$'",
            name="check_email_format"
        ),
        Index("idx_users_email_role", "email", "role"),
        Index("idx_users_last_login", "last_login"),
    )

    def __repr__(self) -> str:
        return (
            "<User("
            f"id={self.id}, "
            f"email='{self.email}', "
            f"role='{self.role}', "
            f"active={self.is_active}"
            ")>"
        )

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"

    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == "admin"

    def can_access(self, required_role: str) -> bool:
        """Check if user can access resource requiring specific role."""
        role_hierarchy = {
            "user": 1,
            "researcher": 2,
            "moderator": 3,
            "admin": 4
        }
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(required_role, 0)
