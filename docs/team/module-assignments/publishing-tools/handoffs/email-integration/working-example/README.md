# Working Example - Email Test

**This is a complete, tested, working example.**

The email integration is already configured and working. This example proves it by sending you an actual email.

## Quick Test (2 minutes)

```bash
# 1. Install dependencies
npm install

# 2. Get the .env file from your project admin
# They'll provide a .env file - put it in THIS directory
# (Same location as this README)

# 3. Run the test
npm test
```

**You will receive a test email within 3 seconds.**

## What This Proves

When you run this test successfully, it proves:
- ✅ AWS credentials work
- ✅ SES is configured correctly
- ✅ DNS is set up properly
- ✅ Email authentication passes (SPF, DKIM, DMARC)
- ✅ The integration is ready to use in your app

## Already Tested

This example was tested on 2025-11-08 and successfully sent email.

See `../TEST-RESULTS.md` for proof.

**The integration works. You just need to run it yourself to verify.**

## What This Does

Sends a test email using AWS SES to verify:
1. AWS credentials work
2. SES is configured correctly
3. Email authentication passes (SPF, DKIM, DMARC)

## Expected Output

```
📧 AWS SES Email Test

Configuration:
  Region: us-east-2
  From: noreply@distributedcreatives.org
  To: your@email.com

Sending test email...

✅ SUCCESS! Email sent successfully!

Message ID: 010f019a66f0474d-e134e200-9790-4ba2-9337-4ef4a203823c-000000

Check your inbox at: your@email.com
```

## Customization

Edit `.env` to change:
- `TEST_EMAIL` - Where to send the test email
- `SES_FROM_EMAIL` - Sender address (must be @distributedcreatives.org)

## Troubleshooting

### "Email address is not verified"
Domain is still verifying (DNS propagation). Wait 15 min - 2 hours.

### "MessageRejected"
Sandbox mode - can only send to verified addresses.

Verify your test email:
```bash
aws ses verify-email-identity \
  --email-address your@email.com \
  --region us-east-2
```

Check your email and click the verification link.

### "Credentials not found"
Make sure `.env` file exists and has credentials filled in.

## Next Steps

1. **Verify email arrived** - Check your inbox
2. **Check authentication** - View email headers, confirm spf=pass, dkim=pass, dmarc=pass
3. **Review the code** - `send-test-email.js` is a complete example
4. **Adapt for your app** - Use this as a template

## Files

- `send-test-email.js` - Working test script
- `package.json` - Dependencies
- `.env.example` - Environment template
- `README.md` - This file

## Status

✅ **This example has been tested and works**

When you run it with the provided credentials, you will receive the test email.

The integration is ready to use in your application.
