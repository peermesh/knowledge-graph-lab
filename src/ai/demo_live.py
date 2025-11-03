#!/usr/bin/env python3
"""
Live Demo - AI Module
Real entity extraction using actual API calls (not mock data)
"""

import asyncio
import json
import sys
import os
import uuid

# Add parent to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.ai.services.entity_extractor import entity_extractor
from src.ai.lib.deduplication import deduplicate_entities, update_relationship_entity_ids


def print_header(title):
    """Print formatted header"""
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)
    print()


def visualize_graph(entities, relationships):
    """Create simple ASCII graph visualization"""
    print("📈 GRAPH VISUALIZATION:")
    print("-" * 70)
    
    if not relationships:
        print("  (No relationships found)")
        print()
        return
    
    # Create entity ID to text mapping
    entity_map = {e['id']: e['text'] for e in entities}
    
    # Simple linear graph
    for rel in relationships:
        source = entity_map.get(rel['source_entity_id'], 'Unknown')
        target = entity_map.get(rel['target_entity_id'], 'Unknown')
        rel_type = rel['relationship_type']
        conf = rel['confidence']
        print(f"  {source} ──[{rel_type}]──> {target} (confidence: {conf:.2f})")
    
    print()


async def extract_and_display(
    content: str,
    entity_types=None,
    relationship_types=None,
    show_full_json=False
):
    """Extract entities from real content and display results"""
    
    print("📝 INPUT:")
    print("-" * 70)
    print(f"Text: {content}")
    print(f"Entity types: {entity_types if entity_types else 'ALL (flexible)'}")
    print(f"Relationship types: {relationship_types if relationship_types else 'ALL (flexible)'}")
    print()
    
    print("⏳ Extracting entities using LLM...")
    
    try:
        # Call real entity extractor
        result = await entity_extractor.extract(
            document_id=str(uuid.uuid4()),
            content=content,
            entity_types=entity_types,
            relationship_types=relationship_types,
            confidence_threshold=0.7,
            source_type="unknown"
        )
        
        # Deduplicate entities
        deduplicated_entities, id_mapping = deduplicate_entities(
            result['entities'],
            similarity_threshold=0.85
        )
        
        # Update relationship IDs
        updated_relationships = update_relationship_entity_ids(
            result['relationships'],
            id_mapping
        )
        
        print("✅ EXTRACTION COMPLETE!")
        print()
        
        # Show summary stats
        print("📊 SUMMARY:")
        print(f"   • Entities extracted: {len(deduplicated_entities)}")
        print(f"   • Relationships found: {len(updated_relationships)}")
        unique_types = len(set(e['type'] for e in deduplicated_entities))
        print(f"   • Unique entity types: {unique_types}")
        print(f"   • Processing time: {result['stats']['processing_time_seconds']:.2f}s")
        print()
        
        # Show entities
        if deduplicated_entities:
            print("🏷️  ENTITIES:")
            print("-" * 70)
            for i, entity in enumerate(deduplicated_entities, 1):
                print(f"{i}. {entity['text']}")
                print(f"   Type: {entity['type']}")
                print(f"   Confidence: {entity['confidence']:.2f}")
                print()
        else:
            print("🏷️  ENTITIES: None found")
            print()
        
        # Show relationships
        if updated_relationships:
            print("🔗 RELATIONSHIPS:")
            print("-" * 70)
            
            # Create entity map
            entity_map = {e['id']: e for e in deduplicated_entities}
            
            for i, rel in enumerate(updated_relationships, 1):
                source_entity = entity_map.get(rel['source_entity_id'])
                target_entity = entity_map.get(rel['target_entity_id'])
                
                if source_entity and target_entity:
                    print(f"{i}. {source_entity['text']} ──[{rel['relationship_type']}]──> {target_entity['text']}")
                    print(f"   Confidence: {rel['confidence']:.2f}")
                    if rel.get('evidence'):
                        evidence = rel['evidence'][:80] + '...' if len(rel['evidence']) > 80 else rel['evidence']
                        print(f"   Evidence: \"{evidence}\"")
                    print()
        else:
            print("🔗 RELATIONSHIPS: None found")
            print()
        
        # ASCII Graph
        visualize_graph(deduplicated_entities, updated_relationships)
        
        # Full JSON if requested
        if show_full_json:
            print("📄 FULL JSON OUTPUT:")
            print("=" * 70)
            output = {
                "entities": deduplicated_entities,
                "relationships": updated_relationships,
                "stats": result['stats']
            }
            print(json.dumps(output, indent=2))
            print()
        
        return result
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        import traceback
        traceback.print_exc()
        return None


async def main():
    """Run live demo"""
    print_header("🚀 AI Module - Live Demo (Real Extraction)")
    
    print("This demo uses REAL entity extraction with your actual API keys!")
    print("It demonstrates the flexible type system that accepts ANY types.")
    print()
    
    # Check if LLM is available
    from src.ai.config import settings
    if not settings.openai_api_key and not settings.anthropic_api_key:
        print("⚠️  WARNING: No LLM API keys found in .env")
        print("   Add OPENAI_API_KEY or ANTHROPIC_API_KEY to enable extraction")
        print()
        return
    
    print("✅ LLM API key detected - ready to extract!")
    print()
    
    # Example 1: Basic extraction (all types)
    print_header("EXAMPLE 1: Extract ALL Types (entity_types=None)")
    
    await extract_and_display(
        content="Microsoft invested $10 billion in OpenAI. Sam Altman is the CEO.",
        entity_types=None,
        relationship_types=None,
        show_full_json=False
    )
    
    # Example 2: Custom tech types
    print_header("EXAMPLE 2: Custom Tech Types")
    
    await extract_and_display(
        content="React is a JavaScript framework developed by Meta. It uses TypeScript.",
        entity_types=["framework", "language", "company"],
        relationship_types=["developed_by", "uses"],
        show_full_json=False
    )
    
    # Example 3: With full JSON
    print_header("EXAMPLE 3: Full JSON Output")
    
    await extract_and_display(
        content="GPT-4 by OpenAI competes with Claude by Anthropic.",
        entity_types=["model", "company"],
        relationship_types=["competes_with", "developed_by"],
        show_full_json=True
    )
    
    # Summary
    print_header("✨ SUMMARY")
    print("You just saw REAL entity extraction with:")
    print("  ✅ Flexible entity types (ANY type accepted)")
    print("  ✅ Dynamic relationship types (ANY type accepted)")
    print("  ✅ Live LLM processing")
    print("  ✅ Confidence scoring")
    print("  ✅ Simple JSON output")
    print("  ✅ ASCII graph visualization")
    print()
    print("🎯 All data is REAL - extracted by the AI module you just rebuilt!")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Demo stopped. Goodbye!")

