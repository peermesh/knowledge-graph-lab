require('dotenv').config();
const { SESClient, SendEmailCommand } = require("@aws-sdk/client-ses");

// Validate environment variables
const requiredEnvVars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION'];
const missing = requiredEnvVars.filter(v => !process.env[v]);

if (missing.length > 0) {
  console.error('❌ Missing required environment variables:', missing.join(', '));
  console.error('\nMake sure you have a .env file with:');
  console.error('AWS_ACCESS_KEY_ID=your_key');
  console.error('AWS_SECRET_ACCESS_KEY=your_secret');
  console.error('AWS_REGION=us-east-2');
  console.error('TEST_EMAIL=your_email@example.com');
  process.exit(1);
}

// Get test email from env or use default
const testEmail = process.env.TEST_EMAIL || 'grig@lumeneo.com';
const fromEmail = process.env.SES_FROM_EMAIL || 'noreply@distributedcreatives.org';

console.log('📧 AWS SES Email Test\n');
console.log('Configuration:');
console.log('  Region:', process.env.AWS_REGION);
console.log('  From:', fromEmail);
console.log('  To:', testEmail);
console.log('\nSending test email...\n');

// Create SES client
const sesClient = new SESClient({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

// Email content
const params = {
  Source: fromEmail,
  Destination: {
    ToAddresses: [testEmail],
  },
  Message: {
    Subject: {
      Data: '✅ SES Integration Test - Success!',
      Charset: 'UTF-8',
    },
    Body: {
      Text: {
        Data: `This is a test email from the working example.

If you're reading this, the AWS SES integration is working correctly!

Configuration:
- Region: ${process.env.AWS_REGION}
- From: ${fromEmail}
- To: ${testEmail}

Next steps:
1. Check that SPF, DKIM, DMARC all pass (view email headers)
2. Review the code in send-test-email.js
3. Use this as a template for your application

The email integration is ready to use!`,
        Charset: 'UTF-8',
      },
      Html: {
        Data: `<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background: #007bff; color: white; padding: 20px; text-align: center; }
    .content { padding: 20px; background: #f9f9f9; }
    .footer { padding: 20px; text-align: center; font-size: 12px; color: #666; }
    .success { color: #28a745; font-size: 24px; }
    code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
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
        <li><strong>Region:</strong> ${process.env.AWS_REGION}</li>
        <li><strong>From:</strong> ${fromEmail}</li>
        <li><strong>To:</strong> ${testEmail}</li>
      </ul>

      <h3>Next Steps:</h3>
      <ol>
        <li>Check that SPF, DKIM, DMARC all pass (view email headers)</li>
        <li>Review the code in <code>send-test-email.js</code></li>
        <li>Use this as a template for your application</li>
      </ol>

      <p><strong>The email integration is ready to use!</strong></p>
    </div>
    <div class="footer">
      <p>Sent via Amazon SES • Distributed Creatives</p>
    </div>
  </div>
</body>
</html>`,
        Charset: 'UTF-8',
      },
    },
  },
};

// Send email
async function sendTestEmail() {
  try {
    const command = new SendEmailCommand(params);
    const response = await sesClient.send(command);

    console.log('✅ SUCCESS! Email sent successfully!\n');
    console.log('Message ID:', response.MessageId);
    console.log('\nCheck your inbox at:', testEmail);
    console.log('\nTo verify authentication:');
    console.log('  1. Open the email');
    console.log('  2. View email headers (Gmail: three dots → Show original)');
    console.log('  3. Look for: spf=pass, dkim=pass, dmarc=pass');
    console.log('\n🎉 Integration test complete!\n');

  } catch (error) {
    console.error('❌ FAILED to send email\n');
    console.error('Error:', error.message);
    console.error('\nCommon issues:');

    if (error.message.includes('not verified')) {
      console.error('  → Domain verification pending (wait 15 min - 2 hours)');
      console.error('  → Or verify recipient email in sandbox mode:');
      console.error(`     aws ses verify-email-identity --email-address ${testEmail} --region ${process.env.AWS_REGION}`);
    }

    if (error.message.includes('Throttling')) {
      console.error('  → Rate limit exceeded (1 email/second in sandbox)');
      console.error('  → Wait a moment and try again');
    }

    if (error.message.includes('credentials')) {
      console.error('  → Check AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env');
    }

    console.error('\nSee troubleshooting.md for more help\n');
    process.exit(1);
  }
}

sendTestEmail();
