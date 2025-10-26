"""Vector similarity search service using embeddings"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import logging
import numpy as np

from src.ai.integrations.vector_db import vector_db_client
from src.ai.integrations.llm_client import llm_client
from src.ai.models import ExtractedEntity

logger = logging.getLogger(__name__)


class VectorSearch:
    """Service for vector-based similarity search"""
    
    def __init__(self):
        """Initialize vector search service"""
        self.vector_client = vector_db_client
        self.llm_client = llm_client
    
    async def search_similar_by_text(
        self,
        db: Session,
        query_text: str,
        limit: int = 20,
        confidence_threshold: float = 0.7,
        entity_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Find entities similar to query text using vector embeddings.
        
        Args:
            db: Database session
            query_text: Search query text
            limit: Maximum number of results
            confidence_threshold: Minimum entity confidence score
            entity_types: Optional filter by entity types
        
        Returns:
            List of similar entities with similarity scores
        """
        try:
            # Generate embedding for query text
            query_embedding = await self._generate_embedding(query_text)
            
            # Search vector database
            similar_results = await self.vector_client.search_similar(
                query_vector=query_embedding,
                limit=limit,
                confidence_threshold=confidence_threshold,
                entity_types=entity_types
            )
            
            # Enrich with full entity data from database
            enriched_results = []
            for result in similar_results:
                entity_id = result['entity_id']
                entity = db.query(ExtractedEntity).filter(
                    ExtractedEntity.id == entity_id
                ).first()
                
                if entity:
                    enriched_results.append({
                        'entity': {
                            'id': str(entity.id),
                            'text': entity.text,
                            'type': entity.entity_type,
                            'confidence': float(entity.confidence),
                            'metadata': entity.metadata or {}
                        },
                        'similarity_score': result['similarity_score']
                    })
            
            logger.info(
                f"Found {len(enriched_results)} similar entities for: {query_text}"
            )
            return enriched_results
        
        except Exception as e:
            logger.error(f"Vector similarity search failed: {e}")
            raise
    
    async def search_similar_by_entity(
        self,
        db: Session,
        entity_id: str,
        limit: int = 20,
        confidence_threshold: float = 0.7,
        entity_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Find entities similar to a given entity.
        
        Args:
            db: Database session
            entity_id: UUID of the entity to find similar to
            limit: Maximum number of results
            confidence_threshold: Minimum confidence score
            entity_types: Optional filter by entity types
        
        Returns:
            List of similar entities with similarity scores
        """
        try:
            # Get source entity
            source_entity = db.query(ExtractedEntity).filter(
                ExtractedEntity.id == entity_id
            ).first()
            
            if not source_entity:
                logger.warning(f"Entity {entity_id} not found")
                return []
            
            # Get entity's vector embedding
            if not source_entity.vector_embedding:
                logger.warning(f"Entity {entity_id} has no embedding")
                return []
            
            query_embedding = list(source_entity.vector_embedding)
            
            # Search vector database
            similar_results = await self.vector_client.search_similar(
                query_vector=query_embedding,
                limit=limit + 1,  # +1 to exclude self
                confidence_threshold=confidence_threshold,
                entity_types=entity_types
            )
            
            # Filter out the source entity itself
            enriched_results = []
            for result in similar_results:
                result_entity_id = result['entity_id']
                
                # Skip self
                if str(result_entity_id) == str(entity_id):
                    continue
                
                entity = db.query(ExtractedEntity).filter(
                    ExtractedEntity.id == result_entity_id
                ).first()
                
                if entity:
                    enriched_results.append({
                        'entity': {
                            'id': str(entity.id),
                            'text': entity.text,
                            'type': entity.entity_type,
                            'confidence': float(entity.confidence),
                            'metadata': entity.metadata or {}
                        },
                        'similarity_score': result['similarity_score']
                    })
                
                if len(enriched_results) >= limit:
                    break
            
            logger.info(
                f"Found {len(enriched_results)} similar entities to "
                f"{source_entity.text}"
            )
            return enriched_results
        
        except Exception as e:
            logger.error(f"Entity similarity search failed: {e}")
            raise
    
    async def find_related_entities(
        self,
        db: Session,
        entity_ids: List[str],
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Find entities related to a set of entities.
        
        Uses centroid of entity embeddings to find related entities.
        
        Args:
            db: Database session
            entity_ids: List of entity UUIDs
            limit: Maximum number of results
        
        Returns:
            List of related entities
        """
        try:
            # Get embeddings for all input entities
            embeddings = []
            for entity_id in entity_ids:
                entity = db.query(ExtractedEntity).filter(
                    ExtractedEntity.id == entity_id
                ).first()
                
                if entity and entity.vector_embedding:
                    embeddings.append(np.array(entity.vector_embedding))
            
            if not embeddings:
                logger.warning("No valid embeddings found for input entities")
                return []
            
            # Calculate centroid (average) of embeddings
            centroid = np.mean(embeddings, axis=0)
            centroid_list = centroid.tolist()
            
            # Search using centroid
            similar_results = await self.vector_client.search_similar(
                query_vector=centroid_list,
                limit=limit + len(entity_ids),  # Extra to filter out inputs
                confidence_threshold=0.5
            )
            
            # Filter out input entities
            input_ids_set = set(str(eid) for eid in entity_ids)
            enriched_results = []
            
            for result in similar_results:
                result_entity_id = str(result['entity_id'])
                
                # Skip if it's one of the input entities
                if result_entity_id in input_ids_set:
                    continue
                
                entity = db.query(ExtractedEntity).filter(
                    ExtractedEntity.id == result_entity_id
                ).first()
                
                if entity:
                    enriched_results.append({
                        'entity': {
                            'id': str(entity.id),
                            'text': entity.text,
                            'type': entity.entity_type,
                            'confidence': float(entity.confidence),
                            'metadata': entity.metadata or {}
                        },
                        'similarity_score': result['similarity_score']
                    })
                
                if len(enriched_results) >= limit:
                    break
            
            logger.info(
                f"Found {len(enriched_results)} related entities "
                f"for {len(entity_ids)} input entities"
            )
            return enriched_results
        
        except Exception as e:
            logger.error(f"Related entities search failed: {e}")
            raise
    
    async def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate vector embedding for text.
        
        Uses OpenAI embeddings API or similar.
        
        Args:
            text: Input text
        
        Returns:
            768-dimensional embedding vector
        """
        try:
            # For now, generate a simple embedding
            # In production, use OpenAI embeddings API:
            # from openai import OpenAI
            # client = OpenAI()
            # response = client.embeddings.create(
            #     model="text-embedding-ada-002",
            #     input=text
            # )
            # return response.data[0].embedding
            
            # Placeholder: generate deterministic embedding based on text
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()
            
            # Create 768-dimensional vector from hash
            embedding = []
            for i in range(768):
                # Use different parts of hash for each dimension
                seed = int(text_hash[i % len(text_hash)], 16) + i
                value = (seed % 1000) / 1000.0 - 0.5  # Range: -0.5 to 0.5
                embedding.append(value)
            
            # Normalize to unit vector
            embedding = np.array(embedding)
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            
            return embedding.tolist()
        
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            # Return zero vector as fallback
            return [0.0] * 768
    
    async def add_entity_embedding(
        self,
        entity_id: str,
        text: str,
        entity_type: str,
        confidence: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Generate and store embedding for an entity.
        
        Args:
            entity_id: Entity UUID
            text: Entity text
            entity_type: Entity type
            confidence: Confidence score
            metadata: Optional metadata
        
        Returns:
            True if successful
        """
        try:
            # Generate embedding
            embedding = await self._generate_embedding(text)
            
            # Store in vector database
            payload = {
                'entity_id': entity_id,
                'text': text,
                'entity_type': entity_type,
                'confidence': confidence,
                'metadata': metadata or {}
            }
            
            success = await self.vector_client.add_entity_embedding(
                entity_id=entity_id,
                embedding=embedding,
                payload=payload
            )
            
            return success
        
        except Exception as e:
            logger.error(f"Add entity embedding failed: {e}")
            return False


# Global vector search instance
vector_search = VectorSearch()

