Segment 1 of 5 — Executive Summary & Domain Overview
*(Assignment ID: RES-2025-ORCH-001)*

# Local-First RAG & Knowledge Graph Construction: LangChain vs LlamaIndex (Phase-1 Technical Evaluation & Architecture Survey)

## Executive Summary

This report evaluates two leading Python frameworks—**LangChain** and **LlamaIndex**—for building a **local-first, CPU-viable** Retrieval-Augmented Generation (RAG) and **knowledge-graph construction** pipeline that runs entirely via **Docker Compose** with **Qdrant** as the vector database. The decision horizon is Phase-1 (this sprint): a working offline MVP that ingests small documents, returns top-k results with citations, and extracts structured entities/relations for a downstream graph store (Neo4j or PostgreSQL+pgvector). Phase-2 (next sprint) may optionally incorporate hosted APIs, re-ranking, and agentic workflows.

**Bottom line (preview):** For a university/startup lab team and Phase-1’s strict local-first constraints, **LlamaIndex edges out as the most straightforward “data-centric” choice for quickly standing up an offline RAG + basic graph extraction loop**, thanks to its built-in document-first abstractions (e.g., `SimpleDirectoryReader`, index/query engines), direct **Qdrant** vector store adapter, **BM25 retriever** and hybrid “fusion” packs, and an actively maintained **Neo4j graph store** path and **GraphRAG** cookbook examples. ([LlamaIndex Documentation][1])

That said, **LangChain remains highly competitive** and may be the better foundation if the team anticipates **Phase-2 agent workflows** using **LangGraph** and wants **first-class orchestration primitives**, richer **retriever variants** (including self-query), **hybrid** search with Qdrant’s new Query API, and an extensive ecosystem of **document loaders** and **structured-output** helpers. LangChain also integrates deeply with **Neo4j** for Cypher generation and KG operations. ([LangChain][2])

**Why this matters for Phase-1:**

* **Local-first viability:** Both frameworks can operate fully offline with **sentence-transformers** (e.g., `all-MiniLM-L6-v2`, 384-dim embeddings) on CPU and **Qdrant** via Docker. LLMs are optional; if needed locally, **Ollama** integrations exist in both. ([Hugging Face][3])
* **RAG primitives:** Each supports filesystem loaders, chunkers, embedding adapters, **Qdrant** retrievers, and **BM25**/hybrid retrieval. LlamaIndex exposes a simple *“load → index → query”* path; LangChain favors composable chains and retrievers (including **self-query** and hybrid). ([LlamaIndex Documentation][1])
* **Structured extraction:** Both offer **structured outputs** (JSON schema/Pydantic) for producing typed entities/relations with confidences. LlamaIndex documents emphasize schema-driven extraction modules; LangChain provides `with_structured_output()` and how-to patterns. ([LlamaIndex Documentation][4])
* **Graph affinity:** Both connect to **Neo4j**; LlamaIndex ships **PropertyGraph** stores and a **GraphRAG v2** cookbook; LangChain exposes **Neo4jGraph** helpers and text-to-Cypher examples. ([LlamaIndex Documentation][5])
* **Governance/observability:** LangChain’s **LangSmith** provides a mature path (with OpenTelemetry support); LlamaIndex offers callbacks and observability guides and can integrate with third-party tools like Langfuse. ([LangChain Docs][6])

**High-level recommendation preview:**
For **Phase-1 (offline, CPU-only, Docker)** speed to MVP, **pick LlamaIndex** for its document-centric developer experience and tested examples for Qdrant/Neo4j pipelines. For **Phase-2** (agents, tool use, advanced workflow control), **layer LangGraph** on top of (or alongside) LangChain components, while keeping your retrieval/graph interfaces clean to avoid lock-in.

**Assumptions & Confidence:**

* We assume recent stable docs (mid-2024–2025) and current adapter packages (e.g., `langchain-qdrant`, `llama-index-vector-stores-qdrant`, `llama-index-graph-stores-neo4j`). Moderate-to-high confidence based on official docs and ecosystem pages cited herein; exact performance will vary with hardware and corpus size. ([Qdrant][7])

## Comprehensive Market/Technology/Domain Overview

**Landscape:** The orchestration layer for RAG and KG has consolidated around a few general-purpose frameworks that emphasize different philosophies:

