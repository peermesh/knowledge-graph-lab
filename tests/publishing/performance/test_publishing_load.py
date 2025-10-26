import pytest
import asyncio

from src.publishing.services.publication_service import PublicationService


@pytest.mark.asyncio
async def test_concurrent_publication_mark_complete_smoke():
    svc = PublicationService()
    pub_ids = [str(i) for i in range(50)]

    async def mark_done(pid):
        await svc.update_publication_status(pid, "completed", channel_results={})

    # just ensure the function can be called concurrently without raising in our stub
    await asyncio.gather(*(mark_done(pid) for pid in pub_ids))
    assert True
