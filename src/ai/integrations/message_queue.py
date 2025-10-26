"""RabbitMQ message queue client for job processing"""

import pika
import json
import logging
from typing import Dict, Any, Callable, Optional
import asyncio
from datetime import datetime

from src.ai.config import settings

logger = logging.getLogger(__name__)


class MessageQueue:
    """RabbitMQ client for async job processing"""
    
    # Queue names by priority
    HIGH_PRIORITY_QUEUE = "ai.jobs.high"
    NORMAL_PRIORITY_QUEUE = "ai.jobs.normal"
    LOW_PRIORITY_QUEUE = "ai.jobs.low"
    RESULTS_QUEUE = "ai.results"
    ERROR_QUEUE = "ai.errors"
    
    def __init__(self):
        """Initialize message queue connection"""
        self.connection = None
        self.channel = None
        self._connect()
    
    def _connect(self):
        """Establish connection to RabbitMQ"""
        try:
            params = pika.URLParameters(settings.rabbitmq_url)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            
            # Declare queues
            self._declare_queues()
            
            logger.info("Connected to RabbitMQ")
        
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def _declare_queues(self):
        """Declare all queues with appropriate settings"""
        # Priority queues for job processing
        for queue_name in [self.HIGH_PRIORITY_QUEUE, self.NORMAL_PRIORITY_QUEUE, self.LOW_PRIORITY_QUEUE]:
            self.channel.queue_declare(
                queue=queue_name,
                durable=True,  # Survive broker restart
                arguments={
                    'x-message-ttl': 3600000,  # 1 hour TTL
                    'x-max-length': 10000  # Max queue size
                }
            )
        
        # Results and error queues
        for queue_name in [self.RESULTS_QUEUE, self.ERROR_QUEUE]:
            self.channel.queue_declare(
                queue=queue_name,
                durable=True
            )
        
        logger.info("Declared all message queues")
    
    def publish_job(
        self,
        job_data: Dict[str, Any],
        priority: str = "normal"
    ) -> bool:
        """
        Publish a job to the appropriate priority queue.
        
        Args:
            job_data: Job information (document_id, content, config, etc.)
            priority: Priority level (high, normal, low)
        
        Returns:
            True if published successfully
        """
        try:
            # Select queue based on priority
            queue_map = {
                'high': self.HIGH_PRIORITY_QUEUE,
                'normal': self.NORMAL_PRIORITY_QUEUE,
                'low': self.LOW_PRIORITY_QUEUE
            }
            
            queue_name = queue_map.get(priority, self.NORMAL_PRIORITY_QUEUE)
            
            # Add metadata
            message = {
                'job_id': job_data.get('job_id'),
                'document_id': job_data.get('document_id'),
                'content': job_data.get('content'),
                'config': job_data.get('config', {}),
                'priority': priority,
                'created_at': datetime.utcnow().isoformat(),
                'retry_count': job_data.get('retry_count', 0)
            }
            
            # Publish message
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Persistent message
                    content_type='application/json'
                )
            )
            
            logger.info(f"Published job {message['job_id']} to {queue_name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to publish job: {e}")
            return False
    
    def publish_result(
        self,
        job_id: str,
        result_data: Dict[str, Any]
    ) -> bool:
        """
        Publish job results to results queue.
        
        Args:
            job_id: Job identifier
            result_data: Processing results
        
        Returns:
            True if published successfully
        """
        try:
            message = {
                'job_id': job_id,
                'status': 'completed',
                'result': result_data,
                'completed_at': datetime.utcnow().isoformat()
            }
            
            self.channel.basic_publish(
                exchange='',
                routing_key=self.RESULTS_QUEUE,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
            
            logger.info(f"Published results for job {job_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to publish results: {e}")
            return False
    
    def publish_error(
        self,
        job_id: str,
        error_message: str,
        retry_count: int = 0
    ) -> bool:
        """
        Publish job error to error queue.
        
        Args:
            job_id: Job identifier
            error_message: Error details
            retry_count: Number of retries attempted
        
        Returns:
            True if published successfully
        """
        try:
            message = {
                'job_id': job_id,
                'status': 'failed',
                'error': error_message,
                'retry_count': retry_count,
                'failed_at': datetime.utcnow().isoformat()
            }
            
            self.channel.basic_publish(
                exchange='',
                routing_key=self.ERROR_QUEUE,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
            
            logger.warning(f"Published error for job {job_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to publish error: {e}")
            return False
    
    def consume_jobs(
        self,
        callback: Callable,
        priority: str = "normal",
        prefetch_count: int = 1
    ):
        """
        Start consuming jobs from queue.
        
        Args:
            callback: Function to process jobs (should be async)
            priority: Priority queue to consume from
            prefetch_count: Number of messages to prefetch
        """
        queue_map = {
            'high': self.HIGH_PRIORITY_QUEUE,
            'normal': self.NORMAL_PRIORITY_QUEUE,
            'low': self.LOW_PRIORITY_QUEUE
        }
        
        queue_name = queue_map.get(priority, self.NORMAL_PRIORITY_QUEUE)
        
        # Set QoS
        self.channel.basic_qos(prefetch_count=prefetch_count)
        
        # Start consuming
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=self._create_callback_wrapper(callback),
            auto_ack=False
        )
        
        logger.info(f"Started consuming from {queue_name}")
        self.channel.start_consuming()
    
    def _create_callback_wrapper(self, async_callback: Callable):
        """Wrap async callback for pika's sync interface"""
        def callback_wrapper(ch, method, properties, body):
            try:
                # Parse message
                message = json.loads(body)
                
                # Run async callback
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(async_callback(message))
                loop.close()
                
                # Acknowledge message
                ch.basic_ack(delivery_tag=method.delivery_tag)
            
            except Exception as e:
                logger.error(f"Message processing failed: {e}")
                # Reject and requeue message
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        return callback_wrapper
    
    def close(self):
        """Close connection to RabbitMQ"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("Closed RabbitMQ connection")


# Global message queue client
message_queue = MessageQueue()