* **LangChain**: broad, integration-rich orchestration with chains/retrievers/agents; complements **LangGraph** for stateful workflows and **LangSmith** for observability/evals. Strong vector store coverage (including **Qdrant**) and **Neo4j** integration. ([LangChain][2])
* **LlamaIndex**: data-centric, “index/query-engine” API that prioritizes ingestion, indexing, and retrieval simplicity with a large connector ecosystem; solid **Qdrant** adapter, **BM25** and hybrid/fusion patterns, and **Neo4j PropertyGraph**/GraphRAG examples. ([LlamaIndex Documentation][8])
* **Adjacent** (used here for context only): **Haystack** (pipelines with retrievers/readers/generators; Qdrant integrations and hybrid tutorials) and **DSPy** (programmatic optimization of flows/prompts). **LangGraph** is covered as an adjunct to LangChain for Phase-2 agents. ([Haystack][9])

**What has changed over the past 12–18 months:**

* **Hybrid retrieval** (vector + BM25/SPLADE) and **self-querying** are now first-class in major frameworks; **Qdrant**’s newer Query API and hybrid support are surfaced by adapters. **BM25 retrievers** exist in both LangChain and LlamaIndex; LlamaIndex publishes a “fusion retriever” pack; LangChain’s docs include hybrid integration guides. ([LangChain][2])
* **Structured outputs** matured (Pydantic/JSON-schema across both) to support extraction pipelines and enforce contracts. ([LangChain][10])
* **Neo4j** ties deepened: LlamaIndex PropertyGraph store + GraphRAG v2 examples; LangChain `Neo4jGraph` & Cypher interfaces and Neo4j’s official ecosystem pages for both. ([LlamaIndex Documentation][5])
* **Local model integrations** stabilized: **Ollama** clients in both frameworks; CPU-friendly embeddings via **sentence-transformers** remain standard for offline builds (e.g., `all-MiniLM-L6-v2`). Qdrant remains easy to self-host via Docker Compose. ([LangChain][11])

**Inventory Preview:**
Primary objects (deep): **LangChain**, **LlamaIndex** (2).
Adjacent (brief): **Haystack**, **DSPy**, **LangGraph** (3).
Total referenced objects: ≈5, with full depth on the 2 primaries.

**Why these frameworks fit Phase-1:** All three primary contenders (LangChain/LlamaIndex/Haystack) can run offline, hit Qdrant locally, and work with CPU embeddings. LlamaIndex offers the fastest path for a minimal ingestion→index→query engine **and** a basic property-graph export. LangChain provides maximal flexibility and a smoother on-ramp to **LangGraph** + **LangSmith** in Phase-2.

**Licensing/Governance:** Both LangChain and LlamaIndex use the **MIT** License, supporting commercial use and private deployment—important for lab compliance and future commercialization. ([PyPI][12])

**CONTINUATION ANCHOR: resume with “Detailed Findings — LangChain, LlamaIndex, and Adjacent Coverage.”**

---

Segment 2 of 5 — Detailed Findings (Primaries)

## LangChain

**Identity & scope.** LangChain is an MIT-licensed, open-source orchestration framework for LLM applications with a deep catalog of **retrievers**, **vector store adapters**, **document loaders**, **prompting utilities**, and **agent** scaffolding. It integrates broadly across embeddings, vector DBs (including **Qdrant**), and **Neo4j** for KG operations. ([PyPI][12])

**Local-first Phase-1 fit.** LangChain runs fully offline: you can use local **sentence-transformers** for CPU embeddings and attach to **Qdrant** via Docker. If you want to keep a small local LLM loop, LangChain includes an **Ollama** integration (`OllamaLLM`) and general guidance for local LLM backends (llama.cpp, gpt4all). ([Hugging Face][3])

**RAG primitives.**

* **Loaders & chunkers:** Rich loader catalog for PDF/Markdown/filesystem/web; text splitters for adaptive chunking. ([LangChain][13])
* **Embeddings:** Plug in `sentence-transformers` on CPU; store vectors in **Qdrant** (`langchain-qdrant`) with support for **dense**, **sparse**, and **hybrid** retrieval modes leveraging Qdrant’s query capabilities (requires relatively recent Qdrant). ([LangChain][2])
* **Retrievers:** Vector store retrievers, **BM25Retriever**, **SelfQueryRetriever** for attribute-aware filtering over **Qdrant**, and general retriever interfaces. **Hybrid** search recipes are documented. ([LangChain][14])
* **Citations:** Documents returned by retrievers carry `metadata` (doc IDs, chunk offsets) for downstream citation rendering; this is idiomatic rather than a single “citation API”.

