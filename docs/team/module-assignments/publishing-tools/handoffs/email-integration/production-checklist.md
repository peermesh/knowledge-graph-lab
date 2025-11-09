# Production Checklist

Before deploying to production, complete these steps.

## 1. Remove Sandbox Mode

### Request Production Access

1. Go to AWS SES Console → Account dashboard
2. Click "Request production access"
3. Fill form:
   - **Mail type**: Transactional
   - **Website**: distributedcreatives.org
   - **Use case**: Describe your email needs (password resets, notifications, etc.)
   - **Bounce handling**: "We remove hard bounces from our list"
4. Submit (approval usually within 24-48 hours)

**Why:** Sandbox limits you to 200 emails/day and verified recipients only.

## 2. New Credentials

Create production IAM user with minimal permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ses:SendEmail",
        "ses:SendRawEmail"
      ],
      "Resource": "*"
    }
  ]
}
```

**Why:** Test credentials have full SES access. Production should have send-only.

## 3. Monitor Bounce/Complaint Rates

### Set Up SNS Topics

1. Create SNS topic for bounces
2. Create SNS topic for complaints
3. Configure SES to publish to these topics
4. Subscribe your monitoring system

**Critical limits:**
- Bounce rate: Keep below 5%
- Complaint rate: Keep below 0.1%

**Why:** High rates get you suspended.

## 4. CloudWatch Alarms

Set up alarms for:
- Bounce rate > 5%
- Complaint rate > 0.1%
- Sending quota approaching limit
- Reputation dashboard warnings

**Why:** Catch issues before suspension.

## 5. Email Templates

- Test in Gmail, Outlook, Apple Mail
- Include unsubscribe link (for marketing emails)
- Include plain text version always
- Test on mobile devices

**Why:** Poor rendering = spam complaints.

## 6. Environment Variables

Use secrets manager instead of `.env`:
- AWS Secrets Manager
- AWS Systems Manager Parameter Store
- Kubernetes Secrets
- HashiCorp Vault

**Never** commit credentials to git.

**Why:** Security.

## 7. Rate Limiting

Implement per-user sending limits:
```javascript
// Example: Max 5 password reset emails per hour
const rateLimits = {
  'password-reset': { max: 5, window: 3600 }
};
```

**Why:** Prevent abuse and stay under quotas.

## 8. Error Handling

Log all email failures with context:
```javascript
try {
  await sendEmail(...);
} catch (error) {
  logger.error('Email failed', {
    error: error.message,
    to: email,
    template: 'password-reset',
    timestamp: new Date()
  });
  // Retry logic or queue for later
}
```

**Why:** Debug production issues.

## 9. Email Queue

Use queue for high volume:
- AWS SQS
- Redis Queue
- Bull (Node.js)
- Celery (Python)

**Why:** Handle spikes and retries gracefully.

## 10. Testing

Before go-live:
- [ ] Send 100 test emails
- [ ] Check spam score (aim for 8+/10)
- [ ] Verify all auth passes (SPF, DKIM, DMARC)
- [ ] Test unsubscribe flow
- [ ] Test all email templates
- [ ] Test error scenarios

## 11. Monitoring Dashboard

Track:
- Emails sent (today, this week, this month)
- Delivery rate
- Bounce rate
- Complaint rate
- Average send time

## 12. Custom MAIL FROM (Optional)

Set up `mail.distributedcreatives.org` for better deliverability:
1. Configure in SES console
2. Add MX and TXT records to DNS
3. Wait for verification

**Why:** Improves sender reputation.

## Quick Reference

**Production limits (after approval):**
- 50,000 emails/day (default)
- 14 emails/second
- Can request increase

**Sender reputation factors:**
- Bounce rate (< 5%)
- Complaint rate (< 0.1%)
- Email engagement (opens, clicks)
- Spam trap hits (avoid purchased lists)

**Best practices:**
- Double opt-in for signups
- Clear unsubscribe in every email
- Send only requested emails
- Remove hard bounces immediately
- Monitor reputation daily
