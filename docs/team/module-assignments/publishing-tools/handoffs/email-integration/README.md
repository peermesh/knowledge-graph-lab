# AWS SES Email Integration Guide

Complete guide for integrating Amazon SES (Simple Email Service) for transactional email sending.

## Overview

This guide covers:
- AWS SES setup and configuration
- DNS records (SPF, DKIM, DMARC)
- Code examples for multiple languages
- Docker integration
- Testing and troubleshooting

## Prerequisites

- AWS account with SES access
- Domain with DNS management access
- Docker (for containerized deployment)

## Quick Start

### 1. AWS SES Setup

1. **Create IAM User**:
   - Go to IAM Console → Users → Create user
   - Grant `AmazonSESFullAccess` policy (or custom policy with `ses:SendEmail`)
   - Create access key for programmatic access

2. **Verify Domain Identity**:
   - Go to SES Console → Verified identities
   - Add domain (e.g., `example.com`)
   - Copy verification TXT record to DNS
   - Enable DKIM (Easy DKIM with 2048-bit key)

3. **Configure DNS**:
   - Add SES verification TXT record
   - Add 3 DKIM CNAME records (provided by SES)
   - Update SPF record to include SES
   - Ensure DMARC is configured

### 2. Environment Setup

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your AWS credentials
```

### 3. Install SDK

**Node.js**:
```bash
npm install @aws-sdk/client-ses
```

**Python**:
```bash
pip install boto3
```

**Go**:
```bash
go get github.com/aws/aws-sdk-go/service/ses
```

## DNS Configuration

### Required DNS Records

#### 1. Domain Verification TXT
```
Name: _amazonses.example.com
Type: TXT
Value: <verification-token-from-ses>
```

#### 2. DKIM CNAME Records (3 required)
```
Name: <token1>._domainkey.example.com
Type: CNAME
Value: <token1>.dkim.amazonses.com

Name: <token2>._domainkey.example.com
Type: CNAME
Value: <token2>.dkim.amazonses.com

Name: <token3>._domainkey.example.com
Type: CNAME
Value: <token3>.dkim.amazonses.com
```

#### 3. SPF Record
Update existing SPF or create new:
```
Name: example.com
Type: TXT
Value: "v=spf1 include:amazonses.com ~all"
```

If you already have SPF (e.g., for Google Workspace):
```
Before: "v=spf1 include:_spf.google.com -all"
After:  "v=spf1 include:_spf.google.com include:amazonses.com -all"
```

#### 4. DMARC (Recommended)
```
Name: _dmarc.example.com
Type: TXT
Value: "v=DMARC1; p=none; rua=mailto:admin@example.com"
```

## Code Examples

### Node.js (AWS SDK v3)

```javascript
import { SESClient, SendEmailCommand } from "@aws-sdk/client-ses";