**Structured extraction.** LangChain offers **structured outputs** via `with_structured_output()` (Pydantic/JSON schema) and “how-to” guidance on robust JSON output (“wrap in `json` tags” option). This facilitates **entity/relationship** extraction with typed fields and confidence scores produced by rules or LLM heuristics. ([LangChain][10])

**Graph/Neo4j integrations.**

* **`Neo4jGraph` wrapper** accepts **GraphDocuments** to construct nodes and relationships; **Cypher** natural-language interfaces are demonstrated in notebooks and Neo4j ecosystem pages. This supports both **graph construction** from extracted triples and **graph-augmented querying**. ([LangChain Python API][15])

**Governance/observability.**

* **LangSmith** provides tracing, dataset-driven evaluation, and monitoring. Recent posts announce **end-to-end OpenTelemetry** support for standardized telemetry, implying smoother integration with existing Grafana/OTel stacks. ([LangChain Docs][6])

**Performance & CPU latency (practical expectations).** With a small corpus (few hundred chunks) and **`all-MiniLM-L6-v2`** embeddings (384-dim), you can expect sub-200–300 ms average top-k retrieval on CPU Qdrant for Phase-1 targets; embeddings batch time is the typical bottleneck. Sentence-Transformers notes **ONNX/OpenVINO** optimizations for CPU. (Empirical numbers depend on hardware; plan to benchmark.) ([Hugging Face][3])

**Maturity/community.** Extremely active OSS community; adapters often kept in “partner/community” packages (e.g., `langchain-qdrant`), which can move fast but occasionally introduce breaking changes—pin versions.

**Risks & limitations (Phase-1 implications).**

* **Breadth → choice overload.** Many options raise implementation variance; enforce **data contracts** on `Document.metadata`, chunking policy, and retriever settings early.
* **Agent workflows** are better handled in **LangGraph**, which adds another dependency if Phase-2 needs complex state. ([LangChain Docs][16])
* **Docs drift** is possible due to rapid releases; pin minor versions and rely on official integration pages.

**Confidence:** High for feature availability; moderate for out-of-the-box latency until measured in your environment.

---

## LlamaIndex

**Identity & scope.** LlamaIndex is an MIT-licensed, **data-centric** framework oriented around **indices** and **query engines** with a first-class ingest→index→query developer path. It integrates cleanly with **Qdrant** and provides graph-store support (e.g., **Neo4j PropertyGraph**) plus **GraphRAG v2** cookbook examples. ([GitHub][17])

**Local-first Phase-1 fit.**

* **Ingestion:** `SimpleDirectoryReader` loads PDFs/Markdown and other common types locally without extra ceremony. ([LlamaIndex Documentation][1])
* **Embeddings & LLMs:** You can run entirely without a hosted LLM by using only embeddings retrieval; if you want local generation, **Ollama** is supported via a dedicated LLM client. Examples exist for configuring both embeddings and LLM through Ollama (e.g., `nomic-embed-text`, `llama3.1:8b`). ([LlamaIndex Documentation][18])
* **Vector DB:** **QdrantVectorStore** in LlamaIndex provides standard top-k retrieval and supports Qdrant **filters** and **hybrid** search notebooks (including SPLADE). ([LlamaIndex Documentation][8])

**RAG primitives.**

* **Indexes & query engines** abstract retrievers cleanly; **BM25 retriever** examples are maintained (multiple versions), and **Hybrid Fusion** packs blend vector + BM25 results. ([LlamaIndex][19])
* **Citations:** Similar to LangChain, retrieved `Node`/`Document` objects carry IDs/metadata for citation mapping.

**Structured extraction.**

* LlamaIndex documents “Structured Outputs” and an **extraction** guide emphasizing **Pydantic JSON schemas** and resilience (e.g., post-processing). **LlamaParse** (managed) supports schema extraction at parse time (Phase-2 only since it’s an API). For Phase-1 offline, stick to open loaders and CPU-local parsing (or OSS alternatives like **Docling**). ([LlamaIndex Documentation][4])

