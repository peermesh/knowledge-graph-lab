"""
Tests for API health endpoints.

This module contains integration tests for health check endpoints
following TDD principles.
"""

import pytest
from httpx import AsyncClient

from app.main import app


class TestHealthEndpoints:
    """Test cases for health check endpoints."""

    @pytest.mark.asyncio
    async def test_health_check_endpoint(self):
        """Test the main health check endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")

            assert response.status_code == 200
            data = response.json()

            assert "status" in data
            assert "service" in data
            assert "version" in data
            assert "timestamp" in data
            assert "checks" in data

            assert data["status"] == "healthy"
            assert data["service"] == "AI Development Module"

    @pytest.mark.asyncio
    async def test_readiness_endpoint(self):
        """Test Kubernetes readiness probe."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/ready")

            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "ready"

    @pytest.mark.asyncio
    async def test_liveness_endpoint(self):
        """Test Kubernetes liveness probe."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/live")

            assert response.status_code == 200
            data = response.json()

            assert data["status"] == "alive"

    @pytest.mark.asyncio
    async def test_root_endpoint(self):
        """Test root endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/")

            assert response.status_code == 200
            data = response.json()

            assert "message" in data
            assert "AI Development Module" in data["message"]
