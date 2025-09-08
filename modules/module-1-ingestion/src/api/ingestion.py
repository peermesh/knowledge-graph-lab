"""
Ingestion API endpoints for content processing
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from sqlalchemy.orm import Session
import uuid

from ..core.database import get_db, IngestionJob
from ..services.ingestion_service import IngestionService

router = APIRouter()

class UrlIngestRequest(BaseModel):
    """Request model for single URL ingestion"""
    url: HttpUrl
    source_type: Optional[str] = "scrape"
    priority: Optional[int] = 5  # 1-10 priority scale

class BulkIngestRequest(BaseModel):
    """Request model for bulk URL processing"""
    urls: List[HttpUrl]
    source_type: Optional[str] = "scrape"
    priority: Optional[int] = 5

class RssSubscribeRequest(BaseModel):
    """Request model for RSS feed subscription"""
    feed_url: HttpUrl
    name: str
    check_interval: Optional[int] = 3600  # seconds

class JobStatus(BaseModel):
    """Job status response model"""
    job_id: str
    status: str
    progress: float
    url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None

@router.post("/url", response_model=dict)
async def ingest_url(
    request: UrlIngestRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Ingest content from a single URL
    
    Starts a background job to scrape and process the URL.
    Returns immediately with a job ID for status tracking.
    """
    job_id = str(uuid.uuid4())
    
    # Create job record
    job = IngestionJob(
        job_id=job_id,
        url=str(request.url),
        status="pending"
    )
    db.add(job)
    db.commit()
    
    # Start background processing
    ingestion_service = IngestionService()
    background_tasks.add_task(
        ingestion_service.process_url,
        job_id,
        str(request.url),
        request.source_type
    )
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": "URL ingestion started",
        "url": str(request.url)
    }

@router.post("/bulk", response_model=dict)
async def ingest_bulk(
    request: BulkIngestRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Process multiple URLs in a batch job
    
    Creates individual jobs for each URL but processes them efficiently.
    """
    job_ids = []
    
    for url in request.urls:
        job_id = str(uuid.uuid4())
        job_ids.append(job_id)
        
        # Create job record
        job = IngestionJob(
            job_id=job_id,
            url=str(url),
            status="pending"
        )
        db.add(job)
    
    db.commit()
    
    # Start bulk processing
    ingestion_service = IngestionService()
    background_tasks.add_task(
        ingestion_service.process_bulk_urls,
        job_ids,
        [str(url) for url in request.urls],
        request.source_type
    )
    
    return {
        "job_ids": job_ids,
        "status": "pending",
        "message": f"Bulk ingestion started for {len(request.urls)} URLs",
        "total_urls": len(request.urls)
    }

@router.post("/rss", response_model=dict)
async def subscribe_rss(
    request: RssSubscribeRequest,
    background_tasks: BackgroundTasks
):
    """
    Subscribe to an RSS feed for continuous monitoring
    
    Sets up automatic polling of the RSS feed at specified intervals.
    """
    # TODO: Implement RSS subscription logic
    return {
        "message": "RSS subscription feature coming soon",
        "feed_url": str(request.feed_url),
        "name": request.name
    }

@router.get("/status/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """
    Check the status of an ingestion job
    
    Returns current progress, status, and any error messages.
    """
    job = db.query(IngestionJob).filter(IngestionJob.job_id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatus(
        job_id=job.job_id,
        status=job.status,
        progress=job.progress,
        url=job.url,
        error_message=job.error_message,
        created_at=job.created_at.isoformat(),
        completed_at=job.completed_at.isoformat() if job.completed_at else None
    )

@router.get("/jobs", response_model=List[JobStatus])
async def list_jobs(
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    List recent ingestion jobs with optional status filtering
    """
    query = db.query(IngestionJob)
    
    if status:
        query = query.filter(IngestionJob.status == status)
    
    jobs = query.order_by(IngestionJob.created_at.desc()).limit(limit).all()
    
    return [
        JobStatus(
            job_id=job.job_id,
            status=job.status,
            progress=job.progress,
            url=job.url,
            error_message=job.error_message,
            created_at=job.created_at.isoformat(),
            completed_at=job.completed_at.isoformat() if job.completed_at else None
        ) for job in jobs
    ]