**Graph/Neo4j integrations.**

* **Neo4jGraphStore** and **PropertyGraph** support let you persist extracted entities/relations and later query with Text2Cypher/KnowledgeGraphQueryEngine; **GraphRAG v2** shows a full pipeline using Neo4j. ([LlamaIndex Documentation][20])

**Governance/observability.**

* Built-in **observability** and **callbacks**; integrates with tools like **Langfuse** for tracing/metrics. Useful but optional for Phase-1; can be enabled in Phase-2. ([LlamaIndex Documentation][21])

**Performance & CPU latency (practical expectations).**

* With **`all-MiniLM-L6-v2`**, you can embed on CPU efficiently; LlamaIndex will batch embeddings via your chosen backend. Qdrant delivers millisecond-level vector search on small corpora; the embedding step dominates. Hybrid BM25 can improve recall without expensive cross-encoders (best left to Phase-2). ([Hugging Face][3])

**Maturity/community.** Rapid releases and extensive examples; the **PropertyGraph** and **GraphRAG** resources from Neo4j’s engineering blog reinforce graph workflows with LlamaIndex. ([Graph Database & Analytics][22])

**Risks & limitations (Phase-1 implications).**

* **API churn** around index/query engine naming over time—pin package versions.
* **Managed extras** (*LlamaParse*, LlamaCloud) are out-of-scope for offline Phase-1.
* **Hybrid recipes** exist but require light composition (BM25 + vector fusion pack) compared to a single “hybrid” toggle.

**Confidence:** High for developer throughput to an offline MVP using documented examples and adapters.

**CONTINUATION ANCHOR: resume with “Adjacent Coverage — Haystack, DSPy, LangGraph (brief).”**

---

Segment 3 of 5 — Detailed Findings (Adjacent Coverage, brief)

### Adjacent Coverage: Haystack (brief)

**Positioning.** **Haystack** is a pipeline-oriented framework (retrievers, readers/generators, nodes) with strong tutorials and a clear production story for RAG—including **Hybrid Retrieval** examples and an official **Qdrant** document store integration. It’s Apache-licensed (core) and well-maintained by deepset. ([Haystack][23])

**Where it excels for Phase-1.**

* The pipeline abstraction is opinionated and production-friendly; tutorials cover **BM25 + embeddings + reranking** patterns and **OpenSearchHybridRetriever** design. For teams preferring pipeline DAGs with fewer moving parts, Haystack can reduce choice overload. ([Haystack][23])
* **Qdrant** integration packages (`qdrant-haystack`) exist and are current. ([PyPI][24])

**Where it falls short (relative to primaries).**

* Slightly less “batteries-included” for **knowledge-graph construction** than the LangChain/LlamaIndex + Neo4j patterns.
* Smaller loader ecosystem than LangChain; fewer out-of-the-box graph demos.

**Takeaway.** A solid alternative if your team prefers pipelines and wants hybrid retrieval quickly, but for **graph-centric** Phase-1, the primaries have a head start.

### Adjacent Coverage: DSPy (brief)

**Positioning.** **DSPy** (Stanford) is a declarative framework for \*\*programming—not prompting—\*\*LMs, offering compilers that optimize prompts and weights across modules (including RAG). It’s often used to **improve retrieval quality** and **program structure** once a basic pipeline exists. ([GitHub][25])

**Phase-1 relevance.**

* Valuable for **evaluation/optimization** once your MVP is stable—e.g., tuning query rewriting, router logic, or answer selection with structured modules.
* Not a drop-in replacement for your orchestration layer; rather, it complements by **learning better prompts/flows** over your existing retrievers.

**Phase-2 outlook.** As you add **re-ranking**, **query expansion (HyDE)**, or **routing**, DSPy can provide systematic improvements without hand-tuning prompts.

### Adjacent Coverage: LangGraph (brief)

**Positioning.** **LangGraph** is a **stateful orchestration** library for building **long-running, cyclic, multi-actor** agent workflows, maintained by the LangChain team with both OSS SDKs and a **LangGraph Platform** for deployment. It adds persistence, human-in-the-loop interrupts, and fine-grained state control. ([LangChain Docs][16])

