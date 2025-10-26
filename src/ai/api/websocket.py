"""WebSocket endpoints for real-time graph updates"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set, Any
import json
import logging
import asyncio

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai/v1", tags=["websocket"])


class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        """Initialize connection manager"""
        self.active_connections: Set[WebSocket] = set()
        self.subscriptions: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        """Remove WebSocket connection"""
        self.active_connections.discard(websocket)
        
        # Remove from all subscriptions
        for entity_id, subscribers in self.subscriptions.items():
            subscribers.discard(websocket)
        
        logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")
    
    async def subscribe_to_entity(
        self,
        websocket: WebSocket,
        entity_id: str
    ):
        """Subscribe to updates for a specific entity"""
        if entity_id not in self.subscriptions:
            self.subscriptions[entity_id] = set()
        
        self.subscriptions[entity_id].add(websocket)
        logger.info(f"Client subscribed to entity {entity_id}")
    
    async def unsubscribe_from_entity(
        self,
        websocket: WebSocket,
        entity_id: str
    ):
        """Unsubscribe from entity updates"""
        if entity_id in self.subscriptions:
            self.subscriptions[entity_id].discard(websocket)
            logger.info(f"Client unsubscribed from entity {entity_id}")
    
    async def broadcast_entity_update(
        self,
        entity_id: str,
        update_data: Dict[str, any]
    ):
        """
        Broadcast update to all clients subscribed to an entity.
        
        Args:
            entity_id: Entity UUID
            update_data: Update information to send
        """
        if entity_id not in self.subscriptions:
            return
        
        message = {
            'type': 'entity_update',
            'entity_id': entity_id,
            'data': update_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Send to all subscribers
        disconnected = set()
        for connection in self.subscriptions[entity_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send to client: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.subscriptions[entity_id].discard(connection)
            self.active_connections.discard(connection)
    
    async def broadcast_graph_update(
        self,
        update_data: Dict[str, Any]
    ):
        """
        Broadcast graph update to all connected clients.
        
        Args:
            update_data: Update information
        """
        from datetime import datetime
        
        message = {
            'type': 'graph_update',
            'data': update_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Send to all active connections
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send broadcast: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.active_connections.discard(connection)


# Global connection manager
manager = ConnectionManager()


@router.websocket("/ws/graph/{client_id}")
async def websocket_graph_updates(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time knowledge graph updates.
    
    Protocol:
    - Client connects with unique client_id
    - Client can subscribe to specific entities
    - Server broadcasts updates when entities/relationships change
    """
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                action = message.get('action')
                
                if action == 'subscribe':
                    # Subscribe to entity updates
                    entity_id = message.get('entity_id')
                    if entity_id:
                        await manager.subscribe_to_entity(websocket, entity_id)
                        await websocket.send_json({
                            'type': 'subscription_confirmed',
                            'entity_id': entity_id
                        })
                
                elif action == 'unsubscribe':
                    # Unsubscribe from entity
                    entity_id = message.get('entity_id')
                    if entity_id:
                        await manager.unsubscribe_from_entity(websocket, entity_id)
                        await websocket.send_json({
                            'type': 'unsubscription_confirmed',
                            'entity_id': entity_id
                        })
                
                elif action == 'ping':
                    # Heartbeat
                    await websocket.send_json({
                        'type': 'pong'
                    })
                
                else:
                    logger.warning(f"Unknown action from client {client_id}: {action}")
                    await websocket.send_json({
                        'type': 'error',
                        'message': f'Unknown action: {action}'
                    })
            
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON from client {client_id}")
                await websocket.send_json({
                    'type': 'error',
                    'message': 'Invalid JSON'
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        logger.info(f"Client {client_id} disconnected normally")
    
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        manager.disconnect(websocket, client_id)


async def notify_entity_update(entity_id: str, update_type: str, data: Dict[str, Any]):
    """
    Helper function to notify subscribers of entity updates.
    
    Call this after entity/relationship changes.
    
    Args:
        entity_id: Entity UUID that was updated
        update_type: Type of update (created, updated, deleted, relationship_added)
        data: Update data
    """
    update_data = {
        'update_type': update_type,
        'entity_id': entity_id,
        'data': data
    }
    
    await manager.broadcast_entity_update(entity_id, update_data)


async def notify_graph_change(change_type: str, data: Dict[str, Any]):
    """
    Helper function to notify all clients of graph changes.
    
    Args:
        change_type: Type of change (bulk_update, schema_change, etc.)
        data: Change data
    """
    update_data = {
        'change_type': change_type,
        'data': data
    }
    
    await manager.broadcast_graph_update(update_data)

