#!/usr/bin/env python3
"""
AWS SES Email Test Script

Python equivalent of the Node.js send-test-email.js from the handoff guide.
Tests the existing EmailService implementation with real AWS credentials.

Usage:
    python scripts/send_test_email.py

Requirements:
    - .env file with AWS credentials (copy from .env.example)
    - boto3 installed (pip install boto3)
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import email service
from src.publishing.integrations.email_service import EmailService


def validate_environment():
    """Validate required environment variables."""
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print('❌ Missing required environment variables:', ', '.join(missing))
        print('\nMake sure you have a .env file with:')
        print('AWS_ACCESS_KEY_ID=your_key')
        print('AWS_SECRET_ACCESS_KEY=your_secret')
        print('AWS_REGION=us-east-2')
        print('TEST_EMAIL=your_email@example.com')
        return False
    
    return True


async def send_test_email():
    """Send a test email using the EmailService."""
    
    # Get configuration
    test_email = os.getenv('TEST_EMAIL', 'test@example.com')
    from_email = os.getenv('SES_SENDER_EMAIL', 'noreply@distributedcreatives.org')
    aws_region = os.getenv('AWS_REGION', 'us-east-2')
    
    print('📧 AWS SES Email Test\n')
    print('Configuration:')
    print(f'  Region: {aws_region}')
    print(f'  From: {from_email}')
    print(f'  To: {test_email}')
    print('\nSending test email...\n')
    
    # Initialize email service
    email_service = EmailService()
    
    # Prepare email content
    timestamp = datetime.utcnow().isoformat()
    
    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <style>
    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
    .header {{ background: #007bff; color: white; padding: 20px; text-align: center; }}
    .content {{ padding: 20px; background: #f9f9f9; }}
    .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
    .success {{ color: #28a745; font-size: 24px; }}
    code {{ background: #e9ecef; padding: 2px 6px; border-radius: 3px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 class="success">✅ SES Integration Test</h1>
    </div>
    <div class="content">
      <p>If you're reading this, the <strong>AWS SES integration is working correctly</strong>!</p>

      <h3>Configuration:</h3>
      <ul>
        <li><strong>Region:</strong> {aws_region}</li>
        <li><strong>From:</strong> {from_email}</li>
        <li><strong>To:</strong> {test_email}</li>
        <li><strong>Timestamp:</strong> {timestamp}</li>
      </ul>

      <h3>Next Steps:</h3>
      <ol>
        <li>Check that SPF, DKIM, DMARC all pass (view email headers)</li>
        <li>Review the code in <code>scripts/send_test_email.py</code></li>
        <li>Review the EmailService in <code>src/publishing/integrations/email_service.py</code></li>
        <li>Use the API endpoint at <code>POST /api/v1/email/test</code> for testing</li>
      </ol>

      <p><strong>The email integration is ready to use!</strong></p>
    </div>
    <div class="footer">
      <p>Sent via Amazon SES • Knowledge Graph Lab Publishing Module</p>
    </div>
  </div>
</body>
</html>"""
    
    text_body = f"""SES Integration Test - Success!

If you're reading this, the AWS SES integration is working correctly!

Configuration:
- Region: {aws_region}
- From: {from_email}
- To: {test_email}
- Timestamp: {timestamp}

Next steps:
1. Check that SPF, DKIM, DMARC all pass (view email headers)
2. Review the code in scripts/send_test_email.py
3. Review the EmailService in src/publishing/integrations/email_service.py
4. Use the API endpoint at POST /api/v1/email/test for testing

The email integration is ready to use!

---
Sent via Amazon SES • Knowledge Graph Lab Publishing Module
"""
    
    # Send the email
    try:
        result = await email_service.send_email(
            to_addresses=[test_email],
            subject='✅ SES Integration Test - Success!',
            body_html=html_body,
            body_text=text_body
        )
        
        if result.get('status') in ('sent', 'simulated'):
            print('✅ SUCCESS! Email sent successfully!\n')
            
            if result.get('status') == 'sent':
                print(f"Message ID: {result.get('message_id')}")
                print(f'Provider: {result.get("provider")}')
                print(f'\nCheck your inbox at: {test_email}')
                print('\nTo verify authentication:')
                print('  1. Open the email')
                print('  2. View email headers (Gmail: three dots → Show original)')
                print('  3. Look for: spf=pass, dkim=pass, dmarc=pass')
            else:
                print('📧 PLACEHOLDER MODE - Email simulated (not actually sent)')
                print(f"Message ID: {result.get('message_id')}")
                print('\nTo send real emails:')
                print('  1. Get AWS credentials from project admin')
                print('  2. Update .env file with real credentials')
                print('  3. Run this script again')
            
            print('\n🎉 Integration test complete!\n')
            return True
            
        else:
            print('❌ FAILED to send email\n')
            print(f"Error: {result.get('error', 'Unknown error')}")
            print(f"Error Code: {result.get('error_code', 'N/A')}")
            
            error_message = result.get('error', '').lower()
            
            if 'not verified' in error_message:
                print('\nCommon issue: Domain/email verification pending')
                print('  → Wait 15 min - 2 hours for DNS propagation')
                print('  → Or verify recipient email in sandbox mode:')
                print(f'     aws ses verify-email-identity --email-address {test_email} --region {aws_region}')
            
            if 'throttling' in error_message:
                print('\nCommon issue: Rate limit exceeded')
                print('  → Sandbox mode: 1 email/second limit')
                print('  → Wait a moment and try again')
            
            if 'credentials' in error_message or 'access' in error_message:
                print('\nCommon issue: Invalid AWS credentials')
                print('  → Check AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env')
                print('  → Verify IAM user has ses:SendEmail permission')
            
            print('\nSee docs/team/module-assignments/publishing-tools/handoffs/email-integration/troubleshooting.md')
            print('for more help\n')
            return False
            
    except Exception as e:
        print(f'❌ ERROR: {str(e)}\n')
        print('Check your .env file and AWS credentials\n')
        return False


def main():
    """Main entry point."""
    print('='*60)
    print('AWS SES Email Integration Test')
    print('='*60)
    print()
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Run async test
    success = asyncio.run(send_test_email())
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

