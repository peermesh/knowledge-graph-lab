import pytest


@pytest.mark.asyncio
async def test_health_ready_contract(client):
    r = await client.get("/health/ready")
    assert r.status_code == 200
    body = r.json()
    assert "status" in body and body["status"] in {"ok", "degraded"}
    assert "dependencies" in body and isinstance(body["dependencies"], dict)