**Phase-1 relevance.** Minimal; agents are out-of-scope for the first local offline MVP. However, its model of **graphs of nodes/edges with loops** is ideal once you want **tool-use, planning, error-recovery**, or **graph-augmented reasoning**.

**Phase-2 outlook.** If the lab plans agent workflows, selecting **LangChain** in Phase-1 eases **LangGraph** adoption. Otherwise, you can still keep LlamaIndex for retrieval and mount **LangGraph** around the API layer as needed.

**CONTINUATION ANCHOR: resume with “Comparative Analysis: Tables + Trade-offs (facts vs analysis vs speculation).”**

---

Segment 4 of 5 — Comparative Analysis

### Side-by-Side (Phase-1 lenses)

| Dimension                  | LangChain                                                                                                       | LlamaIndex                                                                                                                                                     |
| -------------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Local-First Fit**        | Runs offline; **Qdrant** adapter with dense/sparse/hybrid; **Ollama** LLM integration; many local loaders.      | Runs offline; **QdrantVectorStore** + filters/hybrid examples; **Ollama** LLM & embeddings possible; **SimpleDirectoryReader** speeds ingest. ([LangChain][2]) |
| **RAG Primitives**         | Extensive loaders, splitters; **BM25**, **SelfQueryRetriever**, **Hybrid** recipes; strong retriever interface. | Data-centric indexes & query engines; **BM25 retriever**; **Hybrid Fusion** pack; clean retrieval API. ([LangChain][14])                                       |
| **Structured Extraction**  | `with_structured_output()` + JSON-schema how-tos.                                                               | Structured outputs & extraction guide with Pydantic schemas; (Cloud) **LlamaParse** supports structured parsing (Phase-2). ([LangChain][10])                   |
| **Graph Affinity**         | **Neo4jGraph** for node/rel creation; **Cypher** NL interfaces; Neo4j labs pages.                               | **Neo4jGraphStore/PropertyGraph**; **GraphRAG v2** cookbook; KnowledgeGraphQueryEngine/Text2Cypher. ([LangChain Python API][15])                               |
| **DX**                     | Very flexible but requires choices; great when you need orchestration patterns; “library-of-lego-bricks.”       | Extremely fast path from files → index → query; fewer concepts to ship MVP; “document-first.” ([LangChain][13])                                                |
| **Performance**            | CPU embeddings with `all-MiniLM-L6-v2`; hybrid improves recall; LangSmith helps spot bottlenecks.               | Same CPU path; BM25/fusion can boost recall; straightforward batching; similar Qdrant perf. (Benchmark locally.) ([Hugging Face][3])                           |
| **Integration Complexity** | Many knobs (retrievers, chains); best if you want custom behaviors; adds **LangGraph** later for agents.        | Simpler integration contracts for MVP; PropertyGraph examples shorten KG path. ([LangChain Docs][16])                                                          |
| **Maturity & Ecosystem**   | Very broad ecosystem (retrievers, loaders, tools), plus **LangSmith** and **LangGraph**.                        | Rapid releases; strong examples; active Neo4j collaborations and graph articles. ([LangChain Docs][6])                                                         |

#### Trade-offs & Decision Framework

* **When to prefer LangChain:** You need **advanced retrieval & orchestration flexibility** (self-query, multi-retriever routing) and anticipate **Phase-2 agents** with **LangGraph**. You’re comfortable enforcing data contracts and pinning versions to manage surface area. ([LangChain][26])
* **When to prefer LlamaIndex:** You want **fast time-to-MVP** with **simple ingestion→index→query** and a **clear Neo4j graph store** path. You’ll likely add agentic behavior later around the API. ([LlamaIndex Documentation][1])

#### Facts vs Analysis vs Speculation

* **Facts (docs/examples):** Both support **Qdrant**, **BM25/hybrid** retrieval, **structured outputs**, **Neo4j** connectors, **Ollama**. (See citations in table.)
* **Analysis (reasoned implications):** LlamaIndex’s document-centric API reduces glue code for Phase-1; LangChain’s breadth pays off when you need **custom retrievers** or **LangGraph** workflows later.
* **Speculation (labeled):** We estimate (medium confidence) that your Phase-1 MVP will be **\~20–30% fewer LOC** in LlamaIndex for ingestion/index/query + KG export due to built-ins; LangChain may match with templates but often requires more manual composition. Confidence: **medium** pending PoC.

