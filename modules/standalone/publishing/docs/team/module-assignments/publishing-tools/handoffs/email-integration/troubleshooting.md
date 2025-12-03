# Troubleshooting

## Email Not Sending

### "Email address is not verified"

**Problem:** Domain still verifying (DNS propagation).

**Fix:**
```bash
# Check domain status
aws ses get-identity-verification-attributes \
  --identities distributedcreatives.org \
  --region us-east-2

# Wait 15 min - 2 hours for DNS to propagate
```

### "MessageRejected: Email address not verified" (recipient)

**Problem:** Sandbox mode - can only send TO verified addresses.

**Fix:** Verify test email:
```bash
aws ses verify-email-identity \
  --email-address test@example.com \
  --region us-east-2
```

Check email and click verification link.

### "Throttling: Rate exceeded"

**Problem:** Sending too fast (1 email/second limit in sandbox).

**Fix:** Add delay between emails or queue them.

## Email Goes to Spam

### Check Authentication

View email headers (Gmail: three dots → Show original):
```
SPF: PASS
DKIM: PASS
DMARC: PASS
```

If any FAIL:
- SPF fail: DNS issue, check SPF record
- DKIM fail: Domain not verified yet, wait
- DMARC fail: Check DMARC policy

### Check Spam Score

Use https://www.mail-tester.com/
- Send email to address provided
- Check score (aim for 8+/10)

Common issues:
- Missing plain text version (always include both HTML and text)
- Spammy subject line
- Too many links
- Poor sender reputation (new domain)

## Code Not Working

### "Cannot find module"

**Fix:**
```bash
# Node.js
npm install @aws-sdk/client-ses dotenv

# Python
pip install boto3 python-dotenv

# Go
go get github.com/aws/aws-sdk-go/service/ses
```

### "Credentials not found"

**Fix:**
1. Check `.env` file exists
2. Check file is named exactly `.env` (not `.env.txt`)
3. Check you're loading it:
   - Node: `require('dotenv').config()`
   - Python: `from dotenv import load_dotenv; load_dotenv()`
   - Go: `godotenv.Load()`

### "Region not found"

**Fix:** Set region in `.env`:
```bash
AWS_REGION=us-east-2
```

## Production Issues

### Bounce Rate High

**Problem:** Sending to invalid/inactive email addresses.

**Fix:**
- Validate emails before sending
- Remove hard bounces from list
- Use double opt-in for signups

### Complaint Rate High

**Problem:** Users marking as spam.

**Fix:**
- Include clear unsubscribe link
- Send only requested emails
- Don't buy email lists

### Sending Quota Exceeded

**Problem:** Hit daily limit (200/day in sandbox, 50K/day in production).

**Fix:**
- Request production access (remove sandbox)
- Request quota increase via AWS Support

## DNS Issues

### Domain Verification Stuck

**Check DNS propagation:**
```bash
dig @8.8.8.8 _amazonses.distributedcreatives.org TXT
```

Should return: `"TE66lbYIPqac+aNTDisfCdY1P/CNBOhLkup03Zhk7MU="`

If not:
- Wait longer (up to 72 hours)
- Check DNS settings in Cloudflare
- Ensure record isn't proxied

### DKIM Not Verifying

**Check DKIM records:**
```bash
dig @8.8.8.8 <token>._domainkey.distributedcreatives.org CNAME
```

Should return: `<token>.dkim.amazonses.com`

If not:
- Wait for DNS propagation
- Check all 3 DKIM CNAMEs are added
- Ensure TTL is low (300)

## Still Stuck?

1. Check AWS SES console for specific errors
2. View email headers for delivery details
3. Check CloudWatch logs if configured
4. Contact project admin for credential issues
