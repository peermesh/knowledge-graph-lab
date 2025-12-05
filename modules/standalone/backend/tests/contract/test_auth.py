import pytest


@pytest.mark.asyncio
async def test_issue_token_contract(client):
    r = await client.post("/auth/token", json={"email": "test@example.com", "password": "pw"})
    assert r.status_code == 200
    data = r.json()
    assert data.get("access_token") and data.get("token_type") == "bearer"

