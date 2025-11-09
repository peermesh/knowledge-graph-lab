"""
Mock Data Generator for AI Module Integration.

Generates realistic test data for AI-powered content delivery including user profiles,
dispatch configurations, and content metadata. Used for testing without real AI module.

Constitution Compliance:
- AI-First Research Platform: Mock AI scoring and content analysis
- Test-Driven Development: Support for comprehensive testing
- Scalable Architecture: Configurable mock data generation
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random


class MockDataGenerator:
    """Generate mock data for AI module testing."""

    # Sample user names
    FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ian", "Julia"]
    LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    
    # Sample email domains
    EMAIL_DOMAINS = ["example.com", "test.com", "demo.org", "sample.net", "mock.io"]
    
    # Content topics
    TOPICS = [
        "artificial intelligence",
        "machine learning",
        "data science",
        "blockchain",
        "cryptocurrency",
        "cloud computing",
        "cybersecurity",
        "quantum computing",
        "edge computing",
        "5G networks"
    ]
    
    # Research areas
    RESEARCH_AREAS = [
        "computer vision",
        "natural language processing",
        "reinforcement learning",
        "distributed systems",
        "network security",
        "database optimization",
        "software architecture",
        "DevOps automation"
    ]

    @staticmethod
    def generate_user(user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a mock user with AI preferences.
        
        Returns:
            Dict containing user profile with name, email, dispatch type, frequency,
            and AI metadata (prompts and refined requests).
        """
        first_name = random.choice(MockDataGenerator.FIRST_NAMES)
        last_name = random.choice(MockDataGenerator.LAST_NAMES)
        email_domain = random.choice(MockDataGenerator.EMAIL_DOMAINS)
        
        user = {
            "id": user_id or str(uuid.uuid4()),
            "name": f"{first_name} {last_name}",
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}@{email_domain}",
            "created_at": datetime.utcnow().isoformat(),
            
            # Dispatch Configuration
            "dispatch_type": "email",  # For now, only email as requested
            "dispatch_config": {
                "email": {
                    "format": random.choice(["html", "plain", "both"]),
                    "include_images": random.choice([True, False]),
                    "include_links": True
                }
            },
            
            # Frequency Settings
            "frequency": random.choice(["daily", "weekly", "bi-weekly", "monthly"]),
            "frequency_settings": {
                "type": random.choice(["daily", "weekly", "bi-weekly", "monthly"]),
                "time_of_day": random.choice(["morning", "afternoon", "evening"]),
                "timezone": random.choice(["America/New_York", "America/Los_Angeles", "Europe/London", "Asia/Tokyo"]),
                "preferred_days": random.sample(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], k=random.randint(1, 3))
            },
            
            # AI Module Metadata
            "ai_metadata": {
                # User's original prompts/queries
                "prompts": [
                    f"Find latest research on {random.choice(MockDataGenerator.TOPICS)}",
                    f"Discover trends in {random.choice(MockDataGenerator.RESEARCH_AREAS)}",
                    f"Track developments in {random.choice(MockDataGenerator.TOPICS)} and {random.choice(MockDataGenerator.RESEARCH_AREAS)}"
                ],
                
                # Refined/processed requests from AI module
                "refined_requests": {
                    "topics": random.sample(MockDataGenerator.TOPICS, k=random.randint(2, 4)),
                    "keywords": [
                        f"{random.choice(['advanced', 'emerging', 'innovative', 'cutting-edge'])} {topic}"
                        for topic in random.sample(MockDataGenerator.TOPICS, k=3)
                    ],
                    "research_areas": random.sample(MockDataGenerator.RESEARCH_AREAS, k=random.randint(1, 3)),
                    "content_types": random.sample(["papers", "articles", "news", "tutorials", "videos"], k=random.randint(2, 4)),
                    "relevance_threshold": random.uniform(0.7, 0.95),
                    "novelty_score_min": random.uniform(0.5, 0.8)
                },
                
                # Content preferences learned by AI
                "learned_preferences": {
                    "preferred_sources": random.sample([
                        "arxiv.org",
                        "research.google",
                        "techcrunch.com",
                        "medium.com",
                        "github.com"
                    ], k=random.randint(2, 4)),
                    "reading_level": random.choice(["beginner", "intermediate", "advanced", "expert"]),
                    "content_length": random.choice(["short", "medium", "long", "mixed"]),
                    "engagement_history": {
                        "avg_open_rate": random.uniform(0.4, 0.9),
                        "avg_click_rate": random.uniform(0.2, 0.6),
                        "favorite_topics": random.sample(MockDataGenerator.TOPICS, k=2)
                    }
                },
                
                # Personalization settings
                "personalization": {
                    "enabled": True,
                    "style": random.choice(["concise", "detailed", "balanced"]),
                    "tone": random.choice(["formal", "casual", "technical"]),
                    "summarization": random.choice(["bullet-points", "paragraph", "mixed"]),
                    "ai_scoring_weight": random.uniform(0.6, 1.0)
                }
            }
        }
        
        return user

    @staticmethod
    def generate_users(count: int = 10) -> List[Dict[str, Any]]:
        """Generate multiple mock users."""
        return [MockDataGenerator.generate_user() for _ in range(count)]

    @staticmethod
    def generate_content_item(topic: Optional[str] = None) -> Dict[str, Any]:
        """Generate a mock content item with AI scoring."""
        selected_topic = topic or random.choice(MockDataGenerator.TOPICS)
        
        return {
            "id": str(uuid.uuid4()),
            "title": f"Latest Developments in {selected_topic.title()}",
            "summary": f"Exploring cutting-edge research and applications in {selected_topic}...",
            "url": f"https://example.com/article/{uuid.uuid4()}",
            "source": random.choice(["arxiv.org", "techcrunch.com", "medium.com"]),
            "published_at": (datetime.utcnow() - timedelta(days=random.randint(0, 7))).isoformat(),
            
            # AI-generated scores
            "ai_scores": {
                "relevance": random.uniform(0.7, 1.0),
                "quality": random.uniform(0.6, 1.0),
                "novelty": random.uniform(0.5, 0.9),
                "credibility": random.uniform(0.7, 1.0),
                "engagement_prediction": random.uniform(0.4, 0.9),
                "overall": random.uniform(0.6, 1.0)
            },
            
            # Extracted entities
            "entities": {
                "topics": [selected_topic] + random.sample([t for t in MockDataGenerator.TOPICS if t != selected_topic], k=2),
                "people": [f"Dr. {random.choice(MockDataGenerator.LAST_NAMES)}" for _ in range(random.randint(1, 3))],
                "organizations": random.sample(["MIT", "Stanford", "Google", "OpenAI", "Microsoft"], k=2),
                "technologies": random.sample(["Python", "TensorFlow", "PyTorch", "React", "Docker"], k=3)
            },
            
            "metadata": {
                "word_count": random.randint(500, 3000),
                "reading_time_minutes": random.randint(3, 15),
                "content_type": random.choice(["article", "paper", "tutorial", "news"]),
                "difficulty_level": random.choice(["beginner", "intermediate", "advanced"])
            }
        }

    @staticmethod
    def generate_dispatch_batch(user_count: int = 5, content_per_user: int = 3) -> Dict[str, Any]:
        """
        Generate a complete dispatch batch with users and their personalized content.
        
        Args:
            user_count: Number of users to generate
            content_per_user: Number of content items per user
            
        Returns:
            Dict containing users and their personalized content items
        """
        users = MockDataGenerator.generate_users(user_count)
        
        dispatch_batch = {
            "batch_id": str(uuid.uuid4()),
            "created_at": datetime.utcnow().isoformat(),
            "dispatch_type": "email",
            "total_recipients": user_count,
            "recipients": []
        }
        
        for user in users:
            # Generate personalized content based on user's AI metadata
            user_topics = user["ai_metadata"]["refined_requests"]["topics"]
            content_items = [
                MockDataGenerator.generate_content_item(topic=random.choice(user_topics))
                for _ in range(content_per_user)
            ]
            
            dispatch_batch["recipients"].append({
                "user": user,
                "content": content_items,
                "personalization_applied": {
                    "topic_match_score": random.uniform(0.7, 1.0),
                    "style_applied": user["ai_metadata"]["personalization"]["style"],
                    "tone_applied": user["ai_metadata"]["personalization"]["tone"],
                    "summarization_used": user["ai_metadata"]["personalization"]["summarization"]
                }
            })
        
        return dispatch_batch

    @staticmethod
    def generate_ai_analysis_result(content_text: str) -> Dict[str, Any]:
        """Generate mock AI analysis result for content."""
        return {
            "content_id": str(uuid.uuid4()),
            "analyzed_at": datetime.utcnow().isoformat(),
            "scores": {
                "relevance": random.uniform(0.7, 1.0),
                "quality": random.uniform(0.6, 1.0),
                "novelty": random.uniform(0.5, 0.9),
                "credibility": random.uniform(0.7, 1.0)
            },
            "extracted_entities": {
                "topics": random.sample(MockDataGenerator.TOPICS, k=random.randint(2, 4)),
                "keywords": random.sample(MockDataGenerator.RESEARCH_AREAS, k=random.randint(3, 6)),
            },
            "summary": "AI-generated summary of the content...",
            "sentiment": random.choice(["positive", "neutral", "negative"]),
            "complexity_level": random.choice(["beginner", "intermediate", "advanced", "expert"])
        }


