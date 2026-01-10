# Output Gate: Publishing & Syndication Layer

**Version:** 0.1.0  
**Created:** 2026-01-10  
**Status:** Design  
**Purpose:** Controlled egress for notifications, emails, posts, and scheduled releases

---

## Overview

The Output Gate is the downstream counterpart to the Input Gate. While the Input Gate controls what enters the system, the Output Gate controls what leaves and when.

**Key functions:**
- Queue outputs for scheduled release
- Format content for each channel
- Deliver via appropriate transport
- Track delivery and engagement
- Respect user preferences

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INNER LOOP                                       │
│  ... → SYNTH → Answer                                                   │
└─────────────────────────────────────────┬───────────────────────────────┘
                                          │
                                          │ SynthesizedAnswer
                                          ▼
╔═══════════════════════════════════════════════════════════════════════════╗
║                            OUTPUT GATE                                     ║
║═══════════════════════════════════════════════════════════════════════════║
║                                                                            ║
║  ┌───────────────┐                                                        ║
║  │  CLASSIFIER   │  What type of output? Who cares?                       ║
║  └───────┬───────┘                                                        ║
║          │                                                                 ║
║          ▼                                                                 ║
║  ┌───────────────┐                                                        ║
║  │   SCHEDULER   │  When should it go out?                                ║
║  └───────┬───────┘                                                        ║
║          │                                                                 ║
║          ▼                                                                 ║
║  ┌───────────────┐                                                        ║
║  │   FORMATTER   │  How should it look for each channel?                  ║
║  └───────┬───────┘                                                        ║
║          │                                                                 ║
║          ▼                                                                 ║
║  ┌───────────────────────────────────────────────────────────────────┐   ║
║  │                      DELIVERY QUEUE                                │   ║
║  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │   ║
║  │  │ EMAIL   │  │  PUSH   │  │  SLACK  │  │   RSS   │  │ WEBHOOK │ │   ║
║  │  │ Queue   │  │  Queue  │  │  Queue  │  │  Queue  │  │  Queue  │ │   ║
║  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘ │   ║
║  └───────┼───────────┼───────────┼───────────┼───────────┼──────────┘   ║
║          │           │           │           │           │              ║
║          ▼           ▼           ▼           ▼           ▼              ║
║  ┌───────────────────────────────────────────────────────────────────┐   ║
║  │                      TRANSPORT LAYER                               │   ║
║  │  SendGrid    FCM/APNs    Slack API    Feed Gen    HTTP POST       │   ║
║  └───────────────────────────────────────────────────────────────────┘   ║
║          │           │           │           │           │              ║
║          ▼           ▼           ▼           ▼           ▼              ║
║  ┌───────────────────────────────────────────────────────────────────┐   ║
║  │                      TRACKER                                       │   ║
║  │  Delivery status, opens, clicks, bounces, engagement              │   ║
║  └───────────────────────────────────────────────────────────────────┘   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
                                          │
                                          ▼
                                    EXTERNAL WORLD
                                    (Devices, Inboxes, Feeds)
```

---

## Components

### 1. Classifier

**Purpose:** Determine output type, audience, and urgency

```typescript
interface ClassifiedOutput {
  output_id: string;
  content: SynthesizedAnswer | Report | Alert | Digest;
  
  output_type: "answer" | "report" | "alert" | "digest" | "notification";
  urgency: "immediate" | "high" | "normal" | "low" | "batch";
  
  audience: {
    type: "user" | "group" | "subscribers" | "public";
    targets: string[];
  };
  
  topics: string[];
  entities: string[];
  relevance_threshold: number;
}
```

**Classification Rules:**

| Output Type | Urgency | Audience | Example |
|-------------|---------|----------|---------|
| answer | immediate | user | Response to user query |
| alert | high | subscribers | Breaking news, deadline approaching |
| report | normal | subscribers | Daily research report |
| digest | batch | subscribers | Weekly summary |

---

### 2. Scheduler

**Purpose:** Determine when outputs should be delivered

**Scheduling Modes:**

| Mode | Description | Use Case |
|------|-------------|----------|
| Immediate | Send now | Urgent alerts, user responses |
| Scheduled | Send at specific time | Reports, digests |
| Window | Send within time window | Non-urgent, batch with others |
| Hold | Queue but don't send | Draft, needs approval |

**User Preference Schema:**

```typescript
interface DeliveryPreferences {
  user_id: string;
  timezone: string;
  
  quiet_hours: {
    enabled: boolean;
    start: string;  // "22:00"
    end: string;    // "08:00"
    override_urgent: boolean;
  };
  
  digest_time: string;      // "09:00"
  report_time: string;      // "08:00"
  
  channels: {
    alerts: ("email" | "push" | "slack")[];
    reports: ("email" | "rss")[];
    digests: ("email")[];
  };
  
