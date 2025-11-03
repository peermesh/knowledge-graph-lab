#!/usr/bin/env python3
"""
Mock Demo - AI Module
Shows example JSON output showcasing flexible entity and relationship types
(Uses mock data to demonstrate the system without requiring LLM API calls)
"""

import json


def demo_example_1():
    """Tech Companies & Investment"""
    print()
    print("=" * 70)
    print("EXAMPLE 1: Tech Companies & Investment")
    print("=" * 70)
    print()
    
    input_data = {
        "content": "Microsoft invested $10 billion in OpenAI. Sam Altman is the CEO of OpenAI. The company competes with Anthropic.",
        "entity_types": None,  # Extract ALL types
        "relationship_types": None  # Identify ALL relationships
    }
    
    result = {
        "entities": [
            {"id": "e1", "text": "Microsoft", "type": "company", "confidence": 0.95},
            {"id": "e2", "text": "$10 billion", "type": "funding_amount", "confidence": 0.98},
            {"id": "e3", "text": "OpenAI", "type": "company", "confidence": 0.92},
            {"id": "e4", "text": "Sam Altman", "type": "person", "confidence": 0.94},
            {"id": "e5", "text": "Anthropic", "type": "company", "confidence": 0.89}
        ],
        "relationships": [
            {"source": "e1", "target": "e3", "type": "invested_in", "confidence": 0.96},
            {"source": "e4", "target": "e3", "type": "ceo_of", "confidence": 0.93},
            {"source": "e3", "target": "e5", "type": "competes_with", "confidence": 0.87}
        ],
        "stats": {
            "entities_extracted": 5,
            "relationships_found": 3,
            "unique_entity_types": 3,
            "processing_time_seconds": 2.45
        }
    }
    
    print(f"INPUT: {input_data['content']}\n")
    print("OUTPUT (JSON):")
    print(json.dumps(result, indent=2))
    print()
    
    print("GRAPH VISUALIZATION:")
    print("-" * 70)
    print("  Microsoft ──[invested_in]──> OpenAI ──[competes_with]──> Anthropic")
    print("                                  ↑")
    print("                                  │")
    print("                             [ceo_of]")
    print("                                  │")
    print("                              Sam Altman")
    print()


def demo_example_2():
    """Tech Stack with Custom Types"""
    print()
    print("=" * 70)
    print("EXAMPLE 2: Tech Stack (Custom Entity Types)")
    print("=" * 70)
    print()
    
    input_data = {
        "content": "React is a JavaScript framework developed by Meta. It uses TypeScript and deploys on Vercel.",
        "entity_types": ["framework", "language", "company", "platform"],  # Custom types!
        "relationship_types": ["developed_by", "uses", "deploys_on"]  # Custom types!
    }
    
    result = {
        "entities": [
            {"id": "e1", "text": "React", "type": "framework", "confidence": 0.92},
            {"id": "e2", "text": "JavaScript", "type": "language", "confidence": 0.88},
            {"id": "e3", "text": "Meta", "type": "company", "confidence": 0.95},
            {"id": "e4", "text": "TypeScript", "type": "language", "confidence": 0.89},
            {"id": "e5", "text": "Vercel", "type": "platform", "confidence": 0.86}
        ],
        "relationships": [
            {"source": "e1", "target": "e3", "type": "developed_by", "confidence": 0.93},
            {"source": "e1", "target": "e4", "type": "uses", "confidence": 0.87},
            {"source": "e1", "target": "e5", "type": "deploys_on", "confidence": 0.84}
        ],
        "stats": {
            "entities_extracted": 5,
            "relationships_found": 3,
            "unique_entity_types": 4,
            "processing_time_seconds": 1.82
        }
    }
    
    print(f"INPUT: {input_data['content']}\n")
    print(f"CUSTOM TYPES: {json.dumps(input_data['entity_types'])}\n")
    print("OUTPUT (JSON):")
    print(json.dumps(result, indent=2))
    print()
    
    print("GRAPH VISUALIZATION:")
    print("-" * 70)
    print("         ┌──[uses]──> TypeScript")
    print("         │")
    print("  React ─┼──[developed_by]──> Meta")
    print("         │")
    print("         └──[deploys_on]──> Vercel")
    print()


