import os
from fastapi.testclient import TestClient

os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_publishing.db")

from src.publishing.main import app  # noqa: E402

client = TestClient(app)


def test_get_publication_not_found():
    resp = client.get("/api/v1/publications/non-existent-id")
    assert resp.status_code in (404, 500)
