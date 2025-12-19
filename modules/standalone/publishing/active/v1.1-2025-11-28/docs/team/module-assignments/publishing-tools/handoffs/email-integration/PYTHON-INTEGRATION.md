# Python AWS SES Email Integration Guide

Complete guide for using the existing Python email service in the Knowledge Graph Lab Publishing Module.

## Overview

The Publishing Module has **two email service implementations**:

1. **`src/publishing/integrations/email_service.py`** - Simple, production-ready service with placeholder mode
2. **`src/publishing/integrations/aws_ses.py`** - Advanced service with templates, SNS notifications, and statistics

Both services are built on `boto3` (AWS SDK for Python) and support AWS SES.

## Quick Start

### Prerequisites

- Python 3.11+
- AWS SES account configured (see [README.md](./README.md))
- Domain verified with SPF, DKIM, DMARC (see [dns-configuration.md](./dns-configuration.md))

### 1. Configure Credentials

Create a `.env` file in the project root:

```bash
# Copy the example
cp .env.example .env

# Edit with your credentials
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-2
SES_SENDER_EMAIL=noreply@distributedcreatives.org
TEST_EMAIL=your-email@example.com
```

**Security**: The `.env` file is **automatically ignored** by git (`.gitignore` line 6).

### 2. Test the Integration

#### Option A: Run the Test Script

```bash
# From project root
python scripts/send_test_email.py
```

**What it does**:
- Validates AWS credentials
- Sends a test email with HTML and text versions
- Provides clear success/failure messages
- Includes SPF/DKIM/DMARC verification instructions

#### Option B: Use the API Endpoint

```bash
# Start the API (in Docker)
docker-compose up api

# Or without Docker (requires .env file)
python -m uvicorn src.publishing.main:app --reload
```

Then visit: **http://localhost:8080/api/v1/docs**

Find the `POST /api/v1/email/test` endpoint and try it:

```json
{
  "to_email": "test@example.com",
  "subject": "Test Email",
  "custom_message": "Testing the email integration!"
}
```

### 3. Verify Email Authentication

When you receive the test email:

1. Open the email
2. View email headers (Gmail: three dots → "Show original")
3. Look for:
   - `spf=pass`
   - `dkim=pass`
   - `dmarc=pass`

All three should show **PASS** for proper email authentication.

## Code Examples

### Basic Email Sending

```python
from src.publishing.integrations.email_service import email_service

async def send_welcome_email(user_email: str, user_name: str):
    """Send a welcome email to a new subscriber."""
    
    html_body = f"""
    <html>
    <body>
        <h2>Welcome, {user_name}!</h2>
        <p>Thank you for subscribing to our newsletter.</p>
    </body>
    </html>
    """
    
    text_body = f"""
    Welcome, {user_name}!
    
    Thank you for subscribing to our newsletter.
    """
    
    result = await email_service.send_email(
        to_addresses=[user_email],
        subject="Welcome to Our Newsletter!",
        body_html=html_body,
        body_text=text_body
    )
    
    if result['status'] == 'sent':
        print(f"Email sent! Message ID: {result['message_id']}")
    else:
        print(f"Email failed: {result.get('error')}")
```

### Bulk Email Sending

```python
async def send_newsletter(subscribers: list, content: str):
    """Send a newsletter to multiple subscribers."""
    
    emails = [sub['email'] for sub in subscribers]
    
    result = await email_service.send_bulk_email(
        to_addresses=emails,
        subject="Monthly Newsletter",
        body_html=content,
        body_text="See HTML version"
    )
    
    print(f"Sent to {result['successful']} recipients")
    print(f"Failed: {result['failed']}")
```

### Using the Advanced Service (aws_ses.py)

