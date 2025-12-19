#!/usr/bin/env python3
"""
Initialize Mock Data Script

Loads mock data into the publishing module for testing and demo purposes.
Creates realistic users, subscriptions, and content with AI metadata.

Usage:
    python scripts/init_mock_data.py [--subscribers N] [--content N]
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.publishing.services.mock_data_loader import MockDataLoader
from src.publishing.core.logging import setup_logging
import structlog


async def main(subscribers: int = 10, content: int = 20):
    """Load mock data into the system."""
    # Setup logging
    setup_logging()
    logger = structlog.get_logger(__name__)
    
    logger.info(
        "Starting mock data initialization",
        subscribers=subscribers,
        content=content
    )
    
    try:
        loader = MockDataLoader()
        
        # Initialize demo environment
        result = await loader.initialize_demo_environment()
        
        logger.info(
            "Mock data initialization complete",
            subscribers_loaded=len(result["subscribers"]),
            content_loaded=result["content_count"],
            sample_batch_id=result["sample_batch"]["batch_id"]
        )
        
        print("\n✅ Mock data loaded successfully!")
        print(f"  • Subscribers: {len(result['subscribers'])}")
        print(f"  • Content items: {result['content_count']}")
        print(f"  • Sample batch: {result['sample_batch']['batch_id']}")
        print("\nSample subscriber emails:")
        for sub in result["subscribers"][:5]:
            print(f"  - {sub['email']} ({sub['frequency']})")
        
        return 0
        
    except Exception as e:
        logger.error("Mock data initialization failed", error=str(e))
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize mock data for publishing module")
    parser.add_argument(
        "--subscribers",
        type=int,
        default=10,
        help="Number of mock subscribers to create (default: 10)"
    )
    parser.add_argument(
        "--content",
        type=int,
        default=20,
        help="Number of mock content items to create (default: 20)"
    )
    
    args = parser.parse_args()
    
    exit_code = asyncio.run(main(subscribers=args.subscribers, content=args.content))
    sys.exit(exit_code)


