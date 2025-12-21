import os
import uuid
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

# Ensure test-friendly settings
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_publishing.db")

from src.publishing.main import app  # noqa: E402

client = TestClient(app)


def create_channel(name: str = "Email", channel_type: str = "email"):
    resp = client.post("/api/v1/channels", json={
        "name": f"{name}-{uuid.uuid4().hex[:6]}",
        "channel_type": channel_type,
        "configuration": {},
        "is_active": True
    })
    assert resp.status_code in (200, 201)
    return resp.json()["data"]["id"]


def test_create_publication_returns_200_or_400():
    channel_id = create_channel()
    content_id = str(uuid.uuid4())

    payload = {
        "content_ids": [content_id],
        "channels": [channel_id],
        "publication_type": "newsletter",
        "scheduled_time": (datetime.utcnow() + timedelta(minutes=1)).isoformat() + "Z",
    }

    resp = client.post("/api/v1/publications", json=payload)
    assert resp.status_code in (200, 400, 422)
    # If 200, basic shape
    if resp.status_code == 200:
        body = resp.json()
        assert "data" in body and "meta" in body and "errors" in body
        assert body["data"]["publication_type"] == "newsletter"
    # If error (400/422), check RFC7807 format
    elif resp.status_code in (400, 422):
        assert resp.headers["Content-Type"] == "application/problem+json"
        error = resp.json()
        assert "type" in error
        assert "title" in error
        assert "status" in error
        assert "detail" in error
        assert "instance" in error
        assert error["status"] in (400, 422)
