import pytest

from src.publishing.services.slack_service import SlackService
import httpx


class _MockResponse:
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json


class _MockAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, url, json=None, headers=None):
        return _MockResponse({"ok": True, "channel": json.get("channel"), "text": json.get("text")})


@pytest.mark.asyncio
async def test_slack_send_message_monkeypatched(monkeypatch):
    monkeypatch.setattr(httpx, "AsyncClient", _MockAsyncClient)
    svc = SlackService()
    result = await svc.send_message(channel="#test", text="hello")
    assert result.get("ok") is True
    assert result.get("text") == "hello"