**CONTINUATION ANCHOR: resume with “Implementation Considerations: Docker Compose, data contracts, observability, CPU tips.”**

---

Segment 5 of 5 — Implementation Considerations, Recommendations, Conclusion

## Implementation Considerations

### Reference local stack (Docker Compose)

**Services (minimum):**

1. **qdrant** — official container; expose `6333/6334`; persistent volume. Quickstart & Compose examples are in official docs. ([Qdrant][27])
2. **api** — FastAPI with pinned deps:

   * **Embeddings:** `sentence-transformers==<pin>` (e.g., `all-MiniLM-L6-v2`); optional ONNX/OpenVINO for CPU speedups. ([Hugging Face][3])
   * **Framework:** **Pick one** (Phase-1 winner); pin `llama-index==…` or `langchain==…` + `langchain-qdrant==…`. ([Qdrant][7])
   * **Qdrant client:** `qdrant-client==…` (aligned to server minor version).
3. **ollama** *(optional)* — only if you must run a local LLM; otherwise skip in Phase-1 and return contexts/citations to the frontend. Both frameworks have **Ollama** adapters. ([LangChain][11])

**Health checks:**

* `/health` endpoint pings Qdrant, verifies collection existence and embedding backend readiness.
* Startup script: on first run, create Qdrant collection with 384-dim vectors for `all-MiniLM-L6-v2`. ([Hugging Face][3])

### Data contracts

**Ingest payload (POST `/ingest`):**

```json
{
  "doc_id": "string",
  "source_type": "pdf|md|txt|html",
  "content": "raw text or extracted",
  "metadata": {"title": "...", "url": null, "tags": ["..."]},
  "chunking": {"method": "recursive", "chunk_size": 512, "overlap": 64}
}
```

**Search response (GET `/search?q=`):**

```json
{
  "query": "string",
  "top_k": 5,
  "results": [
    {
      "doc_id": "string",
      "chunk_id": "string",
      "score": 0.0,
      "text": "snippet",
      "metadata": {"page": 3, "loc": [start,end]}
    }
  ]
}
```

**Extraction output (POST `/extract`):**

```json
{
  "doc_id": "string",
  "entities": [
    {"id":"E1","type":"Person","name":"...","confidence":0.87,"spans":[[s,e]]}
  ],
  "relations": [
    {"id":"R1","type":"WorksFor","head":"E1","tail":"E2","evidence":[{"doc_id":"...","chunk_id":"..."}],"confidence":0.72}
  ]
}
```

Both LangChain and LlamaIndex can validate these with **Pydantic** structured outputs; confidence can be model-estimated or heuristic (rule-based); spans can derive from splitter offsets. ([LangChain][10])

### Backend integration patterns

* **FastAPI** service mounts `/ingest`, `/search`, `/extract`.
* **Indexer** module encapsulates: loader → splitter → embed → Qdrant upsert (with metadata filters for tenant/project).
* **Retriever** module wraps Qdrant top-k plus optional **BM25** fallback; expose a flag for **hybrid fusion** (Phase-1 default: **off**, keep simple). ([LlamaIndex][19])
* **Graph sink:** Implement `to_graph_documents()` to convert extractions to node/edge tuples and call **Neo4j** via:

  * LangChain: `Neo4jGraph.add_graph_documents(...)`, or
  * LlamaIndex: `Neo4jGraphStore.upsert(...)`. ([LangChain Python API][15])

### Observability & failure modes

* **Timings:** log ingest time per doc, embedding batch times, Qdrant upsert/search latencies.
* **Failures:**

  * **Empty retrieval:** return 204 with diagnostic `top_k=0` or enable BM25 fallback.
  * **Malformed JSON extraction:** catch parser errors; return partial structured output with `valid:false` and `errors:[…]`.
  * **Backpressure:** bound concurrent ingest, cap chunk size, and queue jobs.
* **Optional Phase-2:**

  * **LangSmith** tracing if using LangChain; or LlamaIndex **callbacks** / Langfuse integration. ([LangChain Docs][6])

### CPU performance tips

