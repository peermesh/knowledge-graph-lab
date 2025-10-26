"""Job processing service with batch support and retry logic"""

from typing import List, Dict, Any, Optional
import logging
import asyncio
from datetime import datetime
import time

from src.ai.services.entity_extractor import entity_extractor
from src.ai.lib.deduplication import deduplicate_entities, update_relationship_entity_ids
from src.ai.integrations.message_queue import message_queue
from src.ai.config import settings

logger = logging.getLogger(__name__)


class JobProcessor:
    """Processes entity extraction jobs with batch support and retry logic"""
    
    MAX_RETRIES = 3
    RETRY_DELAYS = [1, 2, 4, 8, 16]  # Exponential backoff in seconds
    BATCH_SIZE = 10  # Process up to 10 documents at once
    
    def __init__(self):
        """Initialize job processor"""
        self.message_queue = message_queue
        self.active_jobs: Dict[str, Dict[str, Any]] = {}
    
    async def process_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single extraction job with retry logic.
        
        Args:
            job_data: Job information from message queue
        
        Returns:
            Processing results
        """
        job_id = job_data.get('job_id')
        retry_count = job_data.get('retry_count', 0)
        
        logger.info(
            f"Processing job {job_id} (attempt {retry_count + 1}/{self.MAX_RETRIES + 1})"
        )
        
        try:
            # Mark as active
            self.active_jobs[job_id] = {
                'started_at': datetime.utcnow(),
                'retry_count': retry_count
            }
            
            # Extract entities
            result = await entity_extractor.extract(
                document_id=job_data.get('document_id'),
                content=job_data.get('content'),
                entity_types=job_data.get('config', {}).get('entity_types'),
                relationship_types=job_data.get('config', {}).get('relationship_types'),
                confidence_threshold=job_data.get('config', {}).get('confidence_threshold', 0.7),
                language=job_data.get('config', {}).get('language')
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
            
            result['entities'] = deduplicated_entities
            result['relationships'] = updated_relationships
            
            # Publish results
            self.message_queue.publish_result(job_id, result)
            
            # Remove from active jobs
            del self.active_jobs[job_id]
            
            logger.info(
                f"Job {job_id} completed: {len(result['entities'])} entities, "
                f"{len(result['relationships'])} relationships"
            )
            
            return result
        
        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}")
            
            # Retry logic
            if retry_count < self.MAX_RETRIES:
                await self._retry_job(job_data, retry_count)
            else:
                # Max retries exceeded
                self.message_queue.publish_error(
                    job_id,
                    f"Job failed after {retry_count + 1} attempts: {str(e)}",
                    retry_count
                )
                
                # Remove from active jobs
                if job_id in self.active_jobs:
                    del self.active_jobs[job_id]
            
            raise
    
    async def _retry_job(self, job_data: Dict[str, Any], retry_count: int):
        """
        Retry failed job with exponential backoff.
        
        Args:
            job_data: Original job data
            retry_count: Current retry count
        """
        job_id = job_data.get('job_id')
        
        # Calculate delay (exponential backoff)
        delay = self.RETRY_DELAYS[min(retry_count, len(self.RETRY_DELAYS) - 1)]
        
        logger.info(
            f"Retrying job {job_id} in {delay} seconds "
            f"(attempt {retry_count + 2}/{self.MAX_RETRIES + 1})"
        )
        
        # Wait before retry
        await asyncio.sleep(delay)
        
        # Increment retry count
        job_data['retry_count'] = retry_count + 1
        
        # Re-publish to queue
        priority = job_data.get('priority', 'normal')
        self.message_queue.publish_job(job_data, priority)
        
        # Remove from active jobs
        if job_id in self.active_jobs:
            del self.active_jobs[job_id]
    
    async def process_batch(
        self,
        jobs: List[Dict[str, Any]],
        max_concurrent: int = None
    ) -> List[Dict[str, Any]]:
        """
        Process multiple jobs in batch.
        
        Args:
            jobs: List of job data
            max_concurrent: Maximum concurrent jobs (default: from settings)
        
        Returns:
            List of results
        """
        if max_concurrent is None:
            max_concurrent = min(self.BATCH_SIZE, settings.max_concurrent_jobs)
        
        logger.info(f"Processing batch of {len(jobs)} jobs (max concurrent: {max_concurrent})")
        
        # Create semaphore for concurrency control
        sem = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(job):
            async with sem:
                return await self.process_job(job)
        
        # Process jobs in parallel with concurrency limit
        tasks = [process_with_semaphore(job) for job in jobs]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Separate successful and failed results
        successful = []
        failed = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed.append({
                    'job_id': jobs[i].get('job_id'),
                    'error': str(result)
                })
            else:
                successful.append(result)
        
        logger.info(
            f"Batch complete: {len(successful)} successful, {len(failed)} failed"
        )
        
        return successful
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """
        Get statistics about message queues.
        
        Returns:
            Queue depth and active jobs count
        """
        try:
            stats = {}
            
            for queue_name in [self.HIGH_PRIORITY_QUEUE, self.NORMAL_PRIORITY_QUEUE, self.LOW_PRIORITY_QUEUE]:
                queue_info = self.channel.queue_declare(
                    queue=queue_name,
                    passive=True  # Don't create, just get info
                )
                stats[queue_name] = {
                    'message_count': queue_info.method.message_count,
                    'consumer_count': queue_info.method.consumer_count
                }
            
            stats['active_jobs'] = len(self.active_jobs)
            
            return stats
        
        except Exception as e:
            logger.error(f"Failed to get queue stats: {e}")
            return {}
    
    async def start_worker(
        self,
        priority: str = "normal",
        worker_id: Optional[str] = None
    ):
        """
        Start a worker to process jobs from queue.
        
        Args:
            priority: Priority level to process (high, normal, low)
            worker_id: Optional worker identifier
        """
        worker_id = worker_id or f"worker-{priority}-{id(self)}"
        
        logger.info(f"Starting worker {worker_id} for {priority} priority queue")
        
        async def job_callback(message: Dict[str, Any]):
            """Callback for processing job messages"""
            try:
                await self.process_job(message)
            except Exception as e:
                logger.error(f"Worker {worker_id} job processing failed: {e}")
        
        # Start consuming in separate thread
        # (In production, use celery or separate worker processes)
        self.message_queue.consume_jobs(
            callback=job_callback,
            priority=priority,
            prefetch_count=1
        )
    
    def shutdown(self):
        """Shutdown job processor gracefully"""
        logger.info("Shutting down job processor...")
        
        # Wait for active jobs to complete (with timeout)
        timeout = 60  # seconds
        start_time = time.time()
        
        while self.active_jobs and (time.time() - start_time) < timeout:
            logger.info(f"Waiting for {len(self.active_jobs)} active jobs to complete...")
            time.sleep(1)
        
        if self.active_jobs:
            logger.warning(
                f"Shutdown timeout: {len(self.active_jobs)} jobs still active"
            )
        
        # Close message queue connection
        self.message_queue.close()
        
        logger.info("Job processor shut down")


# Global job processor instance
job_processor = JobProcessor()

