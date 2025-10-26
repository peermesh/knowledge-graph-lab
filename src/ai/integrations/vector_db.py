"""Qdrant vector database client wrapper"""

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import logging
import uuid

from src.ai.config import settings

logger = logging.getLogger(__name__)


class VectorDBClient:
    """Manages vector database operations with Qdrant"""
    
    COLLECTION_NAME = "entity_embeddings"
    VECTOR_SIZE = 768
    
    def __init__(self):
        """Initialize Qdrant client"""
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            timeout=30
        )
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if self.COLLECTION_NAME not in collection_names:
                logger.info(f"Creating collection: {self.COLLECTION_NAME}")
                self.client.create_collection(
                    collection_name=self.COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=self.VECTOR_SIZE,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Collection created successfully")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise
    
    async def add_entity_embedding(
        self,
        entity_id: str,
        embedding: List[float],
        payload: Dict[str, Any]
    ) -> bool:
        """
        Add entity embedding to vector database
        
        Args:
            entity_id: UUID of the entity
            embedding: 768-dimensional vector embedding
            payload: Metadata (entity text, type, confidence, etc.)
            
        Returns:
            True if successful
        """
        try:
            point = PointStruct(
                id=str(entity_id),
                vector=embedding,
                payload=payload
            )
            
            self.client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=[point]
            )
            
            logger.info(f"Added embedding for entity {entity_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding embedding: {e}")
            raise
    
    async def batch_add_embeddings(
        self,
        embeddings: List[Dict[str, Any]]
    ) -> int:
        """
        Batch add multiple entity embeddings
        
        Args:
            embeddings: List of dicts with entity_id, embedding, and payload
            
        Returns:
            Number of embeddings added
        """
        try:
            points = [
                PointStruct(
                    id=str(item['entity_id']),
                    vector=item['embedding'],
                    payload=item['payload']
                )
                for item in embeddings
            ]
            
            self.client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=points
            )
            
            logger.info(f"Batch added {len(points)} embeddings")
            return len(points)
        except Exception as e:
            logger.error(f"Error batch adding embeddings: {e}")
            raise
    
    async def search_similar(
        self,
        query_vector: List[float],
        limit: int = 20,
        confidence_threshold: float = 0.7,
        entity_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar entities using vector similarity
        
        Args:
            query_vector: Query embedding vector
            limit: Maximum number of results
            confidence_threshold: Minimum confidence score filter
            entity_types: Optional list of entity types to filter by
            
        Returns:
            List of similar entities with scores
        """
        try:
            # Build filter conditions
            filter_conditions = []
            
            if entity_types:
                filter_conditions.append(
                    FieldCondition(
                        key="entity_type",
                        match=MatchValue(any=entity_types)
                    )
                )
            
            # Note: Qdrant filter syntax needs to be adjusted based on actual payload structure
            query_filter = Filter(must=filter_conditions) if filter_conditions else None
            
            # Perform similarity search
            results = self.client.search(
                collection_name=self.COLLECTION_NAME,
                query_vector=query_vector,
                query_filter=query_filter,
                limit=limit,
                with_payload=True
            )
            
            # Format results
            similar_entities = []
            for result in results:
                if result.payload.get('confidence', 0) >= confidence_threshold:
                    similar_entities.append({
                        'entity_id': result.id,
                        'similarity_score': result.score,
                        'entity': result.payload
                    })
            
            logger.info(f"Found {len(similar_entities)} similar entities")
            return similar_entities
        except Exception as e:
            logger.error(f"Error searching similar entities: {e}")
            raise
    
    async def delete_entity_embedding(self, entity_id: str) -> bool:
        """Delete entity embedding from vector database"""
        try:
            self.client.delete(
                collection_name=self.COLLECTION_NAME,
                points_selector=[str(entity_id)]
            )
            logger.info(f"Deleted embedding for entity {entity_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting embedding: {e}")
            raise


# Global vector DB client instance
vector_db_client = VectorDBClient()

