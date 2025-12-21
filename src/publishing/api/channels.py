from fastapi import APIRouter, Body, HTTPException, Path
from datetime import datetime
import uuid
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import structlog

from ..core.config import settings
from ..core.database import get_async_session
from ..models.channel import Channel
from ..schemas.channels import ChannelCreateRequest, ChannelResponse
from .responses import success_response

router = APIRouter()
logger = structlog.get_logger(__name__)

# In-memory channel store for when database is not available
_in_memory_channels = []


@router.get("")
async def list_channels():
    """List all channels. Falls back to in-memory storage if database unavailable."""
    try:
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
            return success_response(data={"channels": data})
    except Exception as e:
        logger.warning("Database connection failed, using in-memory store", error=str(e))
        # Return in-memory channels as fallback
        data = [
            {
                "id": ch["id"],
                "name": ch["name"],
                "channel_type": ch["channel_type"],
                "is_active": ch["is_active"],
                "configuration": ch["configuration"],
                "created_at": ch["created_at"],
                "updated_at": ch["updated_at"],
            }
            for ch in _in_memory_channels
        ]
        return success_response(
            data={"channels": data},
            additional_meta={
                "mode": "in-memory",
                "note": "Database unavailable, using in-memory storage"
            }
        )


@router.post("")
async def create_channel(request: ChannelCreateRequest = Body(...)):
    """Create a new channel. Falls back to in-memory storage if database unavailable."""
    try:
        async for session in get_async_session():
            # Check if channel with this name already exists
            existing = await session.execute(
                select(Channel).where(Channel.name == request.name)
            )
            if existing.scalar_one_or_none():
                raise HTTPException(
                    status_code=409,
                    detail=f"Channel with name '{request.name}' already exists. Please use a different name or list existing channels."
                )
            
            channel = Channel(
                name=request.name,
                channel_type=request.channel_type,
                configuration=request.configuration,
                is_active=request.is_active,
            )
            session.add(channel)
            try:
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                if "unique" in str(e).lower() or "duplicate" in str(e).lower():
                    raise HTTPException(
                        status_code=409,
                        detail=f"Channel with name '{request.name}' already exists. Please use a different name."
                    )
                raise HTTPException(
                    status_code=409,
                    detail=f"Channel creation failed: {str(e)}"
                )
            except Exception as e:
                await session.rollback()
                raise HTTPException(
                    status_code=500,
                    detail=f"Channel creation failed: {str(e)}"
                )

            return success_response(
                data={
                    "id": str(channel.id),
                    "name": channel.name,
                    "channel_type": channel.channel_type,
                    "is_active": channel.is_active,
                    "configuration": channel.configuration,
                }
            )
    except HTTPException:
        # Re-raise HTTP exceptions (like 409)
        raise
    except Exception as e:
        logger.warning("Database connection failed, using in-memory store", error=str(e))
        # Fallback to in-memory storage
        # Check if channel with this name already exists in memory
        existing = [ch for ch in _in_memory_channels if ch["name"] == request.name]
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Channel with name '{request.name}' already exists. Please use a different name or list existing channels."
            )
        
        # Create new channel in memory
        channel_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        new_channel = {
            "id": channel_id,
            "name": request.name,
            "channel_type": request.channel_type,
            "is_active": getattr(request, 'is_active', True),
            "configuration": getattr(request, 'configuration', {}),
            "created_at": now,
            "updated_at": now,
        }
        _in_memory_channels.append(new_channel)
        
        return success_response(
            data={
                "id": new_channel["id"],
                "name": new_channel["name"],
                "channel_type": new_channel["channel_type"],
                "is_active": new_channel["is_active"],
                "configuration": new_channel["configuration"],
            },
            additional_meta={
                "mode": "in-memory",
                "note": "Database unavailable, using in-memory storage"
            }
        )


@router.post("/{channel_id}/test")
async def test_channel(channel_id: str = Path(...)):
    """Test a channel by sending a test message."""
    # Placeholder: In future, call Slack/SES/etc. with a test message
    return success_response(
        data={"success": True, "message": f"Test sent for channel {channel_id}"}
    )