def demo_example_3():
    """AI Models"""
    print()
    print("=" * 70)
    print("EXAMPLE 3: AI Models (More Custom Types!)")
    print("=" * 70)
    print()
    
    input_data = {
        "content": "GPT-4 by OpenAI supports multimodal inputs. Claude 3 Opus by Anthropic excels at long context tasks.",
        "entity_types": ["model", "company", "capability"],  # Custom types!
        "relationship_types": ["developed_by", "supports", "excels_at"]  # Custom types!
    }
    
    result = {
        "entities": [
            {"id": "e1", "text": "GPT-4", "type": "model", "confidence": 0.93},
            {"id": "e2", "text": "OpenAI", "type": "company", "confidence": 0.95},
            {"id": "e3", "text": "multimodal inputs", "type": "capability", "confidence": 0.85},
            {"id": "e4", "text": "Claude 3 Opus", "type": "model", "confidence": 0.91},
            {"id": "e5", "text": "Anthropic", "type": "company", "confidence": 0.94},
            {"id": "e6", "text": "long context tasks", "type": "capability", "confidence": 0.87}
        ],
        "relationships": [
            {"source": "e1", "target": "e2", "type": "developed_by", "confidence": 0.94},
            {"source": "e1", "target": "e3", "type": "supports", "confidence": 0.88},
            {"source": "e4", "target": "e5", "type": "developed_by", "confidence": 0.92},
            {"source": "e4", "target": "e6", "type": "excels_at", "confidence": 0.86}
        ],
        "stats": {
            "entities_extracted": 6,
            "relationships_found": 4,
            "unique_entity_types": 3,
            "processing_time_seconds": 2.15
        }
    }
    
    print(f"INPUT: {input_data['content']}\n")
    print(f"CUSTOM TYPES: {json.dumps(input_data['entity_types'])}\n")
    print("OUTPUT (JSON):")
    print(json.dumps(result, indent=2))
    print()
    
    print("GRAPH VISUALIZATION:")
    print("-" * 70)
    print("  GPT-4 ──[developed_by]──> OpenAI")
    print("    │")
    print("    └──[supports]──> multimodal inputs")
    print()
    print("  Claude 3 Opus ──[developed_by]──> Anthropic")
    print("    │")
    print("    └──[excels_at]──> long context tasks")
    print()


def main():
    """Run all demo examples"""
    print()
    print("=" * 70)
    print("🚀 AI Module - Simple JSON Demo")
    print("=" * 70)
    print()
    print("This demonstrates the FLEXIBLE type system that accepts:")
    print("  ✅ ANY entity type (not just 5 hardcoded types)")
    print("  ✅ ANY relationship type (not just 6 hardcoded types)")
    print()
    
    demo_example_1()
    demo_example_2()
    demo_example_3()
    
    print()
    print("=" * 70)
    print("✨ KEY IMPROVEMENTS")
    print("=" * 70)
    print()
    print("BEFORE (Old System):")
    print("  ❌ Only 5 entity types: organization, person, funding_amount, date, location")
    print("  ❌ Only 6 relationship types: fund, partner, acquire, compete, collaborate, mention")
    print("  ❌ DATABASE had CHECK constraints enforcing hardcoded types")
    print("  ❌ API would REJECT custom types")
    print()
    print("AFTER (New System - What You Just Saw):")
    print("  ✅ Accepts ANY entity type!")
    print("  ✅ Accepts ANY relationship type!")
    print("  ✅ NO database constraints limiting types")
    print("  ✅ entity_types=None → extract ALL types")
    print("  ✅ relationship_types=None → identify ALL types")
    print()
    print("NEW TYPES DEMONSTRATED:")
    print("  Entity Types:")
    print("    • framework, language, company, platform")
    print("    • model, capability, funding_amount, person")
    print("  ")
    print("  Relationship Types:")
    print("    • invested_in, ceo_of, competes_with")
    print("    • developed_by, uses, deploys_on")
    print("    • supports, excels_at")
    print()
    print("=" * 70)
    print("🎯 TO USE THE REAL API:")
    print("=" * 70)
    print()
    print("1. Make sure API is running:")
    print("   uvicorn src.ai.api.main:app --reload")
    print()
    print("2. Open Swagger UI:")
    print("   http://localhost:8000/docs")
    print()
    print("3. Test POST /ai/v1/extract-entities with:")
    print(json.dumps({
        "document_id": "550e8400-e29b-41d4-a716-446655440000",
        "content": "Your text here",
        "document_type": "text",
        "extraction_config": {
            "entity_types": None,
            "relationship_types": None
        }
    }, indent=2))
    print()
    print("=" * 70)
    print("✅ Demo Complete!")
    print()


if __name__ == "__main__":
    main()

