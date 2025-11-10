import pytest


@pytest.mark.asyncio
async def test_entities_crud_contract(client):
    # Obtain token
    tok = await client.post("/auth/token", json={"email": "a@b.com", "password": "x"})
    assert tok.status_code == 200
    token = tok.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create
    r = await client.post("/entities", json={"name": "Acme", "type": "org"}, headers=headers)
    assert r.status_code == 201
    ent = r.json()

    # Read
    r = await client.get(f"/entities/{ent['id']}", headers=headers)
    assert r.status_code == 200

    # Update
    r = await client.put(f"/entities/{ent['id']}", json={"name": "Acme Inc"}, headers=headers)
    assert r.status_code == 200

    # List
    r = await client.get("/entities", headers=headers)
    assert r.status_code == 200

    # Delete
    r = await client.delete(f"/entities/{ent['id']}", headers=headers)
    assert r.status_code == 204

