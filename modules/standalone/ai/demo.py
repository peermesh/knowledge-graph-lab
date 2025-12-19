#!/usr/bin/env python3
"""
Knowledge Graph Lab Demo - Updated according to new spec.md

This demo showcases the flexible entity extraction and knowledge graph system
with dynamic entity/relationship types and configurable embeddings.
"""


class KnowledgeGraphDemo:
    """Demo class showcasing the updated system capabilities"""

    def __init__(self):
        """Initialize demo"""
        self.sample_documents = [
            {
                "id": "doc_1",
                "title": "OpenAI Investment News",
                "content": """
                Microsoft has invested $10 billion in OpenAI, the artificial intelligence company
                founded by Elon Musk and Sam Altman in 2015. The partnership between Microsoft
                and OpenAI began in 2019 and has grown significantly over the years. This latest
                investment values OpenAI at $29 billion and represents Microsoft's largest AI bet.
                The companies will collaborate on developing advanced AI technologies that could
                revolutionize industries from healthcare to finance.
                """
            },
            {
                "id": "doc_2",
                "title": "Tech Partnership Announcement",
                "content": """
                Google and Anthropic have announced a strategic partnership to develop next-generation
                AI safety technologies. Anthropic, founded by former OpenAI researchers, will receive
                $2.7 billion in funding from Google over the next five years. The collaboration will
                focus on creating more reliable and ethical AI systems. This partnership comes as
                major tech companies compete for AI talent and market dominance.
                """
            },
            {
                "id": "doc_3",
                "title": "AI Competition Heats Up",
                "content": """
                xAI, founded by Elon Musk in 2023, has raised $6 billion in Series B funding.
                The company competes directly with OpenAI and Anthropic in the race to build
                artificial general intelligence. xAI's mission is to understand the true nature
                of the universe, and they have attracted top researchers from leading AI labs.
                The funding round was led by Andreessen Horowitz with participation from Sequoia Capital.
                """
            }
        ]


    def demo_flexible_extraction(self):
        """Demonstrate flexible entity extraction without hardcoded types"""
        print("📝 1. Flexible Entity Extraction")
        print("-" * 50)

        print("🔄 Before (Old System):")
        print("   • Restricted to 5 core entity types: organization, person, funding_amount, date, location")
        print("   • Hardcoded entity type validation")
        print("   • Limited to specific entity categories")

        print("")
        print("✨ After (New System):")
        print("   • No restrictions on entity types")
        print("   • Dynamic type detection from content")
        print("   • Supports any entity type: company, product, technology, event, etc.")

        print("")
        print("📊 Example extraction from sample document:")

        # Simulate flexible extraction results
        sample_entities = [
            {"text": "Microsoft", "type": "company", "confidence": 0.95},
            {"text": "OpenAI", "type": "company", "confidence": 0.92},
            {"text": "$10 billion", "type": "funding_amount", "confidence": 0.98},
            {"text": "Elon Musk", "type": "person", "confidence": 0.94},
            {"text": "Sam Altman", "type": "person", "confidence": 0.91},
            {"text": "2015", "type": "year", "confidence": 0.88},
            {"text": "artificial intelligence", "type": "technology", "confidence": 0.85},
            {"text": "healthcare", "type": "industry", "confidence": 0.82},
            {"text": "finance", "type": "industry", "confidence": 0.81}
        ]

        for entity in sample_entities:
            print(f"   • {entity['text']} ({entity['type']}) - {entity['confidence']:.2f}")

        print(f"\n   📈 Total: {len(sample_entities)} entities extracted with {len(set(e['type'] for e in sample_entities))} unique types")
        print("")

    def demo_dynamic_relationships(self):
        """Demonstrate dynamic relationship types"""
        print("🔗 2. Dynamic Relationship Types")
        print("-" * 50)

        print("🔄 Before (Old System):")
        print("   • Restricted to 6 core relationship types: fund, partner, acquire, compete, collaborate, mention")
        print("   • Hardcoded relationship validation")
        print("   • Limited relationship expressiveness")

        print("")
        print("✨ After (New System):")
        print("   • No restrictions on relationship types")
        print("   • Dynamic relationship discovery")
        print("   • Supports complex relationship types: invested_in, founded_by, competes_with, etc.")

        print("")
        print("📊 Example relationships from sample documents:")

        sample_relationships = [
            {"source": "Microsoft", "target": "OpenAI", "type": "invested_in", "confidence": 0.96},
            {"source": "Microsoft", "target": "OpenAI", "type": "partnered_with", "confidence": 0.94},
            {"source": "Elon Musk", "target": "OpenAI", "type": "founded", "confidence": 0.92},
            {"source": "Sam Altman", "target": "OpenAI", "type": "ceo_of", "confidence": 0.91},
            {"source": "Google", "target": "Anthropic", "type": "funded", "confidence": 0.89},
            {"source": "Google", "target": "Anthropic", "type": "partnered_with", "confidence": 0.87},
            {"source": "xAI", "target": "OpenAI", "type": "competes_with", "confidence": 0.85},
            {"source": "xAI", "target": "Anthropic", "type": "competes_with", "confidence": 0.83},
            {"source": "Elon Musk", "target": "xAI", "type": "founded", "confidence": 0.95},
        ]

        for rel in sample_relationships:
            print(f"   • {rel['source']} → {rel['target']} ({rel['type']}) - {rel['confidence']:.2f}")

        print(f"\n   📈 Total: {len(sample_relationships)} relationships with {len(set(r['type'] for r in sample_relationships))} unique types")
        print("")

    def demo_configurable_embeddings(self):
        """Demonstrate configurable embedding dimensions"""
        print("🧮 3. Configurable Vector Embeddings")
        print("-" * 50)

        print("🔄 Before (Old System):")
        print("   • Fixed 768-dimensional embeddings")
        print("   • Hardcoded vector dimensions in database schema")
        print("   • No flexibility for different embedding models")

        print("")
        print("✨ After (New System):")
        print("   • Configurable embedding dimensions (default: 384)")
        print("   • Dynamic vector dimensions in database")
        print("   • Support for different embedding models and sizes")

        print("")
        print("⚙️  Configuration Options:")
        print("   • embedding_dimensions: 384 (default, good balance of quality/speed)")
        print("   • Alternative options: 256 (faster), 512 (higher quality), 768 (maximum quality)")
        print("   • Configurable via environment variables or settings")

        print("")
        print("📊 Embedding Performance Comparison:")
        print("   • 256 dimensions: Fast search, lower memory usage")
        print("   • 384 dimensions: Balanced performance (recommended)")
        print("   • 512 dimensions: Higher accuracy, moderate resource usage")
        print("   • 768 dimensions: Maximum accuracy, higher resource usage")

        print("")

    def demo_system_architecture(self):
        """Show system architecture and capabilities"""
        print("🏗️  4. System Architecture")
        print("-" * 50)

        architecture = [
            "🎯 Core Components:",
            "   • Entity Extractor: Flexible type detection with confidence scoring",
            "   • Relationship Mapper: Dynamic relationship identification",
            "   • Knowledge Graph Builder: Scalable graph construction",
            "   • Vector Search: Configurable dimensional embeddings",
            "   • Graph Query Engine: Multi-hop relationship traversal",
            "",
            "🔧 Technical Features:",
            "   • Async processing with configurable concurrency",
            "   • Confidence-based filtering and quality monitoring",
            "   • RESTful API with OpenAPI documentation",
            "   • WebSocket support for real-time updates",
            "   • Rate limiting and error handling",
            "",
            "📈 Scalability:",
            "   • 100-200 documents/hour processing capacity",
            "   • 500+ concurrent queries support",
            "   • <5 seconds entity extraction latency (p95)",
            "   • <2 seconds graph query latency (p95)",
            "",
            "🛡️  Quality Assurance:",
            "   • Configurable confidence thresholds",
            "   • Processing performance monitoring",
            "   • Extraction accuracy tracking",
            "   • Automated quality reporting"
        ]

        for item in architecture:
            print(item)

        print("")


