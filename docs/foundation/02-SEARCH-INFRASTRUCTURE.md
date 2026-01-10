# Knowledge Graph Lab: Search Infrastructure

**Version:** 1.0.0
**Created:** 2026-01-09
**Status:** Foundational (source of truth)

---

## Strategic Decision

**KGL uses general-purpose search tools, not code-specific search tools.**

Rationale: KGL indexes *knowledge about* domains (research, documentation, specifications), not the domains themselves. We're building a knowledge graph about vector databases, not parsing vector database source code.

Code-specific tools (Zoekt, OpenGrok) provide structural intelligence (symbols, cross-references, call hierarchies) that's irrelevant when treating code files as documents to understand.

---

## Code Search Tools (Secondary)

These are documented for reference. Use only when code intelligence is explicitly needed.

### Zoekt
- **License:** Apache 2.0
- **Language:** Go
- **Mechanism:** Trigram-based
- **Latency:** Sub-10ms for billion-scale repos
- **Notable:** Sourcegraph's actual search backend
- **Repo:** https://github.com/sourcegraph/zoekt
- **Use when:** Need "grep but faster" across large codebases

### OpenGrok
- **License:** CDDL
- **Language:** Java
- **Mechanism:** Lucene + AST parsing
- **Latency:** 50-200ms typical
- **Notable:** Full cross-reference, jump-to-definition, symbol navigation
- **Repo:** https://github.com/oracle/opengrok
- **Use when:** Need code intelligence (find all callers, first declaration)

### Hound
- **License:** MIT
- **Language:** Go + React
- **Mechanism:** Trigram
- **Latency:** ~50ms
- **Notable:** Simple setup, good for small-medium repos
- **Repo:** https://github.com/hound-search/hound
- **Use when:** Simple self-hosted code search

### Livegrep
- **License:** BSD
- **Language:** C++ + Go
- **Mechanism:** Trigram
- **Latency:** 10-50ms
- **Notable:** Handles tens of millions of files
- **Repo:** https://github.com/livegrep/livegrep
- **Use when:** Extreme scale, command-line workflows

### SeaGOAT
- **License:** MIT
- **Language:** Python
- **Mechanism:** Vector embeddings
- **Latency:** 100-500ms
- **Notable:** Semantic code search ("find functions that handle auth")
- **Repo:** https://github.com/kantord/SeaGOAT
- **Use when:** Need semantic understanding, not just text matching

---

## General Search Tools (Primary)

These are the tools KGL uses for knowledge indexing.

### Meilisearch ⭐ PRIMARY
- **License:** MIT
- **Language:** Rust
- **Type:** Full-text + hybrid (vector since v1.3)
- **Latency:** Sub-50ms
- **API:** REST, simple
- **Notable:** Typo-tolerance, faceted search, excellent DX
- **Repo:** https://github.com/meilisearch/meilisearch

**Why primary:** Best balance of speed, features, and developer experience. Hybrid search eliminates need for separate vector store in many cases.

### Qdrant ⭐ PRIMARY
- **License:** Apache 2.0
- **Language:** Rust
- **Type:** Vector-native
- **Latency:** Sub-20ms
- **API:** REST + gRPC
- **Notable:** Real-time updates, metadata filtering, scalar quantization
- **Repo:** https://github.com/qdrant/qdrant

**Why primary:** Best pure vector performance. Pair with Meilisearch for hybrid semantic + keyword search.

### Typesense
- **License:** GPL-3.0
- **Language:** C++
- **Type:** Full-text + vector
- **Latency:** Sub-50ms
- **API:** REST
- **Notable:** Strong faceted search, field weighting
- **Repo:** https://github.com/typesense/typesense

**Consider when:** Need stronger faceted search than Meilisearch, GPL acceptable.

### Weaviate
- **License:** BSD-3
- **Language:** Go
- **Type:** Vector + knowledge graph
- **Latency:** 50-200ms
- **API:** REST + GraphQL
- **Notable:** Built-in knowledge graph, auto-embedding modules
- **Repo:** https://github.com/weaviate/weaviate

**Consider when:** Want vector + graph in one system. More complex than Meilisearch/Qdrant combo.

### Milvus
- **License:** Apache 2.0
- **Language:** Go + C++
- **Type:** Vector-native
- **Latency:** Variable (optimized for scale)
- **API:** SDK-first
- **Notable:** Billion-scale vectors, GPU acceleration
- **Repo:** https://github.com/milvus-io/milvus