# Convenience functions
def create_mock_user() -> Dict[str, Any]:
    """Create a single mock user."""
    return MockDataGenerator.generate_user()


def create_mock_users(count: int = 10) -> List[Dict[str, Any]]:
    """Create multiple mock users."""
    return MockDataGenerator.generate_users(count)


def create_mock_dispatch_batch(user_count: int = 5, content_per_user: int = 3) -> Dict[str, Any]:
    """Create a complete mock dispatch batch."""
    return MockDataGenerator.generate_dispatch_batch(user_count, content_per_user)


if __name__ == "__main__":
    # Example usage
    print("=== Mock Data Generator Examples ===\n")
    
    # Generate a single user
    user = create_mock_user()
    print("Sample User:")
    print(f"  Name: {user['name']}")
    print(f"  Email: {user['email']}")
    print(f"  Dispatch Type: {user['dispatch_type']}")
    print(f"  Frequency: {user['frequency']}")
    print(f"  Topics: {', '.join(user['ai_metadata']['refined_requests']['topics'])}")
    print()
    
    # Generate a dispatch batch
    batch = create_mock_dispatch_batch(user_count=3, content_per_user=2)
    print(f"Sample Dispatch Batch: {batch['batch_id']}")
    print(f"  Recipients: {batch['total_recipients']}")
    print(f"  First recipient: {batch['recipients'][0]['user']['name']}")
    print(f"  Content items for first recipient: {len(batch['recipients'][0]['content'])}")


