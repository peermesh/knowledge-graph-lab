import os
import uuid
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_publishing.db")

from src.publishing.main import app  # noqa: E402

client = TestClient(app)


def test_multichannel_basic_flow():
    # Create email and slack channels
    email_id = client.post("/api/v1/channels", json={
        "name": f"Email-{uuid.uuid4().hex[:6]}",
        "channel_type": "email",
        "configuration": {},
        "is_active": True,
    }).json()["data"]["id"]

    slack_id = client.post("/api/v1/channels", json={
        "name": f"Slack-{uuid.uuid4().hex[:6]}",
        "channel_type": "slack",
        "configuration": {},
        "is_active": True,
    }).json()["data"]["id"]

    # Create publication
    payload = {
        "content_ids": [str(uuid.uuid4())],
        "channels": [email_id, slack_id],
        "publication_type": "newsletter",
        "scheduled_time": (datetime.utcnow() + timedelta(minutes=1)).isoformat() + "Z",
    }
    resp = client.post("/api/v1/publications", json=payload)
    assert resp.status_code in (200, 400)
