"""Quality monitoring service for extraction metrics"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
from collections import defaultdict

from src.ai.models import (
    DocumentProcessingJob,
    ProcessingQualityMetric,
    ExtractedEntity
)

logger = logging.getLogger(__name__)


class QualityMonitor:
    """Service for monitoring extraction quality and generating reports"""
    
    ACCURACY_THRESHOLD = 0.80
    PRECISION_THRESHOLD = 0.85
    RECALL_THRESHOLD = 0.80
    
    def __init__(self):
        """Initialize quality monitor"""
        pass
    
    async def calculate_metrics(
        self,
        db: Session,
        job_id: str,
        ground_truth: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate quality metrics for a processing job.
        
        Args:
            db: Database session
            job_id: Processing job UUID
            ground_truth: Optional ground truth data for validation
        
        Returns:
            Dictionary with calculated metrics
        """
        try:
            job = db.query(DocumentProcessingJob).filter(
                DocumentProcessingJob.id == job_id
            ).first()
            
            if not job:
                logger.error(f"Job {job_id} not found")
                return {}
            
            metrics = {}
            
            # Basic metrics (always available)
            metrics['latency'] = float(job.processing_time_seconds) if job.processing_time_seconds else 0
            metrics['entities_extracted'] = job.entities_extracted or 0
            metrics['relationships_found'] = job.relationships_found or 0
            metrics['cost'] = self._estimate_cost(metrics['entities_extracted'])
            
            # If ground truth provided, calculate accuracy metrics
            if ground_truth:
                accuracy_metrics = self._calculate_accuracy(
                    job_id,
                    ground_truth
                )
                metrics.update(accuracy_metrics)
            
            # Store metrics in database
            await self._store_metrics(db, job_id, metrics)
            
            return metrics
        
        except Exception as e:
            logger.error(f"Metric calculation failed: {e}")
            raise
    
    def _calculate_accuracy(
        self,
        job_id: str,
        ground_truth: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate precision, recall, and accuracy"""
        # Ground truth format:
        # {
        #   'entities': [{'text': '...', 'type': '...'}],
        #   'relationships': [{'source': '...', 'target': '...', 'type': '...'}]
        # }
        
        # This is a simplified version - in production, use actual entity matching
        extracted_entities = ground_truth.get('extracted', [])
        expected_entities = ground_truth.get('expected', [])
        
        if not expected_entities:
            return {}
        
        # Calculate true positives, false positives, false negatives
        true_positives = len(
            set(e['text'] for e in extracted_entities) &
            set(e['text'] for e in expected_entities)
        )
        
        false_positives = len(extracted_entities) - true_positives
        false_negatives = len(expected_entities) - true_positives
        
        # Calculate metrics
        precision = true_positives / len(extracted_entities) if extracted_entities else 0
        recall = true_positives / len(expected_entities) if expected_entities else 0
        
        f1_score = 0
        if precision + recall > 0:
            f1_score = 2 * (precision * recall) / (precision + recall)
        
        return {
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'f1_score': round(f1_score, 4),
            'accuracy': round((precision + recall) / 2, 4)
        }
    
    def _estimate_cost(self, entity_count: int) -> float:
        """
        Estimate processing cost based on entity count.
        
        Rough estimate: $0.10 per document with 5-10 entities
        """
        # Simple linear model
        base_cost = 0.05
        per_entity_cost = 0.01
        
        total_cost = base_cost + (entity_count * per_entity_cost)
        
        return round(total_cost, 2)
    
    async def _store_metrics(
        self,
        db: Session,
        job_id: str,
        metrics: Dict[str, float]
    ):
        """Store metrics in database"""
        try:
            for metric_type, value in metrics.items():
                if metric_type in ['precision', 'recall', 'accuracy', 'latency', 'cost']:
                    metric_record = ProcessingQualityMetric(
                        job_id=job_id,
                        metric_type=metric_type,
                        value=value,
                        calculated_at=datetime.utcnow()
                    )
                    db.add(metric_record)
            
            db.commit()
            logger.info(f"Stored {len(metrics)} metrics for job {job_id}")
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to store metrics: {e}")
    
    async def generate_daily_report(
        self,
        db: Session,
        date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Generate daily quality report.
        
        Args:
            db: Database session
            date: Date for report (default: today)
        
        Returns:
            Daily quality report
        """
        if date is None:
            date = datetime.utcnow()
        
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        try:
            # Get all jobs for the day
            jobs = db.query(DocumentProcessingJob).filter(
                DocumentProcessingJob.created_at >= start_of_day,
                DocumentProcessingJob.created_at < end_of_day
            ).all()
            
            # Get metrics for the day
            metrics = db.query(ProcessingQualityMetric).filter(
                ProcessingQualityMetric.calculated_at >= start_of_day,
                ProcessingQualityMetric.calculated_at < end_of_day
            ).all()
            
            # Aggregate metrics by entity type
            metrics_by_type = defaultdict(list)
            for metric in metrics:
                entity_type = metric.entity_type or 'overall'
                metrics_by_type[entity_type].append({
                    'type': metric.metric_type,
                    'value': float(metric.value)
                })
            
            # Calculate summary statistics
            report = {
                'date': start_of_day.date().isoformat(),
                'jobs_processed': len(jobs),
                'jobs_completed': sum(1 for j in jobs if j.status == 'completed'),
                'jobs_failed': sum(1 for j in jobs if j.status == 'failed'),
                'total_entities': sum(j.entities_extracted or 0 for j in jobs),
                'total_relationships': sum(j.relationships_found or 0 for j in jobs),
                'metrics_by_entity_type': {}
            }
            
            # Add metrics by type
            for entity_type, type_metrics in metrics_by_type.items():
                precision_values = [m['value'] for m in type_metrics if m['type'] == 'precision']
                recall_values = [m['value'] for m in type_metrics if m['type'] == 'recall']
                
                report['metrics_by_entity_type'][entity_type] = {
                    'avg_precision': round(sum(precision_values) / len(precision_values), 4) if precision_values else None,
                    'avg_recall': round(sum(recall_values) / len(recall_values), 4) if recall_values else None,
                    'sample_count': len(type_metrics)
                }
            
            # Identify low-confidence entities
            low_confidence_entities = db.query(ExtractedEntity).filter(
                ExtractedEntity.created_at >= start_of_day,
                ExtractedEntity.created_at < end_of_day,
                ExtractedEntity.confidence < 0.70
            ).count()
            
            report['low_confidence_entities'] = low_confidence_entities
            
            logger.info(f"Generated daily report for {start_of_day.date()}")
            return report
        
        except Exception as e:
            logger.error(f"Daily report generation failed: {e}")
            raise
    
    async def check_quality_degradation(
        self,
        db: Session,
        lookback_hours: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Check for quality degradation in recent processing.
        
        Args:
            db: Database session
            lookback_hours: Hours to look back
        
        Returns:
            List of alerts/issues found
        """
        since = datetime.utcnow() - timedelta(hours=lookback_hours)
        
        alerts = []
        
        try:
            # Get recent metrics
            recent_metrics = db.query(ProcessingQualityMetric).filter(
                ProcessingQualityMetric.calculated_at >= since
            ).all()
            
            # Group by entity type
            metrics_by_type = defaultdict(lambda: defaultdict(list))
            
            for metric in recent_metrics:
                entity_type = metric.entity_type or 'overall'
                metrics_by_type[entity_type][metric.metric_type].append(
                    float(metric.value)
                )
            
            # Check thresholds
            for entity_type, type_metrics in metrics_by_type.items():
                # Check accuracy
                if 'accuracy' in type_metrics:
                    avg_accuracy = sum(type_metrics['accuracy']) / len(type_metrics['accuracy'])
                    if avg_accuracy < self.ACCURACY_THRESHOLD:
                        alerts.append({
                            'severity': 'high',
                            'entity_type': entity_type,
                            'metric': 'accuracy',
                            'value': round(avg_accuracy, 4),
                            'threshold': self.ACCURACY_THRESHOLD,
                            'message': f'Accuracy below threshold for {entity_type}'
                        })
                
                # Check precision
                if 'precision' in type_metrics:
                    avg_precision = sum(type_metrics['precision']) / len(type_metrics['precision'])
                    if avg_precision < self.PRECISION_THRESHOLD:
                        alerts.append({
                            'severity': 'medium',
                            'entity_type': entity_type,
                            'metric': 'precision',
                            'value': round(avg_precision, 4),
                            'threshold': self.PRECISION_THRESHOLD,
                            'message': f'Precision below threshold for {entity_type}'
                        })
            
            # Check low-confidence entity rate
            total_entities = db.query(ExtractedEntity).filter(
                ExtractedEntity.created_at >= since
            ).count()
            
            low_confidence = db.query(ExtractedEntity).filter(
                ExtractedEntity.created_at >= since,
                ExtractedEntity.confidence < 0.70
            ).count()
            
            if total_entities > 0:
                low_conf_rate = low_confidence / total_entities
                if low_conf_rate > 0.30:  # More than 30% low confidence
                    alerts.append({
                        'severity': 'medium',
                        'entity_type': 'overall',
                        'metric': 'low_confidence_rate',
                        'value': round(low_conf_rate, 4),
                        'threshold': 0.30,
                        'message': f'{low_conf_rate:.1%} of entities have low confidence'
                    })
            
            if alerts:
                logger.warning(f"Found {len(alerts)} quality alerts")
            else:
                logger.info("No quality degradation detected")
            
            return alerts
        
        except Exception as e:
            logger.error(f"Quality degradation check failed: {e}")
            raise
    
    async def get_metrics_by_entity_type(
        self,
        db: Session,
        entity_type: str,
        since: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get metrics for a specific entity type.
        
        Args:
            db: Database session
            entity_type: Entity type to query
            since: Start date (default: 7 days ago)
        
        Returns:
            Metrics summary for entity type
        """
        if since is None:
            since = datetime.utcnow() - timedelta(days=7)
        
        try:
            metrics = db.query(ProcessingQualityMetric).filter(
                ProcessingQualityMetric.entity_type == entity_type,
                ProcessingQualityMetric.calculated_at >= since
            ).all()
            
            if not metrics:
                return {
                    'entity_type': entity_type,
                    'sample_count': 0,
                    'message': 'No metrics available'
                }
            
            # Aggregate by metric type
            by_type = defaultdict(list)
            for metric in metrics:
                by_type[metric.metric_type].append(float(metric.value))
            
            summary = {
                'entity_type': entity_type,
                'sample_count': len(metrics),
                'date_range': {
                    'from': since.isoformat(),
                    'to': datetime.utcnow().isoformat()
                }
            }
            
            # Calculate averages
            for metric_type, values in by_type.items():
                summary[f'avg_{metric_type}'] = round(sum(values) / len(values), 4)
                summary[f'min_{metric_type}'] = round(min(values), 4)
                summary[f'max_{metric_type}'] = round(max(values), 4)
            
            return summary
        
        except Exception as e:
            logger.error(f"Get metrics by type failed: {e}")
            raise
    
    async def identify_problematic_documents(
        self,
        db: Session,
        since: Optional[datetime] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Identify documents with low-quality extraction.
        
        Args:
            db: Database session
            since: Start date (default: 24 hours ago)
            limit: Maximum results to return
        
        Returns:
            List of problematic documents
        """
        if since is None:
            since = datetime.utcnow() - timedelta(hours=24)
        
        try:
            # Find jobs with low entity counts or high retry counts
            problematic_jobs = db.query(DocumentProcessingJob).filter(
                DocumentProcessingJob.created_at >= since
            ).filter(
                or_(
                    DocumentProcessingJob.entities_extracted < 1,
                    DocumentProcessingJob.retry_count > 1,
                    DocumentProcessingJob.status == 'failed'
                )
            ).limit(limit).all()
            
            results = []
            for job in problematic_jobs:
                results.append({
                    'job_id': str(job.id),
                    'document_id': str(job.document_id),
                    'status': job.status,
                    'entities_extracted': job.entities_extracted or 0,
                    'retry_count': job.retry_count,
                    'error_message': job.error_message,
                    'created_at': job.created_at.isoformat()
                })
            
            logger.info(f"Found {len(results)} problematic documents")
            return results
        
        except Exception as e:
            logger.error(f"Identify problematic documents failed: {e}")
            raise
    
    async def get_trend_analysis(
        self,
        db: Session,
        metric_type: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Analyze metric trends over time.
        
        Args:
            db: Database session
            metric_type: Metric to analyze (accuracy, precision, recall, latency, cost)
            days: Number of days to analyze
        
        Returns:
            Trend analysis with daily values
        """
        since = datetime.utcnow() - timedelta(days=days)
        
        try:
            metrics = db.query(ProcessingQualityMetric).filter(
                ProcessingQualityMetric.metric_type == metric_type,
                ProcessingQualityMetric.calculated_at >= since
            ).order_by(ProcessingQualityMetric.calculated_at).all()
            
            # Group by day
            daily_values = defaultdict(list)
            for metric in metrics:
                day = metric.calculated_at.date().isoformat()
                daily_values[day].append(float(metric.value))
            
            # Calculate daily averages
            trend_data = []
            for day in sorted(daily_values.keys()):
                values = daily_values[day]
                trend_data.append({
                    'date': day,
                    'avg_value': round(sum(values) / len(values), 4),
                    'min_value': round(min(values), 4),
                    'max_value': round(max(values), 4),
                    'sample_count': len(values)
                })
            
            # Calculate overall trend (improving, stable, declining)
            trend_direction = 'stable'
            if len(trend_data) >= 2:
                first_avg = trend_data[0]['avg_value']
                last_avg = trend_data[-1]['avg_value']
                
                # For latency and cost, lower is better
                if metric_type in ['latency', 'cost']:
                    if last_avg < first_avg * 0.9:
                        trend_direction = 'improving'
                    elif last_avg > first_avg * 1.1:
                        trend_direction = 'declining'
                else:
                    # For accuracy/precision/recall, higher is better
                    if last_avg > first_avg * 1.05:
                        trend_direction = 'improving'
                    elif last_avg < first_avg * 0.95:
                        trend_direction = 'declining'
            
            return {
                'metric_type': metric_type,
                'days_analyzed': days,
                'trend_direction': trend_direction,
                'daily_data': trend_data
            }
        
        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            raise


# Helper function import for test
from sqlalchemy import or_


# Global quality monitor instance
quality_monitor = QualityMonitor()

