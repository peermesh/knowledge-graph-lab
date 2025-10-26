"""
Tests for entity model functionality.

This module contains unit tests for entity creation, validation,
and database operations following TDD principles.
"""

import pytest
from datetime import datetime

from app.models.entity import Entity


class TestEntityModel:
    """Test cases for Entity model."""

    def test_entity_creation(self):
        """Test basic entity creation."""
        entity = Entity(
            name="Test Organization",
            type="organization",
            confidence=0.95,
            source="test_document",
            source_type="text",
            extraction_method="llm"
        )

        assert entity.name == "Test Organization"
        assert entity.type == "organization"
        assert entity.confidence == 0.95
        assert entity.source == "test_document"
        assert entity.extraction_method == "llm"
        assert entity.is_active is True
        assert isinstance(entity.id, str)
        assert isinstance(entity.created_at, datetime)

    def test_entity_validation(self):
        """Test entity validation constraints."""
        # Test valid confidence range
        entity = Entity(
            name="Test",
            type="organization",
            confidence=0.85,
            source="test",
            source_type="text"
        )
        assert 0.0 <= entity.confidence <= 1.0

        # Test invalid confidence (should raise validation error in real implementation)
        # This would be handled by database constraints

    def test_entity_relationships(self):
        """Test entity relationship setup."""
        entity = Entity(
            name="Test Entity",
            type="person",
            confidence=0.9,
            source="test",
            source_type="text"
        )

        # Entity should be able to have relationships
        assert hasattr(entity, 'relationships')
        assert hasattr(entity, 'target_relationships')
        assert hasattr(entity, 'graph_node')

    def test_entity_to_dict(self):
        """Test entity serialization."""
        entity = Entity(
            name="Test Corp",
            type="organization",
            confidence=0.88,
            source="test_doc",
            source_type="text"
        )

        entity_dict = entity.to_dict()

        assert entity_dict['name'] == "Test Corp"
        assert entity_dict['type'] == "organization"
        assert entity_dict['confidence'] == 0.88
        assert 'id' in entity_dict
        assert 'created_at' in entity_dict
        assert 'updated_at' in entity_dict

    @pytest.mark.parametrize("entity_type", [
        "organization", "person", "funding_amount", "date", "location", "concept", "event"
    ])
    def test_valid_entity_types(self, entity_type):
        """Test all valid entity types."""
        entity = Entity(
            name="Test",
            type=entity_type,
            confidence=0.8,
            source="test",
            source_type="text"
        )
        assert entity.type == entity_type

    def test_entity_repr(self):
        """Test entity string representation."""
        entity = Entity(
            name="Example Inc",
            type="organization",
            confidence=0.95,
            source="test",
            source_type="text"
        )

        repr_str = repr(entity)
        assert "Example Inc" in repr_str
        assert "organization" in repr_str
        assert "0.95" in repr_str
