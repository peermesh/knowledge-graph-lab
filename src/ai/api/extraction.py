"""Entity extraction API endpoints"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, status
from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from src.ai.services.entity_extractor import entity_extractor
from src.ai.lib.deduplication import deduplicate_entities, update_relationship_entity_ids

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai/v1", tags=["entity-extraction"])


# Request/Response Models
class ExtractionConfig(BaseModel):
    """Configuration for entity extraction"""
    entity_types: List[str] = Field(
        default=['organization', 'person', 'funding_amount', 'date', 'location'],
        description="Entity types to extract"
    )
    relationship_types: List[str] = Field(
        default=['fund', 'partner', 'acquire', 'compete', 'collaborate'],
        description="Relationship types to identify"
    )
    confidence_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum confidence score"
    )
    language: Optional[str] = Field(
        default="en",
        description="Document language (en, es, fr, zh)"
    )


class ExtractionRequest(BaseModel):
    """Request for entity extraction"""
    document_id: UUID4 = Field(description="Unique document identifier")
    content: str = Field(min_length=1, max_length=1000000, description="Document content")
    document_type: str = Field(description="Document type (text, html, pdf)")
    extraction_config: Optional[ExtractionConfig] = Field(default=None)
    priority: str = Field(default="normal", description="Priority (high, normal, low)")


class Entity(BaseModel):
    """Extracted entity"""
    id: str
    text: str
    type: str
    confidence: float
    positions: List[List[int]]
    metadata: Optional[Dict[str, Any]] = None


class Relationship(BaseModel):
    """Entity relationship"""
    id: str
    source_entity: str  # entity ID
    target_entity: str  # entity ID
    relationship_type: str
    confidence: float
    evidence: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ExtractionResponse(BaseModel):
    """Response from entity extraction"""
    job_id: str
    status: str
    entities: List[Entity]
    relationships: List[Relationship]
    processing_time_seconds: float


class JobAcceptedResponse(BaseModel):
    """Response when job is accepted for async processing"""
    job_id: str
    status: str
    estimated_completion_seconds: Optional[int] = None


class JobStatusResponse(BaseModel):
    """Response for job status query"""
    job_id: str
    status: str
    entities: Optional[List[Entity]] = None
    relationships: Optional[List[Relationship]] = None
    processing_time_seconds: Optional[float] = None
    error_message: Optional[str] = None
    retry_count: Optional[int] = None


# In-memory job storage (replace with database in production)
jobs_store: Dict[str, Dict[str, Any]] = {}


@router.post("/extract-entities", response_model=ExtractionResponse, status_code=status.HTTP_200_OK)
async def extract_entities(request: ExtractionRequest, background_tasks: BackgroundTasks):
    """
    Extract entities and relationships from document content.
    
    Processes document synchronously for small documents (<10KB) or returns
    job ID for async processing of larger documents.
    """
    try:
        # Generate job ID
        import uuid
        job_id = str(uuid.uuid4())
        
        # Get extraction config
        config = request.extraction_config or ExtractionConfig()
        
        # Determine if should process synchronously or async
        content_size = len(request.content)
        process_async = content_size > 10000 or request.priority == "low"
        
        if process_async:
            # Store job for async processing
            jobs_store[job_id] = {
                'job_id': job_id,
                'status': 'pending',
                'document_id': str(request.document_id),
                'created_at': datetime.utcnow().isoformat()
            }
            
            # Schedule background processing
            background_tasks.add_task(
                _process_extraction_job,
                job_id,
                request,
                config
            )
            
            return JobAcceptedResponse(
                job_id=job_id,
                status='pending',
                estimated_completion_seconds=60
            )
        else:
            # Process synchronously
            result = await _extract_entities(
                document_id=str(request.document_id),
                content=request.content,
                config=config
            )
            
            return ExtractionResponse(
                job_id=job_id,
                status='completed',
                entities=[Entity(**e) for e in result['entities']],
                relationships=[Relationship(
                    id=r['id'],
                    source_entity=r['source_entity_id'],
                    target_entity=r['target_entity_id'],
                    relationship_type=r['relationship_type'],
                    confidence=r['confidence'],
                    evidence=r.get('evidence'),
                    metadata=r.get('metadata')
                ) for r in result['relationships']],
                processing_time_seconds=result['stats']['processing_time_seconds']
            )
    
    except Exception as e:
        logger.error(f"Entity extraction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Entity extraction failed: {str(e)}"
        )


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """
    Get the status and results of an extraction job.
    """
    if job_id not in jobs_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )
    
    job = jobs_store[job_id]
    
    response = JobStatusResponse(
        job_id=job_id,
        status=job['status'],
        retry_count=job.get('retry_count', 0)
    )
    
    # Add results if completed
    if job['status'] == 'completed':
        response.entities = [Entity(**e) for e in job.get('entities', [])]
        response.relationships = [Relationship(
            id=r['id'],
            source_entity=r['source_entity_id'],
            target_entity=r['target_entity_id'],
            relationship_type=r['relationship_type'],
            confidence=r['confidence'],
            evidence=r.get('evidence'),
            metadata=r.get('metadata')
        ) for r in job.get('relationships', [])]
        response.processing_time_seconds = job.get('processing_time_seconds')
    
    # Add error if failed
    if job['status'] == 'failed':
        response.error_message = job.get('error_message')
    
    return response


async def _extract_entities(
    document_id: str,
    content: str,
    config: ExtractionConfig
) -> Dict[str, Any]:
    """Internal function to extract entities"""
    # Extract entities using the service
    result = await entity_extractor.extract(
        document_id=document_id,
        content=content,
        entity_types=config.entity_types,
        relationship_types=config.relationship_types,
        confidence_threshold=config.confidence_threshold,
        language=config.language
    )
    
    # Deduplicate entities
    deduplicated_entities, id_mapping = deduplicate_entities(
        result['entities'],
        similarity_threshold=0.85
    )
    
    # Update relationship entity IDs
    updated_relationships = update_relationship_entity_ids(
        result['relationships'],
        id_mapping
    )
    
    return {
        'entities': deduplicated_entities,
        'relationships': updated_relationships,
        'stats': result['stats']
    }


async def _process_extraction_job(
    job_id: str,
    request: ExtractionRequest,
    config: ExtractionConfig
):
    """Background task to process extraction job"""
    try:
        # Update job status
        jobs_store[job_id]['status'] = 'processing'
        jobs_store[job_id]['started_at'] = datetime.utcnow().isoformat()
        
        # Extract entities
        result = await _extract_entities(
            document_id=str(request.document_id),
            content=request.content,
            config=config
        )
        
        # Update job with results
        jobs_store[job_id].update({
            'status': 'completed',
            'entities': result['entities'],
            'relationships': result['relationships'],
            'processing_time_seconds': result['stats']['processing_time_seconds'],
            'completed_at': datetime.utcnow().isoformat()
        })
        
        logger.info(f"Job {job_id} completed successfully")
    
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}", exc_info=True)
        
        # Update job with error
        retry_count = jobs_store[job_id].get('retry_count', 0)
        jobs_store[job_id].update({
            'status': 'failed',
            'error_message': str(e),
            'retry_count': retry_count + 1,
            'failed_at': datetime.utcnow().isoformat()
        })

