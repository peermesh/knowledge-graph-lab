# Getting Started with Email Integration

## What This Does

Sends transactional emails (password resets, notifications, etc.) from your application using Amazon SES.

## Before You Start

You need:
1. AWS credentials (get from project admin)
2. Docker installed
3. 15-20 minutes

## Step 1: Set Up Environment

```bash
# Copy the template
cp .env.example .env

# Open .env and fill in the credentials you received
# Should look like:
# AWS_ACCESS_KEY_ID=AKIA...
# AWS_SECRET_ACCESS_KEY=...
# AWS_REGION=us-east-2
```

## Step 2: Test It Works

### Option A: Quick Test with AWS CLI

```bash
# Install AWS CLI if needed
brew install awscli  # macOS
# or: apt-get install awscli  # Linux

# Configure credentials
aws configure set aws_access_key_id YOUR_KEY_HERE
aws configure set aws_secret_access_key YOUR_SECRET_HERE
aws configure set region us-east-2

# Send test email
aws ses send-email \
  --from "test@distributedcreatives.org" \
  --destination "ToAddresses=YOUR_EMAIL@example.com" \
  --message "Subject={Data='Test Email'},Body={Text={Data='It works!'}}"
```

Check your inbox. If you got the email, AWS SES is working.

### Option B: Test with Code (Node.js)

```bash
# Install dependencies
npm install @aws-sdk/client-ses dotenv

# Create test.js (code below)
node test.js
```

**test.js:**
```javascript
require('dotenv').config();
const { SESClient, SendEmailCommand } = require("@aws-sdk/client-ses");

const sesClient = new SESClient({ region: process.env.AWS_REGION });

async function sendTestEmail() {
  const params = {
    Source: "test@distributedcreatives.org",
    Destination: { ToAddresses: ["YOUR_EMAIL@example.com"] },
    Message: {
      Subject: { Data: "Test from Node.js" },
      Body: { Text: { Data: "It works from code!" } }
    }
  };

  try {
    const command = new SendEmailCommand(params);
    const response = await sesClient.send(command);
    console.log("✅ Email sent! Message ID:", response.MessageId);
  } catch (error) {
    console.error("❌ Error:", error.message);
  }
}

sendTestEmail();
```

## Step 3: Use in Your App

See `code-examples.md` for complete examples in:
- Node.js
- Python
- Go

See `docker-setup.md` for containerized deployment.

## Common Issues

### "Email address is not verified"
The domain is still verifying. Wait 15 min - 2 hours, then try again.

Check status:
```bash
aws ses get-identity-verification-attributes \
  --identities distributedcreatives.org \
  --region us-east-2
```

### "Cannot send to this address"
We're in sandbox mode. Can only send to verified addresses.

Verify a test address:
```bash
aws ses verify-email-identity \
  --email-address yourtest@example.com \
  --region us-east-2
```

Check your email and click the verification link.

### "Credentials not found"
Your `.env` file isn't being read. Make sure:
1. File is named exactly `.env` (not `.env.txt`)
2. It's in the same directory as your code
3. You're loading it (use `dotenv` package)

## Next Steps

1. **Send your first email** (Step 2 above)
2. **Read code examples** for your language (`code-examples.md`)
3. **Set up Docker** if deploying in container (`docker-setup.md`)
4. **Understand DNS** to troubleshoot delivery (`dns-configuration.md`)

## Need Help?

- **Can't send email**: Check "Common Issues" above
- **Email goes to spam**: See `dns-configuration.md`
- **Production setup**: See `production-checklist.md`
- **Code not working**: See `code-examples.md` for your language
