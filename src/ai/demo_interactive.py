#!/usr/bin/env python3
"""
Interactive Demo - AI Module
Simple JSON output demo showcasing flexible entity and relationship extraction
"""

import asyncio
import json
import sys
from typing import Dict, Any, List

# Add parent to path
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.ai.services.entity_extractor import entity_extractor
from src.ai.lib.deduplication import deduplicate_entities, update_relationship_entity_ids


async def demo_extraction(
    content: str,
    entity_types: List[str] = None,
    relationship_types: List[str] = None,
    show_json: bool = True
):
    """
    Run entity extraction and display results
    
    Args:
        content: Text to analyze
        entity_types: List of entity types or None for all
        relationship_types: List of relationship types or None for all
        show_json: Whether to display full JSON output
    """
    print()
    print("📝 INPUT:")
    print("-" * 70)
    print(f"Content: {content}")
    print(f"Entity Types: {entity_types if entity_types else 'ALL (flexible)'}")
    print(f"Relationship Types: {relationship_types if relationship_types else 'ALL (flexible)'}")
    print()
    
    try:
        # Extract entities
        print("⏳ Extracting entities...")
        result = await entity_extractor.extract(
            document_id="demo-doc-001",
            content=content,
            entity_types=entity_types,
            relationship_types=relationship_types,
            confidence_threshold=0.7,
            source_type="unknown"
        )
        
        # Deduplicate
        deduplicated_entities, id_mapping = deduplicate_entities(
            result['entities'],
            similarity_threshold=0.85
        )
        
        updated_relationships = update_relationship_entity_ids(
            result['relationships'],
            id_mapping
        )
        
        # Show results
        print("✅ EXTRACTION COMPLETE!")
        print("=" * 70)
        print()
        
        # Simple summary
        print(f"📊 SUMMARY:")
        print(f"   • Entities extracted: {len(deduplicated_entities)}")
        print(f"   • Relationships found: {len(updated_relationships)}")
        print(f"   • Unique entity types: {len(set(e['type'] for e in deduplicated_entities))}")
        print(f"   • Processing time: {result['stats']['processing_time_seconds']:.2f}s")
        print()
        
        # Show entities
        print("🏷️  ENTITIES:")
        print("-" * 70)
        for i, entity in enumerate(deduplicated_entities, 1):
            print(f"{i}. {entity['text']}")
            print(f"   Type: {entity['type']}")
            print(f"   Confidence: {entity['confidence']:.2f}")
            print()
        
        # Show relationships
        if updated_relationships:
            print("🔗 RELATIONSHIPS:")
            print("-" * 70)
            
            # Create entity ID to text mapping
            entity_map = {e['id']: e['text'] for e in deduplicated_entities}
            
            for i, rel in enumerate(updated_relationships, 1):
                source_text = entity_map.get(rel['source_entity_id'], 'Unknown')
                target_text = entity_map.get(rel['target_entity_id'], 'Unknown')
                print(f"{i}. {source_text} ──[{rel['relationship_type']}]──> {target_text}")
                print(f"   Confidence: {rel['confidence']:.2f}")
                if rel.get('evidence'):
                    evidence = rel['evidence'][:100] + '...' if len(rel['evidence']) > 100 else rel['evidence']
                    print(f"   Evidence: {evidence}")
                print()
        else:
            print("🔗 RELATIONSHIPS: None found")
            print()
        
        # ASCII Graph
        if updated_relationships:
            print("📈 GRAPH VISUALIZATION:")
            print("-" * 70)
            entity_map = {e['id']: e['text'] for e in deduplicated_entities}
            
            for rel in updated_relationships:
                source = entity_map.get(rel['source_entity_id'], 'Unknown')
                target = entity_map.get(rel['target_entity_id'], 'Unknown')
                rel_type = rel['relationship_type']
                print(f"  {source} ──[{rel_type}]──> {target}")
            print()
        
        # Full JSON output
        if show_json:
            print("📄 FULL JSON OUTPUT:")
            print("=" * 70)
            output = {
                "entities": deduplicated_entities,
                "relationships": updated_relationships,
                "stats": result['stats']
            }
            print(json.dumps(output, indent=2))
            print()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        import traceback
        traceback.print_exc()


async def main():
    """Run interactive demo"""
    print("=" * 70)
    print("🚀 AI Module - Interactive Demo")
    print("=" * 70)
    print()
    print("This demo showcases the flexible entity and relationship extraction")
    print("system that accepts ANY entity type and ANY relationship type!")
    print()
    
    # Example 1: Tech companies
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Tech Companies & Investment")
    print("=" * 70)
    
    await demo_extraction(
        content="Microsoft invested $10 billion in OpenAI. Sam Altman is the CEO of OpenAI. The company competes with Anthropic.",
        entity_types=None,  # Extract ALL types
        relationship_types=None,  # Identify ALL relationships
        show_json=False
    )
    
    # Example 2: Tech stack
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Tech Stack with Custom Types")
    print("=" * 70)
    
    await demo_extraction(
        content="React is a JavaScript framework developed by Meta. It uses TypeScript and deploys on Vercel.",
        entity_types=["framework", "language", "company", "platform"],
        relationship_types=["developed_by", "uses", "deploys_on"],
        show_json=False
    )
    
    # Example 3: AI Models
    print("\n" + "=" * 70)
    print("EXAMPLE 3: AI Models & Capabilities")
    print("=" * 70)
    
    await demo_extraction(
        content="GPT-4 by OpenAI supports multimodal inputs. Claude 3 by Anthropic excels at long context.",
        entity_types=["model", "company", "capability"],
        relationship_types=["developed_by", "supports", "excels_at"],
        show_json=False
    )
    
    # Summary
    print("\n" + "=" * 70)
    print("✨ WHAT MAKES THIS SPECIAL")
    print("=" * 70)
    print()
    print("OLD SYSTEM (Before Rebuild):")
    print("  ❌ Only 5 hardcoded entity types")
    print("  ❌ Only 6 hardcoded relationship types")
    print("  ❌ Would REJECT custom types like 'framework', 'platform'")
    print()
    print("NEW SYSTEM (After Rebuild):")
    print("  ✅ Accepts ANY entity type!")
    print("  ✅ Accepts ANY relationship type!")
    print("  ✅ entity_types=None extracts ALL types")
    print("  ✅ relationship_types=None identifies ALL types")
    print()
    print("TYPES DEMONSTRATED:")
    print("  • company, person, framework, language, platform")
    print("  • model, capability, funding_amount")
    print("  • invested_in, ceo_of, competes_with")
    print("  • developed_by, uses, deploys_on, supports, excels_at")
    print()
    print("=" * 70)
    print("✅ Demo Complete!")
    print()


if __name__ == "__main__":
    asyncio.run(main())

