# 📚 Synthesis: Retrieval + Generation (RAG) Pipelines

## 1. Fundamentals

* **Workflow:** *Embed → Retrieve (top-k) → Assemble Prompt (instructions + context + citation tags) → Generate → Surface citations + metadata → Cache*.
* **Goal:** Ground LLM responses in factual context to reduce hallucinations while balancing **latency, accuracy, and cost**.
* **Core stages:**

  1. Document ingestion & chunking (semantic, overlapping windows, metadata tagging).
  2. Embedding + vectorization.
  3. Semantic similarity retrieval (dense, sparse, or hybrid).
  4. Context assembly with **prompt templates**.
  5. Generation with citations, caching, and validation.

---

## 2. Framework Landscape

| Framework                | Retrieval                                                                  | Prompting                                     | Citations                                              | Caching                                   | Ideal Use                                              |
| ------------------------ | -------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------ | ----------------------------------------- | ------------------------------------------------------ |
| **LangChain**            | Modular retrievers, hybrid (dense + BM25), reranking, ensembles.           | LCEL templating, structured outputs.          | Configurable but requires manual mapping.              | In-memory, SQLite, Redis.                 | Flexible prototyping, custom pipelines.                |
| **LlamaIndex**           | Advanced engines: similarity\_top\_k, multi-modal, hierarchical retrieval. | High-level APIs, built-in Q\&A templates.     | **Excellent**: native citation tracing, node metadata. | Ingestion/query caches, Redis.            | Document/Q\&A-centric apps, citation-critical systems. |
| **Haystack**             | Production-grade retriever→reader→generator pipelines, async support.      | DAG-based orchestration with Jinja templates. | Strong: integrates evidence into answer object.        | Multi-level cache (retrieval, docs, gen). | Enterprise-scale, monitored production.                |
| **Custom (DSPy/others)** | Full control of retriever + index.                                         | Optimize prompts and retrieval jointly.       | Manual implementation.                                 | Custom.                                   | Research or max-accuracy use cases.                    |

---

## 3. Comparative Insights

| Criterion                 | LangChain                 | LlamaIndex                          | Haystack             | Custom                  |
| ------------------------- | ------------------------- | ----------------------------------- | -------------------- | ----------------------- |
| **Answer Quality**        | High (with tuning)        | **Very High** (optimized retrieval) | High                 | **Potentially Highest** |
| **Latency**               | Medium                    | Low                                 | **Low**              | Varies                  |
| **Ease of Orchestration** | Medium (steeper curve)    | **High** (clean abstractions)       | **High** (clear DAG) | Low                     |
| **Maintainability**       | Medium (complexity grows) | **High**                            | **Very High**        | Low                     |
| **Production Readiness**  | ⭐⭐⭐⭐                      | ⭐⭐⭐⭐                                | **⭐⭐⭐⭐⭐**            | Depends on team         |

---

## 4. Best Practices

1. **Retrieval Optimization**

   * Use **hybrid search** (dense + sparse) to capture semantics and keywords.
   * Add **cross-encoder reranking** for top candidates (e.g., BGE reranker).
   * Tune **top-k** (5–10 typical); balance recall vs. latency.
   * Dynamic adjustment based on query complexity.

2. **Prompt Templates**

   * Clear **role + context + instructions** (e.g., “use only provided context; if insufficient, say so”).
   * **Citation forcing:** inline `[1]`, JSON with `{answer, citations}`, or structured outputs.
   * Optimize for **context window**: avoid overstuffing, keep relevant headers.

3. **Citation Handling**

   * Always attach **metadata** (doc\_id, URL, page, timestamp).
   * Inline, footnote, or JSON-formatted citations; ensure traceability.
   * Verification via cross-checking and confidence scoring.

4. **Caching Strategies**

   * **Embedding cache:** store vectors to avoid recomputation.
   * **Retrieval cache:** map query → ANN results.
   * **Generation cache:** store LLM responses (with context fingerprints).
   * **Semantic caching:** Redis or LangCache to reuse near-duplicate queries.

---

## 5. Case Studies

* **Perplexity AI:**

  * Hybrid retrieval + reranking.
  * Multi-layer caching for real-time latency.
  * Streaming token-level responses while retrieval finishes.
  * Parallel multi-source retrieval.

* **Microsoft GraphRAG:**

  * Builds a **knowledge graph** of entities/relations instead of flat chunks.
  * Enables **multi-hop reasoning** across docs.
  * Useful for temporal or composite queries.

---

## 6. Open Challenges

* **Multi-hop queries:** vanilla top-k struggles; GraphRAG and agent-based decomposition help.
* **Hallucination risk:** even with context → mitigate via strict citation schema, cross-verification, fallback “I don’t know” policies.
* **Caching granularity:** coarse (whole answer) vs. fine (chunks/embeddings) → trade-offs in freshness vs. performance.
* **Scalability:** vector storage cost, cache invalidation, and index maintenance at scale.
* **Evaluation:** hard to measure faithfulness/citation accuracy → combine human eval + automated metrics (e.g., LLM-as-judge, semantic similarity).

---

## 7. Recommendations

* **For prototyping:** LangChain (flexibility, experiments).
* **For production RAG systems:** LlamaIndex (clean API, strong retrieval, built-in citations).
* **For enterprise deployments:** Haystack (monitoring, reliability, DAG pipelines).
* **For research/max performance:** Custom (DSPy, reinforcement-tuned retrieval).
