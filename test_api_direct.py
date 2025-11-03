#!/usr/bin/env python3
"""
Direct API Test - Makes actual HTTP calls to the running API
Shows real JSON output from entity extraction
"""

import requests
import json
import uuid

API_URL = "http://localhost:8000"

def test_extraction(content, entity_types=None, relationship_types=None, description=""):
    """Test entity extraction via API"""
    print()
    print("=" * 70)
    print(description)
    print("=" * 70)
    print()
    
    # Prepare request
    payload = {
        "document_id": str(uuid.uuid4()),
        "content": content,
        "document_type": "text",
        "extraction_config": {
            "entity_types": entity_types,
            "relationship_types": relationship_types,
            "confidence_threshold": 0.7
        }
    }
    
    print("📝 REQUEST:")
    print(json.dumps(payload, indent=2))
    print()
    
    print("⏳ Sending to API...")
    
    try:
        response = requests.post(
            f"{API_URL}/ai/v1/extract-entities",
            json=payload,
            timeout=30
        )
        
        print(f"📡 Response Status: {response.status_code}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            
            # Show summary
            entities = data.get('entities', [])
            relationships = data.get('relationships', [])
            
            print("📊 SUMMARY:")
            print(f"   • Entities: {len(entities)}")
            print(f"   • Relationships: {len(relationships)}")
            print(f"   • Processing time: {data.get('processing_time_seconds', 0):.2f}s")
            print()
            
            # Show entities
            if entities:
                print("🏷️  ENTITIES:")
                print("-" * 70)
                for ent in entities:
                    print(f"  • {ent['text']} ({ent['type']}) - confidence: {ent['confidence']:.2f}")
                print()
            
            # Show relationships
            if relationships:
                print("🔗 RELATIONSHIPS:")
                print("-" * 70)
                
                # Create entity map
                entity_map = {e['id']: e['text'] for e in entities}
                
                for rel in relationships:
                    source = entity_map.get(rel['source_entity'], 'Unknown')
                    target = entity_map.get(rel['target_entity'], 'Unknown')
                    print(f"  • {source} ──[{rel['relationship_type']}]──> {target} (conf: {rel['confidence']:.2f})")
                print()
            
            # Simple graph
            if relationships:
                print("📈 GRAPH:")
                print("-" * 70)
                entity_map = {e['id']: e['text'] for e in entities}
                for rel in relationships:
                    source = entity_map.get(rel['source_entity'], 'Unknown')
                    target = entity_map.get(rel['target_entity'], 'Unknown')
                    print(f"  {source} ──[{rel['relationship_type']}]──> {target}")
                print()
            
            # Full JSON
            print("📄 FULL JSON RESPONSE:")
            print("=" * 70)
            print(json.dumps(data, indent=2))
            print()
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            print()
    
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to API")
        print(f"   Make sure the API is running at {API_URL}")
        print("   Run: uvicorn src.ai.api.main:app --reload")
        print()
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()


def main():
    """Run API tests"""
    print()
    print("=" * 70)
    print("🔗 Direct API Test - Real HTTP Calls")
    print("=" * 70)
    print()
    print(f"API URL: {API_URL}")
    print("This makes REAL HTTP calls to your running API")
    print()
    
    # Check if API is running
    print("🔍 Checking if API is running...")
    try:
        health_response = requests.get(f"{API_URL}/health", timeout=5)
        if health_response.status_code == 200:
            print(f"✅ API is running!")
            print(f"   {health_response.json()}")
            print()
        else:
            print(f"⚠️  API responded with status {health_response.status_code}")
            print()
    except:
        print("❌ API is NOT running!")
        print(f"   Start it with: uvicorn src.ai.api.main:app --reload")
        print()
        return
    
    # Test 1: Basic extraction
    test_extraction(
        content="Microsoft invested $10 billion in OpenAI. Sam Altman is the CEO.",
        entity_types=None,
        relationship_types=None,
        description="TEST 1: Extract ALL Types (Flexible!)"
    )
    
    # Test 2: Custom types
    test_extraction(
        content="React is a JavaScript framework developed by Meta.",
        entity_types=["framework", "language", "company"],
        relationship_types=["developed_by", "uses"],
        description="TEST 2: Custom Tech Types"
    )
    
    print()
    print("=" * 70)
    print("✅ API Testing Complete!")
    print("=" * 70)
    print()
    print("🎯 This showed REAL data extraction via HTTP API calls!")
    print("   All responses are actual JSON from the running API.")
    print()


if __name__ == "__main__":
    main()

