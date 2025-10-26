"""
API request tracking model for monitoring and analytics.

This model logs all API requests for performance monitoring,
security auditing, and usage analytics.
"""

from typing import Optional

from sqlalchemy import DECIMAL, INTEGER, TEXT, CheckConstraint, ForeignKey, Index
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class APIRequest(Base):
    """Model for tracking API requests and performance."""

    __tablename__ = "api_requests"

    # Request identification
    user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )
    endpoint: Mapped[str] = mapped_column(
        VARCHAR(500),
        nullable=False,
        index=True
    )
    method: Mapped[str] = mapped_column(
        VARCHAR(10),
        nullable=False,
        index=True
    )

    # Response data
    status_code: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        index=True
    )
    response_time_ms: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False
    )

    # Request metrics
    request_size_bytes: Mapped[int] = mapped_column(INTEGER, nullable=False)
    response_size_bytes: Mapped[int] = mapped_column(INTEGER, nullable=False)

    # Network information
    ip_address: Mapped[str] = mapped_column(INET, nullable=False)
    user_agent: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    # Error tracking
    error_message: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    # Relationships
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="api_requests"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status_code >= 100 AND status_code <= 599",
            name="check_status_code_range"
        ),
        CheckConstraint(
            "response_time_ms >= 0",
            name="check_response_time_positive"
        ),
        CheckConstraint(
            "method IN ('GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD')",
            name="check_http_method"
        ),
        Index("idx_api_requests_endpoint_method", "endpoint", "method"),
        Index("idx_api_requests_user_timestamp", "user_id", "created_at"),
        Index("idx_api_requests_status_code", "status_code"),
    )

    def __repr__(self) -> str:
        return (
            "<APIRequest("
            f"id={self.id}, "
            f"method='{self.method}', "
            f"endpoint='{self.endpoint}', "
            f"status={self.status_code}, "
            f"response_time={self.response_time_ms}ms"
            ")>"
        )
