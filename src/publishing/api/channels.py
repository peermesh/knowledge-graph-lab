from fastapi import APIRouter, Body, HTTPException, Path
from datetime import datetime
import uuid
from sqlalchemy import select

from ..core.config import settings
from ..core.database import get_async_session
from ..models.channel import Channel
from ..schemas.channels import ChannelCreateRequest, ChannelResponse

router = APIRouter()

# In-memory channel store is provided by src.publishing.state


@router.get("")
async def list_channels():
    async for session in get_async_session():
        result = await session.execute(select(Channel))
        channels = result.scalars().all()
        data = [
            {
                "id": str(c.id),
                "name": c.name,
                "channel_type": c.channel_type,
                "is_active": c.is_active,
                "configuration": c.configuration,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat(),
            }
            for c in channels
        ]
        return {"data": {"channels": data}, "meta": {"timestamp": datetime.utcnow().isoformat()}, "errors": []}


@router.post("")
async def create_channel(request: ChannelCreateRequest = Body(...)):
    async for session in get_async_session():
        channel = Channel(
            name=request.name,
            channel_type=request.channel_type,
            configuration=request.configuration,
            is_active=request.is_active,
        )
        session.add(channel)
        try:
            await session.commit()
        except Exception:
            raise HTTPException(status_code=409, detail="Channel creation failed")

        return {
            "data": {
                "id": str(channel.id),
                "name": channel.name,
                "channel_type": channel.channel_type,
                "is_active": channel.is_active,
                "configuration": channel.configuration,
            },
            "meta": {"timestamp": datetime.utcnow().isoformat()},
            "errors": [],
        }


@router.post("/{channel_id}/test")
async def test_channel(channel_id: str = Path(...)):
    # Placeholder: In future, call Slack/SES/etc. with a test message
    return {
        "data": {"success": True, "message": f"Test sent for channel {channel_id}"},
        "meta": {"timestamp": datetime.utcnow().isoformat()},
        "errors": [],
    }
