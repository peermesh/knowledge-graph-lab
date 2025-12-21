"""Test RFC7807 error format compliance."""
import os
from fastapi.testclient import TestClient

# Ensure test-friendly settings
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_publishing.db")

from src.publishing.main import app

client = TestClient(app)


def test_404_error_returns_rfc7807_format():
    """Test that 404 errors return RFC7807 Problem Details format."""
    response = client.get("/api/v1/nonexistent")
    
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/problem+json"
    
    error = response.json()
    assert "type" in error
    assert "title" in error
    assert "status" in error
    assert "detail" in error
    assert "instance" in error
    
    assert error["status"] == 404
    assert error["title"] == "Not Found"
    assert "httpstatuses.com/404" in error["type"]
    assert "/api/v1/nonexistent" in error["instance"]


def test_400_error_returns_rfc7807_format():
    """Test that 400 errors return RFC7807 Problem Details format."""
    # Create invalid request - missing required fields
    response = client.post("/api/v1/publications", json={"invalid": "data"})
    
    # FastAPI may return 422 for validation errors, which is also valid
    assert response.status_code in (400, 422)
    assert response.headers["Content-Type"] == "application/problem+json"
    
    error = response.json()
    assert error["status"] in (400, 422)
    assert "type" in error
    assert "title" in error
    assert "detail" in error
    assert "instance" in error


def test_409_error_returns_rfc7807_format():
    """Test that 409 errors return RFC7807 Problem Details format."""
    # Create a channel first
    channel_response = client.post("/api/v1/channels", json={
        "name": "test-channel-409",
        "channel_type": "email",
        "configuration": {},
        "is_active": True
    })
    
    # Try to create duplicate channel
    duplicate_response = client.post("/api/v1/channels", json={
        "name": "test-channel-409",
        "channel_type": "email",
        "configuration": {},
        "is_active": True
    })
    
    # Should return 409 Conflict
    assert duplicate_response.status_code == 409
    assert duplicate_response.headers["Content-Type"] == "application/problem+json"
    
    error = duplicate_response.json()
    assert error["status"] == 409
    assert error["title"] == "Conflict"
    assert "type" in error
    assert "detail" in error
    assert "instance" in error
    assert "httpstatuses.com/409" in error["type"]


def test_error_includes_trace_id():
    """Test that error responses include traceId when available."""
    response = client.get("/api/v1/nonexistent")
    
    assert response.status_code == 404
    error = response.json()
    
    # Trace ID should be in X-Correlation-ID header
    assert "X-Correlation-ID" in response.headers
    
    # Trace ID may also be in error body if implemented
    # This is optional per RFC7807, so we check if it exists
    if "traceId" in error:
        assert error["traceId"] == response.headers["X-Correlation-ID"]


def test_error_content_type_header():
    """Test that all error responses have correct Content-Type header."""
    # Test 404
    response = client.get("/api/v1/nonexistent")
    assert response.headers["Content-Type"] == "application/problem+json"
    
    # Test 400/422
    response = client.post("/api/v1/publications", json={})
    assert response.headers["Content-Type"] == "application/problem+json"
    
    # Test 409 (if we can trigger it)
    # Already tested in test_409_error_returns_rfc7807_format


def test_error_structure_required_fields():
    """Test that error responses contain all required RFC7807 fields."""
    response = client.get("/api/v1/nonexistent")
    error = response.json()
    
    # Required fields per RFC7807
    assert "type" in error, "Missing 'type' field"
    assert "title" in error, "Missing 'title' field"
    assert "status" in error, "Missing 'status' field"
    assert "detail" in error, "Missing 'detail' field"
    assert "instance" in error, "Missing 'instance' field"
    
    # Verify types
    assert isinstance(error["type"], str)
    assert isinstance(error["title"], str)
    assert isinstance(error["status"], int)
    assert isinstance(error["detail"], str)
    assert isinstance(error["instance"], str)


def test_error_type_uri_format():
    """Test that error type URIs follow expected format."""
    response = client.get("/api/v1/nonexistent")
    error = response.json()
    
    # Type should be a URI
    assert error["type"].startswith("http://") or error["type"].startswith("https://")
    
    # For standard HTTP errors, should use httpstatuses.com
    if error["status"] in (400, 401, 403, 404, 409, 422, 500, 503):
        assert "httpstatuses.com" in error["type"] or "api.knowledge-graph-lab.com" in error["type"]

