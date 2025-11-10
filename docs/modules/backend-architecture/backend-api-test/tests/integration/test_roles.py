import pytest


@pytest.mark.asyncio
async def test_admin_route_requires_admin_role(client):
    # User token should be forbidden
    t_user = await client.post("/auth/token", json={"email": "user@example.com", "password": "x"})
    user_headers = {"Authorization": f"Bearer {t_user.json()['access_token']}"}
    r = await client.get("/admin/ping", headers=user_headers)
    assert r.status_code == 403

    # Admin token works
    t_admin = await client.post("/auth/token", json={"email": "admin@example.com", "password": "x"})
    admin_headers = {"Authorization": f"Bearer {t_admin.json()['access_token']}"}
    r = await client.get("/admin/ping", headers=admin_headers)
    assert r.status_code == 200
    assert r.json().get("role") == "Admin"