**Consider when:** Need extreme scale (1B+ vectors). Overkill for most KGL use cases.

### Chroma
- **License:** Apache 2.0
- **Language:** Python
- **Type:** Vector-native
- **Latency:** 50-100ms
- **API:** Python SDK
- **Notable:** Built for RAG, easy prototyping
- **Repo:** https://github.com/chroma-core/chroma

**Consider when:** Rapid prototyping, Python-centric workflows.

### pgvector
- **License:** PostgreSQL
- **Language:** C
- **Type:** PostgreSQL extension
- **Latency:** 50-200ms
- **API:** SQL
- **Notable:** Keep vectors in existing Postgres, ACID guarantees
- **Repo:** https://github.com/pgvector/pgvector

**Consider when:** Already using Postgres, want transactional consistency.

---

## Tool Selection Matrix

| Need | Tool | Notes |
|------|------|-------|
| Default hybrid search | Meilisearch | Full-text + vectors in one |
| Pure semantic search | Qdrant | Best vector performance |
| Code intelligence | OpenGrok | Symbols, cross-refs |
| Fast code grep | Zoekt | Sub-10ms at scale |
| Graph + vectors | Weaviate | If you need both integrated |
| Extreme scale | Milvus | 1B+ vectors |
| Quick prototype | Chroma | Python-native |
| Existing Postgres | pgvector | Extension, not separate service |

---

## KGL Default Configuration

```yaml
search:
  primary:
    - backend: meilisearch
      role: full-text, hybrid
      config:
        index: kgl_knowledge
        searchable_attributes: [title, content, summary]
        filterable_attributes: [type, source, date, confidence]
        
    - backend: qdrant
      role: semantic
      config:
        collection: kgl_embeddings
        vector_size: 1536
        distance: cosine
        
  merge_strategy: reciprocal_rank_fusion
  
  routing:
    "*.md|*.txt|*.html": [meilisearch, qdrant]
    "*.pdf": [meilisearch, qdrant]  # After text extraction
    "*.json|*.yaml": [meilisearch]   # Structured data
```

---

## Topology Observation

Code search tools provide domain-specific structural intelligence:
- First declaration of a symbol
- All callers of a function
- Class hierarchy
- Import graph

This is essentially **topology** over code. The same concept could apply to other domains:
- First mention of a term in a book
- All references to a concept
- Thematic callbacks in a narrative
- Citation graph in research

**Future direction:** KGL could develop domain-specific topology analyzers that provide "code intelligence" for non-code domains. Not blocking for current work, but worth tracking.

---

## Sourcegraph Context

Sourcegraph went proprietary in August 2024 (was Apache 2.0 since 2018). This drove the OSS alternatives analysis.

**Key insight:** Zoekt (Sourcegraph's search backend) remains Apache 2.0 and is actively maintained. The proprietary change affected the application layer, not the core search.

---

## Abstraction Layer Requirements

The search module abstraction must support:

1. **Multiple backends active simultaneously**
2. **Algorithmic merging (no LLM)**
3. **Per-query routing by content type**
4. **Normalized result format**
5. **Backend-specific config exposure**
6. **Hot-swap without restart**

```python
class SearchModule:
    backends: list[SearchBackend]
    merge_strategy: MergeStrategy
    router: SourceRouter
    
    async def search(self, query: SearchInput) -> SearchOutput:
        # Route query to appropriate backends
        routed = self.router.route(query)
        
        # Execute backends in parallel
        results = await asyncio.gather(*[
            backend.search(query) for backend in routed.backends
        ])
        
        # Merge results algorithmically
        merged = self.merge_strategy.merge(results)
        
        return SearchOutput(
            results=merged,
            backend_results=dict(zip(routed.backends, results)),
            merge_log=self.merge_strategy.log
        )
```

---

## Related Documents

- [Architecture Principles](./01-ARCHITECTURE-PRINCIPLES.md) — Multi-backend merging details
- [Research Synthesis](../research/ai-pipeline/RESEARCH-SYNTHESIS.md) — Tool validation
- [OSS Code Search Guide](../../mnt/user-data/outputs/oss-code-search-alternatives-guide.md) — Detailed comparison
