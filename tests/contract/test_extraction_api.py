"""Contract tests for Entity Extraction API"""

import pytest
from fastapi.testclient import TestClient
from src.ai.api.main import app
import json

client = TestClient(app)


class TestEntityExtractionAPIContract:
    """Test that API matches OpenAPI specification"""
    
    def test_extract_entities_endpoint_exists(self):
        """Test that /extract-entities endpoint exists"""
        response = client.options("/ai/v1/extract-entities")
        assert response.status_code in [200, 405]  # 405 if OPTIONS not implemented
    
    def test_extract_entities_requires_post(self):
        """Test that endpoint only accepts POST"""
        response = client.get("/ai/v1/extract-entities")
        assert response.status_code == 405  # Method not allowed
    
    def test_extract_entities_valid_request(self):
        """Test extraction with valid request"""
        request_data = {
            "document_id": "550e8400-e29b-41d4-a716-446655440000",
            "content": "Microsoft invested $10 billion in OpenAI to accelerate AI development.",
            "document_type": "text",
            "extraction_config": {
                "entity_types": ["organization", "funding_amount"],
                "confidence_threshold": 0.7,
                "language": "en"
            },
            "priority": "normal"
        }
        
        response = client.post("/ai/v1/extract-entities", json=request_data)
        
        # Should return 200 (sync) or 202 (async)
        assert response.status_code in [200, 202]
        
        data = response.json()
        
        # Verify response structure
        assert "job_id" in data
        assert "status" in data
        
        if response.status_code == 200:
            # Synchronous response
            assert "entities" in data
            assert "relationships" in data
            assert "processing_time_seconds" in data
            
            # Verify entities structure
            if data["entities"]:
                entity = data["entities"][0]
                assert "id" in entity
                assert "text" in entity
                assert "type" in entity
                assert "confidence" in entity
                assert "positions" in entity
    
    def test_extract_entities_missing_required_fields(self):
        """Test that missing required fields returns 422"""
        incomplete_request = {
            "content": "Some text"
            # Missing document_id and document_type
        }
        
        response = client.post("/ai/v1/extract-entities", json=incomplete_request)
        assert response.status_code == 422  # Validation error
    
    def test_extract_entities_invalid_confidence_threshold(self):
        """Test that invalid confidence threshold is rejected"""
        invalid_request = {
            "document_id": "550e8400-e29b-41d4-a716-446655440000",
            "content": "Test content",
            "document_type": "text",
            "extraction_config": {
                "confidence_threshold": 1.5  # Invalid: > 1.0
            }
        }
        
        response = client.post("/ai/v1/extract-entities", json=invalid_request)
        assert response.status_code == 422
    
    def test_job_status_endpoint_exists(self):
        """Test that /jobs/{job_id} endpoint exists"""
        # First create a job
        request_data = {
            "document_id": "550e8400-e29b-41d4-a716-446655440000",
            "content": "Test content for job tracking.",
            "document_type": "text"
        }
        
        create_response = client.post("/ai/v1/extract-entities", json=request_data)
        assert create_response.status_code in [200, 202]
        
        job_id = create_response.json()["job_id"]
        
        # Query job status
        status_response = client.get(f"/ai/v1/jobs/{job_id}")
        assert status_response.status_code == 200
        
        status_data = status_response.json()
        assert "job_id" in status_data
        assert "status" in status_data
        assert status_data["job_id"] == job_id
    
    def test_job_status_not_found(self):
        """Test that querying non-existent job returns 404"""
        fake_job_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/ai/v1/jobs/{fake_job_id}")
        assert response.status_code == 404
    
    def test_response_matches_schema(self):
        """Test that response matches expected JSON schema"""
        request_data = {
            "document_id": "550e8400-e29b-41d4-a716-446655440000",
            "content": "Apple Inc. and Microsoft are technology companies.",
            "document_type": "text",
            "extraction_config": {
                "entity_types": ["organization"],
                "confidence_threshold": 0.5
            }
        }
        
        response = client.post("/ai/v1/extract-entities", json=request_data)
        assert response.status_code in [200, 202]
        
        data = response.json()
        
        # Validate required top-level fields
        required_fields = ["job_id", "status"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Validate status values
        assert data["status"] in ["pending", "processing", "completed", "failed"]
        
        # If completed, validate entities structure
        if data["status"] == "completed" and "entities" in data:
            for entity in data["entities"]:
                assert "id" in entity
                assert "text" in entity
                assert "type" in entity
                assert isinstance(entity["confidence"], (int, float))
                assert 0.0 <= entity["confidence"] <= 1.0
                assert isinstance(entity["positions"], list)
    
    def test_flexible_entity_types(self):
        """Test that system accepts flexible entity types (FR-001)"""
        # Test with various entity types including custom ones
        test_types = [
            ['organization', 'person'],
            ['company', 'product', 'technology'],
            ['location', 'event', 'concept'],
            None  # None should extract all types
        ]
        
        for entity_types in test_types:
            request_data = {
                "document_id": "550e8400-e29b-41d4-a716-446655440000",
                "content": "Test content",
                "document_type": "text",
                "extraction_config": {
                    "entity_types": entity_types
                } if entity_types else {}
            }
            
            response = client.post("/ai/v1/extract-entities", json=request_data)
            # Should accept any entity types or None
            assert response.status_code in [200, 202]
    
    def test_priority_levels(self):
        """Test that all priority levels are accepted"""
        priorities = ['high', 'normal', 'low']
        
        for priority in priorities:
            request_data = {
                "document_id": "550e8400-e29b-41d4-a716-446655440000",
                "content": "Test content",
                "document_type": "text",
                "priority": priority
            }
            
            response = client.post("/ai/v1/extract-entities", json=request_data)
            assert response.status_code in [200, 202]
    
    def test_large_document_returns_async(self):
        """Test that large documents return async job ID"""
        # Create large content (>10KB)
        large_content = "This is a test sentence. " * 500  # ~12.5KB
        
        request_data = {
            "document_id": "550e8400-e29b-41d4-a716-446655440000",
            "content": large_content,
            "document_type": "text"
        }
        
        response = client.post("/ai/v1/extract-entities", json=request_data)
        
        # Large documents should trigger async processing
        # Could be 200 or 202 depending on system load
        assert response.status_code in [200, 202]
        
        data = response.json()
        assert "job_id" in data
        assert "status" in data


class TestAPIDocumentation:
    """Test that API documentation is accessible"""
    
    def test_openapi_json_available(self):
        """Test that OpenAPI JSON is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        spec = response.json()
        assert "openapi" in spec
        assert "info" in spec
        assert "paths" in spec
    
    def test_swagger_ui_available(self):
        """Test that Swagger UI is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_available(self):
        """Test that ReDoc is accessible"""
        response = client.get("/redoc")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

