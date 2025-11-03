#!/usr/bin/env python3
"""
Simple Demo - Knowledge Graph Lab
Shows entity extraction results as JSON (no frontend needed)
"""

import asyncio
import json
from datetime import datetime

print("=" * 70)
print("🧪 AI Module - Simple Demo (JSON Output)")
print("=" * 70)
print()

# Sample data to demonstrate the flexible type system
print("📝 Demonstrating Flexible Entity & Relationship Types")
print("-" * 70)
print()

# Example 1: Tech Companies
print("Example 1: Tech Companies & Investment")
print()
sample_text_1 = "Microsoft invested $10 billion in OpenAI. Sam Altman is the CEO of OpenAI."

result_1 = {
    "document_id": "demo-001",
    "content": sample_text_1,
    "extraction_config": {
        "entity_types": None,  # Extract ALL types (flexible!)
        "relationship_types": None  # Identify ALL types (flexible!)
    },
    "results": {
        "entities": [
            {
                "id": "entity-1",
                "text": "Microsoft",
                "type": "company",  # Custom type!
                "confidence": 0.95,
                "positions": [[0, 9]]
            },
            {
                "id": "entity-2",
                "text": "$10 billion",
                "type": "funding_amount",  # Custom type!
                "confidence": 0.98,
                "positions": [[19, 30]]
            },
            {
                "id": "entity-3",
                "text": "OpenAI",
                "type": "company",  # Custom type!
                "confidence": 0.92,
                "positions": [[34, 40]]
            },
            {
                "id": "entity-4",
                "text": "Sam Altman",
                "type": "person",
                "confidence": 0.94,
                "positions": [[42, 52]]
            }
        ],
        "relationships": [
            {
                "id": "rel-1",
                "source_entity": "entity-1",
                "target_entity": "entity-3",
                "relationship_type": "invested_in",  # Custom type!
                "confidence": 0.96,
                "evidence": "Microsoft invested $10 billion in OpenAI"
            },
            {
                "id": "rel-2",
                "source_entity": "entity-4",
                "target_entity": "entity-3",
                "relationship_type": "ceo_of",  # Custom type!
                "confidence": 0.93,
                "evidence": "Sam Altman is the CEO of OpenAI"
            }
        ],
        "stats": {
            "entities_extracted": 4,
            "relationships_found": 2,
            "unique_entity_types": 3,
            "processing_time": 0.15
        }
    }
}

print(json.dumps(result_1, indent=2))
print()
print("✨ Notice: Custom types like 'company', 'funding_amount', 'ceo_of'")
print("   These would have been REJECTED by the old system!")
print()
print("-" * 70)
print()

# Example 2: Tech Stack
print("Example 2: Tech Stack & Frameworks")
print()
sample_text_2 = "React is a JavaScript framework developed by Meta. It uses TypeScript."

result_2 = {
    "document_id": "demo-002",
    "content": sample_text_2,
    "extraction_config": {
        "entity_types": ["framework", "language", "company", "technology"],
        "relationship_types": ["developed_by", "uses"]
    },
    "results": {
        "entities": [
            {
                "id": "entity-1",
                "text": "React",
                "type": "framework",  # Custom type!
                "confidence": 0.92
            },
            {
                "id": "entity-2",
                "text": "JavaScript",
                "type": "language",  # Custom type!
                "confidence": 0.88
            },
            {
                "id": "entity-3",
                "text": "Meta",
                "type": "company",
                "confidence": 0.95
            },
            {
                "id": "entity-4",
                "text": "TypeScript",
                "type": "language",  # Custom type!
                "confidence": 0.89
            }
        ],
        "relationships": [
            {
                "id": "rel-1",
                "source_entity": "entity-1",
                "target_entity": "entity-3",
                "relationship_type": "developed_by",  # Custom type!
                "confidence": 0.93
            },
            {
                "id": "rel-2",
                "source_entity": "entity-1",
                "target_entity": "entity-4",
                "relationship_type": "uses",  # Custom type!
                "confidence": 0.87
            }
        ],
        "stats": {
            "entities_extracted": 4,
            "relationships_found": 2,
            "unique_entity_types": 3,
            "processing_time": 0.12
        }
    }
}

print(json.dumps(result_2, indent=2))
print()
print("✨ Notice: 'framework', 'language', 'developed_by', 'uses'")
print("   Old system would REJECT these custom types!")
print()
print("-" * 70)
print()

# Summary
print("📊 SUMMARY: Flexible Type System")
print("=" * 70)
print()
print("OLD SYSTEM (Before Rebuild):")
print("  ❌ Only 5 entity types: organization, person, funding_amount, date, location")
print("  ❌ Only 6 relationship types: fund, partner, acquire, compete, collaborate, mention")
print("  ❌ Database CHECK constraints enforced hardcoded types")
print("  ❌ Would ERROR on any custom type")
print()
print("NEW SYSTEM (After Rebuild):")
print("  ✅ Accepts ANY entity type!")
print("  ✅ Accepts ANY relationship type!")
print("  ✅ NO database constraints limiting types")
print("  ✅ entity_types=None → extract ALL types")
print("  ✅ relationship_types=None → identify ALL types")
print()
print("EXAMPLES OF NEW TYPES THAT NOW WORK:")
print("  Entity Types:")
print("    • framework, library, language, technology")
print("    • model, capability, architecture, metric")
print("    • investor, valuation, funding_round")
print("    • platform, tool, product, concept")
print("  ")
print("  Relationship Types:")
print("    • developed_by, uses, depends_on, built_with")
print("    • supports, excels_at, processes")
print("    • invested_in, valued_at, led_round")
print("    • competes_with, founded_by, ceo_of")
print()
print("=" * 70)
print()

# ASCII Graph visualization
print("📈 SIMPLE GRAPH VISUALIZATION")
print("=" * 70)
print()
print("Example 1: Investment Graph")
print()
print("  Microsoft ──[invested_in]──> OpenAI")
print("                                  ↑")
print("                                  │")
print("                             [ceo_of]")
print("                                  │")
print("                              Sam Altman")
print()
print("Example 2: Tech Stack Graph")
print()
print("  React ──[developed_by]──> Meta")
print("    │")
print("    │ [uses]")
print("    ↓")
print("  TypeScript")
print()
print("=" * 70)
print()

# Show API endpoint
print("🔗 TO USE WITH REAL API:")
print("=" * 70)
print()
print("1. Make sure API is running:")
print("   uvicorn src.ai.api.main:app --reload")
print()
print("2. Test with curl:")
print("""   curl -X POST http://localhost:8000/ai/v1/extract-entities \\
     -H "Content-Type: application/json" \\
     -d '{
       "document_id": "test-001",
       "content": "Microsoft invested $10B in OpenAI",
       "document_type": "text",
       "extraction_config": {
         "entity_types": null,
         "relationship_types": null
       }
     }'""")
print()
print("3. Or use Swagger UI:")
print("   http://localhost:8000/docs")
print()
print("=" * 70)
print()
print("✅ Demo Complete!")
print()

