**Non-canonical during concept phase — authoritative conceptual PRDs live in .dev/peermesh-canvases/**

# Publisher Module PRD - MVP Version

## Module Owner: Developer 4

## Executive Summary
Build a Python/FastAPI service that manages email subscribers and sends daily digests with creator economy updates. Total time: 100 hours.

## Goals (MVP)
1. Manage email subscriber list
2. Create email templates
3. Send daily digest emails
4. Track what was sent
5. Run in Docker container

## User Stories

### Phase 1 (Weeks 1-6): Core Features
- As a user, I can subscribe via the Frontend
- As a subscriber, I receive a welcome email
- As a subscriber, I get daily digest emails
- As an admin, I can see subscriber list
- As the system, I track what emails were sent

### Phase 2 (Weeks 7-10): Enhancements
- Add unsubscribe functionality
- Personalize emails based on preferences
- Add email analytics (opens/clicks)
- Improve email templates
- Add scheduling options

## Technical Requirements

### Stack
- Python 3.11
- FastAPI
- SQLite for subscriber data
- Jinja2 for email templates
- smtplib for email sending
- Docker

### API Endpoints (Minimal)
```python
# 1. Subscribe a user
POST /api/subscribers
{
  "email": "user@example.com",
  "preferences": {
    "topics": ["youtube", "grants"],
    "frequency": "daily"
  }
}

# 2. List subscribers
GET /api/subscribers

# 3. Unsubscribe
DELETE /api/subscribers/{email}

# 4. Send digest (manually trigger)
POST /api/send-digest
{"test_mode": true}  # Send to test email only

# 5. Get email templates
GET /api/templates
```

### Database Schema
```sql
CREATE TABLE subscribers (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    preferences TEXT,  -- JSON
    subscribed_at TIMESTAMP,
    active BOOLEAN DEFAULT true,
    unsubscribe_token TEXT
);

CREATE TABLE sent_emails (
    id INTEGER PRIMARY KEY,
    subscriber_id INTEGER,
    sent_at TIMESTAMP,
    template TEXT,
    subject TEXT,
    success BOOLEAN,
    FOREIGN KEY(subscriber_id) REFERENCES subscribers(id)
);
```

## Email Templates

### Welcome Email
```html
<h2>Welcome to Knowledge Graph Lab!</h2>
<p>Hi there!</p>
<p>You're now subscribed to creator economy updates.</p>
<p>You'll receive:</p>
<ul>
  <li>Grant opportunities</li>
  <li>Platform updates</li>
  <li>Creator programs</li>
</ul>
<p>First digest arrives tomorrow!</p>
```

### Daily Digest
```html
<h2>Your Creator Economy Update</h2>
<p>Here's what's new today:</p>

<h3>New Opportunities (3)</h3>
<ul>
  <li><b>YouTube Partner Program</b> - New tier announced</li>
  <li><b>TikTok Creator Fund</b> - Applications open</li>
  <li><b>Twitch Drops</b> - New revenue stream</li>
</ul>

<h3>Platform Updates (2)</h3>
<ul>
  <li>Instagram adds new monetization features</li>
  <li>Twitter launches Super Follows</li>
</ul>

<p><a href="#">Unsubscribe</a></p>
```

## Implementation Plan

### Week 1-2: Setup
- [ ] Create Docker container
- [ ] Setup FastAPI project
- [ ] Create SQLite database
- [ ] Setup email templates

### Week 3-4: Subscriber Management
- [ ] Implement subscribe endpoint
- [ ] Create subscriber list endpoint
- [ ] Add unsubscribe functionality
- [ ] Generate unsubscribe tokens

### Week 5-6: Email Sending
- [ ] Setup SMTP configuration
- [ ] Implement send digest endpoint
- [ ] Create email templates
- [ ] Add sent email tracking

### Week 7-8: Enhancement
- [ ] Add email personalization
- [ ] Improve templates
- [ ] Add scheduling
- [ ] Error handling

### Week 9-10: Integration
- [ ] Connect to Backend for content
- [ ] Test with Frontend signup
- [ ] Fix integration issues

### Week 11-12: Demo Prep
- [ ] End-to-end testing
- [ ] Polish email templates
- [ ] Demo preparation

## Email Configuration

### Development (Local SMTP)
```python
# Use Python's debug server
# python -m smtpd -n -c DebuggingServer localhost:1025

SMTP_HOST = "localhost"
SMTP_PORT = 1025
SMTP_USER = None
SMTP_PASSWORD = None
```

### Production (Gmail Example)
```python
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your-email@gmail.com"
SMTP_PASSWORD = "app-specific-password"
```

## Success Criteria
- [ ] Can add 10+ subscribers
- [ ] Sends welcome emails
- [ ] Sends daily digest
- [ ] Tracks sent emails
- [ ] Unsubscribe works

## Dependencies
- Backend Module: Provides content for digests
- Frontend Module: Sends new subscribers

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| Email deliverability | Use local SMTP for testing |
| Spam filters | Keep emails simple |
| Template complexity | Start with plain text |
| Scheduling issues | Manual trigger for MVP |

## Resources Provided
1. FastAPI template
2. Email template examples
3. SMTP configuration guide
4. Docker configuration
5. Test email list

## Example Code Structure
```
publisher/
├── Dockerfile
├── requirements.txt
├── app/
│   ├── main.py          # FastAPI app
│   ├── database.py      # SQLite setup
│   ├── models.py        # Data models
│   ├── routers/
│   │   ├── subscribers.py # Subscriber endpoints
│   │   └── digest.py     # Digest endpoints
│   ├── services/
│   │   ├── email.py      # Email sending
│   │   └── content.py    # Get content from Backend
│   └── templates/
│       ├── welcome.html
│       └── digest.html
└── tests/
    └── test_email.py
```

## Getting Started
```bash
# Clone repo
git clone <repo>
cd modules/publisher

# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run email debug server (separate terminal)
python -m smtpd -n -c DebuggingServer localhost:1025

# Run app
uvicorn app.main:app --reload --port 8002

# Test subscribe
curl -X POST http://localhost:8002/api/subscribers \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# Test send digest
curl -X POST http://localhost:8002/api/send-digest \
  -d '{"test_mode": true}'
```

## Sample Digest Content
```python
# Mock content for testing
def get_mock_digest_content():
    return {
        "opportunities": [
            {"title": "YouTube Partner Program", "description": "New tier"},
            {"title": "TikTok Creator Fund", "description": "Now open"}
        ],
        "updates": [
            {"platform": "Instagram", "update": "New monetization"},
            {"platform": "Twitter", "update": "Super Follows launch"}
        ]
    }
```

## Questions to Resolve
1. Email frequency? (Daily for MVP)
2. Template format? (HTML with plain text fallback)
3. Personalization level? (Basic topics for MVP)

## Notes
- Use local SMTP to avoid email service setup
- Keep templates simple and clean
- Focus on delivery over design
- Test with personal email first