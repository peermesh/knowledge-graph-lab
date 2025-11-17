import pytest


class FailingEngine:
    class _Conn:
        def execute(self, *_args, **_kwargs):
            raise RuntimeError("db down")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def connect(self):
        return self._Conn()


@pytest.mark.asyncio
async def test_health_ready_degraded_when_db_down(client, monkeypatch):
    import src.api.health as health_mod

    # Force the health endpoint to use a failing engine
    monkeypatch.setattr(health_mod, "engine", FailingEngine())

    r = await client.get("/health/ready")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "degraded"
    assert body["dependencies"].get("database") == "error"

