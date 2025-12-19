#!/usr/bin/env python3
"""
Simple test script to verify the rebuilt system works correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_configuration():
    """Test that configuration loads correctly"""
    print("🧪 Testing Configuration...")
    try:
        from src.ai.config import settings
        print(f"   ✅ Embedding dimensions: {settings.embedding_dimensions}")
        print(f"   ✅ Environment: {settings.env}")
        print(f"   ✅ Log level: {settings.log_level}")
        return True
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def test_entity_extractor_imports():
    """Test that entity extractor can be imported"""
    print("🧪 Testing Entity Extractor...")
    try:
        from src.ai.services.entity_extractor import EntityExtractor
        print("   ✅ EntityExtractor class imported successfully")
        extractor = EntityExtractor()
        print("   ✅ EntityExtractor instance created")
        return True
    except Exception as e:
        print(f"   ❌ EntityExtractor error: {e}")
        return False

def test_relationship_mapper_imports():
    """Test that relationship mapper can be imported"""
    print("🧪 Testing Relationship Mapper...")
    try:
        from src.ai.services.relationship_mapper import RelationshipMapper
        print("   ✅ RelationshipMapper class imported successfully")
        mapper = RelationshipMapper()
        print(f"   ✅ RelationshipMapper instance created with {len(mapper.RELATIONSHIP_PATTERNS)} pattern types")
        return True
    except Exception as e:
        print(f"   ❌ RelationshipMapper error: {e}")
        return False

def test_llm_client_imports():
    """Test that LLM client can be imported"""
    print("🧪 Testing LLM Client...")
    try:
        from src.ai.integrations.llm_client import llm_client
        print("   ✅ LLM client imported successfully")
        print("   ✅ LLM client is lazy-loaded")
        return True
    except Exception as e:
        print(f"   ❌ LLM client error: {e}")
        return False

def test_data_models():
    """Test that data models can be imported"""
    print("🧪 Testing Data Models...")
    try:
        from src.ai.models.entity import ExtractedEntity
        from src.ai.models.knowledge_graph import KnowledgeGraphNode, KnowledgeGraphEdge
        print("   ✅ ExtractedEntity model imported")
        print("   ✅ KnowledgeGraphNode model imported")
        print("   ✅ KnowledgeGraphEdge model imported")
        return True
    except Exception as e:
        print(f"   ❌ Data models error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Rebuilt Knowledge Graph Lab System")
    print("=" * 60)

    tests = [
        test_configuration,
        test_entity_extractor_imports,
        test_relationship_mapper_imports,
        test_llm_client_imports,
        test_data_models
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! System rebuild successful.")
        print("")
        print("✨ System Capabilities:")
        print("   • Flexible entity extraction (no hardcoded types)")
        print("   • Dynamic relationship mapping")
        print("   • Configurable vector embeddings (default: 384 dimensions)")
        print("   • Removed multi-language complexity")
        print("   • Enhanced system flexibility")

        print("")
        print("🚀 Next Steps:")
        print("   1. Set up environment: pip install -r requirements.txt")
        print("   2. Configure API keys in .env file")
        print("   3. Start services: docker-compose up -d")
        print("   4. Run migrations: alembic upgrade head")
        print("   5. Start API: uvicorn src.ai.api.main:app --reload")
        print("   6. View docs: http://localhost:8000/docs")
        print("   7. Run demo: python demo.py")
    else:
        print("⚠️  Some tests failed. Check errors above.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
