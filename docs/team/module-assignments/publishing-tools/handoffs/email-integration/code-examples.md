# Code Examples

Complete, working examples for integrating email sending into your application.

## Node.js

### Install Dependencies

```bash
npm install @aws-sdk/client-ses dotenv
```

### Basic Email Sending

**email.js:**
```javascript
require('dotenv').config();
const { SESClient, SendEmailCommand } = require("@aws-sdk/client-ses");

const sesClient = new SESClient({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

async function sendEmail(to, subject, bodyText, bodyHtml = null) {
  const params = {
    Source: process.env.SES_FROM_EMAIL || "noreply@distributedcreatives.org",
    Destination: {
      ToAddresses: Array.isArray(to) ? to : [to],
    },
    Message: {
      Subject: {
        Data: subject,
        Charset: "UTF-8",
      },
      Body: {
        Text: {
          Data: bodyText,
          Charset: "UTF-8",
        },
      },
    },
  };

  // Add HTML if provided
  if (bodyHtml) {
    params.Message.Body.Html = {
      Data: bodyHtml,
      Charset: "UTF-8",
    };
  }

  try {
    const command = new SendEmailCommand(params);
    const response = await sesClient.send(command);
    console.log("Email sent successfully. Message ID:", response.MessageId);
    return { success: true, messageId: response.MessageId };
  } catch (error) {
    console.error("Failed to send email:", error);
    return { success: false, error: error.message };
  }
}

module.exports = { sendEmail };
```

### Usage Examples

**Send plain text email:**
```javascript
const { sendEmail } = require('./email');

await sendEmail(
  "user@example.com",
  "Welcome!",
  "Thanks for signing up!"
);
```

**Send HTML email:**
```javascript
await sendEmail(
  "user@example.com",
  "Welcome!",
  "Thanks for signing up!",  // Plain text fallback
  "<h1>Welcome!</h1><p>Thanks for signing up!</p>"  // HTML version
);
```

**Send to multiple recipients:**
```javascript
await sendEmail(
  ["user1@example.com", "user2@example.com"],
  "Team Update",
  "Here's what's new..."
);
```

### Email Templates

**templates.js:**
```javascript
const templates = {
  welcome: (userName) => ({
    subject: "Welcome to Distributed Creatives!",
    text: `Hi ${userName},\n\nWelcome! We're excited to have you.\n\nBest,\nThe Team`,
    html: `
      <h2>Welcome to Distributed Creatives!</h2>
      <p>Hi ${userName},</p>
      <p>Welcome! We're excited to have you.</p>
      <p>Best,<br>The Team</p>
    `
  }),

  passwordReset: (resetLink, expiresIn) => ({
    subject: "Password Reset Request",
    text: `You requested a password reset.\n\nClick here: ${resetLink}\n\nThis link expires in ${expiresIn}.\n\nIf you didn't request this, ignore this email.`,
    html: `
      <h2>Password Reset Request</h2>
      <p>You requested a password reset.</p>
      <p><a href="${resetLink}" style="display:inline-block;padding:10px 20px;background:#007bff;color:white;text-decoration:none;border-radius:5px;">Reset Password</a></p>
      <p><small>This link expires in ${expiresIn}</small></p>
      <p><small>If you didn't request this, ignore this email.</small></p>
    `
  }),

  notification: (title, message) => ({
    subject: title,
    text: message,
    html: `<h3>${title}</h3><p>${message}</p>`
  })
};

module.exports = templates;
```

**Using templates:**
```javascript
const { sendEmail } = require('./email');
const templates = require('./templates');

// Send welcome email
const welcome = templates.welcome("Alice");
await sendEmail(
  "alice@example.com",
  welcome.subject,
  welcome.text,
  welcome.html
);

// Send password reset
const reset = templates.passwordReset("https://app.com/reset/abc123", "1 hour");
await sendEmail(
  "user@example.com",
  reset.subject,
  reset.text,
  reset.html
);
```

### Express.js Integration

```javascript
const express = require('express');
const { sendEmail } = require('./email');
const templates = require('./templates');

const app = express();
app.use(express.json());

// POST /api/email/welcome
app.post('/api/email/welcome', async (req, res) => {
  const { email, name } = req.body;

  const template = templates.welcome(name);
  const result = await sendEmail(email, template.subject, template.text, template.html);

  if (result.success) {
    res.json({ message: "Welcome email sent", messageId: result.messageId });
  } else {
    res.status(500).json({ error: result.error });
  }
});