const sesClient = new SESClient({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

async function sendEmail(to, subject, body) {
  const params = {
    Source: process.env.SES_FROM_EMAIL,
    Destination: { ToAddresses: [to] },
    Message: {
      Subject: { Data: subject, Charset: "UTF-8" },
      Body: {
        Text: { Data: body, Charset: "UTF-8" },
      },
    },
  };

  const command = new SendEmailCommand(params);
  return await sesClient.send(command);
}
```

### Python (Boto3)

```python
import boto3
import os

def send_email(to_address, subject, body_text):
    ses_client = boto3.client(
        'ses',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    response = ses_client.send_email(
        Source=os.environ.get('SES_FROM_EMAIL'),
        Destination={'ToAddresses': [to_address]},
        Message={
            'Subject': {'Data': subject, 'Charset': 'UTF-8'},
            'Body': {'Text': {'Data': body_text, 'Charset': 'UTF-8'}}
        }
    )
    return response['MessageId']
```

### Go

```go
package main

import (
    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/ses"
    "os"
)

func sendEmail(to, subject, body string) error {
    sess := session.Must(session.NewSession())
    svc := ses.New(sess, &aws.Config{Region: aws.String(os.Getenv("AWS_REGION"))})

    input := &ses.SendEmailInput{
        Source: aws.String(os.Getenv("SES_FROM_EMAIL")),
        Destination: &ses.Destination{
            ToAddresses: []*string{aws.String(to)},
        },
        Message: &ses.Message{
            Subject: &ses.Content{Data: aws.String(subject)},
            Body: &ses.Body{
                Text: &ses.Content{Data: aws.String(body)},
            },
        },
    }

    _, err := svc.SendEmail(input)
    return err
}
```

## Docker Integration

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    env_file:
      - .env
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_REGION=${AWS_REGION}
      - SES_FROM_EMAIL=${SES_FROM_EMAIL}
    ports:
      - "3000:3000"
```

### .env.example

```bash
# AWS SES Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1

# Email Settings
SES_FROM_EMAIL=noreply@example.com
SES_FROM_NAME=Your App Name
```

## Testing

### Sandbox Mode

By default, SES starts in sandbox mode with limitations:
- Can only send TO verified email addresses
- Limited to 200 emails/day, 1 email/second
- Can send FROM verified domains/addresses

### Verify Test Email

```bash
aws ses verify-email-identity \
  --email-address test@example.com \
  --region us-east-1
```

### Check Domain Verification

```bash
aws ses get-identity-verification-attributes \
  --identities example.com \
  --region us-east-1
```

### Request Production Access

To remove sandbox limitations:
1. SES Console → Account dashboard → "Request production access"
2. Fill out use case form
3. Wait for approval (usually 24-48 hours)

## Troubleshooting

### Domain Verification Pending

**Check DNS propagation**:
```bash
dig _amazonses.example.com TXT
dig token._domainkey.example.com CNAME
```

Wait up to 72 hours for global DNS propagation.

### Emails Going to Spam

**Verify authentication**:
- SPF: PASS
- DKIM: PASS
- DMARC: PASS

**Check spam score**: https://www.mail-tester.com/

**Common issues**:
- Missing plain text version (always include both HTML and text)
- Poor sender reputation
- Spammy content/excessive links

### MessageRejected Error

**Sandbox mode**: Verify recipient email address first
**Production**: Check bounce/complaint rates

## Best Practices

### Email Content

1. **Always include both HTML and plain text versions**
2. **Use clear subject lines** (< 50 chars)
3. **Avoid spam trigger words** (FREE, URGENT, etc.)
4. **Include unsubscribe link** (for marketing emails)

### Error Handling

```javascript
try {
  await sendEmail(to, subject, body);
} catch (error) {
  if (error.code === 'MessageRejected') {
    // Invalid/bounced address
  } else if (error.code === 'Throttling') {
    // Rate limit exceeded
  }
  // Log and handle appropriately
}
```

### Security

- Never commit credentials to version control
- Use environment variables or secrets management
- Rotate credentials every 90 days
- Use minimal IAM permissions (ses:SendEmail only)
- Sanitize user input before including in emails

### Monitoring

Set up CloudWatch alarms for:
- Bounce rate > 5%
- Complaint rate > 0.1%
- Sending quota approaching limit

## Production Checklist

- [ ] Domain verification complete
- [ ] DKIM configured and verified
- [ ] SPF includes amazonses.com
- [ ] DMARC policy configured
- [ ] Production access granted
- [ ] Bounce/complaint handling implemented
- [ ] Monitoring and alerts configured
- [ ] Credentials secured (not in code)
- [ ] Email templates tested across providers
- [ ] Unsubscribe mechanism implemented (if needed)

## Resources

- [AWS SES Developer Guide](https://docs.aws.amazon.com/ses/)
- [AWS SDK Documentation](https://aws.amazon.com/sdk-for-javascript/)
- [Email Authentication Best Practices](https://www.cloudflare.com/learning/email-security/dmarc-dkim-spf/)
- [MX Toolbox Email Headers](https://mxtoolbox.com/EmailHeaders.aspx)

## License

This integration guide is provided as-is for educational and implementation purposes.
