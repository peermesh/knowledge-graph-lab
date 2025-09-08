"""
Source management API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import json

from ..core.database import get_db, Source

router = APIRouter()

class SourceCreate(BaseModel):
    """Request model for creating a new source"""
    name: str
    url: HttpUrl
    source_type: str  # 'rss', 'api', 'scrape', 'manual'
    config: Optional[Dict[str, Any]] = {}

class SourceUpdate(BaseModel):
    """Request model for updating a source"""
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None

class SourceResponse(BaseModel):
    """Response model for source data"""
    id: int
    name: str
    url: str
    source_type: str
    is_active: bool
    config: Dict[str, Any]
    created_at: str
    updated_at: str

@router.get("/", response_model=List[SourceResponse])
async def list_sources(
    source_type: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    List all configured data sources
    
    Optionally filter by source type and active status.
    """
    query = db.query(Source)
    
    if source_type:
        query = query.filter(Source.source_type == source_type)
    
    if active_only:
        query = query.filter(Source.is_active == True)
    
    sources = query.order_by(Source.name).all()
    
    return [
        SourceResponse(
            id=source.id,
            name=source.name,
            url=source.url,
            source_type=source.source_type,
            is_active=source.is_active,
            config=json.loads(source.config) if source.config else {},
            created_at=source.created_at.isoformat(),
            updated_at=source.updated_at.isoformat()
        ) for source in sources
    ]

@router.post("/", response_model=SourceResponse)
async def create_source(
    source_data: SourceCreate,
    db: Session = Depends(get_db)
):
    """
    Add a new data source configuration
    
    Creates a new source that can be used for automated content ingestion.
    """
    # Check if source name already exists
    existing = db.query(Source).filter(Source.name == source_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Source name already exists")
    
    # Create new source
    source = Source(
        name=source_data.name,
        url=str(source_data.url),
        source_type=source_data.source_type,
        config=json.dumps(source_data.config) if source_data.config else "{}"
    )
    
    db.add(source)
    db.commit()
    db.refresh(source)
    
    return SourceResponse(
        id=source.id,
        name=source.name,
        url=source.url,
        source_type=source.source_type,
        is_active=source.is_active,
        config=json.loads(source.config) if source.config else {},
        created_at=source.created_at.isoformat(),
        updated_at=source.updated_at.isoformat()
    )

@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(source_id: int, db: Session = Depends(get_db)):
    """
    Get a specific source by ID
    """
    source = db.query(Source).filter(Source.id == source_id).first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    return SourceResponse(
        id=source.id,
        name=source.name,
        url=source.url,
        source_type=source.source_type,
        is_active=source.is_active,
        config=json.loads(source.config) if source.config else {},
        created_at=source.created_at.isoformat(),
        updated_at=source.updated_at.isoformat()
    )

@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: int,
    update_data: SourceUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing source configuration
    """
    source = db.query(Source).filter(Source.id == source_id).first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    # Update fields if provided
    if update_data.name is not None:
        source.name = update_data.name
    if update_data.url is not None:
        source.url = str(update_data.url)
    if update_data.is_active is not None:
        source.is_active = update_data.is_active
    if update_data.config is not None:
        source.config = json.dumps(update_data.config)
    
    db.commit()
    db.refresh(source)
    
    return SourceResponse(
        id=source.id,
        name=source.name,
        url=source.url,
        source_type=source.source_type,
        is_active=source.is_active,
        config=json.loads(source.config) if source.config else {},
        created_at=source.created_at.isoformat(),
        updated_at=source.updated_at.isoformat()
    )

@router.delete("/{source_id}")
async def delete_source(source_id: int, db: Session = Depends(get_db)):
    """
    Remove a data source configuration
    """
    source = db.query(Source).filter(Source.id == source_id).first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    db.delete(source)
    db.commit()
    
    return {"message": f"Source '{source.name}' deleted successfully"}

@router.get("/{source_id}/stats")
async def get_source_stats(source_id: int, db: Session = Depends(get_db)):
    """
    Get performance statistics for a specific source
    
    Returns metrics like successful ingestions, failures, and performance data.
    """
    source = db.query(Source).filter(Source.id == source_id).first()
    
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    # TODO: Implement actual statistics calculation
    # This would query ingestion jobs and content items for this source
    
    return {
        "source_id": source_id,
        "source_name": source.name,
        "total_jobs": 0,
        "successful_jobs": 0,
        "failed_jobs": 0,
        "average_processing_time": 0,
        "last_successful_run": None,
        "content_items_generated": 0
    }