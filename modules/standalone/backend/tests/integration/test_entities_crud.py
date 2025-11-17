import pytest


@pytest.mark.asyncio
async def test_entities_crud_flow(client):
    tok = await client.post("/auth/token", json={"email": "user@test.io", "password": "pw"})
    token = tok.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create
    r = await client.post("/entities", json={"name": "Widget", "type": "item"}, headers=headers)
    ent = r.json()

    # Update and verify
    await client.put(f"/entities/{ent['id']}", json={"name": "Widget 2"}, headers=headers)
    rr = await client.get(f"/entities/{ent['id']}", headers=headers)
    assert rr.json()["name"] == "Widget 2"

    # Soft delete and ensure excluded from list
    await client.delete(f"/entities/{ent['id']}", headers=headers)
    lst = await client.get("/entities", headers=headers)
    assert all(i["id"] != ent["id"] for i in lst.json())




