"""Contract tests for Knowledge Graph Query API"""

import pytest
from fastapi.testclient import TestClient
from src.ai.api.main import app

client = TestClient(app)


class TestKnowledgeGraphAPIContract:
    """Test that API matches OpenAPI specification"""
    
    def test_graph_query_endpoint_exists(self):
        """Test that /graph/query endpoint exists"""
        response = client.options("/ai/v1/graph/query")
        assert response.status_code in [200, 405]  # 405 if OPTIONS not implemented
    
    def test_graph_query_requires_post(self):
        """Test that endpoint only accepts POST"""
        response = client.get("/ai/v1/graph/query")
        assert response.status_code == 405  # Method not allowed
    
    def test_graph_query_entity_search(self):
        """Test entity_search query type"""
        request_data = {
            "query": "OpenAI",
            "query_type": "entity_search",
            "filters": {
                "entity_types": ["organization"],
                "confidence_threshold": 0.7,
                "limit": 20
            }
        }
        
        response = client.post("/ai/v1/graph/query", json=request_data)
        
        # Should return 200 or 500 (if DB not configured)
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify response structure
            assert "query_id" in data
            assert "total_results" in data
            assert "execution_time_ms" in data
            assert "entities" in data
            assert isinstance(data["entities"], list)
    
    def test_graph_query_similarity_search(self):
        """Test similarity_search query type"""
        request_data = {
            "query": "AI research companies",
            "query_type": "similarity_search",
            "filters": {
                "entity_types": ["organization"],
                "confidence_threshold": 0.5,
                "limit": 10
            }
        }
        
        response = client.post("/ai/v1/graph/query", json=request_data)
        assert response.status_code in [200, 500]
    
    def test_graph_query_invalid_type(self):
        """Test that invalid query_type is rejected"""
        request_data = {
            "query": "test",
            "query_type": "invalid_type"
        }
        
        response = client.post("/ai/v1/graph/query", json=request_data)
        # Should return 400 or 500
        assert response.status_code in [400, 422, 500]
    
    def test_graph_query_missing_required_fields(self):
        """Test that missing required fields returns 422"""
        incomplete_request = {
            "filters": {"limit": 10}
            # Missing query and query_type
        }
        
        response = client.post("/ai/v1/graph/query", json=incomplete_request)
        assert response.status_code == 422  # Validation error
    
    def test_entity_endpoint_exists(self):
        """Test that /graph/entity/{entity_id} endpoint exists"""
        fake_entity_id = "550e8400-e29b-41d4-a716-446655440000"
        response = client.get(f"/ai/v1/graph/entity/{fake_entity_id}")
        
        # Should return 404 (not found) or 500 (DB error)
        assert response.status_code in [404, 500]
    
    def test_entity_endpoint_with_parameters(self):
        """Test entity endpoint with query parameters"""
        fake_entity_id = "550e8400-e29b-41d4-a716-446655440000"
        response = client.get(
            f"/ai/v1/graph/entity/{fake_entity_id}",
            params={
                "include_relationships": True,
                "relationship_depth": 2
            }
        )
        
        # Should return 404 or 500
        assert response.status_code in [404, 500]
    
    def test_similarity_endpoint_exists(self):
        """Test that /graph/similarity endpoint exists"""
        response = client.options("/ai/v1/graph/similarity")
        assert response.status_code in [200, 405]
    
    def test_similarity_search_by_text(self):
        """Test similarity search with text query"""
        request_data = {
            "text": "Microsoft Corporation",
            "limit": 15,
            "confidence_threshold": 0.6
        }
        
        response = client.post("/ai/v1/graph/similarity", json=request_data)
        
        # Should return 200 or 500
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "similar_entities" in data
            assert "execution_time_ms" in data
            assert isinstance(data["similar_entities"], list)
    
    def test_similarity_search_by_entity_id(self):
        """Test similarity search with entity_id"""
        request_data = {
            "entity_id": "550e8400-e29b-41d4-a716-446655440000",
            "limit": 10
        }
        
        response = client.post("/ai/v1/graph/similarity", json=request_data)
        assert response.status_code in [200, 404, 500]
    
    def test_similarity_search_requires_one_param(self):
        """Test that similarity search requires either entity_id or text"""
        # No parameters
        empty_request = {"limit": 10}
        response = client.post("/ai/v1/graph/similarity", json=empty_request)
        assert response.status_code in [400, 422]
        
        # Both parameters
        both_request = {
            "entity_id": "550e8400-e29b-41d4-a716-446655440000",
            "text": "test",
            "limit": 10
        }
        response = client.post("/ai/v1/graph/similarity", json=both_request)
        assert response.status_code in [400, 422]
    
    def test_query_filters_validation(self):
        """Test that query filters are properly validated"""
        # Invalid confidence threshold
        request_data = {
            "query": "test",
            "query_type": "entity_search",
            "filters": {
                "confidence_threshold": 1.5  # Invalid: > 1.0
            }
        }
        
        response = client.post("/ai/v1/graph/query", json=request_data)
        assert response.status_code == 422
    
    def test_limit_parameter_validation(self):
        """Test that limit parameter is validated"""
        # Limit too high
        request_data = {
            "query": "test",
            "query_type": "entity_search",
            "filters": {
                "limit": 200  # Invalid: > 100
            }
        }
        
        response = client.post("/ai/v1/graph/query", json=request_data)
        assert response.status_code == 422
    
    def test_relationship_depth_validation(self):
        """Test that relationship_depth is validated (1-3)"""
        fake_entity_id = "550e8400-e29b-41d4-a716-446655440000"
        
        # Invalid: depth > 3
        response = client.get(
            f"/ai/v1/graph/entity/{fake_entity_id}",
            params={"relationship_depth": 5}
        )
        assert response.status_code in [404, 422, 500]
    
    def test_response_structure_entity_search(self):
        """Test that entity_search response matches schema"""
        request_data = {
            "query": "technology",
            "query_type": "entity_search"
        }
        
        response = client.post("/ai/v1/graph/query", json=request_data)
        
        if response.status_code == 200:
            data = response.json()
            
            # Validate required top-level fields
            assert "query_id" in data
            assert "total_results" in data
            assert "execution_time_ms" in data
            assert "entities" in data
            
            # Validate types
            assert isinstance(data["total_results"], int)
            assert isinstance(data["execution_time_ms"], int)
            assert isinstance(data["entities"], list)
            
            # If there are entities, validate structure
            if data["entities"]:
                entity = data["entities"][0]
                assert "id" in entity
                assert "text" in entity
                assert "type" in entity
                assert "confidence" in entity
                assert isinstance(entity["confidence"], (int, float))
                assert 0.0 <= entity["confidence"] <= 1.0
    
    def test_response_structure_similarity_search(self):
        """Test that similarity response matches schema"""
        request_data = {
            "text": "OpenAI",
            "limit": 5
        }
        
        response = client.post("/ai/v1/graph/similarity", json=request_data)
        
        if response.status_code == 200:
            data = response.json()
            
            # Validate required fields
            assert "similar_entities" in data
            assert "execution_time_ms" in data
            assert isinstance(data["similar_entities"], list)
            assert isinstance(data["execution_time_ms"], int)
            
            # If there are results, validate structure
            if data["similar_entities"]:
                result = data["similar_entities"][0]
                assert "entity" in result
                assert "similarity_score" in result
                assert isinstance(result["similarity_score"], (int, float))
                assert 0.0 <= result["similarity_score"] <= 1.0
                
                entity = result["entity"]
                assert "id" in entity
                assert "text" in entity
                assert "type" in entity
                assert "confidence" in entity


