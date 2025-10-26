"""Graph builder service - constructs knowledge graphs from entities"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import logging
import uuid

from src.ai.models import (
    ExtractedEntity,
    EntityRelationship,
    KnowledgeGraphNode,
    KnowledgeGraphEdge
)
from src.ai.integrations.vector_db import vector_db_client

logger = logging.getLogger(__name__)


class GraphBuilder:
    """Service for building knowledge graphs from extracted entities"""
    
    def __init__(self):
        """Initialize graph builder"""
        self.vector_client = vector_db_client
    
    async def build_from_entities(
        self,
        db: Session,
        entities: List[Dict[str, Any]],
        relationships: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Build knowledge graph from extracted entities and relationships.
        
        Args:
            db: Database session
            entities: List of extracted entities
            relationships: List of entity relationships
        
        Returns:
            Dictionary with created nodes and edges counts
        """
        try:
            nodes_created = 0
            edges_created = 0
            
            # Create nodes for each entity
            entity_id_to_node_id = {}
            
            for entity_data in entities:
                node = await self._create_node(db, entity_data)
                if node:
                    entity_id_to_node_id[entity_data['id']] = node.id
                    nodes_created += 1
            
            # Create edges for each relationship
            for rel_data in relationships:
                source_node_id = entity_id_to_node_id.get(rel_data['source_entity_id'])
                target_node_id = entity_id_to_node_id.get(rel_data['target_entity_id'])
                
                if source_node_id and target_node_id:
                    edge = await self._create_edge(
                        db,
                        source_node_id,
                        target_node_id,
                        rel_data
                    )
                    if edge:
                        edges_created += 1
            
            # Update node degrees
            await self._update_node_degrees(db, list(entity_id_to_node_id.values()))
            
            # Commit all changes
            db.commit()
            
            logger.info(
                f"Graph built: {nodes_created} nodes, {edges_created} edges"
            )
            
            return {
                'nodes_created': nodes_created,
                'edges_created': edges_created,
                'node_ids': list(entity_id_to_node_id.values())
            }
        
        except Exception as e:
            db.rollback()
            logger.error(f"Graph building failed: {e}")
            raise
    
    async def _create_node(
        self,
        db: Session,
        entity_data: Dict[str, Any]
    ) -> Optional[KnowledgeGraphNode]:
        """Create a knowledge graph node from entity data"""
        try:
            # Check if node already exists for this entity
            entity_id = entity_data['id']
            existing_node = db.query(KnowledgeGraphNode).filter(
                KnowledgeGraphNode.entity_id == entity_id
            ).first()
            
            if existing_node:
                logger.debug(f"Node already exists for entity {entity_id}")
                return existing_node
            
            # Prepare node properties
            properties = {
                'name': entity_data['text'],
                'entity_type': entity_data['type'],
                'confidence': float(entity_data['confidence']),
                'aliases': entity_data.get('metadata', {}).get('aliases', [])
            }
            
            # Add additional metadata
            if 'metadata' in entity_data:
                for key, value in entity_data['metadata'].items():
                    if key not in properties:
                        properties[key] = value
            
            # Create node
            node = KnowledgeGraphNode(
                id=uuid.uuid4(),
                entity_id=entity_id,
                node_type='entity',  # Default to 'entity' type
                properties=properties,
                vector_embedding=entity_data.get('vector_embedding', [0.0] * 768),
                degree=0  # Will be updated later
            )
            
            db.add(node)
            
            logger.debug(f"Created node for entity {entity_data['text']}")
            return node
        
        except Exception as e:
            logger.error(f"Node creation failed: {e}")
            return None
    
    async def _create_edge(
        self,
        db: Session,
        source_node_id: uuid.UUID,
        target_node_id: uuid.UUID,
        rel_data: Dict[str, Any]
    ) -> Optional[KnowledgeGraphEdge]:
        """Create a knowledge graph edge from relationship data"""
        try:
            # Check if edge already exists
            existing_edge = db.query(KnowledgeGraphEdge).filter(
                KnowledgeGraphEdge.source_node_id == source_node_id,
                KnowledgeGraphEdge.target_node_id == target_node_id,
                KnowledgeGraphEdge.relationship_type == rel_data['relationship_type']
            ).first()
            
            if existing_edge:
                logger.debug("Edge already exists")
                return existing_edge
            
            # Prepare edge properties
            properties = {
                'evidence': rel_data.get('evidence'),
                'metadata': rel_data.get('metadata', {})
            }
            
            # Create edge
            edge = KnowledgeGraphEdge(
                id=uuid.uuid4(),
                source_node_id=source_node_id,
                target_node_id=target_node_id,
                relationship_type=rel_data['relationship_type'],
                properties=properties,
                confidence=float(rel_data['confidence'])
            )
            
            db.add(edge)
            
            logger.debug(
                f"Created edge: {rel_data['relationship_type']} "
                f"(confidence: {rel_data['confidence']})"
            )
            return edge
        
        except Exception as e:
            logger.error(f"Edge creation failed: {e}")
            return None
    
    async def _update_node_degrees(
        self,
        db: Session,
        node_ids: List[uuid.UUID]
    ):
        """Update degree counts for nodes based on their edges"""
        for node_id in node_ids:
            # Count outgoing edges
            outgoing_count = db.query(KnowledgeGraphEdge).filter(
                KnowledgeGraphEdge.source_node_id == node_id
            ).count()
            
            # Count incoming edges
            incoming_count = db.query(KnowledgeGraphEdge).filter(
                KnowledgeGraphEdge.target_node_id == node_id
            ).count()
            
            # Update node degree (total connections)
            total_degree = outgoing_count + incoming_count
            
            node = db.query(KnowledgeGraphNode).filter(
                KnowledgeGraphNode.id == node_id
            ).first()
            
            if node:
                node.degree = total_degree
    
    async def add_entity_to_graph(
        self,
        db: Session,
        entity: ExtractedEntity
    ) -> Optional[KnowledgeGraphNode]:
        """
        Add a single entity to the knowledge graph.
        
        Args:
            db: Database session
            entity: ExtractedEntity model instance
        
        Returns:
            Created KnowledgeGraphNode or None
        """
        entity_data = {
            'id': entity.id,
            'text': entity.text,
            'type': entity.entity_type,
            'confidence': float(entity.confidence),
            'metadata': entity.metadata or {},
            'vector_embedding': list(entity.vector_embedding) if entity.vector_embedding else [0.0] * 768
        }
        
        node = await self._create_node(db, entity_data)
        
        if node:
            db.commit()
            logger.info(f"Added entity {entity.text} to knowledge graph")
        
        return node
    
    async def get_graph_stats(self, db: Session) -> Dict[str, Any]:
        """Get statistics about the knowledge graph"""
        total_nodes = db.query(KnowledgeGraphNode).count()
        total_edges = db.query(KnowledgeGraphEdge).count()
        
        # Get node type distribution
        node_types = db.query(
            KnowledgeGraphNode.node_type,
            db.func.count(KnowledgeGraphNode.id)
        ).group_by(KnowledgeGraphNode.node_type).all()
        
        # Get relationship type distribution
        rel_types = db.query(
            KnowledgeGraphEdge.relationship_type,
            db.func.count(KnowledgeGraphEdge.id)
        ).group_by(KnowledgeGraphEdge.relationship_type).all()
        
        return {
            'total_nodes': total_nodes,
            'total_edges': total_edges,
            'node_types': dict(node_types),
            'relationship_types': dict(rel_types),
            'average_degree': total_edges * 2 / total_nodes if total_nodes > 0 else 0
        }


# Global graph builder instance
graph_builder = GraphBuilder()

