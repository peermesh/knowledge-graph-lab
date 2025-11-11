"""Quality monitoring API endpoints"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from src.ai.api.dependencies import get_db
from src.ai.services.quality_monitor import quality_monitor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai/v1", tags=["quality"])


# Response Models
class MetricValue(BaseModel):
    """Single metric value"""
    metric_type: str
    value: float
    entity_type: Optional[str] = None
    calculated_at: str


class DailyReportResponse(BaseModel):
    """Daily quality report"""
    date: str
    jobs_processed: int
    jobs_completed: int
    jobs_failed: int
    total_entities: int
    total_relationships: int
    metrics_by_entity_type: Dict[str, Any]
    low_confidence_entities: int


class QualityAlert(BaseModel):
    """Quality degradation alert"""
    severity: str  # high, medium, low
    entity_type: str
    metric: str
    value: float
    threshold: float
    message: str


class AlertsResponse(BaseModel):
    """Response with quality alerts"""
    alerts: List[QualityAlert]
    total_alerts: int
    timestamp: str


class TrendDataPoint(BaseModel):
    """Single point in trend data"""
    date: str
    avg_value: float
    min_value: float
    max_value: float
    sample_count: int


class TrendAnalysisResponse(BaseModel):
    """Trend analysis response"""
    metric_type: str
    days_analyzed: int
    trend_direction: str  # improving, stable, declining
    daily_data: List[TrendDataPoint]


@router.get("/quality/report/daily", response_model=DailyReportResponse)
async def get_daily_report(
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """
    Get daily quality report for extraction metrics.
    
    If date not provided, returns report for today.
    """
    try:
        # Parse date if provided
        report_date = None
        if date:
            try:
                report_date = datetime.fromisoformat(date)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid date format: {date}. Use YYYY-MM-DD"
                )
        
        # Generate report
        report = await quality_monitor.generate_daily_report(db, report_date)
        
        return DailyReportResponse(**report)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Daily report generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate daily report: {str(e)}"
        )


@router.get("/quality/alerts", response_model=AlertsResponse)
async def get_quality_alerts(
    lookback_hours: int = Query(24, ge=1, le=168, description="Hours to look back (max 7 days)"),
    db: Session = Depends(get_db)
):
    """
    Get quality degradation alerts.
    
    Checks for accuracy drops, high error rates, and other quality issues.
    """
    try:
        alerts = await quality_monitor.check_quality_degradation(
            db,
            lookback_hours=lookback_hours
        )
        
        alert_models = [QualityAlert(**alert) for alert in alerts]
        
        return AlertsResponse(
            alerts=alert_models,
            total_alerts=len(alert_models),
            timestamp=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Get quality alerts failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get quality alerts: {str(e)}"
        )


@router.get("/quality/metrics/{entity_type}")
async def get_metrics_by_type(
    entity_type: str,
    days: int = Query(7, ge=1, le=90, description="Days to look back"),
    db: Session = Depends(get_db)
):
    """
    Get quality metrics for a specific entity type.
    
    Returns aggregated metrics over the specified time period.
    """
    try:
        since = datetime.utcnow() - timedelta(days=days)
        
        metrics = await quality_monitor.get_metrics_by_entity_type(
            db,
            entity_type=entity_type,
            since=since
        )
        
        return metrics
    
    except Exception as e:
        logger.error(f"Get metrics by type failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get metrics: {str(e)}"
        )


@router.get("/quality/trends/{metric_type}", response_model=TrendAnalysisResponse)
async def get_trend_analysis(
    metric_type: str,
    days: int = Query(7, ge=1, le=90, description="Days to analyze"),
    db: Session = Depends(get_db)
):
    """
    Get trend analysis for a specific metric.
    
    Analyzes how a metric has changed over time.
    """
    # Validate metric type
    valid_metrics = ['accuracy', 'precision', 'recall', 'latency', 'cost']
    if metric_type not in valid_metrics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid metric_type. Must be one of: {', '.join(valid_metrics)}"
        )
    
    try:
        trend = await quality_monitor.get_trend_analysis(
            db,
            metric_type=metric_type,
            days=days
        )
        
        return TrendAnalysisResponse(**trend)
    
    except Exception as e:
        logger.error(f"Trend analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get trend analysis: {str(e)}"
        )


@router.get("/quality/problematic-documents")
async def get_problematic_documents(
    hours: int = Query(24, ge=1, le=168, description="Hours to look back"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    db: Session = Depends(get_db)
):
    """
    Get list of documents with low-quality extraction.
    
    Useful for manual review and model retraining.
    """
    try:
        since = datetime.utcnow() - timedelta(hours=hours)
        
        documents = await quality_monitor.identify_problematic_documents(
            db,
            since=since,
            limit=limit
        )
        
        return {
            'problematic_documents': documents,
            'total_count': len(documents),
            'lookback_hours': hours
        }
    
    except Exception as e:
        logger.error(f"Get problematic documents failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get problematic documents: {str(e)}"
        )


# Import timedelta for the endpoints above
from datetime import timedelta