def main():
    """Main demo entry point"""
    print("🚀 Knowledge Graph Lab - Updated System Demo")
    print("=" * 70)

    demo = KnowledgeGraphDemo()

    # Run demo sections
    demo.demo_flexible_extraction()
    demo.demo_dynamic_relationships()
    demo.demo_configurable_embeddings()
    demo.demo_system_architecture()

    print("=" * 70)
    print("✅ Demo completed successfully!")
    print("")
    print("🎯 Key Improvements in Updated System:")
    print("   • Removed hardcoded entity type restrictions")
    print("   • Removed hardcoded relationship type limitations")
    print("   • Made embedding dimensions configurable (384 default)")
    print("   • Removed multi-language processing complexity")
    print("   • Simplified and made system more flexible")

    print("")
    print("🚀 Quick Start Instructions:")
    print("=" * 50)
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up environment: cp .env.example .env (add API keys)")
    print("3. Start services: docker-compose up -d")
    print("4. Run migrations: alembic upgrade head")
    print("5. Start API: uvicorn src.ai.api.main:app --reload")
    print("6. View docs: http://localhost:8000/docs")
    print("")
    print("🔗 API Endpoints:")
    print("   • POST /extract - Extract entities from documents")
    print("   • GET /graph/query - Query knowledge graph")
    print("   • GET /search/similar - Vector similarity search")
    print("   • GET /health - System health check")


if __name__ == "__main__":
    main()
