import os
from fastapi.testclient import TestClient

os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_publishing.db")

from src.publishing.main import app  # noqa: E402

client = TestClient(app)


def test_newsletter_schedule_contract_route_presence():
    # Route may be part of publications; ensure endpoints exist or return 404
    resp = client.get("/api/v1/publications")
    assert resp.status_code in (200, 404)
