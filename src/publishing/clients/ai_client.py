"""
AI Module client for Publishing Module.

Integrates with the AI module for content quality scoring, relevance analysis,
and personalization recommendations. Follows async patterns for scalability.

Constitution Compliance:
- AI-First Research Platform: Core integration for content analysis and personalization
- Technology Standards: OpenAI-compatible API integration
- Performance: Optimized for high-volume content processing
"""

import asyncio
from typing import Dict, Any, List, Optional
import structlog
import httpx
from httpx import Timeout, Response
import json

from ..core.config import settings
from ..core.logging import log_ai_integration


class AIClient:
    """Async client for AI module integration."""

    def __init__(self):
        """Initialize AI client with configuration."""
        self.logger = structlog.get_logger(__name__)
        self.base_url = settings.AI_MODULE_URL.rstrip("/")
        self.api_key = settings.AI_API_KEY
        self.timeout = Timeout(30.0, connect=10.0)  # 30s total, 10s connect

        # Headers for API requests
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": f"PublishingModule/{settings.VERSION}"
        }

        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    async def health_check(self) -> bool:
        """Check AI module health status."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/health")

                if response.status_code == 200:
                    self.logger.info("AI module health check passed")
                    return True
                else:
                    self.logger.warning(
                        "AI module health check failed",
                        status_code=response.status_code,
                        response=response.text
                    )
                    return False

        except Exception as e:
            self.logger.error("AI module health check error", error=str(e))
            return False

    async def analyze_content_quality(self, content_id: str, content_text: str) -> Optional[float]:
        """Analyze content quality and return score (0.0-1.0)."""
        correlation_id = str(asyncio.current_task().get_coro_stack()[-1] if asyncio.current_task() else "unknown")

        try:
            payload = {
                "content_id": content_id,
                "content_text": content_text,
                "analysis_type": "quality_scoring"
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/analyze/quality",
                    json=payload,
                    headers=self.headers
                )

                if response.status_code == 200:
                    result = response.json()
                    score = result.get("quality_score", 0.0)

                    log_ai_integration(
                        correlation_id=correlation_id,
                        operation="content_quality_analysis",
                        content_id=content_id,
                        success=True,
                        score=score
                    )

                    self.logger.info(
                        "Content quality analysis completed",
                        content_id=content_id,
                        score=score,
                        correlation_id=correlation_id
                    )

                    return score
                else:
                    log_ai_integration(
                        correlation_id=correlation_id,
                        operation="content_quality_analysis",
                        content_id=content_id,
                        success=False,
                        error=f"HTTP {response.status_code}"
                    )

                    self.logger.error(
                        "Content quality analysis failed",
                        content_id=content_id,
                        status_code=response.status_code,
                        response=response.text
                    )
                    return None

        except httpx.TimeoutException:
            log_ai_integration(
                correlation_id=correlation_id,
                operation="content_quality_analysis",
                content_id=content_id,
                success=False,
                error="Request timeout"
            )
            self.logger.error("AI module timeout for quality analysis", content_id=content_id)
            return None

        except Exception as e:
            log_ai_integration(
                correlation_id=correlation_id,
                operation="content_quality_analysis",
                content_id=content_id,
                success=False,
                error=str(e)
            )
            self.logger.error("AI module error for quality analysis", content_id=content_id, error=str(e))
            return None

    async def analyze_content_relevance(self, content_id: str, content_text: str, user_interests: Dict[str, float]) -> Optional[float]:
        """Analyze content relevance for specific user interests."""
        correlation_id = str(asyncio.current_task().get_coro_stack()[-1] if asyncio.current_task() else "unknown")

        try:
            payload = {
                "content_id": content_id,
                "content_text": content_text,
                "user_interests": user_interests,
                "analysis_type": "relevance_scoring"
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/analyze/relevance",
                    json=payload,
                    headers=self.headers
                )

                if response.status_code == 200:
                    result = response.json()
                    score = result.get("relevance_score", 0.0)

                    log_ai_integration(
                        correlation_id=correlation_id,
                        operation="content_relevance_analysis",
                        content_id=content_id,
                        success=True,
                        score=score
                    )

                    self.logger.info(
                        "Content relevance analysis completed",
                        content_id=content_id,
                        score=score,
                        user_interests=list(user_interests.keys()),
                        correlation_id=correlation_id
                    )

                    return score
                else:
                    log_ai_integration(
                        correlation_id=correlation_id,
                        operation="content_relevance_analysis",
                        content_id=content_id,
                        success=False,
                        error=f"HTTP {response.status_code}"
                    )

                    self.logger.error(
                        "Content relevance analysis failed",
                        content_id=content_id,
                        status_code=response.status_code
                    )
                    return None

        except Exception as e:
            log_ai_integration(
                correlation_id=correlation_id,
                operation="content_relevance_analysis",
                content_id=content_id,
                success=False,
                error=str(e)
            )
            self.logger.error("AI module error for relevance analysis", content_id=content_id, error=str(e))
            return None

    async def get_content_topics(self, content_id: str, content_text: str) -> Optional[List[str]]:
        """Extract topics from content for categorization."""
        correlation_id = str(asyncio.current_task().get_coro_stack()[-1] if asyncio.current_task() else "unknown")

        try:
            payload = {
                "content_id": content_id,
                "content_text": content_text,
                "analysis_type": "topic_extraction"
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/analyze/topics",
                    json=payload,
                    headers=self.headers
                )

                if response.status_code == 200:
                    result = response.json()
                    topics = result.get("topics", [])

                    log_ai_integration(
                        correlation_id=correlation_id,
                        operation="topic_extraction",
                        content_id=content_id,
                        success=True
                    )

                    self.logger.info(
                        "Topic extraction completed",
                        content_id=content_id,
                        topics=topics,
                        correlation_id=correlation_id
                    )

                    return topics
                else:
                    log_ai_integration(
                        correlation_id=correlation_id,
                        operation="topic_extraction",
                        content_id=content_id,
                        success=False,
                        error=f"HTTP {response.status_code}"
                    )
                    return None

        except Exception as e:
            log_ai_integration(
                correlation_id=correlation_id,
                operation="topic_extraction",
                content_id=content_id,
                success=False,
                error=str(e)
            )
            self.logger.error("AI module error for topic extraction", content_id=content_id, error=str(e))
            return None

    async def personalize_content(self, content_id: str, user_profile: Dict[str, Any], available_content: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Get personalized content recommendations for a user."""
        correlation_id = str(asyncio.current_task().get_coro_stack()[-1] if asyncio.current_task() else "unknown")

        try:
            payload = {
                "content_id": content_id,
                "user_profile": user_profile,
                "available_content": available_content,
                "analysis_type": "personalization"
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/personalize",
                    json=payload,
                    headers=self.headers
                )

                if response.status_code == 200:
                    result = response.json()

                    log_ai_integration(
                        correlation_id=correlation_id,
                        operation="content_personalization",
                        content_id=content_id,
                        success=True
                    )

                    self.logger.info(
                        "Content personalization completed",
                        content_id=content_id,
                        recommendations_count=len(result.get("recommendations", [])),
                        correlation_id=correlation_id
                    )

                    return result
                else:
                    log_ai_integration(
                        correlation_id=correlation_id,
                        operation="content_personalization",
                        content_id=content_id,
                        success=False,
                        error=f"HTTP {response.status_code}"
                    )
                    return None

        except Exception as e:
            log_ai_integration(
                correlation_id=correlation_id,
                operation="content_personalization",
                content_id=content_id,
                success=False,
                error=str(e)
            )
            self.logger.error("AI module error for personalization", content_id=content_id, error=str(e))
            return None

    async def batch_analyze_content(self, content_batch: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Analyze multiple content items in batch for efficiency."""
        correlation_id = str(asyncio.current_task().get_coro_stack()[-1] if asyncio.current_task() else "unknown")

        try:
            payload = {
                "content_batch": content_batch,
                "analysis_type": "batch_quality_relevance"
            }

            async with httpx.AsyncClient(timeout=Timeout(60.0, connect=10.0)) as client:
                response = await client.post(
                    f"{self.base_url}/analyze/batch",
                    json=payload,
                    headers=self.headers
                )

                if response.status_code == 200:
                    result = response.json()
                    analyses = result.get("analyses", [])

                    log_ai_integration(
                        correlation_id=correlation_id,
                        operation="batch_content_analysis",
                        content_id="batch",
                        success=True
                    )

                    self.logger.info(
                        "Batch content analysis completed",
                        batch_size=len(content_batch),
                        results_count=len(analyses),
                        correlation_id=correlation_id
                    )

                    return analyses
                else:
                    log_ai_integration(
                        correlation_id=correlation_id,
                        operation="batch_content_analysis",
                        content_id="batch",
                        success=False,
                        error=f"HTTP {response.status_code}"
                    )
                    return []

        except Exception as e:
            log_ai_integration(
                correlation_id=correlation_id,
                operation="batch_content_analysis",
                content_id="batch",
                success=False,
                error=str(e)
            )
            self.logger.error("AI module error for batch analysis", error=str(e))
            return []

    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about available AI models and capabilities."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/models", headers=self.headers)

                if response.status_code == 200:
                    return response.json()
                else:
                    return {"status": "error", "message": f"HTTP {response.status_code}"}

        except Exception as e:
            self.logger.error("Failed to get AI model info", error=str(e))
            return {"status": "error", "message": str(e)}

