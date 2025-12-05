import pytest


@pytest.mark.asyncio
async def test_requires_auth(client):
    r = await client.get("/entities")
    assert r.status_code == 403 or r.status_code == 401


@pytest.mark.asyncio
async def test_invalid_token(client):
    r = await client.get("/entities", headers={"Authorization": "Bearer invalid"})
    assert r.status_code == 401