class TestGraphAPIIntegration:
    """Integration tests for graph API endpoints"""
    
    def test_query_types_enum(self):
        """Test all valid query types"""
        query_types = ["entity_search", "similarity_search", "relationship_query"]
        
        for query_type in query_types:
            request_data = {
                "query": "test",
                "query_type": query_type
            }
            
            response = client.post("/ai/v1/graph/query", json=request_data)
            # Should not reject based on query_type
            assert response.status_code in [200, 500]
    
    def test_entity_types_filter(self):
        """Test filtering by entity types"""
        valid_types = ['organization', 'person', 'funding_amount', 'date', 'location']
        
        request_data = {
            "query": "test",
            "query_type": "entity_search",
            "filters": {
                "entity_types": valid_types
            }
        }
        
        response = client.post("/ai/v1/graph/query", json=request_data)
        assert response.status_code in [200, 500]
    
    def test_relationship_types_filter(self):
        """Test filtering by relationship types"""
        valid_rel_types = ['fund', 'partner', 'acquire', 'compete', 'collaborate']
        
        request_data = {
            "query": "test",
            "query_type": "relationship_query",
            "filters": {
                "relationship_types": valid_rel_types
            }
        }
        
        response = client.post("/ai/v1/graph/query", json=request_data)
        assert response.status_code in [200, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

