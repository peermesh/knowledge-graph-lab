# 📄 Synthesis: Document Preprocessing & Embedding Generation for RAG

## 1. Fundamentals

* **Document preprocessing** is the **bedrock of RAG quality**: poor preprocessing leads to poor retrieval, regardless of the LLM.
* Pipeline steps:

  1. Extract + clean raw text (multi-format: PDF, HTML, DOCX, JSON, code).
  2. Normalize (Unicode, de-hyphenation, remove noise but keep structural cues).
  3. Chunk into retrieval units.
  4. Enrich with **metadata** (headers, section, page, source, entity tags).
  5. Generate embeddings + index into vector DB.

---

## 2. Chunking Strategies

| Strategy            | Description                                  | Pros                             | Cons                        | Best Use                  |
| ------------------- | -------------------------------------------- | -------------------------------- | --------------------------- | ------------------------- |
| **Fixed-size**      | Split by tokens/characters, with overlap     | Fast, simple                     | Breaks semantics            | Uniform docs              |
| **Recursive**       | Hierarchical split (`\n\n`, `.`, space)      | Preserves boundaries             | Still blind to meaning      | General-purpose           |
| **Semantic**        | Split using sentence embeddings & similarity | High coherence, topic-aware      | Slower, requires embeddings | Technical docs, long-form |
| **Structure-aware** | Split by headers, paragraphs, code functions | Preserves intent, easy retrieval | Needs format-specific logic | Markdown, LaTeX, PPT      |
| **Agentic**         | LLM decides splits dynamically               | Most context-aware               | High cost, experimental     | High-value corpora        |

**Best practice defaults:**

* 512–768 tokens with 10–20% overlap.
* Semantic or recursive chunking preferred over fixed.
* Multi-scale chunking (multiple granularities) for robustness.

---

## 3. Metadata Handling

* **Essential fields:** doc\_id, source, chunk\_id, title, section, page.
* **Advanced enrichment:** keywords, entities, dates, authors, recency scores.
* **Uses:**

  * Pre-filter retrieval (e.g., restrict by doc type/date).
  * Adjust scoring (boost authoritative/recent docs).
  * Incremental indexing (hash/timestamp to update only changed chunks).

---

## 4. Embedding Models

### API Models

* **OpenAI text-embedding-3-large/small**: high accuracy, scalable, cost = \$0.02–0.13 /M tokens.
* **Cohere v3**: strong multilingual, compact 1024-dim output.
* **Voyage AI**: competitive with OpenAI, high retrieval performance.

### Open Source

* **BGE-M3**: current SOTA open-source, multilingual, hybrid dense/sparse.
* **Nomic Embed v2**: efficient (768d), outperforms ada-002.
* **mxbai-embed-large**: tuned for RAG, strong retrieval.
* **SentenceTransformers (MiniLM, mpnet, E5)**: efficient baselines, tunable.

**Trade-offs:**

* Local = privacy, no per-token cost, infra heavy.
* API = easy, scalable, recurring cost, privacy risk.
* Recommendation: Hybrid approach (local for bulk, API for critical queries).

---

## 5. Frameworks

* **LangChain:** Recursive splitters, multi-format loaders, integrated with Chroma/FAISS.
* **LlamaIndex:** Semantic + hierarchical chunking, query engines.
* **Unstructured.io:** Best for PDF/HTML/complex layouts.

---

## 6. Case Studies

* **Perplexity AI:** Hybrid retrieval, aggressive metadata tagging, OpenAI embeddings; token streaming while retrieval continues.
* **Microsoft GraphRAG:** Combines vector + knowledge graph; entity/relationship extraction, community detection, multi-hop reasoning.
* **Stanford STORM:** Iterative retrieval guided by LLM-generated questions; uses semantic chunking + perspective enrichment.

---

## 7. Best Practices

1. **Chunking:** Start with 512–768 tokens, 10–20% overlap; switch to semantic/hierarchical for structured docs.
2. **Metadata:** Always attach structural + contextual metadata; use it for pre-filtering and scoring.
3. **Embeddings:** Choose based on scale/privacy; start with BGE-M3 (local) or OpenAI 3-large (API).
4. **Retrieval:** Use hybrid (dense + BM25) + re-ranking.
5. **Indexing:** Incremental, content-hash based updates.
6. **Evaluation:** Use R\@k, nDCG, MRR + latency, cost, memory.

---

## 8. Open Challenges

* **Optimal chunk size**: remains domain-dependent; dynamic/LLM-guided chunking is an active research area.
* **Multi-format docs:** retaining tables, figures, layout integrity is still hard.
* **Evaluation gaps:** retrieval vs generation disentanglement.
* **Evolving models:** rapid churn; architectures must allow easy swapping.

---

## 9. Recommendations

* **Small-scale projects:** SentenceTransformers or Nomic Embed v2 + recursive chunking.
* **Mid-scale production:** BGE-M3 (local) or OpenAI 3-small + semantic chunking.
* **Enterprise scale:** Hybrid retrieval + GraphRAG (entity-aware) + multi-modal expansion.