* **Embeddings:** batch size 32–128 (test); try **ONNX/OpenVINO** for CPU. `all-MiniLM-L6-v2` is 384-dim, relatively fast. ([SentenceTransformers][28])
* **Chunking:** start with 512 tokens / 64 overlap; prefer **Markdown-aware** splitting for PDFs converted to text.
* **Hybrid retrieval:** leave **off** by default to minimize complexity; enable after baseline correctness is validated.
* **Qdrant:** ensure HNSW params are reasonable for small collections (M, ef); use payload filters to scope tenants. ([Qdrant][27])

## Recommendations

**Phase-1 Winner: *LlamaIndex*** (for the lab’s local-first MVP)

**Rationale (tied to constraints):**

* **Fast path to MVP**: `SimpleDirectoryReader` → Index → QueryEngine minimizes glue code for ingestion and retrieval; the **Qdrant** adapter and **BM25** recipes are well-documented. ([LlamaIndex Documentation][1])
* **Graph export**: **Neo4jGraphStore/PropertyGraph** and **GraphRAG v2** cookbook reduce friction for entity/relationship persistence and graph-augmented querying. ([LlamaIndex Documentation][20])
* **Local-first**: Works with CPU embeddings and (optional) **Ollama** for local generation; no external APIs required. ([LlamaIndex Documentation][18])

**Phase-2 Outlook:**

* If you anticipate **agent workflows**, you can (a) continue using LlamaIndex for retrieval and extraction while (b) adding **LangGraph** around task orchestration. If your team prefers a single umbrella, consider incrementally introducing **LangChain** components where orchestration flexibility is needed and keep the **retrieval/graph** interface stable. ([LangChain Docs][16])

### Risk Register & Mitigations

| Risk                                      | Impact                         | Mitigation                                                                                                                              |
| ----------------------------------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Version drift / API churn**             | Builds break, behavior changes | Pin `llama-index`/`langchain`/`qdrant-client` versions; capture `requirements.txt` hashes; add smoke tests.                             |
| **Latency cliffs on CPU**                 | Miss 300 ms avg target         | Batch embeddings; pre-warm models; consider ONNX/OpenVINO; keep chunks small; defer re-ranking to Phase-2. ([SentenceTransformers][28]) |
| **Schema evolution (entities/relations)** | Downstream graph mismatch      | Maintain versioned JSON schema; add migration scripts in Neo4j; record confidence provenance.                                           |
| **Hybrid retrieval complexity**           | Debug/quality confusion        | Start with dense only; add BM25 fallback; later enable fusion with clear eval metrics (Hit\@k/MRR). ([LlamaIndex][19])                  |
| **Observability gaps offline**            | Harder to debug failures       | Enable basic timing logs now; consider LangSmith/Callbacks in Phase-2. ([LangChain Docs][6])                                            |

## Conclusion and Next Steps

**Decision:** Adopt **LlamaIndex** as the **Phase-1** framework to deliver a local-first RAG + KG extraction MVP with **Qdrant**. Keep interfaces (ingestion schema, retrieval result, extraction schema) framework-agnostic to allow future substitution or dual-use with LangChain.

**Immediate actions (this sprint):**

