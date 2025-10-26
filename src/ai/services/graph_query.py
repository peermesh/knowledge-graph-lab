"""Graph query service - queries knowledge graph for relationships"""

from typing import List, Dict, Any, Optional, Set
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import logging

from src.ai.models import (
    ExtractedEntity,
    KnowledgeGraphNode,
    KnowledgeGraphEdge
)

logger = logging.getLogger(__name__)


class GraphQuery:
    """Service for querying the knowledge graph"""
    
    def __init__(self):
        """Initialize graph query service"""
        pass
    
    async def query_entities(
        self,
        db: Session,
        query_text: str,
        entity_types: Optional[List[str]] = None,
        confidence_threshold: float = 0.7,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search for entities by text query.
        
        Args:
            db: Database session
            query_text: Search query
            entity_types: Filter by entity types
            confidence_threshold: Minimum confidence score
            limit: Maximum results to return
        
        Returns:
            List of matching entities with relationships
        """
        try:
            # Build query
            query = db.query(ExtractedEntity).filter(
                ExtractedEntity.text.ilike(f'%{query_text}%'),
                ExtractedEntity.confidence >= confidence_threshold
            )
            
            if entity_types:
                query = query.filter(ExtractedEntity.entity_type.in_(entity_types))
            
            # Execute query
            entities = query.limit(limit).all()
            
            # Enrich with relationships
            results = []
            for entity in entities:
                entity_data = await self._enrich_entity_with_relationships(
                    db,
                    entity
                )
                results.append(entity_data)
            
            logger.info(f"Found {len(results)} entities for query: {query_text}")
            return results
        
        except Exception as e:
            logger.error(f"Entity query failed: {e}")
            raise
    
    async def get_entity_by_id(
        self,
        db: Session,
        entity_id: str,
        include_relationships: bool = True,
        relationship_depth: int = 1
    ) -> Optional[Dict[str, Any]]:
        """
        Get entity by ID with optional relationship traversal.
        
        Args:
            db: Database session
            entity_id: Entity UUID
            include_relationships: Include relationships
            relationship_depth: Degrees of relationships (1-3)
        
        Returns:
            Entity data with relationships
        """
        try:
            entity = db.query(ExtractedEntity).filter(
                ExtractedEntity.id == entity_id
            ).first()
            
            if not entity:
                return None
            
            entity_data = self._entity_to_dict(entity)
            
            if include_relationships:
                entity_data['relationships'] = await self._get_entity_relationships(
                    db,
                    entity_id,
                    depth=relationship_depth
                )
            
            return entity_data
        
        except Exception as e:
            logger.error(f"Get entity failed: {e}")
            raise
    
    async def traverse_relationships(
        self,
        db: Session,
        entity_id: str,
        relationship_types: Optional[List[str]] = None,
        max_depth: int = 3,
        confidence_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Traverse relationships from an entity to specified depth.
        
        Args:
            db: Database session
            entity_id: Starting entity ID
            relationship_types: Filter by relationship types
            max_depth: Maximum traversal depth
            confidence_threshold: Minimum confidence for relationships
        
        Returns:
            Graph structure with nodes and edges
        """
        try:
            visited_nodes: Set[str] = set()
            nodes = []
            edges = []
            
            # Start traversal
            await self._traverse_recursive(
                db,
                entity_id,
                relationship_types,
                confidence_threshold,
                max_depth,
                0,
                visited_nodes,
                nodes,
                edges
            )
            
            return {
                'nodes': nodes,
                'edges': edges,
                'total_nodes': len(nodes),
                'total_edges': len(edges)
            }
        
        except Exception as e:
            logger.error(f"Relationship traversal failed: {e}")
            raise
    
    async def _traverse_recursive(
        self,
        db: Session,
        entity_id: str,
        relationship_types: Optional[List[str]],
        confidence_threshold: float,
        max_depth: int,
        current_depth: int,
        visited_nodes: Set[str],
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]]
    ):
        """Recursively traverse relationships"""
        if current_depth >= max_depth or entity_id in visited_nodes:
            return
        
        visited_nodes.add(entity_id)
        
        # Get entity and add to nodes
        entity = db.query(ExtractedEntity).filter(
            ExtractedEntity.id == entity_id
        ).first()
        
        if entity:
            nodes.append(self._entity_to_dict(entity))
        
        # Get related entities through graph edges
        graph_node = db.query(KnowledgeGraphNode).filter(
            KnowledgeGraphNode.entity_id == entity_id
        ).first()
        
        if not graph_node:
            return
        
        # Get outgoing relationships
        query = db.query(KnowledgeGraphEdge).filter(
            KnowledgeGraphEdge.source_node_id == graph_node.id,
            KnowledgeGraphEdge.confidence >= confidence_threshold
        )
        
        if relationship_types:
            query = query.filter(
                KnowledgeGraphEdge.relationship_type.in_(relationship_types)
            )
        
        outgoing_edges = query.all()
        
        for edge in outgoing_edges:
            # Add edge to results
            edges.append({
                'source': str(entity_id),
                'target': str(edge.target_node_id),
                'relationship_type': edge.relationship_type,
                'confidence': float(edge.confidence),
                'properties': edge.properties
            })
            
            # Get target entity
            target_node = db.query(KnowledgeGraphNode).filter(
                KnowledgeGraphNode.id == edge.target_node_id
            ).first()
            
            if target_node:
                # Recursively traverse
                await self._traverse_recursive(
                    db,
                    str(target_node.entity_id),
                    relationship_types,
                    confidence_threshold,
                    max_depth,
                    current_depth + 1,
                    visited_nodes,
                    nodes,
                    edges
                )
    
    async def _enrich_entity_with_relationships(
        self,
        db: Session,
        entity: ExtractedEntity
    ) -> Dict[str, Any]:
        """Enrich entity with immediate relationships"""
        entity_data = self._entity_to_dict(entity)
        
        # Get immediate relationships
        entity_data['relationships'] = await self._get_entity_relationships(
            db,
            str(entity.id),
            depth=1
        )
        
        return entity_data
    
    async def _get_entity_relationships(
        self,
        db: Session,
        entity_id: str,
        depth: int = 1
    ) -> List[Dict[str, Any]]:
        """Get relationships for an entity"""
        relationships = []
        
        # Get graph node
        graph_node = db.query(KnowledgeGraphNode).filter(
            KnowledgeGraphNode.entity_id == entity_id
        ).first()
        
        if not graph_node:
            return []
        
        # Get outgoing relationships
        outgoing = db.query(KnowledgeGraphEdge).filter(
            KnowledgeGraphEdge.source_node_id == graph_node.id
        ).all()
        
        for edge in outgoing:
            target_node = db.query(KnowledgeGraphNode).filter(
                KnowledgeGraphNode.id == edge.target_node_id
            ).first()
            
            if target_node:
                target_entity = db.query(ExtractedEntity).filter(
                    ExtractedEntity.id == target_node.entity_id
                ).first()
                
                if target_entity:
                    relationships.append({
                        'target_entity': target_entity.text,
                        'target_entity_id': str(target_entity.id),
                        'relationship_type': edge.relationship_type,
                        'confidence': float(edge.confidence),
                        'direction': 'outgoing'
                    })
        
        # Get incoming relationships
        incoming = db.query(KnowledgeGraphEdge).filter(
            KnowledgeGraphEdge.target_node_id == graph_node.id
        ).all()
        
        for edge in incoming:
            source_node = db.query(KnowledgeGraphNode).filter(
                KnowledgeGraphNode.id == edge.source_node_id
            ).first()
            
            if source_node:
                source_entity = db.query(ExtractedEntity).filter(
                    ExtractedEntity.id == source_node.entity_id
                ).first()
                
                if source_entity:
                    relationships.append({
                        'target_entity': source_entity.text,
                        'target_entity_id': str(source_entity.id),
                        'relationship_type': edge.relationship_type,
                        'confidence': float(edge.confidence),
                        'direction': 'incoming'
                    })
        
        return relationships
    
    def _entity_to_dict(self, entity: ExtractedEntity) -> Dict[str, Any]:
        """Convert entity model to dictionary"""
        return {
            'id': str(entity.id),
            'text': entity.text,
            'type': entity.entity_type,
            'confidence': float(entity.confidence),
            'metadata': entity.metadata or {}
        }
    
    async def find_paths(
        self,
        db: Session,
        source_entity_id: str,
        target_entity_id: str,
        max_depth: int = 3
    ) -> List[List[Dict[str, Any]]]:
        """
        Find paths between two entities.
        
        Args:
            db: Database session
            source_entity_id: Starting entity ID
            target_entity_id: Target entity ID
            max_depth: Maximum path length
        
        Returns:
            List of paths (each path is a list of edges)
        """
        paths = []
        current_path = []
        visited = set()
        
        await self._find_paths_recursive(
            db,
            source_entity_id,
            target_entity_id,
            max_depth,
            0,
            current_path,
            visited,
            paths
        )
        
        logger.info(
            f"Found {len(paths)} paths from {source_entity_id} to {target_entity_id}"
        )
        return paths
    
    async def _find_paths_recursive(
        self,
        db: Session,
        current_id: str,
        target_id: str,
        max_depth: int,
        current_depth: int,
        current_path: List[Dict[str, Any]],
        visited: Set[str],
        paths: List[List[Dict[str, Any]]]
    ):
        """Recursively find paths between entities"""
        if current_depth >= max_depth:
            return
        
        if current_id == target_id and current_path:
            paths.append(current_path.copy())
            return
        
        if current_id in visited:
            return
        
        visited.add(current_id)
        
        # Get graph node
        graph_node = db.query(KnowledgeGraphNode).filter(
            KnowledgeGraphNode.entity_id == current_id
        ).first()
        
        if not graph_node:
            visited.remove(current_id)
            return
        
        # Get outgoing edges
        edges = db.query(KnowledgeGraphEdge).filter(
            KnowledgeGraphEdge.source_node_id == graph_node.id
        ).all()
        
        for edge in edges:
            target_node = db.query(KnowledgeGraphNode).filter(
                KnowledgeGraphNode.id == edge.target_node_id
            ).first()
            
            if target_node:
                next_entity_id = str(target_node.entity_id)
                
                # Add edge to current path
                current_path.append({
                    'source': current_id,
                    'target': next_entity_id,
                    'relationship_type': edge.relationship_type,
                    'confidence': float(edge.confidence)
                })
                
                # Recurse
                await self._find_paths_recursive(
                    db,
                    next_entity_id,
                    target_id,
                    max_depth,
                    current_depth + 1,
                    current_path,
                    visited,
                    paths
                )
                
                # Backtrack
                current_path.pop()
        
        visited.remove(current_id)


# Global graph query instance
graph_query = GraphQuery()

