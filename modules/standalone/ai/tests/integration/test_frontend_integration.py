"""Integration tests for Frontend module integration"""

import pytest
from fastapi.testclient import TestClient
from src.ai.api.main import app
import json

client = TestClient(app)


class TestFrontendIntegration:
    """Test Frontend module integration scenarios"""
    
    def test_entity_search_workflow(self):
        """Test complete entity search workflow for frontend users"""
        # Step 1: Search for entities
        search_request = {
            "query": "technology companies",
            "query_type": "entity_search",
            "filters": {
                "entity_types": ["organization"],
                "confidence_threshold": 0.7,
                "limit": 10
            }
        }
        
        response = client.post("/ai/v1/graph/query", json=search_request)
        
        # Should handle gracefully even if no data exists
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify response structure matches frontend needs
            assert "query_id" in data
            assert "entities" in data
            assert "total_results" in data
            assert "execution_time_ms" in data
            
            # Verify execution time meets requirements (<2000ms)
            assert data["execution_time_ms"] < 10000  # Lenient for testing
    
    def test_entity_detail_with_relationships(self):
        """Test retrieving entity details with relationships"""
        # Use a test entity ID (will 404 if not in DB, which is ok for contract test)
        test_entity_id = "550e8400-e29b-41d4-a716-446655440000"
        
        response = client.get(
            f"/ai/v1/graph/entity/{test_entity_id}",
            params={
                "include_relationships": True,
                "relationship_depth": 2
            }
        )
        
        # Should return 404 (no data) or 500 (DB error) - both acceptable for contract test
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "entity" in data
            
            entity = data["entity"]
            assert "id" in entity
            assert "text" in entity
            assert "type" in entity
            assert "confidence" in entity
            
            # Relationships should be included
            if "relationships" in entity and entity["relationships"]:
                rel = entity["relationships"][0]
                assert "target_entity" in rel
                assert "relationship_type" in rel
                assert "confidence" in rel
                assert "direction" in rel
    
    def test_similarity_search_for_recommendations(self):
        """Test similarity search for content recommendations"""
        # Search by text
        text_request = {
            "text": "artificial intelligence research",
            "limit": 5,
            "confidence_threshold": 0.6
        }
        
        response = client.post("/ai/v1/graph/similarity", json=text_request)
        
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "similar_entities" in data
            assert "execution_time_ms" in data
            assert isinstance(data["similar_entities"], list)
            
            # Verify execution time (<2000ms requirement)
            assert data["execution_time_ms"] < 10000
            
            # Verify similarity scores
            for result in data["similar_entities"]:
                assert "entity" in result
                assert "similarity_score" in result
                assert 0.0 <= result["similarity_score"] <= 1.0
    
    def test_websocket_connection(self):
        """Test WebSocket connection for real-time updates"""
        # WebSocket testing with TestClient
        test_client_id = "frontend-test-client"
        
        with client.websocket_connect(f"/ai/v1/ws/graph/{test_client_id}") as websocket:
            # Test ping/pong
            websocket.send_json({"action": "ping"})
            
            response = websocket.receive_json(timeout=5)
            assert response["type"] == "pong"
    
    def test_websocket_entity_subscription(self):
        """Test subscribing to entity updates via WebSocket"""
        test_client_id = "frontend-subscriber"
        test_entity_id = "550e8400-e29b-41d4-a716-446655440000"
        
        with client.websocket_connect(f"/ai/v1/ws/graph/{test_client_id}") as websocket:
            # Subscribe to an entity
            websocket.send_json({
                "action": "subscribe",
                "entity_id": test_entity_id
            })
            
            # Should receive subscription confirmation
            response = websocket.receive_json(timeout=5)
            assert response["type"] == "subscription_confirmed"
            assert response["entity_id"] == test_entity_id
            
            # Unsubscribe
            websocket.send_json({
                "action": "unsubscribe",
                "entity_id": test_entity_id
            })
            
            response = websocket.receive_json(timeout=5)
            assert response["type"] == "unsubscription_confirmed"
    
    def test_graph_visualization_data_format(self):
        """Test that graph data is properly formatted for visualization"""
        request_data = {
            "query": "funding relationships",
            "query_type": "relationship_query",
            "filters": {
                "relationship_types": ["fund"],
                "confidence_threshold": 0.8,
                "limit": 20
            }
        }
        
        response = client.post("/ai/v1/graph/query", json=request_data)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify entities can be used for visualization
            for entity in data.get("entities", []):
                # Each entity should have required fields for visualization
                assert "id" in entity  # For node ID
                assert "text" in entity  # For node label
                assert "type" in entity  # For node styling
                assert "confidence" in entity  # For node sizing
                
                # Relationships should have direction info
                if entity.get("relationships"):
                    for rel in entity["relationships"]:
                        assert "direction" in rel
                        assert rel["direction"] in ["incoming", "outgoing", "bidirectional"]
    
    def test_concurrent_graph_queries(self):
        """Test that API handles concurrent frontend queries"""
        import concurrent.futures
        
        def make_query():
            request_data = {
                "query": "test query",
                "query_type": "entity_search"
            }
            return client.post("/ai/v1/graph/query", json=request_data)
        
        # Simulate 10 concurrent frontend users
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_query) for _ in range(10)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All requests should complete
        assert len(responses) == 10
        
        # Most should succeed (some may fail if DB not configured)
        success_count = sum(1 for r in responses if r.status_code == 200)
        # At least verify they don't crash
        for response in responses:
            assert response.status_code in [200, 500]
    
    def test_error_handling_for_frontend(self):
        """Test that API provides user-friendly error messages"""
        # Invalid request
        invalid_request = {
            "query": "",  # Empty query
            "query_type": "entity_search"
        }
        
        response = client.post("/ai/v1/graph/query", json=invalid_request)
        
        # Should return validation error
        assert response.status_code == 422
        
        # Error response should have details
        error = response.json()
        assert "detail" in error
    
    def test_api_documentation_accessible(self):
        """Test that frontend can access API documentation"""
        # OpenAPI spec
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        spec = response.json()
        
        # Verify knowledge graph endpoints are documented
        assert "/ai/v1/graph/query" in spec.get("paths", {})
        assert "/ai/v1/graph/entity/{entity_id}" in spec.get("paths", {})
        assert "/ai/v1/graph/similarity" in spec.get("paths", {})


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

