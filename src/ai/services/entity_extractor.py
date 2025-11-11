"""Entity extraction service - core business logic"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import logging
import asyncio

from src.ai.integrations.llm_client import llm_client
from src.ai.lib.confidence_scoring import (
    calculate_confidence,
    get_source_reliability_score,
    calculate_context_score,
    get_confidence_label
)
from src.ai.lib.text_processing import (
    chunk_text,
    clean_text,
    count_entity_mentions,
    extract_positions,
    normalize_entity_text
)
from src.ai.services.relationship_mapper import relationship_mapper

logger = logging.getLogger(__name__)


class EntityExtractor:
    """Service for extracting entities from documents with flexible type detection"""

    def __init__(self):
        """Initialize entity extractor"""
        self.llm_client = llm_client
    
    async def extract(
        self,
        document_id: str,
        content: str,
        entity_types: Optional[List[str]] = None,
        relationship_types: Optional[List[str]] = None,
        confidence_threshold: float = 0.70,
        source_type: str = 'unknown'
    ) -> Dict[str, Any]:
        """
        Extract entities and relationships from document content.

        Args:
            document_id: UUID of the document
            content: Document text content
            entity_types: List of entity types to extract (default: None for all types)
            relationship_types: List of relationship types to identify (default: None for all types)
            confidence_threshold: Minimum confidence score (0.0-1.0)
            source_type: Type of document source for reliability scoring

        Returns:
            Dictionary with extracted entities and relationships
        """
        start_time = datetime.utcnow()

        # Clean and prepare text
        cleaned_content = clean_text(content)

        # Get source reliability score
        source_score = get_source_reliability_score(source_type)
        
        # Process document (chunk if too large)
        if len(cleaned_content) > 8000:  # ~2000 tokens
            logger.info("Document large, processing in chunks")
            result = await self._extract_from_chunks(
                cleaned_content,
                entity_types,
                relationship_types,
                source_score
            )
        else:
            result = await self._extract_from_text(
                cleaned_content,
                entity_types,
                relationship_types,
                source_score
            )

        # Calculate context scores and filter by confidence
        result = self._enrich_and_filter(
            result,
            cleaned_content,
            confidence_threshold
        )

        # Identify relationships between entities
        if len(result['entities']) >= 2:
            logger.info("Identifying relationships between entities")
            additional_relationships = await relationship_mapper.identify_relationships(
                entities=result['entities'],
                text=cleaned_content,
                relationship_types=relationship_types
            )

            # Merge with LLM-identified relationships
            result['relationships'].extend(additional_relationships)

        # Ensure each relationship has a unique identifier
        for relationship in result['relationships']:
            if 'id' not in relationship or not relationship['id']:
                relationship['id'] = str(uuid.uuid4())

        # Calculate processing time
        processing_time = (datetime.utcnow() - start_time).total_seconds()

        return {
            'document_id': document_id,
            'entities': result['entities'],
            'relationships': result['relationships'],
            'stats': {
                'entities_extracted': len(result['entities']),
                'relationships_found': len(result['relationships']),
                'processing_time_seconds': processing_time,
                'source_type': source_type
            }
        }
    
    async def _extract_from_text(
        self,
        text: str,
        entity_types: Optional[List[str]],
        relationship_types: Optional[List[str]],
        source_score: float
    ) -> Dict[str, Any]:
        """Extract entities from a single text block"""
        try:
            # Call LLM for extraction
            llm_result = await self.llm_client.extract_entities(
                text=text,
                entity_types=entity_types
            )
            
            # Process entities
            entities = []
            for entity_data in llm_result.get('entities', []):
                entity = self._process_entity(
                    entity_data,
                    text,
                    source_score
                )
                if entity:
                    entities.append(entity)
            
            # Process relationships
            relationships = []
            for rel_data in llm_result.get('relationships', []):
                relationship = self._process_relationship(
                    rel_data,
                    entities,
                    source_score
                )
                if relationship:
                    relationships.append(relationship)
            
            return {
                'entities': entities,
                'relationships': relationships
            }
        
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return {
                'entities': [],
                'relationships': []
            }
    
    async def _extract_from_chunks(
        self,
        text: str,
        entity_types: Optional[List[str]],
        relationship_types: Optional[List[str]],
        source_score: float
    ) -> Dict[str, Any]:
        """Extract entities from multiple text chunks"""
        chunks = chunk_text(text, max_tokens=2000, overlap=200)

        all_entities = []
        all_relationships = []

        # Process chunks in parallel (with concurrency limit)
        sem = asyncio.Semaphore(3)  # Max 3 concurrent requests

        async def process_chunk(chunk):
            async with sem:
                return await self._extract_from_text(
                    chunk['text'],
                    entity_types,
                    relationship_types,
                    source_score
                )
        
        tasks = [process_chunk(chunk) for chunk in chunks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        for result in results:
            if isinstance(result, dict):
                all_entities.extend(result.get('entities', []))
                all_relationships.extend(result.get('relationships', []))
        
        # Deduplicate entities (will be done in next step)
        return {
            'entities': all_entities,
            'relationships': all_relationships
        }
    
    def _process_entity(
        self,
        entity_data: Dict[str, Any],
        full_text: str,
        source_score: float
    ) -> Optional[Dict[str, Any]]:
        """Process and enrich a single entity"""
        try:
            entity_text = normalize_entity_text(entity_data.get('text', ''))
            entity_type = entity_data.get('type', '').lower()
            model_confidence = float(entity_data.get('confidence', 0.5))

            if not entity_text:
                return None
            
            # Find all positions of entity in text
            positions = extract_positions(full_text, entity_text)
            if not positions:
                # If not found exactly, use provided positions if available
                provided_positions = entity_data.get('positions', [])
                if provided_positions:
                    positions = [(p[0], p[1]) for p in provided_positions]
                else:
                    return None
            
            # Count mentions
            mention_count = len(positions)
            
            # Calculate initial confidence (will be updated with context score later)
            entity = {
                'id': str(uuid.uuid4()),
                'text': entity_text,
                'type': entity_type,
                'positions': positions,
                'mention_count': mention_count,
                'model_confidence': model_confidence,
                'source_score': source_score,
                'metadata': entity_data.get('metadata', {})
            }
            
            return entity
        
        except Exception as e:
            logger.warning(f"Failed to process entity: {e}")
            return None
    
    def _process_relationship(
        self,
        rel_data: Dict[str, Any],
        entities: List[Dict[str, Any]],
        source_score: float
    ) -> Optional[Dict[str, Any]]:
        """Process and enrich a single relationship"""
        try:
            rel_type = rel_data.get('relationship_type', '').lower()
            if not rel_type:
                return None
            
            # Find source and target entities
            source_text = rel_data.get('source_entity', '')
            target_text = rel_data.get('target_entity', '')
            
            source_entity = next(
                (e for e in entities if e['text'].lower() == source_text.lower()),
                None
            )
            target_entity = next(
                (e for e in entities if e['text'].lower() == target_text.lower()),
                None
            )
            
            if not source_entity or not target_entity:
                return None
            
            model_confidence = float(rel_data.get('confidence', 0.5))
            
            relationship = {
                'id': str(uuid.uuid4()),
                'source_entity_id': source_entity['id'],
                'target_entity_id': target_entity['id'],
                'relationship_type': rel_type,
                'confidence': model_confidence * source_score,  # Weighted by source
                'evidence': rel_data.get('evidence', ''),
                'metadata': {
                    'source_entity_text': source_entity['text'],
                    'target_entity_text': target_entity['text']
                }
            }
            
            return relationship
        
        except Exception as e:
            logger.warning(f"Failed to process relationship: {e}")
            return None
    
    def _enrich_and_filter(
        self,
        result: Dict[str, Any],
        full_text: str,
        confidence_threshold: float
    ) -> Dict[str, Any]:
        """Enrich entities with context scores and filter by confidence"""
        entities = result['entities']
        total_entities = len(entities)
        
        # Calculate co-occurrence matrix
        co_occurrence = self._calculate_co_occurrence(entities, full_text)
        
        # Enrich entities with final confidence scores
        enriched_entities = []
        for entity in entities:
            # Calculate context score
            mention_count = entity['mention_count']
            co_occurrence_count = co_occurrence.get(entity['id'], 0)
            
            context_score = calculate_context_score(
                mention_count,
                co_occurrence_count,
                total_entities
            )
            
            # Calculate final confidence
            final_confidence = calculate_confidence(
                entity['source_score'],
                context_score,
                entity['model_confidence']
            )
            
            # Filter by threshold
            if final_confidence >= confidence_threshold:
                entity['confidence'] = final_confidence
                entity['confidence_label'] = get_confidence_label(final_confidence)
                entity['context_score'] = context_score
                
                # Clean up temporary fields
                del entity['mention_count']
                del entity['model_confidence']
                del entity['source_score']
                
                enriched_entities.append(entity)
        
        return {
            'entities': enriched_entities,
            'relationships': result['relationships']
        }
    
    def _calculate_co_occurrence(
        self,
        entities: List[Dict[str, Any]],
        full_text: str,
        window_size: int = 200
    ) -> Dict[str, int]:
        """Calculate co-occurrence counts for entities"""
        co_occurrence = {}
        
        for entity in entities:
            count = 0
            for pos in entity['positions']:
                # Check if other entities appear within window
                window_start = max(0, pos[0] - window_size)
                window_end = min(len(full_text), pos[1] + window_size)
                
                for other_entity in entities:
                    if other_entity['id'] == entity['id']:
                        continue
                    
                    # Check if other entity appears in window
                    for other_pos in other_entity['positions']:
                        if window_start <= other_pos[0] <= window_end:
                            count += 1
                            break
            
            co_occurrence[entity['id']] = count
        
        return co_occurrence


# Global entity extractor instance
entity_extractor = EntityExtractor()