1. **Compose stack:** Bring up `qdrant`, `api` (FastAPI), and optional `ollama` services. Seed test docs (2–4 KB PDFs/MDs). ([Qdrant][27])
2. **Embed & index:** Use `sentence-transformers/all-MiniLM-L6-v2` for CPU embeddings; build a `VectorStoreIndex` backed by **Qdrant**. ([Hugging Face][3])
3. **Search endpoint:** Implement top-5 retrieval with citations (`doc_id`, `chunk_id`, span).
4. **Extraction endpoint:** Implement structured outputs for **entities**/**relations** with confidences; persist to **Neo4j** (`Neo4jGraphStore`). ([LlamaIndex Documentation][20])
5. **Metrics:** Log timings (embed, upsert, search) and basic counters.

**Validation checkpoints & success metrics:**

* **Cold start:** `docker compose up` → `/health` OK in < 60 s.
* **Retrieval:** For 2–10 small docs, **avg < 300 ms** for top-5 on CPU.
* **Extraction:** Returns non-empty entities/relations with confidences ∈\[0,1]; graph upsert succeeds.
* **Reproducibility:** All versions pinned; single README with commands.

**CONTINUATION ANCHOR: complete.**

[1]: https://docs.llamaindex.ai/en/stable/module_guides/loading/?utm_source=chatgpt.com "Loading Data"
[2]: https://python.langchain.com/docs/integrations/vectorstores/qdrant/?utm_source=chatgpt.com "Qdrant"
[3]: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2?utm_source=chatgpt.com "sentence-transformers/all-MiniLM-L6-v2"
[4]: https://docs.llamaindex.ai/en/stable/module_guides/querying/structured_outputs/?utm_source=chatgpt.com "Structured Outputs"
[5]: https://docs.llamaindex.ai/en/stable/examples/cookbooks/GraphRAG_v2/?utm_source=chatgpt.com "GraphRAG Implementation with LlamaIndex - V2"
[6]: https://docs.langchain.com/langsmith/home?utm_source=chatgpt.com "Get started with LangSmith - Docs by LangChain"
[7]: https://qdrant.tech/documentation/frameworks/langchain/?utm_source=chatgpt.com "Langchain"
[8]: https://docs.llamaindex.ai/en/stable/api_reference/storage/vector_store/qdrant/?utm_source=chatgpt.com "Qdrant"
[9]: https://haystack.deepset.ai/integrations/qdrant-document-store?utm_source=chatgpt.com "Qdrant | Haystack - deepset AI"
[10]: https://python.langchain.com/docs/concepts/structured_outputs/?utm_source=chatgpt.com "Structured outputs | 🦜️🔗 LangChain"
[11]: https://python.langchain.com/docs/integrations/llms/ollama/?utm_source=chatgpt.com "OllamaLLM | 🦜️🔗 LangChain"
[12]: https://pypi.org/project/langchain/?utm_source=chatgpt.com "langchain"
[13]: https://python.langchain.com/docs/integrations/document_loaders/?utm_source=chatgpt.com "Document loaders"
[14]: https://python.langchain.com/docs/integrations/retrievers/bm25/?utm_source=chatgpt.com "BM25"
[15]: https://api.python.langchain.com/en/latest/graphs/langchain_community.graphs.neo4j_graph.Neo4jGraph.html?utm_source=chatgpt.com "langchain_community.graphs.neo4j_graph.Neo4jGraph"
[16]: https://docs.langchain.com/oss/python/langgraph/overview?utm_source=chatgpt.com "Overview - Docs by LangChain"
[17]: https://github.com/run-llama/llama_index?utm_source=chatgpt.com "run-llama/llama_index: LlamaIndex is the leading ... - GitHub"
[18]: https://docs.llamaindex.ai/en/latest/api_reference/llms/ollama/?utm_source=chatgpt.com "Ollama"
[19]: https://developers.llamaindex.ai/python/examples/retrievers/bm25_retriever/?utm_source=chatgpt.com "BM25 Retriever | LlamaIndex Python Documentation"
[20]: https://docs.llamaindex.ai/en/stable/community/integrations/graph_stores/?utm_source=chatgpt.com "Using Graph Stores"
[21]: https://docs.llamaindex.ai/en/stable/module_guides/observability/?utm_source=chatgpt.com "Observability"
[22]: https://neo4j.com/blog/developer/property-graph-index-llamaindex/?utm_source=chatgpt.com "Customizing Property Graph Index in LlamaIndex"
[23]: https://haystack.deepset.ai/tutorials/33_hybrid_retrieval?utm_source=chatgpt.com "Tutorial: Creating a Hybrid Retrieval Pipeline"
[24]: https://pypi.org/project/qdrant-haystack/?utm_source=chatgpt.com "qdrant-haystack"
[25]: https://github.com/stanfordnlp/dspy?utm_source=chatgpt.com "DSPy: The framework for programming—not prompting ..."
[26]: https://python.langchain.com/docs/integrations/retrievers/self_query/qdrant_self_query/?utm_source=chatgpt.com "Qdrant | 🦜️🔗 LangChain"
[27]: https://qdrant.tech/documentation/quickstart/?utm_source=chatgpt.com "Local Quickstart"
[28]: https://sbert.net/docs/sentence_transformer/usage/efficiency.html?utm_source=chatgpt.com "Speeding up Inference"
