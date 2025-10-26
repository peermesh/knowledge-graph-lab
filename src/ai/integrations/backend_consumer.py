"""Backend integration - message queue consumer for document processing"""

import asyncio
import logging
from typing import Dict, Any
import sys

from src.ai.services.job_processor import job_processor
from src.ai.integrations.message_queue import message_queue

logger = logging.getLogger(__name__)


class BackendConsumer:
    """Consumes document processing jobs from Backend module"""
    
    def __init__(self):
        """Initialize backend consumer"""
        self.job_processor = job_processor
        self.message_queue = message_queue
        self.running = False
    
    async def start(self, num_workers: int = 4):
        """
        Start consuming jobs from backend.
        
        Args:
            num_workers: Number of worker processes to start
        """
        logger.info(f"Starting backend consumer with {num_workers} workers")
        self.running = True
        
        # Start workers for each priority level
        workers = []
        
        # High priority workers (2 workers)
        high_priority_workers = min(2, num_workers // 2)
        for i in range(high_priority_workers):
            worker_id = f"high-priority-worker-{i+1}"
            workers.append(
                asyncio.create_task(
                    self._start_worker(worker_id, 'high')
                )
            )
        
        # Normal priority workers
        normal_priority_workers = num_workers - high_priority_workers
        for i in range(normal_priority_workers):
            worker_id = f"normal-priority-worker-{i+1}"
            workers.append(
                asyncio.create_task(
                    self._start_worker(worker_id, 'normal')
                )
            )
        
        # Low priority workers (1 worker if space available)
        if num_workers > 3:
            workers.append(
                asyncio.create_task(
                    self._start_worker("low-priority-worker-1", 'low')
                )
            )
        
        logger.info(f"Started {len(workers)} workers")
        
        # Wait for all workers
        try:
            await asyncio.gather(*workers)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
            self.running = False
        except Exception as e:
            logger.error(f"Worker error: {e}")
            self.running = False
    
    async def _start_worker(self, worker_id: str, priority: str):
        """
        Start a single worker for a specific priority queue.
        
        Args:
            worker_id: Unique worker identifier
            priority: Priority level (high, normal, low)
        """
        logger.info(f"Worker {worker_id} started for {priority} priority")
        
        while self.running:
            try:
                # Process jobs from queue
                await self.job_processor.start_worker(
                    priority=priority,
                    worker_id=worker_id
                )
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
                
                # Wait before restarting
                await asyncio.sleep(5)
                
                if self.running:
                    logger.info(f"Restarting worker {worker_id}")
        
        logger.info(f"Worker {worker_id} stopped")
    
    async def process_single_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single job directly (for testing).
        
        Args:
            job_data: Job information
        
        Returns:
            Processing results
        """
        return await self.job_processor.process_job(job_data)
    
    async def process_batch_jobs(
        self,
        jobs: List[Dict[str, Any]],
        max_concurrent: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Process multiple jobs in batch.
        
        Args:
            jobs: List of job data
            max_concurrent: Maximum concurrent jobs
        
        Returns:
            List of results
        """
        logger.info(f"Processing batch of {len(jobs)} jobs")
        
        return await self.job_processor.process_batch(
            jobs,
            max_concurrent=max_concurrent
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get consumer statistics"""
        queue_stats = self.message_queue.get_queue_stats()
        
        return {
            'running': self.running,
            'queue_stats': queue_stats,
            'active_jobs': len(self.job_processor.active_jobs)
        }
    
    def shutdown(self):
        """Shutdown consumer gracefully"""
        logger.info("Shutting down backend consumer...")
        self.running = False
        
        # Shutdown job processor
        self.job_processor.shutdown()
        
        logger.info("Backend consumer shut down")


# Global backend consumer instance
backend_consumer = BackendConsumer()


async def main():
    """Main entry point for running consumer as standalone process"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Backend Integration Consumer')
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of worker processes (default: 4)'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("=" * 60)
    logger.info("AI Module - Backend Integration Consumer")
    logger.info("=" * 60)
    logger.info(f"Workers: {args.workers}")
    logger.info(f"Log Level: {args.log_level}")
    logger.info("=" * 60)
    
    try:
        await backend_consumer.start(num_workers=args.workers)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    finally:
        backend_consumer.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

