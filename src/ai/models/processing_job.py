"""Processing job and quality metrics models"""

from sqlalchemy import Column, String, Integer, DECIMAL, TEXT, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship as orm_relationship

from .base import Base, TimestampMixin


class DocumentProcessingJob(Base, TimestampMixin):
    """Tracks document processing lifecycle and results"""
    
    __tablename__ = "document_processing_jobs"
    
    document_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    status = Column(String(20), nullable=False, index=True)
    priority = Column(String(10), nullable=False, default='normal', index=True)
    extraction_config = Column(JSONB)
    entities_extracted = Column(Integer, default=0)
    relationships_found = Column(Integer, default=0)
    processing_time_seconds = Column(DECIMAL(8, 2))
    error_message = Column(TEXT)
    retry_count = Column(Integer, nullable=False, default=0)
    started_at = Column(TIMESTAMP)
    completed_at = Column(TIMESTAMP)
    
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'processing', 'completed', 'failed')",
            name='check_job_status'
        ),
        CheckConstraint(
            "priority IN ('high', 'normal', 'low')",
            name='check_job_priority'
        ),
        CheckConstraint(
            'retry_count >= 0',
            name='check_non_negative_retry_count'
        ),
    )
    
    def __repr__(self):
        return (f"<DocumentProcessingJob(id={self.id}, "
                f"status={self.status}, "
                f"priority={self.priority})>")


class ProcessingQualityMetric(Base, TimestampMixin):
    """Stores quality metrics and performance data"""
    
    __tablename__ = "processing_quality_metrics"
    
    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey('document_processing_jobs.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    metric_type = Column(String(50), nullable=False, index=True)
    entity_type = Column(String(50), index=True)
    value = Column(DECIMAL(10, 4), nullable=False)
    sample_size = Column(Integer)
    confidence_interval = Column(DECIMAL(5, 4))
    calculated_at = Column(TIMESTAMP, nullable=False, index=True)
    job_metadata = Column(JSONB)
    
    # Relationship to DocumentProcessingJob
    job = orm_relationship("DocumentProcessingJob", backref="quality_metrics")
    
    __table_args__ = (
        CheckConstraint(
            "metric_type IN ('accuracy', 'precision', 'recall', 'latency', 'cost')",
            name='check_metric_type'
        ),
        CheckConstraint(
            'sample_size IS NULL OR sample_size > 0',
            name='check_positive_sample_size'
        ),
    )
    
    def __repr__(self):
        return (f"<ProcessingQualityMetric(id={self.id}, "
                f"type={self.metric_type}, "
                f"value={self.value})>")

