"""
User session model for authentication and session management.

This model tracks active user sessions, JWT tokens, and session lifecycle
for security and user experience management.
"""

from typing import Optional

from sqlalchemy import VARCHAR, Boolean, CheckConstraint, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserSession(Base):
    """Model for tracking user sessions and authentication tokens."""

    __tablename__ = "user_sessions"

    # Session identification
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    session_id: Mapped[str] = mapped_column(
        VARCHAR(255),
        unique=True,
        nullable=False,
        index=True
    )

    # Authentication tokens
    access_token: Mapped[str] = mapped_column(TEXT, nullable=False)
    refresh_token: Mapped[str] = mapped_column(TEXT, nullable=False)

    # Session metadata
    ip_address: Mapped[str] = mapped_column(VARCHAR(45), nullable=False)  # IPv6 compatible
    user_agent: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    device_info: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    # Session lifecycle
    expires_at: Mapped[str] = mapped_column(TEXT, nullable=False, index=True)
    refresh_expires_at: Mapped[str] = mapped_column(TEXT, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "is_active IN (true, false)",
            name="check_session_active"
        ),
        Index("idx_sessions_user_active", "user_id", "is_active"),
        Index("idx_sessions_expires_at", "expires_at"),
    )

    def __repr__(self) -> str:
        return (
            "<UserSession("
            f"id={self.id}, "
            f"user={self.user_id}, "
            f"session_id='{self.session_id}', "
            f"active={self.is_active}"
            ")>"
        )

    def is_expired(self) -> bool:
        """Check if session has expired."""
        from datetime import datetime
        try:
            expires = datetime.fromisoformat(self.expires_at.replace('Z', '+00:00'))
            return datetime.now(expires.tzinfo) > expires
        except ValueError:
            return True  # Invalid timestamp, consider expired

    def can_refresh(self) -> bool:
        """Check if refresh token is still valid."""
        from datetime import datetime
        try:
            refresh_expires = datetime.fromisoformat(
                self.refresh_expires_at.replace('Z', '+00:00')
            )
            return datetime.now(refresh_expires.tzinfo) <= refresh_expires
        except ValueError:
            return False  # Invalid timestamp, cannot refresh
