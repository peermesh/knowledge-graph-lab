# Publishing Module API Endpoints

This document summarizes key endpoints for the Publishing Module.

## Publications

- POST `/api/v1/publications`
  - Create a publication (newsletter, alert, digest, manual)
- GET `/api/v1/publications`
  - List publications with filters
- GET `/api/v1/publications/{id}`
  - Get publication details
- PUT `/api/v1/publications/{id}`
  - Update a publication
- DELETE `/api/v1/publications/{id}`
  - Cancel a scheduled publication
- POST `/api/v1/publications/{id}/retry`
  - Retry a failed publication
- NEW: POST `/api/v1/publications/newsletter/schedule`
  - Schedule a newsletter (timezone-aware in DEBUG via UTC normalization)

## Subscribers

- POST `/api/v1/subscribers`
  - Create or update a subscriber
- GET `/api/v1/subscribers`
  - List subscribers with filters
- GET `/api/v1/subscribers/{id}`
  - Get subscriber details
- PUT `/api/v1/subscribers/{id}`
  - Update subscriber preferences

## Channels

- POST `/api/v1/channels`
  - Create channel
- GET `/api/v1/channels`
  - List channels
- GET `/api/v1/channels/{id}`
  - Get channel
- PUT `/api/v1/channels/{id}`
  - Update channel
- DELETE `/api/v1/channels/{id}`
  - Deactivate channel
- POST `/api/v1/channels/{id}/test`
  - Test channel configuration

## Analytics

- GET `/api/v1/analytics/engagement`
  - Engagement analytics summary
- GET `/api/v1/analytics/performance`
  - Performance analytics and recommendations
- NEW: POST `/api/v1/analytics/engagement/track/open`
  - Track an open event for a publication (DEBUG in-memory)
- NEW: POST `/api/v1/analytics/engagement/track/click`
  - Track a click event for a publication (DEBUG in-memory)

## Authentication

All endpoints require JWT bearer tokens issued by the Backend module.

## Notes

- DEBUG mode uses in-memory stores for channels, subscribers, publications, and engagement to support early testing.
- T049–T051 implemented: timezone-aware scheduling, in-memory engagement tracking, and migration stubs for subscribers/templates.
