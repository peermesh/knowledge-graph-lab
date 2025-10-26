"""Alerting service for quality degradation and system issues"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)


class AlertLevel:
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertingService:
    """Service for managing alerts and notifications"""
    
    def __init__(self):
        """Initialize alerting service"""
        self.alert_handlers = []
        self.active_alerts: Dict[str, Dict[str, Any]] = {}
    
    async def send_alert(
        self,
        alert_type: str,
        severity: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send an alert notification.
        
        Args:
            alert_type: Type of alert (quality_degradation, system_error, cost_limit, etc.)
            severity: Alert severity (critical, high, medium, low, info)
            message: Alert message
            details: Additional alert context
        
        Returns:
            True if alert sent successfully
        """
        alert_id = f"{alert_type}_{datetime.utcnow().timestamp()}"
        
        alert = {
            'id': alert_id,
            'type': alert_type,
            'severity': severity,
            'message': message,
            'details': details or {},
            'timestamp': datetime.utcnow().isoformat(),
            'acknowledged': False
        }
        
        # Store active alert
        self.active_alerts[alert_id] = alert
        
        # Log alert
        log_method = self._get_log_method(severity)
        log_method(f"ALERT [{severity.upper()}] {alert_type}: {message}")
        
        # Send to all registered handlers
        for handler in self.alert_handlers:
            try:
                await handler(alert)
            except Exception as e:
                logger.error(f"Alert handler failed: {e}")
        
        return True
    
    def _get_log_method(self, severity: str):
        """Get appropriate logging method for severity"""
        if severity in [AlertLevel.CRITICAL, AlertLevel.HIGH]:
            return logger.error
        elif severity == AlertLevel.MEDIUM:
            return logger.warning
        else:
            return logger.info
    
    async def alert_quality_degradation(
        self,
        entity_type: str,
        metric: str,
        current_value: float,
        threshold: float
    ):
        """
        Send alert for quality degradation.
        
        Args:
            entity_type: Entity type affected
            metric: Metric that degraded (accuracy, precision, recall)
            current_value: Current metric value
            threshold: Threshold that was violated
        """
        # Determine severity based on how far below threshold
        severity = AlertLevel.HIGH
        if current_value < threshold * 0.8:
            severity = AlertLevel.CRITICAL
        elif current_value < threshold * 0.9:
            severity = AlertLevel.HIGH
        else:
            severity = AlertLevel.MEDIUM
        
        message = (
            f"Quality degradation detected for {entity_type}: "
            f"{metric} = {current_value:.2%} (threshold: {threshold:.2%})"
        )
        
        await self.send_alert(
            alert_type="quality_degradation",
            severity=severity,
            message=message,
            details={
                'entity_type': entity_type,
                'metric': metric,
                'current_value': current_value,
                'threshold': threshold,
                'degradation_percent': ((threshold - current_value) / threshold) * 100
            }
        )
    
    async def alert_cost_limit(
        self,
        current_cost: float,
        daily_limit: float,
        remaining_budget: float
    ):
        """
        Send alert when approaching or exceeding cost limit.
        
        Args:
            current_cost: Current daily cost
            daily_limit: Daily cost limit
            remaining_budget: Remaining budget
        """
        utilization = current_cost / daily_limit
        
        if utilization >= 1.0:
            severity = AlertLevel.CRITICAL
            message = f"Daily cost limit EXCEEDED: ${current_cost:.2f} / ${daily_limit:.2f}"
        elif utilization >= 0.9:
            severity = AlertLevel.HIGH
            message = f"Daily cost limit 90% reached: ${current_cost:.2f} / ${daily_limit:.2f}"
        elif utilization >= 0.8:
            severity = AlertLevel.MEDIUM
            message = f"Daily cost limit 80% reached: ${current_cost:.2f} / ${daily_limit:.2f}"
        else:
            return  # No alert needed
        
        await self.send_alert(
            alert_type="cost_limit",
            severity=severity,
            message=message,
            details={
                'current_cost': current_cost,
                'daily_limit': daily_limit,
                'remaining_budget': remaining_budget,
                'utilization_percent': utilization * 100
            }
        )
    
    async def alert_processing_failure(
        self,
        job_id: str,
        document_id: str,
        error_message: str,
        retry_count: int
    ):
        """
        Send alert for job processing failure.
        
        Args:
            job_id: Job identifier
            document_id: Document identifier
            error_message: Error details
            retry_count: Number of retries attempted
        """
        # Determine severity based on retry count
        if retry_count >= 3:
            severity = AlertLevel.HIGH  # Max retries exceeded
        elif retry_count >= 2:
            severity = AlertLevel.MEDIUM
        else:
            severity = AlertLevel.LOW
        
        message = f"Job {job_id} failed after {retry_count + 1} attempts: {error_message[:100]}"
        
        await self.send_alert(
            alert_type="processing_failure",
            severity=severity,
            message=message,
            details={
                'job_id': job_id,
                'document_id': document_id,
                'error_message': error_message,
                'retry_count': retry_count
            }
        )
    
    async def alert_queue_backlog(
        self,
        queue_name: str,
        message_count: int,
        threshold: int = 1000
    ):
        """
        Send alert when queue backlog exceeds threshold.
        
        Args:
            queue_name: Queue name
            message_count: Number of pending messages
            threshold: Alert threshold
        """
        if message_count < threshold:
            return
        
        severity = AlertLevel.CRITICAL if message_count > threshold * 2 else AlertLevel.HIGH
        
        message = f"Queue backlog alert: {queue_name} has {message_count} pending messages"
        
        await self.send_alert(
            alert_type="queue_backlog",
            severity=severity,
            message=message,
            details={
                'queue_name': queue_name,
                'message_count': message_count,
                'threshold': threshold
            }
        )
    
    def register_handler(self, handler_func):
        """
        Register a custom alert handler.
        
        Handler should be async function accepting alert dict.
        
        Args:
            handler_func: Async function(alert: Dict) -> None
        """
        self.alert_handlers.append(handler_func)
        logger.info(f"Registered alert handler: {handler_func.__name__}")
    
    def get_active_alerts(
        self,
        severity: Optional[str] = None,
        alert_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get list of active alerts.
        
        Args:
            severity: Filter by severity
            alert_type: Filter by alert type
        
        Returns:
            List of active alerts
        """
        alerts = list(self.active_alerts.values())
        
        # Filter by severity
        if severity:
            alerts = [a for a in alerts if a['severity'] == severity]
        
        # Filter by type
        if alert_type:
            alerts = [a for a in alerts if a['type'] == alert_type]
        
        # Filter unacknowledged
        alerts = [a for a in alerts if not a['acknowledged']]
        
        return alerts
    
    async def acknowledge_alert(self, alert_id: str) -> bool:
        """
        Acknowledge an alert.
        
        Args:
            alert_id: Alert identifier
        
        Returns:
            True if acknowledged
        """
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id]['acknowledged'] = True
            self.active_alerts[alert_id]['acknowledged_at'] = datetime.utcnow().isoformat()
            logger.info(f"Alert {alert_id} acknowledged")
            return True
        
        return False
    
    async def clear_old_alerts(self, hours: int = 24):
        """
        Clear acknowledged alerts older than specified hours.
        
        Args:
            hours: Age threshold in hours
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        to_remove = []
        for alert_id, alert in self.active_alerts.items():
            if alert['acknowledged']:
                alert_time = datetime.fromisoformat(alert['timestamp'])
                if alert_time < cutoff:
                    to_remove.append(alert_id)
        
        for alert_id in to_remove:
            del self.active_alerts[alert_id]
        
        if to_remove:
            logger.info(f"Cleared {len(to_remove)} old alerts")


# Example alert handlers

async def log_alert_handler(alert: Dict[str, Any]):
    """Example handler that logs alerts"""
    logger.info(f"Alert Handler: {alert['severity']} - {alert['message']}")


async def email_alert_handler(alert: Dict[str, Any]):
    """Example handler that sends email alerts"""
    # In production, integrate with email service (AWS SES, SendGrid, etc.)
    if alert['severity'] in [AlertLevel.CRITICAL, AlertLevel.HIGH]:
        logger.info(f"Would send email for: {alert['message']}")
        # await send_email(
        #     to='ops-team@example.com',
        #     subject=f"[{alert['severity'].upper()}] {alert['type']}",
        #     body=alert['message']
        # )


async def slack_alert_handler(alert: Dict[str, Any]):
    """Example handler that sends Slack notifications"""
    # In production, integrate with Slack API
    if alert['severity'] in [AlertLevel.CRITICAL, AlertLevel.HIGH]:
        logger.info(f"Would send Slack notification for: {alert['message']}")
        # await send_slack_message(
        #     channel='#ai-alerts',
        #     message=f"🚨 {alert['severity'].upper()}: {alert['message']}"
        # )


# Import timedelta
from datetime import timedelta


# Global alerting service instance
alerting_service = AlertingService()

# Register default handlers
alerting_service.register_handler(log_alert_handler)
# alerting_service.register_handler(email_alert_handler)  # Enable in production
# alerting_service.register_handler(slack_alert_handler)   # Enable in production

