"""LLM client wrapper using LangChain with fallback providers"""

from typing import List, Dict, Any, Optional
import logging
import httpx
import json

from src.ai.config import settings

logger = logging.getLogger(__name__)

# Optional imports - gracefully handle missing dependencies
try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    logger.warning("langchain_openai not installed - OpenAI features will be limited")
    OPENAI_AVAILABLE = False
    ChatOpenAI = None

try:
    from langchain_anthropic import ChatAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    logger.info("langchain_anthropic not installed - Claude fallback disabled")
    ANTHROPIC_AVAILABLE = False
    ChatAnthropic = None


class LLMClient:
    """Manages LLM interactions with fallback support"""
    
    def __init__(self):
        """Initialize LLM clients with primary (Perplexity) and fallback providers"""
        # Primary: Perplexity
        if settings.perplexity_api_key:
            self.primary_client = "perplexity"
            logger.info("Perplexity configured as primary LLM provider")
        else:
            self.primary_client = None
            logger.warning("Perplexity API key not set - set PERPLEXITY_API_KEY environment variable")
        
        # Fallback: OpenAI
        if OPENAI_AVAILABLE and settings.openai_api_key:
            self.fallback_client = self._create_openai_client()
        else:
            self.fallback_client = None
        
        # Fallback: Anthropic Claude
        if ANTHROPIC_AVAILABLE and settings.anthropic_api_key:
            self.claude_fallback = self._create_anthropic_client()
        else:
            self.claude_fallback = None
        
    def _create_openai_client(self):
        """Create OpenAI client"""
        if not OPENAI_AVAILABLE or not settings.openai_api_key:
            return None
        
        try:
            return ChatOpenAI(
                model="gpt-4",
                temperature=0.1,
                api_key=settings.openai_api_key,
                timeout=30,
                max_retries=3
            )
        except Exception as e:
            logger.error(f"Failed to create OpenAI client: {e}")
            return None
    
    def _create_anthropic_client(self):
        """Create Anthropic Claude client as fallback"""
        if not ANTHROPIC_AVAILABLE or not settings.anthropic_api_key:
            return None
        
        try:
            return ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                temperature=0.1,
                api_key=settings.anthropic_api_key,
                timeout=30,
                max_retries=3
            )
        except Exception as e:
            logger.error(f"Failed to create Anthropic client: {e}")
            return None
    
    async def extract_entities(
        self,
        text: str,
        entity_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Extract entities from text using LLM

        Args:
            text: Document text to process
            entity_types: List of entity types to extract (None for all types)

        Returns:
            Dictionary with extracted entities and relationships
        """
        prompt = self._build_extraction_prompt(text, entity_types)
        
        # Check if LLM clients are available
        if not self.primary_client and not self.fallback_client and not self.claude_fallback:
            logger.error("No LLM clients available - please set API keys")
            return {"entities": [], "relationships": []}
        
        try:
            # Try primary client (Perplexity)
            if self.primary_client == "perplexity":
                logger.info("Extracting entities using Perplexity")
                response_text = await self._call_perplexity_api(prompt)
                return self._parse_extraction_response(response_text)
            elif self.fallback_client:
                logger.info("Using OpenAI fallback (Perplexity not available)")
                response = await self.fallback_client.ainvoke(prompt)
                return self._parse_extraction_response(response.content)
            elif self.claude_fallback:
                logger.info("Using Claude fallback")
                response = await self.claude_fallback.ainvoke(prompt)
                return self._parse_extraction_response(response.content)
            else:
                return {"entities": [], "relationships": []}
        except Exception as e:
            logger.warning(f"Primary LLM failed: {e}, trying fallback")
            
            # Try OpenAI fallback
            if self.fallback_client:
                try:
                    logger.info("Extracting entities using OpenAI fallback")
                    response = await self.fallback_client.ainvoke(prompt)
                    return self._parse_extraction_response(response.content)
                except Exception as fallback_error:
                    logger.warning(f"OpenAI fallback failed: {fallback_error}")
            
            # Try Claude fallback
            if self.claude_fallback:
                try:
                    logger.info("Extracting entities using Claude fallback")
                    response = await self.claude_fallback.ainvoke(prompt)
                    return self._parse_extraction_response(response.content)
                except Exception as fallback_error:
                    logger.error(f"All LLM providers failed. Last error: {fallback_error}")
                    raise
            else:
                raise
    
    async def _call_perplexity_api(self, prompt: str) -> str:
        """Call Perplexity API for entity extraction"""
        if not settings.perplexity_api_key:
            raise ValueError("Perplexity API key not configured")
        
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.perplexity_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-sonar-large-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert at extracting entities and relationships from text. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 4000
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Extract content from Perplexity response
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise ValueError(f"Unexpected Perplexity API response: {result}")
    
    def _build_extraction_prompt(
        self,
        text: str,
        entity_types: Optional[List[str]] = None
    ) -> str:
        """Build prompt for flexible entity extraction"""
        if entity_types:
            entity_types_str = ", ".join(entity_types)
            entity_instruction = f"Focus on these entity types: {entity_types_str}"
        else:
            entity_instruction = "Extract all relevant entity types you can identify"

        return f"""Extract entities and relationships from the following text.

{entity_instruction}

For each entity, provide:
1. The entity text
2. Entity type (use any relevant type you identify)
3. Confidence score (0.0-1.0)
4. Positions in text (start and end character indices)

For relationships between entities, provide:
1. Source entity
2. Target entity
3. Relationship type (use any relevant relationship type you identify)
4. Confidence score (0.0-1.0)
5. Evidence text

Text to analyze:
{text}

Return the results in JSON format with 'entities' and 'relationships' arrays."""
    
    def _parse_extraction_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured format and normalize keys"""
        import re

        data: Dict[str, Any] = {"entities": [], "relationships": []}

        try:
            data = json.loads(response)
        except json.JSONDecodeError:
            # If not valid JSON, try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                except Exception:
                    logger.error(f"Failed to parse LLM response: {response[:200]}")
                    return {"entities": [], "relationships": []}
            else:
                logger.error(f"Failed to parse LLM response: {response[:200]}")
                return {"entities": [], "relationships": []}

        return self._normalize_extraction_payload(data)

    def _normalize_extraction_payload(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize LLM payload keys to match downstream expectations."""

        def normalize_positions(raw_positions: Any) -> List[List[int]]:
            positions: List[List[int]] = []
            if isinstance(raw_positions, list):
                if all(isinstance(item, (int, float)) for item in raw_positions):
                    # List of bare indices -> assume pairs
                    it = iter(raw_positions)
                    for start in it:
                        end = next(it, start)
                        positions.append([int(start), int(end)])
                else:
                    for item in raw_positions:
                        if isinstance(item, dict):
                            start = item.get("start") or item.get("begin")
                            end = item.get("end") or item.get("finish")
                            if start is not None and end is not None:
                                positions.append([int(start), int(end)])
                        elif isinstance(item, (list, tuple)) and len(item) == 2:
                            positions.append([int(item[0]), int(item[1])])
                        elif isinstance(item, (int, float)):
                            # Single index provided – we can't infer span length, skip.
                            continue
            return positions

        normalized_entities: List[Dict[str, Any]] = []
        for entity in data.get("entities", []) or []:
            text = (
                entity.get("text")
                or entity.get("entity_text")
                or entity.get("name")
                or entity.get("value")
            )
            entity_type = entity.get("type") or entity.get("entity_type")
            confidence = (
                entity.get("confidence")
                if entity.get("confidence") is not None
                else entity.get("confidence_score")
            )
            positions = entity.get("positions") or entity.get("positions_in_text") or []

            normalized_entities.append(
                {
                    "text": text or "",
                    "type": (entity_type or "").lower(),
                    "confidence": float(confidence) if confidence is not None else 0.5,
                    "positions": normalize_positions(positions),
                    "metadata": entity.get("metadata", {}),
                }
            )

        normalized_relationships: List[Dict[str, Any]] = []
        for relationship in data.get("relationships", []) or []:
            source = (
                relationship.get("source_entity")
                or relationship.get("source")
                or relationship.get("subject")
                or relationship.get("from")
            )
            target = (
                relationship.get("target_entity")
                or relationship.get("target")
                or relationship.get("object")
                or relationship.get("to")
            )
            rel_type = (
                relationship.get("relationship_type")
                or relationship.get("type")
                or relationship.get("relation")
            )
            confidence = (
                relationship.get("confidence")
                if relationship.get("confidence") is not None
                else relationship.get("confidence_score")
            )
            evidence = (
                relationship.get("evidence")
                or relationship.get("evidence_text")
                or relationship.get("description")
            )

            normalized_relationships.append(
                {
                    "source_entity": source or "",
                    "target_entity": target or "",
                    "relationship_type": (rel_type or "").lower(),
                    "confidence": float(confidence) if confidence is not None else 0.5,
                    "evidence": evidence or "",
                    "metadata": relationship.get("metadata", {}),
                }
            )

        return {
            "entities": normalized_entities,
            "relationships": normalized_relationships,
        }


# Global LLM client instance (lazy-loaded to avoid startup errors)
_llm_client_instance = None

def _get_llm_client_instance():
    """Get or create the global LLM client instance"""
    global _llm_client_instance
    if _llm_client_instance is None:
        _llm_client_instance = LLMClient()
    return _llm_client_instance

# Create a lazy-loaded wrapper class
class LazyLLMClient:
    """Lazy-loaded wrapper for LLMClient to avoid import-time initialization errors"""
    
    def __init__(self):
        self._client = None
    
    def __getattr__(self, name):
        if self._client is None:
            try:
                self._client = LLMClient()
            except Exception as e:
                logger.warning(f"Failed to initialize LLM client: {e}. Some features may be unavailable.")
                # Return a dummy object that handles method calls gracefully
                class DummyClient:
                    async def extract_entities(self, *args, **kwargs):
                        logger.error("LLM client not available")
                        return {"entities": [], "relationships": []}
                    async def generate_embeddings(self, *args, **kwargs):
                        logger.error("LLM client not available")
                        return []
                self._client = DummyClient()
        return getattr(self._client, name)

# Create lazy-loaded instance
llm_client = LazyLLMClient()

