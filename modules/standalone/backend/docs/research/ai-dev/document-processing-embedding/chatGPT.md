# Option A — Single Comprehensive Prompt

**Role:** You are an AI systems specialist evaluating document preprocessing and embedding generation for retrieval-augmented generation (RAG).

**Goal:** Produce an evidence-backed playbook covering chunking strategies, metadata handling, and embedding models (local + API). Include an experiment-driven recommendation for default settings and when to deviate.

## Scope (cover both OSS and commercial)

* **Chunking & preprocessing:** fixed/windowed chunks, semantic/sentence-aware splits, sliding overlap, section/heading-aware splits, hierarchical splits; token limits; handling tables/code/figures.
* **Embeddings:** Local (e.g., SentenceTransformers, Instructor, E5, GTE, BGE) and API (e.g., OpenAI, Cohere, Azure OpenAI); model dimensions, cost, throughput, latency.
* **Metadata & indexing:** fielded metadata, doc IDs, section headers, page numbers, embeddings + BM25 hybrid, re-ranking, incremental updates.
* **Case studies:** Perplexity, Microsoft GraphRAG, Stanford STORM (focus on what they actually did for chunking/metadata/embeddings and why).
* **Open questions:** optimal chunk size/overlap, multi-format handling (PDF/HTML/JSON), code/doc math, multilingual, privacy.

## Must-Do Experiments (ablation plan)

1. **Datasets (choose 2–3):**

   * Public QA or retrieval sets (e.g., NQ, HotpotQA) **or** your domain docs (build a small gold set with \~200 Q/A pairs).
2. **Chunking grid:**

   * Sizes (tokens): 256, 512, 768, 1,024
   * Overlap (% of size): 0%, 10%, 20%, 30%
   * Splitters: sentence/semantic, fixed-token, header-aware
3. **Embedding grid (representative):**

   * **API:** OpenAI (text-embedding-3-small/large or ada-002 if legacy), Cohere (latest embed model)
   * **Local:** BGE-base/gemma-embed/gte-base/e5-base; 384–1024 dims
4. **Retrieval configs:**

   * Pure dense vs **hybrid** (BM25 + dense)
   * With/without cross-encoder re-ranker (e.g., msmarco-MiniLM-L6-v2)
5. **Metrics & logs:**

   * R\@k, nDCG\@k, MRR; query latency P50/P95; index build time; memory; \$\$ cost/1k queries; footprint on disk; ingestion throughput.

## Evidence Requirements

* Cite papers, official docs, or credible benchmarks for model specs; cite your experiment runs (seed, commit hash, config files).
* Include per-experiment JSON/CSV artifacts and command lines to reproduce.

## Deliverables

1. **Inventory of chunking + embedding methods** (what, when, trade-offs).
2. **Comparison table of embedding options** (template below).
3. **Best-practices summary** (quick-start defaults + knobs).
4. **Open challenges** (what’s still unclear + next tests).
5. **Recommendation**: default stack for small, mid, and large deployments.

## Comparison Table (fill during research)

| Model | Local/API | Dim | Tokenizer | Throughput (docs/s) | Latency P95 (ms) | Cost /1k queries | R\@5 | nDCG\@10 | Notes (domain fit, licensing) |
| ----- | --------- | --: | --------- | ------------------: | ---------------: | ---------------: | ---: | -------: | ----------------------------- |

## Best-Practices Checklist (to confirm with data)

* Start with sentence/semantic splits; **512–768 tokens** with **10–20% overlap** as a strong baseline.
* Preserve **structural metadata** (title, H1–H3, page, section) and **source pointers** for grounded citations.
* Prefer **hybrid retrieval** (BM25 + dense); add **re-ranker** for long-tail queries.
* Normalize text (unicode, de-hyphenation), keep **code/math blocks intact**; don’t strip tables—extract them to text with headers.
* **Incremental indexing:** immutable doc IDs, version field, delta upserts; background compaction.
* Cache frequent query embeddings; batch and stream ingestion.

## Evaluation Rubric

* **Accuracy/effectiveness (40%)**, **Performance/scalability (20%)**, **Ease of implementation (15%)**, **Ecosystem maturity (15%)**, **Cost (10%)**.

---

# Option B — Four Focused Prompts

## B1 — Chunking & Preprocessing

**Goal:** Find chunking defaults that maximize retrieval quality with stable latency/cost.
**Do:**

* Compare fixed token splits vs sentence/semantic vs header-aware; sizes 256–1024; overlap 0–30%.
* Measure R\@5/nDCG\@10, ingestion time, index size.
* Analyze failure cases: tables, code blocks, long lists, PDFs with OCR noise.
  **Deliverables:** Settings matrix, before/after examples, recommended defaults per doc type (PDF report, wiki page, API docs, codebase), and a “gotchas” list.

## B2 — Embeddings (Local vs API)

**Goal:** Pick 2–3 go-to models for local and API use, with clear selection rules.
**Do:**

* Benchmark representative local (BGE/GTE/E5/Instructor) vs API (OpenAI/Cohere/Azure OpenAI).
* Track dim, indexing speed, query P95, accuracy, \$\$, VRAM/RAM.
* Test multilingual and code/text mixed corpora if relevant.
  **Deliverables:** Filled comparison table, cost models, and “choose-this-model-if…” decision tree.

## B3 — Metadata & Indexing Strategy

**Goal:** Prove metadata helps retrieval and citations.
**Do:**

* Add metadata fields (title, headings, page, source URL, doc date, tags).
* Compare dense-only vs hybrid (BM25 + dense) vs hybrid + re-ranker.
* Implement incremental indexing (upserts, tombstones, versioning).
  **Deliverables:** Ablation results, example index schema, ingestion pipeline diagram, operational runbook (backfills, compaction, monitoring).

## B4 — Case Studies & Synthesis

**Goal:** Extract patterns from Perplexity, Microsoft GraphRAG, Stanford STORM.
**Do:**

* For each: document **chunking**, **metadata**, **embeddings**, **ranking**, and **why** they chose them.
* Map patterns to your findings; note divergences.
  **Deliverables:** 1-page briefs per system + a synthesis table of common patterns and where they differ.

---

## Output Package (for either option)

* **Report (10–20 pages)** with citations.
* **Artifacts:** configs, scripts, CSVs with metrics, sample indexed corpus.
* **One-pager TL;DR:** default settings, cost/latency, when to switch strategies.

## Starter Inventory (sections to fill)

* **Chunking methods:** fixed, sliding, semantic, header-aware, hierarchical; pros/cons; best doc types.
* **Embedding families:** BGE/GTE/E5/Instructor (local), OpenAI/Cohere (API); dims; licensing notes; infra needs.
* **Indexing patterns:** FAISS/HNSW/ScaNN, BM25, hybrid, cross-encoder re-rank.
* **Pipelines:** PDF/HTML/Markdown/JSON normalization, code and tables handling, OCR.

---

Want me to turn this into a runnable checklist (with experiment commands/templates) or create a comparison-table spreadsheet you can fill in as you run tests?
