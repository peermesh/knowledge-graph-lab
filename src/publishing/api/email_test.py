"""
Email Test API Endpoints

Provides endpoints for testing email functionality via the API.
Useful for validating AWS SES configuration and email delivery.

Constitution Compliance:
- Multi-Channel Publishing Excellence: Email testing and validation
- API Standards: RESTful endpoints with comprehensive documentation
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import structlog

from ..integrations.email_service import email_service


logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/email", tags=["Email Testing"])


class EmailTestRequest(BaseModel):
    """Request model for test email."""
    to_email: EmailStr = Field(..., description="Recipient email address")
    subject: Optional[str] = Field("Test Email from Publishing Module", description="Email subject line")
    custom_message: Optional[str] = Field(None, description="Optional custom message to include in email")


class EmailTestResponse(BaseModel):
    """Response model for test email."""
    status: str = Field(..., description="Email send status (sent, simulated, failed)")
    message: str = Field(..., description="Human-readable status message")
    message_id: Optional[str] = Field(None, description="AWS SES Message ID (if sent)")
    provider: Optional[str] = Field(None, description="Email provider used")
    timestamp: Optional[str] = Field(None, description="Send timestamp")
    note: Optional[str] = Field(None, description="Additional notes or instructions")
    error: Optional[str] = Field(None, description="Error message if failed")


@router.post("/test", response_model=EmailTestResponse, summary="Send Test Email")
async def send_test_email(request: EmailTestRequest):
    """
    Send a test email to verify AWS SES configuration.
    
    This endpoint allows you to test email delivery without using the full
    publication/newsletter system. Useful for:
    
    - Validating AWS SES credentials
    - Testing domain verification
    - Checking SPF/DKIM/DMARC configuration
    - Verifying email delivery in sandbox mode
    
    **In Placeholder Mode** (no real AWS credentials):
    - Returns status "simulated"
    - Logs email details but doesn't actually send
    
    **With Real Credentials**:
    - Sends actual email via AWS SES
    - Returns AWS Message ID for tracking
    - Check email headers to verify SPF/DKIM/DMARC pass
    
    **Example Request**:
    ```json
    {
      "to_email": "test@example.com",
      "subject": "Custom Test Subject",
      "custom_message": "Testing the email integration!"
    }
    ```
    """
    try:
        logger.info("Test email requested", to_email=request.to_email)
        
        # Prepare email content
        custom_msg = request.custom_message or "This is a test email from the Publishing Module."
        
        html_body = f"""<!DOCTYPE html>
<html>
<head>
  <style>
    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
    .header {{ background: #007bff; color: white; padding: 20px; text-align: center; }}
    .content {{ padding: 20px; background: #f9f9f9; }}
    .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📧 Test Email</h1>
    </div>
    <div class="content">
      <p>{custom_msg}</p>
      <p>If you received this email, the Publishing Module's email integration is working correctly!</p>
      <h3>What to check:</h3>
      <ol>
        <li>Email arrived in inbox (not spam)</li>
        <li>From address is correct</li>
        <li>View email headers and verify:<br>
            - <strong>SPF:</strong> PASS<br>
            - <strong>DKIM:</strong> PASS<br>
            - <strong>DMARC:</strong> PASS
        </li>
      </ol>
    </div>
    <div class="footer">
      <p>Knowledge Graph Lab Publishing Module • Powered by AWS SES</p>
    </div>
  </div>
</body>
</html>"""
        
        text_body = f"""{custom_msg}

If you received this email, the Publishing Module's email integration is working correctly!

What to check:
1. Email arrived in inbox (not spam)
2. From address is correct
3. View email headers and verify:
   - SPF: PASS
   - DKIM: PASS
   - DMARC: PASS

---
Knowledge Graph Lab Publishing Module • Powered by AWS SES
"""
        
        # Send the email
        result = await email_service.send_email(
            to_addresses=[request.to_email],
            subject=request.subject,
            body_html=html_body,
            body_text=text_body
        )
        
        # Format response based on result
        if result.get('status') == 'sent':
            return EmailTestResponse(
                status="sent",
                message=f"Test email sent successfully to {request.to_email}",
                message_id=result.get('message_id'),
                provider=result.get('provider'),
                timestamp=result.get('timestamp'),
                note="Check the recipient's inbox and verify email headers for SPF/DKIM/DMARC."
            )
        elif result.get('status') == 'simulated':
            return EmailTestResponse(
                status="simulated",
                message="Email simulated (not actually sent) - running in placeholder mode",
                message_id=result.get('message_id'),
                provider=result.get('provider'),
                timestamp=result.get('timestamp'),
                note=result.get('note', 'Configure AWS SES credentials in .env to send real emails')
            )
        else:
            # Failed
            error_msg = result.get('error', 'Unknown error')
            logger.error("Test email failed", error=error_msg, to_email=request.to_email)
            return EmailTestResponse(
                status="failed",
                message=f"Failed to send test email: {error_msg}",
                error=error_msg,
                note="Check AWS credentials, domain verification, and sandbox mode restrictions. See /docs for troubleshooting."
            )
            
    except Exception as e:
        logger.error("Test email error", error=str(e), to_email=request.to_email)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send test email: {str(e)}"
        )


@router.get("/status", summary="Check Email Service Status")
async def email_service_status():
    """
    Check the status of the email service.
    
    Returns information about:
    - Whether running in placeholder mode or with real credentials
    - Configured sender email
    - AWS region (if configured)
    
    **Response**:
    ```json
    {
      "service": "email",
      "mode": "placeholder" or "aws_ses",
      "sender_email": "noreply@example.com",
      "region": "us-east-2",
      "ready": true
    }
    ```
    """
    try:
        from ..core.config import settings
        
        return success_response(
            data={
                "service": "email",
                "mode": "placeholder" if email_service.is_placeholder else "aws_ses",
                "sender_email": email_service.sender_email,
                "region": settings.AWS_REGION if not email_service.is_placeholder else None,
                "ready": True,
                "note": "Use POST /email/test to send a test email" if not email_service.is_placeholder 
                        else "Running in placeholder mode. Configure AWS credentials to send real emails."
            }
        )
    except Exception as e:
        logger.error("Email status check failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check email service status: {str(e)}"
        )

