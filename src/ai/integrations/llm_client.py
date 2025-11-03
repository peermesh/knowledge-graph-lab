"""LLM client wrapper using LangChain with fallback providers"""

from typing import List, Dict, Any, Optional
import logging

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
        """Initialize LLM clients with primary and fallback providers"""
        if not OPENAI_AVAILABLE or not settings.openai_api_key:
            logger.warning("OpenAI client not available or API key not set - install langchain-openai and set OPENAI_API_KEY")
            self.primary_client = None
        else:
            self.primary_client = self._create_openai_client()
        
        if ANTHROPIC_AVAILABLE and settings.anthropic_api_key:
            self.fallback_client = self._create_anthropic_client()
        else:
            self.fallback_client = None
        
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
        if not self.primary_client and not self.fallback_client:
            logger.error("No LLM clients available - please install dependencies")
            return {"entities": [], "relationships": []}
        
        try:
            # Try primary client (OpenAI)
            if self.primary_client:
                logger.info(f"Extracting entities using OpenAI GPT-4")
                response = await self.primary_client.ainvoke(prompt)
                return self._parse_extraction_response(response.content)
            elif self.fallback_client:
                logger.info(f"Using fallback LLM (primary not available)")
                response = await self.fallback_client.ainvoke(prompt)
                return self._parse_extraction_response(response.content)
            else:
                return {"entities": [], "relationships": []}
        except Exception as e:
            logger.warning(f"Primary LLM failed: {e}, trying fallback")
            
            if self.fallback_client:
                try:
                    # Try fallback client (Claude)
                    logger.info(f"Extracting entities using Claude")
                    response = await self.fallback_client.ainvoke(prompt)
                    return self._parse_extraction_response(response.content)
                except Exception as fallback_error:
                    logger.error(f"Fallback LLM also failed: {fallback_error}")
                    raise
            else:
                raise
    
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
        """Parse LLM response into structured format"""
        import json
        
        try:
            # Try to parse as JSON
            data = json.loads(response)
            return data
        except json.JSONDecodeError:
            # If not valid JSON, try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    return data
                except:
                    pass
            
            # Return empty result if parsing fails
            logger.error(f"Failed to parse LLM response: {response[:200]}")
            return {"entities": [], "relationships": []}


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