```python
from src.publishing.integrations.aws_ses import ses_client

async def send_with_tracking(user_email: str):
    """Send email with delivery tracking."""
    
    result = await ses_client.send_email(
        to_email=user_email,
        subject="Your Report",
        html_body="<h1>Monthly Report</h1>",
        text_body="Monthly Report"
    )
    
    if result['success']:
        message_id = result['message_id']
        # Track this message_id for delivery status
        print(f"Sent: {message_id}")
```

### Check SES Quota and Statistics

```python
from src.publishing.integrations.aws_ses import ses_client

async def check_email_limits():
    """Check current SES sending quota."""
    
    quota = await ses_client.get_send_quota()
    
    print(f"Sent today: {quota['sent_last_24_hours']}")
    print(f"Daily limit: {quota['max_24_hour_send']}")
    print(f"Remaining: {quota['remaining_quota']}")
    print(f"Send rate: {quota['max_send_rate']} emails/second")
    
    # Get statistics
    stats = await ses_client.get_send_statistics()
    print(f"Bounce rate: {stats['bounce_rate']}%")
    print(f"Complaint rate: {stats['complaint_rate']}%")
```

## Placeholder Mode (Development Without Credentials)

Both email services support **placeholder mode** for development:

- Runs without AWS credentials
- Logs email details to console
- Returns simulated success responses
- Perfect for testing without AWS account

**How it works**:

```python
# The service automatically detects placeholder credentials
if settings.AWS_ACCESS_KEY_ID == "placeholder":
    # Simulates email sending
    # Logs to console instead
```

**Example output in placeholder mode**:

```
📧 PLACEHOLDER EMAIL (not actually sent)
  to: ['user@example.com']
  subject: "Welcome!"
  body_preview: "<html><body>Welcome...</body></html>"
```

## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AWS_ACCESS_KEY_ID` | Yes | - | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | Yes | - | AWS IAM secret key |
| `AWS_REGION` | Yes | `us-east-1` | AWS region for SES |
| `SES_SENDER_EMAIL` | Yes | - | Verified sender email |
| `TEST_EMAIL` | No | - | Email for testing |

### Config in code

```python
from src.publishing.core.config import settings

# Access configuration
print(settings.AWS_REGION)
print(settings.SES_SENDER_EMAIL)
```

## Error Handling

### Common Errors and Solutions

#### 1. MessageRejected - Email Not Verified

```python
# Error: "Email address is not verified"
# Solution: Verify the recipient in SES sandbox mode

# AWS CLI:
aws ses verify-email-identity \
  --email-address user@example.com \
  --region us-east-2
```

#### 2. Throttling - Rate Limit Exceeded

```python
# Error: "Throttling: Maximum sending rate exceeded"
# Solution: Add delay between emails or request production access

import asyncio

for email in emails:
    await email_service.send_email([email], subject, body)
    await asyncio.sleep(1)  # 1 second delay (sandbox limit)
```

#### 3. Invalid Credentials

```python
# Error: "The security token included in the request is invalid"
# Solution: Check .env file has correct AWS credentials

# Verify credentials:
import boto3
client = boto3.client('sts')
identity = client.get_caller_identity()
print(f"AWS Account: {identity['Account']}")
```

### Error Handling Pattern

```python
async def safe_send_email(to_email: str):
    """Send email with proper error handling."""
    try:
        result = await email_service.send_email(
            to_addresses=[to_email],
            subject="Test",
            body_html="<p>Test</p>"
        )
        
        if result['status'] == 'sent':
            return True
        else:
            logger.error("Email failed", error=result.get('error'))
            return False
            
    except Exception as e:
        logger.error("Email exception", error=str(e))
        return False
```

## Docker Integration

The email service works seamlessly in Docker:

### docker-compose.yml

Already configured with env var passthrough:

```yaml
services:
  api:
    env_file:
      - .env
    environment:
      - AWS_REGION=${AWS_REGION:-us-east-1}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-placeholder}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-placeholder}
```

### Running in Docker

```bash
# Start services
docker-compose up --build

# Test email via API
curl -X POST http://localhost:8080/api/v1/email/test \
  -H "Content-Type: application/json" \
  -d '{"to_email": "test@example.com"}'

# Check logs
docker-compose logs -f api
```