// POST /api/email/password-reset
app.post('/api/email/password-reset', async (req, res) => {
  const { email, resetLink } = req.body;

  const template = templates.passwordReset(resetLink, "1 hour");
  const result = await sendEmail(email, template.subject, template.text, template.html);

  res.json({ success: result.success });
});

app.listen(3000);
```

---

## Python

### Install Dependencies

```bash
pip install boto3 python-dotenv
```

### Basic Email Sending

**email.py:**
```python
import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

ses_client = boto3.client(
    'ses',
    region_name=os.getenv('AWS_REGION', 'us-east-2'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def send_email(to_address, subject, body_text, body_html=None):
    """
    Send an email via Amazon SES

    Args:
        to_address: Recipient email (str or list)
        subject: Email subject
        body_text: Plain text body
        body_html: HTML body (optional)

    Returns:
        dict: {'success': bool, 'message_id': str or 'error': str}
    """
    from_email = os.getenv('SES_FROM_EMAIL', 'noreply@distributedcreatives.org')

    # Ensure to_address is a list
    if isinstance(to_address, str):
        to_address = [to_address]

    # Build email body
    body = {'Text': {'Data': body_text, 'Charset': 'UTF-8'}}
    if body_html:
        body['Html'] = {'Data': body_html, 'Charset': 'UTF-8'}

    try:
        response = ses_client.send_email(
            Source=from_email,
            Destination={'ToAddresses': to_address},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': body
            }
        )
        print(f"Email sent successfully. Message ID: {response['MessageId']}")
        return {'success': True, 'message_id': response['MessageId']}

    except ClientError as e:
        error_msg = e.response['Error']['Message']
        print(f"Failed to send email: {error_msg}")
        return {'success': False, 'error': error_msg}
```

### Usage Examples

```python
from email import send_email

# Send plain text email
send_email(
    "user@example.com",
    "Welcome!",
    "Thanks for signing up!"
)

# Send HTML email
send_email(
    "user@example.com",
    "Welcome!",
    "Thanks for signing up!",  # Fallback
    "<h1>Welcome!</h1><p>Thanks for signing up!</p>"  # HTML
)

# Send to multiple recipients
send_email(
    ["user1@example.com", "user2@example.com"],
    "Team Update",
    "Here's what's new..."
)
```

### Email Templates

**templates.py:**
```python
def welcome_email(user_name):
    return {
        'subject': "Welcome to Distributed Creatives!",
        'text': f"Hi {user_name},\n\nWelcome! We're excited to have you.\n\nBest,\nThe Team",
        'html': f"""
            <h2>Welcome to Distributed Creatives!</h2>
            <p>Hi {user_name},</p>
            <p>Welcome! We're excited to have you.</p>
            <p>Best,<br>The Team</p>
        """
    }

def password_reset_email(reset_link, expires_in="1 hour"):
    return {
        'subject': "Password Reset Request",
        'text': f"You requested a password reset.\n\nClick here: {reset_link}\n\nExpires in {expires_in}.\n\nIf you didn't request this, ignore this email.",
        'html': f"""
            <h2>Password Reset Request</h2>
            <p>You requested a password reset.</p>
            <p><a href="{reset_link}" style="display:inline-block;padding:10px 20px;background:#007bff;color:white;text-decoration:none;border-radius:5px;">Reset Password</a></p>
            <p><small>Expires in {expires_in}</small></p>
            <p><small>If you didn't request this, ignore this email.</small></p>
        """
    }
```

**Using templates:**
```python
from email import send_email
from templates import welcome_email, password_reset_email

# Send welcome email
template = welcome_email("Alice")
send_email(
    "alice@example.com",
    template['subject'],
    template['text'],
    template['html']
)

# Send password reset
template = password_reset_email("https://app.com/reset/abc123")
send_email(
    "user@example.com",
    template['subject'],
    template['text'],
    template['html']
)
```

### Flask Integration

```python
from flask import Flask, request, jsonify
from email import send_email
from templates import welcome_email, password_reset_email

app = Flask(__name__)

@app.route('/api/email/welcome', methods=['POST'])
def send_welcome():
    data = request.json
    email = data.get('email')
    name = data.get('name')

    template = welcome_email(name)
    result = send_email(
        email,
        template['subject'],
        template['text'],
        template['html']
    )

    if result['success']:
        return jsonify({'message': 'Welcome email sent', 'message_id': result['message_id']})
    else:
        return jsonify({'error': result['error']}), 500

@app.route('/api/email/password-reset', methods=['POST'])
def send_password_reset():
    data = request.json
    email = data.get('email')
    reset_link = data.get('reset_link')

    template = password_reset_email(reset_link)
    result = send_email(
        email,
        template['subject'],
        template['text'],
        template['html']
    )

    return jsonify({'success': result['success']})

if __name__ == '__main__':
    app.run(port=5000)
```

---

## Go

### Install Dependencies

```bash
go get github.com/aws/aws-sdk-go/aws
go get github.com/aws/aws-sdk-go/service/ses
go get github.com/joho/godotenv
```

### Basic Email Sending

**email.go:**
```go
package main

import (
    "fmt"
    "log"
    "os"

    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/credentials"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/ses"
    "github.com/joho/godotenv"
)

type EmailClient struct {
    svc *ses.SES
}

func NewEmailClient() *EmailClient {
    godotenv.Load()

    sess, err := session.NewSession(&aws.Config{
        Region: aws.String(os.Getenv("AWS_REGION")),
        Credentials: credentials.NewStaticCredentials(
            os.Getenv("AWS_ACCESS_KEY_ID"),
            os.Getenv("AWS_SECRET_ACCESS_KEY"),
            "",
        ),
    })
    if err != nil {
        log.Fatal("Failed to create session:", err)
    }

    return &EmailClient{svc: ses.New(sess)}
}

func (e *EmailClient) SendEmail(to, subject, bodyText, bodyHtml string) error {
    from := os.Getenv("SES_FROM_EMAIL")
    if from == "" {
        from = "noreply@distributedcreatives.org"
    }

    input := &ses.SendEmailInput{
        Source: aws.String(from),
        Destination: &ses.Destination{
            ToAddresses: []*string{aws.String(to)},
        },
        Message: &ses.Message{
            Subject: &ses.Content{
                Data:    aws.String(subject),
                Charset: aws.String("UTF-8"),
            },
            Body: &ses.Body{
                Text: &ses.Content{
                    Data:    aws.String(bodyText),
                    Charset: aws.String("UTF-8"),
                },
            },
        },
    }

    // Add HTML if provided
    if bodyHtml != "" {
        input.Message.Body.Html = &ses.Content{
            Data:    aws.String(bodyHtml),
            Charset: aws.String("UTF-8"),
        }
    }

    result, err := e.svc.SendEmail(input)
    if err != nil {
        return fmt.Errorf("failed to send email: %w", err)
    }

    fmt.Printf("Email sent successfully. Message ID: %s\n", *result.MessageId)
    return nil
}
```

### Usage Example

**main.go:**
```go
package main

import "log"

func main() {
    client := NewEmailClient()

    // Send plain text email
    err := client.SendEmail(
        "user@example.com",
        "Welcome!",
        "Thanks for signing up!",
        "",
    )
    if err != nil {
        log.Fatal(err)
    }

    // Send HTML email
    err = client.SendEmail(
        "user@example.com",
        "Welcome!",
        "Thanks for signing up!",
        "<h1>Welcome!</h1><p>Thanks for signing up!</p>",
    )
    if err != nil {
        log.Fatal(err)
    }
}
```

---

## Error Handling

All languages should handle these common errors:

### MessageRejected
Email address is invalid or not verified (sandbox mode).

**Node.js:**
```javascript
if (error.name === 'MessageRejected') {
  console.error('Email rejected - check if address is verified');
}
```

**Python:**
```python
if 'MessageRejected' in str(e):
    print('Email rejected - check if address is verified')
```

### Throttling
Rate limit exceeded (1 email/second in sandbox).

**Node.js:**
```javascript
if (error.name === 'Throttling') {
  console.error('Rate limit exceeded - slow down');
  // Wait and retry
}
```

### MailFromDomainNotVerified
Domain not verified yet (DNS still propagating).

```javascript
if (error.message.includes('not verified')) {
  console.error('Domain verification pending - wait 15-120 minutes');
}
```

## Testing Your Integration

1. **Send to yourself first** - Use your own email
2. **Check spam folder** - New sender reputation is low initially
3. **Verify email headers** - Ensure DKIM/SPF pass
4. **Test HTML rendering** - Check in Gmail, Outlook, Apple Mail
5. **Test error handling** - Try invalid email, rate limiting

## Next Steps

- **Docker setup**: See `docker-setup.md`
- **Production prep**: See `production-checklist.md`
- **DNS troubleshooting**: See `dns-configuration.md`
