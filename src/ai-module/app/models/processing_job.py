"""
Processing job model for tracking async document processing operations.

This model manages the lifecycle of document processing jobs including
status tracking, error handling, and performance metrics.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy import DECIMAL, INTEGER, TEXT, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class DocumentProcessingJob(Base):
    """Model for tracking document processing jobs."""

    __tablename__ = "document_processing_jobs"

    # Job identification
    document_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True
    )

    # Job status and lifecycle
    status: Mapped[str] = mapped_column(
        VARCHAR(20),
        nullable=False,
        default="pending",
        index=True
    )
    priority: Mapped[str] = mapped_column(
        VARCHAR(10),
        nullable=False,
        default="normal"
    )

    # Processing configuration
    extraction_config: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False
    )

    # Results tracking
    entities_extracted: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        default=0
    )
    relationships_found: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        default=0
    )
    processing_time_seconds: Mapped[Optional[float]] = mapped_column(
        DECIMAL(8, 2),
        nullable=True
    )

    # Error handling
    error_message: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    retry_count: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        default=0
    )

    # Timing
    started_at: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    completed_at: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    # Relationships
    quality_metrics: Mapped[List["ProcessingQualityMetrics"]] = relationship(
        "ProcessingQualityMetrics",
        back_populates="job",
        cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'processing', 'completed', 'failed', 'cancelled')",
            name="check_job_status"
        ),
        CheckConstraint(
            "priority IN ('high', 'normal', 'low')",
            name="check_job_priority"
        ),
        CheckConstraint(
            "retry_count >= 0",
            name="check_retry_count"
        ),
        Index("idx_jobs_status_priority", "status", "priority"),
        Index("idx_jobs_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return (
            "<DocumentProcessingJob("
            f"id={self.id}, "
            f"status='{self.status}', "
            f"priority='{self.priority}', "
            f"entities={self.entities_extracted}, "
            f"relationships={self.relationships_found}"
            ")>"
        )