## Testing Checklist

Before deploying to production:

- [ ] Test script runs successfully: `python scripts/send_test_email.py`
- [ ] API endpoint works: `POST /api/v1/email/test`
- [ ] Email received in inbox (not spam)
- [ ] SPF passes (check headers)
- [ ] DKIM passes (check headers)
- [ ] DMARC passes (check headers)
- [ ] Bulk sending works without throttling errors
- [ ] Error handling works (test with invalid email)
- [ ] Placeholder mode works without credentials

## Performance Optimization

### For High-Volume Sending

```python
from src.publishing.integrations.aws_ses import ses_client

# Use bulk sending for better performance
async def send_newsletter_optimized(recipients: list, content: str):
    """Send to many recipients efficiently."""
    
    # Split into batches of 50 (SES limit)
    batch_size = 50
    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i + batch_size]
        
        result = await ses_client.send_bulk_email(
            recipients=batch,
            subject="Newsletter",
            html_body=content
        )
        
        # Track results
        print(f"Batch {i//batch_size + 1}: {result['successful_count']} sent")
```

### Request Production Access

For >200 emails/day and removing sandbox restrictions:

1. Go to AWS SES Console → Account Dashboard
2. Click "Request production access"
3. Fill out use case form
4. Wait 24-48 hours for approval

## Comparison: email_service.py vs aws_ses.py

| Feature | email_service.py | aws_ses.py |
|---------|-----------------|------------|
| **Purpose** | Simple, fast, production-ready | Advanced features, statistics |
| **Placeholder Mode** | ✅ Yes | ❌ No |
| **Async Support** | ✅ Yes | ✅ Yes |
| **HTML/Text Email** | ✅ Yes | ✅ Yes |
| **Bulk Sending** | ✅ Yes (individual) | ✅ Yes (optimized) |
| **Templates** | ❌ No | ✅ Yes |
| **Statistics** | ❌ No | ✅ Yes |
| **SNS Integration** | ❌ No | ✅ Yes |
| **Bounce Tracking** | ❌ No | ✅ Yes |

**Recommendation**: Use `email_service.py` for most cases. Use `aws_ses.py` if you need templates, statistics, or bounce tracking.

## Troubleshooting

### Email Goes to Spam

**Check authentication**:
```bash
# Test with mail-tester.com
# Send email to their test address and check score
```

**Common fixes**:
- Ensure SPF, DKIM, DMARC all pass
- Always include plain text version
- Avoid spam trigger words (FREE, URGENT, etc.)
- Add unsubscribe link for marketing emails

### Can't Send to External Emails

**Issue**: SES is in sandbox mode

**Solution**:
```bash
# Verify individual recipients (sandbox mode only)
aws ses verify-email-identity \
  --email-address recipient@example.com \
  --region us-east-2

# Or request production access (see above)
```

### Rate Limit Errors

**Issue**: Throttling: Maximum sending rate exceeded

**Solution**:
- Sandbox: 1 email/second limit
- Production: Higher limits (check quota)
- Add delays between sends
- Use bulk sending methods

## Resources

- [Main Email Integration Guide](./README.md)
- [DNS Configuration](./dns-configuration.md)
- [Troubleshooting Guide](./troubleshooting.md)
- [Production Checklist](./production-checklist.md)
- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)
- [boto3 SES Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html)

## Next Steps

1. **Configure credentials**: Create `.env` file with AWS credentials
2. **Run test**: `python scripts/send_test_email.py`
3. **Verify delivery**: Check email headers for SPF/DKIM/DMARC
4. **Integrate into app**: Use code examples above
5. **Monitor**: Set up CloudWatch alarms for bounce/complaint rates
6. **Scale**: Request production access when ready

---

**Questions?** See [troubleshooting.md](./troubleshooting.md) or contact your project admin.

