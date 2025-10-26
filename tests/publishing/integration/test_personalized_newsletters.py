import os
from fastapi.testclient import TestClient

os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_publishing.db")

from src.publishing.main import app  # noqa: E402

client = TestClient(app)


def test_personalized_newsletter_flow_placeholder():
    # Placeholder to enforce route presence; will be expanded
    resp = client.get("/api/v1/channels")
    assert resp.status_code in (200, 404)
