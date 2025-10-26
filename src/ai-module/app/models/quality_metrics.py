"""
Quality metrics model for tracking AI processing performance and accuracy.

This model stores metrics for monitoring entity extraction quality,
processing performance, and system health over time.
"""

from typing import Any, Dict, Optional

from sqlalchemy import DECIMAL, CheckConstraint, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ProcessingQualityMetrics(Base):
    """Model for tracking processing quality and performance metrics."""

    __tablename__ = "processing_quality_metrics"

    # Reference to processing job
    job_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("document_processing_jobs.id"),
        nullable=False,
        index=True
    )

    # Metric information
    metric_type: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False,
        index=True
    )
    entity_type: Mapped[Optional[str]] = mapped_column(
        VARCHAR(50),
        nullable=True,
        index=True
    )
    value: Mapped[float] = mapped_column(
        DECIMAL(10, 4),
        nullable=False
    )

    # Statistical information
    sample_size: Mapped[Optional[int]] = mapped_column(
        INTEGER,
        nullable=True
    )
    confidence_interval: Mapped[Optional[float]] = mapped_column(
        DECIMAL(5, 4),
        nullable=True
    )

    # Additional context
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # Relationship
    job: Mapped["DocumentProcessingJob"] = relationship(
        "DocumentProcessingJob",
        back_populates="quality_metrics"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "metric_type IN ('accuracy', 'precision', 'recall', 'latency', 'cost', 'throughput')",
            name="check_metric_type"
        ),
        CheckConstraint(
            "value >= 0",
            name="check_metric_value_positive"
        ),
        Index("idx_metrics_job_type", "job_id", "metric_type"),
        Index("idx_metrics_entity_type", "entity_type", "metric_type"),
    )

    def __repr__(self) -> str:
        return (
            "<ProcessingQualityMetrics("
            f"id={self.id}, "
            f"job={self.job_id}, "
            f"type='{self.metric_type}', "
            f"entity_type='{self.entity_type}', "
            f"value={self.value}"
            ")>"
        )
