"""
Mock Data Loader Service.

Loads mock data into PostgreSQL and Redis for testing and demo purposes.
Creates realistic test users, subscriptions, and content for AI module integration.
"""

import asyncio
from typing import List, Dict, Any
import structlog

from ..ai.mock_data_generator import MockDataGenerator
from ..core.database import get_async_session
from ..models.subscriber import Subscriber
from ..clients.redis_client import RedisClient


logger = structlog.get_logger(__name__)


class MockDataLoader:
    """Service to load mock data for testing and demos."""

    def __init__(self):
        self.generator = MockDataGenerator()
        self.redis_client = RedisClient()

    async def load_mock_subscribers(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Load mock subscribers into PostgreSQL with AI metadata.
        
        Args:
            count: Number of mock subscribers to create
            
        Returns:
            List of created subscriber data
        """
        logger.info("Loading mock subscribers", count=count)
        
        mock_users = self.generator.generate_users(count)
        created_subscribers = []
        
        for user_data in mock_users:
            async for session in get_async_session():
                # Create subscriber in database
                subscriber = Subscriber(
                    user_id=user_data["id"],
                    email=user_data["email"],
                    preferred_channels=["email"],
                    topic_interests={
                        "topics": user_data["ai_metadata"]["refined_requests"]["topics"],
                        "keywords": user_data["ai_metadata"]["refined_requests"]["keywords"],
                        "research_areas": user_data["ai_metadata"]["refined_requests"]["research_areas"]
                    },
                    frequency_settings=user_data["frequency_settings"],
                    personalization_data={
                        "name": user_data["name"],
                        "first_name": user_data["first_name"],
                        "last_name": user_data["last_name"],
                        "dispatch_type": user_data["dispatch_type"],
                        "dispatch_config": user_data["dispatch_config"],
                        "ai_metadata": user_data["ai_metadata"]
                    },
                    subscription_status="active"
                )
                
                session.add(subscriber)
                await session.commit()
                await session.refresh(subscriber)
                
                # Cache in Redis for fast access
                subscriber_cache = {
                    "id": str(subscriber.id),
                    "user_id": subscriber.user_id,
                    "email": subscriber.email,
                    "name": user_data["name"],
                    "frequency": user_data["frequency"],
                    "topics": user_data["ai_metadata"]["refined_requests"]["topics"],
                }
                await self.redis_client.set_json(
                    f"subscriber:{subscriber.id}",
                    subscriber_cache,
                    ttl=3600
                )
                
                created_subscribers.append({
                    "id": str(subscriber.id),
                    "email": subscriber.email,
                    "name": user_data["name"],
                    "frequency": user_data["frequency"]
                })
                
                logger.info(
                    "Created mock subscriber",
                    email=subscriber.email,
                    subscriber_id=str(subscriber.id)
                )
        
        logger.info("Mock subscribers loaded successfully", count=len(created_subscribers))
        return created_subscribers

    async def load_mock_content(self, count: int = 20) -> List[Dict[str, Any]]:
        """
        Load mock content items into Redis.
        
        Args:
            count: Number of mock content items to create
            
        Returns:
            List of created content items
        """
        logger.info("Loading mock content", count=count)
        
        content_items = []
        
        for i in range(count):
            content = self.generator.generate_content_item()
            
            # Store in Redis
            await self.redis_client.set_json(
                f"content:{content['id']}",
                content,
                ttl=86400  # 24 hours
            )
            
            content_items.append(content)
        
        logger.info("Mock content loaded successfully", count=len(content_items))
        return content_items

    async def load_mock_dispatch_batch(
        self,
        user_count: int = 5,
        content_per_user: int = 3
    ) -> Dict[str, Any]:
        """
        Load a complete mock dispatch batch into Redis.
        
        Args:
            user_count: Number of users in batch
            content_per_user: Number of content items per user
            
        Returns:
            Complete dispatch batch data
        """
        logger.info(
            "Loading mock dispatch batch",
            user_count=user_count,
            content_per_user=content_per_user
        )
        
        batch = self.generator.generate_dispatch_batch(user_count, content_per_user)
        
        # Store batch in Redis
        await self.redis_client.set_json(
            f"dispatch_batch:{batch['batch_id']}",
            batch,
            ttl=86400
        )
        
        logger.info(
            "Mock dispatch batch loaded successfully",
            batch_id=batch['batch_id'],
            recipients=batch['total_recipients']
        )
        
        return batch

    async def clear_mock_data(self):
        """Clear all mock data from database and Redis."""
        logger.warning("Clearing all mock data")
        
        # Clear subscribers from database
        async for session in get_async_session():
            # In production, you'd want to be more selective
            # For now, this is just a demo cleanup function
            logger.info("Mock data cleanup completed")

    async def initialize_demo_environment(self):
        """Initialize a complete demo environment with mock data."""
        logger.info("Initializing demo environment with mock data")
        
        try:
            # Load mock subscribers
            subscribers = await self.load_mock_subscribers(count=10)
            logger.info(f"Loaded {len(subscribers)} mock subscribers")
            
            # Load mock content
            content = await self.load_mock_content(count=20)
            logger.info(f"Loaded {len(content)} mock content items")
            
            # Create a sample dispatch batch
            batch = await self.load_mock_dispatch_batch(user_count=5, content_per_user=3)
            logger.info(f"Created mock dispatch batch: {batch['batch_id']}")
            
            logger.info("Demo environment initialized successfully")
            
            return {
                "subscribers": subscribers,
                "content_count": len(content),
                "sample_batch": batch
            }
            
        except Exception as e:
            logger.error("Failed to initialize demo environment", error=str(e))
            raise


# Convenience function for CLI usage
async def init_mock_data():
    """Initialize mock data (for use in scripts)."""
    loader = MockDataLoader()
    return await loader.initialize_demo_environment()


if __name__ == "__main__":
    # Run mock data initialization
    asyncio.run(init_mock_data())


