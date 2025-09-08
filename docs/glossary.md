# Glossary

## Project Terms

**Knowledge Graph Lab (KGL)**: The complete AI research platform project demonstrating PeerMesh's modular architecture philosophy through autonomous knowledge discovery in the creator economy.

**PeerMesh**: The parent organization's vision for modular, composable AI systems that can work independently or together.

**Creator Economy**: The economic ecosystem of independent content creators, including platforms, tools, funding opportunities, and support systems.

## Core Technical Concepts

**Claim**: Structured statement with predicate/value and confidence score for knowledge representation.

**Evidence**: Source metadata including URL, publisher, excerpt hash, and timestamp for claim verification.

**Ontology**: Domain schema defining types, predicates, and constraints layered over a stable meta-schema.

**Living Ontology**: Versioned, auditable evolution of the domain schema allowing controlled growth.

**Neuro-symbolic**: Hybrid approach combining rules/constraints with embeddings/LLMs for reasoning.

**Graph-aware RAG**: Retrieval-augmented generation guided by graph structure (communities/paths) with reflection/correction.

## AI/ML Terms

**Entity Extraction**: The process of identifying and extracting named entities (people, organizations, locations, etc.) from unstructured text.

**Entity Resolution**: The process of determining when different entity mentions refer to the same real-world entity.

**Knowledge Graph**: A structured representation of entities and their relationships, typically stored in a graph database.

**NER (Named Entity Recognition)**: AI technique for identifying and classifying named entities in text.

**Frontier Queue**: A prioritized list of items to research next, managed by the reasoning engine.

**Topic Clustering**: Grouping related content or entities based on similarity metrics.

## Architecture Terms

**Module**: An independent, self-contained component of the system that provides specific functionality.

**Adapter Pattern**: Design pattern for pluggable source adapters that normalize different data formats.

**Repository Pattern**: Abstraction layer between business logic and data access.

**API Gateway**: Single entry point for all client requests to backend services.

## Development Terms

**Tier 1/2 Implementation**: Phased development approach with basic features (Tier 1) followed by enhanced features (Tier 2).

**Mock Interface**: Simulated API responses used during development when actual services aren't available.

**Docker Compose**: Tool for defining and running multi-container Docker applications.

**FastAPI**: Modern Python web framework for building APIs.

**Next.js**: React framework for production-grade web applications.

## Module-Specific Terms

### Module 1: Data Ingestion
**Source Adapter**: Component that fetches and normalizes data from a specific source type.

**Rate Limiting**: Controlling the frequency of requests to external services.

**robots.txt**: File that specifies which parts of a website can be crawled.

**Content Normalization**: Converting diverse data formats into a consistent schema.

### Module 2: Knowledge Graph
**Graph Database**: Database optimized for storing and querying graph structures (e.g., Neo4j).

**Embedding**: Vector representation of text for similarity comparisons.

**Schema**: Structure defining entity types and relationship types.

**Entity Linking**: Connecting entity mentions to knowledge base entries.

### Module 3: Reasoning Engine
**Content Synthesis**: Generating new content by combining information from multiple sources.

**Personalization**: Tailoring content to individual user preferences and needs.

**Digest Generation**: Creating summaries of recent activity or discoveries.

**Multi-channel Publishing**: Distributing content across different platforms (email, social, web).

### Module 4: Frontend
**Server Components**: React components that render on the server.

**shadcn/ui**: Modern component library for React applications.

**Tailwind CSS**: Utility-first CSS framework.

**WebSocket**: Protocol for real-time bidirectional communication.

## Process Terms

**Research Brief**: Week 1 deliverable documenting technology choices and implementation planning.

**GitHub Issue**: Tracking mechanism for tasks, bugs, and features.

**Sprint**: Time-boxed development period (typically 1-2 weeks).

**Integration Testing**: Testing how different modules work together.

## Acronyms

- **API**: Application Programming Interface
- **CI/CD**: Continuous Integration/Continuous Deployment
- **GDPR**: General Data Protection Regulation
- **LLM**: Large Language Model
- **NLP**: Natural Language Processing
- **RAG**: Retrieval-Augmented Generation
- **REST**: Representational State Transfer
- **RSS**: Really Simple Syndication
- **UI/UX**: User Interface/User Experience