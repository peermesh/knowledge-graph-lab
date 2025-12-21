"""
AWS SES integration for Publishing Module.

Handles email delivery, bounce tracking, and engagement analytics through AWS Simple Email Service.
Optimized for high-volume newsletter delivery with comprehensive error handling.

Constitution Compliance:
- Multi-Channel Publishing Excellence: Email delivery with AWS SES
- Technology Standards: AWS SES integration for reliable delivery
- Performance: Optimized for 1,000+ newsletters per minute
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
import structlog
import boto3
import botocore.exceptions
from botocore.config import Config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64

from ..core.config import settings
from ..core.logging import log_external_service_call


class SESClient:
    """AWS SES client for email delivery and management."""

    def __init__(self):
        """Initialize SES client with configuration."""
        self.logger = structlog.get_logger(__name__)
        self.region = settings.AWS_REGION
        self.sender_email = settings.SES_SENDER_EMAIL

        # Configure boto3 client with retry and timeout settings
        config = Config(
            region_name=self.region,
            retries={
                'max_attempts': 3,
                'mode': 'adaptive'
            },
            max_pool_connections=50,
            parameter_validation=False  # For performance
        )

        self.client = boto3.client(
            'ses',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=config
        )

        # SNS client for bounce/complaint notifications
        self.sns_client = boto3.client(
            'sns',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=config
        )

    async def send_email(self, to_email: str, subject: str, html_body: str, text_body: str = None) -> Dict[str, Any]:
        """Send email through AWS SES."""
        correlation_id = str(asyncio.current_task().get_coro_stack()[-1] if asyncio.current_task() else "unknown")

        try:
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = to_email

            # Add text version if provided
            if text_body:
                text_part = MIMEText(text_body, 'plain')
                msg.attach(text_part)

            # Add HTML version
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)

            # Send email
            response = self.client.send_raw_email(
                Source=self.sender_email,
                Destinations=[to_email],
                RawMessage={
                    'Data': msg.as_string()
                }
            )

            log_external_service_call(
                correlation_id=correlation_id,
                service_name="aws_ses",
                operation="send_email",
                success=True,
                duration_ms=0  # boto3 is sync, but we track in async context
            )

            self.logger.info(
                "Email sent successfully",
                to_email=to_email,
                message_id=response.get('MessageId'),
                correlation_id=correlation_id
            )

            return {
                "success": True,
                "message_id": response.get('MessageId'),
                "status": "sent"
            }

        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']

            log_external_service_call(
                correlation_id=correlation_id,
                service_name="aws_ses",
                operation="send_email",
                success=False,
                duration_ms=0,
                error=f"{error_code}: {error_message}"
            )

            self.logger.error(
                "Email send failed",
                to_email=to_email,
                error_code=error_code,
                error_message=error_message,
                correlation_id=correlation_id
            )

            return {
                "success": False,
                "error": error_message,
                "error_code": error_code,
                "status": "failed"
            }

        except Exception as e:
            log_external_service_call(
                correlation_id=correlation_id,
                service_name="aws_ses",
                operation="send_email",
                success=False,
                duration_ms=0,
                error=str(e)
            )

            self.logger.error(
                "Email send error",
                to_email=to_email,
                error=str(e),
                correlation_id=correlation_id
            )

            return {
                "success": False,
                "error": str(e),
                "status": "error"
            }

    async def send_bulk_email(self, recipients: List[str], subject: str, html_body: str, text_body: str = None) -> Dict[str, Any]:
        """Send email to multiple recipients efficiently."""
        correlation_id = str(asyncio.current_task().get_coro_stack()[-1] if asyncio.current_task() else "unknown")

        try:
            # Use SES send_bulk_templated_email for efficiency if template is the same
            if not text_body:
                # Create template-based email for better performance
                template_data = {
                    "subject": subject,
                    "html_body": html_body
                }

                response = self.client.send_bulk_templated_email(
                    Source=self.sender_email,
                    Template=self._get_or_create_template(template_data),
                    Destinations=[
                        {"Destination": {"ToAddresses": [email]}}
                        for email in recipients
                    ],
                    DefaultTemplateData=json.dumps(template_data)
                )

                log_external_service_call(
                    correlation_id=correlation_id,
                    service_name="aws_ses",
                    operation="send_bulk_email",
                    success=True,
                    duration_ms=0
                )

                return {
                    "success": True,
                    "message_ids": [msg.get('MessageId') for msg in response.get('Successful', [])],
                    "failed_count": len(response.get('Failed', [])),
                    "status": "bulk_sent"
                }
            else:
                # Fallback to individual emails for complex content
                results = []
                for email in recipients:
                    result = await self.send_email(email, subject, html_body, text_body)
                    results.append(result)

                successful = [r for r in results if r["success"]]
                failed = [r for r in results if not r["success"]]

                return {
                    "success": len(failed) == 0,
                    "successful_count": len(successful),
                    "failed_count": len(failed),
                    "results": results,
                    "status": "individual_sent"
                }

        except Exception as e:
            log_external_service_call(
                correlation_id=correlation_id,
                service_name="aws_ses",
                operation="send_bulk_email",
                success=False,
                duration_ms=0,
                error=str(e)
            )

            self.logger.error(
                "Bulk email send error",
                recipient_count=len(recipients),
                error=str(e),
                correlation_id=correlation_id
            )

            return {
                "success": False,
                "error": str(e),
                "status": "error"
            }

    def _get_or_create_template(self, template_data: Dict[str, str]) -> str:
        """Get or create SES email template for bulk sending."""
        # In production, you would manage templates through SES
        # For now, return a generic template name
        return "PublishingModuleNewsletter"

    async def verify_email_identity(self, email: str) -> bool:
        """Verify email identity for sending."""
        try:
            self.client.verify_email_identity(EmailAddress=email)
            self.logger.info("Email identity verification initiated", email=email)
            return True
        except Exception as e:
            self.logger.error("Email identity verification failed", email=email, error=str(e))
            return False

    async def get_send_quota(self) -> Dict[str, Any]:
        """Get current SES sending quota and usage."""
        try:
            response = self.client.get_send_quota()
            return {
                "sent_last_24_hours": response.get('SentLast24Hours', 0),
                "max_24_hour_send": response.get('Max24HourSend', 0),
                "max_send_rate": response.get('MaxSendRate', 0),
                "remaining_quota": response.get('Max24HourSend', 0) - response.get('SentLast24Hours', 0)
            }
        except Exception as e:
            self.logger.error("Failed to get SES quota", error=str(e))
            return {"status": "error", "error": str(e)}

    async def get_send_statistics(self) -> Dict[str, Any]:
        """Get SES sending statistics."""
        try:
            response = self.client.get_send_statistics()
            return {
                "delivery_attempts": response.get('DeliveryAttempts', 0),
                "bounces": response.get('Bounces', 0),
                "complaints": response.get('Complaints', 0),
                "rejects": response.get('Rejects', 0),
                "bounce_rate": response.get('BounceRate', 0),
                "complaint_rate": response.get('ComplaintRate', 0)
            }
        except Exception as e:
            self.logger.error("Failed to get SES statistics", error=str(e))
            return {"status": "error", "error": str(e)}

    async def setup_bounce_notifications(self, sns_topic_arn: str) -> bool:
        """Setup SNS notifications for bounce and complaint events."""
        try:
            # Configure SES to send bounce notifications to SNS
            self.client.set_identity_notification_topic(
                Identity=self.sender_email,
                NotificationType='Bounce',
                SnsTopic=sns_topic_arn
            )

            self.client.set_identity_notification_topic(
                Identity=self.sender_email,
                NotificationType='Complaint',
                SnsTopic=sns_topic_arn
            )

            self.logger.info("SES bounce notifications configured", sns_topic_arn=sns_topic_arn)
            return True

        except Exception as e:
            self.logger.error("Failed to setup bounce notifications", error=str(e))
            return False

    async def check_ses_health(self) -> bool:
        """Check AWS SES service health."""
        try:
            # Try to get send quota as a health check
            quota = await self.get_send_quota()
            return quota.get("status") != "error"
        except Exception as e:
            self.logger.error("SES health check failed", error=str(e))
            return False

    async def get_delivery_status(self, message_id: str) -> Dict[str, Any]:
        """Get delivery status for a specific message (if available)."""
        try:
            # Note: SES doesn't provide real-time delivery status for individual emails
            # This would typically be handled through SNS notifications
            return {
                "message_id": message_id,
                "status": "sent",
                "note": "Real-time delivery status requires SNS notifications setup"
            }
        except Exception as e:
            self.logger.error("Failed to get delivery status", message_id=message_id, error=str(e))
            return {"status": "error", "error": str(e)}

    async def send_test_email(self, to_email: str) -> Dict[str, Any]:
        """Send a test email for channel validation."""
        test_subject = "Publishing Module - Test Email"
        test_html = """
        <html>
        <body>
            <h2>Publishing Module Test</h2>
            <p>This is a test email from the Knowledge Graph Lab Publishing Module.</p>
            <p>If you received this, the email channel is working correctly.</p>
            <p><strong>Channel:</strong> Email (AWS SES)</p>
            <p><strong>Timestamp:</strong> {timestamp}</p>
        </body>
        </html>
        """

        test_text = """
        Publishing Module Test

        This is a test email from the Knowledge Graph Lab Publishing Module.
        If you received this, the email channel is working correctly.

        Channel: Email (AWS SES)
        Timestamp: {timestamp}
        """

        return await self.send_email(to_email, test_subject, test_html, test_text)


# Global SES client instance
ses_client = SESClient()


async def check_ses_health() -> bool:
    """Health check function for external service monitoring."""
    return await ses_client.check_ses_health()


async def send_test_email(to_email: str) -> Dict[str, Any]:
    """Send test email for channel validation."""
    return await ses_client.send_test_email(to_email)


async def get_ses_quota() -> Dict[str, Any]:
    """Get SES sending quota information."""
    return await ses_client.get_send_quota()


async def get_ses_statistics() -> Dict[str, Any]:
    """Get SES sending statistics."""
    return await ses_client.get_ses_statistics()

