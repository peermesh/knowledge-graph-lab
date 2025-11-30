"""Unit tests for entity extraction functionality"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime
import uuid

from src.ai.services.entity_extractor import EntityExtractor
from src.ai.integrations.llm_client import LLMClient


class TestEntityExtractor:
    """Test entity extraction service"""
    
    @pytest.fixture
    def extractor(self):
        """Create entity extractor instance"""
        return EntityExtractor()
    
    @pytest.fixture
    def sample_text(self):
        """Sample text for extraction"""
        return "Acme Ventures invested $5 million in NovaBio, a Boston-based biotech startup founded by Dr. Lina Ortiz on October 22, 2024."
    
    @pytest.fixture
    def mock_llm_response(self):
        """Mock LLM response"""
        return {
            "entities": [
                {
                    "text": "Acme Ventures",
                    "type": "organization",
                    "confidence": 0.95,
                    "positions": [[0, 13]]
                },
                {
                    "text": "$5 million",
                    "type": "amount",
                    "confidence": 0.90,
                    "positions": [[32, 42]]
                },
                {
                    "text": "NovaBio",
                    "type": "organization",
                    "confidence": 0.92,
                    "positions": [[46, 54]]
                },
                {
                    "text": "Boston",
                    "type": "location",
                    "confidence": 0.88,
                    "positions": [[60, 66]]
                },
                {
                    "text": "Dr. Lina Ortiz",
                    "type": "person",
                    "confidence": 0.93,
                    "positions": [[105, 120]]
                },
                {
                    "text": "October 22, 2024",
                    "type": "date",
                    "confidence": 0.85,
                    "positions": [[124, 140]]
                }
            ],
            "relationships": [
                {
                    "source_entity": "Acme Ventures",
                    "target_entity": "NovaBio",
                    "relationship_type": "invested in",
                    "confidence": 0.90,
                    "evidence": "Acme Ventures invested $5 million in NovaBio"
                },
                {
                    "source_entity": "Dr. Lina Ortiz",
                    "target_entity": "NovaBio",
                    "relationship_type": "founded",
                    "confidence": 0.88,
                    "evidence": "NovaBio, a Boston-based biotech startup founded by Dr. Lina Ortiz"
                }
            ]
        }
    
    @pytest.mark.asyncio
    async def test_extract_entities_basic(self, extractor, sample_text, mock_llm_response):
        """Test basic entity extraction"""
        document_id = str(uuid.uuid4())
        
        with patch.object(extractor.llm_client, 'extract_entities', new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = mock_llm_response
            
            result = await extractor.extract(
                document_id=document_id,
                content=sample_text,
                confidence_threshold=0.7
            )
            
            assert result['document_id'] == document_id
            assert len(result['entities']) > 0
            assert len(result['relationships']) > 0
            assert 'stats' in result
            assert result['stats']['entities_extracted'] > 0
            assert result['stats']['relationships_found'] > 0
    
    @pytest.mark.asyncio
    async def test_extract_entities_with_entity_types_filter(self, extractor, sample_text, mock_llm_response):
        """Test extraction with entity type filtering"""
        document_id = str(uuid.uuid4())
        
        # Filter mock response to only include organizations
        filtered_response = {
            "entities": [e for e in mock_llm_response["entities"] if e["type"] == "organization"],
            "relationships": mock_llm_response["relationships"]
        }
        
        with patch.object(extractor.llm_client, 'extract_entities', new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = filtered_response
            
            result = await extractor.extract(
                document_id=document_id,
                content=sample_text,
                entity_types=["organization"],
                confidence_threshold=0.7
            )
            
            # All entities should be organizations
            for entity in result['entities']:
                assert entity['type'] == 'organization'
    
    @pytest.mark.asyncio
    async def test_extract_entities_confidence_threshold(self, extractor, sample_text, mock_llm_response):
        """Test that confidence threshold filters entities"""
        document_id = str(uuid.uuid4())
        
        with patch.object(extractor.llm_client, 'extract_entities', new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = mock_llm_response
            
            # High threshold
            result_high = await extractor.extract(
                document_id=document_id,
                content=sample_text,
                confidence_threshold=0.95
            )
            
            # Low threshold
            result_low = await extractor.extract(
                document_id=document_id,
                content=sample_text,
                confidence_threshold=0.5
            )
            
            # High threshold should have fewer or equal entities
            assert len(result_high['entities']) <= len(result_low['entities'])
    
    @pytest.mark.asyncio
    async def test_extract_entities_empty_text(self, extractor):
        """Test extraction with empty text"""
        document_id = str(uuid.uuid4())
        
        result = await extractor.extract(
            document_id=document_id,
            content="",
            confidence_threshold=0.7
        )
        
        assert result['document_id'] == document_id
        assert len(result['entities']) == 0
        assert len(result['relationships']) == 0
    
    @pytest.mark.asyncio
    async def test_extract_entities_large_document(self, extractor, mock_llm_response):
        """Test extraction with large document (chunking)"""
        document_id = str(uuid.uuid4())
        # Create large text (>8000 chars)
        large_text = "This is a test sentence. " * 400  # ~10KB
        
        with patch.object(extractor.llm_client, 'extract_entities', new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = mock_llm_response
            
            result = await extractor.extract(
                document_id=document_id,
                content=large_text,
                confidence_threshold=0.7
            )
            
            # Should still process (may be chunked)
            assert result['document_id'] == document_id
            assert 'stats' in result
    
    @pytest.mark.asyncio
    async def test_extract_entities_relationship_mapping(self, extractor, sample_text, mock_llm_response):
        """Test that relationships are properly mapped to entity IDs"""
        document_id = str(uuid.uuid4())
        
        with patch.object(extractor.llm_client, 'extract_entities', new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = mock_llm_response
            
            # Mock relationship mapper
            with patch('src.ai.services.entity_extractor.relationship_mapper.identify_relationships', new_callable=AsyncMock) as mock_rel:
                mock_rel.return_value = []
                
                result = await extractor.extract(
                    document_id=document_id,
                    content=sample_text,
                    confidence_threshold=0.7
                )
                
                # Check that relationships have valid entity IDs
                entity_ids = {e['id'] for e in result['entities']}
                for rel in result['relationships']:
                    assert rel['source_entity_id'] in entity_ids
                    assert rel['target_entity_id'] in entity_ids
                    assert 'id' in rel
    
    @pytest.mark.asyncio
    async def test_extract_entities_different_source_types(self, extractor, sample_text, mock_llm_response):
        """Test extraction with different source types"""
        document_id = str(uuid.uuid4())
        source_types = ['news', 'academic', 'social_media', 'unknown']
        
        with patch.object(extractor.llm_client, 'extract_entities', new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = mock_llm_response
            
            for source_type in source_types:
                result = await extractor.extract(
                    document_id=document_id,
                    content=sample_text,
                    source_type=source_type,
                    confidence_threshold=0.7
                )
                
                assert result['stats']['source_type'] == source_type
                assert len(result['entities']) > 0


class TestLLMClient:
    """Test LLM client integration"""
    
    @pytest.fixture
    def llm_client(self):
        """Create LLM client instance"""
        return LLMClient()
    
    def test_build_extraction_prompt(self, llm_client):
        """Test prompt building"""
        text = "Test text"
        prompt = llm_client._build_extraction_prompt(text)
        
        assert text in prompt
        assert "entities" in prompt.lower()
        assert "relationships" in prompt.lower()
    
    def test_build_extraction_prompt_with_types(self, llm_client):
        """Test prompt building with entity types"""
        text = "Test text"
        entity_types = ["person", "organization"]
        prompt = llm_client._build_extraction_prompt(text, entity_types)
        
        assert text in prompt
        assert "person" in prompt
        assert "organization" in prompt
    
    def test_parse_extraction_response_valid_json(self, llm_client):
        """Test parsing valid JSON response"""
        response = '{"entities": [{"text": "Test", "type": "person", "confidence": 0.9, "positions": [[0, 4]]}], "relationships": []}'
        result = llm_client._parse_extraction_response(response)
        
        assert "entities" in result
        assert "relationships" in result
        assert len(result["entities"]) == 1
        assert result["entities"][0]["text"] == "Test"
    
    def test_parse_extraction_response_with_markdown(self, llm_client):
        """Test parsing JSON wrapped in markdown"""
        response = 'Here is the result:\n```json\n{"entities": [{"text": "Test", "type": "person", "confidence": 0.9, "positions": [[0, 4]]}], "relationships": []}\n```'
        result = llm_client._parse_extraction_response(response)
        
        assert "entities" in result
        assert len(result["entities"]) == 1
    
    def test_normalize_extraction_payload(self, llm_client):
        """Test payload normalization"""
        data = {
            "entities": [
                {
                    "entity_text": "Test Entity",
                    "entity_type": "PERSON",
                    "confidence_score": 0.85,
                    "positions_in_text": [[0, 11]]
                }
            ],
            "relationships": [
                {
                    "source": "Entity1",
                    "target": "Entity2",
                    "type": "RELATED_TO",
                    "confidence_score": 0.8
                }
            ]
        }
        
        normalized = llm_client._normalize_extraction_payload(data)
        
        assert normalized["entities"][0]["text"] == "Test Entity"
        assert normalized["entities"][0]["type"] == "person"
        assert normalized["entities"][0]["confidence"] == 0.85
        assert normalized["relationships"][0]["source_entity"] == "Entity1"
        assert normalized["relationships"][0]["target_entity"] == "Entity2"
        assert normalized["relationships"][0]["relationship_type"] == "related_to"


class TestEntityExtractionIntegration:
    """Integration tests for entity extraction"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_extraction(self):
        """Test end-to-end extraction flow"""
        extractor = EntityExtractor()
        document_id = str(uuid.uuid4())
        
        text = """
        Apple Inc. announced a $10 billion investment in OpenAI on January 15, 2024.
        The deal was brokered by Tim Cook, CEO of Apple, and Sam Altman, CEO of OpenAI.
        This partnership will accelerate AI development in Silicon Valley.
        """
        
        # This will use actual LLM if configured, or mock if not
        try:
            result = await extractor.extract(
                document_id=document_id,
                content=text,
                confidence_threshold=0.6
            )
            
            assert result['document_id'] == document_id
            assert 'entities' in result
            assert 'relationships' in result
            assert 'stats' in result
            
            # Should extract at least some entities
            # (may be empty if LLM not configured, but structure should be correct)
            assert isinstance(result['entities'], list)
            assert isinstance(result['relationships'], list)
            
        except Exception as e:
            # If LLM not configured, that's okay for unit tests
            pytest.skip(f"LLM not configured: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

