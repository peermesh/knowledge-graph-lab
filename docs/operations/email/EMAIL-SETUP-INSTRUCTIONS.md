# Email Integration Setup Instructions

## ✅ What's Been Done

The email integration has been set up and is ready to test! Here's what was created:

### 1. Test Script (`scripts/send_test_email.py`)
Python script to test email sending - equivalent to the Node.js example from the handoff guide.

### 2. API Test Endpoint (`/api/v1/email/test`)
REST API endpoint accessible via Swagger UI for testing email functionality.

### 3. Documentation (`docs/.../PYTHON-INTEGRATION.md`)
Complete guide for using the existing Python email services.

### 4. Template File (`env.template`)
Template for creating your `.env` file with AWS credentials.

---

## 🚀 Next Steps (You Need To Do)

### Step 1: Create Your `.env` File

```bash
# Copy the template
cp env.template .env

# Edit .env with your AWS credentials
# (provided by project admin)
nano .env  # or use your preferred editor
```

**Important**: Replace these placeholder values in `.env`:
- `AWS_ACCESS_KEY_ID=your-aws-access-key-id` → Your actual AWS access key
- `AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key` → Your actual AWS secret key
- `TEST_EMAIL=your-email@example.com` → Your email address for testing

**Security**: The `.env` file is automatically protected:
- ✅ Already in `.gitignore` (line 6: `*.env`)
- ✅ Will NOT be committed to git
- ✅ Safe to store credentials locally

### Step 2: Verify Git Protection

```bash
# After creating .env, verify it's ignored:
git status  # Should NOT show .env file
git check-ignore .env  # Should output: .env
```

### Step 3: Test Email Sending

#### Option A: Run the Test Script

```bash
python scripts/send_test_email.py
```

**Expected output**:
```
============================================================
AWS SES Email Integration Test
============================================================

📧 AWS SES Email Test

Configuration:
  Region: us-east-2
  From: noreply@distributedcreatives.org
  To: your-email@example.com

Sending test email...

✅ SUCCESS! Email sent successfully!

Message ID: 0000abc123def456...
Provider: aws_ses

Check your inbox at: your-email@example.com

To verify authentication:
  1. Open the email
  2. View email headers (Gmail: three dots → Show original)
  3. Look for: spf=pass, dkim=pass, dmarc=pass

🎉 Integration test complete!
```

#### Option B: Test via API (Swagger UI)

```bash
# Start the API with Docker
docker-compose up --build

# Then visit: http://localhost:8080/api/v1/docs
# Find: POST /api/v1/email/test
# Try it with:
{
  "to_email": "your-email@example.com",
  "subject": "Test Email",
  "custom_message": "Testing!"
}
```

### Step 4: Verify Email Authentication

When you receive the test email:

1. Open the email in your inbox
2. View the email headers:
   - **Gmail**: Click three dots → "Show original"
   - **Outlook**: File → Properties → Internet headers
3. Look for these lines - all should show **PASS**:
   ```
   spf=pass
   dkim=pass
   dmarc=pass
   ```

---

## 📚 Documentation

- **Python Integration Guide**: `docs/team/module-assignments/publishing-tools/handoffs/email-integration/PYTHON-INTEGRATION.md`
- **Handoff Documentation**: `docs/team/module-assignments/publishing-tools/handoffs/email-integration/`
  - `START-HERE.md` - Quick start guide
  - `README.md` - Complete AWS SES setup
  - `troubleshooting.md` - Common issues and fixes
  - `production-checklist.md` - Before going live

---

## 🔧 Troubleshooting

### Email Not Sending?

1. **Check AWS credentials in `.env`**:
   ```bash
   cat .env  # Verify credentials are set
   ```

2. **SES in Sandbox Mode?**
   - Can only send TO verified email addresses
   - Verify your test email:
     ```bash
     aws ses verify-email-identity \
       --email-address your-email@example.com \
       --region us-east-2
     ```

3. **Domain not verified?**
   - Check DNS records (see `dns-configuration.md`)
   - Wait up to 72 hours for DNS propagation

4. **Rate limited?**
   - Sandbox: 1 email/second, 200/day limit
   - Wait a moment and try again
   - Request production access for higher limits

### Still Having Issues?

See the comprehensive troubleshooting guide:
```bash
cat docs/team/module-assignments/publishing-tools/handoffs/email-integration/troubleshooting.md
```

---

## 🎯 Quick Commands Reference

```bash
# Create .env file
cp env.template .env

# Edit .env (add your credentials)
nano .env

# Verify .env is protected
git check-ignore .env

# Run test script
python scripts/send_test_email.py

# Start API for testing via Swagger
docker-compose up api

# View API docs
open http://localhost:8080/api/v1/docs

# Check Docker logs
docker-compose logs -f api
```

---

## ✨ Features Available

The email integration supports:

- ✅ **HTML and plain text emails**
- ✅ **Single email sending**
- ✅ **Bulk email sending** (newsletters)
- ✅ **Placeholder mode** (works without credentials for dev)
- ✅ **Error handling** with detailed messages
- ✅ **API endpoint** for testing
- ✅ **CLI script** for quick testing
- ✅ **Async support** for high performance
- ✅ **SPF/DKIM/DMARC** authentication

---

## 📝 Implementation Details

### Email Service Files

1. **Simple Service** (`src/publishing/integrations/email_service.py`)
   - Production-ready
   - Placeholder mode for dev
   - Recommended for most use cases

2. **Advanced Service** (`src/publishing/integrations/aws_ses.py`)
   - Templates support
   - SNS notifications
   - Delivery statistics
   - Bounce tracking

### Configuration

Email service is already integrated in:
- `docker-compose.yml` (line 60-64, 76)
- `requirements.txt` (boto3)
- `src/publishing/core/config.py`

---

## 🎉 Success Criteria

You'll know everything is working when:

- ✅ Test script runs without errors
- ✅ Email arrives in your inbox
- ✅ Email headers show SPF=pass, DKIM=pass, DMARC=pass
- ✅ API endpoint returns 200 with message_id
- ✅ No placeholder mode messages (unless intended)

---

**Ready to test?** Create your `.env` file and run `python scripts/send_test_email.py`! 🚀