  max_emails_per_day: number;
  max_push_per_hour: number;
  batch_similar_content: boolean;
}
```

---

### 3. Formatter

**Purpose:** Transform content for each delivery channel

#### Email Formatting

```typescript
interface EmailPayload {
  to: string;
  from: string;
  subject: string;
  html: string;
  text: string;  // plain text fallback
  tracking_pixel: string;
  unsubscribe_link: string;
}
```

#### Push Notification Formatting

```typescript
interface PushPayload {
  title: string;
  body: string;
  icon?: string;
  badge?: number;
  action_url: string;
}
```

#### Slack Formatting

```typescript
interface SlackPayload {
  channel: string;
  blocks: SlackBlock[];
  text: string;  // fallback
}
```

#### RSS Formatting

```typescript
interface RssItem {
  title: string;
  description: string;
  link: string;
  guid: string;
  pubDate: Date;
  categories: string[];
}
```

#### Webhook Formatting

```typescript
interface WebhookPayload {
  event_type: string;
  timestamp: Date;
  data: object;
  signature: string;  // HMAC for verification
}
```

---

### 4. Delivery Queue

**Purpose:** Manage per-channel queues with rate limiting and retry

```typescript
interface QueuedDelivery {
  delivery_id: string;
  output_id: string;
  channel: string;
  formatted: FormattedOutput;
  state: "pending" | "sending" | "sent" | "failed" | "retry";
  attempts: number;
  scheduled_for: Date;
}
```

---

### 5. Transport Layer

**Purpose:** Actual delivery via external services

| Channel | Provider Options |
|---------|------------------|
| Email | SendGrid, Mailgun, AWS SES |
| Push | Firebase (FCM), Apple (APNs) |
| Slack | Slack Bot API |
| RSS | Static feed generation |
| Webhook | HTTP POST with HMAC |

---

### 6. Tracker

**Purpose:** Monitor delivery status and engagement

```typescript
interface DeliveryTracking {
  delivery_id: string;
  channel: string;
  recipient: string;
  
  sent_at?: Date;
  delivered_at?: Date;
  failed_at?: Date;
  
  // Email engagement
  opened_at?: Date;
  open_count: number;
  clicked_at?: Date;
  click_count: number;
  
  // Push engagement
  tapped_at?: Date;
  dismissed_at?: Date;
}
```

**Tracking Events:**

| Event | Channel | How Tracked |
|-------|---------|-------------|
| sent | all | Transport response |
| delivered | email | Webhook from provider |
| bounced | email | Webhook from provider |
| opened | email | Tracking pixel |
| clicked | email | Redirect link |
| tapped | push | App callback |

---

## User-Configurable Settings

Everything the user can control:

```typescript
interface UserOutputSettings {
  user_id: string;
  
  channels: {
    email: { enabled: boolean; address: string; verified: boolean };
    push: { enabled: boolean; devices: DeviceToken[] };
    slack: { enabled: boolean; workspace_id: string; channel_id: string };
    rss: { enabled: boolean; feed_url: string };
    webhook: { enabled: boolean; url: string; secret: string; events: string[] };
  };
  
  timezone: string;
  quiet_hours: { enabled: boolean; start: string; end: string };
  
  digest_frequency: "daily" | "weekly" | "none";
  digest_time: string;
  max_emails_per_day: number;
  
  topics_subscribed: string[];
  entities_following: string[];
  min_relevance: number;
}
```

---

## Configuration Reference

```yaml
output_gate:
  enabled: true
  
  classifier:
    use_topic_subscriptions: true
    use_entity_following: true
    min_relevance_score: 0.7
  
  scheduler:
    default_digest_time: "09:00"
    default_timezone: "UTC"
    enable_batching: true
    batch_window_minutes: 30
    global_max_emails_per_user_per_day: 20
  
  formatter:
    template_dir: /templates/output
    enable_personalization: true
    email:
      track_opens: true
      track_clicks: true
  
  delivery_queue:
    channels:
      email:
        max_concurrent: 10
        rate_limit_per_second: 5
        retry_delays: [60, 300, 900, 3600]
      push:
        max_concurrent: 50
        rate_limit_per_second: 100
      webhook:
        timeout_seconds: 30
  
  transport:
    email:
      provider: sendgrid
      api_key: ${SENDGRID_API_KEY}
    push:
      fcm:
        credentials_file: /secrets/firebase-credentials.json
  
  tracker:
    storage: postgresql
    retention_days: 365
    publish_events: true
```

---

## Metrics

| Metric | Description |
|--------|-------------|
| `output_gate_classified_total` | Outputs classified |
| `output_gate_scheduled_total` | Outputs scheduled |
| `output_gate_sent_total` | Deliveries sent |
| `output_gate_delivered_total` | Deliveries confirmed |
| `output_gate_failed_total` | Deliveries failed |
| `output_gate_opened_total` | Emails opened |
| `output_gate_clicked_total` | Links clicked |
| `output_gate_queue_depth` | Current queue sizes |
