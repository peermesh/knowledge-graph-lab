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
        
        return ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            api_key=settings.openai_api_key,
            timeout=30,
            max_retries=3
        )
    
    def _create_anthropic_client(self):
        """Create Anthropic Claude client as fallback"""
        if not ANTHROPIC_AVAILABLE or not settings.anthropic_api_key:
            return None
        
        return ChatAnthropic(
            model="claude-3-opus-20240229",
            temperature=0.1,
            api_key=settings.anthropic_api_key,
            timeout=30,
            max_retries=3
        )
    
    async def extract_entities(
        self,
        text: str,
        entity_types: List[str],
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Extract entities from text using LLM
        
        Args:
            text: Document text to process
            entity_types: List of entity types to extract
            language: Language code (en, es, fr, zh)
            
        Returns:
            Dictionary with extracted entities and relationships
        """
        prompt = self._build_extraction_prompt(text, entity_types, language)
        
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
        entity_types: List[str],
        language: str
    ) -> str:
        """Build prompt for entity extraction with language-specific templates"""
        entity_types_str = ", ".join(entity_types)
        
        # Language-specific prompts
        prompts = {
            'en': self._build_english_prompt(text, entity_types_str),
            'es': self._build_spanish_prompt(text, entity_types_str),
            'fr': self._build_french_prompt(text, entity_types_str),
            'zh': self._build_chinese_prompt(text, entity_types_str)
        }
        
        return prompts.get(language, prompts['en'])
    
    def _build_english_prompt(self, text: str, entity_types: str) -> str:
        """English extraction prompt"""
        return f"""Extract entities and relationships from the following text.

Entity types to extract: {entity_types}
Language: English

For each entity, provide:
1. The entity text
2. Entity type (organization, person, funding_amount, date, location)
3. Confidence score (0.0-1.0)
4. Positions in text (start and end character indices)

For relationships between entities, provide:
1. Source entity
2. Target entity  
3. Relationship type (fund, partner, acquire, compete, collaborate, mention)
4. Confidence score (0.0-1.0)
5. Evidence text

Text to analyze:
{text}

Return the results in JSON format with 'entities' and 'relationships' arrays."""
    
    def _build_spanish_prompt(self, text: str, entity_types: str) -> str:
        """Spanish extraction prompt"""
        return f"""Extrae entidades y relaciones del siguiente texto.

Tipos de entidades a extraer: {entity_types}
Idioma: Español

Para cada entidad, proporciona:
1. El texto de la entidad
2. Tipo de entidad (organization, person, funding_amount, date, location)
3. Puntuación de confianza (0.0-1.0)
4. Posiciones en el texto (índices de inicio y fin)

Para las relaciones entre entidades, proporciona:
1. Entidad fuente
2. Entidad destino
3. Tipo de relación (fund, partner, acquire, compete, collaborate, mention)
4. Puntuación de confianza (0.0-1.0)
5. Texto de evidencia

Texto a analizar:
{text}

Devuelve los resultados en formato JSON con arrays 'entities' y 'relationships'."""
    
    def _build_french_prompt(self, text: str, entity_types: str) -> str:
        """French extraction prompt"""
        return f"""Extraire les entités et les relations du texte suivant.

Types d'entités à extraire: {entity_types}
Langue: Français

Pour chaque entité, fournir:
1. Le texte de l'entité
2. Type d'entité (organization, person, funding_amount, date, location)
3. Score de confiance (0.0-1.0)
4. Positions dans le texte (indices de début et fin)

Pour les relations entre entités, fournir:
1. Entité source
2. Entité cible
3. Type de relation (fund, partner, acquire, compete, collaborate, mention)
4. Score de confiance (0.0-1.0)
5. Texte de preuve

Texte à analyser:
{text}

Retourner les résultats au format JSON avec les tableaux 'entities' et 'relationships'."""
    
    def _build_chinese_prompt(self, text: str, entity_types: str) -> str:
        """Chinese extraction prompt"""
        return f"""从以下文本中提取实体和关系。

要提取的实体类型: {entity_types}
语言: 中文

对于每个实体，提供：
1. 实体文本
2. 实体类型 (organization, person, funding_amount, date, location)
3. 置信度分数 (0.0-1.0)
4. 在文本中的位置（起始和结束字符索引）

对于实体之间的关系，提供：
1. 源实体
2. 目标实体
3. 关系类型 (fund, partner, acquire, compete, collaborate, mention)
4. 置信度分数 (0.0-1.0)
5. 证据文本

要分析的文本：
{text}

以JSON格式返回结果，包含'entities'和'relationships'数组。"""
    
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

