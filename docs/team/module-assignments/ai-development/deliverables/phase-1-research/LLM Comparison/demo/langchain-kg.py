# kg_langchain_llm_entities.py
import os, re, json, traceback
from collections import defaultdict, Counter
from typing import List
from pydantic import BaseModel, Field

os.environ["OPENAI_API_KEY"] = 

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data-dir")
DOC_EXTS = {".txt", ".md"}

print(f"[info] BASE_DIR = {BASE_DIR}")
print(f"[info] DATA_DIR = {DATA_DIR}")

# OpenAI API key bootstrap
def ensure_openai_key():
    key = os.getenv("OPENAI_API_KEY")
    if key and key.strip():
        return
    # key.txt fallback
    key_path = os.path.join(BASE_DIR, "key.txt")
    if os.path.isfile(key_path):
        with open(key_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
        if first_line:
            os.environ["OPENAI_API_KEY"] = first_line
            print("[info] OPENAI_API_KEY loaded from key.txt")
            return
    raise RuntimeError(
        "OPENAI_API_KEY not set. Set the env var or create key.txt (first line = key)."
    )

ensure_openai_key()

# --- IO helpers ---
def iter_docs(data_dir):
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    names = [n for n in os.listdir(data_dir)
             if os.path.isfile(os.path.join(data_dir, n))
             and os.path.splitext(n)[1].lower() in DOC_EXTS]
    print(f"[info] Files found in data-dir: {names}")
    for name in names:
        p = os.path.join(data_dir, name)
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            yield name, f.read()

def sentences(text):
    return [s.strip() for s in re.split(r'[.!?]\s+', text) if s.strip()]

# --- LangChain setup (LLM + structured output) ---
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class ConceptList(BaseModel):
    concepts: List[str] = Field(
        description="Short domain keywords or phrases mentioned in the sentence"
    )

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
# Tip: if you’re using an OpenAI-compatible endpoint, set OPENAI_BASE_URL accordingly.
llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

# Use the structured output helper (tool-calling/JSON mode under the hood)
structured = llm.with_structured_output(ConceptList)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Extract domain-relevant keywords/short phrases from the sentence. "
     "Focus on RAG/LangChain/LangGraph topics (e.g., Retriever, Chroma, FAISS, LCEL, LangSmith, Tool calling)."),
    ("user", "{sentence}")
])

# Build the chain
chain = prompt | structured

# --- One-time smoke test to surface auth/model issues early ---
try:
    test_out = chain.invoke({"sentence": "FAISS retriever uses embeddings from an LLM model via LangChain."})
    print(f"[info] LLM smoke test OK → {test_out}")
except Exception as e:
    print("[error] LLM smoke test failed. Details below:\n" + "".join(traceback.format_exception_only(type(e), e)))
    raise  # fail fast so you see the real problem

# --- Build graph ---
doc_to_concepts = defaultdict(set)
concept_to_docs = defaultdict(set)
concept_cooccur = Counter()

docs_found = []
for fname, content in iter_docs(DATA_DIR):
    docs_found.append(fname)
    for sent in sentences(content):
        try:
            cl: ConceptList = chain.invoke({"sentence": sent})
            scons = sorted({c.strip().lower() for c in (cl.concepts or []) if c.strip()})
            if not scons:
                # uncomment for verbose debugging
                # print(f"[debug] No concepts extracted for sentence: {sent[:120]}...")
                pass
        except Exception as e:
            # Show a tiny snippet so you can trace which sentence fails
            short = sent.replace("\n", " ")[:160]
            print(f"[warn] Extraction failed for: \"{short}...\"\n"
                  f"       {e.__class__.__name__}: {e}")
            scons = []
        for c in scons:
            doc_to_concepts[fname].add(c)
            concept_to_docs[c].add(fname)
        # co-occurrence within sentence
        for i in range(len(scons)):
            for j in range(i + 1, len(scons)):
                a, b = scons[i], scons[j]
                concept_cooccur[(a, b)] += 1

if not docs_found:
    print("[hint] No .txt/.md files in data-dir/. Add a couple and re-run.")
    # still write an empty graph so you see the file path
else:
    print(f"[info] Processed {len(docs_found)} docs.")

# --- Save graph ---
graph = {
    "documents": sorted(doc_to_concepts.keys()),
    "concepts": sorted(concept_to_docs.keys()),
    "doc_concept_edges": [
        {"doc": d, "concept": c} for d, cs in doc_to_concepts.items() for c in cs
    ],
    "concept_concept_edges": [
        {"a": a, "b": b, "weight": w} for (a, b), w in concept_cooccur.items()
    ],
}
out_path = os.path.join(BASE_DIR, "graph-langchain-llm.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(graph, f, indent=2, ensure_ascii=False)
print(f"[info] Saved LLM-derived graph to: {out_path}")
