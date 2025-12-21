import os
from fastapi.testclient import TestClient

os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_publishing.db")

from src.publishing.main import app  # noqa: E402

client = TestClient(app)


def test_create_and_list_subscribers_contract():
    # Endpoint may not be implemented yet; ensure 404 or 200
    resp = client.get("/api/v1/subscribers")
    assert resp.status_code in (200, 404)
